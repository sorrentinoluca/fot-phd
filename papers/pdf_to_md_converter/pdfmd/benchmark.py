from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import csv
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
from time import perf_counter
from typing import Callable

from .images import atomic_write_text, find_markdown_images
from .reporting import format_bytes, format_duration, path_size


BACKENDS = ("pymupdf4llm", "marker", "docling")


@dataclass
class BenchmarkResult:
    pdf: str
    backend: str
    succeeded: bool
    elapsed_seconds: float
    markdown_bytes: int = 0
    artifact_bytes: int = 0
    characters: int = 0
    headings: int = 0
    tables: int = 0
    image_references: int = 0
    image_placeholders: int = 0
    display_math_blocks: int = 0
    error: str = ""
    output_markdown: str = ""


def package_version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def structural_metrics(markdown: str) -> dict[str, int]:
    return {
        "characters": len(markdown),
        "headings": len(
            re.findall(r"(?m)^#{1,6}[ \t]+\S", markdown)
        ),
        "tables": len(
            re.findall(
                r"(?m)^\s*\|?\s*:?-{3,}:?\s*"
                r"(?:\|\s*:?-{3,}:?\s*)+\|?\s*$",
                markdown,
            )
        ),
        "image_references": len(find_markdown_images(markdown)),
        "image_placeholders": markdown.count("<!-- image -->"),
        "display_math_blocks": (
            markdown.count("$$") // 2
            + markdown.count(r"\[")
        ),
    }


def convert_with_pymupdf4llm(pdf: Path, output_dir: Path) -> Path:
    try:
        import pymupdf4llm
    except ImportError as error:
        raise RuntimeError(
            "Install the benchmark backend with: "
            "python -m pip install pymupdf4llm"
        ) from error

    image_dir = output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    markdown = pymupdf4llm.to_markdown(
        str(pdf),
        write_images=True,
        image_path=str(image_dir),
        image_format="png",
        dpi=200,
        force_text=False,
        show_progress=False,
    )
    for absolute_prefix in {
        str(image_dir) + os.sep,
        image_dir.as_posix() + "/",
    }:
        markdown = markdown.replace(absolute_prefix, "images/")
    output = output_dir / f"{pdf.stem}.md"
    atomic_write_text(output, markdown)
    return output


def convert_with_marker(pdf: Path, output_dir: Path) -> Path:
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered
    except ImportError as error:
        raise RuntimeError(
            "Install the benchmark backend with: "
            "python -m pip install marker-pdf"
        ) from error

    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(str(pdf))
    markdown, _, images = text_from_rendered(rendered)

    for raw_name, image in (images or {}).items():
        name = Path(str(raw_name)).name
        destination = output_dir / name
        if hasattr(image, "save"):
            image.save(destination)
        elif isinstance(image, bytes):
            destination.write_bytes(image)

    # Marker references the names returned in `images`; keep its Markdown
    # unchanged so the benchmark measures the backend's native output.
    output = output_dir / f"{pdf.stem}.md"
    atomic_write_text(output, markdown)
    return output


def convert_with_docling(pdf: Path, output_dir: Path) -> Path:
    try:
        from docling.document_converter import DocumentConverter
        from docling_core.types.doc import ImageRefMode
    except ImportError as error:
        raise RuntimeError(
            "Install the benchmark backend with: "
            "python -m pip install docling"
        ) from error

    result = DocumentConverter().convert(pdf)
    output = output_dir / f"{pdf.stem}.md"
    result.document.save_as_markdown(
        output,
        artifacts_dir=output_dir / "images",
        image_mode=ImageRefMode.REFERENCED,
    )
    return output


CONVERTERS: dict[str, Callable[[Path, Path], Path]] = {
    "pymupdf4llm": convert_with_pymupdf4llm,
    "marker": convert_with_marker,
    "docling": convert_with_docling,
}


def collect_pdfs(inputs: list[Path]) -> list[Path]:
    pdfs: list[Path] = []
    for item in inputs:
        resolved = item.expanduser().resolve()
        if resolved.is_dir():
            pdfs.extend(
                child.resolve()
                for child in resolved.glob("*.pdf")
                if child.is_file()
            )
        elif resolved.is_file() and resolved.suffix.lower() == ".pdf":
            pdfs.append(resolved)
        else:
            raise ValueError(f"Not a PDF or directory containing PDFs: {item}")

    unique = sorted(set(pdfs), key=lambda path: str(path).lower())
    if not unique:
        raise ValueError("No PDF files were found in the supplied inputs.")
    return unique


def run_one(
    pdf: Path,
    backend: str,
    benchmark_dir: Path,
    overwrite: bool,
) -> BenchmarkResult:
    output_dir = benchmark_dir / pdf.stem / backend
    if output_dir.exists():
        if not overwrite:
            return BenchmarkResult(
                pdf=pdf.name,
                backend=backend,
                succeeded=False,
                elapsed_seconds=0.0,
                error=(
                    f"Output exists: {output_dir}. Use --overwrite to replace it."
                ),
            )
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    started = perf_counter()
    try:
        markdown_path = CONVERTERS[backend](pdf, output_dir)
        markdown = markdown_path.read_text(encoding="utf-8")
        metrics = structural_metrics(markdown)
        return BenchmarkResult(
            pdf=pdf.name,
            backend=backend,
            succeeded=True,
            elapsed_seconds=perf_counter() - started,
            markdown_bytes=markdown_path.stat().st_size,
            artifact_bytes=path_size(output_dir),
            output_markdown=str(markdown_path),
            **metrics,
        )
    except Exception as error:
        return BenchmarkResult(
            pdf=pdf.name,
            backend=backend,
            succeeded=False,
            elapsed_seconds=perf_counter() - started,
            artifact_bytes=path_size(output_dir),
            error=f"{type(error).__name__}: {error}",
        )


def write_human_scorecard(
    path: Path,
    pdfs: list[Path],
    backends: list[str],
) -> None:
    if path.exists():
        return
    with path.open("w", encoding="utf-8", newline="") as score_file:
        writer = csv.writer(score_file)
        writer.writerow(
            [
                "pdf",
                "backend",
                "reading_order_1_to_5",
                "equations_1_to_5",
                "tables_1_to_5",
                "figures_1_to_5",
                "captions_1_to_5",
                "overall_1_to_5",
                "notes",
            ]
        )
        for pdf in pdfs:
            for backend in backends:
                writer.writerow([pdf.name, backend, "", "", "", "", "", "", ""])


def markdown_report(
    *,
    results: list[BenchmarkResult],
    versions: dict[str, str],
    scorecard_path: Path,
) -> str:
    lines = [
        "# PDF-to-Markdown backend benchmark",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Measured structural counts are diagnostics, not quality scores. Complete "
        f"`{scorecard_path.name}` while comparing each output with its PDF before "
        "selecting a default backend.",
        "",
        "## Environment",
        "",
        "| Component | Version |",
        "| --- | --- |",
    ]
    lines.extend(f"| {name} | {version} |" for name, version in versions.items())
    lines.extend(
        [
            "",
            "## Results",
            "",
            "| PDF | Backend | Status | Time | Markdown | Artifacts | "
            "Headings | Tables | Images | Math blocks |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in results:
        status = "ok" if item.succeeded else f"failed: {item.error}"
        lines.append(
            f"| {item.pdf} | {item.backend} | {status} | "
            f"{format_duration(item.elapsed_seconds)} | "
            f"{format_bytes(item.markdown_bytes)} | "
            f"{format_bytes(item.artifact_bytes)} | {item.headings} | "
            f"{item.tables} | {item.image_references} "
            f"(+{item.image_placeholders} placeholders) | "
            f"{item.display_math_blocks} |"
        )
    lines.extend(
        [
            "",
            "## Decision rule",
            "",
            "Do not change the converter's default backend from these counts alone. "
            "Use the human scorecard, pay particular attention to reading order, "
            "equations, tables, figure/caption pairing, and then compare elapsed "
            "time and disk use among outputs that meet the required quality.",
            "",
        ]
    )
    return "\n".join(lines)


def run_benchmark(
    *,
    inputs: list[Path],
    output_dir: Path,
    backends: list[str],
    overwrite: bool,
) -> tuple[list[BenchmarkResult], Path]:
    pdfs = collect_pdfs(inputs)
    invalid = sorted(set(backends) - set(BACKENDS))
    if invalid:
        raise ValueError(f"Unknown backend(s): {', '.join(invalid)}")

    benchmark_dir = output_dir.expanduser().resolve()
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    results = [
        run_one(pdf, backend, benchmark_dir, overwrite)
        for pdf in pdfs
        for backend in backends
    ]

    versions = {
        "Python": os.sys.version.split()[0],
        "pymupdf4llm": package_version("pymupdf4llm"),
        "marker-pdf": package_version("marker-pdf"),
        "docling": package_version("docling"),
    }
    raw_report = benchmark_dir / "benchmark_results.json"
    atomic_write_text(
        raw_report,
        json.dumps(
            {
                "generated_at": datetime.now().astimezone().isoformat(),
                "versions": versions,
                "results": [asdict(item) for item in results],
            },
            indent=2,
        ),
    )
    scorecard = benchmark_dir / "human_quality_scorecard.csv"
    write_human_scorecard(scorecard, pdfs, backends)
    report = benchmark_dir / "benchmark_report.md"
    atomic_write_text(
        report,
        markdown_report(
            results=results,
            versions=versions,
            scorecard_path=scorecard,
        ),
    )
    return results, report

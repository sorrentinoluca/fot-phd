from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import os
import shlex
from typing import Any

IMAGE_EXTENSIONS = {
    ".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"
}


@dataclass
class ImageHandlingRecord:
    filename: str
    status: str
    details: str
    content_from_cache: bool = False
    file_size_bytes: int = 0
    chart_probability: float | None = None
    image_path: Path | None = None
    image_reference: str = ""
    markdown_image: str = ""
    surrounding_text: str = ""
    occurrence_index: int = -1
    clip_classification: str = ""


@dataclass
class ModelCacheUsage:
    model_name: str
    path: Path
    size_before_bytes: int
    size_after_bytes: int


@dataclass
class StorageReport:
    input_pdf: Path
    output_file: Path
    image_folder: Path
    cache_file: Path
    input_pdf_bytes: int
    markdown_bytes: int
    image_folder_bytes: int
    extracted_image_count: int
    extracted_image_bytes: int
    cache_bytes: int
    artifacts_before_bytes: int
    artifacts_after_bytes: int
    model_caches: list[ModelCacheUsage] = field(default_factory=list)


@dataclass
class OpenAIAnalysisResult:
    text: str
    figure_type: str = "unknown"
    clip_agreement: str = "uncertain"
    one_line_finding: str = "No concise finding was returned."
    uncertainty: str = "Not specified."
    table_extracted: bool = False
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    image_bytes_submitted: int = 0
    image_was_resized: bool = False

    def to_cache_entry(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "figure_type": self.figure_type,
            "clip_agreement": self.clip_agreement,
            "one_line_finding": self.one_line_finding,
            "uncertainty": self.uncertainty,
            "table_extracted": self.table_extracted,
        }

    @classmethod
    def from_cache_entry(cls, entry: Any) -> "OpenAIAnalysisResult":
        if not isinstance(entry, dict):
            raise ValueError("Cached OpenAI analysis has an unsupported format.")
        return cls(
            text=str(entry.get("text", "")).strip(),
            figure_type=str(entry.get("figure_type", "unknown")).strip(),
            clip_agreement=str(
                entry.get("clip_agreement", "uncertain")
            ).strip(),
            one_line_finding=str(
                entry.get(
                    "one_line_finding",
                    "No concise finding was returned.",
                )
            ).strip(),
            uncertainty=str(
                entry.get("uncertainty", "Not specified.")
            ).strip(),
            table_extracted=bool(entry.get("table_extracted", False)),
        )


@dataclass
class APIReviewRecord:
    filename: str
    chart_probability: float | None
    before_details: str
    after_details: str
    elapsed_seconds: float
    content_from_cache: bool = False
    succeeded: bool = False


@dataclass
class APIReviewSummary:
    threshold_percent: float
    records: list[APIReviewRecord] = field(default_factory=list)
    api_calls: int = 0
    cache_items_reused: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    image_bytes_sent: int = 0
    total_seconds: float = 0.0
    markdown_bytes_before: int = 0
    markdown_bytes_after: int = 0
    cache_bytes_before: int = 0
    cache_bytes_after: int = 0
    resized_images: int = 0
    candidate_images: int = 0
    grouped_images: int = 0

    def print_report(self) -> None:
        succeeded = sum(record.succeeded for record in self.records)
        failed = len(self.records) - succeeded

        print(
            "\nAPI review comparison for selected images "
            f"(score threshold: {self.threshold_percent:g}%)"
        )
        print("=" * 58)

        for record in self.records:
            cache_note = " [cached]" if record.content_from_cache else ""
            confidence = (
                f"{record.chart_probability:.1%} chart confidence"
                if record.chart_probability is not None
                else "chart classification unavailable"
            )
            print(
                f"- {record.filename} "
                f"({confidence})"
            )
            print(f"  Before: {record.before_details}")
            print(
                f"  After: {record.after_details}{cache_note} "
                f"[{format_duration(record.elapsed_seconds)}]"
            )

        print("\nAPI review totals")
        print(f"- Candidate images: {self.candidate_images}")
        print(f"- Analysis units: {len(self.records)}")
        print(f"- Images covered by grouped analyses: {self.grouped_images}")
        print(f"- API analyses added: {succeeded}")
        print(f"- Failed or unavailable analyses: {failed}")
        print(f"- New OpenAI API calls: {self.api_calls}")
        print(f"- Cached API analyses reused: {self.cache_items_reused}")
        print(f"- Input tokens: {self.input_tokens:,}")
        print(f"- Output tokens: {self.output_tokens:,}")
        print(f"- Total tokens: {self.total_tokens:,}")
        print(
            f"- Raw image bytes submitted: "
            f"{format_bytes(self.image_bytes_sent)}"
        )
        print(f"- Images resized for API submission: {self.resized_images}")
        print(f"- Additional elapsed time: {format_duration(self.total_seconds)}")
        print(
            "- Markdown size change: "
            f"{format_signed_bytes(self.markdown_bytes_after - self.markdown_bytes_before)}"
            f" (now {format_bytes(self.markdown_bytes_after)})"
        )
        print(
            "- Analysis-cache size change: "
            f"{format_signed_bytes(self.cache_bytes_after - self.cache_bytes_before)}"
            f" (now {format_bytes(self.cache_bytes_after)})"
        )


@dataclass
class RunSummary:
    pdf_name: str
    records: list[ImageHandlingRecord] = field(default_factory=list)
    classifier_calls: int = 0
    chart_model_calls: int = 0
    openai_calls: int = 0
    cache_items_reused: int = 0
    openai_input_tokens: int = 0
    openai_output_tokens: int = 0
    openai_total_tokens: int = 0
    openai_image_bytes_sent: int = 0
    started_at: str = ""
    finished_at: str = ""
    total_seconds: float = 0.0
    classifier_load_seconds: float = 0.0
    chart_model_load_seconds: float = 0.0
    pdf_conversion_seconds: float = 0.0
    figure_processing_seconds: float = 0.0
    classifier_inference_seconds: float = 0.0
    chart_inference_seconds: float = 0.0
    openai_request_seconds: float = 0.0
    markdown_write_seconds: float = 0.0
    stale_images_removed: int = 0
    stale_image_bytes_removed: int = 0
    resized_api_images: int = 0
    storage: StorageReport | None = None

    def add(
        self,
        filename: str,
        status: str,
        details: str,
        *,
        content_from_cache: bool = False,
        file_size_bytes: int = 0,
        chart_probability: float | None = None,
        image_path: Path | None = None,
        image_reference: str = "",
        markdown_image: str = "",
        surrounding_text: str = "",
        occurrence_index: int = -1,
        clip_classification: str = "",
    ) -> None:
        self.records.append(
            ImageHandlingRecord(
                filename=filename,
                status=status,
                details=details,
                content_from_cache=content_from_cache,
                file_size_bytes=file_size_bytes,
                chart_probability=chart_probability,
                image_path=image_path,
                image_reference=image_reference,
                markdown_image=markdown_image,
                surrounding_text=surrounding_text,
                occurrence_index=occurrence_index,
                clip_classification=clip_classification,
            )
        )

    def print_report(self) -> None:
        labels = {
            "chart_local": "Charts converted locally to tables",
            "chart_rejected": "Local chart tables rejected by validation",
            "openai": "Figures analyzed by OpenAI",
            "local_only_non_chart": "Non-charts retained without API analysis",
            "ambiguous": "Ambiguous figures held for review",
            "skipped": "Figures extracted without analysis",
            "missing": "Referenced image files not found",
            "classification_failed": "Local classifications that failed",
            "failed": "Figure-processing failures",
        }
        counts = Counter(record.status for record in self.records)

        print(f"\nImage handling summary for {self.pdf_name}")
        print("=" * (27 + len(self.pdf_name)))

        if not self.records:
            print("No image references were found in the generated Markdown.")
        else:
            for record in self.records:
                cache_note = " [cached content]" if record.content_from_cache else ""
                size_note = (
                    f" [{format_bytes(record.file_size_bytes)}]"
                    if record.file_size_bytes
                    else ""
                )
                print(
                    f"- {record.filename}: {record.details}"
                    f"{cache_note}{size_note}"
                )

        print("\nTotals")
        print(f"- Images referenced in Markdown: {len(self.records)}")
        for status, label in labels.items():
            print(f"- {label}: {counts.get(status, 0)}")
        print(f"- Local classifier executions: {self.classifier_calls}")
        print(f"- Local chart-to-table executions: {self.chart_model_calls}")
        print(f"- OpenAI API calls: {self.openai_calls}")
        print(f"- Cached items reused: {self.cache_items_reused}")
        print(
            f"- Oversized images resized for API submission: "
            f"{self.resized_api_images}"
        )
        print(
            f"- Stale extracted images removed: {self.stale_images_removed}"
            f" ({format_bytes(self.stale_image_bytes_removed)})"
        )

        if self.openai_calls or self.openai_total_tokens:
            print("\nOpenAI usage for this run")
            print(f"- Input tokens: {self.openai_input_tokens:,}")
            print(f"- Output tokens: {self.openai_output_tokens:,}")
            print(f"- Total tokens: {self.openai_total_tokens:,}")
            print(
                "- Figure image data submitted: "
                f"{format_bytes(self.openai_image_bytes_sent)}"
            )
            print(
                "- Note: base64/API transport overhead and surrounding text "
                "are not included in the raw image-byte figure."
            )

        self._print_timing_report()
        if self.storage is not None:
            self._print_storage_report()
            self._print_cleanup_guide()

    def _print_timing_report(self) -> None:
        print("\nElapsed time")
        if self.started_at:
            print(f"- Started: {self.started_at}")
        if self.finished_at:
            print(f"- Finished: {self.finished_at}")
        print(f"- Total run: {format_duration(self.total_seconds)}")
        print(
            "- Local classifier model loading: "
            f"{format_duration(self.classifier_load_seconds)}"
        )
        print(
            "- Local DePlot model loading: "
            f"{format_duration(self.chart_model_load_seconds)}"
        )
        print(
            "- PDF conversion and image extraction: "
            f"{format_duration(self.pdf_conversion_seconds)}"
        )
        print(
            "- Figure routing and enrichment: "
            f"{format_duration(self.figure_processing_seconds)}"
        )
        print(
            "  - Local classification inference: "
            f"{format_duration(self.classifier_inference_seconds)}"
        )
        print(
            "  - Local chart-to-table inference: "
            f"{format_duration(self.chart_inference_seconds)}"
        )
        print(
            "  - OpenAI request wait time: "
            f"{format_duration(self.openai_request_seconds)}"
        )
        print(
            "- Markdown file writing: "
            f"{format_duration(self.markdown_write_seconds)}"
        )
        print(
            "- Note: model-loading and inference times can be nested inside "
            "figure-processing time, so the lines should not be added together."
        )

    def _print_storage_report(self) -> None:
        storage = self.storage
        if storage is None:
            return

        artifact_delta = (
            storage.artifacts_after_bytes - storage.artifacts_before_bytes
        )
        print("\nDisk usage")
        print(
            f"- Input PDF (pre-existing): {format_bytes(storage.input_pdf_bytes)}"
        )
        print(
            f"- Generated Markdown: {format_bytes(storage.markdown_bytes)}"
            f" — {storage.output_file}"
        )
        print(
            f"- Image/cache directory: {format_bytes(storage.image_folder_bytes)}"
            f" — {storage.image_folder}"
        )
        print(
            f"  - Extracted image files: {storage.extracted_image_count}"
            f" using {format_bytes(storage.extracted_image_bytes)}"
        )
        print(
            f"  - Analysis cache: {format_bytes(storage.cache_bytes)}"
            f" — {storage.cache_file}"
        )
        print(
            "- Managed output total now: "
            f"{format_bytes(storage.artifacts_after_bytes)}"
        )
        print(
            "- Managed output change this run: "
            f"{format_signed_bytes(artifact_delta)}"
        )

        if storage.model_caches:
            print("\nLocal model cache")
            total_after = 0
            total_delta = 0
            for model_cache in storage.model_caches:
                delta = (
                    model_cache.size_after_bytes
                    - model_cache.size_before_bytes
                )
                total_after += model_cache.size_after_bytes
                total_delta += delta
                print(
                    f"- {model_cache.model_name}: "
                    f"{format_bytes(model_cache.size_after_bytes)}"
                    f" ({format_signed_bytes(delta)} this run)"
                )
                print(f"  {model_cache.path}")
            print(
                "- Tracked model-cache total: "
                f"{format_bytes(total_after)}"
            )
            print(
                "- Tracked model-cache growth this run: "
                f"{format_signed_bytes(total_delta)}"
            )
            print(
                "- Model caches are shared; their full size was not necessarily "
                "created by this PDF conversion."
            )
        else:
            print(
                "\nLocal model cache\n"
                "- No matching Hugging Face model-cache directories were found."
            )
        print(
            "- Python packages, temporary operating-system files, and unrelated "
            "runtime caches are not included because they cannot be attributed "
            "reliably to this PDF."
        )

    def _print_cleanup_guide(self) -> None:
        storage = self.storage
        if storage is None:
            return

        print("\nOptional cleanup — nothing is deleted automatically")
        print(
            "- Delete this paper's generated Markdown, images, and analysis "
            f"cache to free up to {format_bytes(storage.artifacts_after_bytes)}:"
        )
        print(
            "  "
            + cleanup_command([storage.output_file, storage.image_folder])
        )

        if storage.cache_bytes:
            print(
                "- Delete only the analysis cache to force future "
                f"reprocessing and free {format_bytes(storage.cache_bytes)}:"
            )
            print("  " + cleanup_command([storage.cache_file]))

        existing_model_paths = [
            item.path
            for item in storage.model_caches
            if item.size_after_bytes > 0
        ]
        model_bytes = sum(
            item.size_after_bytes
            for item in storage.model_caches
        )
        if existing_model_paths:
            print(
                "- Delete the tracked local models only if no other project "
                f"needs them; this can free {format_bytes(model_bytes)}. "
                "They will be downloaded again when needed:"
            )
            print("  " + cleanup_command(existing_model_paths))


def format_duration(seconds: float) -> str:
    seconds = max(0.0, seconds)
    if seconds < 1.0:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 60.0:
        return f"{seconds:.2f} s"

    minutes, remaining_seconds = divmod(seconds, 60.0)
    if minutes < 60:
        return f"{int(minutes)} min {remaining_seconds:.1f} s"

    hours, remaining_minutes = divmod(int(minutes), 60)
    return (
        f"{hours} h {remaining_minutes} min "
        f"{remaining_seconds:.1f} s"
    )


def format_bytes(size_bytes: int) -> str:
    size = float(max(0, size_bytes))
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size_bytes} B"


def format_signed_bytes(size_bytes: int) -> str:
    if size_bytes > 0:
        return f"+{format_bytes(size_bytes)}"
    if size_bytes < 0:
        return f"-{format_bytes(abs(size_bytes))}"
    return "0 B"


def path_size(path: Path) -> int:
    try:
        if path.is_file():
            return path.stat().st_size
        if not path.is_dir():
            return 0
    except OSError:
        return 0

    total = 0
    try:
        children = path.rglob("*")
        for child in children:
            try:
                if child.is_file() and not child.is_symlink():
                    total += child.stat().st_size
            except OSError:
                continue
    except OSError:
        return total
    return total


def image_directory_stats(image_folder: Path) -> tuple[int, int]:
    count = 0
    total = 0
    if not image_folder.is_dir():
        return count, total

    try:
        children = image_folder.rglob("*")
        for child in children:
            try:
                if (
                    child.is_file()
                    and not child.is_symlink()
                    and child.suffix.lower() in IMAGE_EXTENSIONS
                ):
                    count += 1
                    total += child.stat().st_size
            except OSError:
                continue
    except OSError:
        pass
    return count, total


def huggingface_cache_roots() -> list[Path]:
    candidates: list[Path] = []

    for variable in (
        "HF_HUB_CACHE",
        "HUGGINGFACE_HUB_CACHE",
        "TRANSFORMERS_CACHE",
    ):
        value = os.getenv(variable)
        if value:
            candidates.append(Path(value).expanduser())

    hf_home = os.getenv("HF_HOME")
    if hf_home:
        candidates.append(Path(hf_home).expanduser() / "hub")

    xdg_cache = os.getenv("XDG_CACHE_HOME")
    if xdg_cache:
        candidates.append(
            Path(xdg_cache).expanduser() / "huggingface" / "hub"
        )

    candidates.append(Path.home() / ".cache" / "huggingface" / "hub")

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = os.path.normcase(os.path.abspath(candidate))
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def model_cache_snapshot(
    model_names: list[str],
) -> dict[tuple[str, Path], int]:
    snapshot: dict[tuple[str, Path], int] = {}
    for model_name in model_names:
        cache_directory_name = "models--" + model_name.replace("/", "--")
        for cache_root in huggingface_cache_roots():
            model_path = cache_root / cache_directory_name
            size = path_size(model_path)
            if size > 0 or model_path.exists():
                snapshot[(model_name, model_path)] = size
    return snapshot


def build_storage_report(
    *,
    input_pdf: Path,
    output_file: Path,
    image_folder: Path,
    cache_file: Path,
    artifacts_before_bytes: int,
    model_cache_before: dict[tuple[str, Path], int],
    model_cache_after: dict[tuple[str, Path], int],
) -> StorageReport:
    extracted_image_count, extracted_image_bytes = image_directory_stats(
        image_folder
    )
    model_caches = [
        ModelCacheUsage(
            model_name=model_name,
            path=path,
            size_before_bytes=model_cache_before.get((model_name, path), 0),
            size_after_bytes=model_cache_after.get((model_name, path), 0),
        )
        for model_name, path in sorted(
            set(model_cache_before) | set(model_cache_after),
            key=lambda item: (item[0], str(item[1])),
        )
        if (
            model_cache_before.get((model_name, path), 0) > 0
            or model_cache_after.get((model_name, path), 0) > 0
        )
    ]

    markdown_bytes = path_size(output_file)
    image_folder_bytes = path_size(image_folder)
    return StorageReport(
        input_pdf=input_pdf,
        output_file=output_file,
        image_folder=image_folder,
        cache_file=cache_file,
        input_pdf_bytes=path_size(input_pdf),
        markdown_bytes=markdown_bytes,
        image_folder_bytes=image_folder_bytes,
        extracted_image_count=extracted_image_count,
        extracted_image_bytes=extracted_image_bytes,
        cache_bytes=path_size(cache_file),
        artifacts_before_bytes=artifacts_before_bytes,
        artifacts_after_bytes=markdown_bytes + image_folder_bytes,
        model_caches=model_caches,
    )


def cleanup_command(paths: list[Path]) -> str:
    if os.name == "nt":
        quoted_paths = []
        for path in paths:
            escaped_path = str(path).replace('"', '`"')
            quoted_paths.append(f'"{escaped_path}"')
        quoted = ", ".join(quoted_paths)
        return f"Remove-Item -LiteralPath {quoted} -Recurse -Force"

    quoted = " ".join(shlex.quote(str(path)) for path in paths)
    return f"rm -rf -- {quoted}"

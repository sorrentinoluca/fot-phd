#!/usr/bin/env python
"""Interactive launcher for ``convert_pdf.py`` with the same CLI flags.

Usage:
  1) Start the script.
  2) Enter one or more PDF paths separated by comma.
  3) Insert a comma-separated list (e.g., "file1.pdf, file2.pdf") to process
     those files immediately in one batch.
  4) Press Enter on an empty line to start conversion on all collected files.
"""

from __future__ import annotations

import argparse
import hashlib
import shlex
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pdfmd import build_argument_parser
from pdfmd import confirm_overwrite


MAX_IMAGE_PATH_BYTES = 255
MAX_FILES_PER_RUN = 25

DEBUG_PATH_RESOLUTION = True
UNSAFE_STEM_CHARS = re.compile(r"[() :]")


def _option_parser() -> argparse.ArgumentParser:
    parser = build_argument_parser()
    for action in parser._actions:
        if action.dest == "pdf_file" and not action.option_strings:
            action.nargs = "*"
            break
    return parser


def _split_csv_paths(raw_value: str) -> list[str]:
    text = raw_value.strip()
    if not text:
        return []

    text = re.sub(r"^\s*,+", "", text)
    text = re.sub(r",+\s*$", "", text)

    if "," in text:
        raw_parts = [part for part in re.split(r"\s*,\s*", text) if part.strip()]
    else:
        try:
            raw_parts = shlex.split(text)
        except ValueError:
            # shlex can fail on unterminated quotes; fallback to whitespace split.
            raw_parts = text.split()

        if not raw_parts:
            return []

    # In case the user pasted a long list without commas, keep extracting PDF tokens.
    if len(raw_parts) == 1:
        candidates = re.findall(r"(?i)[^\s,;]+?\.pdf", raw_parts[0])
        if candidates:
            raw_parts = candidates

    def _normalize_token(token: str) -> str:
        token = token.strip().strip('"').strip("'")
        token = re.sub(r"\\(.)", r"\1", token)

        while token.endswith((".", ",", ";", ":" )):
            token = token[:-1].strip()

        return token

    cleaned = []
    for part in raw_parts:
        if "," in part:
            for item in [chunk for chunk in part.split(",") if chunk.strip()]:
                normalized = _normalize_token(item)
                if normalized:
                    cleaned.append(normalized)
            continue

        normalized = _normalize_token(part)
        if normalized:
            cleaned.append(normalized)

    return cleaned


def _collect_inputs(initial_files: list[str]) -> list[str]:
    files: list[str] = []
    for raw_value in initial_files:
        files.extend(_split_csv_paths(raw_value))
        if len(files) > MAX_FILES_PER_RUN:
            print(
                f"Superato il limite di {MAX_FILES_PER_RUN} file per run: "
                f"elaborati solo i primi {MAX_FILES_PER_RUN}."
            )
            return files[:MAX_FILES_PER_RUN]

    while True:
        if not files:
            prompt = "Inserisci uno o più file concatenati da virgola (Invio vuoto per avviare): "
        else:
            prompt = "Inserisci uno o più file concatenati da virgola (Invio vuoto per avviare): "

        value = input(prompt).strip()
        if not value:
            break

        new_files = _split_csv_paths(value)
        if not new_files:
            continue

        files.extend(new_files)
        if len(files) > MAX_FILES_PER_RUN:
            print(
                f"Superato il limite di {MAX_FILES_PER_RUN} file per run: "
                f"elaborati solo i primi {MAX_FILES_PER_RUN}."
            )
            return files[:MAX_FILES_PER_RUN]

        if "," in value:
            break

    return files


def _resolve_input_file(input_file: Path) -> tuple[Path, list[str], bool]:
    candidates = []
    seen: set[str] = set()
    resolved_input = input_file.expanduser()

    def _add_candidate(candidate: Path) -> None:
        candidate = candidate.expanduser()
        resolved = candidate
        try:
            resolved = candidate.resolve()
        except RuntimeError:
            resolved = candidate
        key = str(resolved)
        if key not in seen:
            candidates.append(resolved)
            seen.add(key)

    _add_candidate(resolved_input)

    if resolved_input.suffix.lower() != ".pdf":
        _add_candidate(resolved_input.with_suffix(".pdf"))

    if not resolved_input.is_absolute():
        base_dir = Path(__file__).resolve().parent
        _add_candidate(base_dir / resolved_input)
        _add_candidate(base_dir.parent / resolved_input)
        _add_candidate((base_dir.parent / resolved_input.name))
        _add_candidate((base_dir.parent / resolved_input.with_suffix(".pdf").name))
        if resolved_input.suffix.lower() != ".pdf":
            _add_candidate((base_dir.parent / resolved_input.with_suffix(".pdf")))

    for candidate in candidates:
        if candidate.is_file():
            direct_match = candidate == resolved_input
            if direct_match:
                return candidate, candidates, True
            return candidate, candidates, False

    return resolved_input, candidates, False


def _has_to_mitigate_path_limits(input_file: Path) -> bool:
    sample_image_name = f"{input_file.stem}_000.png"
    sample_path = input_file.parent / f"{input_file.stem}_images" / sample_image_name
    return len(str(sample_path).encode("utf-8")) > MAX_IMAGE_PATH_BYTES


def _has_unsafe_name_chars(input_file: Path) -> bool:
    return UNSAFE_STEM_CHARS.search(input_file.stem) is not None


def _normalize_pdf_path(input_file: Path) -> Path:
    seed = f"{input_file}"
    short_stem = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
    return input_file.with_name(f"conv_{short_stem}.pdf")


def _prepare_input_path(input_file: Path) -> tuple[Path, Path]:
    """Return (path_to_process, original_path)."""
    if not _has_to_mitigate_path_limits(input_file) and not _has_unsafe_name_chars(
        input_file
    ):
        return input_file, input_file

    normalized = _normalize_pdf_path(input_file)
    if normalized == input_file:
        return input_file, input_file

    if normalized.exists():
        normalized.unlink()
    shutil.copy2(input_file, normalized)
    return normalized, input_file


def _extract_option_args(
    namespace: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> list[str]:
    option_args: list[str] = []
    namespace_dict = vars(namespace)

    for action in parser._actions:
        if (
            not action.option_strings
            or action.dest == "pdf_file"
            or isinstance(action, argparse._HelpAction)
        ):
            continue

        if action.dest not in namespace_dict:
            continue

        value = namespace_dict[action.dest]
        default = parser.get_default(action.dest)
        flag = next(
            option
            for option in action.option_strings
            if option.startswith("--")
        )

        if isinstance(action, argparse._StoreTrueAction):
            if value:
                option_args.append(flag)
            continue

        if isinstance(action, argparse._StoreFalseAction):
            if not value:
                option_args.append(flag)
            continue

        if value is None:
            continue

        if isinstance(action, argparse._StoreConstAction):
            option_args.append(flag)
            if value is not None and value != default:
                option_args.append(str(value))
            continue

        if value == default:
            continue

        option_args.extend((flag, str(value)))

    return option_args


def _rewrite_image_folder_refs(markdown: str, source_stem: str, target_stem: str) -> str:
    if source_stem == target_stem:
        return markdown

    return (
        markdown
        .replace(f"{source_stem}_images/", f"{target_stem}_images/")
        .replace(f"{source_stem}_images\\", f"{target_stem}_images\\")
    )


def _finalize_outputs(
    converter_pdf: Path,
    source_pdf: Path,
) -> None:
    temp_markdown = converter_pdf.with_suffix(".md")
    if not temp_markdown.exists():
        return

    final_markdown = source_pdf.with_suffix(".md")
    target_text = temp_markdown.read_text(encoding="utf-8")
    target_text = _rewrite_image_folder_refs(
        target_text,
        converter_pdf.stem,
        source_pdf.stem,
    )
    final_markdown.write_text(target_text, encoding="utf-8")

    temp_images = converter_pdf.parent / f"{converter_pdf.stem}_images"
    final_images = source_pdf.parent / f"{source_pdf.stem}_images"
    if temp_images.exists():
        if final_images.exists():
            shutil.rmtree(final_images)
        temp_images.replace(final_images)


def _run_for_file(
    pdf_file: str,
    converter: Path,
    option_args: list[str],
    overwrite: bool,
) -> tuple[int, str | None]:
    requested_path = Path(pdf_file)
    input_file, checked_paths, direct_match = _resolve_input_file(requested_path)
    requested_for_report = str(requested_path)
    if requested_path.suffix == "" and input_file.suffix.lower() == ".pdf":
        requested_for_report = str(requested_path.with_suffix(".pdf"))
    if DEBUG_PATH_RESOLUTION and not direct_match:
        print(f"Nome file inserito -> percorso risolto: {requested_path} -> {input_file}")
    output_file = input_file.with_suffix(".md")

    if output_file.exists() and not overwrite:
        if not confirm_overwrite(output_file):
            print("Conversion cancelled. The existing file was not changed.")
            return 0, None

    if not input_file.is_file():
        tried = ", ".join(str(path) for path in checked_paths)
        message = (
            f"File not found: {requested_for_report}\n"
            f"Percorsi provati: {tried}"
        )
        print(message)
        return 1, message

    if input_file.suffix.lower() != ".pdf":
        message = f"Expected a PDF file: {input_file}"
        print(message)
        return 1, message

    staged_pdf, source_pdf = _prepare_input_path(input_file)
    is_staged = staged_pdf != source_pdf

    command = [
        sys.executable,
        str(converter),
        str(staged_pdf),
        *option_args,
    ]

    print(f"\n=== Avvio conversione: {source_pdf} ===")
    return_code = subprocess.run(command).returncode

    if is_staged and return_code == 0:
        _finalize_outputs(staged_pdf, source_pdf)

    if is_staged:
        temp_markdown = staged_pdf.with_suffix(".md")
        if temp_markdown.exists():
            temp_markdown.unlink()
        temp_images = staged_pdf.parent / f"{staged_pdf.stem}_images"
        if temp_images.exists():
            shutil.rmtree(temp_images)
        staged_pdf.unlink()

    if return_code == 0:
        return return_code, None

    return return_code, f"convert_pdf.py exited with code {return_code}"


def main() -> int:
    parser = _option_parser()
    args = parser.parse_args()

    option_args = _extract_option_args(args, parser)
    files = _collect_inputs(list(getattr(args, "pdf_file", [])))

    if not files:
        print("Nessun PDF specificato. Nessuna conversione eseguita.")
        return 0

    converter_path = Path(__file__).with_name("convert_pdf.py")
    if not converter_path.exists():
        print(f"Errore: script di conversione non trovato: {converter_path}")
        return 1

    failed: list[tuple[str, str]] = []
    for pdf_file in files:
        result_code, failure = _run_for_file(
            pdf_file=pdf_file,
            converter=converter_path,
            option_args=option_args,
            overwrite=getattr(args, "overwrite", False),
        )
        if result_code != 0 and failure is not None:
            failed_path = str(Path(pdf_file).expanduser())
            if failed_path and not failed_path.endswith(".pdf"):
                failed_path = f"{failed_path}.pdf"
            failed.append((failed_path, failure))

    if failed:
        print(f"Completato con {len(failed)} errore/i su {len(files)} file.")
        print("File non elaborati:")
        for failed_file, reason in failed:
            print(f" - {failed_file}: {reason}")
        return 1

    print(f"Completato per {len(files)} file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

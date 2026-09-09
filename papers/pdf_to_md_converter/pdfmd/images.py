from __future__ import annotations

import base64
from contextlib import contextmanager
from dataclasses import dataclass
from io import BytesIO
import mimetypes
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterator
from urllib.parse import unquote

from .config import DEFAULT_API_MAX_IMAGE_EDGE


@dataclass(frozen=True)
class MarkdownImageReference:
    start: int
    end: int
    markdown: str
    path: str


@dataclass(frozen=True)
class PreparedImage:
    data: bytes
    mime_type: str
    was_resized: bool
    original_bytes: int


@dataclass(frozen=True)
class GeneratedImageLocation:
    pdf_name: str
    page_number: int
    image_number: int


def atomic_write_text(file_path: Path, text: str) -> None:
    """Replace a text file only after its complete content reaches disk."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(text)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        temporary_path.replace(file_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def prepare_image_for_api(
    image_path: Path,
    max_edge: int = DEFAULT_API_MAX_IMAGE_EDGE,
) -> PreparedImage:
    original_data = image_path.read_bytes()
    original_mime = mimetypes.guess_type(image_path.name)[0] or "image/png"
    if max_edge <= 0:
        return PreparedImage(
            data=original_data,
            mime_type=original_mime,
            was_resized=False,
            original_bytes=len(original_data),
        )

    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            "Image resizing requires Pillow. Install it with:\n"
            "python -m pip install Pillow"
        ) from error

    with Image.open(image_path) as opened_image:
        width, height = opened_image.size
        if max(width, height) <= max_edge:
            return PreparedImage(
                data=original_data,
                mime_type=original_mime,
                was_resized=False,
                original_bytes=len(original_data),
            )

        scale = max_edge / float(max(width, height))
        new_size = (
            max(1, round(width * scale)),
            max(1, round(height * scale)),
        )
        resized = opened_image.convert("RGB").resize(
            new_size,
            Image.Resampling.LANCZOS,
        )
        from io import BytesIO

        buffer = BytesIO()
        # PNG is lossless and preserves labels/line art in research figures.
        resized.save(buffer, format="PNG", optimize=True)
        resized_data = buffer.getvalue()

    return PreparedImage(
        data=resized_data,
        mime_type="image/png",
        was_resized=True,
        original_bytes=len(original_data),
    )


def encode_prepared_image(prepared: PreparedImage) -> str:
    encoded = base64.b64encode(prepared.data).decode("utf-8")
    mime_type = prepared.mime_type
    return f"data:{mime_type};base64,{encoded}"


def encode_image(
    image_path: Path,
    max_edge: int = DEFAULT_API_MAX_IMAGE_EDGE,
) -> str:
    return encode_prepared_image(prepare_image_for_api(image_path, max_edge))


def generated_image_location(
    image_path: Path,
) -> GeneratedImageLocation | None:
    match = re.fullmatch(
        r"(?P<pdf>.+\.pdf)-(?P<page>\d{4})-(?P<image>\d+)"
        r"\.(?:png|jpe?g|webp|tiff?|bmp|gif)",
        image_path.name,
        flags=re.IGNORECASE,
    )
    if match is None:
        return None
    return GeneratedImageLocation(
        pdf_name=match.group("pdf"),
        page_number=int(match.group("page")),
        image_number=int(match.group("image")),
    )


def locate_source_pdf(
    image_path: Path,
    location: GeneratedImageLocation,
) -> Path | None:
    for directory in (image_path.parent, *image_path.parents):
        candidate = directory / location.pdf_name
        if candidate.is_file():
            return candidate
    return None


@contextmanager
def rendered_pdf_page_for_analysis(
    pdf_path: Path,
    page_number: int,
    *,
    dpi: int = 180,
) -> Iterator[Path]:
    """Render one 1-based PDF page to a temporary PNG for grouped analysis."""
    try:
        import pymupdf
    except ImportError as error:
        raise RuntimeError(
            "Grouped figure analysis requires PyMuPDF, which is installed "
            "with pymupdf4llm."
        ) from error

    document = pymupdf.open(str(pdf_path))
    temporary_path: Path | None = None
    try:
        if page_number < 1 or page_number > document.page_count:
            raise ValueError(
                f"PDF page {page_number} is outside the document range."
            )
        page = document.load_page(page_number - 1)
        pixmap = page.get_pixmap(dpi=dpi, alpha=False)
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".png",
            prefix="pdfmd-grouped-page-",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(pixmap.tobytes("png"))
        yield temporary_path
    finally:
        document.close()
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _find_unescaped(text: str, character: str, start: int) -> int:
    escaped = False
    for index in range(start, len(text)):
        value = text[index]
        if escaped:
            escaped = False
            continue
        if value == "\\":
            escaped = True
            continue
        if value == character:
            return index
    return -1


def _destination_from_link_content(content: str) -> str:
    content = content.strip()
    if content.startswith("<"):
        closing = _find_unescaped(content, ">", 1)
        if closing >= 0:
            return content[: closing + 1]

    escaped = False
    nested_parentheses = 0
    for index, value in enumerate(content):
        if escaped:
            escaped = False
            continue
        if value == "\\":
            escaped = True
            continue
        if value == "(":
            nested_parentheses += 1
        elif value == ")" and nested_parentheses:
            nested_parentheses -= 1
        elif value.isspace() and nested_parentheses == 0:
            return content[:index]
    return content


def find_markdown_images(markdown: str) -> list[MarkdownImageReference]:
    """Parse inline Markdown images, including destinations with parentheses."""
    references: list[MarkdownImageReference] = []
    cursor = 0

    while True:
        start = markdown.find("![", cursor)
        if start < 0:
            break

        alt_end = _find_unescaped(markdown, "]", start + 2)
        if alt_end < 0 or alt_end + 1 >= len(markdown):
            cursor = start + 2
            continue

        open_parenthesis = alt_end + 1
        if markdown[open_parenthesis] != "(":
            cursor = alt_end + 1
            continue

        depth = 1
        escaped = False
        in_angle_destination = False
        closing_parenthesis = -1
        for index in range(open_parenthesis + 1, len(markdown)):
            value = markdown[index]
            if escaped:
                escaped = False
                continue
            if value == "\\":
                escaped = True
                continue
            if value == "<" and depth == 1:
                in_angle_destination = True
                continue
            if value == ">" and in_angle_destination:
                in_angle_destination = False
                continue
            if in_angle_destination:
                continue
            if value == "(":
                depth += 1
            elif value == ")":
                depth -= 1
                if depth == 0:
                    closing_parenthesis = index
                    break

        if closing_parenthesis < 0:
            cursor = open_parenthesis + 1
            continue

        content = markdown[open_parenthesis + 1 : closing_parenthesis]
        path = _destination_from_link_content(content)
        end = closing_parenthesis + 1
        references.append(
            MarkdownImageReference(
                start=start,
                end=end,
                markdown=markdown[start:end],
                path=path,
            )
        )
        cursor = end

    return references


def replace_markdown_images(
    markdown: str,
    replacement: Any,
) -> str:
    references = find_markdown_images(markdown)
    if not references:
        return markdown

    output: list[str] = []
    cursor = 0
    for occurrence_index, reference in enumerate(references):
        output.append(markdown[cursor : reference.start])
        output.append(replacement(reference, occurrence_index))
        cursor = reference.end
    output.append(markdown[cursor:])
    return "".join(output)


def normalized_image_reference(raw_reference: str) -> str:
    reference = unquote(raw_reference.strip())
    if reference.startswith("<") and reference.endswith(">"):
        reference = reference[1:-1]
    return reference


def remove_stale_generated_images(
    *,
    image_folder: Path,
    input_file: Path,
    markdown: str,
    keep_stale: bool,
) -> tuple[int, int]:
    """Remove obsolete PyMuPDF4LLM images while preserving unrelated files."""
    if keep_stale or not image_folder.is_dir():
        return 0, 0

    referenced_paths: set[Path] = set()
    for reference in find_markdown_images(markdown):
        normalized = normalized_image_reference(reference.path)
        referenced_paths.add((input_file.parent / normalized).resolve())

    generated_name = re.compile(
        rf"^{re.escape(input_file.name)}-\d{{4}}-\d+\."
        rf"(?:png|jpe?g|webp|tiff?|bmp|gif)$",
        re.IGNORECASE,
    )
    removed_count = 0
    removed_bytes = 0
    for candidate in image_folder.iterdir():
        if (
            not candidate.is_file()
            or not generated_name.fullmatch(candidate.name)
            or candidate.resolve() in referenced_paths
        ):
            continue
        try:
            size = candidate.stat().st_size
            candidate.unlink()
        except OSError as error:
            print(f"Warning: Could not remove stale image {candidate}: {error}")
            continue
        removed_count += 1
        removed_bytes += size

    return removed_count, removed_bytes

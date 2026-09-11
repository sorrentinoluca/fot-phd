from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

from .images import generated_image_location, locate_source_pdf


NUMBER_PATTERN = re.compile(
    r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?"
)


@dataclass(frozen=True)
class ChartTableValidation:
    accepted: bool
    markdown: str
    reasons: tuple[str, ...]
    numeric_values_checked: int = 0
    numeric_values_matched: int = 0
    source_text_available: bool = False

    @property
    def summary(self) -> str:
        if not self.accepted:
            return "; ".join(self.reasons)
        if self.source_text_available:
            return (
                "structure passed; "
                f"{self.numeric_values_matched}/"
                f"{self.numeric_values_checked} numeric values were found "
                "in the source PDF page text"
            )
        return (
            "structure passed; source PDF text was unavailable for the "
            "numeric cross-check"
        )


def parse_deplot_rows(raw_table: str) -> list[list[str]]:
    normalized = raw_table.replace("<0x0A>", "\n").strip()
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in lines
    ]


def render_markdown_table(rows: list[list[str]]) -> str:
    if len(rows) < 2:
        raise ValueError("At least a header and one data row are required.")

    column_count = len(rows[0])
    if column_count < 2 or any(len(row) != column_count for row in rows):
        raise ValueError("Rows must have a consistent multi-column structure.")

    def render_row(row: list[str]) -> str:
        escaped = [
            cell.replace("\\", "\\\\").replace("|", "\\|")
            for cell in row
        ]
        return "| " + " | ".join(escaped) + " |"

    output_lines = [
        render_row(rows[0]),
        "| " + " | ".join(["---"] * column_count) + " |",
    ]
    output_lines.extend(render_row(row) for row in rows[1:])
    return "\n".join(output_lines)


def source_pdf_page_text(image_path: Path) -> str | None:
    location = generated_image_location(image_path)
    if location is None:
        return None
    pdf_path = locate_source_pdf(image_path, location)
    if pdf_path is None:
        return None

    try:
        import pymupdf
    except ImportError:
        return None

    try:
        document = pymupdf.open(str(pdf_path))
    except Exception:
        return None
    try:
        if not 1 <= location.page_number <= document.page_count:
            return None
        text = document.load_page(location.page_number - 1).get_text().strip()
        return text or None
    except Exception:
        return None
    finally:
        document.close()


def _normalized_number(token: str) -> str | None:
    cleaned = token.rstrip("%").replace(",", "")
    try:
        number = Decimal(cleaned)
    except InvalidOperation:
        return None
    if number == 0:
        return "0"
    return format(number.normalize(), "f")


def _numeric_values(text: str) -> list[str]:
    values: list[str] = []
    for match in NUMBER_PATTERN.finditer(text):
        normalized = _normalized_number(match.group())
        if normalized is not None:
            values.append(normalized)
    return values


def _normalized_label(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def validate_deplot_table(
    raw_table: str,
    *,
    source_text: str | None = None,
    minimum_numeric_match_ratio: float = 0.80,
) -> ChartTableValidation:
    rows = parse_deplot_rows(raw_table)
    reasons: list[str] = []

    # DePlot sometimes emits a title metadata row before the real header.
    # It is useful context, but it is not itself a table header.
    if rows and _normalized_label(rows[0][0]) == "title":
        rows = rows[1:]

    if len(rows) < 3:
        reasons.append(
            "fewer than two data rows were produced after the header"
        )

    column_count = len(rows[0]) if rows else 0
    if column_count < 2:
        reasons.append("the output is not a multi-column table")
    elif any(len(row) != column_count for row in rows):
        reasons.append("rows have inconsistent column counts")

    if rows and column_count >= 2:
        headers = [_normalized_label(cell) for cell in rows[0]]
        if any(not header for header in headers):
            reasons.append("one or more column headers are blank")
        duplicate_headers = [
            header
            for header, count in Counter(headers).items()
            if header and count > 1
        ]
        if duplicate_headers:
            reasons.append("column headers are duplicated")

        data_rows = rows[1:]
        sparse_rows = [
            row
            for row in data_rows
            if (
                len(row) == column_count
                and sum(bool(cell.strip()) for cell in row)
                / float(column_count)
                < 0.75
            )
        ]
        if sparse_rows:
            reasons.append("one or more data rows are mostly empty")

        primary_labels = [
            _normalized_label(row[0])
            for row in data_rows
            if len(row) == column_count and row and row[0].strip()
        ]
        repeated_labels = [
            label
            for label, count in Counter(primary_labels).items()
            if label and count > 1
        ]
        if repeated_labels:
            reasons.append(
                "the first column contains repeated row labels without a "
                "reliable panel or series mapping"
            )

    numeric_values = _numeric_values(
        "\n".join("|".join(row) for row in rows[1:])
        if len(rows) > 1
        else ""
    )
    if len(numeric_values) < 2:
        reasons.append("fewer than two numeric data values were produced")

    source_available = bool(source_text and source_text.strip())
    matched_values = 0
    if source_available and numeric_values:
        source_numbers = set(_numeric_values(source_text or ""))
        matched_values = sum(
            value in source_numbers
            for value in numeric_values
        )
        match_ratio = matched_values / float(len(numeric_values))
        if match_ratio < minimum_numeric_match_ratio:
            reasons.append(
                f"only {matched_values}/{len(numeric_values)} numeric values "
                "could be corroborated in the source PDF page text"
            )

    markdown = ""
    if not reasons:
        try:
            markdown = render_markdown_table(rows)
        except ValueError as error:
            reasons.append(str(error))

    return ChartTableValidation(
        accepted=not reasons,
        markdown=markdown,
        reasons=tuple(reasons),
        numeric_values_checked=len(numeric_values),
        numeric_values_matched=matched_values,
        source_text_available=source_available,
    )

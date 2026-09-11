from __future__ import annotations

from collections import Counter
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from .cache import load_cache, make_cache_key, save_cache, sha256_bytes
from .chart_validation import (
    source_pdf_page_text,
    validate_deplot_table,
)
from .config import (
    CHART_LABEL, NON_CHART_LABEL, ROUTING_CACHE_VERSION,
    CHART_TABLE_CACHE_VERSION, CHART_TABLE_PROMPT,
    CHART_TABLE_MAX_NEW_TOKENS, FIGURE_PROMPT_VERSION,
    FIGURE_REVIEW_PROMPT_VERSION, FIGURE_GROUP_REVIEW_PROMPT_VERSION,
    CHART_REVIEW_PROMPT_VERSION, IMAGE_PREPARATION_VERSION,
    DEFAULT_API_MAX_IMAGE_EDGE,
)
from .images import (
    MarkdownImageReference, find_markdown_images, generated_image_location,
    locate_source_pdf, normalized_image_reference,
    rendered_pdf_page_for_analysis, replace_markdown_images,
)
from .models import LocalChartModels
from .reporting import (
    APIReviewRecord, APIReviewSummary, ImageHandlingRecord,
    OpenAIAnalysisResult, RunSummary, path_size,
)
from .vision import analyze_research_figure


@dataclass(frozen=True)
class APIReviewUnit:
    records: tuple[ImageHandlingRecord, ...]
    pdf_path: Path | None = None
    page_number: int | None = None

    @property
    def is_grouped(self) -> bool:
        return len(self.records) > 1

    @property
    def label(self) -> str:
        if self.is_grouped and self.pdf_path is not None:
            return (
                f"{self.pdf_path.name} page {self.page_number} "
                f"({len(self.records)} grouped fragments)"
            )
        return self.records[0].filename


def build_api_review_units(
    candidates: list[ImageHandlingRecord],
) -> list[APIReviewUnit]:
    group_keys: dict[int, tuple[Path, int]] = {}
    grouped_records: dict[
        tuple[Path, int],
        list[ImageHandlingRecord],
    ] = {}

    for record in candidates:
        if record.image_path is None:
            continue
        location = generated_image_location(record.image_path)
        if location is None:
            continue
        pdf_path = locate_source_pdf(record.image_path, location)
        if pdf_path is None:
            continue
        key = (pdf_path.resolve(), location.page_number)
        group_keys[id(record)] = key
        grouped_records.setdefault(key, []).append(record)

    units: list[APIReviewUnit] = []
    consumed: set[int] = set()
    for record in candidates:
        if id(record) in consumed:
            continue
        key = group_keys.get(id(record))
        records = grouped_records.get(key, []) if key is not None else []
        if key is not None and len(records) > 1:
            unit_records = tuple(records)
            consumed.update(id(item) for item in unit_records)
            units.append(
                APIReviewUnit(
                    records=unit_records,
                    pdf_path=key[0],
                    page_number=key[1],
                )
            )
        else:
            consumed.add(id(record))
            units.append(APIReviewUnit(records=(record,)))
    return units


def grouped_clip_classification(
    records: tuple[ImageHandlingRecord, ...],
) -> str:
    if len(records) == 1:
        return records[0].clip_classification or "not run"
    counts = Counter(
        record.clip_classification or "not run"
        for record in records
    )
    parts = [
        f"{count} {classification}"
        for classification, count in sorted(counts.items())
    ]
    return "grouped fragments: " + ", ".join(parts)


def grouped_surrounding_text(
    records: tuple[ImageHandlingRecord, ...],
) -> str:
    if len(records) == 1:
        return records[0].surrounding_text
    first = records[0].surrounding_text[:3000]
    last = records[-1].surrounding_text[-3000:]
    return first + "\n\n[... grouped figure fragments ...]\n\n" + last


def print_openai_outcome(
    *,
    filename: str,
    result: OpenAIAnalysisResult,
    clip_classification: str,
    clip_chart_probability: float | None,
    from_cache: bool,
) -> None:
    source_note = " [cached]" if from_cache else ""
    probability_note = (
        f", {clip_chart_probability:.1%} chart confidence"
        if clip_chart_probability is not None
        else ""
    )
    agreement_labels = {
        "agree": "agreement",
        "disagree": "disagreement",
        "uncertain": "uncertain",
        "not_applicable": "not applicable",
    }
    agreement = agreement_labels.get(
        result.clip_agreement,
        result.clip_agreement,
    )
    print(f"\nOpenAI figure result: {filename}{source_note}")
    print(f"- Detected figure type: {result.figure_type}")
    print(
        f"- Agreement/disagreement with CLIP: {agreement} "
        f"(CLIP: {clip_classification}{probability_note})"
    )
    print(f"- One-line finding: {result.one_line_finding}")
    print(f"- Unreadable or uncertain content: {result.uncertainty}")
    print(
        "- Table extracted: "
        + ("yes" if result.table_extracted else "no")
    )


def confirm_overwrite(file_path: Path) -> bool:
    while True:
        answer = input(
            f"\nThe file already exists:\n{file_path}\n"
            "Replace it? [y/N]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("", "n", "no"):
            return False

        print("Please enter 'y' for yes or 'n' for no.")


def enrich_markdown(
    *,
    markdown: str,
    document_directory: Path,
    client: Any | None,
    openai_model: str,
    local_models: LocalChartModels | None,
    classifier_model: str,
    chart_model: str,
    chart_threshold: float,
    cache_file: Path,
    reanalyze: bool,
    skip_analysis: bool,
    local_only: bool,
    use_local_chart_tables: bool,
    summary: RunSummary,
    api_max_image_edge: int = DEFAULT_API_MAX_IMAGE_EDGE,
) -> str:
    cache = load_cache(cache_file)

    def replace_image(
        reference: MarkdownImageReference,
        occurrence_index: int,
    ) -> str:
        markdown_image = reference.markdown
        image_reference = normalized_image_reference(reference.path)
        image_path = document_directory / Path(image_reference)
        filename = image_path.name

        if not image_path.is_file():
            summary.add(
                filename,
                "missing",
                "referenced file was not found",
                occurrence_index=occurrence_index,
            )
            return markdown_image

        image_size = path_size(image_path)

        if skip_analysis:
            summary.add(
                filename,
                "skipped",
                "extracted only; all analysis was disabled",
                file_size_bytes=image_size,
                image_path=image_path,
                image_reference=image_reference,
                markdown_image=markdown_image,
                occurrence_index=occurrence_index,
            )
            return markdown_image

        image_hash = sha256_bytes(image_path.read_bytes())
        context_start = max(0, reference.start - 2000)
        context_end = min(len(markdown), reference.end + 2000)
        surrounding_text = markdown[context_start:context_end]

        route = "openai"
        chart_probability: float | None = None

        if use_local_chart_tables:
            routing_key = make_cache_key(
                ROUTING_CACHE_VERSION,
                classifier_model,
                CHART_LABEL,
                NON_CHART_LABEL,
                f"{chart_threshold:.12g}",
                image_hash,
            )
            routing_entry = cache["routing"].get(routing_key)

            if routing_entry is not None and not reanalyze:
                route = routing_entry["route"]
                chart_probability = float(
                    routing_entry["chart_probability"]
                )
                summary.cache_items_reused += 1
            else:
                if local_models is None:
                    raise RuntimeError(
                        "Local chart models were not initialized."
                    )

                try:
                    summary.classifier_calls += 1
                    chart_probability = (
                        local_models.classify_chart_probability(image_path)
                    )
                except Exception as error:
                    summary.add(
                        filename,
                        "classification_failed",
                        f"local chart classification failed: {error}",
                        file_size_bytes=image_size,
                        chart_probability=None,
                        image_path=image_path,
                        image_reference=image_reference,
                        markdown_image=markdown_image,
                        surrounding_text=surrounding_text,
                        occurrence_index=occurrence_index,
                        clip_classification="unavailable",
                    )
                    return markdown_image

                if chart_probability >= chart_threshold:
                    route = "chart"
                elif chart_probability <= 1.0 - chart_threshold:
                    route = "non_chart"
                else:
                    route = "ambiguous"

                cache["routing"][routing_key] = {
                    "route": route,
                    "chart_probability": chart_probability,
                }
                save_cache(cache_file, cache)

        if route == "chart":
            rejection_detail: str | None = None
            table_key = make_cache_key(
                CHART_TABLE_CACHE_VERSION,
                chart_model,
                CHART_TABLE_PROMPT,
                str(CHART_TABLE_MAX_NEW_TOKENS),
                image_hash,
            )
            cached_table_entry = cache["chart_tables"].get(table_key)
            from_cache = (
                isinstance(cached_table_entry, dict)
                and isinstance(cached_table_entry.get("accepted"), bool)
                and not reanalyze
            )

            if from_cache:
                validation_summary = str(
                    cached_table_entry.get(
                        "validation_summary",
                        "cached validation result",
                    )
                )
                if cached_table_entry["accepted"]:
                    table_markdown = str(
                        cached_table_entry.get("markdown", "")
                    )
                    if not table_markdown.strip():
                        from_cache = False
                else:
                    rejection_detail = validation_summary
                if from_cache:
                    summary.cache_items_reused += 1

            if not from_cache:
                if local_models is None:
                    raise RuntimeError(
                        "Local chart models were not initialized."
                    )

                try:
                    summary.chart_model_calls += 1
                    raw_table = local_models.extract_chart_table(image_path)
                    validation = validate_deplot_table(
                        raw_table,
                        source_text=source_pdf_page_text(image_path),
                    )
                    if not validation.accepted:
                        rejection_detail = validation.summary
                    else:
                        table_markdown = validation.markdown
                        validation_summary = validation.summary
                except Exception as error:
                    rejection_detail = (
                        f"local table extraction or validation failed: {error}"
                    )

                cache["chart_tables"][table_key] = (
                    {
                        "accepted": True,
                        "markdown": table_markdown,
                        "validation_summary": validation_summary,
                    }
                    if rejection_detail is None
                    else {
                        "accepted": False,
                        "validation_summary": rejection_detail,
                    }
                )
                save_cache(cache_file, cache)

            confidence = (
                f"{chart_probability:.1%}"
                if chart_probability is not None
                else "unknown"
            )
            if rejection_detail is not None:
                if local_only:
                    summary.add(
                        filename,
                        "chart_rejected",
                        "local chart table rejected "
                        f"({confidence} chart confidence): "
                        f"{rejection_detail}; image retained for API or "
                        "manual review",
                        content_from_cache=from_cache,
                        file_size_bytes=image_size,
                        chart_probability=chart_probability,
                        image_path=image_path,
                        image_reference=image_reference,
                        markdown_image=markdown_image,
                        surrounding_text=surrounding_text,
                        occurrence_index=occurrence_index,
                        clip_classification="chart",
                    )
                    return markdown_image
                route = "chart_review"
            else:
                summary.add(
                    filename,
                    "chart_local",
                    "validated local chart-to-table conversion "
                    f"({confidence} chart confidence; "
                    f"{validation_summary})",
                    content_from_cache=from_cache,
                    file_size_bytes=image_size,
                    chart_probability=chart_probability,
                    image_path=image_path,
                    image_reference=image_reference,
                    markdown_image=markdown_image,
                    surrounding_text=surrounding_text,
                    occurrence_index=occurrence_index,
                    clip_classification="chart",
                )
                return (
                    f"{markdown_image}\n\n"
                    "### Chart data\n\n"
                    f"{table_markdown}"
                )

        if route == "chart":
            raise AssertionError("Chart routing did not produce a result.")

        if route == "chart_review":
            confidence = (
                f"{chart_probability:.1%}"
                if chart_probability is not None
                else "unknown"
            )
            chart_review_detail = (
                "local chart table was rejected "
                f"({confidence} chart confidence): {rejection_detail}"
            )
        else:
            chart_review_detail = ""

        if route == "ambiguous":
            confidence = (
                f"{chart_probability:.1%}"
                if chart_probability is not None
                else "unknown"
            )
            summary.add(
                filename,
                "ambiguous",
                "classification was uncertain "
                f"({confidence} chart confidence); no API call was made "
                "during initial routing",
                file_size_bytes=image_size,
                chart_probability=chart_probability,
                image_path=image_path,
                image_reference=image_reference,
                markdown_image=markdown_image,
                surrounding_text=surrounding_text,
                occurrence_index=occurrence_index,
                clip_classification="ambiguous",
            )
            return markdown_image

        if local_only:
            confidence = (
                f"{chart_probability:.1%}"
                if chart_probability is not None
                else "not classified"
            )
            summary.add(
                filename,
                (
                    "chart_rejected"
                    if route == "chart_review"
                    else "local_only_non_chart"
                ),
                (
                    f"{chart_review_detail}; image retained for API or "
                    "manual review"
                    if route == "chart_review"
                    else "retained without API analysis "
                    f"({confidence} chart confidence)"
                ),
                file_size_bytes=image_size,
                chart_probability=chart_probability,
                image_path=image_path,
                image_reference=image_reference,
                markdown_image=markdown_image,
                surrounding_text=surrounding_text,
                occurrence_index=occurrence_index,
                clip_classification=(
                    "chart"
                    if route == "chart_review"
                    else (
                        "non-chart"
                        if chart_probability is not None
                        else "not run"
                    )
                ),
            )
            return markdown_image

        if client is None:
            summary.add(
                filename,
                "failed",
                "OpenAI analysis was requested but no API client was available",
                file_size_bytes=image_size,
                chart_probability=chart_probability,
                image_path=image_path,
                image_reference=image_reference,
                markdown_image=markdown_image,
                surrounding_text=surrounding_text,
                occurrence_index=occurrence_index,
                clip_classification=(
                    route.replace("_", "-")
                    if use_local_chart_tables
                    else "not run"
                ),
            )
            return markdown_image

        include_charts = route == "chart_review"
        context_hash = sha256_bytes(surrounding_text.encode("utf-8"))
        analysis_key = make_cache_key(
            (
                CHART_REVIEW_PROMPT_VERSION
                if include_charts
                else FIGURE_PROMPT_VERSION
            ),
            openai_model,
            IMAGE_PREPARATION_VERSION,
            str(api_max_image_edge),
            image_hash,
            context_hash,
        )
        cached_analysis = cache["openai_analyses"].get(analysis_key)
        from_cache = cached_analysis is not None and not reanalyze

        clip_classification = (
            "chart"
            if include_charts
            else route.replace("_", "-")
            if use_local_chart_tables
            else "not run"
        )
        if from_cache:
            result = OpenAIAnalysisResult.from_cache_entry(cached_analysis)
            summary.cache_items_reused += 1
        else:
            request_started = perf_counter()
            try:
                summary.openai_calls += 1
                result = analyze_research_figure(
                    client=client,
                    image_path=image_path,
                    surrounding_text=surrounding_text,
                    model=openai_model,
                    include_charts=include_charts,
                    max_image_edge=api_max_image_edge,
                    clip_classification=clip_classification,
                    clip_chart_probability=chart_probability,
                )
                summary.openai_image_bytes_sent += (
                    result.image_bytes_submitted
                )
                if result.image_was_resized:
                    summary.resized_api_images += 1
                summary.openai_input_tokens += result.input_tokens
                summary.openai_output_tokens += result.output_tokens
                summary.openai_total_tokens += result.total_tokens
            except Exception as error:
                summary.add(
                    filename,
                    "failed",
                    f"OpenAI analysis failed: {error}",
                    file_size_bytes=image_size,
                    chart_probability=chart_probability,
                    image_path=image_path,
                    image_reference=image_reference,
                    markdown_image=markdown_image,
                    surrounding_text=surrounding_text,
                    occurrence_index=occurrence_index,
                    clip_classification=clip_classification,
                )
                return markdown_image
            finally:
                summary.openai_request_seconds += (
                    perf_counter() - request_started
                )

            cache["openai_analyses"][analysis_key] = result.to_cache_entry()
            save_cache(cache_file, cache)

        print_openai_outcome(
            filename=filename,
            result=result,
            clip_classification=clip_classification,
            clip_chart_probability=chart_probability,
            from_cache=from_cache,
        )

        confidence_detail = ""
        if chart_probability is not None:
            confidence_detail = (
                f"; {chart_probability:.1%} chart confidence"
            )
        summary.add(
            filename,
            "openai",
            (
                "chart reviewed by OpenAI after local table validation "
                f"rejected it: {rejection_detail}"
                if include_charts
                else f"non-chart visual analysis via OpenAI"
                f"{confidence_detail}"
            ),
            content_from_cache=from_cache,
            file_size_bytes=image_size,
            chart_probability=chart_probability,
            image_path=image_path,
            image_reference=image_reference,
            markdown_image=markdown_image,
            surrounding_text=surrounding_text,
            occurrence_index=occurrence_index,
            clip_classification=clip_classification,
        )
        return (
            f"{markdown_image}\n\n"
            "### Figure analysis\n\n"
            f"{result.text}"
        )

    return replace_markdown_images(markdown, replace_image)


def api_review_candidates(
    summary: RunSummary,
    threshold_percent: float,
) -> list[ImageHandlingRecord]:
    return [
        record
        for record in summary.records
        if (
            record.status != "openai"
            and (
                record.status == "classification_failed"
                or record.status == "chart_rejected"
                or (
                    record.chart_probability is not None
                    and record.chart_probability * 100.0 < threshold_percent
                )
            )
            and record.image_path is not None
            and record.image_path.is_file()
        )
    ]


def confirm_api_review(
    candidate_count: int,
    threshold_percent: float,
) -> bool:
    while True:
        answer = input(
            f"\n{candidate_count} image(s) were not analyzed by OpenAI and "
            "either failed local chart-table validation, scored below "
            f"{threshold_percent:g}% chart confidence, or could not be "
            "classified locally.\n"
            "Call the OpenAI API for these images now? [y/N]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True
        if answer in ("", "n", "no"):
            return False
        print("Please enter 'y' for yes or 'n' for no.")


def add_api_review_to_markdown(
    markdown: str,
    record: ImageHandlingRecord,
    analysis: str,
    threshold_percent: float,
) -> str:
    del threshold_percent  # Operational threshold never belongs in final MD.
    if not record.markdown_image:
        raise ValueError("The original Markdown image reference is unavailable.")
    references = find_markdown_images(markdown)
    if not 0 <= record.occurrence_index < len(references):
        raise ValueError(
            "The original Markdown image occurrence could not be found."
        )
    reference = references[record.occurrence_index]
    if (
        normalized_image_reference(reference.path)
        != record.image_reference
    ):
        raise ValueError("The Markdown image occurrence no longer matches.")

    review_section = (
        f"{reference.markdown}\n\n"
        "### Figure analysis\n\n"
        f"{analysis}"
    )
    return (
        markdown[: reference.start]
        + review_section
        + markdown[reference.end :]
    )


def perform_api_review(
    *,
    markdown: str,
    candidates: list[ImageHandlingRecord],
    client: Any | None,
    openai_model: str,
    threshold_percent: float,
    cache_file: Path,
    reanalyze: bool,
    api_max_image_edge: int = DEFAULT_API_MAX_IMAGE_EDGE,
) -> tuple[str, APIReviewSummary]:
    review_summary = APIReviewSummary(
        threshold_percent=threshold_percent,
        candidate_images=len(candidates),
    )
    cache = load_cache(cache_file)
    review_started = perf_counter()
    units = build_api_review_units(candidates)
    review_summary.grouped_images = sum(
        len(unit.records)
        for unit in units
        if unit.is_grouped
    )

    for unit in units:
        item_started = perf_counter()
        from_cache = False
        anchor_record = unit.records[-1]
        probability = (
            anchor_record.chart_probability
            if not unit.is_grouped
            else None
        )
        image_path = anchor_record.image_path

        if image_path is None:
            review_summary.records.append(
                APIReviewRecord(
                    filename=unit.label,
                    chart_probability=probability,
                    before_details=anchor_record.details,
                    after_details=(
                        "API analysis was not performed because the extracted "
                        "image path was unavailable"
                    ),
                    elapsed_seconds=perf_counter() - item_started,
                    succeeded=False,
                )
            )
            continue

        try:
            page_context = (
                rendered_pdf_page_for_analysis(
                    unit.pdf_path,
                    unit.page_number,
                )
                if (
                    unit.is_grouped
                    and unit.pdf_path is not None
                    and unit.page_number is not None
                )
                else nullcontext(image_path)
            )
            with page_context as analysis_image_path:
                image_hash = sha256_bytes(
                    analysis_image_path.read_bytes()
                )
                surrounding_text = grouped_surrounding_text(unit.records)
                context_hash = sha256_bytes(
                    surrounding_text.encode("utf-8")
                )
                prompt_version = (
                    FIGURE_GROUP_REVIEW_PROMPT_VERSION
                    if unit.is_grouped
                    else FIGURE_REVIEW_PROMPT_VERSION
                )
                cache_key_parts = [
                    prompt_version,
                    openai_model,
                    IMAGE_PREPARATION_VERSION,
                    str(api_max_image_edge),
                    image_hash,
                    context_hash,
                ]
                if unit.is_grouped:
                    cache_key_parts.append(str(len(unit.records)))
                analysis_key = make_cache_key(*cache_key_parts)
                cached_analysis = cache["openai_analyses"].get(
                    analysis_key
                )
                from_cache = (
                    cached_analysis is not None and not reanalyze
                )

                if not from_cache and client is None:
                    raise RuntimeError(
                        "No cached review was available and a new API call "
                        "could not be made because the OpenAI client or API "
                        "key was unavailable"
                    )

                clip_classification = grouped_clip_classification(
                    unit.records
                )
                if from_cache:
                    result = OpenAIAnalysisResult.from_cache_entry(
                        cached_analysis
                    )
                    review_summary.cache_items_reused += 1
                else:
                    review_summary.api_calls += 1
                    result = analyze_research_figure(
                        client=client,
                        image_path=analysis_image_path,
                        surrounding_text=surrounding_text,
                        model=openai_model,
                        include_charts=True,
                        max_image_edge=api_max_image_edge,
                        clip_classification=clip_classification,
                        clip_chart_probability=(
                            anchor_record.chart_probability
                            if not unit.is_grouped
                            else None
                        ),
                        grouped_fragment_count=len(unit.records),
                    )
                    review_summary.image_bytes_sent += (
                        result.image_bytes_submitted
                    )
                    if result.image_was_resized:
                        review_summary.resized_images += 1
                    review_summary.input_tokens += result.input_tokens
                    review_summary.output_tokens += result.output_tokens
                    review_summary.total_tokens += result.total_tokens
                    cache["openai_analyses"][
                        analysis_key
                    ] = result.to_cache_entry()
                    save_cache(cache_file, cache)

                print_openai_outcome(
                    filename=unit.label,
                    result=result,
                    clip_classification=clip_classification,
                    clip_chart_probability=(
                        anchor_record.chart_probability
                        if not unit.is_grouped
                        else None
                    ),
                    from_cache=from_cache,
                )
            markdown = add_api_review_to_markdown(
                markdown=markdown,
                record=anchor_record,
                analysis=result.text,
                threshold_percent=threshold_percent,
            )
        except Exception as error:
            review_summary.records.append(
                APIReviewRecord(
                    filename=unit.label,
                    chart_probability=probability,
                    before_details=(
                        f"{len(unit.records)} fragments grouped from PDF "
                        f"page {unit.page_number}"
                        if unit.is_grouped
                        else anchor_record.details
                    ),
                    after_details=f"API review failed: {error}",
                    elapsed_seconds=perf_counter() - item_started,
                    content_from_cache=from_cache,
                    succeeded=False,
                )
            )
            continue

        review_summary.records.append(
            APIReviewRecord(
                filename=unit.label,
                chart_probability=probability,
                before_details=(
                    f"{len(unit.records)} fragments grouped from PDF "
                    f"page {unit.page_number}"
                    if unit.is_grouped
                    else anchor_record.details
                ),
                after_details=(
                    "One grouped API analysis was added to the Markdown"
                    if unit.is_grouped
                    else "API analysis was added to the Markdown"
                ),
                elapsed_seconds=perf_counter() - item_started,
                content_from_cache=from_cache,
                succeeded=True,
            )
        )

    review_summary.total_seconds = perf_counter() - review_started
    return markdown, review_summary

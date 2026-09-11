from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
from time import perf_counter
from typing import Any

from .config import (
    DEFAULT_API_MAX_IMAGE_EDGE, DEFAULT_CHART_MODEL,
    DEFAULT_CLASSIFIER_MODEL, DEFAULT_OPENAI_MODEL,
)
from .extraction import extract_markdown_and_images
from .images import atomic_write_text, remove_stale_generated_images
from .models import LocalChartModels
from .reporting import (
    RunSummary, build_storage_report, model_cache_snapshot, path_size,
)
from .routing import (
    api_review_candidates, confirm_api_review, confirm_overwrite,
    enrich_markdown, perform_api_review,
)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a research-paper PDF to Markdown, validate local "
            "chart-table proposals, and analyze figures."
        )
    )
    parser.add_argument(
        "pdf_file",
        type=Path,
        help="Name or path of the PDF file",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_OPENAI_MODEL,
        help=f"OpenAI model for non-chart figures (default: {DEFAULT_OPENAI_MODEL})",
    )
    parser.add_argument(
        "--classifier-model",
        default=DEFAULT_CLASSIFIER_MODEL,
        help="Local Hugging Face model used to identify charts",
    )
    parser.add_argument(
        "--chart-model",
        default=DEFAULT_CHART_MODEL,
        help="Local Hugging Face model used to propose chart tables",
    )
    parser.add_argument(
        "--chart-threshold",
        type=float,
        default=0.65,
        help=(
            "Confidence required to route an image as chart or non-chart "
            "(default: 0.65)"
        ),
    )
    parser.add_argument(
        "--reanalyze-images",
        action="store_true",
        help="Ignore cached routing, tables, and visual analyses",
    )
    parser.add_argument(
        "--skip-image-analysis",
        action="store_true",
        help="Extract figures without local or API-based analysis",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help=(
            "Prevent automatic OpenAI calls during the initial pass; the "
            "optional end review can still be approved"
        ),
    )
    parser.add_argument(
        "--no-local-chart-tables",
        action="store_true",
        help=(
            "Disable local chart classification and send all figures to "
            "OpenAI"
        ),
    )
    parser.add_argument(
        "--api-review-below",
        type=float,
        default=65.0,
        metavar="PERCENT",
        help=(
            "Offer an OpenAI review for rejected local chart tables, "
            "classification failures, and non-API images below this chart-"
            "confidence percentage; 0 disables the prompt (default: 65)"
        ),
    )
    parser.add_argument(
        "--auto-api-review",
        action="store_true",
        help=(
            "Automatically perform eligible end-of-run OpenAI reviews "
            "without asking for confirmation"
        ),
    )
    parser.add_argument(
        "--api-max-image-edge",
        type=int,
        default=DEFAULT_API_MAX_IMAGE_EDGE,
        metavar="PIXELS",
        help=(
            "Resize oversized API image submissions to this longest edge; "
            "0 disables resizing (default: 2048)"
        ),
    )
    parser.add_argument(
        "--keep-stale-images",
        action="store_true",
        help=(
            "Keep obsolete PyMuPDF4LLM-generated images instead of removing "
            "files no longer referenced by the new Markdown"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace an existing Markdown output without asking for "
            "confirmation"
        ),
    )
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()

    if not 0.5 < args.chart_threshold <= 1.0:
        parser.error("--chart-threshold must be greater than 0.5 and at most 1.0")

    if not 0.0 <= args.api_review_below <= 100.0:
        parser.error("--api-review-below must be between 0 and 100")

    if args.api_max_image_edge < 0:
        parser.error("--api-max-image-edge must be 0 or greater")

    if args.auto_api_review and args.api_review_below <= 0:
        parser.error(
            "--auto-api-review requires --api-review-below to be greater "
            "than 0"
        )

    if args.auto_api_review and args.skip_image_analysis:
        parser.error(
            "--auto-api-review cannot be combined with "
            "--skip-image-analysis"
        )

    if args.local_only and args.no_local_chart_tables:
        parser.error(
            "--local-only cannot be combined with --no-local-chart-tables"
        )

    input_file = args.pdf_file.expanduser().resolve()

    if not input_file.is_file():
        parser.error(f"File not found: {input_file}")

    if input_file.suffix.lower() != ".pdf":
        parser.error(f"Expected a PDF file: {input_file}")

    output_file = input_file.with_suffix(".md")

    if (
        output_file.exists()
        and not args.overwrite
        and not confirm_overwrite(output_file)
    ):
        print("Conversion cancelled. The existing file was not changed.")
        return

    image_folder_name = f"{input_file.stem}_images"
    image_folder = input_file.parent / image_folder_name
    cache_file = image_folder / "figure_analysis_cache.json"

    needs_openai = (
        not args.skip_image_analysis
        and not args.local_only
    )
    if needs_openai and not os.getenv("OPENAI_API_KEY"):
        parser.error(
            "OPENAI_API_KEY is not set. Set it, use --local-only, or use "
            "--skip-image-analysis."
        )

    use_local_chart_tables = (
        not args.skip_image_analysis
        and not args.no_local_chart_tables
    )

    run_started = perf_counter()
    summary = RunSummary(
        pdf_name=input_file.name,
        started_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )
    artifacts_before_bytes = (
        path_size(output_file) + path_size(image_folder)
    )
    tracked_model_names = (
        [args.classifier_model, args.chart_model]
        if use_local_chart_tables
        else []
    )
    model_cache_before = model_cache_snapshot(tracked_model_names)

    local_models: LocalChartModels | None = None
    if use_local_chart_tables:
        local_models = LocalChartModels(
            classifier_model=args.classifier_model,
            chart_model=args.chart_model,
        )
        try:
            local_models.load_classifier()
        except Exception as error:
            parser.exit(
                status=2,
                message=f"Local chart classifier could not be loaded:\n{error}\n",
            )

    client: Any | None = None
    if needs_openai:
        try:
            from openai import OpenAI
        except ImportError:
            parser.exit(
                status=2,
                message=(
                    "The OpenAI package is not installed. Install it with:\n"
                    "python -m pip install openai\n"
                ),
            )
        client = OpenAI()

    image_folder.mkdir(exist_ok=True)

    conversion_started = perf_counter()
    try:
        markdown = extract_markdown_and_images(
            input_file=input_file,
            image_folder_name=image_folder_name,
        )
    except Exception as error:
        parser.exit(status=2, message=f"PDF conversion failed:\n{error}\n")
    finally:
        summary.pdf_conversion_seconds = (
            perf_counter() - conversion_started
        )

    (
        summary.stale_images_removed,
        summary.stale_image_bytes_removed,
    ) = remove_stale_generated_images(
        image_folder=image_folder,
        input_file=input_file,
        markdown=markdown,
        keep_stale=args.keep_stale_images,
    )

    enrichment_started = perf_counter()
    markdown = enrich_markdown(
        markdown=markdown,
        document_directory=input_file.parent,
        client=client,
        openai_model=args.model,
        local_models=local_models,
        classifier_model=args.classifier_model,
        chart_model=args.chart_model,
        chart_threshold=args.chart_threshold,
        cache_file=cache_file,
        reanalyze=args.reanalyze_images,
        skip_analysis=args.skip_image_analysis,
        local_only=args.local_only,
        use_local_chart_tables=use_local_chart_tables,
        summary=summary,
        api_max_image_edge=args.api_max_image_edge,
    )
    summary.figure_processing_seconds = (
        perf_counter() - enrichment_started
    )

    write_started = perf_counter()
    atomic_write_text(output_file, markdown)
    summary.markdown_write_seconds = perf_counter() - write_started

    if local_models is not None:
        summary.classifier_load_seconds = (
            local_models.classifier_load_seconds
        )
        summary.chart_model_load_seconds = (
            local_models.chart_model_load_seconds
        )
        summary.classifier_inference_seconds = (
            local_models.classifier_inference_seconds
        )
        summary.chart_inference_seconds = (
            local_models.chart_inference_seconds
        )

    model_cache_after = model_cache_snapshot(tracked_model_names)
    summary.storage = build_storage_report(
        input_pdf=input_file,
        output_file=output_file,
        image_folder=image_folder,
        cache_file=cache_file,
        artifacts_before_bytes=artifacts_before_bytes,
        model_cache_before=model_cache_before,
        model_cache_after=model_cache_after,
    )
    summary.total_seconds = perf_counter() - run_started
    summary.finished_at = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    print(f"\nMarkdown created: {output_file}")
    print(f"Figures extracted to: {image_folder}")
    summary.print_report()

    if (
        args.api_review_below <= 0
        or args.skip_image_analysis
        or not use_local_chart_tables
    ):
        return

    candidates = api_review_candidates(
        summary,
        args.api_review_below,
    )
    if not candidates:
        print(
            "\nAPI review: no eligible non-API images failed local chart "
            f"validation, scored below {args.api_review_below:g}%, or had "
            "a classification failure."
        )
        return

    if args.auto_api_review:
        print(
            "\nEligible API review automatically approved by "
            "--auto-api-review."
        )
    else:
        if not confirm_api_review(
            candidate_count=len(candidates),
            threshold_percent=args.api_review_below,
        ):
            print("API review skipped. The initial Markdown was not changed.")
            return

    review_started = perf_counter()
    review_client = client
    if review_client is None:
        if not os.getenv("OPENAI_API_KEY"):
            print(
                "\nOPENAI_API_KEY is not set. Cached API reviews can still be "
                "reused, but new API calls cannot be performed."
            )
        else:
            try:
                from openai import OpenAI
            except ImportError:
                print(
                    "\nThe OpenAI package is not installed. Install it with:\n"
                    "python -m pip install openai"
                )
            else:
                review_client = OpenAI()

    markdown_bytes_before = path_size(output_file)
    cache_bytes_before = path_size(cache_file)
    markdown, review_summary = perform_api_review(
        markdown=markdown,
        candidates=candidates,
        client=review_client,
        openai_model=args.model,
        threshold_percent=args.api_review_below,
        cache_file=cache_file,
        reanalyze=args.reanalyze_images,
        api_max_image_edge=args.api_max_image_edge,
    )
    atomic_write_text(output_file, markdown)
    review_summary.total_seconds = perf_counter() - review_started
    review_summary.markdown_bytes_before = markdown_bytes_before
    review_summary.markdown_bytes_after = path_size(output_file)
    review_summary.cache_bytes_before = cache_bytes_before
    review_summary.cache_bytes_after = path_size(cache_file)

    print(f"\nMarkdown updated after API review: {output_file}")
    review_summary.print_report()

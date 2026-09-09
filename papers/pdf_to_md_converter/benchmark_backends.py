"""Benchmark PyMuPDF4LLM, Marker, and Docling on the same research PDFs.

Examples:
    python benchmark_backends.py papers/
    python benchmark_backends.py P001.pdf P002.pdf --overwrite
    python benchmark_backends.py papers/ --backends pymupdf4llm docling

This runner records objective timing/storage/structure measurements and creates
a human quality scorecard. It does not select or change the converter's default
backend automatically.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pdfmd.benchmark import BACKENDS, run_benchmark


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run PyMuPDF4LLM, Marker, and Docling against an identical PDF set."
        )
    )
    parser.add_argument(
        "inputs",
        type=Path,
        nargs="+",
        help="PDF files and/or directories containing research-paper PDFs",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("pdf_backend_benchmark"),
        help="Benchmark output directory (default: pdf_backend_benchmark)",
    )
    parser.add_argument(
        "--backends",
        nargs="+",
        choices=BACKENDS,
        default=list(BACKENDS),
        help="Backends to execute (default: all three)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing per-paper backend outputs",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        results, report = run_benchmark(
            inputs=args.inputs,
            output_dir=args.output_dir,
            backends=args.backends,
            overwrite=args.overwrite,
        )
    except ValueError as error:
        parser.error(str(error))

    succeeded = sum(item.succeeded for item in results)
    failed = len(results) - succeeded
    print(f"\nBenchmark completed: {succeeded} succeeded, {failed} failed.")
    print(f"Report: {report}")
    if failed:
        print("Open the report for dependency or conversion errors.")


if __name__ == "__main__":
    main()

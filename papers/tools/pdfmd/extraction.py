from __future__ import annotations

import os
from pathlib import Path


def extract_markdown_and_images(
    input_file: Path,
    image_folder_name: str,
) -> str:
    try:
        import pymupdf4llm
    except ImportError as error:
        raise RuntimeError(
            "PyMuPDF4LLM is not installed. Install it with:\n"
            "python -m pip install pymupdf4llm"
        ) from error

    original_directory = Path.cwd()
    try:
        os.chdir(input_file.parent)
        return pymupdf4llm.to_markdown(
            input_file.name,
            write_images=True,
            image_path=image_folder_name,
            image_format="png",
            dpi=200,
            force_text=False,
            show_progress=True,
        )
    finally:
        os.chdir(original_directory)

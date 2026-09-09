from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Any

from .config import (
    CHART_LABEL, NON_CHART_LABEL, CHART_TABLE_PROMPT,
    CHART_TABLE_MAX_NEW_TOKENS,
)
from .chart_validation import parse_deplot_rows, render_markdown_table


def select_torch_device(torch_module: Any) -> str:
    if torch_module.cuda.is_available():
        return "cuda"
    if (
        hasattr(torch_module.backends, "mps")
        and torch_module.backends.mps.is_available()
    ):
        return "mps"
    return "cpu"


class LocalChartModels:
    """Lazily loads local models used for chart routing and table extraction."""

    def __init__(self, classifier_model: str, chart_model: str) -> None:
        self.classifier_model_name = classifier_model
        self.chart_model_name = chart_model
        self.torch: Any = None
        self.device = "cpu"
        self.classifier_processor: Any = None
        self.classifier_model: Any = None
        self.chart_processor: Any = None
        self.chart_model: Any = None
        self.image_class: Any = None
        self.classifier_load_seconds = 0.0
        self.chart_model_load_seconds = 0.0
        self.classifier_inference_seconds = 0.0
        self.chart_inference_seconds = 0.0

    def load_classifier(self) -> None:
        if self.classifier_model is not None:
            return

        load_started = perf_counter()
        try:
            try:
                import torch
                from PIL import Image
                from transformers import CLIPModel, CLIPProcessor
            except ImportError as error:
                raise RuntimeError(
                    "Local chart processing requires torch, Pillow, "
                    "transformers, and sentencepiece. Install them with:\n"
                    "python -m pip install torch pillow transformers "
                    "sentencepiece"
                ) from error

            self.torch = torch
            self.image_class = Image
            self.device = select_torch_device(torch)

            print(
                f"Loading local chart classifier "
                f"'{self.classifier_model_name}' on {self.device}..."
            )
            self.classifier_processor = CLIPProcessor.from_pretrained(
                self.classifier_model_name
            )
            self.classifier_model = CLIPModel.from_pretrained(
                self.classifier_model_name
            ).to(self.device)
            self.classifier_model.eval()
        finally:
            self.classifier_load_seconds += perf_counter() - load_started

    def load_chart_model(self) -> None:
        if self.chart_model is not None:
            return

        load_started = perf_counter()
        try:
            self.load_classifier()

            try:
                from transformers import (
                    Pix2StructForConditionalGeneration,
                    Pix2StructProcessor,
                )
            except ImportError as error:
                raise RuntimeError(
                    "DePlot requires a Transformers installation with "
                    "Pix2Struct support. Upgrade it with:\n"
                    "python -m pip install --upgrade transformers sentencepiece"
                ) from error

            print(
                f"Loading local chart-to-table model "
                f"'{self.chart_model_name}' on {self.device}..."
            )
            self.chart_processor = Pix2StructProcessor.from_pretrained(
                self.chart_model_name
            )
            self.chart_model = (
                Pix2StructForConditionalGeneration.from_pretrained(
                    self.chart_model_name
                ).to(self.device)
            )
            self.chart_model.eval()
        finally:
            self.chart_model_load_seconds += perf_counter() - load_started

    def classify_chart_probability(self, image_path: Path) -> float:
        self.load_classifier()
        inference_started = perf_counter()
        try:
            with self.image_class.open(image_path) as opened_image:
                image = opened_image.convert("RGB")
                inputs = self.classifier_processor(
                    text=[CHART_LABEL, NON_CHART_LABEL],
                    images=image,
                    return_tensors="pt",
                    padding=True,
                )

            inputs = {
                key: value.to(self.device)
                for key, value in inputs.items()
            }

            with self.torch.inference_mode():
                output = self.classifier_model(**inputs)
                probabilities = output.logits_per_image.softmax(dim=1)[0]

            return float(probabilities[0].item())
        finally:
            self.classifier_inference_seconds += (
                perf_counter() - inference_started
            )

    def extract_chart_table(self, image_path: Path) -> str:
        self.load_chart_model()
        inference_started = perf_counter()
        try:
            with self.image_class.open(image_path) as opened_image:
                image = opened_image.convert("RGB")
                inputs = self.chart_processor(
                    images=image,
                    text=CHART_TABLE_PROMPT,
                    return_tensors="pt",
                )

            inputs = {
                key: value.to(self.device)
                for key, value in inputs.items()
            }

            with self.torch.inference_mode():
                predictions = self.chart_model.generate(
                    **inputs,
                    max_new_tokens=CHART_TABLE_MAX_NEW_TOKENS,
                )

            return self.chart_processor.decode(
                predictions[0],
                skip_special_tokens=True,
            ).strip()
        finally:
            self.chart_inference_seconds += perf_counter() - inference_started


def deplot_output_to_markdown(raw_table: str) -> str:
    rows = parse_deplot_rows(raw_table)

    if len(rows) < 2 or max((len(row) for row in rows), default=0) < 2:
        raise ValueError(
            "The local model did not return a usable multi-row table."
        )

    column_count = max(len(row) for row in rows)
    padded_rows = [
        row + [""] * (column_count - len(row))
        for row in rows
    ]
    return render_markdown_table(padded_rows)

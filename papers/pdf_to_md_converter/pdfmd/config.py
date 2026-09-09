from __future__ import annotations

import os

CACHE_VERSION = 3
FIGURE_PROMPT_VERSION = "research-figure-v3-structured"
FIGURE_REVIEW_PROMPT_VERSION = "research-figure-api-review-v2-structured"
FIGURE_GROUP_REVIEW_PROMPT_VERSION = (
    "research-figure-group-api-review-v1-structured"
)
CHART_REVIEW_PROMPT_VERSION = "research-chart-validation-v1-structured"
ROUTING_CACHE_VERSION = "routing-v2"
CHART_TABLE_CACHE_VERSION = "chart-table-v3-validated"
CHART_TABLE_PROMPT = "Generate underlying data table of the figure below:"
CHART_TABLE_MAX_NEW_TOKENS = 512
DEFAULT_API_MAX_IMAGE_EDGE = 2048
IMAGE_PREPARATION_VERSION = "api-image-v1"

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-5.5")
DEFAULT_CLASSIFIER_MODEL = "openai/clip-vit-base-patch32"
DEFAULT_CHART_MODEL = "google/deplot"

CHART_LABEL = (
    "a scientific chart or data plot with axes, bars, lines, points, "
    "curves, plotted measurements, or a heatmap"
)
NON_CHART_LABEL = (
    "a scientific diagram, flowchart, photograph, microscopy image, "
    "illustration, equation, or other non-chart figure"
)

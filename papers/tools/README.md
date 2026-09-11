# Research PDF to enriched Markdown

The normal converter still runs from the same command:

```powershell
python -m pip install -r requirements.txt
python convert_pdf.py "C:\Research\P001.pdf"
```

Useful examples:

```powershell
# Entire initial run is local; allow the optional final API-review question
python convert_pdf.py "C:\Research\P001.pdf" --local-only

# Strictly local, including no final API-review question
python convert_pdf.py "C:\Research\P001.pdf" --local-only --api-review-below 0

# Run locally first, then automatically perform every eligible API review
python convert_pdf.py "C:\Research\P001.pdf" --local-only --auto-api-review

# Also replace an existing Markdown file without asking
python convert_pdf.py "C:\Research\P001.pdf" --local-only --auto-api-review --overwrite

# Keep obsolete generated image files instead of removing them
python convert_pdf.py "C:\Research\P001.pdf" --keep-stale-images

# Disable in-memory downscaling of oversized OpenAI image submissions
python convert_pdf.py "C:\Research\P001.pdf" --api-max-image-edge 0
```

The originals in `<paper>_images` are never resized. By default, only the
temporary API representation is reduced to a longest edge of 2048 pixels.

## `convert_pdf.py` parameters

General syntax:

```powershell
python convert_pdf.py PDF_FILE [OPTIONS]
```

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `pdf_file` | Yes | — | Name or path of the research-paper PDF. Relative and absolute paths are supported. The output Markdown is created beside this PDF. |
| `--model MODEL` | No | `OPENAI_VISION_MODEL`, or `gpt-5.5` | OpenAI vision-capable model used to analyze non-chart figures and figures selected during the optional API-review pass. |
| `--classifier-model MODEL` | No | `openai/clip-vit-base-patch32` | Local Hugging Face CLIP model used to estimate whether an extracted image is a chart. |
| `--chart-model MODEL` | No | `google/deplot` | Local Hugging Face model used to propose a table from an image classified as a chart. The proposal is validated before it can enter the Markdown. |
| `--chart-threshold NUMBER` | No | `0.65` | Classification confidence boundary. It must be greater than `0.5` and at most `1.0`. At the default, scores at or above `0.65` are treated as charts, scores at or below `0.35` as non-charts, and scores between those boundaries as ambiguous. |
| `--reanalyze-images` | No | Disabled | Ignores cached routing, chart tables and OpenAI analyses, forcing figures to be processed again. |
| `--skip-image-analysis` | No | Disabled | Extracts images but performs no classification, chart-to-table conversion or OpenAI analysis. It also skips the final API-review offer. |
| `--local-only` | No | Disabled | Prevents automatic OpenAI calls during the initial pass. The final API-review question can still be offered. Combine it with `--api-review-below 0` for a completely local run. |
| `--no-local-chart-tables` | No | Disabled | Disables local chart classification and DePlot. Extracted figures are sent directly to OpenAI unless analysis is otherwise disabled. It cannot be combined with `--local-only`. |
| `--api-review-below PERCENT` | No | `65` | After the initial summary, offers to send eligible figures below this chart-confidence percentage to OpenAI. Figures whose local classification failed are also eligible. Valid range: `0`–`100`; use `0` to disable the question. |
| `--auto-api-review` | No | Disabled | Automatically performs all eligible end-of-run OpenAI reviews without asking for confirmation. It also includes rejected chart-table proposals even when their CLIP score exceeds `--api-review-below`. It requires a review threshold greater than `0` and cannot be combined with `--skip-image-analysis`. |
| `--api-max-image-edge PIXELS` | No | `2048` | Downscales an oversized image in memory before sending it to OpenAI. The original extracted image is unchanged. Use `0` to disable resizing; negative values are invalid. |
| `--keep-stale-images` | No | Disabled | Keeps obsolete PyMuPDF4LLM-generated images. Without this option, generated image files no longer referenced by the new Markdown are removed; unrelated files are preserved. |
| `--overwrite` | No | Disabled | Replaces an existing output Markdown file without displaying the overwrite question. It does not affect OpenAI-review confirmation; combine it with `--auto-api-review` to suppress both questions. |
| `-h`, `--help` | No | — | Displays the command-line help and exits. |

Important parameter combinations:

```powershell
# Completely local conversion
python convert_pdf.py "P001.pdf" --local-only --api-review-below 0

# Extract Markdown and figures without analyzing any figures
python convert_pdf.py "P001.pdf" --skip-image-analysis

# Send every extracted figure to OpenAI without local chart processing
python convert_pdf.py "P001.pdf" --no-local-chart-tables

# Reprocess everything and use a stricter local chart threshold
python convert_pdf.py "P001.pdf" --reanalyze-images --chart-threshold 0.75

# Local routing followed by automatic eligible API review; replace old output
python convert_pdf.py "P001.pdf" --local-only --auto-api-review --overwrite
```

Environment variables used by `convert_pdf.py`:

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | Required when a run needs to make a new OpenAI API request. It is not required for strictly local conversion or cache-only reuse. |
| `OPENAI_VISION_MODEL` | Optional default for `--model`. An explicit `--model` argument takes precedence. |

## `convert_pdf.py` compared with `benchmark_backends.py`

`convert_pdf.py` is the normal production tool. It converts one research PDF
into enriched Markdown. `benchmark_backends.py` is an evaluation tool for
comparing the raw Markdown produced by different PDF extraction libraries.

| Feature | `convert_pdf.py` | `benchmark_backends.py` |
| --- | --- | --- |
| Main purpose | Produce enriched Markdown | Compare PDF extraction backends |
| Input | One PDF | One or more PDFs, or a directory |
| PDF backend | PyMuPDF4LLM | PyMuPDF4LLM, Marker and Docling |
| Local chart detection | Yes | No |
| Chart-to-table with DePlot | Yes | No |
| OpenAI image analysis | Optional | No |
| Analysis cache | Yes | No |
| Output | Final `.md` and image directory | Separate raw output from every backend |
| Changes the default backend | No | No |
| Typical usage | Regular conversion | Occasional quality testing |

The normal conversion workflow is:

```text
PDF
  → PyMuPDF4LLM extraction
  → image classification
  → local chart-to-table proposal
  → structural and source-PDF numeric validation
  → reject unsafe tables or publish validated tables
  → optional OpenAI figure analysis
  → final enriched Markdown
```

CLIP confidence is only a routing score: it estimates whether an image is a
chart. It does **not** measure whether DePlot reconstructed the table correctly.
A DePlot proposal is inserted under `### Chart data` only when:

- it has a consistent multi-column structure and usable headers;
- its data rows are sufficiently complete;
- it has no repeated primary labels that lose panel/series identity;
- it contains enough numeric data; and
- when the source PDF page has a usable text layer, at least 80% of proposed
  numeric values also occur in that source page text.

If validation fails, the proposed table is not added to the Markdown. During a
normal run it is sent to OpenAI as a chart for cautious extraction and
description. During `--local-only`, the image is retained unchanged and remains
eligible for the optional end-of-run API review even when its CLIP chart score
is above `--api-review-below`. Use `--api-review-below 0` to keep that run
strictly local.

Validation is intentionally conservative. Passing it reduces obvious DePlot
errors, but does not prove that every series, row and column association is
correct. Critical research values should still be checked against the paper.

The benchmark runs the same input through each selected backend independently:

```text
PDF → PyMuPDF4LLM → raw Markdown
PDF → Marker       → raw Markdown
PDF → Docling      → raw Markdown
```

Use `convert_pdf.py` for normal research work. Use
`benchmark_backends.py` occasionally to determine whether another extraction
backend produces better reading order, equations, tables, figures or captions
for your particular collection of papers.

During the optional OpenAI review, two or more candidate images extracted from
the same PDF page are treated as possible fragments of one larger figure. The
script temporarily renders the complete source page, analyzes it once, and
adds one combined figure analysis after the final fragment. The temporary page
render is deleted immediately. Single-image pages continue to be analyzed
individually.

## Backend benchmark

Install the optional, much larger comparison dependencies:

```powershell
python -m pip install -r requirements-benchmark.txt
```

Run every backend on exactly the same folder of research PDFs:

```powershell
python benchmark_backends.py "C:\Research\Papers" --overwrite
```

### `benchmark_backends.py` parameters

General syntax:

```powershell
python benchmark_backends.py INPUT [INPUT ...] [OPTIONS]
```

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `inputs` | Yes | — | One or more PDF files and/or directories. For a directory, PDFs directly inside it are included; subdirectories are not searched recursively. Every selected backend receives the same collected PDF set. |
| `--output-dir DIRECTORY` | No | `pdf_backend_benchmark` | Directory in which per-paper backend outputs, the JSON measurements, Markdown report and human scorecard are created. |
| `--backends BACKEND [BACKEND ...]` | No | All three | Backends to run. Valid values are `pymupdf4llm`, `marker` and `docling`. Supply one or more values separated by spaces. |
| `--overwrite` | No | Disabled | Removes and regenerates an existing per-paper/backend benchmark output. Without it, an existing output is reported as a failure and is left unchanged. |
| `-h`, `--help` | No | — | Displays the command-line help and exits. |

Benchmark examples:

```powershell
# Run all three backends on every PDF directly inside a directory
python benchmark_backends.py "C:\Research\Papers" --overwrite

# Compare only PyMuPDF4LLM and Docling
python benchmark_backends.py "C:\Research\Papers" --backends pymupdf4llm docling

# Benchmark two explicitly selected papers and choose an output directory
python benchmark_backends.py "P001.pdf" "P002.pdf" --output-dir "comparison"
```

The benchmark creates:

- native Markdown and artifacts for each paper/backend combination;
- `benchmark_results.json` with timings and structural measurements;
- `benchmark_report.md`;
- `human_quality_scorecard.csv`.

Complete the human scorecard while comparing each result with the source PDF.
Do not select a default backend from heading/table/image counts alone.

## Project layout

- `convert_pdf.py`: documented compatibility entry point.
- `benchmark_backends.py`: three-backend benchmark entry point.
- `pdfmd/cli.py`: command-line orchestration.
- `pdfmd/extraction.py`: PyMuPDF4LLM extraction.
- `pdfmd/routing.py`: figure routing, enrichment, and API review.
- `pdfmd/chart_validation.py`: structural and source-PDF numeric validation of
  proposed DePlot tables.
- `pdfmd/images.py`: Markdown image parsing, atomic output, resizing, and stale
  image handling.
- `pdfmd/models.py`: CLIP and DePlot local models, including CUDA/MPS/CPU
  selection.
- `pdfmd/vision.py`: OpenAI research-figure analysis.
- `pdfmd/cache.py`: versioned cache keys and atomic cache persistence.
- `pdfmd/reporting.py`: run, timing, storage, cleanup, and review reports.
- `pdfmd/benchmark.py`: backend adapters and benchmark reporting.
- `test_convert_pdf.py`: regression and orchestration tests.

Run the test suite with:

```powershell
python -m unittest -v
```

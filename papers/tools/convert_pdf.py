# =============================================================================
# convert_pdf.py — Research-paper PDF to enriched Markdown converter
#
# WHAT IT DOES
#   1. Converts a PDF to Markdown with PyMuPDF4LLM.
#   2. Extracts figures into a sibling "<pdf-name>_images" directory.
#   3. Uses a local CLIP model to classify each figure.
#   4. Attempts to convert confidently detected charts to Markdown tables
#      locally with DePlot, then validates table structure and checks numeric
#      values against the source PDF page text when available.
#   5. Publishes only validated local chart tables. Rejected tables are sent to
#      OpenAI for chart review in a normal run, or retained as candidates for
#      the optional API review in local-only mode.
#   6. Sends confidently detected non-chart figures to OpenAI for a structured
#      scientific explanation, unless local-only mode is selected.
#   7. Holds ambiguous figures for manual review without sending them to an API.
#   8. Caches routing, validated chart tables, and OpenAI analyses.
#   9. Prints image-routing, elapsed-time, API-usage, disk-usage, and cleanup
#      information after a successful run.
#  10. Removes only obsolete images matching PyMuPDF4LLM's generated filename
#      pattern, unless --keep-stale-images is selected.
#
# INSTALL
#   python -m pip install -r requirements.txt
#
# OPENAI KEY (PowerShell; needed unless using --local-only or
# --skip-image-analysis)
#   $env:OPENAI_API_KEY="your-api-key"
#
# USAGE EXAMPLES
#   Normal: local chart tables + OpenAI analysis for non-charts
#     python convert_pdf.py "C:\Research\P001.pdf"
#
#   Use a local initial pass; optionally approve low-score API review afterward
#     python convert_pdf.py "C:\Research\P001.pdf" --local-only
#
#   Use a local initial pass, then automatically perform eligible API reviews
#     python convert_pdf.py "C:\Research\P001.pdf" --local-only --auto-api-review
#
#   Replace existing Markdown and automatically perform eligible API reviews
#     python convert_pdf.py "C:\Research\P001.pdf" --local-only --auto-api-review --overwrite
#
#   Keep the entire run strictly local with no API-review prompt
#     python convert_pdf.py "C:\Research\P001.pdf" --local-only --api-review-below 0
#
#   Change the optional end-of-run API review threshold to 50%
#     python convert_pdf.py "C:\Research\P001.pdf" --local-only --api-review-below 50
#
#   Disable the optional end-of-run API review prompt
#     python convert_pdf.py "C:\Research\P001.pdf" --api-review-below 0
#
#   Extract images but perform no figure analysis
#     python convert_pdf.py "C:\Research\P001.pdf" --skip-image-analysis
#
#   Ignore all cached figure results and process again
#     python convert_pdf.py "C:\Research\P001.pdf" --reanalyze-images
#
#   Disable local chart routing and send every figure to OpenAI
#     python convert_pdf.py "C:\Research\P001.pdf" --no-local-chart-tables
#
#   Compare extraction backends on the same folder of research PDFs
#     python -m pip install -r requirements-benchmark.txt
#     python benchmark_backends.py "C:\Research\Papers" --overwrite
#
# INPUT PARAMETERS
#   pdf_file
#       Required PDF filename, relative path, or absolute path.
#   --model MODEL
#       OpenAI vision-capable model used for non-chart figures.
#       Default: OPENAI_VISION_MODEL or "gpt-5.5".
#   --classifier-model MODEL
#       Local Hugging Face CLIP model used to distinguish charts from
#       non-charts. Default: "openai/clip-vit-base-patch32".
#   --chart-model MODEL
#       Local Hugging Face chart-to-table model.
#       Default: "google/deplot".
#   --chart-threshold NUMBER
#       Confidence threshold in the range (0.5, 1.0]. Images between the chart
#       and non-chart confidence boundaries are held for manual review.
#       Default: 0.65.
#   --reanalyze-images
#       Ignores cached classification, table, and OpenAI analysis results.
#   --skip-image-analysis
#       Extracts figures but performs neither local nor OpenAI analysis.
#   --local-only
#       Prevents automatic OpenAI calls during the initial pass. The optional
#       end-of-run review can still be approved; use --api-review-below 0 for a
#       strictly local run.
#   --no-local-chart-tables
#       Disables local classification and sends all figures to OpenAI.
#   --api-review-below PERCENT
#       After the initial summary, offers to send non-API images with local
#       chart confidence below this percentage to OpenAI for a second opinion.
#       Default: 65. Use 0 to disable the review prompt.
#   --auto-api-review
#       Automatically approves eligible end-of-run OpenAI reviews without
#       asking in the terminal. It requires --api-review-below to be greater
#       than 0 and cannot be combined with --skip-image-analysis.
#   --api-max-image-edge PIXELS
#       Downscales oversized API submissions in memory while preserving the
#       original extracted image. Default: 2048. Use 0 to disable resizing.
#   --keep-stale-images
#       Keeps obsolete PyMuPDF4LLM-generated image files. By default, generated
#       images no longer referenced by the new Markdown are removed.
#   --overwrite
#       Replaces an existing Markdown output without asking for confirmation.
#       This affects only the Markdown overwrite question.
#
# OUTPUTS
#   <pdf-name>.md
#   <pdf-name>_images/                 extracted images
#   <pdf-name>_images/figure_analysis_cache.json
#
# NOTES
#   - Local Hugging Face models are downloaded on first use and shared with
#     other projects through the Hugging Face cache.
#   - DePlot output is never inserted solely because CLIP confidently detected
#     a chart. Structural validation and, when available, a source-PDF numeric
#     cross-check must pass first. This reduces risk but is not a mathematical
#     proof that every row/column association is correct.
#   - Rejected local tables remain visible in the terminal report and are
#     eligible for OpenAI or manual review; they are not placed in Markdown.
#   - The final cleanup guide never deletes the Markdown, current images, cache,
#     or models. Only obsolete generated images are removed automatically;
#     select --keep-stale-images to retain those too.
#   - The implementation is split across the pdfmd/ package: CLI, extraction,
#     routing, image/Markdown handling, cache, local models, API analysis,
#     reporting, and backend benchmarking.
#   - The benchmark runner never changes the converter's default backend. Its
#     human scorecard must be completed before making that decision.
# =============================================================================

from pdfmd import *


if __name__ == "__main__":
    main()

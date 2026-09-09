from contextlib import nullcontext, redirect_stdout
from io import StringIO
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

import convert_pdf
from pdfmd import benchmark


class FakeLocalModels:
    def __init__(self, chart_probability: float) -> None:
        self.chart_probability = chart_probability

    def classify_chart_probability(self, image_path: Path) -> float:
        return self.chart_probability

    def extract_chart_table(self, image_path: Path) -> str:
        return "Series | Value<0x0A>A | 10<0x0A>B | 20"


class FailingLocalModels:
    def classify_chart_probability(self, image_path: Path) -> float:
        raise RuntimeError("classifier unavailable")


class InvalidChartLocalModels(FakeLocalModels):
    def extract_chart_table(self, image_path: Path) -> str:
        return (
            "TITLE | Multi-panel result | | <0x0A>"
            "Method | Value | Series | Score<0x0A>"
            "Base | 10 | A | 10<0x0A>"
            "Base | 20 | B | 20"
        )


class CountingLocalModels(FakeLocalModels):
    def __init__(self, chart_probability: float) -> None:
        super().__init__(chart_probability)
        self.classifier_calls = 0

    def classify_chart_probability(self, image_path: Path) -> float:
        self.classifier_calls += 1
        return super().classify_chart_probability(image_path)


class FakeResponses:
    def create(self, **kwargs):
        return SimpleNamespace(
            output_text=json.dumps(
                {
                    "figure_type": "scientific diagram",
                    "clip_agreement": "agree",
                    "one_line_finding": (
                        "The diagram shows the tested processing workflow."
                    ),
                    "uncertainty": "Some small labels are unreadable.",
                    "table_extracted": False,
                    "analysis_markdown": (
                        "**Purpose:** Shows the tested processing workflow.\n\n"
                        "**Key observations:** The stages proceed from input "
                        "to output."
                    ),
                }
            ),
            usage=SimpleNamespace(
                input_tokens=100,
                output_tokens=25,
                total_tokens=125,
            ),
        )


class FakeClient:
    responses = FakeResponses()


class ConverterTests(unittest.TestCase):
    def setUp(self) -> None:
        from PIL import Image

        self.temporary_directory = tempfile.TemporaryDirectory(dir=".")
        self.root = Path(self.temporary_directory.name)
        self.image = self.root / "figure.png"
        Image.new("RGB", (2, 2), "white").save(self.image)
        self.markdown = "![](figure.png)"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def enrich(
        self,
        *,
        summary: convert_pdf.RunSummary,
        local_models,
        classifier_model: str,
        cache_name: str,
        client=None,
        local_only: bool = False,
        chart_threshold: float = 0.65,
        markdown: str | None = None,
    ) -> str:
        return convert_pdf.enrich_markdown(
            markdown=self.markdown if markdown is None else markdown,
            document_directory=self.root,
            client=client,
            openai_model="test-openai",
            local_models=local_models,
            classifier_model=classifier_model,
            chart_model="test-chart",
            chart_threshold=chart_threshold,
            cache_file=self.root / cache_name,
            reanalyze=False,
            skip_analysis=False,
            local_only=local_only,
            use_local_chart_tables=True,
            summary=summary,
        )

    def test_chart_is_converted_locally_without_api_call(self) -> None:
        summary = convert_pdf.RunSummary("chart-paper.pdf")
        output = self.enrich(
            summary=summary,
            local_models=FakeLocalModels(0.9),
            classifier_model="chart-classifier",
            cache_name="chart-cache.json",
            client=FakeClient(),
        )

        self.assertIn("### Chart data", output)
        self.assertNotIn("Locally", output)
        self.assertNotIn("confidence", output)
        self.assertIn("| A | 10 |", output)
        self.assertEqual(summary.records[0].status, "chart_local")
        self.assertEqual(summary.openai_calls, 0)

    def test_chart_result_is_reused_from_cache(self) -> None:
        first_summary = convert_pdf.RunSummary("chart-paper.pdf")
        first_output = self.enrich(
            summary=first_summary,
            local_models=FakeLocalModels(0.9),
            classifier_model="cached-classifier",
            cache_name="cached-chart.json",
            client=FakeClient(),
        )

        cached_summary = convert_pdf.RunSummary("chart-paper.pdf")
        cached_output = self.enrich(
            summary=cached_summary,
            local_models=None,
            classifier_model="cached-classifier",
            cache_name="cached-chart.json",
            client=FakeClient(),
        )

        self.assertEqual(cached_output, first_output)
        self.assertTrue(cached_summary.records[0].content_from_cache)
        self.assertEqual(cached_summary.classifier_calls, 0)
        self.assertEqual(cached_summary.chart_model_calls, 0)
        self.assertEqual(cached_summary.openai_calls, 0)

    def test_invalid_local_chart_table_is_not_published(self) -> None:
        summary = convert_pdf.RunSummary("chart-paper.pdf")
        output = self.enrich(
            summary=summary,
            local_models=InvalidChartLocalModels(0.9),
            classifier_model="invalid-chart-classifier",
            cache_name="invalid-chart-cache.json",
            client=None,
            local_only=True,
        )

        self.assertEqual(output, self.markdown)
        self.assertNotIn("### Chart data", output)
        self.assertEqual(summary.records[0].status, "chart_rejected")
        self.assertIn("repeated row labels", summary.records[0].details)

        candidates = convert_pdf.api_review_candidates(summary, 65.0)
        self.assertEqual(candidates, summary.records)

        cached_summary = convert_pdf.RunSummary("chart-paper.pdf")
        cached_output = self.enrich(
            summary=cached_summary,
            local_models=None,
            classifier_model="invalid-chart-classifier",
            cache_name="invalid-chart-cache.json",
            client=None,
            local_only=True,
        )

        self.assertEqual(cached_output, self.markdown)
        self.assertTrue(cached_summary.records[0].content_from_cache)
        self.assertEqual(cached_summary.chart_model_calls, 0)

    def test_invalid_local_chart_table_is_reviewed_in_normal_run(self) -> None:
        summary = convert_pdf.RunSummary("chart-paper.pdf")
        output = self.enrich(
            summary=summary,
            local_models=InvalidChartLocalModels(0.9),
            classifier_model="invalid-chart-api-classifier",
            cache_name="invalid-chart-api-cache.json",
            client=FakeClient(),
        )

        self.assertNotIn("### Chart data", output)
        self.assertIn("### Figure analysis", output)
        self.assertEqual(summary.records[0].status, "openai")
        self.assertIn(
            "local table validation rejected it",
            summary.records[0].details,
        )
        self.assertEqual(summary.openai_calls, 1)

    def test_non_chart_is_analyzed_by_openai(self) -> None:
        summary = convert_pdf.RunSummary("diagram-paper.pdf")
        terminal = StringIO()
        with redirect_stdout(terminal):
            output = self.enrich(
                summary=summary,
                local_models=FakeLocalModels(0.1),
                classifier_model="non-chart-classifier",
                cache_name="non-chart-cache.json",
                client=FakeClient(),
            )

        self.assertIn("### Figure analysis", output)
        self.assertNotIn("API review", output)
        self.assertNotIn("CLIP", output)
        self.assertNotIn("confidence", output)
        rendered_terminal = terminal.getvalue()
        self.assertIn("Detected figure type: scientific diagram", rendered_terminal)
        self.assertIn(
            "Agreement/disagreement with CLIP: agreement",
            rendered_terminal,
        )
        self.assertIn(
            "One-line finding: The diagram shows the tested processing workflow.",
            rendered_terminal,
        )
        self.assertIn(
            "Unreadable or uncertain content: Some small labels are unreadable.",
            rendered_terminal,
        )
        self.assertIn("Table extracted: no", rendered_terminal)
        self.assertEqual(summary.records[0].status, "openai")
        self.assertEqual(summary.openai_calls, 1)
        self.assertEqual(summary.openai_input_tokens, 100)
        self.assertEqual(summary.openai_output_tokens, 25)
        self.assertEqual(summary.openai_total_tokens, 125)
        self.assertEqual(
            summary.openai_image_bytes_sent,
            self.image.stat().st_size,
        )

    def test_ambiguous_image_is_not_sent_to_api(self) -> None:
        summary = convert_pdf.RunSummary("ambiguous-paper.pdf")
        output = self.enrich(
            summary=summary,
            local_models=FakeLocalModels(0.5),
            classifier_model="ambiguous-classifier",
            cache_name="ambiguous-cache.json",
            client=None,
        )

        self.assertEqual(output, self.markdown)
        self.assertEqual(summary.records[0].status, "ambiguous")
        self.assertEqual(summary.openai_calls, 0)

    def test_low_score_local_image_can_receive_api_review(self) -> None:
        cache_name = "review-cache.json"
        initial_summary = convert_pdf.RunSummary("review-paper.pdf")
        initial_markdown = self.enrich(
            summary=initial_summary,
            local_models=FakeLocalModels(0.1),
            classifier_model="review-classifier",
            cache_name=cache_name,
            client=None,
            local_only=True,
        )

        candidates = convert_pdf.api_review_candidates(
            initial_summary,
            threshold_percent=65.0,
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].status, "local_only_non_chart")

        reviewed_markdown, review_summary = convert_pdf.perform_api_review(
            markdown=initial_markdown,
            candidates=candidates,
            client=FakeClient(),
            openai_model="test-openai",
            threshold_percent=65.0,
            cache_file=self.root / cache_name,
            reanalyze=False,
        )

        self.assertIn("### Figure analysis", reviewed_markdown)
        self.assertNotIn("API review", reviewed_markdown)
        self.assertNotIn("Initial pass:", reviewed_markdown)
        self.assertNotIn("chart confidence", reviewed_markdown)
        self.assertEqual(review_summary.api_calls, 1)
        self.assertEqual(review_summary.total_tokens, 125)
        self.assertTrue(review_summary.records[0].succeeded)

        cached_markdown, cached_summary = convert_pdf.perform_api_review(
            markdown=initial_markdown,
            candidates=candidates,
            client=None,
            openai_model="test-openai",
            threshold_percent=65.0,
            cache_file=self.root / cache_name,
            reanalyze=False,
        )

        self.assertIn("### Figure analysis", cached_markdown)
        self.assertEqual(cached_summary.api_calls, 0)
        self.assertEqual(cached_summary.cache_items_reused, 1)
        self.assertTrue(cached_summary.records[0].succeeded)

    def test_api_review_excludes_images_already_analyzed_by_openai(self) -> None:
        summary = convert_pdf.RunSummary("review-paper.pdf")
        summary.add(
            "already-analyzed.png",
            "openai",
            "non-chart visual analysis via OpenAI",
            chart_probability=0.1,
            image_path=self.image,
        )
        summary.add(
            "local.png",
            "local_only_non_chart",
            "retained without API analysis",
            chart_probability=0.2,
            image_path=self.image,
        )

        candidates = convert_pdf.api_review_candidates(
            summary,
            threshold_percent=65.0,
        )

        self.assertEqual(
            [record.filename for record in candidates],
            ["local.png"],
        )

    def test_api_review_prompt_and_default_threshold(self) -> None:
        parsed = convert_pdf.build_argument_parser().parse_args(["paper.pdf"])
        self.assertEqual(parsed.api_review_below, 65.0)
        self.assertFalse(parsed.auto_api_review)
        self.assertFalse(parsed.overwrite)

        with patch("builtins.input", return_value="yes"):
            approved = convert_pdf.confirm_api_review(
                candidate_count=3,
                threshold_percent=65.0,
            )

        self.assertTrue(approved)

    def test_automatic_review_and_overwrite_flags_are_parsed(self) -> None:
        parsed = convert_pdf.build_argument_parser().parse_args(
            [
                "paper.pdf",
                "--local-only",
                "--auto-api-review",
                "--overwrite",
            ]
        )

        self.assertTrue(parsed.local_only)
        self.assertTrue(parsed.auto_api_review)
        self.assertTrue(parsed.overwrite)

    def test_image_path_with_parentheses_is_processed(self) -> None:
        image = self.root / "figure(appendix).png"
        image.write_bytes(b"parenthesized-image")
        summary = convert_pdf.RunSummary("paper.pdf")

        output = self.enrich(
            summary=summary,
            local_models=FakeLocalModels(0.1),
            classifier_model="parentheses-classifier",
            cache_name="parentheses-cache.json",
            client=None,
            local_only=True,
            markdown="![](figure(appendix).png)",
        )

        self.assertEqual(output, "![](figure(appendix).png)")
        self.assertEqual(summary.records[0].filename, image.name)

    def test_duplicate_image_references_receive_distinct_reviews(self) -> None:
        source = "![](figure.png)\n\nFirst\n\n![](figure.png)\n\nSecond"
        summary = convert_pdf.RunSummary("paper.pdf")
        initial = self.enrich(
            summary=summary,
            local_models=FakeLocalModels(0.1),
            classifier_model="duplicate-classifier",
            cache_name="duplicate-cache.json",
            client=None,
            local_only=True,
            markdown=source,
        )
        candidates = convert_pdf.api_review_candidates(summary, 65.0)

        reviewed, result = convert_pdf.perform_api_review(
            markdown=initial,
            candidates=candidates,
            client=FakeClient(),
            openai_model="test-openai",
            threshold_percent=65.0,
            cache_file=self.root / "duplicate-cache.json",
            reanalyze=False,
        )

        self.assertEqual(len(candidates), 2)
        self.assertEqual(reviewed.count("### Figure analysis"), 2)
        self.assertNotIn("API review", reviewed)
        self.assertNotIn("Initial pass", reviewed)
        self.assertEqual(sum(item.succeeded for item in result.records), 2)

    def test_same_page_fragments_receive_one_grouped_api_analysis(self) -> None:
        pdf = self.root / "paper.pdf"
        pdf.write_bytes(b"test-pdf")
        markdown_parts: list[str] = []
        summary = convert_pdf.RunSummary("paper.pdf")

        for index in range(1, 4):
            filename = f"paper.pdf-0005-0{index}.png"
            image = self.root / filename
            image.write_bytes(self.image.read_bytes())
            markdown_image = f"![]({filename})"
            markdown_parts.append(markdown_image)
            summary.add(
                filename,
                "local_only_non_chart",
                "retained without API analysis",
                chart_probability=0.1,
                image_path=image,
                image_reference=filename,
                markdown_image=markdown_image,
                surrounding_text="Figure 4: complete framework diagram.",
                occurrence_index=index - 1,
                clip_classification="non-chart",
            )

        terminal = StringIO()
        with (
            patch(
                "pdfmd.routing.rendered_pdf_page_for_analysis",
                return_value=nullcontext(self.image),
            ),
            redirect_stdout(terminal),
        ):
            reviewed, result = convert_pdf.perform_api_review(
                markdown="\n\n".join(markdown_parts),
                candidates=summary.records,
                client=FakeClient(),
                openai_model="test-openai",
                threshold_percent=65.0,
                cache_file=self.root / "grouped-cache.json",
                reanalyze=False,
            )

        self.assertEqual(result.candidate_images, 3)
        self.assertEqual(result.grouped_images, 3)
        self.assertEqual(result.api_calls, 1)
        self.assertEqual(len(result.records), 1)
        self.assertEqual(reviewed.count("### Figure analysis"), 1)
        self.assertIn(
            "paper.pdf page 5 (3 grouped fragments)",
            terminal.getvalue(),
        )

    def test_routing_cache_changes_when_threshold_changes(self) -> None:
        cache_name = "threshold-cache.json"
        first_models = CountingLocalModels(0.7)
        first_summary = convert_pdf.RunSummary("paper.pdf")
        first = self.enrich(
            summary=first_summary,
            local_models=first_models,
            classifier_model="threshold-classifier",
            cache_name=cache_name,
            client=None,
            chart_threshold=0.65,
        )

        second_models = CountingLocalModels(0.7)
        second_summary = convert_pdf.RunSummary("paper.pdf")
        second = self.enrich(
            summary=second_summary,
            local_models=second_models,
            classifier_model="threshold-classifier",
            cache_name=cache_name,
            client=None,
            chart_threshold=0.75,
        )

        self.assertIn("### Chart data", first)
        self.assertEqual(second, self.markdown)
        self.assertEqual(second_models.classifier_calls, 1)

    def test_classifier_failure_is_eligible_for_api_review(self) -> None:
        summary = convert_pdf.RunSummary("paper.pdf")
        initial = self.enrich(
            summary=summary,
            local_models=FailingLocalModels(),
            classifier_model="broken-classifier",
            cache_name="broken-cache.json",
            client=None,
        )

        candidates = convert_pdf.api_review_candidates(summary, 65.0)
        reviewed, result = convert_pdf.perform_api_review(
            markdown=initial,
            candidates=candidates,
            client=FakeClient(),
            openai_model="test-openai",
            threshold_percent=65.0,
            cache_file=self.root / "broken-cache.json",
            reanalyze=False,
        )

        self.assertEqual(summary.records[0].status, "classification_failed")
        self.assertEqual(len(candidates), 1)
        self.assertIn("### Figure analysis", reviewed)
        self.assertNotIn("classification failed", reviewed)
        self.assertTrue(result.records[0].succeeded)

    def test_atomic_markdown_write_preserves_existing_file_on_replace_failure(
        self,
    ) -> None:
        output = self.root / "paper.md"
        output.write_text("old content", encoding="utf-8")

        with patch.object(Path, "replace", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                convert_pdf.atomic_write_text(output, "new content")

        self.assertEqual(output.read_text(encoding="utf-8"), "old content")
        self.assertEqual(list(self.root.glob(".paper.md.*.tmp")), [])

    def test_mps_is_selected_when_cuda_is_unavailable(self) -> None:
        torch_module = SimpleNamespace(
            cuda=SimpleNamespace(is_available=lambda: False),
            backends=SimpleNamespace(
                mps=SimpleNamespace(is_available=lambda: True)
            ),
        )

        self.assertEqual(
            convert_pdf.select_torch_device(torch_module),
            "mps",
        )

    def test_api_image_is_resized_without_changing_original(self) -> None:
        from PIL import Image

        image = self.root / "large.png"
        Image.new("RGB", (100, 50), "white").save(image)
        original = image.read_bytes()

        prepared = convert_pdf.prepare_image_for_api(image, max_edge=40)

        self.assertTrue(prepared.was_resized)
        self.assertEqual(image.read_bytes(), original)
        self.assertLessEqual(prepared.original_bytes, len(original))

    def test_only_unreferenced_generated_images_are_removed(self) -> None:
        image_folder = self.root / "paper_images"
        image_folder.mkdir()
        current = image_folder / "paper.pdf-0001-01.png"
        stale = image_folder / "paper.pdf-0002-01.png"
        unrelated = image_folder / "notes.png"
        current.write_bytes(b"current")
        stale.write_bytes(b"stale")
        unrelated.write_bytes(b"keep")
        input_file = self.root / "paper.pdf"
        input_file.write_bytes(b"pdf")
        markdown = "![](paper_images/paper.pdf-0001-01.png)"

        count, size = convert_pdf.remove_stale_generated_images(
            image_folder=image_folder,
            input_file=input_file,
            markdown=markdown,
            keep_stale=False,
        )

        self.assertEqual((count, size), (1, len(b"stale")))
        self.assertTrue(current.exists())
        self.assertFalse(stale.exists())
        self.assertTrue(unrelated.exists())

    def test_deplot_output_is_converted_to_markdown_table(self) -> None:
        table = convert_pdf.deplot_output_to_markdown(
            "Method | Accuracy<0x0A>A | 82.5<0x0A>B | 75.0"
        )

        self.assertEqual(
            table,
            "\n".join(
                [
                    "| Method | Accuracy |",
                    "| --- | --- |",
                    "| A | 82.5 |",
                    "| B | 75.0 |",
                ]
            ),
        )

    def test_chart_table_validation_accepts_corroborated_values(self) -> None:
        validation = convert_pdf.validate_deplot_table(
            "Method | Accuracy<0x0A>A | 82.5<0x0A>B | 75.0",
            source_text="A achieved 82.5 percent and B achieved 75.0 percent.",
        )

        self.assertTrue(validation.accepted)
        self.assertEqual(validation.numeric_values_checked, 2)
        self.assertEqual(validation.numeric_values_matched, 2)
        self.assertIn("| A | 82.5 |", validation.markdown)

    def test_chart_table_validation_rejects_p001_figure_1_shape(self) -> None:
        validation = convert_pdf.validate_deplot_table(
            (
                "TITLE | Agent: AppWorld | | <0x0A>"
                "Method | Value 1 | Value 2 | Accuracy<0x0A>"
                "Base LLM | 42.4 | 46.0 | 46.4<0x0A>"
                "ACE | 70.0 | 72.3 | 80.0<0x0A>"
                "Base LLM | 67.5 | 67.0 | 71.5"
            ),
            source_text=(
                "42.4 46.0 46.4 70.0 72.3 80.0 67.5 67.0 71.5"
            ),
        )

        self.assertFalse(validation.accepted)
        self.assertIn(
            "repeated row labels",
            validation.summary,
        )

    def test_chart_table_validation_rejects_uncorroborated_values(self) -> None:
        validation = convert_pdf.validate_deplot_table(
            "Step | Tokens<0x0A>20 | 10922<0x0A>30 | 9322",
            source_text="The source reports step 60 with 18,282 tokens.",
        )

        self.assertFalse(validation.accepted)
        self.assertIn("could be corroborated", validation.summary)

    def test_summary_reports_timing_storage_and_cleanup(self) -> None:
        output_file = self.root / "paper.md"
        output_file.write_text("# Paper", encoding="utf-8")
        image_folder = self.root / "paper_images"
        image_folder.mkdir()
        extracted_image = image_folder / "figure.png"
        extracted_image.write_bytes(b"figure-data")
        cache_file = image_folder / "figure_analysis_cache.json"
        cache_file.write_text("{}", encoding="utf-8")

        summary = convert_pdf.RunSummary(
            pdf_name="paper.pdf",
            started_at="2026-01-01T10:00:00+00:00",
            finished_at="2026-01-01T10:00:02+00:00",
            total_seconds=2.0,
        )
        summary.storage = convert_pdf.build_storage_report(
            input_pdf=self.image,
            output_file=output_file,
            image_folder=image_folder,
            cache_file=cache_file,
            artifacts_before_bytes=0,
            model_cache_before={},
            model_cache_after={},
        )

        report = StringIO()
        with redirect_stdout(report):
            summary.print_report()

        rendered = report.getvalue()
        self.assertIn("Elapsed time", rendered)
        self.assertIn("Total run: 2.00 s", rendered)
        self.assertIn("Disk usage", rendered)
        self.assertIn("Managed output total now", rendered)
        self.assertIn("Optional cleanup", rendered)
        self.assertIn(str(output_file), rendered)

    def test_benchmark_uses_the_same_pdf_for_each_backend(self) -> None:
        pdf = self.root / "paper.pdf"
        pdf.write_bytes(b"pdf")
        output_dir = self.root / "benchmark"

        def fake_converter(source: Path, destination: Path) -> Path:
            output = destination / f"{source.stem}.md"
            convert_pdf.atomic_write_text(
                output,
                "# Paper\n\n| A | B |\n| --- | --- |\n| 1 | 2 |",
            )
            return output

        fake_backends = {
            "pymupdf4llm": fake_converter,
            "docling": fake_converter,
        }
        with patch.dict(benchmark.CONVERTERS, fake_backends, clear=True):
            results, report = benchmark.run_benchmark(
                inputs=[pdf],
                output_dir=output_dir,
                backends=list(fake_backends),
                overwrite=False,
            )

        self.assertEqual(
            [(item.pdf, item.backend) for item in results],
            [
                ("paper.pdf", "pymupdf4llm"),
                ("paper.pdf", "docling"),
            ],
        )
        self.assertTrue(all(item.succeeded for item in results))
        self.assertTrue(report.exists())
        self.assertTrue(
            (output_dir / "human_quality_scorecard.csv").exists()
        )


if __name__ == "__main__":
    unittest.main()

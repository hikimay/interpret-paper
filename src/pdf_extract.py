#!/usr/bin/env python3
"""Extract structured text from a PDF for paper interpretation."""

import json
import re
import sys
from pathlib import Path

import click
import fitz  # PyMuPDF


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def extract_pdf(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)

    # Collect font sizes to determine heading thresholds
    all_sizes: list[float] = []
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        all_sizes.append(span["size"])

    if not all_sizes:
        return {"title": Path(pdf_path).stem, "authors": "", "sections": [], "page_count": len(doc)}

    body_size = sorted(all_sizes)[len(all_sizes) // 2]  # median ≈ body text
    heading_threshold = body_size * 1.15

    sections: list[dict] = []
    current: dict = {"title": "前文", "content": ""}

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                line_text = " ".join(s["text"] for s in line["spans"]).strip()
                if not line_text:
                    continue

                max_size = max(s["size"] for s in line["spans"])
                is_bold = any(("Bold" in s.get("font", "") or s.get("flags", 0) & 2**4)
                               for s in line["spans"])

                if max_size >= heading_threshold and len(line_text) < 120 and is_bold:
                    if current["content"].strip():
                        sections.append(current)
                    current = {"title": line_text, "content": ""}
                else:
                    current["content"] += line_text + "\n"

    if current["content"].strip():
        sections.append(current)

    # Heuristic: title is the largest text on page 0
    page0_spans = []
    for block in doc[0].get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if span["text"].strip():
                    page0_spans.append(span)

    page0_spans.sort(key=lambda s: -s["size"])
    title = page0_spans[0]["text"].strip() if page0_spans else Path(pdf_path).stem

    # Authors: second-largest font cluster on page 0
    authors = ""
    if len(page0_spans) > 1:
        second_size = page0_spans[1]["size"]
        author_spans = [s["text"].strip() for s in page0_spans
                        if abs(s["size"] - second_size) < 0.5 and s["text"].strip() != title]
        authors = ", ".join(author_spans[:6])

    return {
        "title": title,
        "authors": authors,
        "sections": sections,
        "page_count": len(doc),
        "source": str(Path(pdf_path).resolve()),
    }


@click.command()
@click.argument("pdf_path")
@click.option("--output", "-o", default="-", help="Output file (default: stdout)")
def main(pdf_path: str, output: str) -> None:
    """Extract structured text from PDF_PATH as JSON."""
    result = extract_pdf(pdf_path)
    json_str = json.dumps(result, ensure_ascii=False, indent=2)

    if output == "-":
        print(json_str)
    else:
        Path(output).write_text(json_str, encoding="utf-8")
        click.echo(f"Saved to {output}", err=True)


if __name__ == "__main__":
    main()

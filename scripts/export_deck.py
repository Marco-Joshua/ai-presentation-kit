#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(args: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def chrome_binary() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError("Chrome 또는 Chromium을 찾지 못했습니다.")


def make_contact_sheet(images: list[Path], target: Path) -> None:
    if not images:
        raise RuntimeError("PDF에서 렌더된 페이지가 없습니다.")
    inputs: list[str] = []
    for image in images:
        inputs.extend(["-i", str(image)])
    columns = 3
    width, height = 640, 360
    prepared = ";".join(f"[{index}:v]scale={width}:{height}[v{index}]" for index in range(len(images)))
    streams = "".join(f"[v{index}]" for index in range(len(images)))
    layout = "|".join(f"{(index % columns) * width}_{(index // columns) * height}" for index in range(len(images)))
    run([
        "ffmpeg", "-y", "-loglevel", "error", *inputs,
        "-filter_complex", f"{prepared};{streams}xstack=inputs={len(images)}:layout={layout}:fill=#111111[out]",
        "-map", "[out]", str(target),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description="HTML 장표를 PDF로 내보내고 전 페이지를 검사합니다.")
    parser.add_argument("html", type=Path)
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()

    html = args.html.expanduser().resolve()
    if not html.exists():
        raise FileNotFoundError(html)
    if not shutil.which("pdfinfo") or not shutil.which("pdftoppm") or not shutil.which("ffmpeg"):
        run([str(ROOT / "scripts" / "bootstrap.sh")])

    pdf = (args.pdf or ROOT / "output" / f"{html.stem}.pdf").expanduser().resolve()
    pdf.parent.mkdir(parents=True, exist_ok=True)
    run([
        chrome_binary(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri(),
    ])

    info = run(["pdfinfo", str(pdf)], capture=True).stdout
    pages_line = next((line for line in info.splitlines() if line.startswith("Pages:")), "")
    pages = int(pages_line.split(":", 1)[1].strip()) if pages_line else 0
    if pages <= 0:
        raise RuntimeError("PDF 페이지 수를 확인하지 못했습니다.")

    qa_dir = pdf.parent / "qa" / pdf.stem
    qa_dir.mkdir(parents=True, exist_ok=True)
    prefix = qa_dir / "slide"
    run(["pdftoppm", "-png", "-r", "96", str(pdf), str(prefix)])
    images = sorted(qa_dir.glob("slide-*.png"))
    if len(images) != pages:
        raise RuntimeError(f"PDF {pages}쪽과 렌더 이미지 {len(images)}장이 일치하지 않습니다.")
    contact = qa_dir / "contact-sheet.png"
    make_contact_sheet(images, contact)
    (qa_dir / "report.json").write_text(json.dumps({
        "pdf": str(pdf),
        "pages": pages,
        "renderedPages": len(images),
        "contactSheet": str(contact),
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"✓ PDF: {pdf} · {pages}쪽")
    print(f"✓ QA: {contact}")


if __name__ == "__main__":
    main()

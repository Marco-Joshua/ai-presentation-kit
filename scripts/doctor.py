#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def good(label: str, detail: str = "") -> None:
    print(f"✓ {label}{' · ' + detail if detail else ''}")


def bad(label: str, detail: str = "") -> None:
    print(f"✗ {label}{' · ' + detail if detail else ''}")


def crier_root() -> Path | None:
    candidates = [
        os.environ.get("CRIER_HOME"),
        str(Path.home() / ".crier"),
        str(ROOT / ".tools" / "crier"),
    ]
    for value in candidates:
        if value and (Path(value) / "bin" / "crier").exists():
            return Path(value)
    return None


def main() -> int:
    failed = False
    for command in ("node", "npm", "ffmpeg", "ffprobe", "pdfinfo", "pdftoppm"):
        if shutil.which(command):
            good(command, shutil.which(command) or "")
        else:
            bad(command, "없음")
            failed = True

    remotion = ROOT / "video" / "node_modules" / ".bin" / "remotion"
    if remotion.exists():
        good("Remotion", str(remotion))
    else:
        bad("Remotion", "scripts/bootstrap.sh를 실행하세요")
        failed = True

    crier = crier_root()
    if not crier:
        bad("Crier/Supertonic", "scripts/bootstrap.sh를 실행하세요")
        failed = True
    else:
        try:
            subprocess.run([str(crier / "bin" / "crier"), "start"], check=True, capture_output=True)
            config = json.loads((crier / "config.json").read_text())
            port = int(config.get("port", 7788))
            payload = json.dumps({
                "text": "설치 확인입니다.",
                "voice": "F2",
                "lang": "ko",
                "speed": 1.08,
                "steps": 8,
                "response_format": "wav",
            }, ensure_ascii=False).encode()
            request = urllib.request.Request(
                f"http://127.0.0.1:{port}/v1/tts",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=600) as response:
                audio = response.read()
            if len(audio) <= 44:
                raise RuntimeError("빈 WAV가 반환됐습니다")
            with tempfile.NamedTemporaryFile(suffix=".wav") as sample:
                sample.write(audio)
                sample.flush()
                probe = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", sample.name],
                    check=True, capture_output=True, text=True,
                )
                if float(probe.stdout.strip()) <= 0:
                    raise RuntimeError("음성 길이가 0초입니다")
            good("Crier/Supertonic", f"F2 · 127.0.0.1:{port}")
        except Exception as exc:
            bad("Crier/Supertonic", f"음성 데몬 확인 실패: {exc}")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

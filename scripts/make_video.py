#!/usr/bin/env python3
"""정지 장표 방식 대신 동적 영상 렌더러로 안내합니다."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) >= 2:
        candidate = Path(sys.argv[1]).expanduser()
        if candidate.suffix == ".json" and candidate.exists():
            payload = json.loads(candidate.read_text())
            if isinstance(payload, dict) and payload.get("scenes"):
                command = [sys.executable, str(ROOT / "scripts" / "render_video.py"), str(candidate)]
                command.extend(sys.argv[2:])
                return subprocess.call(command)

    print("정지된 PPT 이미지에 음성만 붙이는 방식은 사용하지 않습니다.")
    print("동적 영상은 manifest.json을 만든 뒤 다음 명령으로 생성하세요:")
    print("  python3 scripts/render_video.py manifest.json --output output/final.mp4")
    print("고품질 기준 예제:")
    print("  python3 scripts/render_video.py examples/customer-support-weekly-20260827/manifest.json")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

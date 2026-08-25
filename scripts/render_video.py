#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO = ROOT / "video"
PUBLIC = VIDEO / "public"
FPS = 30

PRONUNCIATION = {
    "AI": "에이아이",
    "Codex": "코덱스",
    "Claude Code": "클로드 코드",
    "Claude": "클로드",
    "ChatGPT": "챗지피티",
    "PROJECT_STATE": "프로젝트 스테이트",
    "refs": "레퍼런스",
    "STT": "에스티티",
    "Notion": "노션",
    "Slack": "슬랙",
    "GitHub": "깃허브",
    "Pull Request": "풀 리퀘스트",
    "PR": "풀 리퀘스트",
    "HTML": "에이치티엠엘",
    "PDF": "피디에프",
    "PPT": "피피티",
    "MARCO": "마르코",
}


def run(args: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=capture)


def crier_root() -> Path | None:
    candidates = [os.environ.get("CRIER_HOME"), str(Path.home() / ".crier"), str(ROOT / ".tools" / "crier")]
    for value in candidates:
        if value and (Path(value) / "bin" / "crier").exists():
            return Path(value)
    return None


def ensure_runtime() -> Path:
    crier = crier_root()
    remotion = VIDEO / "node_modules" / ".bin" / "remotion"
    if crier and remotion.exists() and shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return crier
    run([str(ROOT / "scripts" / "bootstrap.sh")])
    crier = crier_root()
    if not crier:
        raise RuntimeError("Crier 설치를 찾지 못했습니다.")
    return crier


def duration(path: Path) -> float:
    result = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], capture=True)
    return float(result.stdout.strip())


def clean_for_speech(text: str, korean_module) -> str:
    for source, spoken in sorted(PRONUNCIATION.items(), key=lambda pair: -len(pair[0])):
        text = text.replace(source, spoken)
    text = text.replace("→", "에서 ").replace("·", ", ")
    text = re.sub(r"\s+", " ", text).strip()
    return korean_module.normalize(text)


def resolve_asset(path_value: str, manifest_path: Path) -> Path:
    raw = Path(path_value).expanduser()
    candidates = [raw] if raw.is_absolute() else [manifest_path.parent / raw, ROOT / raw]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f"이미지 에셋을 찾지 못했습니다: {path_value}")


def copy_asset(path_value: str, manifest_path: Path, run_dir: Path) -> str:
    source = resolve_asset(path_value, manifest_path)
    digest = hashlib.sha256(str(source).encode()).hexdigest()[:8]
    target = run_dir / f"{source.stem}-{digest}{source.suffix.lower()}"
    shutil.copy2(source, target)
    return str(target.relative_to(PUBLIC))


def prepare_runtime(manifest_path: Path, crier: Path) -> tuple[dict, Path]:
    manifest = json.loads(manifest_path.read_text())
    if not manifest.get("scenes"):
        raise ValueError("manifest.json에 scenes가 없습니다.")

    sys.path.insert(0, str(crier / "bin"))
    import korean  # type: ignore

    config = json.loads((crier / "config.json").read_text())
    voice_cfg = manifest.get("voice", {})
    voice = voice_cfg.get("id", "F2")
    speed = float(voice_cfg.get("speed", 1.08))
    steps = int(voice_cfg.get("steps", 8))
    port = int(config.get("port", 7788))
    run([str(crier / "bin" / "crier"), "start"])

    run_id = hashlib.sha256((str(manifest_path.resolve()) + manifest_path.read_text()).encode()).hexdigest()[:10]
    public_run = PUBLIC / "generated" / run_id
    public_run.mkdir(parents=True, exist_ok=True)
    runtime_scenes = []

    for index, scene in enumerate(manifest["scenes"], start=1):
        current = dict(scene)
        if current.get("image"):
            current["image"] = copy_asset(current["image"], manifest_path, public_run)

        narration = current.pop("narration", "").strip()
        if not narration:
            raise ValueError(f"장면 {index}에 narration이 없습니다.")
        spoken = clean_for_speech(narration, korean)
        audio = public_run / f"{index:02d}.wav"
        if not audio.exists() or audio.stat().st_size <= 44:
            body = json.dumps({
                "text": spoken,
                "voice": voice,
                "lang": "ko",
                "speed": speed,
                "steps": steps,
                "response_format": "wav",
            }, ensure_ascii=False).encode()
            request = urllib.request.Request(
                f"http://127.0.0.1:{port}/v1/tts",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=600) as response:
                audio.write_bytes(response.read())
        seconds = duration(audio)
        pad = 0.85 if index in (1, len(manifest["scenes"])) else 0.55
        current["audio"] = str(audio.relative_to(PUBLIC))
        current["frames"] = max(1, math.ceil((seconds + pad) * FPS))
        runtime_scenes.append(current)
        print(f"  음성 {index}/{len(manifest['scenes'])} · {seconds:.1f}초 · {voice}")

    runtime = {
        "fps": FPS,
        "totalFrames": sum(scene["frames"] for scene in runtime_scenes),
        "meta": manifest.get("meta", {}),
        "scenes": runtime_scenes,
    }
    if manifest.get("bgm"):
        runtime["bgm"] = copy_asset(manifest["bgm"], manifest_path, public_run)
        runtime["bgmVolume"] = float(manifest.get("bgmVolume", 0.07))

    props = ROOT / "output" / f"{manifest_path.stem}-{run_id}-runtime.json"
    props.parent.mkdir(parents=True, exist_ok=True)
    props.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n")
    return runtime, props


def qa_video(output: Path, runtime: dict) -> Path:
    result = run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-show_entries", "stream=codec_type,width,height,r_frame_rate", "-of", "json", str(output)], capture=True)
    probe = json.loads(result.stdout)
    streams = probe.get("streams", [])
    if not any(stream.get("codec_type") == "audio" for stream in streams):
        raise RuntimeError("완성 영상에 오디오 스트림이 없습니다.")
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    if (video_stream.get("width"), video_stream.get("height")) != (1920, 1080):
        raise RuntimeError(f"영상 해상도가 1920×1080이 아닙니다: {video_stream}")

    qa_dir = output.parent / "qa" / output.stem
    qa_dir.mkdir(parents=True, exist_ok=True)
    total = float(probe["format"]["duration"])
    frames = []
    for label, ratio in (("start", 0.08), ("middle", 0.5), ("end", 0.92)):
        frame = qa_dir / f"{label}.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{total * ratio:.3f}", "-i", str(output), "-frames:v", "1", str(frame)])
    elapsed_frames = 0
    for index, scene in enumerate(runtime["scenes"], start=1):
        timestamp = (elapsed_frames + scene["frames"] / 2) / runtime["fps"]
        frame = qa_dir / f"scene-{index:02d}.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{timestamp:.3f}", "-i", str(output), "-frames:v", "1", str(frame)])
        frames.append(frame)
        elapsed_frames += scene["frames"]
    contact = qa_dir / "contact-sheet.png"
    inputs = []
    for frame in frames:
        inputs.extend(["-i", str(frame)])
    prepared = ";".join(f"[{index}:v]scale=640:360[v{index}]" for index in range(len(frames)))
    streams = "".join(f"[v{index}]" for index in range(len(frames)))
    layout = "|".join(f"{(index % 3) * 640}_{(index // 3) * 360}" for index in range(len(frames)))
    run([
        "ffmpeg", "-y", "-loglevel", "error", *inputs,
        "-filter_complex", f"{prepared};{streams}xstack=inputs={len(frames)}:layout={layout}:fill=white[out]",
        "-map", "[out]",
        str(contact),
    ])
    (qa_dir / "probe.json").write_text(json.dumps(probe, ensure_ascii=False, indent=2) + "\n")
    print(f"  검사 · {total:.1f}초 · 1920×1080 · 오디오 있음")
    return contact


def main() -> None:
    parser = argparse.ArgumentParser(description="AI 발표 자료 제작 키트 동적 영상 렌더러")
    parser.add_argument("manifest", type=Path, help="영상 장면 manifest.json")
    parser.add_argument("--output", type=Path, help="완성 MP4 경로")
    args = parser.parse_args()

    manifest = args.manifest.expanduser().resolve()
    if not manifest.exists():
        raise FileNotFoundError(manifest)
    output = (args.output or (ROOT / "output" / f"{manifest.parent.name}.mp4")).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    crier = ensure_runtime()
    runtime, props = prepare_runtime(manifest, crier)
    remotion = VIDEO / "node_modules" / ".bin" / "remotion"
    print(f"  렌더 · {len(runtime['scenes'])}장면 · {runtime['totalFrames'] / FPS:.1f}초")
    run([
        str(remotion), "render", "src/index.jsx", "WeeklyReport", str(output),
        f"--props={props}", "--codec=h264", "--crf=17", "--concurrency=4",
    ], cwd=VIDEO)
    contact = qa_video(output, runtime)
    print(f"✓ 완성: {output}")
    print(f"✓ QA: {contact}")


if __name__ == "__main__":
    main()

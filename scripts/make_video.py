#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  장표 HTML + 대사 → 내레이션·자막이 붙은 MP4
#
#  사용법:
#    python3 scripts/make_video.py 장표.html 장면.json
#    python3 scripts/make_video.py 장표.html 장면.json --voice ko-KR-InJoonNeural
#    python3 scripts/make_video.py --voices        # 쓸 수 있는 목소리 듣기 전 목록
#
#  장면.json 형식 (장표 순서대로):
#    [ {"slide": 1, "text": "환영합니다. 첫 주에 필요한 세 가지를 안내합니다."},
#      {"slide": 2, "text": "채널 규칙, 자료 정리, 주간 보고입니다."} ]
#
#  필요한 것: Chrome, ffmpeg, edge-tts  (없으면 아래 안내가 나옵니다)
#    ffmpeg   : brew install ffmpeg     (윈도우: winget install ffmpeg)
#    edge-tts : pip3 install edge-tts   (무료 · 마이크로소프트 뉴럴 보이스)
# ─────────────────────────────────────────────────────────────
import json, re, shutil, subprocess, sys, tempfile, pathlib

# 두 엔진을 지원한다. Supertonic(로컬·고품질)이 있으면 그쪽을, 없으면 edge-tts를 쓴다.
#   Supertonic 보이스: F1~F5(여성) · M1~M5(남성)   ← pip3 install supertonic
#   edge-tts  보이스: ko-KR-SunHiNeural(여) · ko-KR-InJoonNeural(남) 등
VOICES = {
    "F2": "Supertonic · 여성 (권장 기본값)",
    "M1": "Supertonic · 남성",
    "F1": "Supertonic · 여성 차분",
    "ko-KR-SunHiNeural":  "edge-tts · 여성 (Supertonic 없을 때)",
    "ko-KR-InJoonNeural": "edge-tts · 남성",
}
import re as _re
def supertonic_bin():
    for c in [shutil.which("supertonic"),
              str(pathlib.Path.home()/".crier/.venv/bin/supertonic")]:
        if c and pathlib.Path(c).exists(): return c
    return None
def synth(voice, text, out_mp3, tmp):
    """voice가 F1~M5면 Supertonic, 아니면 edge-tts. 성공 시 mp3 경로 반환."""
    if _re.fullmatch(r"[FM][1-5]", voice):
        st = supertonic_bin()
        if not st: die(f"'{voice}'는 Supertonic 보이스입니다 → pip3 install supertonic")
        wav = out_mp3.with_suffix(".wav")
        r = subprocess.run([st, "tts", "-o", str(wav), "--voice", voice,
                            "--lang", "ko", text], capture_output=True)
        if r.returncode or not wav.exists(): die(f"Supertonic 합성 실패: {r.stderr.decode()[:120]}")
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), str(out_mp3)], capture_output=True)
        return out_mp3
    r = subprocess.run(["edge-tts", "--voice", voice, "--text", text,
                        "--write-media", str(out_mp3)], capture_output=True)
    if r.returncode or not out_mp3.exists(): die("edge-tts 합성 실패 (인터넷 연결 확인)")
    return out_mp3
W, H, PAD = 1280, 720, 0.45   # 해상도, 장면 간 여백(초)
BGM_VOL = 0.12                 # 배경음악 크기 (내레이션 대비 · 귀로 듣고 조절)

def die(msg): print(f"✗ {msg}"); sys.exit(1)

def chrome():
    for p in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome"), shutil.which("chromium")]:
        if p and pathlib.Path(p).exists(): return p
    die("Chrome을 찾지 못했습니다. 크롬을 설치해 주세요.")

def need(cmd, hint):
    if not shutil.which(cmd): die(f"{cmd}가 없습니다 → {hint}")

def main():
    if "--voices" in sys.argv:
        print("목소리 목록 (--voice 로 선택):")
        for v, d in VOICES.items(): print(f"  {v:<36} {d}")
        return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2: die("사용법: make_video.py 장표.html 장면.json [--voice 이름]")
    deck, scenes_p = pathlib.Path(args[0]), pathlib.Path(args[1])
    default_voice = "F2" if supertonic_bin() else "ko-KR-SunHiNeural"
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else default_voice
    need("ffmpeg", "brew install ffmpeg")
    if not _re.fullmatch(r"[FM][1-5]", voice):
        need("edge-tts", "pip3 install edge-tts")
    CH = chrome()

    html = deck.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", html, re.S)
    slides = re.findall(r'<section class="slide.*?</section>', html, re.S)
    scenes = json.loads(scenes_p.read_text(encoding="utf-8"))
    if not slides: die("장표(.slide)를 찾지 못했습니다.")
    print(f"장표 {len(slides)}장 · 장면 {len(scenes)}개 · 목소리 {voice}")

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="mkvideo_"))
    segs, t0 = [], 0.0
    for i, sc in enumerate(scenes, 1):
        sl = slides[sc["slide"] - 1]
        page = tmp / f"s{i}.html"
        cap = (f'<div style="position:fixed;left:50%;bottom:34px;transform:translateX(-50%);'
               f'max-width:900px;background:rgba(11,11,12,.82);color:#fff;font-size:19px;'
               f'line-height:1.5;padding:10px 22px;border-radius:10px;text-align:center;'
               f'letter-spacing:-.01em;z-index:99">{sc["text"]}</div>')
        page.write_text(f'<!doctype html><html><head><meta charset="utf-8">'
                        f'{style.group(0) if style else ""}'
                        f'<style>body{{margin:0;background:#fff}}.slide{{margin:0!important}}</style>'
                        f'</head><body>{sl}{cap}</body></html>', encoding="utf-8")
        png = tmp / f"s{i}.png"
        subprocess.run([CH, "--headless", "--disable-gpu", f"--screenshot={png}",
                        f"--window-size={W},{H}", "--hide-scrollbars", str(page.as_uri())],
                       capture_output=True)
        mp3 = synth(voice, sc["text"], tmp / f"s{i}.mp3", tmp)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "format=duration", "-of", "csv=p=0", str(mp3)],
                    capture_output=True, text=True).stdout.strip())
        seg = tmp / f"seg{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(png), "-i", str(mp3),
                        "-t", f"{dur + PAD:.2f}", "-r", "30", "-pix_fmt", "yuv420p",
                        "-c:v", "libx264", "-c:a", "aac", str(seg)], capture_output=True)
        if not seg.exists() or seg.stat().st_size < 1000: die(f"장면 {i} 세그먼트 생성 실패")
        segs.append(seg)
        t0 += dur + PAD
        print(f"  장면 {i}/{len(scenes)} — {dur:.1f}초")

    (tmp / "list.txt").write_text("".join(f"file '{s}'\n" for s in segs))
    out = deck.with_suffix("").name + "_영상.mp4"
    # 자막은 화면에 이미 구워져 있으므로 이어붙이기만 한다 (미니멀 ffmpeg에서도 동작)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp/"list.txt"),
                    "-c", "copy", out], capture_output=True)
    if not pathlib.Path(out).exists(): die("최종 합성 실패")

    # ── 배경음악: 기본 꺼짐. --bgm 을 줬을 때만 깔린다 ──
    #    --bgm            → 키트에 들어 있는 곡(assets/bgm*.mp3) 사용
    #    --bgm 파일경로    → 지정한 곡 사용
    bgms = []
    if "--bgm" in sys.argv:
        i = sys.argv.index("--bgm")
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--") \
           and pathlib.Path(sys.argv[i + 1]).suffix.lower() in (".mp3", ".wav"):
            bgms = [pathlib.Path(sys.argv[i + 1])]
        else:
            kit_root = pathlib.Path(__file__).resolve().parent.parent
            bgms = sorted(kit_root.glob("assets/bgm*.mp3")) + sorted(kit_root.glob("assets/bgm*.wav"))
            if not bgms: die("--bgm: 키트 assets/에 bgm 파일이 없습니다. 경로를 지정해 주세요")
    if bgms:
        bgm, mixed = bgms[0], out.replace("_영상", "_영상_bgm")
        fade = max(t0 - 2.0, 0)
        r = subprocess.run(["ffmpeg", "-y", "-i", out, "-stream_loop", "-1", "-i", str(bgm),
             "-filter_complex",
             f"[1:a]volume={BGM_VOL},afade=t=out:st={fade:.1f}:d=2[bg];"
             f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-t", f"{t0:.2f}", mixed],
             capture_output=True)
        if r.returncode == 0 and pathlib.Path(mixed).exists():
            pathlib.Path(mixed).replace(out)
            print(f"  배경음악: {bgm.name} (볼륨 {BGM_VOL})")
        else:
            print("  배경음악 합성 실패 — 내레이션만으로 완성했습니다")
    print(f"✓ 완성: {out}  ({t0:.0f}초)")
    print("  검사: 영상을 직접 열어 소리·자막·화면 전환을 확인하세요 (03_검사.md 참고)")

if __name__ == "__main__": main()

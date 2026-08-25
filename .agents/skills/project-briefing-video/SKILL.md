---
name: project-briefing-video
description: Create and verify narrated project briefing, weekly-report, onboarding, or presentation videos with this repository's Remotion engine and free local Crier/Supertonic voice. Use for 영상, 브리핑 영상, 발표 영상, 주간보고 영상, or onboarding video requests.
---

# Project Briefing Video

Create a real dynamic video, not static slides held for the duration of an audio track.

## Required workflow

1. Read the user's latest request and use the approved report or deck as the content source. Do not change the requested subject because an example uses a different topic.
2. Run `python3 scripts/doctor.py`. If required components are missing, run `bash scripts/bootstrap.sh` and run the doctor again.
3. Do not fall back to browser `speechSynthesis`, macOS `say`, or an unrelated low-quality TTS. Stop with the failed component if Crier/Supertonic cannot be prepared.
4. Create an `output/<name>-manifest.json` based on `examples/customer-support-weekly-20260827/manifest.json` and the schema in the reference below. Use the example only as a quality and motion reference, not as a source of facts.
5. Make screen, narration, and caption express the same fact in the same scene. Every scene must have a short readable `closedCaption`. Write service names phonetically in Korean narration where needed.
6. Inventory `refs/**/첨부/` and `assets/visuals/`, then use actual screenshots and supplied images first. A relevant available image must appear large in at least one scene. Generate new assets with Codex only when needed, at the intended aspect ratio, then inspect them for text, anatomy, cropping, and style errors.
7. Render with `python3 scripts/render_video.py output/<name>-manifest.json --output output/<name>.mp4`.
8. Inspect start, middle, end, every scene frame, and the contact sheet. Confirm 1920×1080, 30fps, audio stream, readable captions, and no broken or placeholder visuals.

## Default production choices

- Voice: Crier/Supertonic F2, speed 1.08, steps 8
- Weekly report BGM: none
- Onboarding or opening BGM: only when requested or appropriate, mixed under narration
- Visual tone: white canvas, black editorial type, one accent color, large imagery, restrained motion
- Duration: follow the user's request; if absent, keep a briefing between 45 and 90 seconds

Read [references/video-system.md](references/video-system.md) before writing a manifest or changing the video engine.

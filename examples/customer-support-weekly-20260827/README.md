# 고객지원팀 주간보고 영상 예제

`refs/20260825/`와 `refs/20260827/`의 가상 고객지원 업무 기록으로 만든 고품질 기준 예제입니다.

설치 전에는 `preview-contact-sheet.png`로 전체 장면을 확인하고, `preview.mp4`로 실제 음성·자막·모션을 확인할 수 있습니다.

```bash
python3 scripts/render_video.py examples/customer-support-weekly-20260827/manifest.json \
  --output output/customer-support-weekly-20260827.mp4
```

주간보고 영상의 기본 원칙을 확인할 수 있습니다.

- 흰 배경, 검정 타이포, 파란색 포인트 한 가지
- 실제 업무 맥락을 나타내는 큰 이미지 에셋
- 수치 카운트업, 비교선, 순차 등장
- 화면과 내레이션이 일치하는 큰 자막
- Crier/Supertonic F2 무료 로컬 음성
- 주간보고이므로 BGM 없음

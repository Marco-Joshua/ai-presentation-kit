# 8월 14일 주간보고 완주 예제

이 예제는 `examples/weekly-report-20260814/refs/20260814/`의 메일·통화·회의·메신저 네 파일을 읽어 만든
약 30초짜리 **온보딩 프로젝트 주간보고**입니다. 온보딩 안내 영상 예제가 아닙니다.

예제 자료는 루트 `refs/`와 분리되어 있어, 새 업무를 요청했을 때 온보딩 산출물을 잘못 만드는 원인이 되지 않습니다.

## 먼저 결과부터 확인하기

- `preview.mp4` — 같은 렌더러로 만든 27.8초 주간보고 영상
- `preview-deck.pdf` — 5장짜리 주간보고 장표 PDF
- `preview-contact-sheet.png` — 영상의 모든 장면 대표 프레임

세 파일은 설치 전 품질을 확인하는 예시입니다. 아래 명령을 실행하면 같은 구조의 결과물을 다시 만들 수 있습니다.

```bash
python3 scripts/render_video.py examples/weekly-report-20260814/manifest.json \
  --output output/weekly-report-20260814.mp4
```

렌더러가 자동으로 수행하는 작업:

1. Crier/Supertonic F2 장면별 음성 생성
2. 이미지 에셋 복사와 장면 시간 계산
3. Remotion 1920×1080 동적 영상 렌더
4. 오디오 스트림·해상도·길이 검사
5. 모든 장면 대표 프레임과 콘택트시트 생성

`manifest.json`의 내용만 바꾸면 같은 엔진으로 다른 주간보고를 만들 수 있습니다.

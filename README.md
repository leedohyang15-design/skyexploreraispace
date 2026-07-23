---
title: Sky Explorer AI
emoji: 🔭
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
---

# Sky Explorer AI — 자연어 → 플라네타리움 Python 스크립트

Sky Explorer SDK 의 **실측 검증된 지식**(레퍼런스 + 함정 + 검증 예제)을 시스템 프롬프트로
주입해, 자연어 요청을 Studio 에서 바로 실행 가능한 Python 으로 변환합니다.

## Space 설정 (필수)
1. **Settings → Variables and secrets → New secret**
   - Name: `GROQ_API_KEY` / Value: console.groq.com 에서 발급한 키
2. (선택) `GROQ_MODEL` 변수로 모델 변경 — 기본 `llama-3.3-70b-versatile`

## 파일 구성
| 파일 | 역할 |
|---|---|
| `app.py` | Gradio UI + Groq 호출 + 지식팩 조립 |
| `knowledge/reference.md` | 정제 AI 프롬프트 (원본: 레포 `reference/AI_SYSTEM_PROMPT.md` — 전체 클래스 레시피 압축본) |
| `knowledge/examples.md` | 검증된 자연어→코드 few-shot |
| `converter/` | 순수 파이썬 SPC→Python 변환기 (레포 `scripts/spc_convert/` 와 동기화) |

## 지식 갱신 방법
레포에서 record-confirm 루프로 지식이 갱신되면:
```bash
cp reference/AI_SYSTEM_PROMPT.md   webapp/hf_space/knowledge/reference.md
cp scripts/spc_convert/spc_to_python.py scripts/spc_convert/spc_converter.py \
   scripts/spc_convert/tz_table.py  webapp/hf_space/converter/
```
후 Space 에 다시 업로드 — 재학습 없이 즉시 반영됩니다.
(⚠️ CLAUDE.md 원본을 그대로 넣지 말 것 — 실험 로그라 토큰만 잡아먹고 생성 품질↓. 반드시 정제본 사용.)

# -*- coding: utf-8 -*-
"""
Sky Explorer AI — 자연어 → Python 스크립트 생성기 (Hugging Face Space + Groq)
====================================================================
UI: 커스텀 HTML(우주 테마) 전면 + Gradio 는 API 엔진으로 숨김
    사이드바 = 대화 로그(localStorage 저장, 클릭 복원) — Claude/Gemini 스타일
지식: knowledge/reference.md(정제 AI 프롬프트) + knowledge/examples.md 를 시스템 프롬프트로 주입
Space 설정: Settings → Variables and secrets → GROQ_API_KEY (필수)
"""
import datetime as dt
import json
import math
import os
import re
import urllib.request
from pathlib import Path

import gradio as gr
from groq import Groq

HERE = Path(__file__).parent

PREFERRED_MODELS = [
    "llama-3.3-70b-versatile",       # 분당 12K tok — TPM 가장 넉넉 → 1순위
    "openai/gpt-oss-120b",           # 분당 8K tok
    "openai/gpt-oss-20b",            # 분당 8K tok
    "llama-3.1-8b-instant",          # 분당 6K tok (일일 요청 한도는 가장 큼)
    "qwen/qwen3-32b",                # 분당 6K tok, 일 500K tok
]

# ── 남용/쿼터 보호 상한 (공개 엔드포인트라 서버측에서 강제) ──
MAX_PROMPT_CHARS = 2000          # 단일 요청 프롬프트 길이 상한 (초과분 잘라냄)
MAX_SPC_BYTES = 5_000_000        # SPC 변환 입력 상한 (5MB)
QUEUE_CONCURRENCY = 3            # 동시 LLM 실행 수 상한
QUEUE_MAX_SIZE = 40             # 대기열 최대 길이 (폭주 시 초과 요청 거절)

BASE_RULES = """당신은 Sky Explorer 플라네타리움 SDK 의 Python 스크립트 생성 전문가다.
사용자의 자연어 요청을 Studio 에서 바로 실행 가능한 Python 스크립트로 변환한다.

절대 규칙:
1. 아래 레퍼런스에 실측으로 검증된 API/패턴만 사용한다. 추측 금지.
2. import 3종 세트로 시작: from skyExplorer import * / from studio import * / from Initialization import *
3. 카메라 R(거리)에 절대값을 넣지 않는다 — positionLBR 를 읽어 배율을 곱한다 (R 단위 = 트랙 대상 반지름).
   줌인/줌아웃은 **setPositionR(읽은 R × 배율, Anim, track)** 로 R 만 바꾼다.
   setPositionLBR 로 L/B 를 다시 쓰면 줌 중 화면이 움직인다(사용자 리포트) — 줌엔 금지.
   줌 시작 전에 setTargetHeight(조준값) 조준을 sleep 으로 완전히 끝낸다.
4. 성운은 이름 enum(NebulaName.HORSEHEAD 등)만. 숫자 인덱스는 id=-1 (null).
5. 애니메이션 뒤에는 반드시 그 시간만큼 sleep() 한다.
6. 불확실한 enum/포트는 try/except 나 getattr 로 방어하고, 실패 시 print 로 알린다.
7. 격한 카메라 슬루는 GlobalIntensity 0(암전)에서 세팅한 뒤 페이드인으로 숨긴다.
8. 출력은 파이썬 코드 블록 하나만. 코드 밖 설명은 한두 문장 이내. 코드 안 주석은 한국어로 핵심만.
9. **대화 연속성**: 사용자가 "이 코드", "방금 코드", "수정해줘", "추가해줘" 라고 하면
   반드시 직전 대화에서 준 코드를 기준으로 요청 부분만 고친다.
   대상 천체를 절대 바꾸지 않는다 (말머리성운 코드 수정 요청에 지구 코드 금지).
10. **예제는 패턴 참고용**: 예제의 천체(지구/토성)를 그대로 복사하지 말고,
   사용자가 말한 천체/성운으로 치환해서 같은 패턴을 적용한다.
11. **회전/공전(오빗) 요청**: 검증된 스텝 오빗 패턴만 사용 — 0.5초 스텝으로
   setPositionLBR 의 L 을 조금씩 증가 + 4스텝마다 setOrientationSmoothXYZR 재조준
   (예제 6). 시간가속 자전, orientation 루프 등 미검증 회전은 만들지 않는다.
12. **기본 관측지 = 대한민국 충북 청주**: 사용자가 다른 장소를 지정하지 않는 한
   Place2D 위치는 Vec(36.64, 127.49, 60.0) (위도, 경도, 고도m) 를 쓴다.
   ⚠️ **시간은 항상 UTC 로 넣는다** — 이 SDK 는 DefaultTimeZone=UTC 라 넘긴 시각을 그대로 UTC 로 해석한다.
   청주 현지시각(KST)을 UTC 로 변환해서 넣을 것: **UTC = KST − 9h**.
   · 청주 밤 22:00 KST → setDateTime(..., 13, 0, 0, tz, ...)  (=13:00 UTC)
   · 청주 현지 정오 12:00 KST → 03:30 UTC
   TimeZone 인자는 tz = DateManager.TimeZone.DefaultTimeZone 를 쓴다
   (하드코딩 TimeZone.UTC 는 존재하지 않아 AttributeError — DefaultTimeZone 사용).

레퍼런스에 없는 요청(스크립트로 불가능하다고 기록된 것 포함)은 코드 대신
'왜 안 되는지 + 가능한 대안'을 짧게 답한다.
"""


DROP_SECTIONS = ("## 실행 방법", "## Hello World")   # 코드 생성에 불필요 → 토큰 절약

# 시스템 프롬프트 입력 토큰이 모델 분당 한도(TPM)를 넘지 않도록 지식 파일 길이 상한.
# reference.md = 정제 AI 프롬프트(전체 클래스 레시피 압축본, ~9.6K자) → 통째로 주입.
# examples.md = 검증된 few-shot(~6.8K자) → 통째로 주입. (초과 시에만 섹션 경계 절단)
# examples 는 기존 5000 유지(이미 그 예산으로 동작 검증됨) — TPM 여유 확보.
KNOWLEDGE_CHAR_LIMIT = {"reference.md": 10000, "examples.md": 5000}


def _read_knowledge(name: str) -> str:
    p = HERE / "knowledge" / name
    if not p.exists():
        return "(경고: knowledge/%s 가 업로드되지 않음 — 지식 없이 동작 중)" % name
    text = p.read_text(encoding="utf-8")
    parts = text.split("\n## ")
    kept = [parts[0]] + [s for s in parts[1:]
                         if not any(("## " + s).startswith(d) for d in DROP_SECTIONS)]
    out = "\n## ".join(kept)
    limit = KNOWLEDGE_CHAR_LIMIT.get(name)
    if limit and len(out) > limit:
        # 섹션 경계에서 자르기(중간 절단 방지) — limit 이전 마지막 "\n## " 기준
        cut = out.rfind("\n## ", 0, limit)
        out = (out[:cut] if cut > 0 else out[:limit]) + "\n\n(…이하 생략: 토큰 한도 보호)"
    return out


SYSTEM = (
    BASE_RULES
    + "\n\n# 실측 레퍼런스 (신뢰 소스)\n\n" + _read_knowledge("reference.md")
    + "\n\n# 검증된 변환 예제\n\n" + _read_knowledge("examples.md")
)

# ── SPC → Python 변환기 (우리가 만든 순수 파이썬 변환기 번들) ──
import sys as _sys
_sys.path.insert(0, str(HERE / "converter"))
try:
    from spc_to_python import to_python as _spc_to_python
except Exception as _e:                      # converter/ 폴더 누락 시에도 앱은 뜸
    _spc_to_python = None
    _conv_err = str(_e)


# ═════════════════════════════════════════════════════════════════
# 천문 달력 — 2026년 한국(충북 청주 기준) 관측 가능 천문 현상
#   type: meteor(유성우) / eclipse(식) / planet(행성) / moon(달) /
#         comet(혜성) / special(특이현상) / conjunction(접근)
#   date: "MM-DD"  |  peak 기간이면 end 로 종료일
#   tip: 한국 관측 팁,  prompt: 클릭 시 스크립트 생성에 넣을 자연어
# ═════════════════════════════════════════════════════════════════
SKY_EVENTS_2026 = [
    {"date": "01-03", "end": "01-04", "type": "meteor", "name": "사분의자리 유성우 극대",
     "desc": "3대 유성우 중 하나. 극대 시간이 짧아 타이밍이 중요합니다.",
     "tip": "새벽 2~5시 북동쪽 하늘. 시간당 최대 60~120개. 청주 외곽(문의·미원 방면)이 광해가 적습니다.",
     "prompt": "사분의자리 유성우가 쏟아지는 새벽 북동쪽 하늘을 보여줘"},
    {"date": "01-10", "type": "planet", "name": "수성 서방최대이각",
     "desc": "수성이 태양에서 가장 멀리 떨어져 새벽에 관측하기 좋은 시기.",
     "tip": "일출 1시간 전 남동쪽 지평선 근처. 낮은 고도라 트인 곳 필요.",
     "prompt": "새벽 동쪽 하늘에 뜬 수성을 확대해서 보여줘"},
    {"date": "02-17", "type": "eclipse", "name": "금환일식 (한국 관측 불가)",
     "desc": "남극권에서 관측되는 금환일식. 한국에서는 볼 수 없습니다.",
     "tip": "국내 관측 불가. 시뮬레이션으로 금환 현상을 재현해 보세요.",
     "prompt": "금환일식이 일어나는 순간을 태양과 달을 정렬해서 보여줘"},
    {"date": "03-03", "type": "eclipse", "name": "개기월식 ★ 한국 관측 가능",
     "desc": "2026년 최대 하이라이트. 달 전체가 지구 그림자에 들어가 붉게 물듭니다.",
     "tip": "저녁~밤 전 과정 관측 가능. 맨눈으로 충분하며 망원경이면 더 좋습니다.",
     "prompt": "개기월식으로 붉게 물든 블러드문을 크게 보여줘"},
    {"date": "03-20", "type": "special", "name": "춘분",
     "desc": "낮과 밤의 길이가 같아지는 날. 태양이 천구 적도를 통과합니다.",
     "tip": "황도와 천구 적도의 교차를 시뮬레이션으로 보면 이해가 쉽습니다.",
     "prompt": "춘분에 태양이 천구 적도를 지나는 모습을 황도와 함께 보여줘"},
    {"date": "04-22", "end": "04-23", "type": "meteor", "name": "거문고자리 유성우",
     "desc": "가장 오래된 기록을 가진 유성우. 밝은 유성이 특징입니다.",
     "tip": "자정 이후 동쪽 하늘. 시간당 15~20개 수준.",
     "prompt": "거문고자리 방향에서 유성이 떨어지는 밤하늘을 보여줘"},
    {"date": "05-06", "type": "meteor", "name": "물병자리 에타 유성우",
     "desc": "핼리 혜성이 남긴 잔해가 만드는 유성우.",
     "tip": "새벽 3~5시 동쪽 낮은 하늘. 한국은 복사점 고도가 낮아 조건이 까다롭습니다.",
     "prompt": "물병자리 에타 유성우를 새벽 동쪽 하늘에서 보여줘"},
    {"date": "06-21", "type": "special", "name": "하지",
     "desc": "북반구에서 낮이 가장 긴 날. 태양 남중고도가 최고에 이릅니다.",
     "tip": "태양의 연중 궤적(아날렘마)을 함께 보면 흥미롭습니다.",
     "prompt": "하지에 태양이 가장 높이 뜬 정오 하늘을 보여줘"},
    {"date": "08-12", "end": "08-13", "type": "meteor", "name": "페르세우스자리 유성우 극대 ★",
     "desc": "연중 가장 인기 있는 유성우. 여름밤 관측 조건이 좋습니다.",
     "tip": "자정~새벽 북동쪽. 시간당 최대 100개. 청주 시내 광해를 피해 대청호·속리산 방면 추천.",
     "prompt": "페르세우스자리 유성우가 쏟아지는 여름 밤하늘을 보여줘"},
    {"date": "08-28", "type": "eclipse", "name": "개기일식 (한국 관측 불가)",
     "desc": "아이슬란드·스페인 등에서 관측되는 개기일식.",
     "tip": "국내 관측 불가. 코로나가 드러나는 순간을 재현해 보세요.",
     "prompt": "개기일식 순간 태양 코로나가 드러나는 장면을 보여줘"},
    {"date": "09-23", "type": "special", "name": "추분",
     "desc": "다시 낮과 밤의 길이가 같아지는 날.",
     "tip": "가을 은하수가 잘 보이기 시작하는 시기입니다.",
     "prompt": "추분 밤에 은하수가 걸린 하늘을 보여줘"},
    {"date": "10-21", "end": "10-22", "type": "meteor", "name": "오리온자리 유성우",
     "desc": "핼리 혜성 기원의 두 번째 유성우. 빠른 유성이 특징.",
     "tip": "자정 이후 오리온자리가 떠오른 뒤 관측. 시간당 20개 내외.",
     "prompt": "오리온자리 유성우가 보이는 새벽 하늘로 이동해줘"},
    {"date": "11-17", "end": "11-18", "type": "meteor", "name": "사자자리 유성우",
     "desc": "33년 주기로 대유성우가 발생하는 것으로 유명한 유성우.",
     "tip": "새벽 동쪽 하늘. 평년에는 시간당 10~15개.",
     "prompt": "사자자리 유성우를 새벽 동쪽 하늘에서 보여줘"},
    {"date": "12-13", "end": "12-14", "type": "meteor", "name": "쌍둥이자리 유성우 극대 ★",
     "desc": "연중 가장 많은 유성을 뿌리는 최대 규모의 유성우.",
     "tip": "밤 10시부터 새벽까지. 시간당 최대 120~150개. 청주 겨울 새벽은 영하권이라 방한 필수.",
     "prompt": "쌍둥이자리 유성우가 가장 활발한 겨울 밤하늘을 보여줘"},
    {"date": "12-22", "type": "special", "name": "동지",
     "desc": "북반구에서 밤이 가장 긴 날. 겨울 별자리 관측 최적기.",
     "tip": "오리온·큰개자리 등 겨울 대삼각형을 함께 보세요.",
     "prompt": "동지 밤에 겨울 대삼각형이 보이는 하늘을 보여줘"},
    # ── 혜성 / 특이 현상 ──
    {"date": "01-01", "end": "12-31", "type": "comet", "name": "혜성 12P/폰스-브룩스 관측 시즌",
     "desc": "약 71년 주기의 주기 혜성. 밝아질 때 쌍안경으로 관측 가능합니다.",
     "tip": "실제 밝기는 해마다 변동이 큽니다. 최신 예보를 함께 확인하세요.",
     "prompt": "혜성이 꼬리를 끌며 지나가는 밤하늘을 보여줘"},
    {"date": "03-19", "type": "conjunction", "name": "금성-토성 근접",
     "desc": "두 행성이 하늘에서 매우 가깝게 보이는 현상.",
     "tip": "해진 직후 서쪽 하늘. 망원경 저배율에서 한 시야에 들어옵니다.",
     "prompt": "금성과 토성이 나란히 붙어 있는 저녁 서쪽 하늘을 보여줘"},
    {"date": "07-15", "type": "planet", "name": "화성 충 근처 관측 호기",
     "desc": "화성이 지구와 가까워져 밝고 크게 보이는 시기.",
     "tip": "밤새 관측 가능. 고배율에서 극관과 표면 무늬를 노려보세요.",
     "prompt": "화성을 크게 확대해서 표면이 보이도록 해줘"},
    {"date": "09-05", "type": "planet", "name": "토성 충 ★",
     "desc": "토성이 지구와 가장 가까워지는 시기. 고리 관측 최적기.",
     "tip": "밤새 관측 가능. 소형 망원경으로도 고리가 뚜렷합니다.",
     "prompt": "토성 고리가 잘 보이도록 크게 확대해서 보여줘"},
    {"date": "11-10", "type": "planet", "name": "목성 충 ★",
     "desc": "목성이 가장 밝고 크게 보이는 시기. 위성 관측도 좋습니다.",
     "tip": "쌍안경으로도 갈릴레이 위성 4개가 보입니다.",
     "prompt": "목성과 갈릴레이 위성들을 함께 보여줘"},
]

EVENT_TYPE_META = {
    "meteor":      {"icon": "☄️", "label": "유성우",  "color": "#ffb84d"},
    "eclipse":     {"icon": "🌑", "label": "일·월식", "color": "#ff6b8a"},
    "planet":      {"icon": "🪐", "label": "행성",    "color": "#5ee6c4"},
    "moon":        {"icon": "🌙", "label": "달",      "color": "#c8b6ff"},
    "comet":       {"icon": "💫", "label": "혜성",    "color": "#7ee8fa"},
    "special":     {"icon": "✨", "label": "특이현상", "color": "#ffd6a5"},
    "conjunction": {"icon": "🔭", "label": "행성접근", "color": "#a0e7a0"},
}


def _moon_phase_kr(d: dt.date) -> dict:
    """간이 달 위상 계산(삭 기준 시노딕 주기). 관측 조건 안내용."""
    known_new = dt.date(2026, 1, 18)          # 2026년 삭 기준일
    synodic = 29.530588853
    days = (d - known_new).days % synodic
    pct = round(days / synodic * 100)
    if days < 1.85 or days > 27.68:
        name, icon, cond = "삭(그믐)", "🌑", "관측 최적 — 달빛 방해 없음"
    elif days < 5.54:
        name, icon, cond = "초승달", "🌒", "관측 좋음"
    elif days < 9.23:
        name, icon, cond = "상현달", "🌓", "자정 이후 관측 유리"
    elif days < 12.91:
        name, icon, cond = "차오르는 달", "🌔", "달빛 다소 방해"
    elif days < 16.61:
        name, icon, cond = "보름달", "🌕", "달빛 강함 — 유성우 관측 불리"
    elif days < 20.30:
        name, icon, cond = "기우는 달", "🌖", "달빛 다소 방해"
    elif days < 23.99:
        name, icon, cond = "하현달", "🌗", "초저녁 관측 유리"
    else:
        name, icon, cond = "그믐달", "🌘", "관측 좋음"
    return {"name": name, "icon": icon, "cond": cond, "pct": pct}


# ── 계절별 천체 풀 (달력 열 때마다 무작위로 골라 노출) ──────────────
#   한국(북반구) 저녁 하늘 기준. 별자리·밝은 별·성운·성단·은하를 섞음.
#   name 은 짧게(가독성), 상세는 prompt 로. 항상 최소 1개 보장의 핵심.
SEASONAL_SKY = {
    "spring": [
        {"icon": "🦁", "name": "사자자리", "label": "봄철 남쪽 하늘",
         "prompt": "봄철 밤하늘에 사자자리를 보여줘"},
        {"icon": "🐻", "name": "북두칠성", "label": "봄철 북쪽 높은 하늘",
         "prompt": "북쪽 하늘의 북두칠성을 보여줘"},
        {"icon": "🔺", "name": "봄철 대삼각형", "label": "봄철 저녁 하늘",
         "prompt": "봄철 대삼각형(아르크투루스·스피카·데네볼라)을 선으로 이어서 보여줘"},
        {"icon": "⭐", "name": "아르크투루스", "label": "봄철 동쪽 하늘",
         "prompt": "봄철 목동자리의 주황색 별 아르크투루스를 보여줘"},
        {"icon": "♍", "name": "처녀자리·스피카", "label": "봄철 남쪽 하늘",
         "prompt": "봄철 처녀자리와 흰 별 스피카를 보여줘"},
        {"icon": "🌀", "name": "소용돌이은하 M51", "label": "봄철 밤 하늘",
         "prompt": "봄철 사냥개자리의 소용돌이은하 M51을 보여줘"},
    ],
    "summer": [
        {"icon": "🔺", "name": "여름 대삼각형", "label": "여름 머리 위",
         "prompt": "여름 대삼각형(직녀별·데네브·견우별)을 보여줘"},
        {"icon": "🦢", "name": "백조자리", "label": "여름 은하수 위",
         "prompt": "여름 은하수 위의 백조자리를 함께 보여줘"},
        {"icon": "🦂", "name": "전갈자리·안타레스", "label": "여름 남쪽 하늘",
         "prompt": "여름 남쪽 하늘의 전갈자리와 붉은 별 안타레스를 보여줘"},
        {"icon": "🏹", "name": "궁수자리", "label": "여름 남쪽 하늘",
         "prompt": "여름 은하수 중심 방향의 궁수자리를 보여줘"},
        {"icon": "💫", "name": "구상성단 M13", "label": "여름 밤 하늘",
         "prompt": "여름철 헤르쿨레스자리의 구상성단 M13을 보여줘"},
        {"icon": "🌫️", "name": "아령성운 M27", "label": "여름 밤 하늘",
         "prompt": "여름철 여우자리의 아령성운 M27을 보여줘"},
        {"icon": "🌌", "name": "여름 은하수", "label": "여름 밤 하늘",
         "prompt": "여름 밤하늘을 가로지르는 은하수를 보여줘"},
    ],
    "autumn": [
        {"icon": "⬜", "name": "페가수스 대사각형", "label": "가을 밤 하늘",
         "prompt": "가을철 페가수스자리의 큰 사각형을 보여줘"},
        {"icon": "🌌", "name": "안드로메다 은하 M31", "label": "가을 밤 하늘",
         "prompt": "가을 밤하늘의 안드로메다 은하 M31을 보여줘"},
        {"icon": "👑", "name": "카시오페이아자리", "label": "가을 북쪽 하늘",
         "prompt": "북쪽 하늘의 W자 모양 카시오페이아자리를 보여줘"},
        {"icon": "🐎", "name": "안드로메다자리", "label": "가을 밤 하늘",
         "prompt": "가을철 안드로메다자리를 보여줘"},
        {"icon": "⭐", "name": "포말하우트", "label": "가을 남쪽 낮은 하늘",
         "prompt": "가을 남쪽 하늘 낮게 뜨는 별 포말하우트를 보여줘"},
        {"icon": "✨", "name": "페르세우스자리", "label": "가을 밤 하늘",
         "prompt": "가을철 페르세우스자리를 보여줘"},
    ],
    "winter": [
        {"icon": "🌟", "name": "오리온자리", "label": "겨울 남쪽 하늘",
         "prompt": "겨울 밤하늘에 오리온자리를 크게 보여줘"},
        {"icon": "🌫️", "name": "오리온 대성운 M42", "label": "겨울 밤 하늘",
         "prompt": "오리온자리의 오리온 대성운 M42를 크게 보여줘"},
        {"icon": "🔺", "name": "겨울 대삼각형", "label": "겨울 밤 하늘",
         "prompt": "겨울 대삼각형(베텔게우스·시리우스·프로키온)을 이어서 보여줘"},
        {"icon": "⬡", "name": "겨울 대육각형", "label": "겨울 밤 하늘",
         "prompt": "겨울 대육각형(겨울 다이아몬드)의 밝은 별들을 보여줘"},
        {"icon": "🐂", "name": "황소자리·플레이아데스", "label": "겨울 밤 하늘",
         "prompt": "겨울 황소자리와 플레이아데스 성단 M45를 보여줘"},
        {"icon": "⭐", "name": "시리우스", "label": "겨울 남동쪽 하늘",
         "prompt": "겨울철 가장 밝은 별 시리우스와 큰개자리를 보여줘"},
        {"icon": "🔴", "name": "베텔게우스", "label": "겨울 밤 하늘",
         "prompt": "오리온자리의 붉은 초거성 베텔게우스를 보여줘"},
        {"icon": "🔵", "name": "리겔", "label": "겨울 밤 하늘",
         "prompt": "오리온자리의 청백색 별 리겔을 보여줘"},
    ],
}


def _season_kr(month: int) -> str:
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    if month in (9, 10, 11):
        return "autumn"
    return "winter"


# ── 관측지(도시) 목록 — 기본 청주. 사용자가 드로어에서 변경 가능 ──────
_CJU_LAT, _CJU_LON = 36.64, 127.49
OBSERVER_CITIES = {
    "청주": (36.64, 127.49), "서울": (37.57, 126.98), "인천": (37.46, 126.71),
    "대전": (36.35, 127.38), "대구": (35.87, 128.60), "광주": (35.16, 126.85),
    "부산": (35.18, 129.08), "울산": (35.54, 129.31), "강릉": (37.75, 128.90),
    "제주": (33.50, 126.53),
}


def _sun_times(d: dt.date, lat: float, lon: float) -> dict:
    """일출·일몰·남중(태양 남중) 시각을 계산해 KST 'HH:MM' 로 반환(NOAA 근사).
    극야/백야면 None. 청주 검증: 05:29/19:39/12:34 (실측 일치)."""
    n = d.timetuple().tm_yday
    lng_hour = lon / 15.0
    zenith = 90.833

    def _event(is_rise):
        t = n + ((6 if is_rise else 18) - lng_hour) / 24.0
        m = 0.9856 * t - 3.289
        el = (m + 1.916 * math.sin(math.radians(m))
              + 0.020 * math.sin(math.radians(2 * m)) + 282.634) % 360
        ra = math.degrees(math.atan(0.91764 * math.tan(math.radians(el)))) % 360
        ra += ((math.floor(el / 90) * 90) - (math.floor(ra / 90) * 90))
        ra /= 15.0
        sin_dec = 0.39782 * math.sin(math.radians(el))
        cos_dec = math.cos(math.asin(sin_dec))
        cos_h = ((math.cos(math.radians(zenith)) - sin_dec * math.sin(math.radians(lat)))
                 / (cos_dec * math.cos(math.radians(lat))))
        if cos_h > 1 or cos_h < -1:
            return None                       # 극야/백야
        h = (360 - math.degrees(math.acos(cos_h))) if is_rise else math.degrees(math.acos(cos_h))
        h /= 15.0
        ut = (h + ra - 0.06571 * t - 6.622 - lng_hour) % 24
        return ut

    def _fmt(ut):
        if ut is None:
            return None
        kst = (ut + 9.0) % 24
        hh = int(kst)
        mm = int(round((kst - hh) * 60))
        if mm == 60:
            hh = (hh + 1) % 24
            mm = 0
        return "%02d:%02d" % (hh, mm)

    rise, sett = _event(True), _event(False)
    transit = None
    if rise is not None and sett is not None:
        transit = ((rise + sett + (24 if sett < rise else 0)) / 2.0) % 24
    return {"rise": _fmt(rise), "set": _fmt(sett), "transit": _fmt(transit)}


# ── 실시간 행성/달: Visible Planets API (무료·키 불필요) ────────────
#   관측지(위·경도) 기준 '오늘 밤 지평선 위' 천체를 조회. 실패해도 조용히 폴백.
_PLANET_KR = {
    "Mercury": ("수성", "🪐"), "Venus": ("금성", "🌟"), "Mars": ("화성", "🔴"),
    "Jupiter": ("목성", "🪐"), "Saturn": ("토성", "🪐"),
    "Uranus": ("천왕성", "🔵"), "Neptune": ("해왕성", "🔵"),
}
_VP_CACHE = {}          # {날짜ISO|lat|lon: [items]} — 하루/관측지당 1회만 외부 호출


def _compass_kr(az: float) -> str:
    dirs = ["북", "북동", "동", "남동", "남", "남서", "서", "북서"]
    return dirs[int((az % 360) / 45.0 + 0.5) % 8]


def _visible_planets(today: dt.date, lat: float, lon: float) -> list:
    """관측지에서 '오늘 밤(21시 KST=12 UTC)' 지평선 위에 뜬 행성을 실시간 조회.
    네트워크/형식 오류 시 조용히 빈 리스트 → 계절 별자리 풀로 폴백."""
    key = "%s|%.2f|%.2f" % (today.isoformat(), lat, lon)
    if key in _VP_CACHE:
        return _VP_CACHE[key]
    out = []
    try:
        url = ("https://api.visibleplanets.dev/v3?latitude=%s&longitude=%s&time=%sT12:00:00Z"
               % (lat, lon, today.isoformat()))
        req = urllib.request.Request(url, headers={"User-Agent": "sky-explorer-ai"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        for b in payload.get("data", []):
            name = b.get("name")
            if name not in _PLANET_KR or not b.get("aboveHorizon"):
                continue
            if b.get("nakedEyeObject") is False:          # 맨눈 불가(천왕성·해왕성) 제외
                continue
            kr, icon = _PLANET_KR[name]
            comp = _compass_kr(b.get("azimuth") or 0)
            out.append({
                "icon": icon, "name": kr,
                "dateLabel": "오늘 밤 %s쪽 하늘" % comp,
                "prompt": "오늘 밤 하늘에서 볼 수 있는 %s을 크게 보여줘" % kr,
            })
    except Exception:                                     # noqa: BLE001 — 조용히 폴백
        out = []
    _VP_CACHE[key] = out
    return out


def _today_real(today: dt.date, lat: float, lon: float) -> list:
    """오늘의 '실제' 항목 = 실시간 행성(최대 2개) + 보름/상현/하현달.
    프런트에서 여기에 계절 풀을 무작위로 섞어 매번 다르게 보여준다."""
    out = list(_visible_planets(today, lat, lon))[:2]   # 실시간 행성 (최대 2)
    mp = _moon_phase_kr(today)
    moon_prompt = {
        "보름달": "오늘 밤 보름달을 크게 보여줘",
        "상현달": "오늘 초저녁 상현달을 보여줘",
        "하현달": "오늘 새벽 하현달을 보여줘",
    }
    if mp["name"] in moon_prompt:                  # 보름/상현/하현달일 때만
        out.append({"icon": mp["icon"], "name": "%s (%d%%)" % (mp["name"], mp["pct"]),
                    "dateLabel": "오늘 밤", "prompt": moon_prompt[mp["name"]]})
    return out


def _season_pool(today: dt.date) -> list:
    """이번 계절에 볼 수 있는 천체 풀 전체(프런트가 열 때마다 무작위 선택)."""
    return [{"icon": p["icon"], "name": p["name"], "dateLabel": p["label"],
             "prompt": p["prompt"]} for p in SEASONAL_SKY[_season_kr(today.month)]]


def sky_events(arg: str = "") -> str:
    """천문 달력 데이터를 JSON 으로 반환.
    arg 는 관측지 JSON({"city","lat","lon"}) 또는 빈 문자열(기본 청주)."""
    try:
        city, lat, lon = "청주", _CJU_LAT, _CJU_LON
        if arg:
            try:
                o = json.loads(arg)
                if isinstance(o, dict):
                    city = str(o.get("city", city))[:20]
                    lat = float(o.get("lat", lat))
                    lon = float(o.get("lon", lon))
                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):   # 방어
                        city, lat, lon = "청주", _CJU_LAT, _CJU_LON
            except Exception:
                pass
        today = dt.date.today()
        # 2026 달력이므로 연도를 2026 으로 맞춰 비교(연도 무관 MM-DD 기준)
        def to_date(mmdd: str) -> dt.date:
            m, d = mmdd.split("-")
            return dt.date(2026, int(m), int(d))

        items = []
        for ev in SKY_EVENTS_2026:
            meta = EVENT_TYPE_META.get(ev["type"], EVENT_TYPE_META["special"])
            sd = to_date(ev["date"])
            ed = to_date(ev["end"]) if ev.get("end") else sd
            span = (ed - sd).days
            if span == 0:
                label = "%d월 %d일" % (sd.month, sd.day)
            elif sd.month == ed.month:
                label = "%d월 %d~%d일" % (sd.month, sd.day, ed.day)
            else:                                   # 달을 넘기는 장기 이벤트(혜성 시즌 등)
                label = "%d월 %d일~%d월 %d일" % (sd.month, sd.day, ed.month, ed.day)
            items.append({
                **ev,
                "icon": meta["icon"], "typeLabel": meta["label"], "color": meta["color"],
                "month": sd.month, "dateLabel": label,
                "isLong": span > 40,                # 장기 시즌 이벤트 표시용
                "_sd": sd.isoformat(), "_ed": ed.isoformat(),
            })

        # 오늘 기준 다가오는 순으로 정렬(지난 것은 뒤로)
        cur = dt.date(2026, today.month, today.day)
        def sort_key(it):
            sd = dt.date.fromisoformat(it["_sd"])
            delta = (sd - cur).days
            # 예정(delta>=0): 가까운 순 우선. 지난(delta<0): 그 뒤로 밀되, 최근 지난 것 우선.
            return (delta < 0, delta if delta >= 0 else -delta)
        upcoming = sorted(items, key=sort_key)

        # 하이라이트: 오늘 진행 중인 '단기' 이벤트 우선 → 없으면 가장 가까운 예정 이벤트
        ongoing = [it for it in items
                   if not it["isLong"]
                   and dt.date.fromisoformat(it["_sd"]) <= cur <= dt.date.fromisoformat(it["_ed"])]
        highlight = ongoing[0] if ongoing else next(
            (it for it in upcoming if not it["isLong"]), upcoming[0])

        return json.dumps({
            "today": today.isoformat(),
            "todayLabel": "%d월 %d일" % (today.month, today.day),
            "moon": _moon_phase_kr(today),
            "loc": {"city": city, "lat": round(lat, 2), "lon": round(lon, 2)},
            "sun": _sun_times(today, lat, lon),  # 오늘 일출/남중/일몰 (KST)
            "always": _today_real(today, lat, lon),  # 실시간 행성 + 달 (실제)
            "seasonPool": _season_pool(today),   # 계절 천체 풀 (열 때마다 무작위)
            "highlight": highlight,
            "upcoming": upcoming[:6],
            "all": sorted(items, key=lambda x: x["_sd"]),
            "types": EVENT_TYPE_META,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "all": []}, ensure_ascii=False)


def convert_spc(spc_text: str, timed: bool) -> str:
    if _spc_to_python is None:
        return "# 오류: converter/ 폴더가 업로드되지 않았습니다 (%s)" % _conv_err
    spc_text = (spc_text or "").strip()
    if not spc_text:
        return "# SPC 내용을 붙여넣어 주세요."
    if len(spc_text) > MAX_SPC_BYTES:
        return "# 오류: 입력이 너무 큽니다 (5MB 초과) — .SPC 파일이 맞는지 확인해 주세요."
    try:
        return _spc_to_python(spc_text, timed=bool(timed))
    except Exception as e:  # noqa: BLE001
        return "# 변환 오류: %s\n# (SPC 형식이 맞는지 확인해 주세요 — TAB 구분 E/C 라인)" % e


_client = None          # 지연 생성 — 키 없이 import 해도 앱은 뜬다
_model = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def _pick_model(client) -> str:
    global _model
    if _model:
        return _model
    env = os.environ.get("GROQ_MODEL", "").strip()
    if env:
        _model = env
        return _model
    try:
        available = {m.id for m in client.models.list().data}
        for cand in PREFERRED_MODELS:
            if cand in available:
                _model = cand
                return _model
        chat_like = sorted(m for m in available
                           if "whisper" not in m and "guard" not in m and "tts" not in m)
        if chat_like:
            _model = chat_like[0]
            return _model
    except Exception:
        pass
    _model = PREFERRED_MODELS[0]
    return _model


def _extract_code(text: str) -> str:
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.DOTALL)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()


def _build_messages(prompt: str, history_json: str) -> list:
    """system + 이전 턴(질문/코드) + 새 질문 — '이 코드 수정해줘'가 통하게 하는 핵심."""
    messages = [{"role": "system", "content": SYSTEM}]
    try:
        hist = json.loads(history_json) if history_json else []
        assert isinstance(hist, list)
    except Exception:
        hist = []
    for m in hist[-4:]:                              # 최근 4턴까지만 (분당 토큰 한도 보호)
        if not isinstance(m, dict):
            continue
        q = str(m.get("q", ""))[:1500]
        code = str(m.get("code", ""))[:3500]
        if q:
            messages.append({"role": "user", "content": q})
        if code:
            messages.append({"role": "assistant",
                             "content": "```python\n" + code + "\n```"})
    messages.append({"role": "user", "content": prompt})
    return messages


def _is_too_large(err) -> bool:
    # 413: 단일 요청이 너무 큼(입력 토큰 과다). 히스토리를 빼면 통과할 수 있음.
    s = str(err)
    return "413" in s or "Request too large" in s or "reduce the length" in s


def _is_rate_limit(err) -> bool:
    # 429: 분당/일일 토큰·요청 한도 초과. 잠시 뒤 재시도 또는 다른 모델 필요.
    s = str(err).lower()
    return "rate_limit" in s or "rate limit" in s or "too many requests" in s or "error code: 429" in s


def _is_decommissioned(err) -> bool:
    # 모델 폐기/미존재: 다음 모델로 자동 스킵.
    s = str(err).lower()
    return "decommissioned" in s or "model_not_found" in s or "does not exist" in s


# ── 씬 플랜 생성 ──────────────────────────────────────────────
PLAN_SYSTEM = """당신은 Sky Explorer 플라네타리움 쇼의 씬 기획자다.
사용자의 자연어 요청을 분석해 쇼를 구성하는 씬 계획을 JSON으로 반환한다.

출력 규칙:
- 반드시 유효한 JSON 객체만 출력한다. 마크다운 코드블록·설명 텍스트 절대 금지.
- 씬은 Sky Explorer Python 스크립트의 논리적 단계를 나타낸다.
- duration은 해당 씬의 총 소요 시간(초, 소수점 1자리).
- camera.type 목록: setup / fadeto / zoom / orbit / travel / observe / text

camera 파라미터 규칙:
  setup   : {"type":"setup"}
  fadeto  : {"type":"fadeto","target_height":90.0}       ← 돔 높이 0~90
  zoom    : {"type":"zoom","scale":0.5}                  ← R×scale (0.5=2배 확대)
  orbit   : {"type":"orbit","degrees":360,"step_dt":0.5} ← 공전
  travel  : {"type":"travel","distance_pc":400.0}        ← 우주 비행
  observe : {"type":"observe"}                           ← 감상/대기
  text    : {"type":"text"}                              ← 텍스트 오버레이

반환 형식 예시:
{"scenes":[
  {"id":1,"name":"초기 세팅","description":"암전 후 천체 활성화","duration":2.0,"camera":{"type":"setup"}},
  {"id":2,"name":"지구 도착","description":"FadeTo로 지구에 시점 고정","duration":4.0,"camera":{"type":"fadeto","target_height":90.0}},
  {"id":3,"name":"2배 줌인","description":"현재 거리 절반으로 줌인","duration":5.0,"camera":{"type":"zoom","scale":0.5}}
],"total_duration":11.0}
"""


def _format_plan_for_prompt(data: dict) -> str:
    """조정된 씬 플랜 → 프롬프트에 삽입할 지시문."""
    scenes = data.get("scenes", [])
    lines = ["[씬 계획 — 반드시 이 타이밍과 카메라 설정을 스크립트에 반영할 것]"]
    for s in scenes:
        cam = s.get("camera", {})
        cam_parts = ["type=%s" % cam.get("type", "?")]
        if "target_height" in cam:
            cam_parts.append("target_height=%.1f" % cam["target_height"])
        if "scale" in cam:
            cam_parts.append("scale=%.2f (R*%.2f로 setPositionR)" % (cam["scale"], cam["scale"]))
        if "degrees" in cam:
            cam_parts.append("orbit=%.0f°" % cam["degrees"])
        if "distance_pc" in cam:
            cam_parts.append("distance=%.1fpc" % cam["distance_pc"])
        lines.append("  씬%d [%s] %s — %.1f초 | %s" % (
            s.get("id", 0), s.get("name", ""), s.get("description", ""),
            s.get("duration", 0), ", ".join(cam_parts)
        ))
    total = sum(s.get("duration", 0) for s in scenes)
    lines.append("  총 소요시간: %.1f초" % total)
    return "\n".join(lines)


def _extract_json(text: str):
    """LLM 응답에서 첫 번째 완전한 JSON 객체를 중괄호 균형으로 추출.
    정규식 greedy 매칭이 뒤따르는 텍스트의 '{'까지 삼키는 문제를 방지."""
    start = text.find("{")
    if start == -1:
        return None
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def plan(prompt: str) -> str:
    """씬 플랜을 JSON 문자열로 반환한다."""
    global _model
    prompt = (prompt or "").strip()[:MAX_PROMPT_CHARS]   # 남용 방지: 길이 상한
    if not prompt:
        return json.dumps({"scenes": [], "error": "요청 없음"}, ensure_ascii=False)
    if not os.environ.get("GROQ_API_KEY"):
        return json.dumps({"scenes": [], "error": "API 키 없음"}, ensure_ascii=False)
    try:
        client = _get_client()
    except Exception as e:
        return json.dumps({"scenes": [], "error": str(e)}, ensure_ascii=False)

    # 캐시 모델이 폐기됐을 경우를 대비해 PREFERRED 순서로 최대 2개까지 시도
    tried = []
    for _ in range(3):
        model = _pick_model(client)
        if model in tried:
            # 후보가 소진되면 다음 PREFERRED 로 강제 이동
            remaining = [m for m in PREFERRED_MODELS if m not in tried]
            if not remaining:
                break
            model = remaining[0]
            _model = model
        tried.append(model)
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=0.3,
                max_tokens=900,
                messages=[
                    {"role": "system", "content": PLAN_SYSTEM},
                    {"role": "user", "content": prompt},
                ],
            )
            break
        except Exception as e:
            if _is_decommissioned(e) or _is_rate_limit(e):
                _model = None            # 캐시 무효화 → 다음 후보로
                continue
            return json.dumps({"scenes": [], "error": str(e)}, ensure_ascii=False)
    else:
        return json.dumps({"scenes": [], "error": "사용 가능한 모델 없음"}, ensure_ascii=False)

    try:
        text = resp.choices[0].message.content or ""
        raw = _extract_json(text)
        if not raw:
            return json.dumps({"scenes": [], "error": "JSON 파싱 실패"}, ensure_ascii=False)
        data = json.loads(raw)
        # 씬 데이터 정규화 — LLM이 필드를 빠뜨려도 UI가 깨지지 않게 기본값 보정
        if "scenes" in data and isinstance(data["scenes"], list):
            clean = []
            for i, s in enumerate(data["scenes"]):
                if not isinstance(s, dict):
                    continue
                cam = s.get("camera") if isinstance(s.get("camera"), dict) else {}
                try:
                    dur = float(s.get("duration", 2.0))
                except (TypeError, ValueError):
                    dur = 2.0
                dur = max(0.5, min(30.0, dur))
                # 카메라 수치 필드도 방어적으로 정규화
                if "target_height" in cam:
                    try:
                        cam["target_height"] = max(0.0, min(90.0, float(cam["target_height"])))
                    except (TypeError, ValueError):
                        cam["target_height"] = 90.0
                if "scale" in cam:
                    try:
                        cam["scale"] = max(0.1, min(3.0, float(cam["scale"])))
                    except (TypeError, ValueError):
                        cam["scale"] = 0.5
                if "degrees" in cam:
                    try:
                        cam["degrees"] = max(30.0, min(720.0, float(cam["degrees"])))
                    except (TypeError, ValueError):
                        cam["degrees"] = 360.0
                if "distance_pc" in cam:
                    try:
                        cam["distance_pc"] = max(1.0, min(1000.0, float(cam["distance_pc"])))
                    except (TypeError, ValueError):
                        cam["distance_pc"] = 400.0
                clean.append({
                    "id": i + 1,
                    "name": str(s.get("name", "씬 %d" % (i + 1)))[:40],
                    "description": str(s.get("description", ""))[:120],
                    "duration": round(dur, 1),
                    "camera": cam if cam else {"type": "observe"},
                })
            data["scenes"] = clean
            data["total_duration"] = round(sum(s["duration"] for s in clean), 1)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"scenes": [], "error": str(e)}, ensure_ascii=False)


def generate(prompt: str, history_json: str = "", scenes_json: str = "") -> str:
    global _model
    prompt = (prompt or "").strip()[:MAX_PROMPT_CHARS]   # 남용 방지: 길이 상한
    if not prompt:
        return "# 요청을 입력해 주세요."
    if not os.environ.get("GROQ_API_KEY"):
        return ("# 오류: GROQ_API_KEY 가 설정되지 않았습니다.\n"
                "# Space Settings → Variables and secrets → New secret 에서\n"
                "# Name: GROQ_API_KEY / Value: console.groq.com 발급 키 를 추가하세요.")

    # 씬 플랜이 있으면 프롬프트에 타이밍 지시문 삽입
    if scenes_json:
        try:
            plan_data = json.loads(scenes_json)
            if plan_data.get("scenes"):
                prompt = _format_plan_for_prompt(plan_data) + "\n\n원래 요청: " + prompt
        except Exception:
            pass

    try:
        client = _get_client()
        first_model = _pick_model(client)
    except Exception as e:
        return "# Groq API 오류: %s" % e

    # 재시도 대상 모델: 현재 모델 우선, 이후 PREFERRED 순서.
    # models.list() 호출은 실패해도 무시하고 PREFERRED 로 폴백(불필요한 API 왕복 방지).
    fallback_models = [first_model] + [m for m in PREFERRED_MODELS if m != first_model]

    last_err = None
    hit_rate_limit = False
    for model_candidate in fallback_models:
        # 히스토리 포함 → (413 발생 시) 히스토리 제거 순으로 시도
        histories = [history_json] + ([""] if history_json else [])
        for hist in histories:
            try:
                resp = client.chat.completions.create(
                    model=model_candidate,
                    temperature=0.2,
                    # Groq TPM = 입력토큰 + max_tokens(응답예약). 8b 모델은 분당 6K 라
                    # 큰 시스템 프롬프트 + 큰 예약분이면 1회 호출로도 한도 초과 → 예약분 축소.
                    max_tokens=1400,
                    messages=_build_messages(prompt, hist),
                )
                _model = model_candidate
                text = resp.choices[0].message.content or ""
                return _extract_code(text)
            except Exception as e:
                last_err = e
                if _is_too_large(e) and hist:
                    continue            # 토큰 초과 → 히스토리 빼고 같은 모델 재시도
                if _is_rate_limit(e):
                    hit_rate_limit = True
                    break               # 이 모델은 한도 초과 → 다음 모델로
                if _is_decommissioned(e):
                    break               # 폐기된 모델 → 다음 모델로 (원문 노출 안 함)
                # 그 외 에러(모델명·파라미터·서버 오류 등)는 원문을 그대로 보여준다.
                _model = None
                return "# Groq API 오류 (%s): %s" % (model_candidate, e)

    _model = None
    if hit_rate_limit:
        return ("# ⏳ 사용 가능한 모델의 분당 토큰 한도(TPM)에 걸렸습니다.\n"
                "# 30초~1분 뒤에 다시 시도해 주세요. (일일 한도가 아니라 분당 한도입니다)\n"
                "# ─ 상세: %s" % last_err)
    return "# Groq API 오류: %s" % last_err


# ═════════════════════════════════════════════════════════════════
# 커스텀 UI — 우주 테마 + 사이드바 대화 로그 (Claude/Gemini 스타일)
# ═════════════════════════════════════════════════════════════════
CUSTOM_HTML = """
<div class="bg"><div class="earth-limb"></div><div class="atmo-glow"></div></div>

<div class="shell">
  <div class="sidebar">
    <div class="brand">🌌 Sky Explorer <span class="g">AI</span></div>
    <div class="side-tab active" id="tabChat">💬 스크립트 생성</div>
    <button class="new-chat" id="newChatBtn">＋ 새 대화</button>
    <div class="side-sec">대화 기록
      <button class="clear-all" id="clearAllBtn" title="기록 전체 삭제">🗑 전체 삭제</button>
    </div>
    <div class="conv-list" id="convList"></div>
    <div class="side-tab" id="tabConv">🔁 SPC → Python 변환</div>
    <div class="side-foot">지식: 실측 검증 레퍼런스<br>엔진: Groq · Llama</div>
  </div>

  <main>
    <div class="welcome" id="welcomeScreen">
      <h1 id="welcomeTitle">당신의 우주를 그려보세요!</h1>
      <div class="input-wrap">
        <div class="input-row">
          <textarea id="promptInput" placeholder="어떤 우주 현상을 보고 싶나요? (예: 토성을 화면 중앙으로 확대해 줘)"></textarea>
          <button class="run" id="runBtn">스크립트 생성 ✨</button>
        </div>
        <div class="gen-opts" id="genOpts">
          <label class="opt-chk"><input type="checkbox" id="teachChk"> 🎓 수업용 해설 주석</label>
          <span class="opt-presets">⏱ 길이
            <button type="button" class="opt-len on" data-len="">기본</button>
            <button type="button" class="opt-len" data-len="전체 길이를 30초 정도로 짧게 만들어줘. ">30초</button>
            <button type="button" class="opt-len" data-len="수업용으로 3분 정도 길이로 만들어줘. ">3분</button>
            <button type="button" class="opt-len" data-len="발표용으로 5분 정도 여유있게 만들어줘. ">5분</button>
          </span>
        </div>
        <div class="chips" id="chipRow">
          <div class="chip" data-p="토성으로 가서 크게 보여줘">🪐 토성으로 가서 크게 보여줘</div>
          <div class="chip" data-p="지구를 돔 한가운데 놓고 두 배 확대해줘">🌍 지구를 돔 한가운데서 두 배로 키워줘</div>
          <div class="chip" data-p="말머리성운까지 여행하는 쇼 만들어줘">🐴 말머리성운까지 여행을 떠나요</div>
          <div class="chip" data-p="오늘 밤 청주 하늘 보여줘">🌃 오늘 밤 청주 하늘을 보여줘</div>
          <div class="chip" data-p="은하수를 켜줘">🌌 은하수를 하늘에 켜줘</div>
          <div class="chip" data-p="화면에 '우주에 오신 것을 환영합니다' 라고 띄워줘">✨ 환영 인사를 화면에 띄워줘</div>
        </div>
        <div class="onboard-hint">💡 생성된 스크립트를 <b>복사·다운로드(.py)</b> → Sky Explorer <b>Studio에 가져오면</b> 돔에서 실행됩니다.</div>
      </div>
    </div>

    <div class="chat-scroll" id="chatScroll"><div class="chat-area" id="chatView"></div></div>

    <div class="conv-view" id="convView" style="display:none">
      <div class="conv-box">
        <h2>🔁 SPC → Python 변환기</h2>
        <p class="conv-hint">Studio 녹화 .SPC 파일 내용을 붙여넣으면, 우리가 실측으로 만든
           매핑 테이블로 Python 스크립트를 복원합니다.</p>
        <div class="conv-controls">
          <label class="file-btn">📂 파일 선택<input type="file" id="spcFile" accept=".SPC,.spc,.txt" hidden></label>
          <label class="timed-chk"><input type="checkbox" id="timedChk" checked> 타임코드 → sleep() 재현</label>
        </div>
        <textarea id="spcInput" class="spc-ta" placeholder="여기에 .SPC 파일 내용을 붙여넣거나, 위에서 파일을 선택하세요"></textarea>
        <button class="run" id="convBtn">Python 으로 변환 🔁</button>
        <div class="msg-result" id="convResult" style="display:none; margin-top:14px">
          <div class="log-ticker done" id="convTicker">✓ 변환 완료</div>
          <div class="code-block">
            <div class="code-tools">
              <button class="tool-btn" id="convEdit">✎ 수정</button>
              <button class="tool-btn" id="convCopy">복사</button>
              <button class="tool-btn" id="convDl">.py 저장</button>
            </div>
            <pre id="convPre" spellcheck="false"></pre>
          </div>
        </div>
      </div>
    </div>

    <button class="sky-fab" id="skyFab" title="2026 천문 달력 열기">📅<span class="sky-fab-txt">천문 달력</span></button>

    <div class="sky-backdrop" id="skyBackdrop"></div>
    <aside class="sky-drawer" id="skyDrawer" aria-hidden="true">
      <div class="sky-drawer-head">
        <div class="sky-drawer-title">
          <h2>🔭 2026 천문 달력</h2>
          <div class="sky-loc-row">📍 관측지
            <select class="sky-loc-select" id="skyLoc"></select>
            <span class="sky-loc-coord" id="skyLocCoord"></span>
          </div>
        </div>
        <button class="sky-close" id="skyClose" title="닫기">✕</button>
      </div>
      <div class="sky-drawer-body">
        <div class="sky-today" id="skyToday"><div class="sky-loading">천문 데이터를 불러오는 중…</div></div>

        <div class="sky-cal">
          <div class="sky-cal-nav">
            <button class="sky-cal-arrow" id="skyPrev" title="이전 달">‹</button>
            <span class="sky-cal-month" id="skyMonthLabel">2026</span>
            <button class="sky-cal-arrow" id="skyNext" title="다음 달">›</button>
          </div>
          <div class="sky-cal-weekdays">
            <span>일</span><span>월</span><span>화</span><span>수</span><span>목</span><span>금</span><span>토</span>
          </div>
          <div class="sky-cal-grid" id="skyCalGrid"></div>
          <div class="sky-cal-legend" id="skyLegend"></div>
        </div>

        <div class="sky-sec-title" id="skyMonthTitle">🗓 이 달의 천문현상</div>
        <div class="sky-list" id="skyMonthList"></div>
      </div>
    </aside>

    <div class="bottom-bar" id="bottomBar" style="display:none">
      <div class="input-row">
        <textarea id="bottomInput" placeholder="다음 장면을 설명하세요... (Enter 전송 · Shift+Enter 줄바꿈)"></textarea>
        <button class="run" id="bottomBtn">생성 ✨</button>
      </div>
    </div>
  </main>

  <a class="meta-badge" href="#" title="METASPACE" onclick="return false;">
    <span class="meta-by">powered by</span> METASPΛCE
  </a>
</div>
"""

CUSTOM_CSS = """
/* ── Gradio 껍데기 숨김 + 페이지 스크롤 잠금(점프 방지) ── */
footer { display: none !important; }
.gradio-container { max-width: 100% !important; padding: 0 !important; margin: 0 !important;
                    background: transparent !important; }
#hidden-io { display: none !important; }
html, body { overflow: hidden !important; height: 100%; }
body { background: #04060c !important; }

:root {
  --bg:#04060c; --panel:rgba(10,13,22,.85); --sb:rgba(5,7,13,.94);
  --line:rgba(255,255,255,.08); --ls:rgba(255,255,255,.05);
  --txt:#d8dff0; --dim:#7a8499;
  --accent:#ffb84d; --as:rgba(255,184,77,.14); --nova:#5ee6c4;
  --mono:"JetBrains Mono","Fira Code",monospace;
  --sans:"Inter","Pretendard",-apple-system,sans-serif;
  --sw:272px;
}

/* ── 우주 배경 + 지구 광채 ── */
@keyframes bgFade { 0%{opacity:0;} 100%{opacity:1;} }
.bg.fresh { animation: bgFade 1.4s ease both; }
.bg { position:fixed; inset:0; z-index:0;
  background: radial-gradient(ellipse 60% 40% at 50% 132%, rgba(255,210,150,.10), transparent 60%),
              radial-gradient(circle at 50% 50%, #0a1a3a 0%, #050a18 38%, #02040a 60%, #000102 100%);
  overflow:hidden; }
.earth-limb { position:absolute; bottom:-78%; left:50%; transform:translateX(-50%);
  width:185%; height:160%; border-radius:50%;
  background: radial-gradient(circle at 38% 22%, #6fb0e8 0%, #3f7fc4 8%, #2a5a9e 16%, #1c3f78 26%, #0f2552 40%, #081636 55%, #04091f 72%, transparent 86%);
  box-shadow: 0 0 120px 40px rgba(80,150,230,.25), 0 0 280px 90px rgba(60,120,210,.10); }
.earth-limb::before { content:""; position:absolute; inset:0; border-radius:50%;
  background: radial-gradient(circle at 30% 18%, rgba(255,255,255,.18), transparent 30%),
              radial-gradient(circle at 60% 30%, rgba(255,255,255,.08), transparent 35%);
  mix-blend-mode:screen; }
.atmo-glow { position:absolute; bottom:-80%; left:50%; transform:translateX(-50%);
  width:190%; height:165%; border-radius:50%;
  box-shadow: 0 0 2px 2px rgba(140,195,255,.55); pointer-events:none; }

/* ── 레이아웃 ── */
.shell { position:fixed; inset:0; z-index:1; display:flex;
         font-family:var(--sans); color:var(--txt); }
.sidebar { width:var(--sw); flex-shrink:0; background:var(--sb); backdrop-filter:blur(20px);
  border-right:1px solid var(--line); display:flex; flex-direction:column;
  padding:20px 12px; height:100vh; z-index:10; }
.brand { display:flex; align-items:center; gap:8px; padding:2px 8px 16px;
         font-size:16px; font-weight:700; letter-spacing:-.01em; flex-wrap:wrap; }
.brand .g { color:var(--accent); }
.brand-logo { height:20px; width:auto; margin-left:2px; margin-top:4px; opacity:.95;
              flex-basis:100%; max-width:210px; }

/* METASPACE 회사 배지 — 우하단 고정(유지, 은은하게) */
.meta-badge { position:fixed; right:16px; bottom:12px; z-index:2;
  font-family:'Arial Black','Helvetica Neue',Arial,sans-serif; font-weight:900;
  font-size:13px; letter-spacing:1px; color:#4a63b8; text-decoration:none;
  opacity:.7; pointer-events:none; user-select:none; }
.meta-badge .meta-by { font-family:var(--sans); font-weight:600; font-size:9.5px;
  letter-spacing:.04em; color:var(--dim); margin-right:5px; text-transform:uppercase; }

/* 온보딩 한 줄 안내 */
.onboard-hint { margin-top:16px; font-size:12.5px; color:var(--dim); line-height:1.6;
  background:rgba(255,255,255,.03); border:1px solid var(--ls); border-radius:10px;
  padding:10px 14px; text-align:center; }
.onboard-hint b { color:#c8d2e8; font-weight:600; }

/* 생성 코드 린트 도움말 */
.lint-box { border-top:1px solid var(--line); padding:10px 14px; display:flex;
  flex-direction:column; gap:6px; background:rgba(255,255,255,.015); }
.lint-head { font-size:11.5px; font-weight:700; color:#cdd6ea; margin-bottom:2px; }
.lint-item { font-size:11.5px; line-height:1.5; color:#b8c2d8; padding:5px 9px;
  border-radius:7px; border-left:2px solid var(--line); }
.lint-err  { background:rgba(255,107,138,.08);  border-left-color:#ff6b8a; color:#ffc2cf; }
.lint-warn { background:rgba(255,184,77,.08);   border-left-color:var(--accent); color:#ffe0b0; }
.lint-info { background:rgba(94,230,196,.06);   border-left-color:var(--nova); color:#b8ead9; }
.lint-ok   { font-size:11.5px; color:#7fcfa8; }

/* 생성 옵션 (해설 주석 · 길이 프리셋) */
.gen-opts { display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  margin-top:12px; justify-content:center; }
.opt-chk { display:flex; align-items:center; gap:6px; font-size:12.5px; color:#c8d2e8;
  cursor:pointer; user-select:none; }
.opt-chk input { accent-color:var(--accent); cursor:pointer; }
.opt-presets { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--dim); }
.opt-len { font-family:var(--sans); font-size:11.5px; color:var(--dim);
  background:rgba(255,255,255,.04); border:1px solid var(--line); border-radius:14px;
  padding:4px 11px; cursor:pointer; transition:all .14s; }
.opt-len:hover { color:#dce3f2; border-color:rgba(255,255,255,.2); }
.opt-len.on { background:var(--as); border-color:rgba(255,184,77,.45); color:var(--accent); font-weight:600; }

/* ── 사이드바: 새 대화 + 대화 목록 ── */
.new-chat { background:var(--as); border:1px solid var(--accent); color:var(--accent);
  border-radius:10px; padding:10px 12px; font-family:var(--sans); font-weight:700;
  font-size:13px; cursor:pointer; margin:0 4px 14px; text-align:left; transition:background .15s; }
.new-chat:hover { background:rgba(255,184,77,.25); }
.side-sec { padding:4px 8px 6px; font-size:11px; font-weight:700; color:var(--dim);
            letter-spacing:.08em; text-transform:uppercase;
            display:flex; align-items:center; justify-content:space-between; }
.clear-all { background:none; border:none; color:var(--dim); font-size:10.5px;
             font-family:var(--sans); cursor:pointer; padding:2px 4px; border-radius:4px; }
.clear-all:hover { color:#ff7a7a; }
.conv-list { flex:1; overflow-y:auto; min-height:0; padding:0 2px; }
.conv-item { display:flex; align-items:center; gap:6px; padding:9px 10px; font-size:13px;
  color:var(--txt); border-radius:8px; cursor:pointer; margin-bottom:2px;
  transition:background .12s; }
.conv-item:hover { background:var(--ls); }
.conv-item.active { background:var(--as); color:var(--accent); }
.conv-title { flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.conv-del, .conv-edit { flex-shrink:0; background:none; border:none; color:var(--dim);
  cursor:pointer; font-size:12px; padding:2px 4px; border-radius:4px; opacity:0;
  transition:opacity .12s, color .12s; }
.conv-item:hover .conv-del, .conv-item:hover .conv-edit { opacity:1; }
.conv-del:hover { color:#ff7a7a; }
.conv-edit:hover { color:var(--accent); }
.conv-empty { padding:10px; font-size:12px; color:var(--dim); }
.side-foot { padding:12px 8px 0; font-size:11px; color:var(--dim); line-height:1.7;
             border-top:1px solid var(--line); margin-top:10px; }

main { flex:1; min-width:0; position:relative; display:flex; flex-direction:column; }

/* ── 웰컴 ── */
.welcome { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; padding:0 28px 60px; z-index:5;
  transition:opacity .38s ease, transform .38s ease; }
.welcome.out { opacity:0; pointer-events:none; transform:translateY(-14px); }
.welcome h1 { font-weight:700; font-size:clamp(26px,4.5vw,46px); line-height:1.14;
  margin:0 0 32px; letter-spacing:-.02em; text-align:center;
  text-shadow:0 2px 32px rgba(0,0,0,.6); }
@keyframes headFade { 0%{opacity:0; transform:translateY(6px); filter:blur(4px);}
                      100%{opacity:1; transform:translateY(0); filter:blur(0);} }
.welcome.fresh h1 { animation:headFade 1.0s ease both; }
.welcome.fresh .input-wrap { animation:headFade 1.0s ease .18s both; }
.input-wrap { width:min(720px, 92%); }

/* ── 입력 ── */
.input-row { display:flex; gap:8px; align-items:flex-end; }
.shell textarea { flex:1; background:rgba(8,12,22,.78); border:1px solid var(--line);
  border-radius:14px; color:var(--txt); font-family:var(--sans); font-size:15px;
  font-weight:500; line-height:1.5; padding:14px 16px; resize:none; min-height:52px;
  max-height:160px; outline:none; transition:border-color .15s, box-shadow .15s; }
.shell textarea:focus { border-color:var(--accent); box-shadow:0 0 0 3px var(--as); }
button.run { background:var(--accent); color:#1a1206; border:none; border-radius:14px;
  font-family:var(--sans); font-weight:700; font-size:13.5px; letter-spacing:.01em;
  padding:15px 20px; cursor:pointer; white-space:nowrap; flex-shrink:0;
  transition:transform .12s, box-shadow .12s; }
button.run:hover { box-shadow:0 0 0 3px var(--as); }
button.run:disabled { opacity:.5; cursor:wait; }

/* ── chips ── */
.chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; justify-content:center; }
.chip { background:rgba(10,14,26,.7); border:1px solid var(--line); border-radius:999px;
  padding:8px 14px; font-size:12.5px; color:var(--txt); cursor:pointer;
  transition:border-color .15s, background .15s; user-select:none; }
.chip:hover { border-color:var(--accent); background:var(--as); }

/* ── 채팅: 자체 스크롤 컨테이너 (페이지 점프 방지 핵심) ── */
.chat-scroll { position:absolute; inset:0; overflow-y:auto; overscroll-behavior:contain;
  opacity:0; pointer-events:none; transition:opacity .35s .12s; }
.chat-scroll.in { opacity:1; pointer-events:auto; }
.chat-area { max-width:840px; margin:0 auto; padding:32px 24px 140px; }
.msg-block { margin-bottom:22px; animation:rise .3s ease; }
@keyframes rise { from{opacity:0; transform:translateY(7px);} to{opacity:1; transform:translateY(0);} }
.msg-user { font-size:14.5px; color:var(--nova); font-family:var(--sans); font-weight:600;
  margin:0 0 8px 2px; }
.msg-result { border:1px solid var(--line); border-radius:4px 14px 14px 14px; overflow:hidden;
  background:var(--panel); backdrop-filter:blur(14px); }
.log-ticker { background:#020408; padding:15px 18px; font-family:var(--sans); font-size:13px;
  min-height:54px; display:flex; align-items:center; gap:10px; color:var(--dim); }
.log-ticker.done { color:var(--nova); }
.code-block { position:relative; background:rgba(2,4,9,.6); }
.code-block pre { margin:0; padding:15px 18px; font-family:var(--mono); font-size:13.5px;
  font-weight:400; line-height:1.75; color:#d9e0f2; overflow-x:auto; white-space:pre; }
.code-block pre[contenteditable]:focus { outline:none; background:rgba(4,8,16,.85);
  box-shadow:inset 0 0 0 1px var(--as); caret-color:var(--accent); }
.code-tools { position:absolute; top:10px; right:10px; display:flex; gap:6px; z-index:2; }
.tool-btn { background:rgba(255,255,255,.06); border:1px solid var(--line); border-radius:8px;
  color:var(--txt); font-size:11.5px; font-family:var(--sans); padding:6px 10px; cursor:pointer;
  transition:border-color .12s, color .12s; }
.tool-btn:hover { border-color:var(--accent); }
.tool-btn.on { border-color:var(--accent); color:var(--accent); background:var(--as); }

/* ── 사이드바 탭 (생성=상단 / SPC 변환=대화기록 아래) ── */
.side-tab { padding:10px 12px; font-size:13px; font-weight:600; color:var(--dim); cursor:pointer;
  border:1px solid var(--line); border-radius:10px; margin:0 4px 10px;
  transition:background .12s, color .12s, border-color .12s; }
.side-tab:hover { background:var(--ls); color:var(--txt); }
.side-tab.active { background:var(--as); color:var(--accent); border-color:var(--accent); }
#tabConv { margin-top:12px; margin-bottom:0; flex-shrink:0; }

/* ── 변환기 뷰 ── */
.conv-view { position:absolute; inset:0; overflow-y:auto; overscroll-behavior:contain; z-index:6; }
.conv-box { max-width:840px; margin:0 auto; padding:40px 24px 80px; }
.conv-box h2 { font-size:22px; font-weight:700; margin:0 0 6px; }
.conv-hint { font-size:13px; color:var(--dim); margin:0 0 18px; line-height:1.6; }
.conv-controls { display:flex; gap:14px; align-items:center; margin-bottom:10px; flex-wrap:wrap; }
.file-btn { background:rgba(10,14,26,.7); border:1px solid var(--line); border-radius:10px;
  padding:9px 14px; font-size:12.5px; cursor:pointer; transition:border-color .15s; }
.file-btn:hover { border-color:var(--accent); }
.timed-chk { font-size:12.5px; color:var(--dim); display:flex; gap:6px; align-items:center; cursor:pointer; }
.spc-ta { width:100%; min-height:180px; max-height:320px; background:rgba(8,12,22,.78);
  border:1px solid var(--line); border-radius:14px; color:var(--txt); font-family:var(--mono);
  font-size:12px; line-height:1.5; padding:14px 16px; resize:vertical; outline:none;
  margin-bottom:10px; }
.spc-ta:focus { border-color:var(--accent); box-shadow:0 0 0 3px var(--as); }

/* ── 하단 바 ── */
.bottom-bar { position:absolute; left:0; right:0; bottom:0; padding:12px 24px 18px;
  background:linear-gradient(to top, rgba(4,6,12,.99) 60%, transparent);
  backdrop-filter:blur(16px); z-index:8; }

@media (max-width: 720px) {
  :root { --sw: 0px; }
  .sidebar { display:none; }
}

/* ══ 천문 달력 탭 ══════════════════════════════════════════ */
.sky-view { position:absolute; inset:0; overflow-y:auto; padding:34px 26px 60px; }
.sky-box { max-width:900px; margin:0 auto; }
.sky-head { display:flex; align-items:baseline; gap:14px; margin-bottom:20px; flex-wrap:wrap; }
.sky-head h2 { margin:0; font-size:21px; font-weight:700; color:#eef1fa; letter-spacing:-.01em; }
.sky-loc { font-family:var(--mono); font-size:11.5px; color:var(--dim);
  background:rgba(255,255,255,.05); border:1px solid var(--line);
  border-radius:20px; padding:4px 11px; }

/* 관측지 선택 */
.sky-loc-row { display:flex; align-items:center; gap:7px; flex-wrap:wrap;
  font-size:11.5px; color:var(--dim); }
.sky-loc-select { font-family:var(--sans); font-size:12px; font-weight:600; color:#eef1fa;
  background:rgba(255,255,255,.06); border:1px solid var(--line); border-radius:8px;
  padding:3px 8px; cursor:pointer; outline:none; }
.sky-loc-select:hover { border-color:rgba(255,184,77,.4); }
.sky-loc-coord { font-family:var(--mono); font-size:10.5px; color:var(--dim); }

/* 오늘 태양(일출/남중/일몰) 라인 */
.sky-sun { font-size:11.5px; color:#b8c2d8; margin:8px 0 2px; letter-spacing:-.01em; }
.sky-sun b { color:var(--accent); font-weight:700; font-family:var(--mono); }

/* 오늘의 하이라이트 */
.sky-today { background:linear-gradient(135deg, rgba(255,184,77,.12), rgba(94,230,196,.07));
  border:1px solid rgba(255,184,77,.28); border-radius:16px; padding:20px 22px; margin-bottom:26px; }
.sky-loading { color:var(--dim); font-family:var(--mono); font-size:13px; padding:12px 0; }
.sky-today-top { display:flex; align-items:center; gap:10px; margin-bottom:14px; flex-wrap:wrap; }
.sky-date-badge { font-family:var(--mono); font-size:11px; color:var(--accent);
  background:var(--as); border:1px solid rgba(255,184,77,.3); border-radius:7px; padding:3px 10px; }
.sky-moon { font-size:12.5px; color:var(--dim); }
.sky-moon b { color:#c8d2e8; font-weight:600; }
.sky-hl-title { display:flex; align-items:center; gap:10px; margin-bottom:6px; }
.sky-hl-icon { font-size:26px; }
.sky-hl-name { font-size:17px; font-weight:700; color:#fff; }
.sky-hl-when { font-family:var(--mono); font-size:12px; color:var(--accent); margin-left:2px; }
.sky-hl-desc { font-size:13.5px; color:#b8c2d8; line-height:1.6; margin:8px 0 10px; }
.sky-hl-tip { font-size:12.5px; color:var(--nova); background:rgba(94,230,196,.08);
  border-left:2px solid rgba(94,230,196,.45); border-radius:0 7px 7px 0;
  padding:8px 12px; margin-bottom:14px; line-height:1.55; }

.sky-btn { background:var(--accent); color:#1a1206; border:none; border-radius:10px;
  padding:10px 16px; font-family:var(--sans); font-weight:700; font-size:13px;
  cursor:pointer; transition:transform .12s, opacity .15s; }
.sky-btn:hover { opacity:.88; transform:translateY(-1px); }
.sky-btn:active { transform:translateY(0); }

/* 섹션 제목 */
.sky-sec-title { display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  font-size:14px; font-weight:700; color:#dce3f2; margin:26px 0 13px; }

/* 다가오는 이벤트 카드 그리드 */
.sky-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(232px,1fr)); gap:11px; }
.sky-card { background:rgba(255,255,255,.04); border:1px solid var(--line);
  border-radius:12px; padding:14px 15px; cursor:pointer;
  transition:border-color .15s, background .15s, transform .12s; }
.sky-card:hover { border-color:rgba(255,184,77,.4); background:rgba(255,184,77,.06);
  transform:translateY(-2px); }
.sky-card-top { display:flex; align-items:center; gap:8px; margin-bottom:7px; }
.sky-card-icon { font-size:17px; }
.sky-card-date { font-family:var(--mono); font-size:10.5px; color:var(--dim); }
.sky-card-tag { margin-left:auto; font-family:var(--mono); font-size:9.5px;
  border-radius:5px; padding:2px 7px; letter-spacing:.04em; }
.sky-card-name { font-size:13.5px; font-weight:600; color:#eef1fa; line-height:1.4; margin-bottom:5px; }
.sky-card-desc { font-size:11.5px; color:var(--dim); line-height:1.5; }

/* 필터 칩 */
.sky-filters { display:flex; gap:6px; flex-wrap:wrap; margin-left:auto; }
.sky-fchip { font-family:var(--mono); font-size:10.5px; color:var(--dim);
  background:rgba(255,255,255,.04); border:1px solid var(--line);
  border-radius:20px; padding:4px 11px; cursor:pointer; transition:all .14s; }
.sky-fchip:hover { color:#dce3f2; border-color:rgba(255,255,255,.2); }
.sky-fchip.on { background:var(--as); border-color:rgba(255,184,77,.45); color:var(--accent); }

/* 전체 일정 리스트 */
.sky-list { display:flex; flex-direction:column; gap:7px; }
.sky-row { display:flex; align-items:flex-start; gap:13px; padding:13px 15px;
  background:rgba(255,255,255,.03); border:1px solid var(--line);
  border-radius:11px; cursor:pointer; transition:border-color .15s, background .15s; }
.sky-row:hover { border-color:rgba(255,184,77,.35); background:rgba(255,184,77,.05); }
.sky-row-icon { font-size:19px; flex-shrink:0; margin-top:1px; }
.sky-row-body { flex:1; min-width:0; }
.sky-row-head { display:flex; align-items:center; gap:9px; flex-wrap:wrap; margin-bottom:4px; }
.sky-row-name { font-size:13.5px; font-weight:600; color:#eef1fa; }
.sky-row-date { font-family:var(--mono); font-size:11px; color:var(--accent); }
.sky-row-desc { font-size:12px; color:var(--dim); line-height:1.55; }
.sky-row-tip { font-size:11.5px; color:#8fa8c8; margin-top:5px; line-height:1.5; }
.sky-row-go { flex-shrink:0; font-size:11px; font-family:var(--mono); color:var(--dim);
  border:1px solid var(--line); border-radius:8px; padding:6px 10px;
  align-self:center; white-space:nowrap; transition:all .14s; }
.sky-row:hover .sky-row-go { color:var(--accent); border-color:rgba(255,184,77,.45); }

@media (max-width: 720px) {
  .sky-view { padding:24px 16px 50px; }
  .sky-grid { grid-template-columns:1fr; }
  .sky-row-go { display:none; }
}

/* ══ 천문 달력 드로어 (📅 버튼 → 우측 슬라이드) ══════════════ */
.sky-fab { position:fixed; top:18px; right:22px; z-index:60;
  display:flex; align-items:center; gap:8px;
  background:linear-gradient(135deg, rgba(255,184,77,.16), rgba(94,230,196,.10));
  border:1px solid rgba(255,184,77,.4); color:var(--accent);
  border-radius:24px; padding:9px 16px 9px 14px; cursor:pointer;
  font-family:var(--sans); font-weight:700; font-size:15px;
  backdrop-filter:blur(12px); transition:transform .14s, box-shadow .18s, background .18s;
  box-shadow:0 4px 20px rgba(0,0,0,.35); }
.sky-fab:hover { transform:translateY(-2px);
  background:linear-gradient(135deg, rgba(255,184,77,.28), rgba(94,230,196,.16));
  box-shadow:0 6px 26px rgba(255,184,77,.22); }
.sky-fab-txt { font-size:14px; letter-spacing:-.01em; }

.sky-backdrop { position:fixed; inset:0; z-index:70; background:rgba(3,5,11,.55);
  backdrop-filter:blur(2px); opacity:0; pointer-events:none; transition:opacity .28s; }
.sky-backdrop.open { opacity:1; pointer-events:auto; }

.sky-drawer { position:fixed; top:0; right:0; z-index:80;
  width:min(440px, 92vw); height:100vh;
  background:var(--sb); backdrop-filter:blur(24px);
  border-left:1px solid var(--line); box-shadow:-16px 0 48px rgba(0,0,0,.5);
  display:flex; flex-direction:column;
  transform:translateX(100%); transition:transform .32s cubic-bezier(.4,0,.2,1); }
.sky-drawer.open { transform:translateX(0); }

.sky-drawer-head { display:flex; align-items:flex-start; gap:12px;
  padding:20px 20px 15px; border-bottom:1px solid var(--line); flex-shrink:0; }
.sky-drawer-title h2 { margin:0 0 7px; font-size:18px; font-weight:700; color:#eef1fa;
  letter-spacing:-.01em; }
.sky-close { margin-left:auto; flex-shrink:0; width:34px; height:34px; border-radius:9px;
  background:rgba(255,255,255,.05); border:1px solid var(--line); color:var(--dim);
  font-size:16px; cursor:pointer; transition:all .14s; }
.sky-close:hover { background:rgba(255,255,255,.1); color:#eef1fa; }

.sky-drawer-body { flex:1; overflow-y:auto; padding:18px 20px 44px; }
.sky-drawer-body .sky-today { margin-bottom:20px; padding:16px 18px; }

/* 오늘 기준 요약 (오늘 진행 중 + 다가오는) */
.sky-sum-lbl { display:flex; align-items:center; gap:8px; font-size:13px; font-weight:700;
  color:#dce3f2; margin:13px 0 8px; }
.sky-sum-lbl.first { margin-top:2px; }
.sky-reshuffle { margin-left:auto; width:26px; height:26px; border-radius:8px;
  background:rgba(255,255,255,.05); border:1px solid var(--line); color:var(--accent);
  font-size:14px; line-height:1; cursor:pointer; transition:all .18s; }
.sky-reshuffle:hover { background:var(--as); border-color:rgba(255,184,77,.45); transform:rotate(90deg); }
.sky-sum-list { display:flex; flex-direction:column; gap:6px; }
.sky-sum-row { display:flex; align-items:center; gap:9px; padding:9px 11px;
  background:rgba(255,255,255,.04); border:1px solid var(--line); border-radius:10px;
  cursor:pointer; transition:border-color .14s, background .14s; }
.sky-sum-row:hover { border-color:rgba(255,184,77,.4); background:rgba(255,184,77,.07); }
.sky-sum-icon { font-size:16px; flex-shrink:0; }
.sky-sum-name { font-size:13.5px; font-weight:600; color:#eef1fa; flex:1; min-width:0;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sky-sum-date { font-family:var(--mono); font-size:11px; color:var(--accent); flex-shrink:0; }
.sky-sum-go { flex-shrink:0; font-size:11px; font-weight:700; color:#1a1206;
  background:var(--accent); border-radius:7px; padding:4px 8px; }
.sky-sum-none { font-size:12.5px; color:var(--dim); padding:7px 2px 2px; line-height:1.5; }

/* 월간 달력 그리드 */
.sky-cal { margin-bottom:22px; }
.sky-cal-nav { display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:12px; }
.sky-cal-arrow { width:32px; height:32px; border-radius:9px; background:rgba(255,255,255,.05);
  border:1px solid var(--line); color:#dce3f2; font-size:18px; line-height:1; cursor:pointer;
  transition:all .14s; }
.sky-cal-arrow:hover { background:var(--as); border-color:rgba(255,184,77,.4); color:var(--accent); }
.sky-cal-arrow:disabled { opacity:.3; cursor:default; }
.sky-cal-month { font-size:15px; font-weight:700; color:#eef1fa; min-width:118px; text-align:center; }
.sky-cal-weekdays { display:grid; grid-template-columns:repeat(7,1fr); gap:4px; margin-bottom:5px; }
.sky-cal-weekdays span { text-align:center; font-size:11.5px; font-weight:600; color:var(--dim); padding:2px 0; }
.sky-cal-weekdays span:first-child { color:#ff6b8a; }
.sky-cal-weekdays span:last-child { color:#7ec8ff; }
.sky-cal-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:4px; }
.sky-day { position:relative; aspect-ratio:1/1; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:3px;
  border-radius:9px; border:1px solid transparent; font-size:13.5px; color:#c8d2e8;
  transition:all .13s; }
.sky-day.blank { visibility:hidden; }
.sky-day.today { border-color:rgba(94,230,196,.5); color:#fff; }
.sky-day.has-ev { cursor:pointer; background:rgba(255,255,255,.035); }
.sky-day.has-ev:hover { background:rgba(255,184,77,.1); border-color:rgba(255,184,77,.35); }
.sky-day.sel { background:var(--as); border-color:var(--accent); color:#fff; font-weight:700; }
.sky-day-dots { display:flex; gap:2.5px; height:5px; align-items:center; }
.sky-day-dot { width:5px; height:5px; border-radius:50%; }
.sky-cal-legend { display:flex; flex-wrap:wrap; gap:8px 13px; margin-top:13px; padding-top:12px;
  border-top:1px solid var(--ls); }
.sky-leg { display:flex; align-items:center; gap:5px; font-size:11.5px; color:var(--dim); }
.sky-leg-dot { width:7px; height:7px; border-radius:50%; }

/* 이 달의 현상 리스트 (드로어) */
.sky-drawer-body .sky-sec-title { font-size:14.5px; font-weight:700; color:#dce3f2;
  margin:4px 0 12px; display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
.sky-clear-day { font-family:var(--mono); font-size:11px; color:var(--accent);
  background:var(--as); border:1px solid rgba(255,184,77,.35); border-radius:14px;
  padding:3px 10px; cursor:pointer; }
.sky-drawer-body .sky-list { gap:9px; }
.sky-ev { background:rgba(255,255,255,.03); border:1px solid var(--line); border-radius:12px;
  padding:13px 15px; }
.sky-ev-head { display:flex; align-items:center; gap:9px; flex-wrap:wrap; margin-bottom:7px; }
.sky-ev-icon { font-size:19px; }
.sky-ev-name { font-size:14.5px; font-weight:700; color:#eef1fa; }
.sky-ev-date { font-family:var(--mono); font-size:12px; color:var(--accent); margin-bottom:7px; }
.sky-ev-desc { font-size:13px; color:#b8c2d8; line-height:1.6; margin-bottom:7px; }
.sky-ev-tip { font-size:12px; color:var(--nova); background:rgba(94,230,196,.07);
  border-left:2px solid rgba(94,230,196,.4); border-radius:0 6px 6px 0; padding:7px 11px;
  line-height:1.55; margin-bottom:12px; }
.sky-ev-go { width:100%; background:var(--accent); color:#1a1206; border:none; border-radius:9px;
  padding:9px 14px; font-family:var(--sans); font-weight:700; font-size:13.5px; cursor:pointer;
  transition:transform .12s, opacity .15s; }
.sky-ev-go:hover { opacity:.9; transform:translateY(-1px); }
.sky-ev-go:active { transform:translateY(0); }
.sky-empty { color:var(--dim); font-size:13px; text-align:center; padding:22px 0; }

@media (max-width:520px) {
  .sky-fab-txt { display:none; }
  .sky-fab { padding:10px 12px; }
}

/* ══ 씬 플랜 패널 ══════════════════════════════════════════ */
.plan-block { margin-bottom:28px; animation:rise .3s ease; }
.user-bubble { font-size:14.5px; color:var(--nova); font-family:var(--sans);
  font-weight:600; margin:0 0 10px 2px; }

.plan-panel { background:rgba(12,16,28,.92); border:1px solid rgba(255,184,77,.22);
  border-radius:14px; padding:18px; margin-top:4px; }
.plan-header { display:flex; align-items:center; gap:8px; margin-bottom:14px;
  font-family:var(--mono); font-size:12px; color:var(--accent); letter-spacing:.05em; }
.plan-header-hint { color:var(--dim); font-size:11.5px; margin-left:2px; }
.plan-total-badge { margin-left:auto; background:var(--as); border:1px solid rgba(255,184,77,.3);
  border-radius:8px; padding:3px 10px; font-size:11px; color:var(--accent); white-space:nowrap; }
.plan-loading-state { color:var(--dim); font-family:var(--mono); font-size:13px;
  padding:18px 4px; display:flex; align-items:center; gap:9px; }
@keyframes spin { to { transform:rotate(360deg); } }
.plan-spin { display:inline-block; animation:spin 1s linear infinite; }

.scene-list { display:flex; flex-direction:column; gap:10px; margin-bottom:14px; }
.scene-card { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
  border-radius:10px; padding:14px 16px; transition:border-color .15s; }
.scene-card:hover { border-color:rgba(255,255,255,.15); }
.scene-card-header { display:flex; align-items:center; gap:10px; margin-bottom:5px; }
.scene-num { font-family:var(--mono); font-size:10px; color:var(--nova); letter-spacing:.1em;
  text-transform:uppercase; background:rgba(94,230,196,.1); border-radius:5px;
  padding:2px 7px; flex-shrink:0; }
.scene-name { font-weight:600; font-size:14px; color:#eef1fa; }
.scene-desc { font-size:12.5px; color:var(--dim); margin-bottom:12px; line-height:1.55; }
.scene-sliders { display:flex; flex-direction:column; gap:9px; }

.slider-row { display:flex; align-items:center; gap:10px; }
.slider-row label { font-family:var(--mono); font-size:11px; color:#8a94b0;
  width:100px; flex-shrink:0; }
.slider-row input[type=range] { flex:1; accent-color:var(--accent); cursor:pointer;
  height:3px; border-radius:2px; }
.slider-val { font-family:var(--mono); font-size:12px; color:var(--accent);
  width:72px; text-align:right; flex-shrink:0; }

.plan-gen-btn { width:100%; background:var(--accent); color:#1a1206; border:none;
  border-radius:11px; padding:13px 18px; font-family:var(--sans); font-weight:700;
  font-size:13.5px; cursor:pointer; transition:opacity .15s, transform .12s; letter-spacing:.01em; }
.plan-gen-btn:hover { opacity:.88; transform:translateY(-1px); }
.plan-gen-btn:active { transform:translateY(0); }
.plan-gen-btn:disabled { opacity:.45; cursor:default; transform:none; }
.plan-summary { font-family:var(--mono); font-size:11.5px; color:var(--nova);
  margin-bottom:10px; padding:6px 10px; background:rgba(94,230,196,.07);
  border-radius:7px; display:none; }
.plan-summary.visible { display:block; }
"""

CUSTOM_JS = r"""
() => {
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                              .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  const LS_KEY = 'sx_convs_v1';
  const PHRASES = [
    '당신의 우주를 그려보세요!',
    '오늘은 어떤 별에 닿아볼까요?',
    '말 한마디로 은하를 여행하세요',
    '상상하는 순간, 우주가 열립니다',
    '어디로 떠나볼까요, 우주 여행자님?',
    '한 문장이면 충분해요 — 우주는 준비됐어요',
    '오늘 밤, 어떤 하늘을 띄워볼까요?',
    '밤하늘이 당신의 문장을 기다립니다'
  ];
  let lastPhrase = -1;
  function freshWelcome() {
    let i;
    do { i = Math.floor(Math.random() * PHRASES.length); } while (i === lastPhrase);
    lastPhrase = i;
    $('welcomeTitle').textContent = PHRASES[i];
    const w = $('welcomeScreen');
    const bg = document.querySelector('.bg');
    w.classList.remove('fresh'); bg && bg.classList.remove('fresh');
    void w.offsetWidth;               // 리플로우 강제 → 애니메이션 재발동
    w.classList.add('fresh'); bg && bg.classList.add('fresh');
  }

  // ── 대화 저장소 (localStorage) ──────────────────────────
  let convs = [];
  try { convs = JSON.parse(localStorage.getItem(LS_KEY) || '[]'); } catch (e) { convs = []; }
  let currentId = null;
  const save = () => { try { localStorage.setItem(LS_KEY, JSON.stringify(convs)); } catch (e) {} };
  const cur = () => convs.find(c => c.id === currentId);

  // ── 스크롤: 채팅 컨테이너 내부만 (페이지 점프 방지) ──────
  function scrollBottom() {
    const sc = $('chatScroll');
    sc.scrollTop = sc.scrollHeight;
  }

  // ── .py 다운로드 ────────────────────────────────────────
  function downloadPy(code, name) {
    const safe = (name || 'sky_script').replace(/[\\/:*?"<>|\n\r]+/g, ' ').trim().slice(0, 40)
                 || 'sky_script';
    const blob = new Blob([code], {type: 'text/x-python'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = safe + '.py';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  // ── 메시지 블록 렌더 ────────────────────────────────────
  function addBlock(q, code, onEdit) {   // code=null 이면 '생성 중' 상태
    const block = document.createElement('div');
    block.className = 'msg-block';
    block.dataset.q = q;
    block.innerHTML =
      '<div class="msg-user">&gt; ' + esc(q) + '</div>' +
      '<div class="msg-result">' +
        '<div class="log-ticker">⟳ Groq 엔진이 스크립트를 생성하는 중...</div>' +
        '<div class="code-block" style="display:none">' +
          '<div class="code-tools">' +
            '<button class="tool-btn edit-btn">✎ 수정</button>' +
            '<button class="tool-btn copy-btn">복사</button>' +
            '<button class="tool-btn dl-btn">.py 저장</button>' +
          '</div>' +
          '<pre spellcheck="false"></pre>' +
        '</div>' +
      '</div>';
    $('chatView').appendChild(block);
    if (code !== null) fillBlock(block, code, onEdit);
    scrollBottom();
    return block;
  }
  // 수정 버튼 토글 — 기본은 읽기 전용(실수 방지), 누르면 편집 모드
  function wireEditToggle(btn, pre) {
    btn.onclick = () => {
      if (pre.isContentEditable) {
        pre.removeAttribute('contenteditable');
        btn.textContent = '✎ 수정'; btn.classList.remove('on');
      } else {
        pre.setAttribute('contenteditable', 'plaintext-only');
        if (!pre.isContentEditable) pre.setAttribute('contenteditable', 'true');  // 미지원 폴백
        btn.textContent = '완료 ✓'; btn.classList.add('on');
        pre.focus();
      }
    };
  }
  function fillBlock(block, code, onEdit) {
    const ticker = block.querySelector('.log-ticker');
    ticker.textContent = '✓ 생성 완료 — ✎ 수정 버튼으로 편집 · 복사 또는 .py 저장';
    ticker.classList.add('done');
    const cb = block.querySelector('.code-block');
    cb.style.display = '';
    const pre = cb.querySelector('pre');
    pre.textContent = code;
    pre.addEventListener('input', () => { if (onEdit) onEdit(pre.textContent); });
    wireEditToggle(cb.querySelector('.edit-btn'), pre);
    cb.querySelector('.copy-btn').onclick = () => {
      navigator.clipboard.writeText(pre.textContent);
      cb.querySelector('.copy-btn').textContent = '복사됨 ✓';
      setTimeout(() => { cb.querySelector('.copy-btn').textContent = '복사'; }, 1500);
    };
    cb.querySelector('.dl-btn').onclick = () => downloadPy(pre.textContent, block.dataset.q);
    appendLint(cb, code);
  }

  // ── 생성 코드 린트 (실측 함정 기반, 클라이언트 정적 검사) ────────
  function lintCode(code) {
    const w = [];
    if (/\b(DateManager|SceneGraph|DataManager|Configuration|Initialization)\b/.test(code)
        && !/from\s+Initialization\s+import/.test(code))
      w.push({t:'err', m:"매니저 클래스(DateManager 등)를 쓰면 'from Initialization import *' 가 필요해요."});
    if (/\.intensity\s*\(/.test(code))
      w.push({t:'err', m:"intensity 는 속성입니다 — '.intensity()' 가 아니라 '.intensity'(읽기) / setIntensity(...) 로."});
    if (/setTarget\s*\(\s*Vec3/.test(code))
      w.push({t:'warn', m:"카메라 타겟은 Vec2(방위, 고도)를 쓰세요 — Vec3 는 DEPRECATED."});
    (code.match(/setPosition(?:LBR|XYZ|R|L)\s*\([^;\n]*\)/g) || []).forEach(c => {
      if (/Anim/.test(c) && !/(,\s*-1\s*\)|portId|track)/.test(c))
        w.push({t:'warn', m:"카메라 이동 «"+c.slice(0,22)+"…» 에 track 인자가 빠진 듯 — (값, Anim, track), 지상이면 track=-1."});
    });
    if (/setDateTime\s*\(/.test(code))
      w.push({t:'info', m:"시각은 UTC 입니다 — 청주 정오=03:30 UTC (KST−9h). 낮/밤이 중요하면 변환을 꼭 확인!"});
    if (/\bBolide\s*\(/.test(code) && !/setModel\s*\(/.test(code))
      w.push({t:'warn', m:"Bolide(화구)는 setModel(ModelID.ColoredFireball, \"\") 가 없으면 안 그려져요."});
    if (/\bClock\s*\(/.test(code) && !/setModelset\s*\(/.test(code))
      w.push({t:'warn', m:"Clock(돔 시계)은 setModelset(Clock.Modelset.SystemClock001) 이 없으면 안 보여요."});
    if (/FadeTo/.test(code) && !/setShadowStrength\s*\(\s*0/.test(code))
      w.push({t:'info', m:"천체를 가까이 볼 땐 그림자 OFF(setShadowStrength(0)+setShadowContrast(0)+setPlanetShineStrength(1)) 권장 — 절반이 어두워지는 것 방지."});
    if (/InsertText\s*\(/.test(code) && /setDistance\s*\(\s*20/.test(code))
      w.push({t:'info', m:"자막 distance=20 은 행성/은하 프레임 전용 — 지상 씬이면 distance=1.0 로."});
    return w;
  }
  function appendLint(cbEl, code) {
    if (!cbEl || !code || code.trim().charAt(0) === '#') return;   // 에러 메시지면 스킵
    const ws = lintCode(code);
    const ICON = {err:'⛔', warn:'⚠️', info:'💡'};
    const box = document.createElement('div');
    box.className = 'lint-box';
    box.innerHTML = ws.length
      ? '<div class="lint-head">🔎 코드 검토 도움말 (' + ws.length + ')</div>' +
        ws.map(x => '<div class="lint-item lint-' + x.t + '">' + ICON[x.t] + ' ' + esc(x.m) + '</div>').join('')
      : '<div class="lint-ok">✓ 자주 나는 함정은 발견되지 않았어요</div>';
    cbEl.appendChild(box);
  }

  // ── 사이드바 대화 목록 ──────────────────────────────────
  function renderSidebar() {
    const list = $('convList');
    if (!convs.length) { list.innerHTML = '<div class="conv-empty">아직 대화가 없습니다</div>'; return; }
    list.innerHTML = '';
    convs.slice().reverse().forEach(c => {
      const item = document.createElement('div');
      item.className = 'conv-item' + (c.id === currentId ? ' active' : '');
      item.innerHTML = '<span class="conv-title">' + esc(c.title) + '</span>' +
                       '<button class="conv-edit" title="이름 수정">✎</button>' +
                       '<button class="conv-del" title="삭제">✕</button>';
      item.onclick = (e) => {
        if (e.target.classList.contains('conv-del') || e.target.classList.contains('conv-edit')) return;
        loadConv(c.id);
      };
      item.querySelector('.conv-edit').onclick = (e) => {
        e.stopPropagation();
        const name = window.prompt('대화 이름 수정', c.title);
        if (name && name.trim()) { c.title = name.trim().slice(0, 60); save(); renderSidebar(); }
      };
      item.querySelector('.conv-del').onclick = (e) => {
        e.stopPropagation();
        convs = convs.filter(x => x.id !== c.id);
        save();
        if (currentId === c.id) newChatView();
        renderSidebar();
      };
      list.appendChild(item);
    });
  }

  function showChat() {
    $('welcomeScreen').classList.add('out');
    $('chatScroll').classList.add('in');
    $('bottomBar').style.display = '';
  }
  function newChatView() {
    currentId = null;
    $('chatView').innerHTML = '';
    $('welcomeScreen').classList.remove('out');
    $('chatScroll').classList.remove('in');
    $('bottomBar').style.display = 'none';
    freshWelcome();                    // 새 문구 + 페이드 재발동
    renderSidebar();
  }
  function loadConv(id) {
    const c = convs.find(x => x.id === id);
    if (!c) return;
    currentId = id;
    $('chatView').innerHTML = '';
    c.msgs.forEach(m => addBlock(m.q, m.code, (v) => { m.code = v; save(); }));
    showChat();
    renderSidebar();
    scrollBottom();
  }

  // ── 탭 전환 (생성기 ↔ 변환기) ───────────────────────────
  let tab = 'chat';
  function switchTab(t) {
    tab = t;
    $('tabChat').classList.toggle('active', t === 'chat');
    $('tabConv').classList.toggle('active', t === 'conv');
    if (t === 'conv') {
      $('welcomeScreen').classList.add('out');
      $('welcomeScreen').style.display = 'none'; // 페이드 잔상 없이 즉시 숨김
      $('chatScroll').classList.remove('in');
      $('chatScroll').style.display = 'none';
      $('bottomBar').style.display = 'none';
      $('convView').style.display = '';
    } else {
      $('convView').style.display = 'none';
      $('chatScroll').style.display = '';
      $('welcomeScreen').style.display = '';
      if (currentId) { $('chatScroll').classList.add('in'); $('bottomBar').style.display = ''; }
      else { $('welcomeScreen').classList.remove('out'); freshWelcome(); }
    }
  }

  // ── 천문 달력 (📅 우측 드로어) ─────────────────────────────
  let skyData = null;
  let skyViewMonth = 7;      // 보고 있는 달(1~12). 로드 시 오늘 달로 재설정
  let skySelDay = null;      // 선택된 날짜 'YYYY-MM-DD' (없으면 그 달 전체)
  const _MON = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'];

  // 관측지(도시) — 기본 청주. localStorage 에 저장, 생성 프롬프트에도 반영.
  const CITIES = { '청주':[36.64,127.49], '서울':[37.57,126.98], '인천':[37.46,126.71],
    '대전':[36.35,127.38], '대구':[35.87,128.60], '광주':[35.16,126.85], '부산':[35.18,129.08],
    '울산':[35.54,129.31], '강릉':[37.75,128.90], '제주':[33.50,126.53] };
  let observer = (() => {
    try { const s = JSON.parse(localStorage.getItem('sky_observer'));
      if (s && s.city && CITIES[s.city]) return s; } catch (e) {}
    return { city:'청주', lat:36.64, lon:127.49 };
  })();
  function setObserver(city) {
    const c = CITIES[city] || CITIES['청주'];
    observer = { city: city, lat: c[0], lon: c[1] };
    try { localStorage.setItem('sky_observer', JSON.stringify(observer)); } catch (e) {}
    skyData = null;               // 관측지 바뀌면 다시 불러오기
    loadSkyEvents();
  }
  function observerPrefix() {     // 청주가 아니면 생성 프롬프트에 관측지 지시
    if (observer.city === '청주') return '';
    return '관측지는 ' + observer.city + '(위도 ' + observer.lat + ', 경도 ' + observer.lon + ')로 설정해줘. ';
  }
  // 생성 옵션(관측지 + 길이 프리셋 + 해설 주석) → API 프롬프트 접두
  let teachMode = false, lengthPreset = '';
  try {
    teachMode = localStorage.getItem('gen_teach') === '1';
    lengthPreset = localStorage.getItem('gen_len') || '';
  } catch (e) {}
  function genPrefix() {
    let p = observerPrefix();
    if (lengthPreset) p += lengthPreset;
    if (teachMode) p += '각 코드 줄에 초보자가 이해할 수 있는 한국어 주석을 자세히 달아줘. ';
    return p;
  }

  async function loadSkyEvents() {
    if (skyData) { renderSky(); return; }      // 캐시 있으면 재사용
    try {
      const raw = await callApi('sky_events', [JSON.stringify(observer)]);
      skyData = JSON.parse(raw);
      if (skyData.today) {
        const mm = parseInt(skyData.today.split('-')[1], 10);
        if (mm >= 1 && mm <= 12) skyViewMonth = mm;
      }
      renderSky();
    } catch (e) {
      $('skyToday').innerHTML =
        '<div class="sky-loading">천문 데이터를 불러오지 못했습니다: ' + esc(String(e)) + '</div>';
    }
  }

  function openSkyDrawer() {
    $('skyBackdrop').classList.add('open');
    $('skyDrawer').classList.add('open');
    $('skyDrawer').setAttribute('aria-hidden', 'false');
    loadSkyEvents();
  }
  function closeSkyDrawer() {
    $('skyBackdrop').classList.remove('open');
    $('skyDrawer').classList.remove('open');
    $('skyDrawer').setAttribute('aria-hidden', 'true');
  }

  // 이벤트 → 곧장 스크립트 생성(플랜 패널 경유). 초기화면으로 튕기지 않음
  function skyGo(prompt) {
    closeSkyDrawer();
    switchTab('chat');
    run(prompt);
  }
  window.__skyGo = skyGo;                       // inline onclick 에서 접근

  // 특정 날짜(ISO)에 걸리는 이벤트 (장기 시즌 제외 = 달력 점 표시용)
  function eventsOnDay(iso) {
    if (!skyData || !skyData.all) return [];
    return skyData.all.filter(e => !e.isLong && e._sd <= iso && iso <= e._ed);
  }
  // 특정 달에 걸치는 이벤트 (장기 시즌 포함 = 리스트용) — 달을 넘겨도 다 보임
  function eventsInMonth(month) {
    if (!skyData || !skyData.all) return [];
    const mm = String(month).padStart(2, '0');
    const first = '2026-' + mm + '-01', last = '2026-' + mm + '-31';
    return skyData.all.filter(e => e._sd <= last && e._ed >= first);
  }

  // 관측지 드롭다운 채우기 + 좌표 표시 + 변경 이벤트
  function fillLocSelect() {
    const sel = $('skyLoc');
    if (!sel) return;
    sel.innerHTML = Object.keys(CITIES).map(c =>
      '<option value="' + c + '"' + (c === observer.city ? ' selected' : '') + '>' + c + '</option>').join('');
    sel.onchange = () => setObserver(sel.value);
    const cc = $('skyLocCoord');
    if (cc) cc.textContent = observer.lat.toFixed(2) + '°N, ' + observer.lon.toFixed(2) + '°E';
  }

  function renderSky() {
    const d = skyData;
    if (!d || d.error) {
      $('skyToday').innerHTML = '<div class="sky-loading">데이터 오류</div>';
      return;
    }
    fillLocSelect();
    // ① 오늘 카드(날짜·달·태양) + '오늘 볼 수 있는 현상' (열 때마다 무작위)
    const m = d.moon, s = d.sun || {};
    const sunLine = (s.rise || s.set)
      ? '<div class="sky-sun">🌅 일출 <b>' + (s.rise || '—') + '</b>' +
        ' · ☀️ 남중 <b>' + (s.transit || '—') + '</b>' +
        ' · 🌇 일몰 <b>' + (s.set || '—') + '</b></div>'
      : '';
    $('skyToday').innerHTML =
      '<div class="sky-today-top">' +
        '<span class="sky-date-badge">오늘 · ' + esc(d.todayLabel) + '</span>' +
        '<span class="sky-moon">' + m.icon + ' <b>' + esc(m.name) + '</b> ' + m.pct + '%</span>' +
      '</div>' + sunLine +
      '<div class="sky-sum-lbl first">🔭 오늘 볼 수 있는 현상' +
        '<button class="sky-reshuffle" id="skyReshuffle" title="다른 현상 보기">↻</button></div>' +
      '<div class="sky-sum-list" id="skyTodayList"></div>';
    renderTodayVisible();
    const rb = $('skyReshuffle');
    if (rb) rb.onclick = renderTodayVisible;

    renderCalendar();
    renderMonthList();
  }

  // '오늘 볼 수 있는 현상' — 실시간 행성/달 + 오늘 진행 이벤트 + 계절 풀 무작위 3개
  function renderTodayVisible() {
    const d = skyData;
    if (!d) return;
    const todayIso = d.today;
    const real = d.always || [];                                   // 실시간 행성 + 달
    const ongoing = (d.all || []).filter(e => !e.isLong && e._sd <= todayIso && todayIso <= e._ed);
    const pool = (d.seasonPool || []).slice();
    for (let i = pool.length - 1; i > 0; i--) {                    // Fisher–Yates 셔플
      const j = (Math.random() * (i + 1)) | 0;
      const t = pool[i]; pool[i] = pool[j]; pool[j] = t;
    }
    const list = real.concat(ongoing).concat(pool.slice(0, 3));
    const sumRow = (e) =>
      '<div class="sky-sum-row" onclick="__skyGo(' + JSON.stringify(e.prompt).replace(/"/g,'&quot;') + ')">' +
        '<span class="sky-sum-icon">' + e.icon + '</span>' +
        '<span class="sky-sum-name">' + esc(e.name) + '</span>' +
        '<span class="sky-sum-date">' + esc(e.dateLabel) + '</span>' +
        '<span class="sky-sum-go">✨</span>' +
      '</div>';
    $('skyTodayList').innerHTML = list.length
      ? list.map(sumRow).join('')
      : '<div class="sky-sum-none">천문 데이터를 불러오는 중…</div>';
  }

  // ② 월간 달력 그리드
  function renderCalendar() {
    const d = skyData;
    $('skyMonthLabel').textContent = '2026년 ' + _MON[skyViewMonth - 1];
    $('skyPrev').disabled = (skyViewMonth <= 1);
    $('skyNext').disabled = (skyViewMonth >= 12);
    const mm = String(skyViewMonth).padStart(2, '0');
    const daysInMonth = new Date(2026, skyViewMonth, 0).getDate();
    const firstDow = new Date(2026, skyViewMonth - 1, 1).getDay();   // 0=일요일

    let cells = '';
    for (let i = 0; i < firstDow; i++) cells += '<div class="sky-day blank"></div>';
    for (let day = 1; day <= daysInMonth; day++) {
      const iso = '2026-' + mm + '-' + String(day).padStart(2, '0');
      const evs = eventsOnDay(iso);
      let cls = 'sky-day';
      if (evs.length) cls += ' has-ev';
      if (d.today === iso) cls += ' today';
      if (skySelDay === iso) cls += ' sel';
      let dots = '';
      if (evs.length) {
        const seen = {};
        evs.forEach(e => { seen[e.type] = e.color; });
        dots = Object.values(seen).slice(0, 3).map(c =>
          '<span class="sky-day-dot" style="background:' + c + '"></span>').join('');
      }
      const attr = evs.length ? ' data-day="' + iso + '"' : '';
      cells += '<div class="' + cls + '"' + attr + '><span>' + day + '</span>' +
               '<div class="sky-day-dots">' + dots + '</div></div>';
    }
    $('skyCalGrid').innerHTML = cells;
    $('skyCalGrid').querySelectorAll('.sky-day.has-ev').forEach(el => {
      el.onclick = () => {
        const iso = el.dataset.day;
        skySelDay = (skySelDay === iso) ? null : iso;   // 같은 날 다시 클릭 = 해제
        renderCalendar();
        renderMonthList();
      };
    });

    // 범례 — 이 달에 등장하는 유형만
    const typesInMonth = {};
    eventsInMonth(skyViewMonth).forEach(e => { if (!e.isLong) typesInMonth[e.type] = e; });
    $('skyLegend').innerHTML = Object.values(typesInMonth).map(e =>
      '<span class="sky-leg"><span class="sky-leg-dot" style="background:' + e.color + '"></span>' +
      esc(e.typeLabel) + '</span>').join('');
  }

  // ③ 이 달(또는 선택한 날)의 천문현상 리스트
  function renderMonthList() {
    let list, title;
    if (skySelDay) {
      list = eventsInMonth(skyViewMonth).filter(e => e._sd <= skySelDay && skySelDay <= e._ed);
      const dd = parseInt(skySelDay.split('-')[2], 10);
      title = '🗓 ' + skyViewMonth + '월 ' + dd + '일' +
        '<span class="sky-clear-day" id="skyClearDay">✕ 이 달 전체 보기</span>';
    } else {
      list = eventsInMonth(skyViewMonth);
      title = '🗓 ' + skyViewMonth + '월의 천문현상 ' +
        '<span style="color:var(--dim);font-weight:400">(' + list.length + ')</span>';
    }
    $('skyMonthTitle').innerHTML = title;
    if (skySelDay) {
      const b = $('skyClearDay');
      if (b) b.onclick = () => { skySelDay = null; renderCalendar(); renderMonthList(); };
    }
    if (!list.length) {
      $('skyMonthList').innerHTML =
        '<div class="sky-empty">이 ' + (skySelDay ? '날' : '달') + '에는 등록된 천문현상이 없습니다.</div>';
      return;
    }
    $('skyMonthList').innerHTML = list.map(e =>
      '<div class="sky-ev">' +
        '<div class="sky-ev-head">' +
          '<span class="sky-ev-icon">' + e.icon + '</span>' +
          '<span class="sky-ev-name">' + esc(e.name) + '</span>' +
          '<span class="sky-card-tag" style="background:' + e.color + '22;color:' + e.color + '">' +
            esc(e.typeLabel) + '</span>' +
        '</div>' +
        '<div class="sky-ev-date">📅 ' + esc(e.dateLabel) + '</div>' +
        '<div class="sky-ev-desc">' + esc(e.desc) + '</div>' +
        '<div class="sky-ev-tip">👀 ' + esc(e.tip) + '</div>' +
        '<button class="sky-ev-go" onclick="__skyGo(' +
          JSON.stringify(e.prompt).replace(/"/g,'&quot;') + ')">✨ 스크립트 만들기</button>' +
      '</div>').join('');
  }

  // ── Gradio REST 호출 (공용) — HTTP 에러/네트워크 실패 방어 ──
  async function callApi(name, data) {
    try {
      const r = await fetch('gradio_api/call/' + name, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: data})
      });
      if (!r.ok) return '# 오류: 서버 응답 ' + r.status + ' — Space 로그를 확인해 주세요';
      const j = await r.json();
      const res = await fetch('gradio_api/call/' + name + '/' + j.event_id);
      if (!res.ok) return '# 오류: 서버 응답 ' + res.status;
      const t = await res.text();
      const lines = t.split('\n').filter(l => l.startsWith('data:'));
      if (!lines.length) return '# 오류: 서버 응답 파싱 실패';
      const parsed = JSON.parse(lines[lines.length - 1].slice(5));
      if (!parsed || typeof parsed[0] !== 'string')
        return '# 오류: 서버 처리 실패 (Space 로그를 확인해 주세요)';
      return parsed[0];
    } catch (e) { return '# 오류: ' + e + ' (네트워크/서버 상태를 확인해 주세요)'; }
  }

  // ── SPC 변환기 ──────────────────────────────────────────
  async function runConvert() {
    const txt = $('spcInput').value;
    if (!txt.trim() || busy) return;
    busy = true;
    $('convBtn').disabled = true;
    $('convResult').style.display = '';
    $('convTicker').textContent = '⟳ 변환 중...';
    $('convTicker').classList.remove('done');
    try {
      const code = await callApi('convert', [txt, $('timedChk').checked]);
      $('convTicker').textContent = code.startsWith('# 오류')
        ? '✗ 변환 실패' : '✓ 변환 완료 — ✎ 수정 버튼으로 편집 · 복사 또는 .py 저장';
      $('convTicker').classList.add('done');
      $('convPre').textContent = code;
    } finally {
      busy = false;
      $('convBtn').disabled = false;
    }
  }

  // ── 씬 플랜 헬퍼 ──────────────────────────────────────────
  function buildSceneCard(scene, planData) {
    const card = document.createElement('div');
    card.className = 'scene-card';
    const cam = scene.camera || {};

    card.innerHTML =
      '<div class="scene-card-header">' +
        '<span class="scene-num">씬 ' + scene.id + '</span>' +
        '<span class="scene-name">' + esc(scene.name) + '</span>' +
      '</div>' +
      '<div class="scene-desc">' + esc(scene.description) + '</div>' +
      '<div class="scene-sliders"></div>';

    const slidersDiv = card.querySelector('.scene-sliders');

    function addSlider(label, min, max, step, initVal, fmt, onUpdate) {
      const row = document.createElement('div');
      row.className = 'slider-row';
      const uid = 'sv-' + scene.id + '-' + label.replace(/\s/g,'');
      row.innerHTML =
        '<label>' + label + '</label>' +
        '<input type="range" min="' + min + '" max="' + max + '" step="' + step + '" value="' + initVal + '">' +
        '<span class="slider-val" id="' + uid + '">' + fmt(initVal) + '</span>';
      const inp = row.querySelector('input');
      inp.oninput = () => {
        const v = parseFloat(inp.value);
        document.getElementById(uid).textContent = fmt(v);
        onUpdate(v);
        // 총 시간 배지 갱신
        const total = planData.scenes.reduce((s, x) => s + (x.duration || 0), 0);
        const badge = document.getElementById('planTotalBadge');
        if (badge) badge.textContent = '총 ' + total.toFixed(1) + '초';
      };
      slidersDiv.appendChild(row);
    }

    addSlider('⏱ 소요시간', 0.5, 30, 0.5, scene.duration,
      v => v + '초', v => { scene.duration = v; });

    if (cam.target_height !== undefined)
      addSlider('🎯 돔 높이', 0, 90, 1, cam.target_height,
        v => v + '°', v => { cam.target_height = v; });

    if (cam.scale !== undefined)
      addSlider('🔭 줌 배율', 0.1, 3.0, 0.1, cam.scale,
        v => 'R×' + parseFloat(v).toFixed(2), v => { cam.scale = v; });

    if (cam.degrees !== undefined)
      addSlider('🔄 공전 각도', 30, 720, 30, cam.degrees,
        v => v + '°', v => { cam.degrees = v; });

    if (cam.distance_pc !== undefined)
      addSlider('🚀 거리(pc)', 1, 1000, 1, cam.distance_pc,
        v => v + ' pc', v => { cam.distance_pc = v; });

    return card;
  }

  function buildPlanPanel(planData, onGenerate) {
    const total = planData.scenes.reduce((s, x) => s + (x.duration || 0), 0);
    const panel = document.createElement('div');
    panel.className = 'plan-panel';
    panel.innerHTML =
      '<div class="plan-header">' +
        '<span>📋 씬 플랜</span>' +
        '<span class="plan-header-hint">슬라이더로 타이밍과 카메라 값을 조정하세요</span>' +
        '<span class="plan-total-badge" id="planTotalBadge">총 ' + total.toFixed(1) + '초</span>' +
      '</div>' +
      '<div class="plan-summary" id="planSummary"></div>' +
      '<div class="scene-list" id="sceneListEl"></div>' +
      '<button class="plan-gen-btn" id="planGenBtn">✨ 이 설정으로 스크립트 생성</button>';

    const list = panel.querySelector('#sceneListEl');
    planData.scenes.forEach(scene => list.appendChild(buildSceneCard(scene, planData)));
    panel.querySelector('#planGenBtn').onclick = onGenerate;
    return panel;
  }

  // ── 실행 ────────────────────────────────────────────────
  let busy = false;
  let planBusy = false;

  async function run(prompt) {
    prompt = (prompt || '').trim();
    if (!prompt || busy) return;
    busy = true;
    const apiPrompt = genPrefix() + prompt;   // 관측지·길이·해설 지시를 API 프롬프트에만 반영

    if (!currentId) {
      currentId = Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
      convs.push({ id: currentId, title: prompt.slice(0, 40), msgs: [] });
    }
    showChat();
    renderSidebar();

    // ① 플랜 로딩 블록
    const planBlock = document.createElement('div');
    planBlock.className = 'plan-block';
    planBlock.innerHTML =
      '<div class="user-bubble">&gt; ' + esc(prompt) + '</div>' +
      '<div class="plan-loading-state"><span class="plan-spin">⟳</span> 씬 플랜 분석 중...</div>';
    $('chatView').appendChild(planBlock);
    document.querySelectorAll('button.run').forEach(b => b.disabled = true);
    scrollBottom();

    try {
      const planJson = await callApi('plan', [apiPrompt]);
      planBlock.querySelector('.plan-loading-state')?.remove();

      let planData = null;
      try { planData = JSON.parse(planJson); } catch(e) {}

      if (planData && planData.scenes && planData.scenes.length) {
        // ② 플랜 패널 표시
        const panel = buildPlanPanel(planData, async () => {
          if (planBusy) return;
          planBusy = true;
          const genBtn = panel.querySelector('#planGenBtn');
          if (genBtn) { genBtn.disabled = true; genBtn.textContent = '⟳ 스크립트 생성 중...'; }

          // 씬 목록 접기
          const sceneListEl = panel.querySelector('#sceneListEl');
          if (sceneListEl) sceneListEl.style.display = 'none';

          // 로딩 표시
          const loadDiv = document.createElement('div');
          loadDiv.className = 'plan-loading-state';
          loadDiv.innerHTML = '<span class="plan-spin">⟳</span> 스크립트 생성 중...';
          panel.appendChild(loadDiv);

          try {
            const c0 = cur();
            const history = JSON.stringify((c0 ? c0.msgs : []).map(m => ({ q: m.q, code: m.code })));
            const scenesJson = JSON.stringify(planData);
            const code = await callApi('generate', [apiPrompt, history, scenesJson]);

            loadDiv.remove();
            if (genBtn) genBtn.style.display = 'none';

            // ③ 요약 표시
            const total = planData.scenes.reduce((s, x) => s + (x.duration || 0), 0);
            const summary = panel.querySelector('#planSummary');
            if (summary) {
              summary.textContent = '✓ ' + planData.scenes.length + '개 씬 · 총 ' + total.toFixed(1) + '초';
              summary.classList.add('visible');
            }

            // ④ 코드 블록 추가 (기존 addBlock/fillBlock 로직 인라인)
            const codeWrap = document.createElement('div');
            codeWrap.className = 'msg-result';
            codeWrap.style.marginTop = '12px';
            codeWrap.innerHTML =
              '<div class="log-ticker done">✓ 생성 완료 — ✎ 수정 버튼으로 편집 · 복사 또는 .py 저장</div>' +
              '<div class="code-block">' +
                '<div class="code-tools">' +
                  '<button class="tool-btn edit-btn">✎ 수정</button>' +
                  '<button class="tool-btn copy-btn">복사</button>' +
                  '<button class="tool-btn dl-btn">.py 저장</button>' +
                '</div>' +
                '<pre spellcheck="false"></pre>' +
              '</div>';
            planBlock.appendChild(codeWrap);

            const pre = codeWrap.querySelector('pre');
            pre.textContent = code;
            wireEditToggle(codeWrap.querySelector('.edit-btn'), pre);
            codeWrap.querySelector('.copy-btn').onclick = () => {
              navigator.clipboard.writeText(pre.textContent).catch(() => {});
              codeWrap.querySelector('.copy-btn').textContent = '복사됨 ✓';
              setTimeout(() => { codeWrap.querySelector('.copy-btn').textContent = '복사'; }, 1500);
            };
            codeWrap.querySelector('.dl-btn').onclick = () => downloadPy(pre.textContent, prompt);
            appendLint(codeWrap.querySelector('.code-block'), code);

            // ⑤ 대화 기록 저장
            const m = { q: prompt, code: code };
            const c = cur();
            if (c) { c.msgs.push(m); save(); }
            scrollBottom();
          } catch(e) {
            loadDiv.textContent = '# 오류: ' + e;
          } finally {
            planBusy = false;
          }
        });
        planBlock.appendChild(panel);
        scrollBottom();
      } else {
        // 플랜 실패 → 기존 방식으로 바로 코드 생성
        const fallbackBlock = addBlock(prompt, null);
        const c0 = cur();
        const history = JSON.stringify((c0 ? c0.msgs : []).map(m => ({ q: m.q, code: m.code })));
        const code = await callApi('generate', [apiPrompt, history, '']);
        const m = { q: prompt, code: code };
        const c = cur();
        if (c) { c.msgs.push(m); save(); }
        fillBlock(fallbackBlock, code, (v) => { m.code = v; save(); });
        scrollBottom();
      }
    } finally {
      busy = false;
      document.querySelectorAll('button.run').forEach(b => b.disabled = false);
    }
  }

  function wireInput(taId, btnId) {
    const ta = $(taId), btn = $(btnId);
    btn.onclick = (e) => { e.preventDefault(); run(ta.value); ta.value = ''; };
    ta.addEventListener('keydown', (e) => {
      if (e.isComposing || e.keyCode === 229) return;   // 한글 IME 조합 중 Enter 무시
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); run(ta.value); ta.value = ''; }
    });
  }

  const boot = setInterval(() => {
    if (!$('runBtn')) return;
    clearInterval(boot);
    wireInput('promptInput', 'runBtn');
    wireInput('bottomInput', 'bottomBtn');
    document.querySelectorAll('.chip').forEach(c => {
      c.onclick = () => run(c.getAttribute('data-p'));
    });
    // 생성 옵션: 해설 주석 토글 + 길이 프리셋 (localStorage 유지)
    const tchk = $('teachChk');
    if (tchk) {
      tchk.checked = teachMode;
      tchk.onchange = () => { teachMode = tchk.checked;
        try { localStorage.setItem('gen_teach', teachMode ? '1' : '0'); } catch (e) {} };
    }
    document.querySelectorAll('.opt-len').forEach(b => {
      b.classList.toggle('on', (b.dataset.len || '') === lengthPreset);
      b.onclick = () => {
        lengthPreset = b.dataset.len || '';
        try { localStorage.setItem('gen_len', lengthPreset); } catch (e) {}
        document.querySelectorAll('.opt-len').forEach(x => x.classList.toggle('on', x === b));
      };
    });
    $('newChatBtn').onclick = () => { switchTab('chat'); newChatView(); };
    $('clearAllBtn').onclick = () => {
      if (!convs.length) return;
      if (window.confirm('대화 기록을 전체 삭제할까요? (되돌릴 수 없음)')) {
        convs = []; save(); switchTab('chat'); newChatView();
      }
    };
    $('tabChat').onclick = () => switchTab('chat');
    $('tabConv').onclick = () => switchTab('conv');
    $('skyFab').onclick  = () => openSkyDrawer();
    $('skyClose').onclick = () => closeSkyDrawer();
    $('skyBackdrop').onclick = () => closeSkyDrawer();
    $('skyPrev').onclick = () => {
      if (skyViewMonth > 1) { skyViewMonth--; skySelDay = null; renderCalendar(); renderMonthList(); }
    };
    $('skyNext').onclick = () => {
      if (skyViewMonth < 12) { skyViewMonth++; skySelDay = null; renderCalendar(); renderMonthList(); }
    };
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && $('skyDrawer').classList.contains('open')) closeSkyDrawer();
    });
    $('convBtn').onclick = () => runConvert();
    $('convCopy').onclick = () => {
      navigator.clipboard.writeText($('convPre').textContent);
      $('convCopy').textContent = '복사됨 ✓';
      setTimeout(() => { $('convCopy').textContent = '복사'; }, 1500);
    };
    $('convDl').onclick = () => downloadPy($('convPre').textContent, 'spc_converted');
    wireEditToggle($('convEdit'), $('convPre'));
    $('spcFile').addEventListener('change', (e) => {
      const f = e.target.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = () => { $('spcInput').value = reader.result; };
      reader.readAsText(f);
      e.target.value = '';               // 같은 파일 재선택도 change 발동되게 리셋
    });
    freshWelcome();                    // 최초 진입도 랜덤 문구 + 페이드
    renderSidebar();
  }, 100);
}
"""

with gr.Blocks(title="Sky Explorer AI", css=CUSTOM_CSS, js=CUSTOM_JS) as demo:
    gr.HTML(CUSTOM_HTML)
    with gr.Row(elem_id="hidden-io"):
        _in = gr.Textbox()
        _hist = gr.Textbox()
        _scenes = gr.Textbox()   # 씬 플랜 JSON (generate 3번째 입력)
        _out = gr.Textbox()
        _btn = gr.Button()
        _cin = gr.Textbox()
        _ctimed = gr.Checkbox()
        _cout = gr.Textbox()
        _cbtn = gr.Button()
        _pin = gr.Textbox()      # plan 입력
        _pout = gr.Textbox()     # plan 출력
        _pbtn = gr.Button()
        _sin = gr.Textbox()      # sky_events 입력(month, 미사용 시 "")
        _sout = gr.Textbox()     # sky_events 출력
        _sbtn = gr.Button()
    _btn.click(generate, inputs=[_in, _hist, _scenes], outputs=_out, api_name="generate")
    _cbtn.click(convert_spc, inputs=[_cin, _ctimed], outputs=_cout, api_name="convert")
    _pbtn.click(plan, inputs=[_pin], outputs=_pout, api_name="plan")
    _sbtn.click(sky_events, inputs=[_sin], outputs=_sout, api_name="sky_events")

# 남용/폭주 방지: 동시 실행·대기열 상한(공개 엔드포인트 쿼터 고갈 방어)
demo.queue(default_concurrency_limit=QUEUE_CONCURRENCY, max_size=QUEUE_MAX_SIZE)

if __name__ == "__main__":
    demo.launch()

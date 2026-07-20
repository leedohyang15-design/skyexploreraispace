# -*- coding: utf-8 -*-
"""
chart2d.py — Chart2D v3: 카테고리 수 고정 문제 수정 (2026-07-20)
★ 렌더는 확정(파이·막대 둘 다 화면에 뜸). 남은 문제 2개를 v3 에서 해결:
  ① (v2 로 해결) 값은 0~1 범위 — 1 넘으면 clamp. → 전부 정규화.
  ② (v3) **막대가 8개를 넣어도 첫 3개만 뜸** — 원인 추정: '처음 표시(intensity>0)할 때 카테고리 수가 고정'.
     v1/v2 는 씬1 파이를 3개로 먼저 띄운 뒤 같은 차트에 8개를 넣어 → 3슬롯만 그려짐(+그 3개로 auto-scale).
  ③ (v5 진짜 원인) **막대가 3개만 뜬 진짜 이유 = `setCategoryCount` 기본값이 3** (하드캡 아님!).
     완본 확인: setCategoryNValue 설명에 "If category count is lesser than N, it has no effect" → **`setCategoryCount(8)` 먼저 호출**해야 4~8번이 먹힘.
     → v5 수정: make_chart 에서 `setCategoryCount(N)` 을 카테고리 세팅 전에 호출.
★★ v4 진짜 문제 수정 (사용자 정정): "항목이 안 뜬다" = 막대 개수가 아니라 **차트 텍스트가 전부 □□ 네모(두부)**.
   원인: **Chart2D 텍스트 렌더러에 한글 폰트 없음** → 한글=네모, 숫자/영문만 정상(범례 '□□□□ 5%'에서 5%만 나온 게 증거).
   Chart2D 엔 폰트 세터 없음 → **카테고리 라벨을 전부 영문/숫자로**. (InsertText 자막은 한글 폰트 있어 그대로 한글 OK.)
★ Chart2D API: setChartType(Histogram/Pie) · setCategoryN{Color/Text/Value} (N=1~10) · setPosition/setSize/setDistance/setIntensity · addChild(FixedForeground).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def make_chart(slot, chart_type, pos, size, ncat):
    """Chart2D 객체 생성 + HUD 부착 + 타입/위치/크기 + ★카테고리 개수. intensity 0 으로 시작."""
    c = None
    try:
        c = Chart2D(Chart2D.Chart2DName(slot)); print("   Chart2D(%d) 생성" % slot)
    except Exception as e:
        print("   Chart2D(%d) 실패: %s" % (slot, e)); return None
    try:
        cam.addChild(c.id, Camera.CameraPort.FixedForeground); print("   ✓ addChild(FixedForeground)")
    except Exception as e:
        print("   ✗ addChild 실패: %s" % e); feat(c, "setParent", cam.id)
    if chart_type is not None:
        feat(c, "setChartType", chart_type, label="(타입)")
    feat(c, "setCategoryCount", int(ncat), label="(★ 카테고리 개수=%d — 이걸 늘려야 N개 다 뜸)" % ncat)
    feat(c, "setPosition", pos, Anim(0.0))
    feat(c, "setDistance", 1.0, Anim(0.0))
    feat(c, "setSize", size, Anim(0.0), label="(size %.2f)" % size)
    feat(c, "setIntensity", 0.0, Anim(0.0))
    return c


def set_cat(chart, i, text, value, color):
    """카테고리 i(1~10): 이름/값(0~1)/색. ★ 표시 전에 호출할 것(카운트 고정 회피)."""
    v = float(value)
    feat(chart, "setCategory%dText" % i, text)
    feat(chart, "setCategory%dValue" % i, v, Anim(0.0))
    feat(chart, "setCategory%dColor" % i, color, Anim(0.0))
    print("     · cat%d '%s' value=%.3f" % (i, text, v))


# ── 무대: 밤하늘 배경 ───────────────────────────────────────
print("무대: Chart2D v3 — 카테고리 수 고정 수정")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
feat(earth, "setElevationScale", 0.0)
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.35, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ══════ 씬1: 막대(Histogram) — 행성 지름 8개 (★ 표시 전에 8개 다 세팅) ══════
narr("행성들의 크기 비교 — 지름(목성=1로 정규화)", 4.0)
histo = make_chart(0, Chart2D.ChartType.Histogram if hasattr(Chart2D.ChartType, "Histogram") else None,
                   Vec(0, 45, 0), 0.75, ncat=8)
if histo is not None:
    # ★ 라벨은 영문(한글은 Chart2D 폰트에서 □□ 로 깨짐)
    planets_raw = [
        ("Mercury", 0.38, Vec(0.7, 0.7, 0.7)), ("Venus", 0.95, Vec(0.9, 0.8, 0.5)),
        ("Earth", 1.00, Vec(0.3, 0.6, 1.0)), ("Mars", 0.53, Vec(0.9, 0.4, 0.3)),
        ("Jupiter", 11.2, Vec(0.9, 0.7, 0.5)), ("Saturn", 9.45, Vec(0.9, 0.85, 0.6)),
        ("Uranus", 4.01, Vec(0.5, 0.8, 0.9)), ("Neptune", 3.88, Vec(0.3, 0.5, 0.95)),
    ]
    mx = max(v for _, v, _ in planets_raw)              # 11.2
    for i, (nm, val, col) in enumerate(planets_raw, start=1):
        set_cat(histo, i, nm, val / mx, col)           # ★ 표시(페이드인) 전에 8개 다 세팅
    feat(histo, "setIntensity", 1.0, Anim(2.0)); sleep(2.3)   # 이제 페이드인 → 8개 다 떠야 함

narr("목성·토성이 압도 — 암석 행성(수성~화성)은 아주 작은 막대", 5.0)
narr("이번엔 8개 막대가 다 보이나?", 4.0)

# 막대 차트 숨김
if histo is not None:
    feat(histo, "setIntensity", 0.0, Anim(1.5)); sleep(1.7)

# ══════ 씬2: 파이(Pie) — 우주의 구성 (다른 Chart2D 객체) ══════
narr("이번엔 파이차트 — 우주는 무엇으로 이루어졌나", 4.0)
pie = make_chart(1, Chart2D.ChartType.Pie if hasattr(Chart2D.ChartType, "Pie") else None,
                 Vec(0, 45, 0), 0.75, ncat=3)
if pie is not None:
    # ★ 라벨 영문 (한글 □□ 회피)
    set_cat(pie, 1, "Dark Energy 68%", 0.68, Vec(0.60, 0.25, 0.80))
    set_cat(pie, 2, "Dark Matter 27%", 0.27, Vec(0.25, 0.45, 0.85))
    set_cat(pie, 3, "Ordinary 5%", 0.05, Vec(1.00, 0.80, 0.20))
    feat(pie, "setIntensity", 1.0, Anim(2.0)); sleep(2.3)     # 페이드인 → 3조각(비율 맞아야)

narr("보라(암흑에너지)가 2/3, 금색(보통물질=별·행성)은 겨우 5%", 5.0)
narr("우리가 아는 물질은 우주의 5% 뿐", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("Chart2D — 돔에 띄우는 데이터 차트", 4.0)
if pie is not None:
    feat(pie, "setIntensity", 0.0, Anim(1.5))
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료(v5 setCategoryCount). ★핵심 리포트: "
      "①★이번엔 막대가 8개(Mercury~Neptune) 다 뜨나 — setCategoryCount(8) 을 추가함(기본 3이라 3개만 떴던 것, 하드캡 아님) "
      "②목성/토성이 압도적으로 높고 암석행성은 낮나 ③파이 3조각 비율 맞나(보라 2/3) ④라벨 영문 잘 읽히나")

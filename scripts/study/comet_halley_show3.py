# -*- coding: utf-8 -*-
"""
comet_halley_show3.py — 핼리 혜성: 본체가 보이는 날짜로 (2026-07-09)
show2 실측: 궤도선은 나오는데 혜성 본체가 안 보임.
원인 = **2024년이 핼리의 원일점(aphelion)** — 1986 근일점 +반주기라 지금 해왕성 너머 35 AU.
      궤도상 가장 멀고 어두운 지점이라 본체가 까마득한 점.
해결: 날짜를 **근일점 근처(2061-06)로 한 번에 점프**(애니 없는 setDateTime = 회전 안 함).
     혜성이 태양 가까이 = 크고 밝게. modelScale ↑ + 포인터 상시 ON 으로 확실히 표시.

지상 시점 유지(궤도선 렌더 구도). FadeTo 안 씀. 모델 먼저(확정 순서).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 지상 하늘 + ★ 근일점 근처 날짜(본체가 크게 보이는 시점) ──
print("무대: 지상 하늘 / 날짜 = 2061-06 (다음 근일점 직전, 혜성 근접)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2061, 6, 20, 0, 0, 0, tz, Anim(0.5))    # ★ 근일점(7/28) 약 5주 전 — 밝고 근접
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 2061년, 태양으로의 귀환"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 혜성 (모델 먼저 → 스케일 크게 → 요소 → 프레임 대기) ──────
print("핼리 궤도 요소 주입 (모델 먼저 + 큰 스케일)")
comet = Comet(Comet.CometName.Comet001)
comet.setStandardModelName(Comet.CometModelSet.Basic)
comet.setModelScale(20.0)                              # ★ 크게 (5→20)
comet.setIntensity(1.0, Anim(0.0))
sleep(0.3)
comet.setEccentricity(0.967, Anim(0.0))
comet.setInclination(162.3, Anim(0.0))
comet.setLongitudeOfAscendingNode(58.42, Anim(0.0))
comet.setArgumentOfPeriapsis(111.33, Anim(0.0))
comet.setDistanceToPeriapsis(0.586, Anim(0.0))
comet.setTimeOfLastPeriapsis(2446470.5, Anim(0.0))
comet.setLabelNameOverride("1P/Halley")
sleep(0.3)

t1.setText("긴 타원 궤도 — 그리고 혜성 본체"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.5))
comet.setLabelIntensity(0.8, Anim(2.0))
# ★ 포인터 상시 ON — 본체가 작아도 위치를 확실히 표시
try:
    comet.setPointerType(Body.PointerType.Model2Bold)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception as e:
    print("   포인터 스킵: %s" % e)
print(">>> ★ 이제 궤도선 + 혜성 본체(포인터 위치)가 보이나? (8초)")
sleep(8.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── 궤도 기하 해설 (정적) ─────────────────────────────────────
narration = [
    ("포인터가 가리키는 밝은 점 — 혜성 본체", 5.0),
    ("근일점 0.59 AU — 곧 금성 궤도 안쪽까지 접근", 5.0),
    ("원일점은 해왕성 너머 — 2024년엔 여기(가장 멀고 어두움)에 있었다", 6.0),
    ("궤도 경사 162° — 행성과 반대로 도는 역행 궤도", 5.0),
    ("마지막 근일점 1986년 · 이번 귀환 2061년", 5.0),
]
for text, dur in narration:
    t1.setText(text); t1.setIntensity(1.0, Anim(0.6))
    print("   자막: %s" % text)
    sleep(dur)
    t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 다시, 76년의 여정"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
comet.setPointerIntensity(0.0, Anim(1.2))
comet.setOrbitIntensity(0.0, Anim(2.5))
comet.setLabelIntensity(0.0, Anim(2.0))
comet.setIntensity(0.0, Anim(2.0))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: 혜성 본체가 이제 보이나? (2061 근접 + scale20 + 포인터)")

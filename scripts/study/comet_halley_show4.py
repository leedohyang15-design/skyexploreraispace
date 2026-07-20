# -*- coding: utf-8 -*-
"""
comet_halley_show4.py — 핼리 혜성: 3D 모델로 본체 크게 (2026-07-09)
show3 실측(스크린샷): 궤도선 아래 근일점 부근에 포인터 동그라미 = 혜성 위치는 맞음.
단 Basic 모델이 작은 점이라 태양 근처에서 안 띄어 보임.
이번 시도:
 ① 모델 = Halley3D (코마+꼬리 3D 전용 모델 — Bolide ColoredFireball 처럼 '진짜' 형태)
    ⚠️ 3D 모델은 에셋 이슈 가능(Bolide Chelyabinsk 전례) → 실패 시 로그로 판정, Basic 폴백.
 ② 날짜 = 2061-04 (근일점 3개월 전) — 태양에서 더 떨어져 혜성이 안 묻힘.
 ③ modelScale 30 + 태양 intensity 0.6 (혜성 대비 ↑) + 포인터 상시.

지상 시점 유지(궤도선 렌더). 모델 먼저(확정 순서).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 ──────────────────────────────────────────────────────
print("무대: 지상 하늘 / 2061-04 (근일점 3개월 전)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(0.6, Anim(0.0))                       # ★ 태양 낮춰 혜성 대비 ↑
dm.stop(); sleep(0.3)
dm.setDateTime(2061, 4, 20, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 2061년, 태양으로의 귀환"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 혜성 (Halley3D 모델 우선, 실패 시 Basic 폴백) ─────────────
print("핼리 궤도 요소 주입 (Halley3D 모델 시도)")
comet = Comet(Comet.CometName.Comet001)
model_used = "Halley3D"
try:
    comet.setStandardModelName(Comet.CometModelSet.Halley3D)
    print("   setStandardModelName(Halley3D) 호출 OK — 읽음=%s" % getattr(comet, "standardModelName", "?"))
except Exception as e:
    print("   Halley3D 실패(%s) → Basic 폴백" % e)
    comet.setStandardModelName(Comet.CometModelSet.Basic)
    model_used = "Basic"
comet.setModelScale(30.0)                              # ★ 크게
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

t1.setText("혜성 본체 — 코마와 꼬리 (%s 모델)" % model_used); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.5))
comet.setLabelIntensity(0.8, Anim(2.0))
try:
    comet.setPointerType(Body.PointerType.Model2Bold)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception as e:
    print("   포인터 스킵: %s" % e)
print(">>> ★ 혜성 본체가 이제 크게/뚜렷이 보이나? (%s 모델, scale 30) (9초)" % model_used)
sleep(9.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── 궤도 기하 해설 ────────────────────────────────────────────
for text, dur in [
    ("포인터가 가리키는 곳 — 핼리 혜성 본체", 5.0),
    ("근일점 0.59 AU — 곧 태양에 최접근", 5.0),
    ("원일점은 해왕성 너머 · 이심률 0.97 극단 타원", 5.0),
    ("궤도 경사 162° — 행성과 반대로 도는 역행", 5.0),
    ("마지막 근일점 1986 · 이번 귀환 2061", 5.0),
]:
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
print("종료. 리포트: ①%s 모델 본체가 크게 보이나(3D면 꼬리 있나) ②Basic 대비 나아졌나" % model_used)

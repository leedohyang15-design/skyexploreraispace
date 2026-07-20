# -*- coding: utf-8 -*-
"""
comet_halley_show2.py — 핼리 혜성: 궤도 기하 쇼 (2026-07-09)
실측으로 갈린 두 사실:
 ✅ 궤도선은 **지상(지구 하늘) 시점**에서만 그려짐 (스크린샷의 그 멋진 타원+라벨).
 ❌ 태양 황도 포트(우주 시점)로 옮기면 궤도선 투영이 사라져 아무것도 안 보임.
 ⚠️ 지상 시점 + 다년 시간가속 = 지구 자전 광란 회전.
→ 결론: **지상 시점의 궤도 자체를 주인공으로**. 어지러운 다년 시간가속은 뺀다.
        대신 궤도 기하(근일점/원일점/역행/주기)를 자막으로 해설하는 정적 쇼.

핼리 궤도 6요소(J2000 실제값). 슬롯 방식 + 모델 먼저(확정 순서). FadeTo 안 씀.
카메라 이동 없음 — reset 기본 지상 시점(궤도선 나오는 그 구도) 유지.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 지상 하늘 (궤도선 나오는 구도 — 카메라 이동 없음) ────
print("무대: 지상 하늘 (궤도선 렌더 구도)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2024, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 76년 주기의 방문자"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 혜성 (확정 순서: 모델 먼저 → 스케일 → 요소 → 프레임 대기) ──
print("핼리 궤도 요소 주입 (모델 먼저!)")
comet = Comet(Comet.CometName.Comet001)
comet.setStandardModelName(Comet.CometModelSet.Basic)
comet.setModelScale(5.0)
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

# 궤도선 페이드인
t1.setText("긴 타원 궤도 — 태양을 초점으로"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.5))
comet.setLabelIntensity(0.8, Anim(2.0))
print(">>> 궤도선 등장 (6초)")
sleep(6.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── 궤도 기하 해설 (자막 시퀀스 — 정적, 어지럽지 않음) ────────
narration = [
    ("포인터가 가리키는 곳 — 혜성 본체", 5.0, "pointer_on"),
    ("근일점 0.59 AU — 금성 궤도 안쪽까지 태양에 접근", 5.0, None),
    ("원일점은 해왕성 너머 — 이심률 0.97 의 극단적 타원", 5.0, None),
    ("궤도 경사 162° — 행성과 반대로 도는 '역행' 궤도", 5.0, None),
    ("마지막 근일점 1986년 · 다음은 2061년", 5.0, "pointer_off"),
]
for text, dur, act in narration:
    t1.setText(text); t1.setIntensity(1.0, Anim(0.6))
    if act == "pointer_on":
        try:
            comet.setPointerType(Body.PointerType.Model2Bold)
            comet.setPointerIntensity(1.0, Anim(1.2))
        except Exception as e:
            print("   포인터 스킵: %s" % e)
    elif act == "pointer_off":
        try:
            comet.setPointerIntensity(0.0, Anim(1.2))
        except Exception:
            pass
    print("   자막: %s" % text)
    sleep(dur)
    t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 다음 만남은 2061년"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
comet.setOrbitIntensity(0.0, Anim(2.5))
comet.setLabelIntensity(0.0, Anim(2.0))
comet.setIntensity(0.0, Anim(2.0))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: 궤도선+라벨+포인터+자막 해설이 안정적으로(회전 없이) 나왔나?")

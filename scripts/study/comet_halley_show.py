# -*- coding: utf-8 -*-
"""
comet_halley_show.py — 핼리 혜성 완성쇼 (2026-07-09)
comet_halley_final 실측: 궤도선+라벨은 완벽히 나옴. 단 **시간가속 때 화면이 어지럽게 회전**.
원인 확정: reset(1) 은 지상(청주 Earth Equatorial Sync)에 둠 → 시간 37년 가속 =
          지구 자전 ~1.3만 바퀴 → 하늘 광란 회전(궤도운동이 자전에 묻힘).
해결: **태양 황도 포트로 카메라 이동 = 우주(태양 중심) 시점** → 자전 제거, 궤도운동만 부드럽게.
     (복합 데모의 확정 태양계 조망 프레이밍 재사용.)

핼리 궤도 6요소(J2000 실제값). FadeTo 안 씀(궤도선 소거 회피). 슬롯 방식 + 모델 먼저.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 우주 조망 (지상 아님!) ──────────────────────────────
print("무대: 태양계 조망 (우주 시점 — 자전 제거)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2024, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

# ★ 핵심: 태양 황도 포트 기준으로 카메라 배치 = 태양 중심(우주) 시점.
#   이 프레임엔 지구 자전이 없어 시간가속해도 궤도운동만 보임.
sun_port = -1
try:
    sun_port = sun.portId(IndividualStar.IndividualStarPort.Ecliptic)
    cam.setPositionLBR(Vec(0.0, 50.0, 35.0), Anim(3.0), sun_port)   # 황도 위 비스듬히 조망
    print("   태양 황도 포트=%s 로 우주 조망 진입" % sun_port)
    sleep(3.5)
except Exception as e:
    print("   ⚠️ 우주 조망 진입 실패(%s) — 지상 시점이면 시간가속 시 회전 주의" % e)

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

t1.setText("긴 타원 궤도 — 태양을 향해"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.0))
comet.setLabelIntensity(0.8, Anim(2.0))
try:
    comet.setPointerType(Body.PointerType.Model2Bold)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception as e:
    print("   포인터 스킵: %s" % e)
print(">>> 궤도선 + 혜성 감상 (8초)")
sleep(8.0)
comet.setPointerIntensity(0.0, Anim(1.0))
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 시간가속: 우주 시점이라 이제 부드럽게 궤도만 이동 ─────────
print("시간가속 2024 → 2061 (우주 시점 = 자전 없이 궤도운동만)")
t1.setText("시간을 빠르게 — 2061년 근일점으로"); t1.setIntensity(1.0, Anim(0.8))
dm.setDateTime(2061, 7, 28, 0, 0, 0, tz, Anim(30.0))   # 37년을 30초에
for i in range(5):
    sleep(6.0)
    try:
        print("   JD=%.1f" % dm.julianDate)
    except Exception:
        pass
print("   ★ 이번엔 화면이 안 돌고 혜성만 궤도를 따라 이동했나?")
t1.setText("태양을 스치고 — 다시 먼 우주로")
sleep(3.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 다음 만남은 2061년"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
comet.setOrbitIntensity(0.0, Anim(2.0))
comet.setIntensity(0.0, Anim(2.0))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①화면 회전이 사라졌나 ②혜성이 궤도선 따라 근일점으로 이동했나")

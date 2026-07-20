# -*- coding: utf-8 -*-
"""
comet_halley_final.py — 핼리 혜성 완성본 (2026-07-09)
v1/v2 실측 확정:
 ✅ 슬롯 혜성(Comet001)에 궤도 6요소가 반영됨 — 단 **모델 먼저 설정 + 한 프레임 뒤** 라야 함
    (v1 실패 = 요소를 모델보다 먼저 넣고 즉시 읽음 → 전부 0).
 ✅ 궤도선(setOrbitIntensity)도 표시됨.
 ⚠️ DB FadeTo(1P/Halley)는 페이드 전환이 궤도선을 지움 → **슬롯 방식이 완전 제어라 정답**.
    (FadeTo 안 씀. 시간가속으로 혜성이 궤도를 도는 것만.)

핼리 궤도 요소 (J2000 실제값). 시간가속: 2024 → 2061 다음 근일점.
무대: 우주 조망(reset 기본 시점 — v2 [A]에서 궤도선 보인 그 구도, 카메라 이동 없음).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 (v2 [A] 재현: reset + 별/태양, 카메라 이동 없음) ──────
print("무대: 태양계 조망")
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

# ── 혜성 생성 (★ 확정 순서: 모델 먼저 → 스케일 → 요소 → 프레임 대기) ──
print("핼리 궤도 요소 주입 (모델 먼저!)")
comet = Comet(Comet.CometName.Comet001)
comet.setStandardModelName(Comet.CometModelSet.Basic)   # ★ ① 모델 먼저 (안 하면 요소 미반영)
comet.setModelScale(5.0)                                # ★ ② 스케일
comet.setIntensity(1.0, Anim(0.0))
sleep(0.3)
# ★ ③ 궤도 6요소 (Anim(0.0) 명시)
comet.setEccentricity(0.967, Anim(0.0))
comet.setInclination(162.3, Anim(0.0))
comet.setLongitudeOfAscendingNode(58.42, Anim(0.0))
comet.setArgumentOfPeriapsis(111.33, Anim(0.0))
comet.setDistanceToPeriapsis(0.586, Anim(0.0))          # AU (실측: 반영 확인)
comet.setTimeOfLastPeriapsis(2446470.5, Anim(0.0))      # JD 1986-02-09
comet.setLabelNameOverride("1P/Halley")
sleep(0.3)                                              # ★ ④ 한 프레임 대기 (반영)

# 궤도선 페이드인 (FadeTo 안 쓰므로 계속 유지됨)
t1.setText("긴 타원 궤도 — 태양을 향해"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.0))
comet.setLabelIntensity(0.8, Anim(2.0))
try:
    comet.setPointerType(Body.PointerType.Model2Bold)   # 개체 직결 포인터 (타입 지정 습관)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception as e:
    print("   포인터 스킵: %s" % e)
print(">>> 궤도선 + 혜성 감상 (8초)")
sleep(8.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 시간가속: 2024 → 2061 근일점 (궤도선 유지한 채 이동) ──────
print("시간가속 2024 → 2061 (다음 근일점)")
t1.setText("시간을 빠르게 — 2061년 근일점으로"); t1.setIntensity(1.0, Anim(0.8))
comet.setPointerIntensity(0.0, Anim(1.0))              # 포인터는 끄고 이동 관찰
dm.setDateTime(2061, 7, 28, 0, 0, 0, tz, Anim(28.0))   # 37년을 28초에
for i in range(5):
    sleep(5.6)
    try:
        print("   JD=%.1f" % dm.julianDate)
    except Exception:
        pass
print("   ★ 혜성이 궤도선을 따라 근일점(태양 근처)으로 이동했나?")
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
print("종료. 리포트: 궤도선 유지된 채 혜성이 근일점으로 이동했는지?")

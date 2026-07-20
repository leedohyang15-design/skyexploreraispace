# -*- coding: utf-8 -*-
"""
night_guide_tour_v4.py — 그리드 '아래 잘림' 해결판 (2026-07-07)
v3 실측: Place2D 그리드 4종 + Planet 적도/황도 그리드 전부 표시 확인! (그리드 본명령 확정)
남은 문제: 그리드가 돔 아래쪽에서 잘림.

★ 잘림의 원인 = Target 30 틸트.
  Target 30 은 관람용 구도라 돔 하단에 '지평선 아래' 영역이 들어옴 —
  하늘 그리드는 지평선 위에만 그려지므로 그 영역이 비어 보이는 것.
  → 그리드 풀 표출 = **Target 90 (천정 정렬)**: 지평선이 돔 가장자리에 정확히 걸려
    방위 그리드가 동심원으로 돔을 가득 채움 (플라네타리움 교육 장면의 고전 구도).
  → Target 재정렬 슬루는 관객에게 보이므로 정석대로 암전 속에서 (2026-07-06 확정).

구성: 천정 정렬 후 그리드 3종을 이어서 감상 → Target 30 복귀.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 청주 겨울밤 (동일) ──────────────────────────────────
print("무대 세팅: 청주 2026-01-15 23:00 KST")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))

earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)

# ★ 핵심: 암전 상태에서 천정 정렬(Target 90) 완료 후 페이드인 — 슬루 숨김 정석
cam.setTargetHeight(90.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))
sleep(0.8)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

# ── 그리드 쇼 (천정 구도 — 지평선이 돔 가장자리) ─────────────
print("=" * 60)
print("그리드 쇼 @ Target 90 — 이제 잘림 없이 돔 가득 차는지 확인!")
print("=" * 60)

print(">>> ① 방위/고도 그리드 — 천정 중심 동심원 (8초)")
t1.setText("방위/고도 그리드 — 하늘의 주소판"); t1.setIntensity(1.0, Anim(0.5))
place.setAzimuthGridIntensity(0.9, Anim(2.0))
place.setCardinalPointsIntensity(0.9, Anim(2.0))     # 동서남북 표지 (가장자리 = 지평선)
sleep(8.0)
place.setAzimuthGridIntensity(0.0, Anim(1.5))
place.setCardinalPointsIntensity(0.0, Anim(1.5))
sleep(1.7)

print(">>> ② 적도 좌표 그리드 — 북극성 중심으로 기울어진 격자 (8초)")
t1.setText("적도 좌표 그리드 — 북극성이 축")
earth.setEquatorialGridIntensity(0.9, Anim(2.0))
sleep(8.0)

print(">>> ③ + 시간각 그리드 겹치기 (6초) — 두 좌표계 비교")
t1.setText("시간각 그리드 — 하늘의 시계")
place.setHourAngleGridIntensity(0.9, Anim(2.0))
sleep(6.0)
earth.setEquatorialGridIntensity(0.0, Anim(1.5))
place.setHourAngleGridIntensity(0.0, Anim(1.5))
sleep(1.7)
t1.setIntensity(0.0, Anim(0.5))

# ── Target 30 복귀 (관람 표준) — 역시 암전 속에서 ────────────
print("Target 30 복귀 (암전 속 재정렬)")
uni.setGlobalIntensity(0.0, Anim(1.5)); sleep(1.8)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.8)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
t1.setText("v4 끝 — 그리드가 돔에 꽉 찼나요?"); t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("v4 종료.")

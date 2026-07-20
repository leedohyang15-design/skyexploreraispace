# -*- coding: utf-8 -*-
"""
celestial_rotation.py — 천구의 회전: 별은 왜 도는가 (2026-07-13, 사용자 확정 Recording15)
새 API 중점: 좌표 그리드 (지상/천구) — 지금껏 Mark 로 헤맸고 '본명령'은 안 써봄.
  · 지상(고정): Place2D.setAzimuthGridIntensity(방위/고도) · setCardinalPointsIntensity(동서남북) ·
    setMeridianIntensity(자오선)
  · 천구(별과 함께 회전): Planet.setEquatorialGridIntensity(적도 그리드)
확정 메커니즘: DateManager 시간가속(setDateTime, Anim) — day_night/eclipse 로 검증된 부드러운 가속.

컨셉: 지상 좌표계(고정)와 천구 좌표계(회전)를 동시에 보여준 뒤 시간을 가속 →
      별·적도그리드가 '북극성(자전축)'을 중심으로 돌고, 방위그리드·동서남북은 그대로.
      = "지구가 도니까 하늘이 도는 것처럼 보인다"가 그리드로 한눈에.

무대: 청정 밤하늘, 전천 구도(Target 0), 북쪽(북극성) 향함.
설계 근거(CLAUDE.md): 지상 전천 그리드 구도 = Target 0. 그리드 '본명령' = Place2D/Planet 속성.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 청정 밤하늘 (북쪽 전천) ────────────────────────────
print("무대: 청정 밤하늘, 북쪽 전천")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))            # 청주
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 3, 20, 12, 0, 0, tz, Anim(0.5))    # 12 UT = 21시 KST(밤)
sleep(1.0)
# 전천 구도 = Target 0, 북쪽 향함 (H = 180 - 방위, 북=방위0 → H=180)
cam.setTargetHeight(0.0, Anim(0.0))
cam.setOrientationH(180.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("밤하늘 — 별은 정말 '떠 있기'만 할까?"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ① 지상 좌표 그리드 (고정: 방위/고도 + 동서남북 + 자오선) ─
print(">>> 지상 좌표 그리드")
t1.setText("내가 선 자리의 좌표 — 방위와 고도(고정된 땅의 격자)"); t1.setIntensity(1.0, Anim(1.0))
try:
    place.setAzimuthGridIntensity(0.45, Anim(2.5))
except Exception as e:
    print("   방위그리드 실패: %s" % e)
try:
    place.setMeridianIntensity(0.4, Anim(2.5))
except Exception as e:
    print("   자오선 실패: %s" % e)
try:
    # 동서남북 표지 — 기본 representation 으로 잘 뜸(Recording15 확인). Representation 세터는 enum 경로 불명이라 생략.
    place.setCardinalPointsIntensity(0.9, Anim(2.5))
except Exception as e:
    print("   동서남북 실패: %s" % e)
sleep(4.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ② 천구 적도 그리드 (별과 함께 회전할 격자) ───────────────
print(">>> 천구 적도 그리드")
t1.setText("하늘의 좌표 — 천구의 적도와 극(자전축이 향한 곳)"); t1.setIntensity(1.0, Anim(1.0))
try:
    earth.setEquatorialGridIntensity(0.6, Anim(2.5))
except Exception as e:
    print("   적도그리드 실패: %s" % e)
sleep(4.5)
# 북극성 지목 (있으면)
try:
    polaris = IndividualStar(IndividualStar.IndividualStarName.Polaris)
    polaris.setPointerIntensity(1.0, Anim(1.5))
    t1.setText("북극성 — 자전축이 가리키는 별, 거의 움직이지 않는다")
    print("   북극성 포인터 ON")
except Exception as e:
    print("   Polaris 포인터 실패(enum 확인 필요): %s" % e)
    t1.setText("천구의 북극 — 자전축이 가리키는 하늘의 한 점")
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ③ 시간가속 — 천구 회전 관찰 ──────────────────────────────
print(">>> 시간가속 (12 UT → 18 UT, 6시간을 32초에)")
t1.setText("시간을 빠르게 감으면… 별과 하늘 격자가 극을 중심으로 돈다"); t1.setIntensity(1.0, Anim(1.0))
try:
    dm.setDateTime(2026, 3, 20, 18, 0, 0, tz, Anim(32.0))   # 6시간 = 90° 회전
    sleep(33.0)
    print("   ★ 별·적도그리드가 북극 중심으로 돌고, 방위그리드/동서남북은 고정됐나?")
except Exception as e:
    print("   시간가속 실패: %s" % e)
    sleep(6.0)
t1.setText("땅의 격자는 그대로 — 도는 건 '하늘'(사실은 지구가 돈다)")
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ④ 그리드 정리 + 피날레 ───────────────────────────────────
print(">>> 그리드 페이드아웃 + 피날레")
for fn in ("setAzimuthGridIntensity", "setMeridianIntensity", "setCardinalPointsIntensity"):
    try:
        getattr(place, fn)(0.0, Anim(2.0))
    except Exception:
        pass
try:
    earth.setEquatorialGridIntensity(0.0, Anim(2.0))
except Exception:
    pass
try:
    polaris.setPointerIntensity(0.0, Anim(1.5))
except Exception:
    pass
sleep(2.2)
t1.setText("천구의 회전 — 하루에 한 바퀴, 지구 자전의 그림자"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①방위그리드/동서남북/자오선 켜지나 ②적도그리드 켜지나(어느 게 뭔지) "
      "③시간가속서 별+적도그리드 회전 & 방위그리드 고정 대비 보이나 ④북극성 포인터 뜨나")

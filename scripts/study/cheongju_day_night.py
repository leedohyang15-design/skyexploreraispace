# -*- coding: utf-8 -*-
"""
cheongju_day_night.py — 청주 아침→낮→석양→밤 타임랩스 (앱 생성본 수정판)
====================================================================
앱 생성본의 '아침/낮이 안 보이는' 원인 2가지 수정:
  ① 시간대: DefaultTimeZone = UTC (실측 확정) — 생성본의 "12:00"은 한국 밤 21시였음!
     → 한국시(KST) 를 UT(-9h) 로 변환해서 지정.
  ② 낮 하늘(파란 하늘) = 대기 산란 렌더 — ★프로브: Planet(Earth) 의
     setAtmosphereIntensity / setScatteringIntensity / setAtmosphereHaloIntensity
표준 적용: Target 30(관람 정위치), 시간 점프 대신 setDateTime+Anim 가속(부드러움)

확인해줘: (a)아침·낮 하늘이 밝게(파랗게) 보이는지 (b)석양 색 (c)밤 별 (d)토성 줌
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 36.64, 127.50, 100.0     # 청주
KST = [(2026, 7, 6, 6, 30),              # 아침
       (2026, 7, 6, 12, 0),              # 정오
       (2026, 7, 6, 19, 40),             # 석양
       (2026, 7, 6, 21, 30)]             # 밤
ACCEL = 8.0                              # 구간당 가속 시간(초)
VIEW  = 5.0                              # 구간당 감상 시간(초)

def to_ut(y, m, d, hh, mm):              # KST → UT (-9h, 자정 넘어가면 전날)
    h = hh - 9
    if h < 0:
        h += 24; d -= 1
    return y, m, d, h, mm

# ── 0) 리셋 + 암전 ──────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(LAT, LON, ALT))
print("★1 관측지: 청주")

# ── 1) ★ 낮 하늘 렌더 프로브 (지구 대기) ─────────────────────
earth = Planet(Planet.PlanetName(2))
for api, v in (("setAtmosphereIntensity", 1.0), ("setScatteringIntensity", 1.0),
               ("setAtmosphereHaloIntensity", 1.0)):
    try:
        getattr(earth, api)(v, Anim(0.0))
        print("★2 %s(%.1f) OK" % (api, v))
    except Exception as e:
        print("★2 %s 실패: %s" % (api, repr(e)[:50]))

# ── 2) 시각 = 아침 (KST→UT 변환 + stop 순서 + JD 확인) ───────
dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
y, m, d, hh, mm = to_ut(*KST[0])
dm.stop(); sleep(0.3)
dm.setDateTime(y, m, d, hh, mm, 0, tz, Anim(0.5))
sleep(1.5)
print("★3 아침 세팅 (KST %02d:%02d = UT %02d:%02d) JD=%.4f"
      % (KST[0][3], KST[0][4], hh, mm, dm.julianDate))

Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # 별은 밤에 켬
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(30.0, Anim(1.5))     # 🎯 관람 표준
sleep(2.0)

# ── 3) 페이드인: 아침 하늘 ───────────────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
print(">>> 아침 (a) 하늘이 밝은지/파란지 확인!")
sleep(VIEW)

# ── 4) 시간 가속: 아침→정오→석양→밤 (각 8초, 부드럽게) ────────
names = ("정오", "석양", "밤")
for i, (label) in enumerate(names, start=1):
    y, m, d, hh, mm = to_ut(*KST[i])
    print(">>> %s 로 가속 (%.0f초)" % (label, ACCEL))
    dm.setDateTime(y, m, d, hh, mm, 0, tz, Anim(ACCEL))
    sleep(ACCEL + 0.5)
    if label == "밤":
        Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(2.0))
        Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(2.0))
    sleep(VIEW)

# ── 5) 토성 FadeTo (암전 클램프) + 화면 고정 줌 ───────────────
print(">>> 토성으로!")
DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
for _ in range(25):                       # FadeTo 자체 페이드 억제 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)
# FadeTo 기본 Target 30 = 관람 정위치 → 재정렬 불필요!
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

p = cam.positionLBR
cam.setPositionR(p.z * 0.5, Anim.cubic(4.0), -1)   # R만 변경 = 화면 고정 줌
sleep(4.5)
print(">>> 끝! (a)아침·낮 밝음? (b)석양? (c)밤 별? (d)토성 줌? — ★2 줄들과 함께 알려줘")

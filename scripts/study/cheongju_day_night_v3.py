# -*- coding: utf-8 -*-
"""
cheongju_day_night_v3.py — ✅✅ 확정(사용자 확인 2026-07-06) — 지상 낮밤 타임랩스 표준 골격
====================================================================
v1: 전부 검은 하늘(토성만 OK) + 사용자 확인 "UI 에서 대기효과 꺼져 있음".
공식 문서(Atmosphere.htm): 대기는 기본 시뮬레이션, 레버 = Planet Atmosphere Intensity(기본 1),
낮 파란 하늘 = 레일리 산란, 낮→밤 별 전환도 대기가 물리적으로 처리.

v2 수정:
  ① ★대기 값 실측: earth.atmosphereIntensity 를 설정 '전/후'로 읽어 출력
     → 우리 호출이 실제로 반영되는지 / 애초에 0이었는지 판별
  ② 태양 켜기 (v1 누락!) — 태양 없으면 대기가 산란시킬 광원이 없음
  ③ 별은 처음부터 1.0 — 낮엔 대기가 알아서 가림(문서: 물리 시뮬레이션)

그래도 하늘이 검으면: Studio 에서 [녹화 시작 → UI 의 '대기효과' 토글 ON → 녹화 정지]
한 번만 해서 SPC 를 보내줘 — 그 토글의 진짜 명령을 변환기로 해독할게!
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 36.64, 127.50, 100.0
KST = [(2026, 7, 6, 6, 30), (2026, 7, 6, 12, 0),
       (2026, 7, 6, 19, 40), (2026, 7, 6, 21, 30)]
ACCEL, VIEW = 8.0, 5.0

def to_ut(y, m, d, hh, mm):
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

# ── 1) ★★ 지구 본체 + 대기 (Recording3 해독: UI '대기효과' 토글 = 이 두 명령!) ──
earth = Planet(Planet.PlanetName(2))
earth.setIntensity(1.0, Anim(0.0))       # ★★ 마스터 스위치 — 이게 꺼져 있으면 대기도 안 그려짐
print("★0 지구 본체 ON (intensity=%s)" % getattr(earth, "intensity", "?"))
for prop, setter in (("atmosphereIntensity", "setAtmosphereIntensity"),
                     ("scatteringIntensity", "setScatteringIntensity"),
                     ("atmosphereHaloIntensity", "setAtmosphereHaloIntensity")):
    try:
        before = getattr(earth, prop)
    except Exception:
        before = "읽기불가"
    try:
        getattr(earth, setter)(1.0, Anim(0.0))
        sleep(0.3)
        after = getattr(earth, prop, "?")
        print("★1 %s: %s → %s" % (prop, before, after))
    except Exception as e:
        print("★1 %s 실패: %s" % (setter, repr(e)[:50]))

# ── 2) ★ 광원(태양)+별 켜기 — v1 누락분 ──────────────────────
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.0))
print("★2 태양 ON (intensity=%s)" % getattr(sun, "intensity", "?"))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))   # 낮엔 대기가 가림
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))

# ── 3) 시각 = 아침 (KST→UT) ─────────────────────────────────
dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
y, m, d, hh, mm = to_ut(*KST[0])
dm.stop(); sleep(0.3)
dm.setDateTime(y, m, d, hh, mm, 0, tz, Anim(0.5))
sleep(1.5)
print("★3 아침 (KST 06:30 = UT %02d:%02d 전날) JD=%.4f" % (hh, mm, dm.julianDate))

cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(30.0, Anim(1.5))
sleep(2.0)

# ── 4) 페이드인: 아침 ───────────────────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
print(">>> 아침! (a) 하늘 밝음/파란색? 태양 보임?")
sleep(VIEW)

# ── 5) 가속: 정오 → 석양 → 밤 ────────────────────────────────
for i, label in enumerate(("정오", "석양", "밤"), start=1):
    y, m, d, hh, mm = to_ut(*KST[i])
    print(">>> %s 로 가속 (%.0f초)" % (label, ACCEL))
    dm.setDateTime(y, m, d, hh, mm, 0, tz, Anim(ACCEL))
    sleep(ACCEL + 0.5)
    sleep(VIEW)

print(">>> v3 끝! (a)아침·정오 파란 하늘? (b)석양 붉은빛? (c)밤 별? "
      "+ ★1 의 전/후 값들을 그대로 보내줘. 그래도 검으면 '대기 토글 녹화' 부탁!")

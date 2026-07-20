# -*- coding: utf-8 -*-
"""
eclipse_2026_v4.py — [v4] 조준 4종 비교: 정지된 개기식에서 하나씩 시연
====================================================================
v3 결과: 코로나 렌더 완벽. 줌 락은 뷰를 움직였지만(가장자리→2시 방향+롤) 중앙엔 못 옴.
의심: 태양 Ecliptic 포트의 Vec(0,0,0) 이 태양이 아닐 수 있음(프레임 원점 문제).

이번 판: 시간을 개기식에 '고정'해 두고, 조준 방법 A~D 를 4초 간격으로 하나씩 시연.
각 단계에서 일식(코로나)이 어디로 가는지만 알려줘!
  ★A setTargetHeight(60)      — 돔 틸트 (Sky View 에서 트랙볼이 먹는지)
  ★B setTarget(az, alt)       — 태양 방위/고도로 직접 조준
  ★C 줌 락 (긴 슬루 8초 대기) — v3 재시도, 이번엔 슬루 완료까지 대기
  ★D FOV 40 줌인              — C 상태에서 조여서 확인
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
SUN_AZ, SUN_ALT = 285.0, 11.0     # 개기식 순간 태양 방위/고도 (사라고사 근사)

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 0) 리셋 + 관측지 + 개기식 시각 고정 (v2 확정 패턴) ────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(LAT, LON, ALT))

dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
want = expected_jd(UTC_TOTAL)
for attempt in (1, 2, 3):
    day, hh, mm = local(UTC_TOTAL)
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 8, day, hh, mm, 0, tz, Anim(0.5))
    sleep(1.5)
    err_h = (dm.julianDate - want) * 24.0
    if abs(err_h) < 0.2:
        print("★0 개기식 시각 고정 OK")
        break
    TZ_OFFSET -= int(round(err_h))

Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
sun_obj = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun_obj.setIntensity(1.0, Anim(0.0))
Satellite(Satellite.SatelliteName.Moon).setIntensity(1.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)
sun_port = sun_obj.portId(IndividualStar.IndividualStarPort.Ecliptic)

# ── 1) 페이드인: 기준 상태 (개기식이 가장자리 어딘가) ──────────
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
print(">>> 기준: 개기식이 돔 가장자리(서쪽)에 있을 것. 이제 A~D 시연 시작")
sleep(4.0)

# ── ★A: 돔 틸트 (setTargetHeight) ────────────────────────────
print("★A setTargetHeight(60) — 4초 뒤 위치 확인 (HUD Target 값도!)")
try:
    cam.setTargetHeight(60.0, Anim(3.0))
except Exception as e:
    print("★A 실패:", repr(e)[:60])
sleep(5.0)

# ── ★B: 방위/고도 직접 조준 (setTarget) ──────────────────────
print("★B setTarget(az=%.0f, h=%.0f) — 일식이 중앙 근처로 오는지" % (SUN_AZ, SUN_ALT))
try:
    cam.setTarget(Vec2(SUN_AZ, SUN_ALT), Anim(3.0))
except Exception as e:
    print("★B 실패:", repr(e)[:60])
sleep(5.0)

# ── ★C: 줌 락 — 이번엔 슬루 완료까지 8초 대기 ─────────────────
print("★C 줌 락(태양 포트) + 8초 대기 — 중앙으로 수렴하는지")
try:
    cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
    cam.setZoomPosition(Vec(0.0, 0.0, 0.0), sun_port, Anim(4.0), Camera.PositionMode.XYZ)
except Exception as e:
    print("★C 실패:", repr(e)[:80])
sleep(8.0)

# ── ★D: FOV 줌인 (C 상태 확인용) ─────────────────────────────
print("★D FOV→40 — 뭐가 화면 중앙에 있는지 (태양? 빈 하늘?)")
try:
    cam.setZoomFov(40.0, Anim.cubic(4.0))
except Exception as e:
    print("★D 실패:", repr(e)[:60])
sleep(6.0)
try:
    cam.setZoomFov(180.0, Anim(3.0))
except Exception:
    pass
sleep(3.5)

print(">>> v4 끝! A/B/C/D 각각에서 일식이 어디 있었는지(중앙/가장자리/화면 밖) + "
      "HUD Target 값 변화 알려줘. B가 성공이면 다음 판은 B+시간가속으로 완성!")

# -*- coding: utf-8 -*-
"""
eclipse_2026_v7.py — [v7] 사용자 수동 캘리브레이션 재현: L 회전 + Target 틸트
====================================================================
v6 실측: 사용자가 수동으로 태양을 정중앙에 → HUD **L=-285.34°, B=0.00°, R=0m**
  = Sky View 조준의 정식 레버는 setTarget 방위가 아니라
    **cam.setPositionLBR(Vec(L, B, 0), Anim, track)** 의 L 회전! (프로덕션 nile SPC 와 동일 패턴)
  + Target 틸트(setTargetHeight)는 이미 동작 확인(HUD 반영).

이번 판: 정지된 개기식에서 단계별 재현 — 어느 단계에서 중앙인지 알려줘!
  ★A 현재 positionLBR 읽기 (기준값)
  ★B setTargetHeight(79) 틸트만
  ★C setPositionLBR(L=-285.34, B=0) 회전 추가  ← 사용자 캘리브레이션 값
  ★D 상태 확인 + FOV 60
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
CAL_L         = -285.34      # ★ 사용자 수동 캘리브레이션 (v6 스크린샷 HUD)
CAL_B         = 0.0
TILT          = 79.0         # Target (= 90 - 태양고도 11)

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 준비 (확정 패턴) ─────────────────────────────────────────
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
        break
    TZ_OFFSET -= int(round(err_h))

Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Satellite(Satellite.SatelliteName.Moon).setIntensity(1.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)

# Place2D 포트 정보 수집 (지식용)
try:
    pports = [n for n in dir(Place2D.Place2DPort) if not n.startswith("_")]
    print("★0 Place2DPort 멤버:", pports[:10])
    for pn in pports[:4]:
        try:
            print("★0 portId(%s) = %s" % (pn, place.portId(getattr(Place2D.Place2DPort, pn))))
        except Exception:
            pass
except Exception as e:
    print("★0 포트 프로브 실패:", repr(e)[:60])

uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(3.0)

# ── ★A 기준값 읽기 ───────────────────────────────────────────
try:
    p = cam.positionLBR
    print("★A 현재 positionLBR = (L=%.2f, B=%.2f, R=%.3f)" % (p.x, p.y, p.z))
except Exception as e:
    print("★A 읽기 실패:", repr(e)[:60])
print("★A 기준: 일식은 가장자리에 있을 것. 5초 뒤 B 시작")
sleep(5.0)

# ── ★B 틸트만 (Target 79) ────────────────────────────────────
print("★B setTargetHeight(%.0f) — 일식 위치?" % TILT)
cam.setTargetHeight(TILT, Anim(2.5))
sleep(5.0)
try:
    p = cam.positionLBR
    print("★B 후 positionLBR = (%.2f, %.2f, %.3f)" % (p.x, p.y, p.z))
except Exception:
    pass

# ── ★C L 회전 추가 (사용자 캘리브레이션 값) ───────────────────
print("★C setPositionLBR(L=%.2f, B=%.2f, R=0) track=-1 — 중앙으로 오는지!" % (CAL_L, CAL_B))
try:
    cam.setPositionLBR(Vec(CAL_L, CAL_B, 0.0), Anim(3.0), -1)
except Exception as e:
    print("★C 실패:", repr(e)[:80])
sleep(5.5)
try:
    p = cam.positionLBR
    print("★C 후 positionLBR = (%.2f, %.2f, %.3f)" % (p.x, p.y, p.z))
except Exception:
    pass

# ── ★D FOV 확인 ──────────────────────────────────────────────
print("★D FOV 60 — 중앙에 일식이 크게?")
try:
    cam.setZoomFov(60.0, Anim(3.0)); sleep(5.0)
    cam.setZoomFov(180.0, Anim(2.5)); sleep(3.0)
except Exception:
    pass

print(">>> v7 끝! (a)B(틸트만)에서 일식 위치 (b)C(L회전 추가)에서 중앙 왔는지 "
      "(c)★A/B/C 의 positionLBR 값들 — 알려줘! C가 성공이면 공식 완성!")

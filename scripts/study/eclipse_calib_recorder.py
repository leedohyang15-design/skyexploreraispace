# -*- coding: utf-8 -*-
"""
eclipse_calib_recorder.py — [v8.1] 수동 조준 녹화기 — 틸트 79 선적용판
====================================================================
v8 실측: 틸트(Target) 없는 순정 상태에선 수동 회전으로 중앙 정렬이 '불가능'
         (Target 0 = 천정 축 스핀만 됨). v7처럼 스크립트가 틸트를 걸어놔야
         좌우 회전(Turn)으로 태양을 중앙에 가져올 수 있음 → 이번 판은 선적용!

사용 방법:
  1. 실행하면 개기식 하늘 + **틸트 79° 적용된 상태**로 120초 카운트 시작
  2. **마우스 좌클릭 Turn 으로 좌우만 돌려서** 일식을 돔 정중앙에 (필요하면 Altitude 미세조정)
  3. 스크립트가 2초마다 카메라 상태를 기록
  4. 끝나면 **[FINAL] 줄 + 직전 [REC] 몇 줄**을 통째로 보내줘 → 최종 쇼 완성!
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
RECORD_SEC    = 120
TILT          = 79.0          # ★ 수동 정렬이 가능해지는 조건 (v7/v8 실측 차이)

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 준비: 개기식 하늘 (확정 패턴) ────────────────────────────
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
cam.setTargetHeight(TILT, Anim(2.0))          # ★ 틸트 선적용 — 이래야 수동 정렬 가능
sleep(2.5)

uni.setGlobalIntensity(1.0, Anim(1.5))
sleep(2.0)

PROPS = ("positionLBR", "positionTrack", "positionMode",
         "orientationHPR", "orientationXYZR", "orientationTrack", "orientationMode",
         "activeTarget", "zoomFov", "port")

def snap():
    out = []
    for name in PROPS:
        try:
            v = getattr(cam, name)
            if hasattr(v, "x"):
                if hasattr(v, "w"):
                    out.append("%s=(%.2f,%.2f,%.2f,%.2f)" % (name, v.x, v.y, v.z, v.w))
                else:
                    out.append("%s=(%.2f,%.2f,%.2f)" % (name, v.x, v.y, v.z))
            else:
                out.append("%s=%s" % (name, v))
        except Exception:
            pass
    return " | ".join(out)

print("=" * 60)
print(">>> 틸트 %.0f° 적용 완료. 지금부터 %d초!" % (TILT, RECORD_SEC))
print(">>> 좌클릭 Turn 으로 좌우 회전해서 일식을 돔 정중앙에 맞춰줘!")
print(">>> 다 맞추면 손 떼고 기다려. 끝나면 [FINAL] 줄을 보내주면 돼.")
print("=" * 60)

last = ""
for t in range(0, RECORD_SEC, 2):
    s = snap()
    if s != last:
        print("[REC %02ds] %s" % (t, s))
        last = s
    sleep(2.0)

print("=" * 60)
print(">>> 녹화 끝! 최종 상태:")
print("[FINAL] " + snap())
print(">>> 위 [FINAL] 줄(과 그 직전 [REC] 몇 줄)을 그대로 복사해서 보내줘!")

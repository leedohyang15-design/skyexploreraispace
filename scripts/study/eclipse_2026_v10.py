# -*- coding: utf-8 -*-
"""
eclipse_2026_v10.py — [v10] 방향(H) 단독 회전 — 위치 명령 없이 조준
====================================================================
v9 실측: setTargetAzimuth 무반응 / 위치 명령(273)은 어떤 포트든 비행 모드 이탈.
새 단서(레코더 로그 재분석): 수동 Turn 때 orientationHPR 의 **H = L + 180** 으로 정확히 동행.
  → 비행 이탈의 범인은 '위치' 명령. **방향(H)만 단독으로** 돌리면 Sky View 유지 가능성!
  캘리브레이션: 정중앙 H = -283.85 + 180 = **-103.85**

⚠️ 실행 전: 좌상단이 Terrain View / 상단이 Land 면 Studio RESET 먼저!

정지된 개기식 + 틸트 79 에서:
  ★A setOrientationH(-103.85)                — 단일 float 방향 세터
  ★B setOrientationHPR(Vec(-103.85, 0, 0))   — HPR 벡터판
  ★C setOrientationHPRD(Vec4(-103.85,0,0,0), track=-1) — HPRD(현재 모드명) 판
각 단계: (1)일식 위치 (2)Sky View 유지(상단 Take off?) 알려줘!

+ 별도 부탁: 내가 변환했던 네 Recording.SPC 원본을 Studio 에서 그대로 재생하면
  중앙 정렬이 재현되는지(Sky View 유지?)도 한 번 확인해줘 — 교차 검증용.
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
CAL_H         = -283.85 + 180.0      # = -103.85 (녹화 실측: H = L + 180)
TILT          = 79.0

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
cam.setTargetHeight(TILT, Anim(2.0))
sleep(2.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(3.0)
try:
    o = cam.orientationHPR
    print(">>> 기준 orientationHPR = (%.2f, %.2f, %.2f) / 목표 H = %.2f" % (o.x, o.y, o.z, CAL_H))
except Exception:
    pass
print(">>> 5초 뒤 A 시작")
sleep(5.0)

# ── ★A 단일 H 세터 ───────────────────────────────────────────
print("★A setOrientationH(%.2f)" % CAL_H)
try:
    cam.setOrientationH(CAL_H, Anim(3.0))
except Exception as e:
    print("★A 실패:", repr(e)[:60])
sleep(6.0)
try:
    o = cam.orientationHPR
    print("★A 후 HPR = (%.2f, %.2f, %.2f)" % (o.x, o.y, o.z))
except Exception:
    pass

# ── ★B HPR 벡터판 ────────────────────────────────────────────
print("★B setOrientationHPR(Vec(%.2f, 0, 0))" % CAL_H)
try:
    cam.setOrientationHPR(Vec(CAL_H, 0.0, 0.0), Anim(3.0))
except Exception as e:
    print("★B 실패:", repr(e)[:60])
sleep(6.0)

# ── ★C HPRD (현재 orientationMode 명칭) ──────────────────────
print("★C setOrientationHPRD(Vec4(%.2f, 0, 0, 0), track=-1)" % CAL_H)
try:
    cam.setOrientationHPRD(Vec4(CAL_H, 0.0, 0.0, 0.0), Anim(3.0), -1)
except Exception as e:
    print("★C 실패:", repr(e)[:60])
sleep(6.0)
try:
    o = cam.orientationHPR
    print("★C 후 HPR = (%.2f, %.2f, %.2f)" % (o.x, o.y, o.z))
except Exception:
    pass

print(">>> v10 끝! A/B/C 중 '중앙 + Sky View 유지'는? + Recording.SPC 재생 결과도!")

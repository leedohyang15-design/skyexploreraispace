# -*- coding: utf-8 -*-
"""
eclipse_2026_v9.py — [v9] setTargetAzimuth 발견! 순수 트랙볼 조준 판별
====================================================================
발견: Camera 에 setTargetHeight 의 쌍둥이 **setTargetAzimuth(값, Anim)** 존재.
  → 위치 명령 없이 좌우 회전 가능 = Terrain View 로 튕길 위험 없음.
Terrain View 원因 판명: 이전 판의 setPositionLBR(track=positionTrack)이
  관측자 이탈(비행 카메라 진입)을 유발 — L/Target 값이 같아도 프레임이 달라 가장자리행.

⚠️ 실행 전: 좌상단 메뉴가 'Terrain View'면 Studio RESET 버튼을 눌러 Sky View 로 돌려놔줘!

정지된 개기식 + 틸트 79 상태에서:
  ★A setTargetAzimuth(-283.85)  — L 컨벤션 그대로
  ★B setTargetAzimuth(+283.85)  — 부호 반대
  ★C Place2D 포트로 273/295 쌍  — 관측자 alt-az 포트 후보들
각 단계에서 (1)일식 위치 (2)좌상단이 Sky View 유지인지 알려줘!
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
CAL_L         = -283.85
TILT          = 79.0

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 준비: 개기식 하늘 + 틸트 (확정 패턴) ─────────────────────
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
print(">>> 기준 상태 (틸트 79, 회전 전). 5초 뒤 A 시작 — 각 단계에서 일식 위치+모드!")
sleep(5.0)

# ── ★A setTargetAzimuth(-283.85) ─────────────────────────────
print("★A setTargetAzimuth(%.2f)" % CAL_L)
try:
    cam.setTargetAzimuth(CAL_L, Anim(3.0))
except Exception as e:
    print("★A 실패:", repr(e)[:60])
sleep(6.0)

# ── ★B setTargetAzimuth(+283.85) ─────────────────────────────
print("★B setTargetAzimuth(%.2f)" % (-CAL_L))
try:
    cam.setTargetAzimuth(-CAL_L, Anim(3.0))
except Exception as e:
    print("★B 실패:", repr(e)[:60])
sleep(6.0)

# ── ★C Place2D 포트로 273/295 쌍 (올바른 관측자 프레임 탐색) ──
try:
    cam.setTargetAzimuth(0.0, Anim(1.5)); sleep(2.0)   # 회전 원위치
except Exception:
    pass
try:
    pports = [n for n in dir(Place2D.Place2DPort) if not n.startswith("_")]
    print("★C Place2DPort:", pports)
    for pn in pports[:5]:
        try:
            pid = place.portId(getattr(Place2D.Place2DPort, pn))
            print("★C %s → portId=%s" % (pn, pid))
            if pid == -1:
                continue
            cam.setPositionLBR(Vec(CAL_L, 0.0, 0.0), Anim(2.0), pid)
            cam.setOrientationSmoothXYZR(Vec4(CAL_L + 180.0, 0.0, 0.0, 1.0), Anim(2.0), pid)
            print("★C [%s] 적용 — 5초 관찰 (위치? Sky View 유지?)" % pn)
            sleep(5.0)
        except Exception as e:
            print("★C %s 실패: %s" % (pn, repr(e)[:50]))
except Exception as e:
    print("★C 프로브 실패:", repr(e)[:80])

print(">>> v9 끝! A/B/C(포트별) 중 '중앙 + Sky View 유지'인 것은? 알려줘!")

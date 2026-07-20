# -*- coding: utf-8 -*-
"""
eclipse_2026_v6.py — [v6] 틸트 방향 보정 사다리 — 한 방에 확정하자
====================================================================
실측 타임라인:
  T=0   : 태양(고도11°) = 가장자리 (축=천정, 태양은 축에서 79°)
  T=11  : 정확히 가장자리 (79+11=90° — 축이 태양 '반대쪽'으로 기움!)
  T=79  : 화면 밖 (더 밀려남)
→ 결론 가설: setTarget(az, T) 는 az 반대쪽으로 기우는 축. 태양을 중앙에 놓으려면
  **방위를 180° 뒤집어** setTarget(az+180, 90-h).

정지된 개기식에서 후보 A~D 를 6초 간격 시연 — 어느 것이 중앙(또는 가장 가까운지)만 알려줘!
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_TOTAL     = (18, 29)
SUN_AZ, SUN_ALT = 285.5, 11.0

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 준비: 리셋 + 관측지 + 개기식 시각 고정 ───────────────────
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

uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(3.0)
print(">>> 보정 사다리 시작 — 각 단계에서 일식 위치(중앙/중간/가장자리/밖)를 기억해줘!")

AZ_FLIP = (SUN_AZ + 180.0) % 360.0
TILT    = 90.0 - SUN_ALT

# ★A 본명 가설: 방위 뒤집기 + 90-h
print("★A setTarget(az=%.0f(=태양+180), T=%.0f)" % (AZ_FLIP, TILT))
cam.setTarget(Vec2(AZ_FLIP, TILT), Anim(3.0)); sleep(6.0)

# ★B 뒤집기 + 얕은 틸트 (과보정 대비)
print("★B setTarget(az=%.0f, T=60)" % AZ_FLIP)
cam.setTarget(Vec2(AZ_FLIP, 60.0), Anim(2.5)); sleep(5.5)

# ★C 뒤집기 + 중간
print("★C setTarget(az=%.0f, T=40)" % AZ_FLIP)
cam.setTarget(Vec2(AZ_FLIP, 40.0), Anim(2.5)); sleep(5.5)

# ★D 원래 방위 + 음수 틸트 (반대 부호 변형)
print("★D setTarget(az=%.0f(태양 방위), T=-%.0f)" % (SUN_AZ, TILT))
try:
    cam.setTarget(Vec2(SUN_AZ, -TILT), Anim(2.5))
except Exception as e:
    print("★D 실패:", repr(e)[:60])
sleep(5.5)

# 마무리: A 로 복귀 후 FOV 확인
print("★E A 재적용 + FOV 60 — 최종 확인")
cam.setTarget(Vec2(AZ_FLIP, TILT), Anim(2.5)); sleep(3.5)
try:
    cam.setZoomFov(60.0, Anim(3.0)); sleep(5.0)
    cam.setZoomFov(180.0, Anim(2.5)); sleep(3.0)
except Exception:
    pass

print(">>> v6 끝! A/B/C/D 중 일식이 '돔 중앙'에 온 것은? (없으면 각각 어디였는지) "
      "+ 각 단계 HUD Target 값도 알려주면 공식 확정 가능!")

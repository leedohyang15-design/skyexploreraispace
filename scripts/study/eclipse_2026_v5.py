# -*- coding: utf-8 -*-
"""
eclipse_2026_v5.py — [v5 완성 후보] 개기일식 풀 쇼 — 90-h 틸트 공식 적용
====================================================================
v4 실측: Sky View 트랙볼 동작 / setTarget 의 2번째 값 = 돔 '틸트각' (천체 고도 아님!)
        / 줌 락은 지상뷰 무반응 / FOV 줌 동작
→ 핵심 공식: 고도 h 천체를 돔 중앙에 = setTarget(Vec2(az, 90-h))
   태양(고도 11°) → 틸트 79°. 가속 중엔 태양이 흐르니 2초마다 따라감.

흐름: 암전(관측지+시각+조준 완료) → 페이드인: 부분식이 돔 중앙 →
      시간 가속(태양 추적) → 개기식 FOV 클로즈업 → 와이드 복귀
확인: (a)부분식이 돔 중앙? (b)가속 중 중앙 유지? (c)개기식 코로나 클로즈업?
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0                  # 실측: DefaultTimeZone = UTC
UTC_START     = (17, 40)           # 부분식
UTC_TOTAL     = (18, 29)           # 개기식
ACCEL_SEC     = 40.0
AZ0, ALT0     = 277.0, 17.5       # 부분식 때 태양 방위/고도 (근사)
AZ1, ALT1     = 285.5, 11.0       # 개기식 때
FOV_WIDE      = 180.0
FOV_CLOSE     = 30.0

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

def aim(cam, az, alt, dur):        # ★ v4 공식: 돔 중앙 = 틸트 90-고도
    cam.setTarget(Vec2(az, 90.0 - alt), Anim(dur))

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

# ── 1) 시각 = 부분식 (확정 패턴: stop → set → JD 검증/보정) ───
dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
want = expected_jd(UTC_START)
for attempt in (1, 2, 3):
    day, hh, mm = local(UTC_START)
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 8, day, hh, mm, 0, tz, Anim(0.5))
    sleep(1.5)
    err_h = (dm.julianDate - want) * 24.0
    if abs(err_h) < 0.2:
        print("★1 JD OK (시도%d)" % attempt)
        break
    TZ_OFFSET -= int(round(err_h))

# ── 2) 콘텐츠 + 일식 API ─────────────────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
sun_obj = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun_obj.setIntensity(1.0, Anim(0.0))
moon = Satellite(Satellite.SatelliteName.Moon)
moon.setIntensity(1.0, Anim(0.0))
for obj in (Planet(Planet.PlanetName(2)), moon):
    for api in ("setEclipseShapeIntensity", "setPenumbraBeforeLineIntensity",
                "setPenumbraBeforeAreaIntensity", "setPenumbraAfterLineIntensity",
                "setAntumbraLineIntensity", "setAntumbraAreaIntensity"):
        try:
            getattr(obj, api)(1.0, Anim(0.0))
        except Exception:
            pass

# ── 3) 조준: 부분식 태양을 돔 중앙에 (암전 속) ─────────────────
cam = Camera(Camera.CameraName.MainCamera)
aim(cam, AZ0, ALT0, 2.5)
print("★3 조준: az=%.0f, 틸트=%.0f (= 90-%.0f)" % (AZ0, 90 - ALT0, ALT0))
for _ in range(15):                              # 슬루 동안 암전 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

# ── 4) 페이드인: 부분식이 돔 중앙에! ─────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인 — (a) 부분식(이지러진 태양)이 돔 중앙인지!")
sleep(5.0)

try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("2026. 8. 12 개기일식 — 스페인 사라고사")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.04)
    txt.setColor(Vec(1.0, 0.85, 0.6)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass
sleep(2.0)

# ── 5) 시간 가속 + 태양 추적 (2초마다 az/alt 보간 조준) ────────
day2, hh2, mm2 = local(UTC_TOTAL)
jd0 = dm.julianDate
print("★5 가속 %.0f초 + 태양 추적" % ACCEL_SEC)
dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
steps = int(ACCEL_SEC / 2)
for i in range(1, steps + 1):
    f = i / float(steps)
    aim(cam, AZ0 + (AZ1 - AZ0) * f, ALT0 + (ALT1 - ALT0) * f, 1.8)
    sleep(2.0)
sleep(1.0)
print("★5 Δ=%.4f일 — (b) 가속 중 태양이 중앙에 있었는지!" % (dm.julianDate - jd0))

# ── 6) 개기식 클로즈업 ───────────────────────────────────────
aim(cam, AZ1, ALT1, 1.5); sleep(2.0)
print(">>> 개기식! FOV %.0f→%.0f — (c) 코로나 클로즈업!" % (FOV_WIDE, FOV_CLOSE))
cam.setZoomFov(FOV_CLOSE, Anim.cubic(5.0))
sleep(10.0)
cam.setZoomFov(FOV_WIDE, Anim(4.0))
sleep(4.5)

print(">>> v5 끝! (a)부분식 중앙? (b)가속 중 유지? (c)코로나 클로즈업? — 알려줘!")

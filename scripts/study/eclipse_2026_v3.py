# -*- coding: utf-8 -*-
"""
eclipse_2026_v3.py — [v3] 태양을 돔 중앙으로: 줌 락(setZoomPosition) 투입
====================================================================
v2 결과: 시간 시스템 완전 확정(JD 1발 OK, Δ=0.0340 정확) + 코로나 렌더링 확인!
남은 문제: 태양 고도 12° = 돔 투영에서 가장자리 (cmd295 는 Sky View 돔 방향 못 틈)

v3 해법 = **줌 락** (말머리·달에서 검증된 '엔진이 중앙 자동 유지'):
  setZoomFormula(GreatCircle) → setZoomPosition(Vec(0,0,0), 태양포트, Anim, XYZ)
  → 이후 setZoomFov 로 줌인/아웃만 하면 태양이 항상 화면 중앙.
  ※ Place2D 지상뷰에서 줌 락이 먹는지가 이번 실험 포인트!

확인해줘: (a)태양(일식)이 돔 중앙으로 왔는지 (b)가속 중에도 중앙 유지됐는지
          (c)개기식 클로즈업(코로나)이 크게 보였는지
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0             # v2 실측: DefaultTimeZone = UTC
UTC_START     = (17, 40)
UTC_TOTAL     = (18, 29)
ACCEL_SEC     = 40.0
FOV_WIDE      = 100.0         # 부분식 감상 화각
FOV_CLOSE     = 25.0          # 개기식 클로즈업

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

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

# ── 1) 날짜 (v2 확정 패턴: stop 먼저 + JD 검증 + 자동 보정) ───
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
        print("★1 JD OK (시도%d, TZ=%d)" % (attempt, TZ_OFFSET))
        break
    TZ_OFFSET -= int(round(err_h))
    print("★1 JD 오차 %+.1fh → TZ=%d 재시도" % (err_h, TZ_OFFSET))

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

# ── 3) ★★ 줌 락: 태양을 화면(돔) 중앙에 자동 유지 ─────────────
cam = Camera(Camera.CameraName.MainCamera)
sun_port = sun_obj.portId(IndividualStar.IndividualStarPort.Ecliptic)
try:
    cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
    cam.setZoomPosition(Vec(0.0, 0.0, 0.0), sun_port, Anim(2.0), Camera.PositionMode.XYZ)
    print("★3 줌 락 ON (태양 포트 %s) — 태양이 돔 중앙으로 오는지!" % sun_port)
except Exception as e:
    print("★3 줌 락 실패:", repr(e)[:80])
try:
    cam.setZoomFov(FOV_WIDE, Anim(2.0))         # 화각도 미리 조여둠 (저고도 보정)
except Exception as e:
    print("★3 FOV 실패:", repr(e)[:60])
for _ in range(15):                             # 슬루 동안 암전 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

# ── 4) 페이드인: 부분식 (태양이 중앙에 크게) ──────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인: 부분식 — 태양 위치가 (돔 중앙? 가장자리?) 알려줘")
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

# ── 5) 시간 가속 (줌 락이 태양을 계속 물고 있어야 함) ──────────
day2, hh2, mm2 = local(UTC_TOTAL)
jd0 = dm.julianDate
print("★5 가속 →%02d:%02d (%.0f초) — 줌 락 유지 확인!" % (hh2, mm2, ACCEL_SEC))
dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
sleep(ACCEL_SEC + 1.0)
print("★5 Δ=%.4f일" % (dm.julianDate - jd0))

# ── 6) 개기식 클로즈업 ───────────────────────────────────────
print(">>> 개기식! FOV %.0f→%.0f (코로나 클로즈업)" % (FOV_WIDE, FOV_CLOSE))
cam.setZoomFov(FOV_CLOSE, Anim.cubic(5.0))
sleep(10.0)
cam.setZoomFov(FOV_WIDE, Anim(3.0))
sleep(3.5)

print(">>> v3 끝! (a)태양 돔 중앙? (b)가속 중 유지? (c)코로나 크게? — 알려줘")

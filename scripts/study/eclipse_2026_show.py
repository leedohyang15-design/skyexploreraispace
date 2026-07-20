# -*- coding: utf-8 -*-
"""
eclipse_2026_show.py — [v1] 2026년 8월 12일 실제 개기일식 재현 (복합 실험)
====================================================================
진짜 이벤트: 2026-08-12 개기일식, 스페인 북부 관통 (사라고사 개기 ~18:29 UTC, 태양고도 ~12°)

이번에 처음 조합하는 것 (전부 ★프로브):
  · Place2D 관측지 + DateManager 날짜 → 특정 시간·장소의 하늘
  · ★시간 가속 = setDateTime(..., Anim(초)) — 날짜를 '애니메이션'으로 흘림
  · ★일식 전용 API = setEclipseShapeIntensity / umbra·penumbra 라인 (Planet·Satellite)
  · ★태양 조준 = cmd295(setOrientationSmoothXYZR)를 IndividualStar(Sun) 포트에
검증된 조각: 암전 클램프 / 페이드인 / FOV 줌

콘솔 ★ 줄 + (a)태양이 화면에 잡혔는지 (b)달이 태양을 가리는 게 보였는지
(c)시간 가속이 부드러웠는지(하늘이 도는 게 보임) 알려줘!
"""
from skyExplorer import *
from studio import *
from Initialization import *

# ── 파라미터 (사라고사, 스페인 — 개기식 중심선) ──────────────
LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 9            # Studio 기본 타임존이 UTC+9(한국)라 가정 — 아니면 조정
UTC_START     = (17, 40)     # 부분식 진행 중 (UTC)
UTC_TOTAL     = (18, 29)     # 개기식 (UTC)
ACCEL_SEC     = 40.0         # 부분식→개기식 49분을 몇 초에 흘릴지
SUN_AZ, SUN_ALT = 277.0, 12.0   # 조준 폴백용 추정치 (서-북서, 저고도)

def kst(utc_hm):             # UTC → Studio 로컬(가정 KST). 자정 넘으면 다음날
    h = utc_hm[0] + TZ_OFFSET
    day = 12 + (1 if h >= 24 else 0)
    return day, h % 24, utc_hm[1]

# ── 0) 리셋 + 암전 (클램프는 세팅 끝까지 유지) ───────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

# ── 1) 관측지 = 사라고사 ─────────────────────────────────────
try:
    place = Place2D(Place2D.Place2DName(0))
    place.setPosition(Vec(LAT, LON, ALT))
    print("★1 관측지 OK: 사라고사 (%.2f, %.2f)" % (LAT, LON))
except Exception as e:
    print("★1 관측지 실패:", repr(e)[:80])

# ── 2) 날짜 = 부분식 진행 중 (시간대 프로브) ─────────────────
dm = DateManager()
tzs = [n for n in dir(DateManager.TimeZone) if not n.startswith("_")]
print("★2 TimeZone 멤버(앞 12):", tzs[:12])
tz = getattr(DateManager.TimeZone, "DefaultTimeZone", None)
if tz is None and tzs:
    tz = getattr(DateManager.TimeZone, tzs[0])
day, hh, mm = kst(UTC_START)
try:
    dm.setDateTime(2026, 8, day, hh, mm, 0, tz, Anim(0.0))
    dm.stop()                                  # 시간 흐름 정지 (우리가 직접 흘림)
    print("★2 날짜 세팅: 2026-08-%02d %02d:%02d (로컬, UTC%+d 가정) / JD=%.5f"
          % (day, hh, mm, TZ_OFFSET, dm.julianDate))
except Exception as e:
    print("★2 날짜 실패:", repr(e)[:80])

# ── 3) 콘텐츠 + ★일식 전용 API 프로브 ────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
sun_obj = None
try:
    sun_obj = IndividualStar(IndividualStar.IndividualStarName.Sun)
    sun_obj.setIntensity(1.0, Anim(0.0))
    print("★3 태양 객체 OK (id=%s)" % sun_obj.id)
except Exception as e:
    print("★3 태양 객체 실패:", repr(e)[:60])

moon = None
try:
    moon = Satellite(Satellite.SatelliteName.Moon)
    moon.setIntensity(1.0, Anim(0.0))
except Exception:
    pass

for obj, oname in ((Planet(Planet.PlanetName(2)), "Earth(Planet)"), (moon, "Moon(Satellite)")):
    if obj is None:
        continue
    for api in ("setEclipseShapeIntensity", "setUmbraLineIntensity", "setUmbraAreaIntensity",
                "setPenumbraBeforeLineIntensity", "setPenumbraBeforeAreaIntensity"):
        try:
            getattr(obj, api)(1.0, Anim(0.0))
            print("★3 %s.%s(1.0) OK" % (oname, api))
        except Exception as e:
            print("   %s.%s 실패: %s" % (oname, api, repr(e)[:40]))

# ── 4) ★태양 조준 (cmd295 → 폴백 setTarget) ──────────────────
cam = Camera(Camera.CameraName.MainCamera)
aimed = False
if sun_obj is not None:
    try:
        sun_port = sun_obj.portId(IndividualStar.IndividualStarPort.Ecliptic)
        print("★4 태양 포트 id =", sun_port)
        if sun_port != -1:
            cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.5), sun_port)
            aimed = True
            print("★4 조준: cmd295 → 태양 포트 (화면에 태양이 잡혔는지!)")
    except Exception as e:
        print("★4 cmd295 실패:", repr(e)[:60])
if not aimed:
    try:
        cam.setTarget(Vec2(SUN_AZ, SUN_ALT), Anim(1.5))
        print("★4 조준 폴백: setTarget(az=%.0f, h=%.0f) — 태양이 안 보이면 값 조정" % (SUN_AZ, SUN_ALT))
    except Exception as e:
        print("★4 조준 폴백도 실패:", repr(e)[:60])

for _ in range(12):                            # 조준 슬루 동안 암전 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

# ── 5) 페이드인 — 부분식이 진행 중인 하늘 ────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인: 부분식 진행 중 (태양 일부가 가려져 있어야 함)")
sleep(5.0)

# ── 6) 자막 ─────────────────────────────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("2026. 8. 12 개기일식 — 스페인 사라고사")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.04)
    txt.setColor(Vec(1.0, 0.85, 0.6)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass
sleep(2.0)

# ── 7) ★★ 시간 가속: 부분식 → 개기식 (49분을 ACCEL_SEC초에) ──
day2, hh2, mm2 = kst(UTC_TOTAL)
jd_before = None
try:
    jd_before = dm.julianDate
    print("★7 시간 가속 시작: →%02d:%02d (로컬), %.0f초 동안" % (hh2, mm2, ACCEL_SEC))
    dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
    sleep(ACCEL_SEC + 1.0)
    print("★7 가속 끝: JD %.5f → %.5f (Δ=%.4f일 — 0.034 근처면 정상 애니메이션)"
          % (jd_before, dm.julianDate, dm.julianDate - jd_before))
except Exception as e:
    print("★7 시간 가속 실패:", repr(e)[:80])

# ── 8) 개기식 순간 — FOV 줌인 (검증된 광학 줌) ────────────────
try:
    f0 = cam.zoomFov
except Exception:
    f0 = 110.0
print(">>> 개기식! FOV 줌인 %.0f→30 (코로나/다이아몬드링이 보이는지!)" % f0)
try:
    cam.setZoomFov(30.0, Anim.cubic(5.0)); sleep(9.0)
    cam.setZoomFov(f0, Anim(3.0)); sleep(3.5)
except Exception as e:
    print("★8 FOV 줌 실패:", repr(e)[:60])

print(">>> v1 끝! (a)태양 잡힘? (b)달이 태양 가림? (c)가속 중 하늘 회전 보임? "
      "(d)개기식 어두워짐/코로나? — ★줄과 함께 알려줘")

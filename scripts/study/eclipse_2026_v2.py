# -*- coding: utf-8 -*-
"""
eclipse_2026_v2.py — [v2] 날짜 미적용 버그 수정 + 가속 중 태양 추적
====================================================================
v1 진단 (JD 로그로 확정):
  · Δ=38.05일 = 날짜 세팅이 무시되고 '오늘'에서 출발 → 38일/40초 = 화면 요동·이상한 시점
  · 범인: setDateTime "직후"의 dm.stop() 이 방금 건 날짜 모션까지 취소
    → v2: stop() 을 setDateTime "앞"으로 + JD 기대값 자동 검증(오차>0.01일이면 재시도)
  · 가속 중 태양이 프레임에서 흐르는 것 방지: 2초마다 cmd295 재조준 (스텝 오빗 트릭)

확인해줘: (a)★2 JD 검증 OK 떴는지 (b)페이드인 때 '이지러진 태양'이었는지
          (c)가속이 부드럽고 태양이 화면에 유지됐는지 (d)개기식 어두워짐/코로나
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0             # ★v1 실측: DefaultTimeZone 은 UTC 로 해석됨 (KST 아님!)
UTC_START     = (17, 40)      # 부분식 진행 중
UTC_TOTAL     = (18, 29)      # 개기식
ACCEL_SEC     = 40.0
SUN_AZ, SUN_ALT = 277.0, 12.0

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):      # 2026-08-12 UTC 기준 율리우스일 (검증용)
    # JD(2026-08-12 00:00 UT) = 2461264.5
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
print("★1 관측지: 사라고사")

# ── 1) ★날짜: stop 먼저! → 세팅 → JD 검증 + 시간대 자동 보정 ──
dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
want = expected_jd(UTC_START)
ok = False
for attempt in (1, 2, 3):
    day, hh, mm = local(UTC_START)
    dm.stop()                                   # ← 순서가 핵심: 정지 먼저 (v1 버그)
    sleep(0.3)
    dm.setDateTime(2026, 8, day, hh, mm, 0, tz, Anim(0.5))
    sleep(1.5)                                  # 적용될 시간을 줌 (stop 으로 끊지 않음!)
    got = dm.julianDate
    err_h = (got - want) * 24.0
    if abs(err_h) < 0.2:
        print("★2 JD 검증 OK (시도%d, TZ_OFFSET=%d): %.5f" % (attempt, TZ_OFFSET, got))
        ok = True
        break
    TZ_OFFSET -= int(round(err_h))              # 오차(시간)만큼 로컬 가정 자동 보정
    print("★2 JD 오차 %+.1f시간 (시도%d) → TZ_OFFSET=%d 로 보정 재시도"
          % (err_h, attempt, TZ_OFFSET))
if not ok:
    print("★2 날짜 세팅 실패 지속 — ★이 줄을 그대로 보내줘")

# ── 2) 콘텐츠 + 일식 API (v1 에서 존재 확인된 것만) ───────────
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
sun_obj = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun_obj.setIntensity(1.0, Anim(0.0))
moon = Satellite(Satellite.SatelliteName.Moon)
moon.setIntensity(1.0, Anim(0.0))

earth = Planet(Planet.PlanetName(2))
for obj in (earth, moon):
    for api in ("setEclipseShapeIntensity", "setPenumbraBeforeLineIntensity",
                "setPenumbraBeforeAreaIntensity", "setPenumbraAfterLineIntensity",
                "setAntumbraLineIntensity", "setAntumbraAreaIntensity"):
        try:
            getattr(obj, api)(1.0, Anim(0.0))
        except Exception:
            pass
print("★3 일식 API 세팅 (EclipseShape + Penumbra/Antumbra 계열)")

# ── 3) 태양 조준 (cmd295 — v1 성공 확인) ─────────────────────
cam = Camera(Camera.CameraName.MainCamera)
sun_port = sun_obj.portId(IndividualStar.IndividualStarPort.Ecliptic)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.5), sun_port)
print("★4 태양 조준 (포트 %s)" % sun_port)
for _ in range(12):
    uni.setGlobalIntensity(0.0, Anim(0.0))      # 클램프
    sleep(0.2)

# ── 4) 페이드인 — 이번엔 진짜 8/12 부분식 하늘이어야 함 ───────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인: 부분식 (태양 일부가 가려져 있는지!)")
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

# ── 5) ★시간 가속 49분/40초 + 2초마다 태양 재조준 (요동 방지) ──
day2, hh2, mm2 = local(UTC_TOTAL)               # 보정된 TZ_OFFSET 반영
jd0 = dm.julianDate
print("★7 가속: →%02d:%02d, %.0f초 (기대 Δ=%.4f일)" % (hh2, mm2, ACCEL_SEC,
      expected_jd(UTC_TOTAL) - expected_jd(UTC_START)))
dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
steps = int(ACCEL_SEC / 2)
for i in range(steps):                          # 가속 내내 태양을 화면에 유지
    cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), sun_port)
    sleep(2.0)
sleep(1.0)
print("★7 가속 끝: Δ=%.4f일 (0.034 근처 = 정상)" % (dm.julianDate - jd0))

# ── 6) 개기식 — FOV 줌인 ─────────────────────────────────────
try:
    f0 = cam.zoomFov
except Exception:
    f0 = 180.0
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), sun_port)
sleep(1.2)
print(">>> 개기식! FOV %.0f→30 줌인" % f0)
cam.setZoomFov(30.0, Anim.cubic(5.0)); sleep(9.0)
cam.setZoomFov(f0, Anim(3.0)); sleep(3.5)

print(">>> v2 끝! (a)JD 검증 OK? (b)이지러진 태양? (c)가속 부드럽고 태양 유지? "
      "(d)개기식 어두워짐/코로나? — 알려줘")

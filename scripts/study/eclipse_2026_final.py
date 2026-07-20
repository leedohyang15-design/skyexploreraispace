# -*- coding: utf-8 -*-
"""
eclipse_2026_final.py — [최종] 2026-08-12 개기일식 풀 쇼 (수동 캘리브레이션 이식)
====================================================================
사용자 수동조작 SPC 녹화 역해석으로 완성 (v1~v8 대장정):
  · 조준 = 틸트(setTargetHeight) + ★273/295 쌍★ (273 단독은 뷰 안 돎 — v7 실측)
      setPositionLBR(Vec(L,0,0), Anim, track) + setOrientationSmoothXYZR(Vec4(L+180,0,0,1), Anim, track)
  · 캘리브레이션: 개기식(태양 az285.5/alt11) 정중앙 = 틸트 79 + L = -283.85 (사용자 실측)
  · track = 런타임 cam.positionTrack (하드코딩 금지 — SPC 파일 id 와 다름)
  · 시각: DefaultTimeZone=UTC / stop→set 순서 / JD 자동 검증·보정
  · 시간 가속: setDateTime(..., Anim(40)) — 49분/40초 (Δ=0.0340 실측)

흐름: 암전(전부 세팅) → 페이드인: 부분식이 돔 중앙 → 자막 →
      가속(태양 추적: L·틸트 보간) → 개기식 FOV 클로즈업 → 와이드 복귀
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_START     = (17, 40)
UTC_TOTAL     = (18, 29)
ACCEL_SEC     = 40.0
FOV_CLOSE     = 30.0

# ★ 캘리브레이션 (사용자 수동 정중앙 상태의 실측값 — 개기식 순간)
#   추정 공식은 전부 폐기: 이 실측 한 점으로 쇼 전체를 고정한다.
#   부분식~개기식 태양 이동은 ~9° 뿐 → 시작엔 중앙 근처, 가속하며 태양이
#   '스스로 정중앙으로 걸어 들어와' 개기식을 맞음 (추적 불필요).
CAL_L         = -283.85       # 개기식 정중앙 L (사용자 실측)
CAL_TILT      = 79.0          # = 90 - 태양고도 11 (사용자 실측)

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

# ── 1) 시각 = 부분식 (확정 패턴) ─────────────────────────────
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
        print("★1 JD OK")
        break
    TZ_OFFSET -= int(round(err_h))

# ── 2) 콘텐츠 + 일식 API ─────────────────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
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

# ── 3) 조준 (암전 속): 실측 캘리브레이션 값으로 고정 ──────────
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(CAL_TILT, Anim(2.0))
sleep(2.5)
track = cam.positionTrack                      # ★ 런타임 관측자 프레임 (하드코딩 금지)
print("★3 track=%s, L=%.2f, 틸트=%.1f (실측 캘리브레이션)" % (track, CAL_L, CAL_TILT))

def aim(L, dur):                               # ★ 수동 Turn 의 스크립트 재현 (273+295 쌍)
    cam.setPositionLBR(Vec(L, 0.0, 0.0), Anim(dur), track)
    cam.setOrientationSmoothXYZR(Vec4(L + 180.0, 0.0, 0.0, 1.0), Anim(dur), track)

aim(CAL_L, 3.0)
for _ in range(18):                            # 조준 슬루 동안 암전 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

# ── 4) 페이드인: 부분식이 돔 중앙에 ──────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인 — 부분식이 돔 중앙!")
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

# ── 5) 시간 가속 — 카메라는 고정, 태양이 중앙으로 걸어 들어옴 ──
day2, hh2, mm2 = local(UTC_TOTAL)
jd0 = dm.julianDate
print("★5 가속 %.0f초 (카메라 고정 — 태양이 중앙으로 이동)" % ACCEL_SEC)
dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
sleep(ACCEL_SEC + 1.0)
print("★5 Δ=%.4f일" % (dm.julianDate - jd0))

# ── 6) 개기식: 태양이 정확히 캘리브레이션 중앙에 → FOV 클로즈업 ─
print(">>> 개기식! FOV→%.0f 클로즈업 (코로나!)" % FOV_CLOSE)
cam.setZoomFov(FOV_CLOSE, Anim.cubic(5.0))
sleep(10.0)
cam.setZoomFov(180.0, Anim(4.0))
sleep(4.5)

print(">>> 최종판 끝! (a)부분식 중앙 (b)추적 유지 (c)코로나 클로즈업 — 확인해줘!")

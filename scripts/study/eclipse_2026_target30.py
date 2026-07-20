# -*- coding: utf-8 -*-
"""
eclipse_2026_target30.py — ✅✅ 확정판(2026-07-06 사용자 최종 확인) 개기일식 쇼
====================================================================
전 요소 실측 확인 완료:
  · 자동 조준 = setTargetHeight(30) + setOrientationH(180-방위) — 수동 개입 불필요 확인
  · Target 30 = 관람 정위치 확인 / 시간가속 = setDateTime+Anim / 일식 렌더링+코로나
  · 클로즈업 = setScale ×25 (태양+달 동시, 원본 scale 읽고 복귀) — "돔 절반 코로나" 확인

지상 이벤트 쇼(특정 날짜·장소 하늘)의 표준 골격. 파라미터만 바꿔 재활용.
"""
from skyExplorer import *
from studio import *
from Initialization import *

LAT, LON, ALT = 41.65, -0.88, 200.0
TZ_OFFSET     = 0
UTC_START     = (17, 40)
UTC_TOTAL     = (18, 29)
ACCEL_SEC     = 40.0
TILT          = 30.0          # 🎯 관람 표준 (쇼 내내 불변 — 카메라 안 움직임)
CAL_H         = -283.85 + 180.0   # 조준 H ≈ 180 - 태양방위 (자동 조준 실측 확인!)
MANUAL_SEC    = 5             # 미세 조정 여유 (자동 조준 확인됨 — 안전 쿠션만)
SCALE         = 25.0          # ★ 확대 배율 (실측: 5는 미미 → 20~30 권장)
SCALE_SEC     = 5.0
HOLD_SEC      = 12.0

def local(utc_hm):
    h = utc_hm[0] + TZ_OFFSET
    return 12 + (1 if h >= 24 else 0), h % 24, utc_hm[1]

def expected_jd(utc_hm):
    return 2461264.5 + (utc_hm[0] + utc_hm[1] / 60.0) / 24.0

# ── 0) 리셋 + 관측지 + 시각(부분식) ─────────────────────────
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

# ── 1) 콘텐츠 + 일식 API ─────────────────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.0))
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

# ── 2) 🎯 틸트 30 + 자동 조준 시도 (암전 속) ─────────────────
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(TILT, Anim(2.0))
sleep(2.5)
try:
    cam.setOrientationH(CAL_H, Anim(2.5))       # ① 자동 조준 시도 (v10 후보)
    print("★2 자동 조준 시도: setOrientationH(%.2f)" % CAL_H)
except Exception as e:
    print("★2 자동 조준 불가:", repr(e)[:60])
for _ in range(15):
    uni.setGlobalIntensity(0.0, Anim(0.0))      # 클램프
    sleep(0.2)

# ── 3) 페이드인 + ② 수동 보정 시간 ───────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)
print(">>> 자동 조준 완료 (미세 조정 필요 시 %d초 안에 좌클릭 Turn)" % MANUAL_SEC)
sleep(MANUAL_SEC)

# ── 4) 자막 → 시간 가속 (카메라 불변) ────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("2026. 8. 12 개기일식 — 스페인 사라고사")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.04)
    txt.setColor(Vec(1.0, 0.85, 0.6)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass
sleep(2.0)

day2, hh2, mm2 = local(UTC_TOTAL)
jd0 = dm.julianDate
print("★4 시간 가속 %.0f초 — 개기식으로!" % ACCEL_SEC)
dm.setDateTime(2026, 8, day2, hh2, mm2, 0, tz, Anim(ACCEL_SEC))
sleep(ACCEL_SEC + 1.0)
print("★4 Δ=%.4f일" % (dm.julianDate - jd0))

# ── 5) 개기식 클로즈업 — ★스케일 확대★ (카메라 불변!) ────────
#  실측: FOV 줌은 지상 Sky View 에서 무효(비행 모드 전용 추정) + 뷰 축 기준이라 부적합.
#  대신 setScale — "겉보기 크기 확대"(공식 문서) — 로 태양+달을 같은 배율로 동시에 키움:
#  정렬 유지된 채 일식 전체가 Target 30 그 자리에서 커짐. 카메라 이동 0 = 부자연스러움 0.
# ★ 원본 scale 을 먼저 읽어둠 — 기본값이 1.0 이 아닐 수 있음(복귀 크기 이상 리포트).
#   확대도 '원본 × 배율', 복귀도 '읽어둔 원본값'으로.
def _read_scale(obj, name):
    try:
        v = float(obj.scale)
        print("★5 %s 원본 scale = %.3f" % (name, v))
        return v
    except Exception:
        print("★5 %s scale 읽기 불가 — 1.0 가정" % name)
        return 1.0

s0_sun  = _read_scale(sun, "태양")
s0_moon = _read_scale(moon, "달")

print(">>> 개기식! 태양+달 ×%.0f 확대 (%.0f초, 카메라 불변)" % (SCALE, SCALE_SEC))
try:
    sun.setScale(s0_sun * SCALE, Anim(SCALE_SEC))
    moon.setScale(s0_moon * SCALE, Anim(SCALE_SEC))
    sleep(SCALE_SEC + 0.5)
    print(">>> 코로나 감상 %.0f초" % HOLD_SEC)
    sleep(HOLD_SEC)
    print(">>> 원본 크기(%.3f/%.3f)로 복귀" % (s0_sun, s0_moon))
    sun.setScale(s0_sun, Anim(3.0))
    moon.setScale(s0_moon, Anim(3.0))
    sleep(3.5)
except Exception as e:
    print("★5 setScale 실패:", repr(e)[:80])

print(">>> 끝! (a)자동 조준만으로 태양 정면? (b)Target 30 위치 보기 좋은지? (c)클로즈업? — 알려줘")

# -*- coding: utf-8 -*-
"""
sun_analemma.py — 태양의 아날렘마 (2026-07-15, ★낮 버전 v3 — 자전 상쇄 확인됨)
★ 그 유명한 '8자 곡선': 1년 동안 매일 같은 시각(정오)에 태양 위치를 찍으면 하늘에 8자가 그려진다.
  (지구 자전축 기울기 + 타원 궤도가 만드는 무늬.)
★ 실측 확정(2026-07-15): `setMotionType(MotionAnalemma)` 가 **일일 자전 365회를 실제로 상쇄** →
  1년 가속 시 하늘이 365바퀴가 아니라 ~1바퀴(반대방향)만 돎. 그 1바퀴 = 별 배경의 연주(年周)회전(정상).
  ★★ 그래서 '낮'(대기 ON)으로 만들면 배경 별이 안 보여 그 1바퀴도 사라지고 → **정오 태양만 8자를 그림**.
  (밤 버전 v2 는 배경이 도는 게 보여 헷갈렸음. 낮으로 전환이 핵심.)
  `IndividualStar(Sun).setTrajectoryIntensity` = 궤적선(8자가 그려질 선). `Earth.setElevationScale(0)` = 지형 평탄.
★ 시점: 정오 태양은 남쪽(방위180) → `setOrientationH(0)`, 고도~53(겨울30~여름77 스윙) 중심 → `setTargetHeight(37)`.
"""

from skyExplorer import *
from studio import *
from Initialization import *
import datetime as _dt

# ── 튜닝 ────────────────────────────────────────────────────
LON, LAT, ALT = 127.49, 36.64, 200.0        # 관측지(청주)
# ⚠️ DefaultTimeZone = UTC! 청주 현지 정오(태양 남중) = 12:00 KST = 03:00 UTC.
#    (12:00 UTC 로 넣으면 21:00 KST = 한밤 → 검은 화면. v3 버그.)
#    03:30 UTC ≈ 12:30 KST ≈ 청주 태양 남중(경도 127.5는 135°E 표준자오선서 30분 서쪽).
Y0, MO0, D0, H0, MI0 = 2026, 1, 1, 3, 30     # 시작: UTC 03:30 = 청주 현지 정오(남중)
SWEEP_DAYS = 365                             # 1년(태양 아날렘마 = 8자 한 바퀴)
SWEEP_TIME = 22.0                            # 진행 연출 시간(초) — 실패(스핀) 시 고통 줄이려 짧게
VIEW_HEADING = 180.0                         # 남쪽(정오 태양)
VIEW_PITCH = 53.0                            # 청주 정오 평균 태양고도 ~53°


def _find_enum(cls, *cands, **kw):
    for n in cands:
        if hasattr(cls, n):
            return getattr(cls, n)
    sub = (kw.get("contains") or "").lower()
    pre = kw.get("prefix")
    for n in [m for m in dir(cls) if not m.startswith("__")]:
        if sub and sub in n.lower():
            print("  [auto] %s <- '%s'" % (cls.__name__, n)); return getattr(cls, n)
        if pre and n.startswith(pre):
            print("  [auto] %s <- '%s'" % (cls.__name__, n)); return getattr(cls, n)
    return None


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


print("태양 아날렘마: 관측지 → 정오 고정 → 궤적 → MotionAnalemma → 1년 진행")

# ── 0) 초기화 ───────────────────────────────────────────────
smoothReset(False)
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0)
earth = Planet(Planet.PlanetName.Earth)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
cam = Camera(Camera.CameraName.MainCamera)
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(★ 대기 ON = 낮 파란 하늘 = 배경 별 숨김 = 8자만 보임)")
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # 낮이라 어차피 안 보임 — 배경 연주회전 숨기려 0

# ── 1) 관측지 = 우리 확정 지상 패턴 (v1 실패: Place 포트 재바인딩 portId=-1) ──
#   reset 후 관측자는 이미 Place2D(0) 지상에 있음 → 위치만 세팅(재바인딩 안 함).
Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))     # (위도, 경도, 고도)

# ── 2) 남쪽 정오 태양 조준 = 확정 지상 조준(setOrientationH + setTargetHeight) ──
#   정오 태양은 남(방위 180) → H = 180-180 = 0. 고도~53 → TH = 90-53 ≈ 37.
cam.setOrientationH(0.0, Anim(0.0))
cam.setTargetHeight(37.0, Anim(0.0))

# ── 3) 날짜/시각(정오) ──────────────────────────────────────
tz = _find_enum(DateManager.TimeZone, "DefaultTimeZone", prefix="Default")
dm = DateManager()
dm.setDateTime(Y0, MO0, D0, H0, MI0, 0, tz, Anim())

# ── 4) 태양 궤적 ON + 크게 ─────────────────────────────────
feat(sun, "setTrajectoryIntensity", 1.0, Anim(0.5), label="(★ 태양 궤적선 = 8자가 그려질 선)")
feat(sun, "setScale", 3.0, label="(태양 크게)")

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 15, 0)); t1.setSize(0.033); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.9, 0.6))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.0)
t1.setText("태양의 아날렘마 — 1년, 매일 정오의 태양"); t1.setIntensity(1.0, Anim(1.2)); sleep(3.5)

# ── 5) ★★ 아날렘마 시간모드 (자전 취소) ────────────────────
_mm = _find_enum(DateManager.MotionType, "MotionAnalemma", contains="analem")
if _mm is not None:
    feat(dm, "setMotionType", _mm, label="(★ MotionAnalemma = 자전 취소)")
else:
    print("   ⚠️ MotionType.MotionAnalemma 미발견 — dir 확인 필요")

# ── 6) 지형 평탄화(안전) ────────────────────────────────────
feat(earth, "setElevationScale", 0.0, label="(지형 평탄=자전 중 지면충돌 방지)")

# ── 7) ★ 1년 진행 → 태양이 8자를 그린다 ───────────────────
t1.setText("정오의 태양이 1년 동안 8자를 그린다"); sleep(0.5)
_end = _dt.date(Y0, MO0, D0) + _dt.timedelta(days=SWEEP_DAYS)
dm.setDateTime(_end.year, _end.month, _end.day, H0, MI0, 0, tz, Anim.cubic(SWEEP_TIME)); sleep(SWEEP_TIME + 1.0)
print("   1년 진행 완료 (JD=%.3f)" % getattr(dm, "julianDate", 0.0))

t1.setText("여름엔 높이, 겨울엔 낮게 — 자전축 기울기 + 타원궤도가 만든 8자"); t1.setIntensity(1.0, Anim(1.2)); sleep(4.5)

# ── 정리 ────────────────────────────────────────────────────
t1.setText("아날렘마 — 하늘에 새겨진 1년"); t1.setIntensity(1.0, Anim(1.2)); sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(낮 v3): ①★이제 '낮 파란 하늘'인가(대기 ON) — 밤 아님 "
      "②정오 태양이 한 자리 근처에서 '8자(또는 위아래로 긴 고리)'를 그리나 — 핵심 "
      "③배경이 더는 안 도나(별 0+낮이라 연주회전 숨김) ④태양 궤적선 보이나 "
      "⑤8자가 시야에 잘 담기나(안 담기면 TargetHeight/H 조정) — 여름 태양이 천정에 붙어 위가 잘리면 알려줘")

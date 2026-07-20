# -*- coding: utf-8 -*-
"""
orbital_satellites.py — OrbitalPlace 클래스 첫 예제: 지구 둘레 인공위성 (2026-07-20, 완본 미개척)
★ Asteroid(궤도요소 렌더) 확정에 이어, OrbitalPlace = '지구 위성용' 궤도 개체(TLE 스타일 세터 보유).
  DrawableInsert 은 BrushType enum 이 Invalid 뿐이라 보류 → OrbitalPlace 가 렌더 확신 높음(Asteroid 와 같은 궤도 세터).
★ OrbitalPlace API: 위성 TLE 스타일 = `setMeanMotion`(revs/day, 단위 명확 → AU/km 모호성 회피!) + setEccentricity/
  setInclination/setAscendingNodeLongitude/setArgumentOfPeriapsis(또는 setPeriapsisLongitude)/setMeanAnomaly +
  setEpochYears/setEpochDays/setBstar. 표시 = setOrbitIntensity/setOrbitColor/setOrbitThickness + setParent.
★ 히어로 = 지구 둘레 위성 5종: ISS·허블(LEO 쌩쌩) / GPS(MEO) / 정지위성(GEO 거의 정지) / 몰니야(찌그러진 타원).
  FadeTo 지구(외부) → 풀백(R↑) → 위성 궤도들 + 시간가속(1일) = 고도별 공전속도 차이(케플러) 한눈에.
★ ⚠️ 미지수: ① 궤도가 FadeTo-지구 프레임에 뜨는지(Asteroid 는 태양 프레임서 떴음) ② setParent 대상 ③ 위성 스케일.
  → mean motion 으로 스케일 자동 결정(엔진이 케플러로 반지름 계산) = 단위 추측 회피.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def dark_clamp(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(step); t += step


# 위성: (이름, meanMotion[revs/day], ecc, incl[°], RAAN[°], argP[°], M[°], 색)
SATS = [
    ("ISS",       15.50, 0.0003, 51.6,  40.0,  60.0,  0.0,  Vec(0.4, 0.9, 1.0)),
    ("Hubble",    15.09, 0.0003, 28.5, 120.0,  90.0, 40.0,  Vec(0.9, 0.9, 0.5)),
    ("GPS",        2.005,0.001,  55.0, 200.0,  30.0, 80.0,  Vec(0.6, 1.0, 0.6)),
    ("Geostationary", 1.0027, 0.0002, 0.1,  0.0,   0.0, 120.0, Vec(1.0, 0.6, 0.4)),
    ("Molniya",    2.006, 0.74,  63.4, 280.0, 270.0,160.0,  Vec(0.9, 0.5, 0.9)),
]


# ── 무대: 우주(지구로) ──────────────────────────────────────
print("무대: 지구 둘레 인공위성 (OrbitalPlace)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))

dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 20, 0, 0, 0, tz, Anim(0.0)); sleep(0.4)

# ── FadeTo 지구(외부) ───────────────────────────────────────
h = DataManager.database().data(Data.Type.PlanetType, "Earth")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); dark_clamp(4.5); print("   FadeTo Earth")

# 지구 렌더: 그림자 OFF(전체 밝게=궤도 잘 보이게) + 대기
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setShadowStrength", 0.0, Anim(0.0), label="(그림자 OFF)")
feat(earth, "setShadowContrast", 0.0, Anim(0.0))
feat(earth, "setPlanetShineStrength", 1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))

# 풀백 + 오블리크 (GEO/몰니야 담기게 R 크게, B 오블리크)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 35.0, 12.0), Anim.cubic(3.0), -1); dark_clamp(3.2)   # B35 오블리크, R=12(지구반지름)
except Exception as e:
    print("   풀백 실패: %s" % e)
cam.setTargetHeight(30.0, Anim(0.0))

# 지구 자전축 프레임(위성 궤도 부착 대상)
earth_port = None
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        earth_port = earth.portId(getattr(Planet.PlanetPort, pn)); print("   지구 포트=%s" % pn); break
    except Exception as e:
        print("   포트 %s 실패: %s" % (pn, e))

# ── ★ 위성 OrbitalPlace 생성 + TLE 요소 ─────────────────────
made = []
for idx, (nm, mm, e, inc, raan, argp, M, col) in enumerate(SATS, start=1):
    try:
        op = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(idx))
    except Exception as ex:
        print("   OrbitalPlace(%d) 실패: %s" % (idx, ex)); continue
    if earth_port is not None:
        feat(op, "setParent", earth_port, label="(부모=지구)")
    feat(op, "setMeanMotion", mm, Anim(0.0), label="(%s MM=%.3f)" % (nm, mm))
    feat(op, "setEccentricity", e, Anim(0.0))
    feat(op, "setInclination", inc, Anim(0.0))
    feat(op, "setAscendingNodeLongitude", raan, Anim(0.0))
    feat(op, "setArgumentOfPeriapsis", argp, Anim(0.0)) or feat(op, "setPeriapsisLongitude", argp, Anim(0.0))
    feat(op, "setMeanAnomaly", M, Anim(0.0))
    feat(op, "setEpochYears", 2026.0, Anim(0.0))
    feat(op, "setBstar", 0.0, Anim(0.0))
    made.append((op, nm, col))
    print("   · %s MM=%.3f i=%.1f e=%.3f" % (nm, mm, inc, e))
sleep(0.4)   # 요소 반영 프레임 대기

for op, nm, col in made:
    feat(op, "setOrbitColor", col, Anim(0.0))
    feat(op, "setOrbitThickness", 1.5, Anim(0.0))
    feat(op, "setOrbitIntensity", 0.9, Anim(0.0))
    feat(op, "setIntensity", 1.0, Anim(0.0))

# 자막
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 55, 0)); txt.setColor(Vec(0.8, 0.95, 1.0)); txt.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("지구를 도는 수천 개의 인공위성", 4.0)
narr("낮게(ISS·허블)·중간(GPS)·높이(정지위성)", 4.5)

# ── 시간가속 → 고도별 공전속도 차이 ─────────────────────────
narr("시간을 빠르게 — 낮은 위성은 쌩쌩, 정지위성은 거의 멈춰있다", 4.5)
dm.setDateTime(2026, 7, 21, 0, 0, 0, tz, Anim(30.0)); sleep(31.0)   # +1일 = ISS 약 16바퀴, GEO 1바퀴
dm.stop()
narr("몰니야 궤도는 찌그러진 타원 — 북반구 상공에 오래 머문다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("인공위성 — 우리가 하늘에 올린 작은 달들", 4.5)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★위성 궤도(5개)가 지구 둘레에 뜨나 — 로그 'OrbitalPlace 생성/MM' 확인 "
      "②고도 차이 보이나(ISS 낮고 GEO 높고, 몰니야 찌그러진 타원) ③시간가속 때 낮은 위성 쌩쌩·GEO 거의 정지 "
      "④안 뜨면 = 궤도가 FadeTo-지구 프레임 미지원 or 스케일/부모 문제 → 로그 값 보고 조정(단위/포트)")

# -*- coding: utf-8 -*-
"""
asteroid_belt.py — Asteroid 클래스 첫 예제: 소행성대 조망 (2026-07-20, 완본 미개척 클래스)
★ 아포피스는 DB(Data)로 했지 'Asteroid 클래스' 직접은 처음. Asteroid = 궤도 6요소로 궤도/본체를 직접 그림(Comet 판박이).
★ 렌더 근거: 궤도요소 세터(setSemiMajorAxis/setEccentricity/setInclination/setLongitudeOfAscendingNode/
  setArgumentOfPeriapsis/setMeanAnomaly/setEpoch) + setOrbitIntensity/setOrbitColor/setOrbitThickness +
  setIntensity/setLabelIntensity/setLabelNameOverride/setPointerType. AsteroidName=Asteroid001~ 슬롯.
★ 히어로 = '소행성대'(화성~목성 사이): 실제 소행성 8개(세레스·베스타·팔라스…)의 궤도요소를 넣어
  태양계를 '위에서'(태양 Ecliptic 포트, B=90) 조망 → 화성·목성 궤도 사이에 소행성 띠. 시간가속으로 공전.
★ 방식 = solar_system_revolution.py(위에서 조망) + Comet(요소로 궤도) 결합. 라벨은 영문(Chart2D 교훈 — 혹시 몰라).
  ⚠️ Comet 궤도선은 '지상 전용'이었으나 행성 궤도는 태양 Ecliptic 프레임서 잘 뜸(solar_system_revolution 확인).
     Asteroid 궤도가 이 위에서-조망 프레임에 뜨는지가 이번 확인 포인트(안 뜨면 지상 시점으로).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# 실제 소행성 궤도요소: (이름, a[AU], e, i[°], Ω[°], ω[°], M[°], 색)
ASTEROIDS = [
    ("Ceres",   2.77, 0.076, 10.6,  80.3,  73.6, 291.0, Vec(0.9, 0.85, 0.7)),
    ("Vesta",   2.36, 0.089,  7.1, 103.8, 151.2, 20.0,  Vec(0.9, 0.7, 0.4)),
    ("Pallas",  2.77, 0.230, 34.8, 173.1, 310.0, 40.0,  Vec(0.6, 0.8, 0.9)),
    ("Juno",    2.67, 0.256, 13.0, 169.9, 248.0, 60.0,  Vec(0.9, 0.5, 0.5)),
    ("Hygiea",  3.14, 0.112,  3.8, 283.2, 312.0, 80.0,  Vec(0.7, 0.9, 0.7)),
    ("Eros",    1.46, 0.223, 10.8, 304.3, 178.6, 100.0, Vec(1.0, 0.6, 0.3)),
    ("Flora",   2.20, 0.156,  5.9, 110.9, 285.0, 120.0, Vec(0.8, 0.8, 1.0)),
    ("Eunomia", 2.64, 0.187, 11.8, 293.0,  98.0, 140.0, Vec(0.9, 0.9, 0.6)),
]


# ── 무대: 우주(태양계) 준비 ─────────────────────────────────
print("무대: 소행성대 조망 (Asteroid 클래스)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.8)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))

# 시작 날짜 오늘 근처 고정(요소 적용/가속 기준)
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 20, 0, 0, 0, tz, Anim(0.0)); sleep(0.4)

# ── 태양계를 '위에서' 조망 (태양 Ecliptic 포트, R=AU, B=90) ──
sp = None
for pn in ("Ecliptic",):
    try:
        sp = sun.portId(getattr(IndividualStar.IndividualStarPort, pn)); print("   태양 포트=%s" % pn); break
    except Exception as e:
        print("   포트 %s 실패: %s" % (pn, e))
if sp is not None:
    cam.setPositionLBR(Vec(0.0, 90.0, 6.0), Anim(0.0), sp)   # 위에서(B90), R=6AU(화성~목성 담김)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), sp)
    cam.setTargetHeight(30.0, Anim(0.0))                     # ★ Target 30 고정(관람 정위치 — 안 잡으면 띠가 구석/아래로 밀림)

# 참조용 행성 궤도(화성·목성) — 소행성대가 그 사이에 있음
for pnm in ("Mars", "Jupiter", "Earth"):
    try:
        p = Planet(getattr(PN, pnm))
        p.setOrbitIntensity(0.7, Anim(0.0)); p.setLabelIntensity(0.8, Anim(0.0))
    except Exception as e:
        print("   %s 궤도 실패: %s" % (pnm, e))

# ── ★ 소행성 생성 + 궤도요소 (Comet 교훈: 요소 넣고 프레임 대기) ──
made = []
for idx, (nm, a, e, inc, node, argp, M, col) in enumerate(ASTEROIDS, start=1):
    try:
        ast = Asteroid(Asteroid.AsteroidName(idx))
    except Exception as ex:
        print("   Asteroid(%d) 실패: %s" % (idx, ex)); continue
    feat(ast, "setSemiMajorAxis", a, Anim(0.0))
    feat(ast, "setEccentricity", e, Anim(0.0))
    feat(ast, "setInclination", inc, Anim(0.0))
    feat(ast, "setLongitudeOfAscendingNode", node, Anim(0.0))
    feat(ast, "setArgumentOfPeriapsis", argp, Anim(0.0))
    feat(ast, "setMeanAnomaly", M, Anim(0.0))
    feat(ast, "setLabelNameOverride", nm)
    made.append((ast, nm, col))
    print("   · %s a=%.2fAU e=%.2f i=%.1f" % (nm, a, e, inc))
sleep(0.4)   # 요소 반영 프레임 대기(Comet 함정)

# 표시 속성 (궤도선/본체/라벨)
for ast, nm, col in made:
    feat(ast, "setOrbitColor", col, Anim(0.0))
    feat(ast, "setOrbitThickness", 1.5, Anim(0.0))
    feat(ast, "setOrbitIntensity", 0.9, Anim(0.0))
    feat(ast, "setIntensity", 1.0, Anim(0.0))
    feat(ast, "setLabelIntensity", 0.7, Anim(0.0))

# 자막
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("화성과 목성 사이 — 소행성대", 4.0)
narr("수십만 개의 암석 조각이 태양을 돈다", 4.5)
narr("가장 큰 세레스·베스타·팔라스…", 4.0)

# ── ★ 시간가속 → 소행성 공전 ───────────────────────────────
narr("시간을 빠르게 — 안쪽이 빠르고 바깥이 느리다(케플러)", 4.0)
dm.setDateTime(2032, 7, 20, 0, 0, 0, tz, Anim(30.0)); sleep(31.0)   # +6년 → 벨트 여러 바퀴(주기 3~6년)
dm.stop()
narr("목성의 중력이 이 띠를 행성으로 뭉치지 못하게 막았다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("소행성대 — 태어나지 못한 행성의 잔해", 4.5)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★소행성 궤도(타원 8개)가 화성~목성 궤도 사이에 띠로 뜨나 — 로그 'Asteroid 생성/요소' 확인 "
      "②라벨(Ceres/Vesta…) 뜨나 ③시간가속 때 소행성들이 궤도를 따라 공전하나(안쪽 빠름) "
      "④궤도가 안 뜨면 = Asteroid 궤도선도 Comet 처럼 '위에서-조망' 프레임 미지원 → 지상 시점으로 바꿔볼게")

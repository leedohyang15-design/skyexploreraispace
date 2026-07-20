# -*- coding: utf-8 -*-
"""
precession.py — 세차운동: 북극성이 바뀐다 (2026-07-16, 안 쓴 SDK: MotionPrecession)
★ 지구 자전축은 팽이처럼 26,000년에 걸쳐 원을 그린다(세차). 그래서 '북극성'이 바뀐다:
  지금은 폴라리스, 기원전 3000년경엔 투반(용자리), 약 14,000년 뒤엔 직녀성(베가)이 북극성이 된다.
★ 안 쓴 코드: `DateManager.setMotionType(MotionType.MotionPrecession)` (아날렘마와 같은 계열 — 일주운동
  상쇄하고 세차만 보여줄 것으로 기대). + 자전축 시각화 `setEquatorialPoleAxisIntensity`(도는 자전축) +
  `setEclipticPoleAxisIntensity`(고정된 황도극 = 세차 원의 중심).
  ⚠️ 문서에 Planet 'Precession Date'(시간 안 흘리고 축만 이동, 정지 하늘) 명령도 있다 함 → dir 로 메서드명 프로브.
★ 시점: 지상 북쪽 하늘. 세차 원(반경 23.4°)이 담기게 북쪽 넓게.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)
stars = Stars(Stars.StarsName.StarrySky)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def star(nm):
    IN = IndividualStar.IndividualStarName
    return IndividualStar(getattr(IN, nm)) if hasattr(IN, nm) else None


# ── 무대: 지상 북쪽 밤 ──────────────────────────────────────
print("무대: 청주 북쪽 하늘, 세차운동")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 검은 하늘)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 2.0, Anim(0.0))

Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 5, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.5)
cam.setOrientationH(180.0, Anim(0.0)); cam.setTargetHeight(42.0, Anim(0.0))   # 북쪽, 세차 원 담기게

# ── ★ 지면 끄기 (하늘만) — 지난번 빠뜨림 ───────────────────
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(★ 지면 OFF)")
feat(earth, "setElevationScale", 0.0, label="(지형 평탄)")

# ── 극 표시 = '동그라미(포인터)'로 (막대/축보다 직관적, 사용자 선호) ──
#   극 포인터는 하늘의 극 '지점'을 동그라미로 찍음. 세차로 천구 북극이 이동하면 청록 동그라미가 따라 움직임.
feat(earth, "setEquatorialPolePointerIntensity", 1.0, Anim(1.0), label="(천구 북극 = 청록 동그라미)")
feat(earth, "setEclipticPolePointerIntensity", 0.9, Anim(1.0), label="(황도극 = 주황 동그라미, 세차 원 중심)")
# 세로 막대(축)는 끔
feat(earth, "setEquatorialPoleAxisIntensity", 0.0, Anim(0.0))
feat(earth, "setEclipticPoleAxisIntensity", 0.0, Anim(0.0))

# ── Planet 세차 메서드 프로브 (문서의 'Precession Date' 대안) ─
pm = [m for m in dir(earth) if any(k in m.lower() for k in ("precess", "nutat"))]
print("   [Planet 세차/장동 메서드] %s" % (pm if pm else "(없음 → MotionPrecession 로만)"))

# ── 자막 ────────────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(1, 1, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("지구의 자전축은 팽이처럼 흔들린다 — '세차운동'", 4.0)
narr("청록 동그라미 = 지금 천구 북극(자전축이 가리키는 곳)", 4.0)
narr("주황 동그라미 = 황도극 — 세차 원의 '중심'(움직이지 않는다)", 4.0)

# ── 현재 북극성 = 폴라리스 ─────────────────────────────────
polaris, vega = star("Polaris"), star("Vega")
if polaris is not None:
    feat(polaris, "setPointerIntensity", 1.0, Anim(1.0), label="(폴라리스)")
    feat(polaris, "setLabelIntensity", 1.0, Anim(1.0))
narr("지금 자전축이 가리키는 별 — 북극성 폴라리스", 4.0)
if vega is not None:
    feat(vega, "setPointerIntensity", 1.0, Anim(1.0), label="(베가)")
    feat(vega, "setLabelIntensity", 1.0, Anim(1.0))
narr("저 멀리 직녀성(베가) — 지금은 북극에서 멀다", 4.0)

# ── ★ 가속 전: 별 포인터(화살표) 끄기 — 세차 중 지랄발광 방지(라벨만 유지) ──
if polaris is not None: feat(polaris, "setPointerIntensity", 0.0, Anim(0.6), label="(폴라리스 화살표 OFF)")
if vega is not None: feat(vega, "setPointerIntensity", 0.0, Anim(0.6), label="(베가 화살표 OFF)")
sleep(0.8)

# ── ★ 세차 모션 모드 + 시간 가속(수천 년) ─────────────────
narr("14,000년을 빨리 감아보면...", 2.5)
_mm = None
for n in ("MotionPrecession",):
    if hasattr(DateManager.MotionType, n):
        _mm = getattr(DateManager.MotionType, n)
if _mm is not None:
    feat(dm, "setMotionType", _mm, label="(★ MotionPrecession)")
else:
    print("   ⚠️ MotionPrecession 미발견")
dm.stop(); sleep(0.3)
# 약 13,700년 흘려 자전축이 세차 원을 절반 돌아 베가 쪽으로
dm.setDateTime(15700, 5, 1, 13, 0, 0, tz, Anim(35.0)); sleep(36.0)
dm.stop()

narr("자전축이 원을 그리며 — 이제 북극성은 '직녀성'", 4.5)
narr("26,000년마다 하늘의 북극이 한 바퀴 — 별들의 시계", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("우리의 북극성도 영원하지 않다", 4.0)
t1.setText("세차운동 — 26,000년의 느린 원"); t1.setIntensity(1.0, Anim(1.2)); sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
if hasattr(DateManager.MotionType, "MotionDiurnal"):
    feat(dm, "setMotionType", DateManager.MotionType.MotionDiurnal, label="(모션 원복)")
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v4): ①막대 대신 '동그라미(극 포인터)'로 바꿈 — 이제 뭐가 뭔지 명확한가 "
      "②★시간가속 때 '청록 동그라미(천구 북극)가 주황 동그라미(황도극) 둘레로 이동'하나 — 세차의 핵심 "
      "③별들도 세차하며 폴라리스가 청록 동그라미(북극)에서 멀어지나 ④이제 볼만한가/완성인가")

# -*- coding: utf-8 -*-
"""
probe_orbit_spiral.py — 궤도선이 왜 나선으로 벌어지는가 (2026-08-13)

★ 배경: 천리안 쇼에서 궤도선이 **닫히지 않고 나선으로 벌어진다**. 세 번 고쳤고 세 번 다 실패했다.
    1차 "가까워서 끊긴다"(프로브 C 오진) → 2차 `setBstar`·`setEpochYears` 누락 → 3차 슬롯 0 회피 +
    시계 정지 후 생성 + 기준일 정렬. **전부 화면이 그대로였다.**
  → 추측을 그만두고 **판별 실험**을 한다. 다섯 단계가 각각 하나씩 가설을 죽인다.

★ 제일 중요한 건 A 다. **검증된 예제(orbital_satellites.py)의 코드를 그대로** 돌린다.
    A 도 나선이면 → 내 쇼의 문제가 아니다(예제가 원래 그랬거나 빌드가 바뀌었다). 거기서 끝난다.
    A 만 멀쩡하면 → B~E 가 무엇이 다른지 짚어 준다.

★ 봐야 할 것: **각 단계에서 궤도가 닫힌 원인가, 벌어지는 나선인가.** 단계마다 15초씩 멈춘다.
   그리고 **실행 로그를 통째로** 남겨 주세요 — 읽은 값(bstar/epoch/meanMotion/semiMajorAxis)이 다 찍힌다.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

# 검증된 예제의 위성 5종을 그대로 (이름, meanMotion, e, i, RAAN, argP, M, 색)
SATS = [
    ("ISS",           15.50,  0.0003, 51.6,  40.0,  60.0,   0.0, Vec(0.4, 0.9, 1.0)),
    ("Hubble",        15.09,  0.0003, 28.5, 120.0,  90.0,  40.0, Vec(0.9, 0.9, 0.5)),
    ("GPS",            2.005, 0.001,  55.0, 200.0,  30.0,  80.0, Vec(0.6, 1.0, 0.6)),
    ("Geostationary",  1.0027,0.0002,  0.1,   0.0,   0.0, 120.0, Vec(1.0, 0.6, 0.4)),
    ("Molniya",        2.006, 0.74,   63.4, 280.0, 270.0, 160.0, Vec(0.9, 0.5, 0.9)),
]

made = []


def feat(obj, fn, *args, **kw):
    label = kw.get("label", "")
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s %s: %s" % (fn, label, e))
        return False


def dark(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(step)
        t += step


def read(o, tag):
    """궤도 개체의 값을 읽어서 찍는다 — 이게 이 프로브의 절반이다."""
    out = ["   [%s]" % tag]
    for a in ("bstar", "epochYears", "epochDays", "meanMotion", "semiMajorAxis",
              "eccentricity", "inclination"):
        try:
            out.append("%s=%s" % (a, getattr(o, a)))
        except Exception as e:
            out.append("%s=(읽기실패 %s)" % (a, type(e).__name__))
    print(" ".join(out))


def clear_all():
    for o, nm, col in made:
        feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
        feat(o, "setIntensity", 0.0, Anim(0.0))
    del made[:]


# ── 무대 ────────────────────────────────────────────────────
print("=" * 60)
print("프로브: 궤도선 나선 원인 판별")
print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))

dm.stop()
sleep(0.2)
dm.setDateTime(2026, 7, 20, 0, 0, 0, tz, Anim(0.0))     # ★ 예제와 똑같은 날짜
sleep(0.4)

h = DataManager.database().data(Data.Type.PlanetType, "Earth")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger()
    dark(4.5)
    print("   FadeTo Earth")

earth.setIntensity(1.0, Anim(0.0))
for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
              ("setPlanetShineStrength", 1.0), ("setAtmosphereIntensity", 1.0)):
    feat(earth, fn, v, Anim(0.0))

# 예제와 똑같은 풀백 — ⚠️ track=-1 = **FadeTo 도킹 프레임 유지**(예제가 이 프레임에 있었다)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 35.0, 12.0), Anim.cubic(3.0), -1)
    dark(3.2)
except Exception as e:
    print("   풀백 실패: %s" % e)
cam.setTargetHeight(30.0, Anim(0.0))

ip = None
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = earth.portId(getattr(Planet.PlanetPort, pn))
        print("   지구 포트=%s" % pn)
        break
    except Exception:
        continue

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 55, 0))
txt.setColor(Vec(0.9, 0.95, 1.0))
txt.setDistance(20.0, Anim(0.0))
txt.setIntensity(1.0, Anim(0.0))


def say(s, hold=0.0):
    txt.setText(s)
    print("── %s" % s)
    if hold:
        sleep(hold)


def make(slot, nm, mm, e, inc, raan, argp, M, col, bstar=0.0, sma=None):
    """예제와 **완전히 같은 호출 순서**. sma 를 주면 meanMotion 대신 반장축으로."""
    o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(slot))
    if ip is not None:
        feat(o, "setParent", ip)
    if sma is None:
        feat(o, "setMeanMotion", mm, Anim(0.0))
    else:
        feat(o, "setSemiMajorAxis", sma, Anim(0.0))
    feat(o, "setEccentricity", e, Anim(0.0))
    feat(o, "setInclination", inc, Anim(0.0))
    feat(o, "setAscendingNodeLongitude", raan, Anim(0.0))
    feat(o, "setArgumentOfPeriapsis", argp, Anim(0.0)) or feat(o, "setPeriapsisLongitude", argp, Anim(0.0))
    feat(o, "setMeanAnomaly", M, Anim(0.0))
    feat(o, "setEpochYears", 2026.0, Anim(0.0))
    feat(o, "setBstar", bstar, Anim(0.0))
    made.append((o, nm, col))
    return o


def show_all(thick=1.5):
    sleep(0.4)
    for o, nm, col in made:
        feat(o, "setOrbitColor", col, Anim(0.0)) or feat(o, "setOrbitColor", col)
        feat(o, "setOrbitThickness", thick, Anim(0.0)) or feat(o, "setOrbitThickness", thick)
        feat(o, "setOrbitIntensity", 0.9, Anim(0.0))
        feat(o, "setIntensity", 1.0, Anim(0.0))
        read(o, nm)


# ══ A. 검증된 예제 그대로 ═══════════════════════════════════
# ★ 이 단계가 핵심이다. A 가 나선이면 내 쇼의 문제가 아니다 — 여기서 끝난다.
try:
    for idx, s in enumerate(SATS, start=1):
        make(idx, *s)
    show_all()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    say("A. 검증된 예제 그대로 (도킹 프레임 · 위성 5개)", 4.0)
    say("A — 몰니야(보라)는 타원, 나머지는 원이어야 한다", 6.0)
    say("A — 나선이면 여기서 끝. 예제 자체가 안 되는 것", 6.0)
except Exception as e:
    print("A 오류:", e)

# ══ B. 같은 궤도, 카메라만 관성 프레임(내 쇼의 구도) ════════
try:
    say("B. 카메라만 관성 프레임으로 (궤도는 그대로)", 3.0)
    dark(1.0)
    if ip is not None:
        cam.setPositionLBR(Vec(0.0, 88.0, 13.0), Anim(0.0), ip)
        feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), ip)
    dark(0.6)
    cam.setTargetHeight(30.0, Anim(0.0))
    dark(0.4)
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    say("B. 관성 프레임 · 북극 위 — A 와 모양이 같은가?", 8.0)
    say("B — A 는 원인데 B 가 나선이면 '카메라 프레임'이 범인", 7.0)
except Exception as e:
    print("B 오류:", e)

# ══ C. 정지궤도 하나만 (내 쇼가 쓰는 값 그대로) ═════════════
try:
    say("C. 정지궤도 하나만 — 내 쇼가 쓰는 값", 3.0)
    dark(1.0)
    clear_all()
    make(1, "GEO", 1.0027, 0.0002, 0.1, 0.0, 0.0, 0.0, Vec(1.0, 0.80, 0.30))
    make(2, "무덤궤도", 0.50, 0.0002, 0.1, 0.0, 0.0, 0.0, Vec(0.60, 0.60, 0.66))
    show_all(3.0)
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    say("C. 금색(정지궤도) + 회색(무덤궤도) — 쇼와 같은 구성", 9.0)
except Exception as e:
    print("C 오류:", e)

# ══ D. meanMotion 대신 semiMajorAxis 로 ════════════════════
# ⚠️ 단위 미상 — 지구반지름? km? 세 값을 다 넣어 보고 **어느 게 그럴듯한 크기로 뜨는지** 본다.
try:
    say("D. 반장축(semiMajorAxis)으로 그려 보기", 3.0)
    dark(1.0)
    clear_all()
    make(1, "sma=6.611(지구반지름?)", 0, 0.0002, 0.1, 0.0, 0.0, 0.0,
         Vec(1.0, 0.5, 0.5), sma=6.611)
    make(2, "sma=42164(km?)", 0, 0.0002, 0.1, 0.0, 0.0, 0.0,
         Vec(0.5, 1.0, 0.5), sma=42164.0)
    make(3, "sma=0.000282(AU?)", 0, 0.0002, 0.1, 0.0, 0.0, 0.0,
         Vec(0.5, 0.5, 1.0), sma=0.000282)
    show_all(2.5)
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    say("D. 셋 중 정지궤도 크기로 뜨는 게 있는가? (빨강/초록/파랑)", 9.0)
    say("D — 하나라도 닫힌 원이면 그걸로 쇼를 고친다", 6.0)
except Exception as e:
    print("D 오류:", e)

# ══ E. bstar 를 일부러 크게 — 나선의 정체 확인 ══════════════
# ★ E 가 사용자 스샷과 똑같이 생겼으면 → 나선의 원인은 확실히 bstar(감쇠)다.
#   E 가 C 와 다를 게 없으면 → bstar 는 애초에 원인이 아니었다.
try:
    say("E. bstar 를 일부러 크게 — 나선이 이것 때문인가?", 3.0)
    dark(1.0)
    clear_all()
    make(1, "bstar=0 (대조군)", 1.0027, 0.0002, 0.1, 0.0, 0.0, 0.0,
         Vec(1.0, 0.80, 0.30), bstar=0.0)
    make(2, "bstar=0.05 (일부러 크게)", 1.0027, 0.0002, 0.1, 0.0, 0.0, 0.0,
         Vec(1.0, 0.30, 0.30), bstar=0.05)
    show_all(2.5)
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    say("E. 금색(bstar 0) vs 빨강(bstar 0.05) — 모양이 다른가?", 9.0)
    say("E — 둘이 똑같으면 bstar 는 범인이 아니다", 7.0)
except Exception as e:
    print("E 오류:", e)

say("프로브 끝 — 어느 단계가 닫힌 원이었는지 + 로그 전체를 알려 주세요", 4.0)
uni.setGlobalIntensity(0.0, Anim.cubic(2.0))
sleep(2.5)
print("=" * 60)
print("프로브 종료")
print("=" * 60)

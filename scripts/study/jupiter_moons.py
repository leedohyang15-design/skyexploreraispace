# -*- coding: utf-8 -*-
"""
jupiter_moons.py — 목성과 갈릴레이 위성 (2026-07-15, 미사용 조합)
★ 1610년 갈릴레이가 망원경으로 본 그것: 목성 곁의 4개 위성(이오·유로파·가니메데·칼리스토)이
  목성을 돈다 → '모든 게 지구를 도는 게 아니다'의 증거.
★ 처음 쓰는 조합: 가스행성 도킹 + 위성(Satellite) 여러 개 동시 표시(setOrbitIntensity/Label) +
  관성 프레임 전환(위성 공전이 깔끔히 보이게) + 시간가속.
  ⚠️ 위성 이름 enum 은 dir() 로 프로브(Io/Europa/Ganymede/Callisto).
  ⚠️ 시간가속은 관성 프레임에서(동기 프레임이면 목성 자전율로 하늘이 통째 돎 — earth_rotation 교훈).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
jupiter = Planet(PN.Jupiter)
SN = Satellite.SatelliteName


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:14] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


# ── 갈릴레이 위성 이름 프로브 ───────────────────────────────
GAL = []
for nm in ("Io", "Europa", "Ganymede", "Callisto"):
    if hasattr(SN, nm):
        try:
            GAL.append((nm, Satellite(getattr(SN, nm)))); print("   위성 OK: %s" % nm)
        except Exception as e:
            print("   위성 %s 생성 실패: %s" % (nm, e))
    else:
        print("   ⚠️ SatelliteName 에 %s 없음" % nm)

# ── 무대(지상) & 인트로 ─────────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.9, 0.75))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("목성과 네 위성 — 갈릴레이의 발견"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 목성으로: reset + FadeTo (가스행성 옆 도킹 R=5) ─────────
narr("목성으로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Jupiter")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Jupiter")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
jupiter.setIntensity(1.0, Anim(0.0))
# 지형/디테일 아님 → 그림자는 목성 줄무늬 입체감에 도움되므로 유지(위상 아님)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)

# ── 풀백: 4개 위성 궤도가 다 담기게 (칼리스토 ~26 목성반지름) ─
narr("뒤로 물러나 — 네 위성이 다 보이게", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 6.0), Anim.cubic(6.0), -1); sleep(6.3)   # R 5→30
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.2)); sleep(1.3)

# ── ★ 관성 프레임 전환 (위성 공전이 깔끔히 보이게) ─────────
#   동기 프레임이면 시간가속 시 목성 자전율(10h)로 하늘이 통째 돎 → 위성 움직임이 묻힘.
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = jupiter.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim.cubic(1.5), ip); sleep(1.8)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim.cubic(1.5), ip); sleep(1.7)
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))

# ── 위성 4개 ON + 궤도선 + 라벨 + 확대 ─────────────────────
narr("이오 · 유로파 · 가니메데 · 칼리스토", 2.5)
for nm, moon in GAL:
    feat(moon, "setIntensity", 1.0, Anim(1.0), label="(%s ON)" % nm)
    feat(moon, "setOrbitIntensity", 1.0, Anim(1.5), label="(%s 궤도선)" % nm)
    feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(%s 라벨)" % nm)
    feat(moon, "setScale", 6.0, Anim(1.5), label="(%s 확대)" % nm)
sleep(2.0)

# ── ★ 시간가속: 위성이 목성을 돈다 (갈릴레이의 춤) ─────────
narr("나흘을 흘린다 — 위성들이 목성을 돈다", 2.0)
narr("이오는 1.8일에 한 바퀴, 칼리스토는 17일", 2.0)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 9, 12, 0, 0, tz, Anim(24.0)); sleep(25.0)         # +8일 → 이오 4바퀴, 칼리스토 반바퀴
dm.stop()
narr("이것이 지구가 우주의 중심이 아니라는 첫 증거였다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("네 개의 세계 — 저마다 다른 얼굴", 3.0)
t1.setText("목성 — 위성 95개를 거느린 거인"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①갈릴레이 위성 4개(Io/Europa/Ganymede/Callisto)가 생성/표시되나([위성 OK] 로그) "
      "②풀백 R=30 으로 목성+4위성 궤도가 한 화면에 담기나 ③관성 프레임 전환 됐나 "
      "④시간가속으로 위성들이 목성을 도는 게 보이나(이오 빠름/칼리스토 느림) ⑤구도/R 조정?")

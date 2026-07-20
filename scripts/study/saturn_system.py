# -*- coding: utf-8 -*-
"""
saturn_system.py — 토성계: 고리 + 위성들 (2026-07-15)
★ 목성 위성(jupiter_moons, 확정) 레시피 재활용 = 가스행성 옆 도킹 → 풀백 → 관성 프레임 → 위성 ON → 시간가속.
  차이점: ① 토성은 고리 → 풀백 때 B(틸트)를 올려 '고리면을 연다'(20→38, CLAUDE.md 확정 B20→45로 고리 개방)
         ② 위성이 많고 주기 차가 큼: 미마스 0.94일 / 타이탄 15.95일 → 시간가속 시 안쪽 빠름/타이탄 느림(케플러)
         ③ 그림자 유지 = 고리가 본체에 드리우는 '고리 그림자'가 볼거리(위상/지형 아님 → 운영 그림자OFF 규칙 예외)
  ⚠️ 관성 프레임(동기 아님)에서 시간가속해야 위성 공전이 깔끔(목성 교훈 — 동기면 토성 자전율로 하늘 통째 돎).
  ⚠️ 위성 이름 enum 은 dir() 로 프로브. 타이탄 궤도 ~20 토성반지름 → 풀백 R~28 이면 다 담김(이아페투스 59는 밖).
★ 시간: 우주(행성 프레임)라 지상 UTC 변환 불필요 — 날짜만 흐르면 됨.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
saturn = Planet(PN.Saturn)
SN  = Satellite.SatelliteName

# 토성 주요 위성(안→밖) + 공전주기(일) — 확대/케플러 설명용
MOONS = [
    ("Mimas",     0.94),
    ("Enceladus", 1.37),
    ("Tethys",    1.89),
    ("Dione",     2.74),
    ("Rhea",      4.52),
    ("Titan",    15.95),
    ("Iapetus",  79.3),
]


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


# ── 위성 프로브 ─────────────────────────────────────────────
SAT = []
for nm, per in MOONS:
    if hasattr(SN, nm):
        try:
            SAT.append((nm, per, Satellite(getattr(SN, nm)))); print("   위성 OK: %s (%.2f일)" % (nm, per))
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
t1.setColor(Vec(1.0, 0.93, 0.78))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("토성 — 고리를 두른 세계"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 토성으로: reset + FadeTo (가스행성 옆 도킹 R=5, B~20) ────
narr("토성으로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Saturn")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Saturn")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
saturn.setIntensity(1.0, Anim(0.0))
# 고리 그림자(본체에 드리움)가 볼거리 → 그림자 유지(위상/지형 아님 = 운영 그림자OFF 규칙 예외)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
narr("가스 거인 — 물에도 뜰 만큼 가볍다", 3.2)

# ── 풀백 + 고리면 열기: B 20→38, R 5→28 (타이탄 궤도 ~20 담기게) ─
narr("뒤로 물러나 고리를 연다", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, p.z * 5.6), Anim.cubic(7.0), -1); sleep(7.3)   # R 5→28, 고리면 개방
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.2)); sleep(1.3)
narr("카시니 간극 — 고리 사이의 검은 틈", 3.2)

# ── ★ 관성 프레임 전환 (위성 공전이 깔끔히 보이게) ─────────
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = saturn.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim.cubic(1.5), ip); sleep(1.8)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim.cubic(1.5), ip); sleep(1.7)
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))

# ── 위성 ON + 궤도선 + 라벨 + 확대 ─────────────────────────
narr("미마스 · 엔셀라두스 · 테티스 · 디오네 · 레아 · 타이탄", 3.0)
for nm, per, moon in SAT:
    feat(moon, "setIntensity", 1.0, Anim(1.0), label="(%s ON)" % nm)
    feat(moon, "setOrbitIntensity", 1.0, Anim(1.5), label="(%s 궤도선)" % nm)
    feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(%s 라벨)" % nm)
    feat(moon, "setScale", 8.0, Anim(1.5), label="(%s 확대)" % nm)
sleep(2.0)

# ── ★ 시간가속: 위성들이 토성을 돈다 (케플러 차등) ─────────
narr("보름을 흘린다 — 위성들이 토성을 돈다", 2.2)
narr("안쪽은 빠르게, 타이탄은 느리게", 2.2)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 15, 12, 0, 0, tz, Anim(26.0)); sleep(27.0)     # +14일 → 미마스 ~15바퀴, 타이탄 ~0.9바퀴
dm.stop()

narr("타이탄 — 짙은 대기와 메탄 호수를 가진 위성", 4.0)

# ── 정리 ────────────────────────────────────────────────────
narr("고리와 146개의 달 — 작은 태양계", 3.0)
t1.setText("토성 — 태양계에서 가장 아름다운 세계"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①위성들(미마스~타이탄, 이아페투스)이 생성/표시되나([위성 OK] 로그) "
      "②풀백 R=28 + B=38 로 고리면이 열리고 위성 궤도가 한 화면에 담기나 "
      "③고리 그림자가 본체에 보이나 ④관성 프레임 전환 됐나 "
      "⑤시간가속으로 위성들이 토성을 도나(미마스 빠름/타이탄 느림) ⑥구도/R/B 조정?")

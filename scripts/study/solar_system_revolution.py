# -*- coding: utf-8 -*-
"""
solar_system_revolution.py — 태양계 공전 (2026-07-15, 미사용 코드 중심)
★ 처음 쓰는 개념 = '공전'(revolution): 우리는 자전(setRotationSpeedScale)만 해봤고, 공전은 안 해봄.
  `Planet.setRevolutionSpeedScale(배율)` + 날짜 흐름 → 행성이 궤도를 따라 태양을 돈다.
  공전량 = 배율 × 날짜Δ(일). 안쪽 행성(수성)은 빨리, 바깥(목성)은 느리게 = 케플러 법칙이 눈에 보임.
★ 구도 = 태양계를 '위에서' (FreeFlySun 방식, 확정): 태양 Ecliptic 포트 + R(단위=AU) + B=90(황도 북극).
  ⚠️ 태양 프레임 R 단위 = AU (실측). 궤도선(setOrbitIntensity)으로 궤도를 그리고, 라벨로 행성 추적.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:16] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def sun_port():
    """태양 Ecliptic 포트 (R 단위 = AU). 포트 이름은 dir() 로도 대비."""
    for nm in ("Ecliptic", "EclipticJ2000", "Galactic"):
        try:
            enum = getattr(IndividualStar, "IndividualStarPort", None)
            if enum is not None and hasattr(enum, nm):
                pid = sun.portId(getattr(enum, nm))
                print("   태양 포트=%s" % nm); return pid
        except Exception:
            pass
    print("   ⚠️ 태양 Ecliptic 포트 실패"); return -1


# ── 무대: 우주(태양계 밖 어둠) ──────────────────────────────
print("무대 준비")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    smoothReset(False); sleep(1.8); print("   smoothReset(False)")
except Exception as e:
    print("   smoothReset 실패(%s) → reset" % e); SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))

# 행성 8개 + 궤도선 + 라벨 (라벨로 작은 점을 추적)
PLANETS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
for i in range(8):
    p = Planet(PN(i))
    p.setIntensity(1.0, Anim(0.0))
    feat(p, "setOrbitIntensity", 1.0, Anim(0.0), label="(%s 궤도선)" % PLANETS[i])
    feat(p, "setLabelIntensity", 1.0, Anim(0.0))
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.4, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.15, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 1, 0, 0, 0, tz, Anim(0.5)); sleep(1.0)

# ── 태양계를 '위에서' (태양 Ecliptic, R=AU, B=90) ───────────
R_AU = 18.0     # AU. 안쪽 행성(수성~목성 5.2AU) 잘 보이고 토성(9.5)·천왕성(19) 가장자리, 해왕성(30)은 밖.
sp = sun_port()
if sp != -1:
    try:
        cam.setTarget(Vec2(0.0, 90.0), Anim(0.0))                    # 위에서 내려다봄(황도면 정면)
        cam.setPositionLBR(Vec(0.0, 90.0, R_AU), Anim.cubic(4.0), sp); sleep(4.3)
        rlog("태양계 위에서 배치")
    except Exception as e:
        print("   배치 실패: %s" % e)
cam.setTargetHeight(90.0, Anim.cubic(1.5)); sleep(1.6)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.9, 0.7))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("태양계 — 위에서 내려다본 공전 궤도"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── ★ 공전 가속 (미사용 setRevolutionSpeedScale) ───────────
#   ⚠️ 자전처럼: 배율 먼저 걸고 → 날짜 흘림. 공전량 = 배율 × 날짜Δ(일).
narr("이제 시간을 흘린다 — 행성이 태양을 돈다", 3.0)
narr("공전 가속 = setRevolutionSpeedScale (처음 쓰는 코드)", 2.5)
SCALE = 2.0
dm.stop(); sleep(0.3)
for i in range(8):
    feat(Planet(PN(i)), "setRevolutionSpeedScale", SCALE, label="(%s ×%.0f)" % (PLANETS[i], SCALE))
sleep(0.4)
try:
    j0 = dm.julianDate
except Exception:
    j0 = 0.0
# 3년 흐름 → 배율2 = 안쪽 수성 ~25바퀴(빠름), 지구 6바퀴, 목성 0.5바퀴(느림) = 케플러 차등
narr("안쪽은 빠르게, 바깥은 느리게 — 케플러의 법칙", 1.0)
dm.setDateTime(2029, 1, 1, 0, 0, 0, tz, Anim(24.0)); sleep(25.0)
try:
    print("   공전 JD Δ=%.1f일 (배율 %.0f)" % (dm.julianDate - j0, SCALE))
except Exception:
    pass

# ── 정리: 공전 배율 원복 ────────────────────────────────────
narr("공전 속도를 원래대로", 1.5)
for i in range(8):
    feat(Planet(PN(i)), "resetRevolutionSpeedScale", label="(%s reset)" % PLANETS[i])
dm.stop()
t1.setText("태양계 — 여덟 행성의 공전"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①태양 Ecliptic 포트+R=18AU 로 태양계가 위에서 보이나(로그 posLBR R 확인) "
      "②궤도선(동심원)+행성 라벨 보이나 ③setRevolutionSpeedScale+시간가속으로 행성이 궤도를 도나 "
      "④안쪽(수성) 빠르고 바깥(목성) 느린 차등 보이나 ⑤R 조정 필요?(안쪽 크게=R↓, 다 담기=R↑ 30)")

# -*- coding: utf-8 -*-
"""
probe_ring_model.py — 직접 만든 궤도선 고리를 어느 방향으로 놓아야 하나 (2026-08-13)

★ 배경: `OrbitalPlace` 는 이 빌드에서 닫힌 원을 못 그린다(프로브 A 단계 = 검증된 예제 코드도 나선).
  → 궤도선을 **직접 구운 모델**(make_orbit_ring.py)로 바꾼다. 전파기가 없으니 나선이 될 수 없다.

★ 남은 미지수는 **딱 하나 — 고리가 적도면에 눕느냐**다.
  고리는 모델의 XY 평면에 있다. 부모 프레임(EquatorialJ2000)의 적도면과 맞는지 모른다.
  → 세 방향을 **동시에** 띄운다. 한눈에 판별된다.

    금색  HPR(0, 0, 0)     — 아무것도 안 돌린 것
    청록  HPR(0, 90, 0)    — 피치 90
    회색  HPR(90, 0, 0)    — 헤딩 90

★ 크기 검증도 같이 한다: **금색 고리를 정지궤도 반지름으로** 잡았으므로
  같이 띄운 **천리안이 그 고리 위에 얹혀 있어야** 맞다. 어긋나면 축척이 틀린 것이다.

★ 봐야 할 것
  ① 셋 중 **어느 색이 지구를 감싸는 납작한 원**으로 보이는가 (나머지는 옆으로 선 고리로 보인다)
  ② 그 원 위에 **천리안이 얹혀 있는가** (크기 확인)
  ③ 원이 **닫혀 있는가** — 당연히 닫혀야 한다. 안 닫히면 모델 자체가 잘못 구워진 것
"""

from skyExplorer import *
from studio import *
from Initialization import *

import os

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

EARTH_R_M = 6378137.0
GEO_M = 42164000.0                       # 정지궤도 반지름(미터)
GEO_R = GEO_M / EARTH_R_M                # 6.611 지구반지름
SCALE_SAT = 1.0e6
KOREA_LON = 128.2

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception:
    pass


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


def dark(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(step)
        t += step


def load(slot, fname):
    """⚠️ 폴링 — 고정 sleep 은 Loading 인 채 지나간다."""
    ins = Insert3D(Insert3D.Insert3DName(slot))
    p = os.path.join(USER, fname) if USER else fname
    ins.setModelFilename(p)
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        try:
            if "Loaded" in str(ins.loadingStatus):
                print("   ✓ %-16s Loaded  modelRadius=%s" % (fname, ins.modelRadius))
                return ins
        except Exception:
            pass
    print("   ✗ %-16s 로드 실패 (%s)" % (fname, p))
    return ins


print("=" * 60)
print("프로브: 궤도선 고리 모델 — 방향과 크기")
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
Stars(Stars.StarsName.StarrySky).setIntensity(0.4, Anim(0.0))

dm.stop()
sleep(0.2)
dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))
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
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))

ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
sp = None
for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
    try:
        sp = earth.portId(getattr(Planet.PlanetPort, nm))
        break
    except Exception:
        continue

# ── 고리 세 개를 서로 다른 방향으로 ─────────────────────────
print("-" * 60)
CASES = [
    ("ring_gold.osg", 41, Vec(0.0, 0.0, 0.0), "금색  HPR(0,0,0)"),
    ("ring_cyan.osg", 42, Vec(0.0, 90.0, 0.0), "청록  HPR(0,90,0)"),
    ("ring_gray.osg", 43, Vec(90.0, 0.0, 0.0), "회색  HPR(90,0,0)"),
]
rings = []
for fname, slot, hpr, label in CASES:
    ins = load(slot, fname)
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setScale", GEO_M, Anim(0.0))       # 반지름 1.0 모델 → 정지궤도 반지름(미터)
    feat(ins, "setOrientationHPR", hpr, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setPositionLBR", Vec(0.0, 0.0, 0.0), Anim(0.0))   # 지구 중심
    rings.append((ins, label))
    print("   · %s  scale=%.0f m" % (label, GEO_M))

# ── 크기 대조용 천리안 ──────────────────────────────────────
sat = load(45, "chollian.osg")
feat(sat, "setIntensity", 0.0, Anim(0.0))
feat(sat, "setShadowStrength", 0.0, Anim(0.0))
feat(sat, "setScale", SCALE_SAT, Anim(0.0))
feat(sat, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
feat(sat, "setParent", sp if sp is not None else ip)
feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GEO_R), Anim(0.0))

# ── 카메라: 쇼의 막5 와 같은 구도(북극 위) ──────────────────
dark(0.6)
cam.setPositionLBR(Vec(0.0, 88.0, 13.0), Anim(0.0), ip)
feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), ip)
dark(0.6)
cam.setTargetHeight(30.0, Anim(0.0))
dark(0.4)

txt = InsertText(InsertText.InsertTextName(5))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 55, 0))
txt.setColor(Vec(1.0, 1.0, 0.6))
txt.setDistance(20.0, Anim(0.0))
txt.setIntensity(1.0, Anim(0.0))


def say(s, hold=0.0):
    txt.setText(s)
    print("── %s" % s)
    if hold:
        sleep(hold)


uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.5)

# ① 하나씩 켜서 어느 게 눕는지 본다
for ins, label in rings:
    feat(ins, "setIntensity", 1.0, Anim(1.0))
    say(label, 9.0)
    feat(ins, "setIntensity", 0.0, Anim(0.8))
    sleep(1.0)

# ② 셋 다 같이 — 한눈에 비교
for ins, label in rings:
    feat(ins, "setIntensity", 1.0, Anim(1.0))
feat(sat, "setIntensity", 1.0, Anim(1.5))
say("셋 다 + 천리안 — 어느 색이 지구를 감싸는 납작한 원인가", 12.0)
say("그 원 위에 천리안이 얹혀 있는가? (크기 확인)", 10.0)

# ③ 옆에서도 본다 — 눕는 것과 서는 것이 확실히 갈린다
say("옆에서 본다", 2.0)
cam.setPositionLBR(Vec(0.0, 12.0, 15.0), Anim(6.0), ip)
feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(6.0), ip)
say("옆에서 — 적도면에 누운 고리는 이제 '선'으로 보인다", 11.0)

say("프로브 끝 — 어느 색이 정답인지 알려 주세요", 4.0)
uni.setGlobalIntensity(0.0, Anim.cubic(2.0))
sleep(2.5)
print("=" * 60)
print("프로브 종료 — 정답 HPR 을 쇼의 RING_HPR 에 넣으면 궤도선이 끝난다")
print("=" * 60)

# -*- coding: utf-8 -*-
"""
blackhole_effects.py — 효과 2/3/4 명확화 + 검증 (2026-07-09)
사용자: 히어로 구도(가)는 좋은데 ②회전 ③발광 ④틸트를 '잘 모르겠다'(너무 미묘).
→ 값을 확 키우고, 각 효과가 실제로 먹는지 로그로 검증한다.

 ② 회전: 큰 시간점프(+10일) + introspection 으로 u_simulationTime 전/후 출력(변하는지 확인).
 ③ 발광: modifyUniform u_emissiveIntensity 를 0.3 ↔ 6.0 큰 스윙(명백히 어두워졌다↔밝아짐).
 ④ 틸트: B -35 → -10 크게(블랙홀이 돔에서 확실히 내려옴).
각 효과 사이 자막으로 '지금 뭘 보는지' 안내.
"""

from skyExplorer import *
from studio import *
from Initialization import *
import re


def first_valid_port(port_enum, prefer):
    ms = [m for m in dir(port_enum) if not m.startswith("_") and not m[0].islower()
          and "Invalid" not in m]
    for pref in prefer:
        for m in ms:
            if pref.lower() in m.lower():
                return m
    return ms[0] if ms else None


def sim_time(bh):
    """introspection JSON 에서 u_simulationTime 값만 뽑아 출력."""
    try:
        bh.getIntrospection(); sleep(0.3)
        s = str(bh.instrospectionOutput)
        m = re.search(r'u_simulationTime"[^}]*?"value":"([-\d.eE+ ]+)"', s)
        return m.group(1).strip() if m else "?"
    except Exception as e:
        return "err:%s" % e


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
MODEL = "..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg"
RC = 5e-14

gport = first_valid_port(Galaxy.GalaxyPort, ("Galactic",))
pport_name = first_valid_port(Place2D.Place2DPort, ("Centered", "Galactic"))

uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.35, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2020, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

bh_place = Place2D(Place2D.Place2DName(0))
bh_place.setPosition(Vec(0.0, 0.0, 2.468542e20))
bh_place.setParent(Galaxy(Galaxy.GalaxyName.MilkyWay).portId(getattr(Galaxy.GalaxyPort, gport)))

bh = Insert3D(Insert3D.Insert3DName(0))
bh.setIntensity(1.0, Anim(0.0))
bh.setModelFilename(MODEL)
sleep(1.0)
pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
bh.setParent(pport)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 40, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))

cam.setPositionLBR(Vec(0.0, -30.0, RC), Anim(0.0), pport)
sleep(0.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("블랙홀 — 효과 확인 (가 구도)"); t1.setIntensity(1.0, Anim(1.0))
sleep(3.5)

# ══ ② 회전: 큰 시간점프 + u_simulationTime 검증 ══════════════
print("=" * 55); print("② 회전 (시간 +10일)")
print("   시간가속 전 u_simulationTime =", sim_time(bh))
t1.setText("② 원반 회전 — 시간을 10일 빠르게 (돌아가는지 보세요)")
try:
    dm.setDateTime(2020, 1, 11, 0, 0, 0, tz, Anim(14.0))     # +10일 크게
    for i in range(3):
        sleep(4.7)
        print("   진행 중 u_simulationTime =", sim_time(bh))
except Exception as e:
    print("   회전 실패: %s" % e)
print("   시간가속 후 u_simulationTime =", sim_time(bh))
print("   ★ u_simulationTime 이 크게 변했으면 회전 구동 중. 화면서 원반 도나?")
sleep(1.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.5); t1.setIntensity(1.0, Anim(0.4))

# ══ ③ 발광: 0.3 ↔ 6.0 큰 스윙 ═══════════════════════════════
print("=" * 55); print("③ 발광 (0.3 ↔ 6.0 큰 스윙)")
try:
    t1.setText("③ 발광 — 어둡게 (0.3)")
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(0.3, 0, 0, 0), Anim(2.5))
    sleep(3.0)
    t1.setText("③ 발광 — 확 밝게 (6.0)")
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(6.0, 0, 0, 0), Anim(2.5))
    sleep(3.0)
    t1.setText("③ 발광 — 원래대로 (1.0)")
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(1.0, 0, 0, 0), Anim(2.0))
    sleep(2.5)
    print("   ★ 어두워졌다 밝아지는 게 보였나?")
except Exception as e:
    print("   발광 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.5)

# ══ ④ 틸트: B -35 → -10 크게 ════════════════════════════════
print("=" * 55); print("④ 틸트 (B -35 → -10 크게)")
try:
    cam.setPositionLBR(Vec(0.0, -35.0, RC), Anim.cubic(2.0), pport); sleep(2.2)
    t1.setText("④ 틸트 — 블랙홀이 돔에서 내려옵니다"); t1.setIntensity(1.0, Anim(0.6))
    cam.setPositionLBR(Vec(0.0, -10.0, RC), Anim.cubic(8.0), pport)
    sleep(8.5)
    print("   ★ 블랙홀이 위→아래로 크게 움직였나?")
except Exception as e:
    print("   틸트 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.6)

# ── 마무리 ────────────────────────────────────────────────────
cam.setPositionLBR(Vec(0.0, -30.0, RC), Anim.cubic(3.0), pport)
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ②u_simulationTime 변화값 + 원반 회전 보임? ③발광 0.3↔6.0 보임? ④틸트 큰 이동 보임?")

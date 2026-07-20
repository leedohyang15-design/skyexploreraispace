# -*- coding: utf-8 -*-
"""
blackhole_emissive_test.py — 원반 밝기 제어법 찾기 (2026-07-09)
실측: 회전·틸트 OK, 그러나 modifyUniform("root/u_emissiveIntensity") = 밝기 변화 안 보임.
(u_emissiveIntensity 는 emissive 맵 강도라 단독으론 화면에 안 이어지는 듯.)
→ 밝기를 바꾸는 '진짜 레버'를 4후보로 테스트:
 A. setIntensity           — Insert3D 본체 밝기 (표준)
 B. setExposure            — 노출
 C. modifyUniform u_insertBrightnessContrast(vec2 밝기/대비) — introspect 에서 발견
 D. setUniform u_emissiveIntensity — modify 말고 set 로 재시도
각 후보 어둡게→밝게 스윙. 어느 게 화면 밝기를 바꾸는지 리포트.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def first_valid_port(port_enum, prefer):
    ms = [m for m in dir(port_enum) if not m.startswith("_") and not m[0].islower()
          and "Invalid" not in m]
    for pref in prefer:
        for m in ms:
            if pref.lower() in m.lower():
                return m
    return ms[0] if ms else None


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
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.3, Anim(0.0))
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
sleep(2.5)


def swing(label, dim_fn, bright_fn, reset_fn):
    print("=" * 50); print(label)
    try:
        t1.setText("%s — 어둡게" % label); t1.setIntensity(1.0, Anim(0.4))
        dim_fn(); sleep(3.0)
        t1.setText("%s — 확 밝게" % label)
        bright_fn(); sleep(3.0)
        t1.setText("%s — 원래대로" % label)
        reset_fn(); sleep(2.5)
        print("   ★ %s 로 밝기 변했나?" % label)
    except Exception as e:
        print("   %s 실패: %s" % (label, e))
    t1.setIntensity(0.0, Anim(0.4)); sleep(0.5)


# A. setIntensity
swing("A) setIntensity",
      lambda: bh.setIntensity(0.25, Anim(2.5)),
      lambda: bh.setIntensity(2.5, Anim(2.5)),
      lambda: bh.setIntensity(1.0, Anim(2.0)))

# B. setExposure
swing("B) setExposure",
      lambda: bh.setExposure(-2.0, Anim(2.5)),
      lambda: bh.setExposure(2.0, Anim(2.5)),
      lambda: bh.setExposure(0.0, Anim(2.0)))

# C. modifyUniform u_insertBrightnessContrast (vec2: 밝기, 대비)
swing("C) u_insertBrightnessContrast",
      lambda: bh.modifyUniform("root/u_insertBrightnessContrast", Vec4(-0.5, 0, 0, 0), Anim(2.5)),
      lambda: bh.modifyUniform("root/u_insertBrightnessContrast", Vec4(1.5, 0, 0, 0), Anim(2.5)),
      lambda: bh.modifyUniform("root/u_insertBrightnessContrast", Vec4(0.0, 0, 0, 0), Anim(2.0)))

# D. setUniform u_emissiveIntensity (modify 말고 set)
swing("D) setUniform u_emissiveIntensity",
      lambda: bh.setUniform("root/u_emissiveIntensity", Vec4(0.3, 0, 0, 0), Anim(2.5)),
      lambda: bh.setUniform("root/u_emissiveIntensity", Vec4(6.0, 0, 0, 0), Anim(2.5)),
      lambda: bh.setUniform("root/u_emissiveIntensity", Vec4(1.0, 0, 0, 0), Anim(2.0)))

# ── 마무리 ────────────────────────────────────────────────────
t1.setText("어느 후보가 밝기를 바꿨는지 리포트!"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: A/B/C/D 중 원반 밝기를 실제로 바꾼 후보는?")

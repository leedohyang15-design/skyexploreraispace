# -*- coding: utf-8 -*-
"""
blackhole_show_v4.py — 카메라 구도 스윕 (2026-07-09)
v3 성공: 원반 중심(R≈0)에 두니 블랙홀 보임! 단 정중앙이라 구도가 어색(원반에 파묻힘).
이번 v4: 거리·고도각을 3~4개 훑어 '멋진 초상화 구도'를 찾는다.
 원리: pport 트랙 기준 (L, B, R) 배치 = 카메라가 중심(블랙홀)을 바라봄.
       R = modelRadius × 배율(중심 밖으로), B = 고도각(원반을 위에서 비스듬히).

각 구도 6초씩 유지 — 어느 게 제일 좋은지 리포트해줘. (모델/부착은 v3 검증분 그대로)
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

gport = first_valid_port(Galaxy.GalaxyPort, ("Galactic",))
pport_name = first_valid_port(Place2D.Place2DPort, ("Centered", "Galactic"))

# ── 무대 + 모델 (v3 검증분) ──────────────────────────────────
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
R0 = bh.modelRadius
print("   modelRadius=%.0f" % R0)
pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
bh.setParent(pport)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))

# 시작: 중심 근처(보이는 것 확인) → 페이드인
cam.setPositionLBR(Vec(0.0, 0.0, R0 * 0.05), Anim(0.0), pport)
sleep(0.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.0)

# ── 구도 스윕: (L, B, R배율) 4종 ─────────────────────────────
shots = [
    ("A", 0.0,  15.0, 0.4,  "A: R=0.4배 · 고도 15° (가까이, 살짝 위)"),
    ("B", 30.0, 30.0, 0.8,  "B: R=0.8배 · 고도 30° (초상화 표준?)"),
    ("C", 0.0,  55.0, 1.2,  "C: R=1.2배 · 고도 55° (위에서 내려다봄)"),
    ("D", 90.0, 5.0,  0.6,  "D: R=0.6배 · 고도 5° (거의 옆에서=원반 에지)"),
]
for tag, L, B, f, memo in shots:
    print("=" * 50); print(memo)
    t1.setText("[%s] 구도" % tag); t1.setIntensity(1.0, Anim(0.4))
    try:
        cam.setPositionLBR(Vec(L, B, R0 * f), Anim.cubic(3.5), pport)
        sleep(4.0)
        print("   R=%.3e (배율 %.2f)" % (cam.positionLBR.z, f))
    except Exception as e:
        print("   %s 실패: %s" % (tag, e))
    sleep(2.5)
    t1.setIntensity(0.0, Anim(0.4)); sleep(0.5)

# ── 좋아보이는 구도(B)에서 시간가속 회전 + 발광 ──────────────
print("=" * 50); print("마무리: B 구도서 회전+발광")
try:
    cam.setPositionLBR(Vec(30.0, 30.0, R0 * 0.8), Anim.cubic(3.0), pport); sleep(3.2)
    t1.setText("궁수자리 A* — 회전하는 강착원반"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2020, 1, 1, 12, 0, 0, tz, Anim(10.0))
    sleep(10.5)
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(2.5, 0, 0, 0), Anim(3.0))
    sleep(3.5)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   마무리 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: A/B/C/D 중 어느 구도가 제일 블랙홀다운가? (그걸로 완성쇼 확정)")

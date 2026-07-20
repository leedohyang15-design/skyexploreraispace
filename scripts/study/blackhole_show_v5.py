# -*- coding: utf-8 -*-
"""
blackhole_show_v5.py — 몰입형: 중심에서 방향만 (2026-07-09)
확정: 이 블랙홀 모델(blackholeAccretionSharp.osg)은 **R≈0 정중앙에서만 보임**.
     v3(R=5e-14) 보임 / v4(R≥0.05배=2.4백만) 전부 안 보임 → '바깥 초상화' 불가.
     = 강착원반 '한가운데 들어가 둘러보는' 몰입형 모델. 원본 SPC 도 R≈0 에서 방향만 바꿈.
→ v5: 중심(R≈0) 고정, **바라보는 방향(L/B)만 조절**해 원반을 비스듬한 띠로 잡고 천천히 둘러봄.
       + 시간가속(u_simulationTime) 회전 + modifyUniform 발광.

리포트: 어느 방향(B 틸트)에서 원반이 제일 멋지게 잡히는지 + 둘러보기 느낌.
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
RC = 5e-14                                   # ★ 중심 R (v3 확정, 이 값에서만 보임)

gport = first_valid_port(Galaxy.GalaxyPort, ("Galactic",))
pport_name = first_valid_port(Place2D.Place2DPort, ("Centered", "Galactic"))

# ── 무대 + 모델 (검증분) ─────────────────────────────────────
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
print("   modelRadius=%.0f" % bh.modelRadius)
pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
bh.setParent(pport)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))

# 중심 진입 (첫 방향 B=20 틸트)
cam.setPositionLBR(Vec(0.0, 20.0, RC), Anim(0.0), pport)
sleep(0.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("강착원반 한가운데 — 궁수자리 A*"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.5)

# ── 방향(B 틸트) 스윕: R 은 중심 고정, B 만 바꿔 원반 각도 찾기 ─
print("=" * 50); print("틸트 스윕 (R 중심 고정, B만)")
for tag, B, memo in [("가", -30.0, "아래로 (원반을 올려다봄)"),
                     ("나", 0.0,   "수평 (원반 에지)"),
                     ("다", 35.0,  "위로 (원반을 내려다봄)")]:
    t1.setText("[%s] 시선 %s" % (tag, memo)); t1.setIntensity(1.0, Anim(0.4))
    try:
        cam.setPositionLBR(Vec(0.0, B, RC), Anim.cubic(3.0), pport)
        sleep(3.5)
    except Exception as e:
        print("   %s 실패: %s" % (tag, e))
    sleep(1.5)
    t1.setIntensity(0.0, Anim(0.4)); sleep(0.4)

# ── 천천히 360° 둘러보기 (L 회전) + 시간가속 원반 회전 ──────
print("=" * 50); print("둘러보기 + 시간가속")
try:
    cam.setPositionLBR(Vec(0.0, 15.0, RC), Anim.cubic(2.0), pport); sleep(2.2)
    t1.setText("사방을 둘러싼 백만 도의 소용돌이"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2020, 1, 1, 18, 0, 0, tz, Anim(20.0))       # 원반 회전(u_simulationTime)
    # 동시에 L 을 천천히 돌려 둘러봄
    for i in range(1, 9):
        cam.setPositionLBR(Vec(i * 45.0, 15.0, RC), Anim(2.4), pport)
        sleep(2.5)
    print("   ★ 둘러보기+원반회전 됐나?")
    t1.setIntensity(0.0, Anim(0.8)); sleep(0.5)
except Exception as e:
    print("   둘러보기 실패: %s" % e)

# ── 발광 펄스 ────────────────────────────────────────────────
try:
    t1.setText("빛나는 죽음의 소용돌이"); t1.setIntensity(1.0, Anim(0.8))
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(2.5, 0, 0, 0), Anim(3.0))
    sleep(3.5)
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(1.0, 0, 0, 0), Anim(2.0))
    sleep(2.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   발광 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: 가/나/다 틸트 중 원반이 제일 멋진 각도 + 둘러보기 느낌")

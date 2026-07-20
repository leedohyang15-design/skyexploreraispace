# -*- coding: utf-8 -*-
"""
blackhole_final.py — 블랙홀 완성쇼 (2026-07-09, 전 파라미터 확정 통합)
v1~effects 전체 여정으로 확정한 것 총집합:
 · Insert3D 강착원반 모델(blackholeAccretionSharp.osg) = 몰입형(R≈0 중심에서만 보임).
 · ★ 구도 = 가(B=-30): 블랙홀 링이 돔 상단 중앙에 완벽(인터스텔라 룩). RC=5e-14→R≈19440km.
 · 포트: Galaxy=Galactic / Place2D=CenteredPort (실측).
 · ② 회전 = 시간가속(u_simulationTime 구동) — 실측 동작.
 · ③ 발광 = **setIntensity**(Insert3D 본체 밝기). ⚠️ modifyUniform("u_emissiveIntensity")는 무효(실측).
 · ④ 틸트 = B 이동(중력렌즈 강조) — 실측 동작.

구성(약 1분 20초): 히어로 홀드 → 원반 회전 → 발광 펄스 → 중력렌즈 틸트 → 피날레.
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

# ── 무대 + 모델 ──────────────────────────────────────────────
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
print("   modelRadius=%.0f loadingStatus=%s" % (bh.modelRadius, bh.loadingStatus))
pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
bh.setParent(pport)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 40, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))

# ── 히어로 홀드 (가 구도 B=-30) ──────────────────────────────
cam.setPositionLBR(Vec(0.0, -30.0, RC), Anim(0.0), pport)
sleep(0.5)
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("궁수자리 A* — 우리은하 중심의 초대질량 블랙홀"); t1.setIntensity(1.0, Anim(1.5))
print(">>> ① 히어로 홀드 (7초)")
sleep(7.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ② 원반 회전 (시간가속) ───────────────────────────────────
print(">>> ② 원반 회전 (시간가속)")
t1.setText("강착원반 — 빨려드는 물질이 마찰로 백만 도까지"); t1.setIntensity(1.0, Anim(0.8))
try:
    dm.setDateTime(2020, 1, 11, 0, 0, 0, tz, Anim(16.0))     # +10일을 16초에 = 원반 회전
    sleep(16.5)
except Exception as e:
    print("   회전 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.7)); sleep(0.6)

# ── ③ 발광 펄스 (setIntensity) ───────────────────────────────
print(">>> ③ 발광 펄스 (setIntensity)")
t1.setText("사건의 지평선 — 빛조차 탈출 못 하는 경계"); t1.setIntensity(1.0, Anim(0.8))
try:
    bh.setIntensity(0.3, Anim(2.5)); sleep(3.0)              # 어둡게
    bh.setIntensity(2.5, Anim(2.5)); sleep(3.0)              # 확 밝게
    bh.setIntensity(1.0, Anim(2.0)); sleep(2.2)              # 원래대로
except Exception as e:
    print("   발광 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.7)); sleep(0.6)

# ── ④ 중력렌즈 틸트 (B -30 → -15) ────────────────────────────
print(">>> ④ 중력렌즈 틸트")
t1.setText("빛이 휘어지는 곳 — 중력렌즈"); t1.setIntensity(1.0, Anim(0.8))
try:
    cam.setPositionLBR(Vec(0.0, -15.0, RC), Anim.cubic(8.0), pport)
    sleep(8.5)
    cam.setPositionLBR(Vec(0.0, -30.0, RC), Anim.cubic(4.0), pport)   # 히어로 구도 복귀
    sleep(4.2)
except Exception as e:
    print("   틸트 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.7)); sleep(0.6)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("블랙홀 완성쇼 종료 — 히어로 구도 + 회전 + 발광 + 렌즈 틸트 (전 파라미터 통합).")

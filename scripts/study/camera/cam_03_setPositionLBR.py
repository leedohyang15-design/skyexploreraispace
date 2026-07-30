# -*- coding: utf-8 -*-
# [카메라 03] setPositionLBR — 프레임 내 카메라 위치(L경도/B위도/R거리).
# 되는 곳: ② 행성/우주 프레임. 🛑 지상 Sky View 금지(관측자 이탈).
# 규칙: track 필수(최소 -1), R단위=트랙 대상 반지름(km 아님), 절대값 금지=읽은값 기준.
# 데모: 토성 옆도킹 후 L(경도)로 옆에서 한 바퀴 돌고, B(위도)로 위에서 내려다본다.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
sleep(4.5)
sat = Planet(Planet.PlanetName.Saturn)
sat.setShadowStrength(0.0, Anim(0.0)); sat.setShadowContrast(0.0, Anim(0.0)); sat.setPlanetShineStrength(1.0, Anim(0.0))
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)

p = cam.positionLBR
print("도킹 위치 L=%.1f B=%.1f R=%.3f" % (p.x, p.y, p.z))
# L(경도) 스윕 = 옆에서 공전하듯 한 바퀴
for dL in [60.0, 120.0, 180.0]:
    cam.setPositionLBR(Vec(p.x + dL, p.y, p.z), Anim.cubic(3.0), -1)
    print("  L +%.0f (옆에서 돌기)" % dL); sleep(3.5)
# B(위도) = 위에서 내려다보기 (고리면 개방)
cam.setPositionLBR(Vec(p.x + 180.0, 55.0, p.z), Anim.cubic(3.0), -1)
print("  B=55 (위에서 내려다봄)"); sleep(3.5)
print("완료 — L=옆으로 돌기 / B=위아래 각도 / R=거리. track=-1=현프레임 유지.")

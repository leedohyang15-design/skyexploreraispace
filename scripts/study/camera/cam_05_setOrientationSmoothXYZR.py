# -*- coding: utf-8 -*-
# [카메라 05] setOrientationSmoothXYZR — 프레임 전환 직후 '시선 정렬'(필수).
# 되는 곳: 프레임을 새 포트로 옮긴 직후 반드시. 안 하면 시점이 뒤틀림("시점 병신").
# 데모: 토성 FadeTo(동기프레임) → 관성프레임(EquatorialJ2000)으로 전환 + 시선정렬.
#   같은 L/B/R 유지 → 카메라 안 움직이고 프레임만 바뀜(그래서 정렬을 붙여야 함).
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
sleep(4.5)
sat = Planet(Planet.PlanetName.Saturn)
sat.setShadowStrength(0.0, Anim(0.0)); sat.setShadowContrast(0.0, Anim(0.0)); sat.setPlanetShineStrength(1.0, Anim(0.0))
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.5)

p = cam.positionLBR
ip = sat.portId(Planet.PlanetPort.EquatorialJ2000)   # 관성(별 고정) 프레임
print("관성 프레임으로 전환 + 시선 정렬 (같은 L/B/R 유지 → 위치 불변)")
cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(2.0), ip)                 # ① 프레임만 갈아탐
cam.setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim(2.0), ip)           # ② ★ 시선 정렬(필수)
sleep(3.0)
print("완료 — 정렬 붙였으니 시점 안 뒤틀림. (이 상태서 setRotationSpeedScale+시간가속=행성 자전)")

# -*- coding: utf-8 -*-
# [카메라 04] setPositionR — 대상까지 '거리'만 변경(줌인/풀백).
# 되는 곳: ② 행성/우주 프레임. 🛑 지상·성단(고정투영) 무효.
# 규칙: 절대값 금지! 'p=cam.positionLBR' 읽어서 p.z × 배율. (<1=줌인, >1=풀백)
# 데모: 토성 도킹 후 절반씩 줌인(×0.5) 두 번 → 크게 풀백(×8).
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

for factor, label in [(0.5,"줌인 ×0.5"), (0.5,"줌인 ×0.5 또"), (8.0,"풀백 ×8")]:
    p = cam.positionLBR                         # ★ 매번 현재값 다시 읽기
    newR = p.z * factor
    print("%s : R %.3f → %.3f" % (label, p.z, newR))
    cam.setPositionR(newR, Anim.cubic(4.0), -1); sleep(4.5)
print("완료 — 거리 줌은 항상 '읽은값×배율'. 절대값(예 setPositionR(3)) 넣으면 프레임마다 튄다.")

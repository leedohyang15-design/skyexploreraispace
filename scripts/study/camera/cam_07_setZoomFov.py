# -*- coding: utf-8 -*-
# [카메라 07] setZoomFov — 광학 FOV 줌(카메라 안 움직이고 화각만 좁힘).
# 되는 곳: ② 우주/행성 뷰. 🛑 지상 Sky View 무효.
# 데모: 목성 도킹 후 화각 110→60→110 (렌즈 줌처럼 확대/축소).
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
DataManager.database().data(Data.Type.PlanetType, "Jupiter").action(Action.Type.FadeTo).trigger()
sleep(4.5)
jup = Planet(Planet.PlanetName.Jupiter)
jup.setShadowStrength(0.0, Anim(0.0)); jup.setShadowContrast(0.0, Anim(0.0)); jup.setPlanetShineStrength(1.0, Anim(0.0))
sleep(1.0)

for fov in [110.0, 60.0, 90.0, 110.0]:
    print("setZoomFov(%.0f)" % fov)
    cam.setZoomFov(fov, Anim.cubic(3.0)); sleep(3.5)
print("완료 — FOV 좁히면 확대(광학줌). 카메라 위치는 그대로. ⚠️ 지상에선 무효라 setScale 써야 함.")

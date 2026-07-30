# -*- coding: utf-8 -*-
# [카메라 01] setOrientationH — 지상 Sky View 좌우 조준 (H = 180 − 천체방위)
# 되는 곳: ① 지상 Sky View 전용. 안 되는 곳: 우주/행성 프레임(의미 달라짐).
# 데모: 남(H=0) → 동(H=90) → 북(H=180) 으로 밤하늘을 돌려본다.
from skyExplorer import *
from studio import *
from Initialization import *

dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)

cam.setTargetHeight(30.0, Anim(0.0))         # 틸트는 관람표준 30 고정
for H, name in [(0.0,"남"), (90.0,"동"), (180.0,"북"), (-90.0,"서")]:
    print("setOrientationH(%.0f) = %s쪽 하늘" % (H, name))
    cam.setOrientationH(H, Anim.cubic(3.0)); sleep(4.0)
print("완료 — 방위가 남→동→북→서로 돌았다. (특정 천체 조준 = H=180−그 천체 방위)")

# -*- coding: utf-8 -*-
# [카메라 02] setTargetHeight — 돔 틸트(Target). 천체 고도가 아니라 '돔 기울기'.
# 되는 곳: 전 프레임. 값 의미: 0=전천(가장자리) / 30=관람표준 / 90=천정 클로즈업.
# 데모: 0 → 30 → 90 으로 돔을 젖혀본다.
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
cam.setOrientationH(0.0, Anim(0.0))

for t, desc in [(0.0,"전천(지평선까지, 그리드용)"), (30.0,"관람 표준"), (90.0,"천정(머리 위)")]:
    print("setTargetHeight(%.0f) = %s" % (t, desc))
    cam.setTargetHeight(t, Anim.cubic(3.0)); sleep(4.0)
print("완료 — 돔 틸트 0/30/90. ⚠️ 같은 값 재호출은 no-op(재조준은 29.9→30 지글로).")

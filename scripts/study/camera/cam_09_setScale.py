# -*- coding: utf-8 -*-
# [카메라 09] obj.setScale — 개체 자체를 키움(위치줌/FOV줌이 안 되는 데서).
# 되는 곳: 지상 클로즈업(태양·달·코로나), 성단 내부. 규칙: orig 먼저 읽고 orig×배율(절대값 금지).
# 데모: 지상 밤하늘의 달을 원본×20 으로 크게(지상은 위치줌 무효라 이게 유일한 확대).
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
Stars(Stars.StarsName.StarrySky).setIntensity(0.8, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 3, 5, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)  # 보름 근처 밤

moon = Satellite(Satellite.SatelliteName.Moon)
moon.setIntensity(1.0, Anim(0.0))
try: orig = moon.scale            # ★ 원본 먼저 읽기
except Exception: orig = 1.0
print("달 원본 scale =", orig)
# 달 쪽으로 대충 조준(방위는 날짜별로 다르니 동쪽 근처)
cam.setOrientationH(90.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0)); sleep(1.5)

for f in [5.0, 12.0, 20.0]:
    print("setScale(원본 × %.0f)" % f)
    moon.setScale(orig * f, Anim.cubic(3.0)); sleep(3.5)
moon.setScale(orig, Anim(2.0))   # 복귀는 읽어둔 원본으로
print("완료 — 지상은 setScale 로만 확대(×5는 미미, ×20 체감). 복귀=원본값(1.0 하드코딩 금지).")

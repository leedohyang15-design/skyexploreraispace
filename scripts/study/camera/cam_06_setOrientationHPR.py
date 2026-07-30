# -*- coding: utf-8 -*-
# [카메라 06] setOrientationHPR — 시선축 회전. Vec(Heading, Pitch, Roll).
# 되는 곳: ③ 성운/성단 내부 회전(위치 무효인 고정투영). 지상서도 '뷰 롤'로 확인 가능.
# 핵심: H=좌우팬 / P=위아래 / R(★셋째값)=Roll=시선축 팽이 스핀. 진짜 '회전'은 R+360.
# 데모: 밤하늘을 시선축 중심으로 360° 굴려본다(별밭이 팽이처럼 돎).
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
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))     # 은하수 있으면 롤이 잘 보임
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(90.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0)); sleep(1.0)

try:
    o = cam.orientationHPR; H, P, R = o.x, o.y, o.z
except Exception:
    H, P, R = 90.0, 0.0, 0.0
print("현재 HPR=(%.0f,%.0f,%.0f) → Roll(셋째값) +360 스핀" % (H, P, R))
cam.setOrientationHPR(Vec(H, P, R + 360.0), Anim.cubic(12.0)); sleep(13.0)
print("완료 — 별밭이 시선축 중심으로 한 바퀴 팽이. (성운·성단 내부 회전이 바로 이 명령)")

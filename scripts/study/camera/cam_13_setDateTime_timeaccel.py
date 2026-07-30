# -*- coding: utf-8 -*-
# [카메라 13] dm.setDateTime(..., Anim(초)) — 시간가속 = '회전 연출'의 정답.
# 카메라 명령은 아니지만, 하늘/천체를 '돌리는' 건 카메라가 아니라 '시간을 흘려서' 한다.
# 되는 곳: 지상 천구회전(일주), 행성 자전(관성프레임 병행), 일식 진행.
# 데모: 지상 밤하늘에서 6시간을 30초에 가속 → 별이 북극 중심으로 회전(지구 자전).
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
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.5)     # 시작: 밤 21시
cam.setOrientationH(180.0, Anim(0.0)); cam.setTargetHeight(50.0, Anim(0.0))  # 북쪽(자전축) 바라보기
sleep(1.5)

print("시간가속: 21시 → 새벽 3시(6시간)를 30초에 → 별이 북극 중심으로 회전")
dm.setDateTime(2026, 1, 16, 3, 0, 0, tz, Anim(30.0)); sleep(31.0)
print("완료 — 하늘이 도는 건 카메라가 아니라 시간가속. (⚠️ 지상 다년 가속=자전 광란, 시/일 단위만)")

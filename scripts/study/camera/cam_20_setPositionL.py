# -*- coding: utf-8 -*-
# [카메라 20] setPositionL — ★기대주 — 단독 경도(L) = 행성 주위 오빗?
#   시그니처: setPositionL(float, Anim, track)
#   ★확인할 것: 화성 주위를 옆으로 도나(오빗). R 이 유지되나(폭발하면 위험)
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone


def state(tag):
    try:
        p = cam.positionLBR; o = cam.orientationHPR
        print("   [%s] pos(L=%.2f B=%.2f z=%.2f)  HPR(%.1f, %.1f, %.1f)"
              % (tag, p.x, p.y, p.z, o.x, o.y, o.z))
    except Exception as e:
        print("   [%s] 읽기 예외: %s" % (tag, e))


# 화성 프레임 (위치 세터는 행성 프레임에서만 유효)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.8)
DataManager.database().data(Data.Type.PlanetType, "Mars").action(Action.Type.StraightGoTo).trigger()
sleep(4.0)
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.5)
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.5)); mars.setShadowContrast(0.0, Anim(0.5))
mars.setPlanetShineStrength(1.0, Anim(0.5)); sleep(1.2)
p0 = cam.positionLBR.z
for z in (1.2, 1.45):                      # 살짝 줌(크기 확보) — 절대타겟+선형+겹침
    cam.setPositionR(p0 / z, Anim(1.3), -1); sleep(1.0)
sleep(1.0)
print("화성 도착 (B=90 도킹 유지). 화성 위치를 기억하세요")
state("기준")

base = cam.positionLBR.x
for d in (45.0, 90.0, 135.0, 180.0):
    print("setPositionL(기준%+.0f)" % d)
    cam.setPositionL(base + d, Anim.cubic(3.0), -1); sleep(3.6); state("L+%.0f" % d)
print("\n★판단: 화성 주위를 도는 '오빗'이 됐나? R(HUD km)이 그대로인가?")
print("  → 되면 '행성 주위 공전 카메라' 도구 확보 (setPositionLBR 로 R 되써넣는 위험 없이)")

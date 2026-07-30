# -*- coding: utf-8 -*-
# [카메라 28] setActiveTarget — 타겟 활성화 플래그? — 켜고 Target 조작 비교
#   시그니처: setActiveTarget(bool, Anim)
#   ★확인할 것: 켠 상태에서 setTargetHeight 가 다르게 동작하나
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


# 지상 밤하늘 (은하수·별자리선 = 변화가 눈에 보이는 기준)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
for c in ("Ori", "UMa", "Cas"):
    try: Constellation(getattr(Constellation.ConstellationName, c)).setLinesIntensity(0.7, Anim(0.0))
    except Exception: pass
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0)); sleep(1.5)
print("기준 화면(지상 밤): 은하수+별자리선을 기억하세요")
state("기준")

print("① setActiveTarget(False) 상태에서 Target 30→60")
cam.setActiveTarget(False, Anim(0.5)); sleep(1.0)
cam.setTargetHeight(60.0, Anim.cubic(2.5)); sleep(3.2); state("False,TH60")
print("② setActiveTarget(True) 상태에서 Target 60→30")
cam.setActiveTarget(True, Anim(0.5)); sleep(1.0)
cam.setTargetHeight(30.0, Anim.cubic(2.5)); sleep(3.2); state("True,TH30")
print("\n★판단: True/False 에 따라 Target 반응이 달랐나? 화면 차이 있나?")

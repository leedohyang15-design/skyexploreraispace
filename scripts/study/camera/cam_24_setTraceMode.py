# -*- coding: utf-8 -*-
# [카메라 24] setTraceMode — 궤적 모드? — 시간가속과 함께 확인
#   시그니처: setTraceMode(bool)  ※Anim 없음
#   ★확인할 것: 천체가 지나간 자리에 궤적(선)이 남나
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

print("setTraceMode(True) 후 시간가속(별이 도는 동안 궤적 남나)")
cam.setTraceMode(True); sleep(1.0)
dm.setDateTime(2026, 1, 15, 18, 0, 0, tz, Anim(18.0)); sleep(19.0)
print("★판단: 별들이 지나간 자리에 선/잔상이 남았나?")
cam.setTraceMode(False); sleep(1.0)
print("setTraceMode(False) 복귀")

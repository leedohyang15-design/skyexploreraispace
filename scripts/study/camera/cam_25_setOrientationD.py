# -*- coding: utf-8 -*-
# [카메라 25] setOrientationD — D 가 뭔가? — API 문서에 설명 0줄, 실측으로만
#   시그니처: setOrientationD(float, Anim)  ※track 없음
#   ★확인할 것: 뭐가 바뀌나. 아무 변화 없으면 '무반응'으로 확정 기록
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

for v in (15.0, 45.0, 90.0, 0.0):
    print("setOrientationD(%.0f)" % v)
    cam.setOrientationD(v, Anim.cubic(2.5)); sleep(3.2); state("D=%.0f" % v)
print("\n★판단: 화면/상태값 중 뭐가 변했나? (HPR? 아무것도?)")
print("  D 후보: Dome tilt / Distance / Declination / Dutch angle …")

# -*- coding: utf-8 -*-
# [카메라 21] setOrientationXYZ — 방향벡터(Roll 없는 버전) — 5번의 형제
#   시그니처: setOrientationXYZ(Vec3, Anim)  ※track 없음
#   ★확인할 것: 지정 방향을 바라보나. (1,0,0)=앞 (0,1,0)=옆 (0,0,1)=위
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

for v, nm in ((Vec(1.0,0.0,0.0),"+X(앞)"), (Vec(0.0,1.0,0.0),"+Y(옆)"),
              (Vec(0.0,0.0,1.0),"+Z(위)"), (Vec(0.0,0.0,0.0),"0(리셋)")):
    print("setOrientationXYZ(%s)" % nm)
    cam.setOrientationXYZ(v, Anim.cubic(2.5)); sleep(3.2); state(nm)
print("\n★판단: 5번(setOrientationSmoothXYZR)의 XYZ 와 같은 축 규약인가?")

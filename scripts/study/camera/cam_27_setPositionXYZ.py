# -*- coding: utf-8 -*-
# [카메라 27] setPositionXYZ — ⚠️위험 가능 — 직교좌표 이동(단위 불명)
#   시그니처: setPositionXYZ(Vec3, Anim, track)
#   ★확인할 것: 화성이 유지되나 사라지나. 사라지면 '단위 불명 → 쓰지 말 것' 확정
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

print("⚠️ 작은 값부터 조심스럽게 (사라지면 그 자체가 결론)")
for v, nm in ((Vec(0.0,0.0,5.0),"(0,0,5)"), (Vec(3.0,0.0,4.0),"(3,0,4)")):
    print("setPositionXYZ%s" % nm)
    cam.setPositionXYZ(v, Anim.cubic(3.0), -1); sleep(3.5); state(nm)
    print("   화성 보이나?")
print("\n★판단: 화성이 화면에 남았나? 사라졌으면 XYZ 는 위험 → LBR/R 만 쓸 것")

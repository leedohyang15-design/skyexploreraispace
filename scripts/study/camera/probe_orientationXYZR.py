# -*- coding: utf-8 -*-
# [프로브] setOrientationSmoothXYZR 의 Vec4(X,Y,Z,R) 파라미터 해독.
# 가설: 축-각도 → (X,Y,Z)=회전축, R=각도(도?). / 아니면 쿼터니언(x,y,z,w).
# 방법: 별밭(은하수+별자리선 = 비대칭 기준)을 두고 성분 하나씩 바꿔 '어떻게/얼마나' 도는지 관찰.
#   각 값은 '절대' 방향이라 (0,0,0,0)으로 매번 리셋됨.
from skyExplorer import *
from studio import *
from Initialization import *

dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
cam = Camera(Camera.CameraName.MainCamera)

# 기준 별밭(은하수 띠 + 별자리선 = 어느 방향으로 도는지 눈에 확 보이게)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.8, Anim(0.0))
for c in ["Ori","UMa","Cyg","Cas"]:
    try: Constellation(getattr(Constellation.ConstellationName, c)).setLinesIntensity(0.7, Anim(0.0))
    except Exception: pass
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(90.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0)); sleep(1.5)

def show(vec4, label):
    print("---- setOrientationSmoothXYZR(Vec4%s) : %s ----" % (vec4, label))
    try:
        cam.setOrientationSmoothXYZR(Vec4(*vec4), Anim.cubic(3.0), -1); sleep(4.0)
        try:
            o = cam.orientationHPR
            print("     결과 HPR = (%.1f, %.1f, %.1f)" % (o.x, o.y, o.z))
        except Exception:
            pass
    except Exception as e:
        print("     예외:", e)
    sleep(1.5)

base = (0.0, 0.0, 0.0, 0.0)
print("\n===== 1) 축 판별: X vs Y vs Z 에 90 =====")
show(base, "기준(0,0,0,0) — 이 화면을 기억")
show((1.0, 0.0, 0.0, 90.0), "X축 90 (위아래 pitch? 좌우 yaw? 롤?)")
show(base, "리셋")
show((0.0, 1.0, 0.0, 90.0), "Y축 90")
show(base, "리셋")
show((0.0, 0.0, 1.0, 90.0), "Z축 90 (시선축 롤이면 별밭이 팽이처럼)")
show(base, "리셋")

print("\n===== 2) R 크기 판별: Z축에 45 / 90 / 180 (도 단위면 각각 1/8,1/4,1/2바퀴) =====")
show((0.0, 0.0, 1.0, 45.0), "Z 45")
show((0.0, 0.0, 1.0, 90.0), "Z 90")
show((0.0, 0.0, 1.0, 180.0), "Z 180")
show(base, "리셋")

print("\n===== 3) 쿼터니언 가능성 체크: (0,0,0,1) 이 기준과 같나 다르나 =====")
show((0.0, 0.0, 0.0, 1.0), "(0,0,0,1) — 축-각도면 각0=무회전(기준과 동일), 쿼터니언이면 identity")

print("\n>>> 각 단계에서 화면이 '어느 방향으로(위아래/좌우/롤) 얼마나' 돌았는지 알려주세요.")
print("    특히: 1)에서 X/Y/Z가 각각 pitch/yaw/roll 중 뭐였나  2)에서 45<90<180 로 회전량이 비례했나")

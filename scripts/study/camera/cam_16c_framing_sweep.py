# -*- coding: utf-8 -*-
# [카메라 16c] 행성 프레이밍 확정 — B 값을 스윕해서 '관람 정위치'를 눈으로 고른다
#
# 확정된 사실(사용자 실측):
#   · setPositionB(값) = R 안 건드리고 B만 바뀜 ✅  · setPositionR(p.z/배율) 정상(16,981→11,321=÷1.5) ✅
#   · ⚠️ 이 프레임에서 '화성의 화면 높이'를 정하는 건 Target 이 아니라 **B** 다:
#       B=90(도킹기본) → 화면 맨 아래 / B=20 → 화면 정가운데(천정=목 꺾임, 부적합)
#   → 그 사이 어딘가가 관람 정위치. 이 스크립트로 B 를 훑어 '딱 좋은 값'을 찾는다.
#
# 각 B 마다 6초 홀드. 화성이 '화면 하단 1/3 쯤(관람 편한 높이)'에 오는 B 를 알려주세요.
from skyExplorer import *
from studio import *
from Initialization import *

B_SWEEP = [90.0, 75.0, 65.0, 55.0, 45.0, 30.0]   # 아래 → 위로 올라옴
HOLD    = 6.0

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# 지상 밤 출발 → 화성 즉시 도착
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.8)

h = DataManager.database().data(Data.Type.PlanetType, "Mars")
h.action(Action.Type.StraightGoTo).trigger(); sleep(4.0)
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.5)

mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.5)); mars.setShadowContrast(0.0, Anim(0.5))
mars.setPlanetShineStrength(1.0, Anim(0.5)); sleep(1.0)

# 살짝 줌인해서 크기 확보 (검증됨: 절대타겟 + 선형 + 겹침)
p0 = cam.positionLBR.z
for zoom in (1.2, 1.45, 1.6):
    cam.setPositionR(p0 / zoom, Anim(1.3), -1); sleep(1.0)
sleep(1.0)
print("줌 완료 — 이제 B 스윕으로 프레이밍 찾기\n")

# ★ B 스윕: 화성이 화면에서 아래→위로 이동한다. 관람 편한 높이를 고르자.
for b in B_SWEEP:
    cam.setPositionB(b, Anim.cubic(2.5), -1)
    sleep(3.0)
    cam.setTargetHeight(30.0, Anim(1.0))     # Target 은 표준 30 고정
    sleep(HOLD)
    try:
        p = cam.positionLBR
        print("B=%-5.0f → 화성 화면 위치 확인   (positionLBR B=%.1f, z=%.1f)" % (b, p.y, p.z))
    except Exception:
        print("B=%-5.0f → 확인" % b)

print("\n===== 보고 =====")
print("화성이 '화면 하단 1/3, 목 안 꺾고 편한 높이'에 온 B 값은 몇이었나요?")
print("  (그 값을 암석행성 표준 프레이밍으로 문서에 확정하겠습니다)")
print("  · B=90 은 화면 맨 아래(너무 낮음) / B=20~30 은 정가운데(천정=목 꺾임)")

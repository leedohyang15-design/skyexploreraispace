# -*- coding: utf-8 -*-
# [카메라 16b] 화성 도착 후 안전한 프레이밍/줌 — ★R 을 '되써넣지 않는' 방식
#
# 앞 버전(16)이 망한 원인 (사용자 스샷 확정):
#   `p = cam.positionLBR` 로 z=105609 를 읽어 `setPositionLBR(Vec(p.x, 20, p.z))` 로 되써넣었는데,
#   그 프레임(Place2D 1 Mars)에서는 **읽기 단위 ≠ 쓰기 단위** → R 이 16,981km 에서 **99.63 Gm(0.66AU)**
#   로 폭발해 화성이 사라짐. → **읽은 z 를 다시 R 로 쓰지 말 것.**
#
# 이 스크립트가 검증하는 것:
#   ① setPositionB(B만 변경) 가 R 을 건드리지 않고 B 를 내리나?
#   ② setPositionR(현재값÷배율) 이 이 프레임서 정상 동작하나? (한 스텝만 조심스럽게)
# 각 단계마다 positionLBR 을 찍고, HUD 의 R(km/Gm)과 비교해 알려주세요.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone


def dump(tag):
    try:
        p = cam.positionLBR
        print("   [%s] positionLBR L=%.2f B=%.2f z=%.4f   ← HUD 의 R(km/Gm)과 비교!" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 읽기 예외: %s" % (tag, e))


# 지상 밤 출발
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(1.0)

# ① StraightGoTo = 즉시 도착 (이건 정상 작동 — R≈5 화성반지름 도킹)
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
print("① StraightGoTo (즉시 도착)")
h.action(Action.Type.StraightGoTo).trigger(); sleep(4.0)
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.5)
dump("도착직후")
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(1.0)); mars.setShadowContrast(0.0, Anim(1.0))
mars.setPlanetShineStrength(1.0, Anim(1.0)); sleep(1.5)
print("   ★지금 화성이 화면 '아래쪽'에 보이나? (B=90 북극상공이라 발밑에 있음)")
sleep(4.0)

# ② B 만 내리기 — setPositionB 사용 (R 을 안 건드림!)
print("\n② setPositionB(20) — B만 90→20 (R 은 손대지 않음)")
try:
    cam.setPositionB(20.0, Anim.cubic(4.0), -1)
    sleep(5.0); dump("B변경후")
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    print("   ★화성이 화면 중앙으로 왔나? R(HUD)이 그대로 16,981km 근처인가?")
except Exception as ex:
    print("   setPositionB 예외: %s" % ex)
    print("   → B 전용 세터가 없으면, 대신 아래를 시도: cam.setPositionL(...) 또는 Target 을 아래로")
sleep(4.0)

# ③ 줌 — 한 스텝만 조심스럽게 (이 프레임서 setPositionR 이 정상인지 확인)
print("\n③ setPositionR 한 스텝만 테스트 (÷1.5)")
try:
    p = cam.positionLBR
    cam.setPositionR(p.z / 1.5, Anim(2.0), -1)
    sleep(2.5); dump("줌1스텝후")
    print("   ★화성이 '조금 커졌나'? 아니면 또 멀어졌나(HUD R 이 Gm 으로 튀었나)?")
    print("     - 커졌으면 → 이 프레임서 setPositionR 정상. 같은 방식 여러 스텝 OK")
    print("     - 멀어졌으면 → 이 프레임은 줌도 불가 → 행성 접근은 FadeTo 를 쓸 것(검증됨)")
except Exception as ex:
    print("   setPositionR 예외: %s" % ex)
sleep(4.0)

print("\n===== 보고 =====")
print("① 도착 직후 화성이 아래쪽에 보였나")
print("② setPositionB(20) 으로 중앙에 왔나 / HUD R 이 유지됐나")
print("③ 줌 1스텝에서 커졌나, 아니면 또 멀어졌나")
print("  (③이 실패면 StraightGoTo 프레임은 후속 카메라 조작이 안 되는 것 → FadeTo 로 갑니다)")

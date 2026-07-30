# -*- coding: utf-8 -*-
# [카메라 29] StraightGoTo 재검증 — "즉시 도착"이 맞나? 태양 쪽에서 멈추나?
#
# ⚠️ 내가 '즉시 도착'이라 단정한 근거가 약했음(스샷 1장 + 2초 간격 4샘플).
#    사용자 관찰: "자꾸 태양 쪽에서 멈춘다" → **직선 비행 도중 정지**일 가능성.
#
# 이 스크립트는 **카메라를 전혀 건드리지 않고 관찰만** 한다(줌·B조정 없음):
#   · 1초 간격 30초 로깅 → 즉시점프인지 / 비행인지 / 중간에 멈추는지 판별
#   · Mars·Jupiter·Moon 3개 대상으로 반복 → 대상별 차이 확인
# 총 ~2분.
from skyExplorer import *
from studio import *
from Initialization import *

TARGETS = [("PlanetType", "Mars"), ("PlanetType", "Jupiter"), ("SatelliteType", "Moon")]
WATCH_SEC = 30          # 관찰 시간(초) — 비행이면 이 안에 R 이 계속 변한다

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone


def R():
    try: return cam.positionLBR.z
    except Exception: return None


def ground():
    SceneGraph().reset(1); sleep(1.5)
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
    e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.3)
    cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.8)


for (tname, oname) in TARGETS:
    print("\n" + "=" * 60)
    print("### StraightGoTo → %s (%s)" % (oname, tname))
    print("=" * 60)
    ground()
    h = DataManager.database().data(getattr(Data.Type, tname), oname)
    if h is None:
        print("  핸들 없음 — 스킵"); continue
    act = h.action(Action.Type.StraightGoTo)
    if act is None:
        print("  StraightGoTo 없음(死) — 스킵"); continue

    print("  실행 전 R = %s" % R())
    act.trigger()

    # ★ 카메라 손대지 않고 1초 간격 관찰
    prev = None
    still = 0
    for s in range(1, WATCH_SEC + 1):
        sleep(1.0)
        r = R()
        mark = ""
        if prev is not None and r is not None:
            if abs(r - prev) < 1e-6:
                still += 1
                mark = "  (정지 %d초째)" % still
            else:
                still = 0
                mark = "  ← 변화중"
        print("   +%2ds  R = %s%s" % (s, r, mark))
        prev = r
        if still >= 6:                      # 6초 연속 정지 = 도착으로 판단
            print("   → 6초간 R 불변 = 정지(도착) 판정, 관찰 종료")
            break

    print("  최종 R = %s" % R())
    print("  ★확인: ① 화면에 %s 이(가) 크게 보이나  ② 아니면 태양/빈 우주인가" % oname)
    print("         ③ R 이 '한 번에 툭' 바뀌었나(즉시) '점점' 바뀌었나(비행)")
    sleep(4.0)

print("\n\n===== 최종 보고 요청 =====")
print("대상별로: (a) 도착했나/태양쪽에 멈췄나  (b) 즉시점프인가 비행인가  (c) 걸린 시간")
print("  → 이걸로 StraightGoTo 의 정체를 확정하고, 안 되면 '쓰지 말 것'으로 도장 찍는다.")

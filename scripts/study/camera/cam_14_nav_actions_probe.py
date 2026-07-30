# -*- coding: utf-8 -*-
# [카메라 14] 누락됐던 '내비게이션 액션' 정체 규명
#   StraightGoTo / GoToPlace / FadeToPlace / LookAt / ScaleUp / FadeToObservation / FadeToParent
#   → API 문서엔 enum 목록만 있고 설명이 없음. 그래서 실측으로 의미를 밝힌다.
#
# 설계: ① 화성(확실히 핸들·액션 있는 개체)에서 각 액션이 '뭘 하는지' 배운다
#       ② 거기서 배운 걸 NGC(장미성운)에 적용해 '여행'을 완성한다
# 각 액션마다: 실행 전 R → 실행 후 3초 간격 R 추적 → 화면 관찰(콘솔에 뭘 볼지 안내)
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

PROBE = ["StraightGoTo", "GoToPlace", "FadeToPlace", "LookAt", "ScaleUp"]


def R():
    try: return round(cam.positionLBR.z, 4)
    except Exception: return None


def ground():
    """지상 밤하늘로 초기화 (각 액션 테스트 전 동일 출발점)"""
    try: SceneGraph().reset(1); sleep(1.6)
    except Exception: pass
    uni.setGlobalIntensity(1.0, Anim(0.0))
    e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
    cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.8)


def try_action(dtype_name, obj_name, action_name, watch=5, label=""):
    """액션 하나를 실행하고 R 변화를 추적. 반환: 살아있었나(bool)"""
    dt = getattr(Data.Type, dtype_name, None)
    if dt is None:
        print("   Data.Type.%s 없음" % dtype_name); return False
    try: h = DataManager.database().data(dt, obj_name)
    except Exception as ex:
        print("   핸들 예외: %s" % ex); return False
    if h is None:
        print("   핸들 없음 (%s/'%s')" % (dtype_name, obj_name)); return False
    act = getattr(Action.Type, action_name, None)
    if act is None:
        print("   Action.Type.%s 없음" % action_name); return False
    try: a = h.action(act)
    except Exception as ex:
        print("   action() 예외: %s" % ex); return False
    if a is None:
        print("   ✗ %-18s = None(死)" % action_name); return False

    print("   ✓ %-18s 살아있음 → 실행 (실행전 R=%s)" % (action_name, R()))
    a.trigger()
    for i in range(watch):
        sleep(3.0); print("        +%2ds  R=%s" % ((i + 1) * 3, R()))
    print("        ★관찰: %s" % (label or "화면이 어떻게 변했나?"))
    return True


# ═════════ ① 화성에서 각 액션 의미 배우기 ═════════
print("\n############ ① 화성 — 액션별 의미 규명 ############")
for an in PROBE:
    print("\n--- [화성] %s ---" % an)
    ground()
    try_action("PlanetType", "Mars", an, watch=5,
               label="R이 줄며 접근했나(비행) / 순간이동인가 / 조준만 바뀌었나 / 무반응인가")

# ═════════ ② NGC(장미성운)에 적용 ═════════
print("\n\n############ ② 장미성운 NGC2237 — 여행 시도 ############")
NGC_CANDS = [("NgcType", "NGC 2237"), ("MessierType", "NGC 2237"),
             ("NgcType", "NGC2237"), ("NgcType", "Rosette")]
for an in PROBE + ["ConnectTo", "GoTo", "FadeTo"]:
    for (tn, nm) in NGC_CANDS:
        print("\n--- [장미성운] %s / %s ---" % (an, tn))
        ground()
        ngc = NGC(NGC.NGCName.NGC2237)
        ngc.setIntensity(1.0, Anim(0.0))
        try: ngc.setLabelIntensity(1.0, Anim(0.0))
        except Exception: pass
        sleep(1.0)
        ok = try_action(tn, nm, an, watch=5,
                        label="장미성운이 커지며 다가왔나? 화면 중앙에 왔나? 검은화면인가?")
        if ok:
            # 액션이 살아있으면 관람 정위치로 정렬 + 줌 시도
            cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
            print("        TargetHeight 30 정렬 후 R=%s" % R())
            p = R()
            if p and p > 0:
                cam.setPositionR(p * 0.4, Anim.cubic(3.0), -1); sleep(3.5)
                print("        줌인 시도(×0.4) 후 R=%s → 성운이 커졌나?" % R())
            break        # 이 액션에서 성공했으니 다음 액션으로

print("\n\n===== 보고 요청 =====")
print("① 화성에서 각 액션이 '뭘 했는지' (비행/순간이동/조준만/무반응)")
print("② 장미성운에서 '살아있음(✓)' 으로 뜬 액션 목록")
print("③ 그중 실제로 성운이 커지며 접근한 액션이 있었나")

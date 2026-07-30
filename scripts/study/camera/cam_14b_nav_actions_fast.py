# -*- coding: utf-8 -*-
# [카메라 14b] 내비게이션 액션 7종 정체 규명 — ★짧은 버전 (v14 는 10분 넘게 걸려 폐기)
#   StraightGoTo / GoToPlace / FadeToPlace / LookAt / ScaleUp / FadeToObservation / FadeToParent
#   API 문서엔 enum 이름만 있고 설명이 없음 → 실측으로 의미를 밝힌다.
#
# 총 예상 시간 ≈ 90초 (액션당 ~12초, 죽은 액션은 즉시 스킵)
# 대상 = 화성 하나(확실히 핸들 있는 개체)로 고정. R 변화 패턴으로 성격을 판별한다.
#   · R 이 여러 번에 걸쳐 점점 줄어듦     → '비행'(연속 이동)
#   · R 이 한 번에 툭 바뀜               → '순간이동'
#   · R 은 그대로인데 화면 방향만 바뀜    → '조준'
#   · R·화면 다 그대로                   → 무반응(또는 다른 걸 건드림)
from skyExplorer import *
from studio import *
from Initialization import *

ACTIONS = ["LookAt", "StraightGoTo", "GoToPlace", "FadeToPlace",
           "FadeToObservation", "FadeToParent", "ScaleUp"]
TARGET  = ("PlanetType", "Mars")

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()


def R():
    try: return round(cam.positionLBR.z, 5)
    except Exception: return None


def ground():
    """지상 밤하늘 초기화 (액션마다 동일 출발점). 짧게."""
    try: SceneGraph().reset(1); sleep(1.5)
    except Exception: pass
    uni.setGlobalIntensity(1.0, Anim(0.0))
    e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.3)
    cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.5)


print("=== 내비게이션 액션 7종 실측 (대상: 화성) — 예상 90초 ===")
dt = getattr(Data.Type, TARGET[0])

for idx, an in enumerate(ACTIONS, 1):
    act_enum = getattr(Action.Type, an, None)
    if act_enum is None:
        print("\n[%d/%d] %-18s → Action.Type 에 없음(스킵)" % (idx, len(ACTIONS), an))
        continue

    # 죽은 액션은 리셋도 하지 말고 즉시 스킵 (시간 절약)
    h = db.data(dt, TARGET[1])
    if h is None:
        print("\n[%d/%d] %-18s → 핸들 없음(스킵)" % (idx, len(ACTIONS), an)); continue
    try: a = h.action(act_enum)
    except Exception as ex:
        print("\n[%d/%d] %-18s → action() 예외 %s (스킵)" % (idx, len(ACTIONS), an, ex)); continue
    if a is None:
        print("\n[%d/%d] %-18s → ✗ None(死), 스킵" % (idx, len(ACTIONS), an)); continue

    # 살아있는 액션만 실측
    print("\n[%d/%d] %-18s → ✓ 살아있음, 실행" % (idx, len(ACTIONS), an))
    ground()
    h = db.data(dt, TARGET[1])                  # reset 후 핸들 재확보
    r0 = R(); print("      실행전 R=%s" % r0)
    h.action(act_enum).trigger()
    samples = []
    for k in range(4):                           # 2초 간격 4회 = 8초 관찰
        sleep(2.0); r = R(); samples.append(r)
        print("      +%ds R=%s" % ((k + 1) * 2, r))
    # 자동 판정 보조
    changed = [s for s in samples if s is not None and r0 is not None and abs(s - r0) > 1e-6]
    if not changed:
        verdict = "R 무변화 → '조준' 또는 '무반응' (화면 방향이 바뀌었는지 눈으로 확인)"
    elif len(set(changed)) == 1:
        verdict = "R 이 한 번에 바뀜 → '순간이동' 계열"
    else:
        verdict = "R 이 여러 단계로 변함 → '비행' 계열"
    print("      ★판정: %s" % verdict)
    sleep(1.0)

print("\n=== 끝 ===")
print("각 액션의 ★판정 줄 + '화면이 실제로 뭘 했는지'(다가감/순간이동/조준만/무반응) 알려주세요.")
print("특히 GoToPlace·FadeToPlace·FadeToObservation·FadeToParent 는 문서에 설명이 없어 이 결과가 유일한 근거입니다.")

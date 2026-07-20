# -*- coding: utf-8 -*-
"""
star_life_cycle.py — 별의 일생 (2026-07-13 v6, docs/19 확정 방식)
★ docs/19 개체별 무빙 매트릭스 준수:
  · 성운(Nebula)은 GoTo 안 됨 / setScale 은 카메라 안 움직임 → **ConnectTo 프레임 + setPositionR 지오메트릭
    줌** 이 확정 이동법. R 이 줄어드는 것 = 카메라가 성운으로 '날아드는' 것(화면 이동). (규칙 #1~3)
  · 줌 = Anim(선형)+ratio 0.6+짧게+절대타겟(겹침=연속·매끄러움), 목표 R 까지 적응형(R0 불문).
  · 별(IndividualStar)은 fly-in 자체가 없음(포트 조망만) → 포인터로 지목만.
  · 🎯 Target 30(관람 표준) 준수.
스토리: 탄생(M42) → 주계열(태양) → 거성(베텔게우스) → 죽음①(M27) → 죽음②(M1) → 순환.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
EASE = [0.86, 0.74, 0.66, 0.62]


def scene_base():
    uni.setGlobalIntensity(0.0, Anim(0.0))
    SceneGraph().reset(1); sleep(2.0)
    uni.setGlobalIntensity(0.0, Anim(0.0))
    Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
    Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
    IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)
    cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))


scene_base()
mw = Galaxy(Galaxy.GalaxyName.MilkyWay)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))

# ⚠️ 목표는 '절대 R' 이 아니라 'R0 의 비율(frac)' — R0 가 개체마다 천차만별(M42 1e16 / M1 3.8e18)이라
#   절대값을 주면 M1 은 성운을 뚫고 지나쳐 새까맣게 됨. frac 이면 개체 불문 같은 배율만큼만 날아듦.
NEB_STAGES = [
    dict(key="M42", enum=Messier.MessierName.M42, chapter="제1막 — 별의 탄생",
         narr=["차가운 수소 구름이 중력으로 뭉친다", "그 심장부에서 새 별이 켜진다 — 별의 요람"],
         frac=0.0094, roll=0),                           # ~100배 날아듦(돔 가득, 검증됨)
    dict(key="M27", enum=Messier.MessierName.M27, chapter="제4막 — 별의 죽음",
         narr=["태양 같은 별은 연료가 바닥나면", "겉껍질을 부드럽게 벗는다 — 행성상성운"],
         frac=0.004, roll=0),                            # 덜 깊게(너무 컸음 → 축소)
    # ⚠️ fly-in 개체 검증: M42/M27=ConnectTo 지원(줌 O) / M1=렌더X / M8=FadeTo만(R=0, 줌 X).
    #   → 순환 마무리는 확정 개체 M42 재방문("다시 요람으로")으로. 시작점 회귀 = 순환의 시적 닫힘.
    dict(key="M42", enum=Messier.MessierName.M42, chapter="제5막 — 순환 (다시, 요람으로)",
         narr=["죽은 별이 흩뿌린 원소가 다시 뭉쳐", "또 다른 별의 요람이 된다 — 순환은 계속된다"],
         frac=0.0094, roll=0),
]
neb_handles = {}
for s in NEB_STAGES:
    try:
        h = DataManager.database().data(Data.Type.NebulaType, s["key"])
        neb_handles[s["key"]] = h
        goto = h.action(Action.Type.GoTo) if h is not None else None
        print("   DB '%s'=%s / GoTo=%s" % (s["key"], h is not None, goto is not None))
    except Exception as e:
        neb_handles[s["key"]] = None; print("   DB '%s' 실패: %s" % (s["key"], e))

uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("별의 일생 — 태어나고, 빛나고, 죽고, 다시 태어난다"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.5); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def bg_off(keep_enum):
    try:
        mw.setIntensity(0.0, Anim(1.5))
    except Exception:
        pass
    for s in NEB_STAGES:
        if s["enum"] != keep_enum:
            try:
                Messier(s["enum"]).setIntensity(0.0, Anim(1.2))
            except Exception:
                pass
    try:
        Messier(keep_enum).setIntensity(1.0, Anim(1.5))
    except Exception:
        pass


def fly_in(s):
    """★ docs/19 확정: 성운 카메라 이동 = setPositionR 지오메트릭 줌(R 줄며 날아듦=화면 이동).
    규칙#3: Anim(선형)+ratio 0.6+짧게+절대타겟(겹침=연속). 목표=R0×frac(개체 불문 같은 배율)."""
    R0 = cam.positionLBR.z
    target = R0 * s["frac"]                               # ★ 비율 기반(절대값 금지 = M1 뚫림 방지)
    print("   비행 시작 R=%.3e (목표 %.3e = ×%.4f)" % (R0, target, s["frac"]))
    if R0 <= target:
        return
    r = R0; targets = []; i = 0
    while r > target and len(targets) < 30:
        r *= EASE[i] if i < len(EASE) else 0.60; targets.append(r); i += 1
    for j, tgt in enumerate(targets):
        cam.setPositionR(tgt, Anim(1.2), -1)          # 선형·짧게
        sleep(1.4 if j == 0 else 0.8)                 # 첫스텝만 완만, 이후 겹침(정지없이 연속)
    sleep(1.0)
    print("   비행 완료 R=%.3e" % cam.positionLBR.z)


def show_nebula(s):
    """성운: ConnectTo 로 프레임 확보(암전으로 슬루 숨김) → setPositionR 로 날아듦(화면 이동) → Target 30."""
    h = neb_handles.get(s["key"])
    print("=" * 55); print("%s (%s)" % (s["key"], s["chapter"]))
    if h is None:
        print("   DB 없음 → 건너뜀"); return
    ct = h.action(Action.Type.ConnectTo) or h.action(Action.Type.FadeTo)
    if ct is None:
        print("   진입 액션 없음 → 건너뜀"); return
    # ★ 매 성운마다 '지상에서' ConnectTo 시작 = 일관된 R0(초대형) 확보 → 줌 작동.
    #   (직전이 다른 성운 근접 프레임이면 ConnectTo R0 가 작게 잡혀 줌이 안 됨 = M8 증상)
    scene_base(); sleep(0.3)                          # reset → 지상(암전 상태 유지)
    ct.trigger(); sleep(8.5)                          # 암전 속 슬루 숨김
    bg_off(s["enum"])
    cam.setTargetHeight(30.0, Anim(0.0))              # 🎯 관람 표준 30
    if s["roll"]:
        try:
            b = cam.orientationHPR
            cam.setOrientationHPR(Vec(b.x, b.y, b.z + s["roll"]), Anim(0.0))
        except Exception:
            pass
    # 페이드인 후 setPositionR 비행(카메라가 성운으로 날아듦)
    t1.setText(s["chapter"]); t1.setIntensity(1.0, Anim(1.0))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.2)); sleep(2.2)
    t1.setText(s["narr"][0])
    fly_in(s)
    if len(s["narr"]) > 1:
        t1.setText(s["narr"][1])
    sleep(3.5)
    t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def show_star(name, star_enum_name, chapter, narr, color):
    """별: docs/19 매트릭스상 fly-in 없음(포트 조망만) → 지상 스타필드 + 포인터로 지목."""
    print("=" * 55); print("STAR %s (%s)" % (name, chapter))
    uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
    scene_base()
    try:
        st = IndividualStar(getattr(IndividualStar.IndividualStarName, star_enum_name))
        st.setIntensity(1.0, Anim(0.0)); st.setPointerIntensity(1.0, Anim(0.0))
        print("   %s 포인터 ON" % name)
    except Exception as e:
        print("   포인터 실패: %s" % e)
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    t1.setColor(Vec(*color)); t1.setText(chapter); t1.setIntensity(1.0, Anim(1.0)); sleep(2.5)
    t1.setText(narr[0]); sleep(4.5)
    if len(narr) > 1:
        t1.setText(narr[1]); sleep(4.0)
    t1.setIntensity(0.0, Anim(1.0)); sleep(1.0); t1.setColor(Vec(0.9, 0.92, 1.0))


show_nebula(NEB_STAGES[0])
show_star("Sun", "Sun", "제2막 — 주계열",
          ["새로 태어난 별은 수십억 년 안정적으로 빛난다", "우리 태양도 지금 이 시기 — 주계열성"],
          (1.0, 0.95, 0.7))
show_star("Betelgeuse", "Betelgeuse", "제3막 — 거성",
          ["늙은 별은 부풀어 붉게 식는다 — 적색초거성",
           "무거운 별은 언젠가 초신성으로 터진다 — 베텔게우스처럼"],
          (1.0, 0.55, 0.4))
show_nebula(NEB_STAGES[1])
show_nebula(NEB_STAGES[2])

uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
scene_base(); uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("별의 일생 — 끝은 곧 새로운 시작"); t1.setIntensity(1.0, Anim(1.2)); sleep(5.0)
t1.setText("우리 몸의 원소도, 한때 별이었다"); sleep(4.5)
t1.setIntensity(0.0, Anim(1.5)); uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①GoTo 로 성운까지 '실제 비행(화면 이동)' 되나(로그 GoTo=True?) "
      "②도착 후 성운 프레이밍 어떤가 ③GoTo 미지원이면 폴백 탔나 ④별 이동 되나")

# -*- coding: utf-8 -*-
"""
bolide_fireball_test_v2.py — 화구 시그니처/속도 3버그 수정판 (2026-07-09)
v1 실측으로 밝혀진 것:
 ★ enum 확정: ModelID = {Chelyabinsk, ColoredFireball, User} /
              Element = {Sodium, Magnesium, Iron, Calcium, NitrogenOxygen, Custom}
 ⚠️ 버그3:
   ① setModel(model, filename) — filename 필수! 내장 모델도 "" 를 줘야 함.
   ② setElement(element, customColor, anim) — 3인자 전부 필수(문서는 optional 이나 바인딩 강제).
   ③ '아예 안 보임' 원인 = set() 의 speed 를 20 으로 준 것. 잘 됐던 v2 는 set(...,1.0).
      → **set() speed = 1.0 고정, 재생 속도는 play() 로만**. (set 은 궤적, play 는 재생 rate)

화구다움 = ColoredFireball 모델 + 원소 색 + 느린 play(). 3발 비교:
 A. 검증용 baseline (모델·색 없음, play 15) — 보여야 정상(이게 안 보이면 무대 문제)
 B. ColoredFireball + Sodium(주황) — 표준 화구
 C. Chelyabinsk + Magnesium(청록) — 2013 첼랴빈스크 대화구 오마주
원소 색 참고: Sodium=주황/노랑, Magnesium=청록, Iron=노랑, Calcium=보라, NitrogenOxygen=적색.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 (유성우 예제와 동일) ─────────────────────────────────
print("무대: 청주 2026-12-14 23:00 KST")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 14, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.9, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)


def fire(label, subtitle, model=None, elem=None, custom_color=None, play_speed=15.0, wait=9.0):
    """화구 한 발 — set() speed 는 항상 1.0(고정), 재생 속도는 play_speed 로."""
    print("=" * 60)
    print("%s — model=%s elem=%s color=%s play=%.0f km/s" % (label, model, elem, custom_color, play_speed))
    print("=" * 60)
    # 매 발 새 객체 — 재사용 시 evolution 이 max 로 남아 재생 안 되는 문제 회피
    bo = Bolide(Bolide.BolideName.Bolide001)
    t1.setText(subtitle); t1.setIntensity(1.0, Anim(0.5))
    try:
        if model is not None:
            bo.setModel(getattr(Bolide.ModelID, model), "")     # ★ filename "" 필수
            print("   setModel(%s, '') OK" % model)
    except Exception as e:
        print("   setModel 실패: %s" % e)
    try:
        if elem is not None:
            col = Vec3(*custom_color) if custom_color is not None else Vec3(0.0, 0.0, 0.0)
            bo.setElement(getattr(Bolide.Element, elem), col, Anim(0.0))   # ★ 3인자 필수
            print("   setElement(%s) OK / 읽은 element=%s" % (elem, getattr(bo, "element", "?")))
    except Exception as e:
        print("   setElement 실패: %s" % e)
    try:
        bo.setIntensity(1.0, Anim(0.0))
        bo.set(-30.0, 70.0, 100000.0, 50.0, 15.0, 30000.0, 1.0)   # ★ set speed 1.0 고정
        sleep(0.3)                                                # set 처리 여유
        bo.play(play_speed)                                       # 재생 속도만 조절
        print("   발사! play(%.0f) → 크로싱 ≈ 148/%.0f = %.1f초" % (play_speed, play_speed, 148.0/play_speed))
    except Exception as e:
        print("   발사 실패: %s" % e)
    sleep(wait)
    t1.setIntensity(0.0, Anim(0.5))
    sleep(1.2)


fire("A. baseline", "A. 기본 화구 (모델·색 없음) — 보이는지 확인",
     model=None, elem=None, play_speed=15.0)

fire("B. 표준 화구", "B. ColoredFireball + 나트륨(주황)",
     model="ColoredFireball", elem="Sodium", play_speed=15.0)

fire("C. 첼랴빈스크", "C. Chelyabinsk 모델 + 마그네슘(청록)",
     model="Chelyabinsk", elem="Magnesium", play_speed=12.0, wait=10.0)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("화구 v2 끝 — A/B/C 중 '불덩이'가 된 건? 색 차이는?")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: A(보임?)/B(주황 불덩이?)/C(청록 첼랴빈스크?) + 크로싱 속도감")

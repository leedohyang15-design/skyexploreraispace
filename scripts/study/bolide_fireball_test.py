# -*- coding: utf-8 -*-
"""
bolide_fireball_test.py — 화구를 '별똥별'이 아닌 '불덩이'로 (2026-07-07)
질문: 화구가 유성우랑 똑같이 날아갔다. 원래 비슷한가? → 아니다. 확연히 달라야 함.

Recording7 + 레퍼런스로 밝혀진 원인:
 ① play(speed) 의 speed = **km/s** (배율 아님!). 경로 ~148km → speed 1=148초, 50=3초.
    극적 화구 = 15~25 km/s (느리고 묵직).
 ② v1/v2 는 setModel/setElement 를 안 줌 → 기본 선 렌더 = 별똥별과 동일 외형.
    화구 특유의 '불덩이+색'은 **setModel(3D모델) + setElement(원소색)** 이 만든다.

이 스크립트: ModelID/Element enum 프로브 후, 화구 4발을 조건 바꿔 나란히 발사 → 비교.
 A. 기본(모델/색 없음) — v1/v2 재현(별똥별처럼 보여야 정상)
 B. + setElement 색만
 C. + setModel(내장 모델) + 느린 속도(20)
 D. 크고 느린 불덩이(모델+색+intensity 최대+속도 15) — '진짜 화구'

무대: 청주 2026-12-14 23:00 KST (유성우 예제와 동일).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d개): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e))
        return []


# ── 프로브: 화구의 모델/원소 enum (미지 — 이번 실험 핵심 수확) ──
print("=" * 60)
print("ACT 0: Bolide.ModelID / Bolide.Element 프로브")
print("=" * 60)
model_members = probe("Bolide.ModelID", Bolide.ModelID) if hasattr(Bolide, "ModelID") else []
elem_members  = probe("Bolide.Element", Bolide.Element) if hasattr(Bolide, "Element") else []

# 내장 모델 후보(User/Invalid/None 제외 첫 멤버)
builtin_model = None
for m in model_members:
    if any(x in m for x in ("Invalid", "User", "None")):
        continue
    builtin_model = m
    break
# 원소 후보(자연색이 나오는 실제 원소 이름 우선, 없으면 첫 실멤버)
named_elem = None
for m in elem_members:
    if any(x in m for x in ("Invalid", "Custom", "None")):
        continue
    named_elem = m
    break
print("[PROBE] 선택 → 내장모델=%s / 명명원소=%s" % (builtin_model, named_elem))


# ── 무대 세팅 (유성우 예제와 동일) ────────────────────────────
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
cam.setOrientationH(0.0, Anim(0.0))          # 남쪽
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.9, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

bo = Bolide(Bolide.BolideName.Bolide001)
print("   Bolide001 id=%s" % bo.id)


def fire(label, subtitle, model=None, elem=None, color=None,
         intensity=1.0, speed=20.0, wait=8.0):
    """화구 한 발 — 조건 지정. 경로는 동일(비교 위해)."""
    print("=" * 60)
    print("%s — model=%s elem=%s color=%s intensity=%.1f speed=%.0f km/s"
          % (label, model, elem, color, intensity, speed))
    print("=" * 60)
    t1.setText(subtitle); t1.setIntensity(1.0, Anim(0.5))
    try:
        if model is not None:
            bo.setModel(getattr(Bolide.ModelID, model))        # filename 은 내장이라 생략
            print("   setModel(%s) OK" % model)
    except Exception as e:
        print("   setModel 실패: %s" % e)
    try:
        if elem is not None:
            if color is not None:
                bo.setElement(getattr(Bolide.Element, elem), Vec3(*color), Anim(0.0))
            else:
                bo.setElement(getattr(Bolide.Element, elem))
            print("   setElement(%s) OK / element=%s" % (elem, getattr(bo, "element", "?")))
    except Exception as e:
        print("   setElement 실패: %s" % e)
    try:
        bo.setIntensity(intensity, Anim(0.0))
        # 경로: 남동 상공(방위 -30, 고도 70, 100km) → 남서 낮게(50, 15, 30km)
        bo.set(-30.0, 70.0, 100000.0, 50.0, 15.0, 30000.0, speed)
        bo.play(speed)
        print("   발사! (speed %.0f km/s → 크로싱 ≈ 148/%.0f = %.1f초)" % (speed, speed, 148.0/speed))
    except Exception as e:
        print("   발사 실패: %s" % e)
    sleep(wait)
    t1.setIntensity(0.0, Anim(0.5))
    sleep(1.0)


# ── A~D 비교 발사 ─────────────────────────────────────────────
fire("A. 기본", "A. 기본 화구 (모델·색 없음) — 별똥별처럼 보이면 정상",
     model=None, elem=None, speed=20.0)

fire("B. 색만", "B. + 원소 색 (%s)" % (named_elem or "?"),
     model=None, elem=named_elem, speed=20.0)

fire("C. 모델+느림", "C. + 3D 모델 + 느린 속도",
     model=builtin_model, elem=named_elem, speed=20.0)

fire("D. 큰 불덩이", "D. 진짜 화구 — 크고 느린 불덩이",
     model=builtin_model, elem="Custom" if "Custom" in elem_members else named_elem,
     color=(1.0, 0.55, 0.15), intensity=1.0, speed=15.0, wait=10.0)


# ── 피날레 ────────────────────────────────────────────────────
t1.setText("화구 비교 끝 — A~D 중 어디서 '불덩이'가 됐는지 + [PROBE] 줄 리포트!")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: ①A~D 차이(특히 D 가 불덩이인가) ②[PROBE] ModelID/Element 멤버 목록")

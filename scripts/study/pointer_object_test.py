# -*- coding: utf-8 -*-
"""
pointer_object_test.py — '개체 직결 포인터' 검증 (2026-07-07)
질문: 좌표 말고 별자리/개체를 그냥 지정해서 포인터를 붙일 수 없나?
답(레퍼런스 확인): DomePointer 는 화면좌표 전용. 개체 직결은 2경로 — 이 스크립트로 실측.
 ① 천체 내장 포인터: body.setPointerIntensity + setPointerType (별/행성/성운/은하 등)
 ② DB 액션: data.action(Action.Type.PointerOn).trigger() — enum 에 없는 천체도 OK
⚠️ Constellation 은 내장 포인터 없음 → 별자리는 대표 별을 포인팅.

무대: 청주 2026-01-15 23:00 KST (오리온 남중, 가이드 투어와 동일).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 (가이드 투어와 동일) ─────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

# 오리온 선 = 참조물
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.7, Anim(1.5))
sleep(2.0)

# ── ① 내장 포인터: 오리온의 대표 별 ──────────────────────────
print("=" * 60)
print("① 내장 포인터 — IndividualStar.setPointerIntensity")
print("=" * 60)
# IndividualStarName 에 어떤 별이 있는지 먼저 지도화 (오리온 별 위주로 출력)
names = [m for m in dir(IndividualStar.IndividualStarName) if not m.startswith("_")]
ori_stars = [n for n in names if n.lower() in
             ("betelgeuse", "rigel", "bellatrix", "alnilam", "alnitak", "mintaka", "saiph")]
print("[PROBE] IndividualStarName 총 %d개 / 오리온 별 후보: %s" % (len(names), ori_stars))

target = None
for cand in ("Betelgeuse", "Rigel", "Alnilam"):
    if cand in names:
        try:
            s = IndividualStar(getattr(IndividualStar.IndividualStarName, cand))
            if s.id != -1:
                target = (cand, s)
                break
        except Exception as e:
            print("   %s 생성 실패: %s" % (cand, e))
if target is not None:
    name, s = target
    print("   대상: %s (id=%s)" % (name, s.id))
    try:
        s.setPointerType(Body.PointerType.Model1Bold)
    except Exception as e:
        print("   setPointerType 스킵: %s" % e)
    t1.setText("① 내장 포인터 — %s 를 직접 지정" % name); t1.setIntensity(1.0, Anim(0.8))
    s.setPointerIntensity(1.0, Anim(1.5))
    print("   ★ 확인: 포인터가 %s 위에 정확히 붙었나? (좌표 계산 없이!)" % name)
    sleep(8.0)
    s.setPointerIntensity(0.0, Anim(1.5))
    sleep(1.7)
    t1.setIntensity(0.0, Anim(0.5))
else:
    print("   오리온 별이 enum 에 없음 → [PROBE] 목록에서 있는 이름 확인 후 재시도")

# ── ② DB 액션 경로: PointerOn (enum 에 없어도 이름으로) ──────
print("=" * 60)
print("② DB 액션 — Action.Type.PointerOn")
print("=" * 60)
for dtype, dname in ((Data.Type.StarType, "Betelgeuse"),
                     (Data.Type.MessierType, "M42"),
                     (Data.Type.PlanetType, "Jupiter")):
    try:
        d = DataManager.database().data(dtype, dname)
        if d is None:
            print("   %s(%s): DB 에 없음" % (dname, dtype))
            continue
        a_on = d.action(Action.Type.PointerOn)
        if a_on is None:
            print("   %s: PointerOn 액션 미지원" % dname)
            continue
        t1.setText("② DB 포인터 — %s" % dname); t1.setIntensity(1.0, Anim(0.5))
        a_on.trigger()
        print("   %s PointerOn ← 포인터 위치 확인!" % dname)
        sleep(6.0)
        a_off = d.action(Action.Type.PointerOff)
        if a_off is not None:
            a_off.trigger()
        sleep(1.0)
        t1.setIntensity(0.0, Anim(0.3))
    except Exception as e:
        print("   %s 실패: %s" % (dname, e))

# ── 정리 ──────────────────────────────────────────────────────
ori.setLinesIntensity(0.0, Anim(1.5))
t1.setText("포인터 테스트 끝 — 어느 방식이 잘 붙었는지 리포트!")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. [PROBE] IndividualStarName 목록도 복사해주면 별 enum 지도가 완성됨!")

# -*- coding: utf-8 -*-
"""
asteroid_apophis.py — 소행성 아포피스 2029 근접 v1 (2026-07-09)
새 예제: 처음 연습하는 Asteroid 클래스 — 혜성에서 배운 궤도요소 워크플로 재활용.

★ Asteroid 궤도요소 (레퍼런스): setSemiMajorAxis / setEccentricity / setInclination /
   setLongitudeOfAscendingNode / setArgumentOfPeriapsis / setMeanAnomaly / setEpoch (전부 val,Anim)
   — 혜성(근일점거리+근일점시각)과 달리 소행성은 **반장축 a + 평균근점이각 M + 에폭**.
   표시: setOrbitColor / setOrbitIntensity / setOrbitThickness / setIntensity / setLabelIntensity.
   ⚠️ 소행성은 setStandardModelName 없음(혜성과 차이) — 궤도요소가 바로 반영되는지 '진단'으로 확인.

99942 아포피스 궤도요소(대략 실제값): a=0.922 AU, e=0.191, i=3.34°, Ω=204°, ω=126.7°.
유명 이벤트: **2029-04-13 지구 초근접** (정지위성보다 가까운 ~31,000 km — 맨눈 관측 가능).

혜성 실측 교훈 적용:
 · 궤도선은 지상 시점 전용 → 지상에서 조망.  · 요소 넣고 sleep 후 read 로 반영 확인.
 · 클로즈업/정밀 위치 = DB FadeTo(AsteroidType). 근접 프레임은 자전 없어 시간가속 부드러움.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e)); return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 프로브 ────────────────────────────────────────────────────
print("=" * 60); print("ACT 0: Asteroid 프로브"); print("=" * 60)
if hasattr(Asteroid, "AsteroidPort"):
    probe("Asteroid.AsteroidPort", Asteroid.AsteroidPort)
apophis_db = None
try:
    for nm in ("99942 Apophis", "Apophis", "99942", "(99942) Apophis"):
        d = DataManager.database().data(Data.Type.AsteroidType, nm)
        print("   DB AsteroidType '%s' → %s" % (nm, "found" if d is not None else "None"))
        if d is not None and apophis_db is None:
            apophis_db = (nm, d)
except Exception as e:
    print("   DB 조회 실패: %s" % e)

# ── 무대: 지상 하늘, 2029-03 (근접 직전) ──────────────────────
print("=" * 60); print("ACT 1: 무대 (2029-03)"); print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(0.9, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2029, 3, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.85, 0.6))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("소행성 아포피스 — 2029년 4월, 지구를 스치다"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── [A] 슬롯 소행성 — 궤도요소 주입 + 진단 ───────────────────
print("=" * 60); print("[A] 슬롯 소행성 궤도요소"); print("=" * 60)
ast = Asteroid(Asteroid.AsteroidName.Asteroid001)
print("   Asteroid001 id=%s" % ast.id)
def set_read(name, setter, val):
    try:
        setter(val, Anim(0.0)); sleep(0.25)
        got = getattr(ast, name)
        print("   %s: 넣음=%.4f 읽음=%.4f %s" % (name, val, got, "OK" if abs(got-val) < 0.01 else "❌미반영"))
    except Exception as e:
        print("   %s 실패: %s" % (name, e))
try:
    ast.setIntensity(1.0, Anim(0.0)); sleep(0.2)
    set_read("semiMajorAxis",            ast.setSemiMajorAxis,            0.9224)
    set_read("eccentricity",             ast.setEccentricity,             0.1914)
    set_read("inclination",              ast.setInclination,              3.339)
    set_read("longitudeOfAscendingNode", ast.setLongitudeOfAscendingNode, 204.0)
    set_read("argumentOfPeriapsis",      ast.setArgumentOfPeriapsis,      126.7)
    set_read("meanAnomaly",              ast.setMeanAnomaly,              180.0)
    set_read("epoch",                    ast.setEpoch,                    2459396.5)
    ast.setLabelNameOverride("99942 Apophis")
    sleep(0.3)
    t1.setText("아포피스의 궤도 — 지구 궤도를 가로지른다"); t1.setIntensity(1.0, Anim(0.8))
    try:
        ast.setOrbitColor(Vec(1.0, 0.5, 0.2), Anim(0.0))
    except Exception as e:
        print("   setOrbitColor 스킵: %s" % e)
    ast.setOrbitThickness(2.0)
    ast.setOrbitIntensity(0.9, Anim(2.5))
    ast.setLabelIntensity(0.8, Anim(2.0))
    try:
        ast.setPointerType(Body.PointerType.Model3Bold)
        ast.setPointerIntensity(1.0, Anim(1.5))
    except Exception as e:
        print("   포인터 스킵: %s" % e)
    print(">>> 궤도선/소행성 조망 (7초)")
    sleep(7.0)
    t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)
except Exception as e:
    print("   [A] 실패: %s" % e)

# ── [B] DB 클로즈업 + 2029-04-13 근접 ────────────────────────
print("=" * 60); print("[B] DB FadeTo + 2029-04-13 근접"); print("=" * 60)
if apophis_db is not None:
    nm, d = apophis_db
    try:
        act = d.action(Action.Type.FadeTo)
        if act is not None:
            t1.setText("아포피스 곁으로 — %s" % nm); t1.setIntensity(1.0, Anim(0.8))
            try:
                ast.setPointerIntensity(0.0, Anim(0.5))
            except Exception:
                pass
            act.trigger()
            sleep(6.0)
            # 당기기 (혜성 레시피)
            try:
                p = cam.positionLBR
                print("   FadeTo 후 R=%.3f → 당기기" % p.z)
                cam.setPositionR(p.z * 0.5, Anim.cubic(4.0), -1)
                sleep(5.0)
            except Exception as e:
                print("   당기기 스킵: %s" % e)
            # 근접일로 시간가속 (황도 프레임 = 부드러움)
            t1.setText("2029년 4월 13일 — 지구 최근접(정지위성보다 가까이)")
            dm.setDateTime(2029, 4, 13, 21, 46, 0, tz, Anim(12.0))
            sleep(13.0)
            print("   ★ 근접 시점에서 소행성이 커졌나/지구 스치는 게 보이나?")
            t1.setText("맨눈으로 보이는 소행성 — 3등급 밝기로 하늘을 가로지른다")
            sleep(4.0)
            t1.setIntensity(0.0, Anim(0.8))
        else:
            print("   FadeTo 미지원")
    except Exception as e:
        print("   [B] 실패: %s" % e)
else:
    print("   DB 핸들 없음 → [PROBE]의 발견 이름으로 재시도 필요")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("아포피스 — 2029, 지구와의 아슬아슬한 랑데부"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①궤도요소 read OK/❌ ②궤도선 보임 ③DB 발견 이름 ④근접 클로즈업 양상")

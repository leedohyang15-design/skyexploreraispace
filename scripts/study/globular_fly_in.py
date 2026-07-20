# -*- coding: utf-8 -*-
"""
globular_fly_in.py — 성단 속으로 '비행' 시도 (2026-07-09)
사용자: setScale 확대 말고 **성단 속으로 날아 들어가기(take off/비행)**.
⚠️ 과거 기록: AdvancedCamera 비행 메서드(takeOffOn/setModeFreeFly/zoom)는 스크립트서 무효였음.
   → 지금 빌드서 다시 되는지 재검증 + 좌표로 이동 확인. 안 되면 '오퍼레이터 Take off' 안내.

절차: FadeTo 성단 → AdvancedCamera 확보 → setModeFreeFly → zoom(전진) → 좌표 변화 확인.
     보조로 move()/takeOffOn()/setModeTerrainView 도 시도.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_")]
        print("[PROBE] %s: %s" % (title, ", ".join(ms[:30])))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e)); return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

gc_db = None
try:
    gc_db = DataManager.database().data(Data.Type.GlobularClusterType, "Omega Centauri")
except Exception as e:
    print("   DB 실패: %s" % e)

# ── AdvancedCamera 확보 방법 프로브 ──────────────────────────
print("=" * 55); print("ACT 0: AdvancedCamera 확보 시도"); print("=" * 55)
ac = None
try:
    probe("AdvancedCamera 클래스", AdvancedCamera)
    # 여러 생성 패턴 시도
    for maker in ("no-arg", "MainCamera", "index0"):
        try:
            if maker == "no-arg":
                ac = AdvancedCamera()
            elif maker == "MainCamera" and hasattr(AdvancedCamera, "AdvancedCameraName"):
                ac = AdvancedCamera(AdvancedCamera.AdvancedCameraName.MainCamera)
            elif maker == "index0" and hasattr(AdvancedCamera, "AdvancedCameraName"):
                ac = AdvancedCamera(AdvancedCamera.AdvancedCameraName(0))
            if ac is not None:
                print("   AdvancedCamera 확보 (%s)" % maker); break
        except Exception as e:
            print("   %s 실패: %s" % (maker, e))
except Exception as e:
    print("   AdvancedCamera 접근 실패: %s" % e)

# ── 무대 + FadeTo 성단 ───────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(-31.0, -71.0, 2400.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 5, 1, 3, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))
gc = GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)
gc.setIntensity(1.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(2.0)

if gc_db is not None:
    act = gc_db.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("성단으로 (FadeTo)"); t1.setIntensity(1.0, Anim(0.8))
        act.trigger(); sleep(6.0)
        gc.setScale(50.0, Anim(3.0))          # 성단 크게(날아들 대상 확보)
        sleep(3.5)
        t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

def readR():
    try:
        return cam.positionLBR.z
    except Exception:
        return None

# ── 비행 시도 1: setModeFreeFly + zoom ──────────────────────
print("=" * 55); print("비행 시도: setModeFreeFly + zoom"); print("=" * 55)
if ac is not None:
    try:
        t1.setText("성단 속으로 — 비행 (free fly + zoom)"); t1.setIntensity(1.0, Anim(0.6))
        print("   before positionLBR.z =", readR())
        ac.setModeFreeFly(); sleep(0.5)
        ac.zoom(5.0)                           # 전진 (looking point 로 접근)
        for i in range(6):
            sleep(1.5)
            print("   zoom 중 R =", readR())
        ac.stop()
        print("   after positionLBR.z =", readR())
        print("   ★ 성단 속으로 날아 들어갔나? (R/화면 변화)")
    except Exception as e:
        print("   free-fly zoom 실패: %s" % e)
    # 보조: move() 전진
    try:
        t1.setText("보조: move() 전진")
        ac.move(Vec2(0.0, 5.0)); sleep(4.0); ac.stop()
        print("   move 후 R =", readR())
    except Exception as e:
        print("   move 실패: %s" % e)
    # 보조: takeOffOn
    try:
        t1.setText("보조: takeOffOn()")
        ac.takeOffOn(); sleep(3.0)
        print("   takeOffOn 후 R =", readR())
    except Exception as e:
        print("   takeOffOn 실패: %s" % e)
else:
    print("   AdvancedCamera 없음 → 비행 스크립트 불가. 오퍼레이터 Take off 필요.")

t1.setText("비행 테스트 끝"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: ①AdvancedCamera 확보됐나 ②zoom/move/takeOff 로 성단 속 비행 됐나(R 변화/화면)")

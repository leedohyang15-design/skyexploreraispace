# -*- coding: utf-8 -*-
"""
globular_cluster_v2.py — 성단 프레이밍/확대 찾기 (2026-07-09)
v1 실측: FadeTo 후 R=0(성단 정중앙에 딱 붙음) → setPositionR(읽은값×배율)=0 무효, setScale(5) 미미.
→ 성단은 행성(R=5 도킹)과 다름. 두 경로를 훑어 '보이게' 만든다:
 [A] FadeTo 후 R=0 에서 setPositionR **절대값**(2/5/10 = 성단반지름 배수)로 뒤로 빼 전체 프레이밍.
 [B] setScale 을 크게(15/40/80) — billboard 확대되는지.
어느 쪽이 성단을 제대로 보여주는지 리포트.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

gc_db = None
try:
    gc_db = DataManager.database().data(Data.Type.GlobularClusterType, "Omega Centauri")
    print("   DB Omega Centauri=%s" % (gc_db is not None))
except Exception as e:
    print("   DB 실패: %s" % e)

# ── 무대 (남반구 밤) ─────────────────────────────────────────
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
try:
    orig_scale = gc.scale
except Exception:
    orig_scale = 1.0
print("   성단 원본 scale=%s" % orig_scale)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(2.5)

# ── FadeTo → 성단 프레임 ─────────────────────────────────────
print("=" * 55); print("FadeTo → 프레임 확보"); print("=" * 55)
if gc_db is not None:
    act = gc_db.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("성단 곁으로 (FadeTo)"); t1.setIntensity(1.0, Anim(0.8))
        act.trigger()
        sleep(6.0)
        try:
            print("   FadeTo 후 R=%.4f" % cam.positionLBR.z)
        except Exception:
            pass
        t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

        # [A] 절대 R 로 뒤로 빼며 프레이밍 (성단반지름 배수)
        print("-- [A] setPositionR 절대값 스윕 (뒤로 빼기) --")
        for absR in (2.0, 5.0, 10.0, 20.0):
            t1.setText("[A] R=%.0f (성단반지름 배수)" % absR); t1.setIntensity(1.0, Anim(0.4))
            try:
                cam.setPositionR(absR, Anim.cubic(2.5), -1)
                sleep(3.0)
                print("   요청 R=%.0f → 실제 R=%.4f" % (absR, cam.positionLBR.z))
            except Exception as e:
                print("   R=%.0f 실패: %s" % (absR, e))
            t1.setIntensity(0.0, Anim(0.3)); sleep(0.3)
        print("   ★ [A] 어느 R 에서 성단 전체가 예쁘게 보였나?")
    else:
        print("   FadeTo 미지원")

# ── [B] setScale 크게 (billboard 확대?) ──────────────────────
print("=" * 55); print("[B] setScale 크게"); print("=" * 55)
for sc in (15.0, 40.0, 80.0):
    t1.setText("[B] setScale %.0f배" % sc); t1.setIntensity(1.0, Anim(0.4))
    try:
        gc.setScale(sc, Anim(2.0))
        sleep(2.5)
        print("   setScale(%.0f)" % sc)
    except Exception as e:
        print("   setScale(%.0f) 실패: %s" % (sc, e))
    t1.setIntensity(0.0, Anim(0.3)); sleep(0.3)
print("   ★ [B] setScale 로 성단이 커졌나?")
try:
    gc.setScale(orig_scale, Anim(1.5))
except Exception:
    pass
sleep(1.5)

# ── 마무리 ────────────────────────────────────────────────────
t1.setText("성단 프레이밍 테스트 끝"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: [A] 절대 R 중 성단이 제일 잘 보인 값? / [B] setScale 로 커졌나? / 개별 별 보이나?")

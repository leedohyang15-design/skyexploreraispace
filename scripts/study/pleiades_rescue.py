# -*- coding: utf-8 -*-
"""
pleiades_rescue.py — 플레이아데스 구출 프로브 (2026-07-13)
문제: M45(플레이아데스) LOS 프레임에 붉은 성운이 껴서 성단이 안 보임. 은하수 OFF 로도 안 꺼짐.
목표: 그 붉은 성운의 '레이어'를 찾아 끈다 → 성단(별무리)이 드러나는지 확인.

절차: Pleiades 프레임 진입(적당 거리 = 성단 프레이밍) → 배경을 단계별로 OFF 하며 5초씩 관찰.
  각 단계 자막으로 명시 — '몇 단계에서 붉은 성운이 사라지고 성단이 보였나'만 리포트받으면 됨.
단계: 1)은하수 2)모든 Nebula개체 3)Stars 감광 4)DB Off액션(California/Merope 등)
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

EASE = [0.86, 0.74, 0.66, 0.62]     # 얕게 = 성단 전체 프레이밍(약 100pc)


# ── 무대 ─────────────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st = Stars(Stars.StarsName.StarrySky); st.setIntensity(1.0, Anim(0.0))
mw = Galaxy(Galaxy.GalaxyName.MilkyWay); mw.setIntensity(0.45, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

mdb = None
try:
    mdb = DataManager.database().data(Data.Type.NebulaType, "M45")
    print("NebulaType 'M45' 핸들=%s" % (mdb is not None))
except Exception as e:
    print("DB 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
t1.setText("플레이아데스 구출 — 배경 성운 끄기 실험"); t1.setIntensity(1.0, Anim(1.2))
sleep(2.5)

# ── Pleiades 프레임 진입 + 성단 프레이밍 ────────────────────
if mdb is not None:
    ct = mdb.action(Action.Type.ConnectTo)
    if ct is not None:
        uni.setGlobalIntensity(0.0, Anim(1.2)); sleep(1.4)
        ct.trigger(); sleep(6.5)
        cam.setTargetHeight(90.0, Anim.cubic(2.5)); sleep(2.7)
        try:
            R = cam.positionLBR.z
            print("진입 후 R=%.3e" % R)
            for ratio in EASE:
                cam.setPositionR(cam.positionLBR.z * ratio, Anim(1.3), -1); sleep(1.1)
            print("프레이밍 후 R=%.3e" % cam.positionLBR.z)
        except Exception as e:
            print("프레이밍 실패: %s" % e)
        # 성단 강조
        try:
            Messier(Messier.MessierName.M45).setIntensity(1.0, Anim(1.0))
        except Exception:
            pass
        uni.setGlobalIntensity(1.0, Anim.cubic(2.0))

# ── 기준 관찰 (아무것도 안 끔) ───────────────────────────────
t1.setText("기준 — 지금 붉은 성운이 보이나 (배경)"); t1.setIntensity(1.0, Anim(0.8))
sleep(5.0)


def turn_off_all_nebula():
    n = 0
    for nm in dir(Nebula.NebulaName):
        if nm.startswith("_"):
            continue
        try:
            Nebula(getattr(Nebula.NebulaName, nm)).setIntensity(0.0, Anim(1.0)); n += 1
        except Exception:
            pass
    print("   Nebula 개체 %d개 OFF 시도" % n)


def try_db_off():
    names = ["California Nebula", "NGC 1499", "Merope Nebula", "NGC 1435",
             "Taurus Molecular Cloud", "Barnard 22"]
    for nm in names:
        for tn in ("NebulaType", "DeepSkyObjectType", "NgcType"):
            dt = getattr(Data.Type, tn, None)
            if dt is None:
                continue
            try:
                h = DataManager.database().data(dt, nm)
                if h is None:
                    continue
                a = h.action(Action.Type.Off)
                if a is not None:
                    a.trigger(); print("   DB Off: %s / %s" % (tn, nm))
            except Exception:
                pass


STAGES = [
    ("1) 은하수(Galaxy) OFF", lambda: mw.setIntensity(0.0, Anim(1.5))),
    ("2) 모든 Nebula 개체 OFF", turn_off_all_nebula),
    ("3) Stars 감광 0.25 (배경별 죽이기)", lambda: st.setIntensity(0.25, Anim(1.5))),
    ("4) DB Off 액션 (California/Merope 등)", try_db_off),
]

for label, fn in STAGES:
    print("=" * 55); print(label)
    t1.setText(label); t1.setIntensity(1.0, Anim(0.6))
    try:
        fn()
    except Exception as e:
        print("   실패: %s" % e)
    sleep(5.5)
    print("   ★ 붉은 성운 사라졌나? 성단(별무리) 보이나?")

t1.setText("어느 단계에서 붉은 성운이 꺼지고 성단이 보였나요?"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.2))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: 붉은 성운이 꺼진 단계(1은하수/2Nebula전체/3Stars/4DB) & 그때 플레이아데스 성단이 보였나")

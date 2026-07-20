# -*- coding: utf-8 -*-
"""
messier_m42_center.py — M42 '센터링' 방법 찾기 (2026-07-13)
확정된 사실(진단):
  · NebulaType+"M42" FadeTo = 진입/센터링 안 됨(성운은 제자리, 라벨 구석).
  · DB ScaleUp = 무효. · Messier(enum).setScale = 확대 됨(제자리에서 커짐).
남은 과제: 성운을 화면 '중앙'으로 데려오기. setScale 은 이미 되니 센터링만 되면 끝.

이 스크립트:
  1) M42 DB 핸들이 지원하는 Action.Type 을 '전부 나열' (뭘로 조준/이동 가능한지 확정)
  2) LookAt 시도 → 성운이 중앙으로 오나?
  3) 중앙에 왔다는 가정 하에 setScale 확대 (확인된 방법)
리포트: ①지원 액션 목록(로그) ②LookAt 로 성운이 중앙 오나 ③확대까지 자연스러운가
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 ─────────────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

mdb = None
try:
    mdb = DataManager.database().data(Data.Type.NebulaType, "M42")
    print("NebulaType 'M42' 핸들=%s" % (mdb is not None))
except Exception as e:
    print("DB 실패: %s" % e)
mess = Messier(Messier.MessierName.M42)

# ── 1) 지원 액션 전부 나열 ──────────────────────────────────
print("=" * 55); print("M42 DB 핸들이 지원하는 Action.Type:")
supported = []
if mdb is not None:
    for aname in sorted(dir(Action.Type)):
        if aname.startswith("_"):
            continue
        try:
            at = getattr(Action.Type, aname)
            a = mdb.action(at)
            if a is not None:
                supported.append(aname)
        except Exception:
            pass
    print("   지원: %s" % ", ".join(supported))
else:
    print("   핸들 없음")

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))

# 성운 보이게 (라벨 + 밝기)
try:
    la = mdb.action(Action.Type.LabelOn) if mdb is not None else None
    if la is not None:
        la.trigger()
except Exception:
    pass
try:
    mess.setIntensity(1.0, Anim(1.0))
except Exception:
    pass
t1.setText("M42 — 지금은 구석에 있다 (센터링 시도)"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0)

# ── 2) LookAt 로 센터링 시도 ────────────────────────────────
print("=" * 55); print("2) LookAt 센터링 시도")
t1.setText("LookAt — 성운이 중앙으로 오나?")
did_lookat = False
if mdb is not None:
    for aname in ("LookAt", "ConnectTo", "GoTo"):   # 우선순위: 조준 > 프레임전환 > 비행
        try:
            at = getattr(Action.Type, aname, None)
            a = mdb.action(at) if at is not None else None
            if a is not None:
                print("   %s trigger (조준/이동 시도)" % aname)
                a.trigger(); did_lookat = True
                sleep(5.0)
                try:
                    print("   %s 후 R=%.4f" % (aname, cam.positionLBR.z))
                except Exception:
                    pass
                break
        except Exception as e:
            print("   %s 실패: %s" % (aname, e))
if not did_lookat:
    print("   조준 액션 없음 → 수동 조준 필요")
sleep(1.0)

# ── 3) setScale 확대 (확인된 방법) ──────────────────────────
print("=" * 55); print("3) Messier.setScale 확대")
t1.setText("확대 — 오리온 대성운, 별의 요람"); t1.setIntensity(1.0, Anim(0.8))
try:
    orig = mess.scale
except Exception:
    orig = 1.0
try:
    print("   orig_scale=%s → ×100" % orig)
    mess.setScale(orig * 100.0, Anim.cubic(7.0))
    sleep(7.5)
    print("   ★ 성운이 (중앙에서?) 확대됐나?")
except Exception as e:
    print("   setScale 실패: %s" % e)

# ── 마무리 ───────────────────────────────────────────────────
t1.setText("리포트: 지원액션 목록 / LookAt 로 중앙 왔나 / 확대 자연스럽나"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.2))
try:
    mess.setScale(orig, Anim(1.5))
except Exception:
    pass
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: ①로그의 '지원:' 액션 목록 ②LookAt/ConnectTo/GoTo 중 성운을 중앙으로 데려온 게 있나 "
      "③확대는 됐나(중앙에서면 완성)")

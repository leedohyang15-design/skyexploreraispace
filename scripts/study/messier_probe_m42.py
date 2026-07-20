# -*- coding: utf-8 -*-
"""
messier_probe_m42.py — M42 확대방법 진단 프로브 (2026-07-13)
문제(실측): NebulaType+"M42" FadeTo → R=0 은 됐으나 '들어가지도 확대도 안 함'.
가설: FadeTo 로 띄운 건 NebulaType DB 객체인데, 내가 Messier(enum).setScale 로 '다른 인스턴스'를
      키워서 무효였다. → 확대는 '화면의 그 DB 객체'를 건드려야 한다.

이 프로브는 M42 하나로 여러 확대법을 순서대로 시험 — 어느 게 실제로 커지는지 리포트받는다:
  0) FadeTo 후 객체 보이게: DB LabelOn + Messier.setIntensity (어디 있는지 확인)
  A) DB 액션 ScaleUp 반복 (화면 DB 객체 직접 확대)  ← 유력
  B) Messier(enum).setScale ×80 (기존 방식, 대조군)
각 구간 자막으로 명시. "A/B 중 뭐가 커졌나 / 라벨은 보이나"만 알려주면 됨.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

NAME = "M42"


def try_action(h, atype_name, label):
    """DB 액션 하나 시도(있으면 trigger). 반환 True=실행됨."""
    try:
        at = getattr(Action.Type, atype_name, None)
        if at is None:
            print("   %s: Action.Type.%s 없음" % (label, atype_name)); return False
        a = h.action(at)
        if a is None:
            print("   %s: 미지원(None)" % label); return False
        a.trigger(); print("   %s: trigger OK" % label); return True
    except Exception as e:
        print("   %s 실패: %s" % (label, e)); return False


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

# DB 핸들 선확보 (NebulaType + M42 = 확정)
mdb = None
try:
    mdb = DataManager.database().data(Data.Type.NebulaType, NAME)
    print("NebulaType '%s' 핸들=%s" % (NAME, mdb is not None))
except Exception as e:
    print("DB 실패: %s" % e)
mess = Messier(Messier.MessierName.M42)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("M42 확대방법 진단"); t1.setIntensity(1.0, Anim(1.2))
sleep(3.0)

# ── FadeTo ───────────────────────────────────────────────────
print("=" * 55); print("FadeTo (NebulaType/M42)")
if mdb is not None:
    fa = mdb.action(Action.Type.FadeTo)
    if fa is not None:
        t1.setText("FadeTo — 오리온 대성운으로"); fa.trigger(); sleep(6.0)
        try:
            print("   FadeTo 후 R=%.4f" % cam.positionLBR.z)
        except Exception:
            pass

# ── 0) 객체 보이게: 라벨 + 밝기 ─────────────────────────────
print("-- 0) 객체 가시화 (LabelOn + setIntensity) --")
t1.setText("0) 라벨/밝기 ON — 성운이 어디 보이나?")
if mdb is not None:
    try_action(mdb, "LabelOn", "LabelOn")
    try_action(mdb, "On", "On")
try:
    mess.setIntensity(1.0, Anim(1.5))
except Exception as e:
    print("   setIntensity 실패: %s" % e)
sleep(5.0)

# ── A) DB ScaleUp 반복 ──────────────────────────────────────
print("-- A) DB 액션 ScaleUp ×5 --")
t1.setText("A) DB ScaleUp — 이 방법으로 커지나?")
okA = False
for i in range(5):
    if try_action(mdb, "ScaleUp", "ScaleUp#%d" % (i + 1)):
        okA = True
    sleep(1.2)
sleep(3.0)
print("   ★ A(ScaleUp) 로 성운이 커졌나?  (실행됨=%s)" % okA)
# 되돌리기
for i in range(5):
    try_action(mdb, "ScaleDown", "ScaleDown#%d" % (i + 1)); sleep(0.6)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── B) Messier.setScale ×80 (대조군) ────────────────────────
print("-- B) Messier(enum).setScale ×80 --")
t1.setText("B) Messier.setScale ×80 — 이건 커지나?"); t1.setIntensity(1.0, Anim(0.6))
try:
    orig = mess.scale
except Exception:
    orig = 1.0
try:
    print("   orig_scale=%s → ×80" % orig)
    mess.setScale(orig * 80.0, Anim.cubic(6.0))
    sleep(6.5)
    print("   ★ B(setScale) 로 성운이 커졌나?")
    mess.setScale(orig, Anim(1.5)); sleep(1.6)
except Exception as e:
    print("   setScale 실패: %s" % e)

# ── 마무리 ───────────────────────────────────────────────────
t1.setText("진단 끝 — A(ScaleUp)와 B(setScale) 중 뭐가 커졌나요?"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.2))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: ①FadeTo 후 성운이 화면에 보이나(라벨 위치?) "
      "②A(DB ScaleUp)로 커졌나 ③B(Messier.setScale)로 커졌나 ④둘 다 안 되면 아무 변화 없었나")

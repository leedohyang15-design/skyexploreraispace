# -*- coding: utf-8 -*-
"""
globular_cluster.py — 오메가 센타우리 v1 (2026-07-09)
새 예제: 처음 연습하는 GlobularCluster 클래스 (구상성단).
소재: NGC 5139 오메가 센타우리 — 우리은하 최대 구상성단(별 약 1천만 개).

★ 새 API: GlobularClusterName(NGC5139_omegaCen 등) / setIntensity / setLabelIntensity /
   setScale / setPointerType / portId. DB = Data.Type.GlobularClusterType.
확정 레시피 적용: DB FadeTo 로 프레임 확보 → setPositionR(읽은값×배율, -1) 매끄러운 줌 (선형+잘게).
                 slot setScale 로 그 자리 확대도 시도.

무대: 지상(남쪽 하늘) → 성단 클로즈업.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d): %s" % (title, len(ms), ", ".join(ms[:40])))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e)); return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 프로브 ────────────────────────────────────────────────────
print("=" * 60); print("ACT 0: GlobularCluster 프로브"); print("=" * 60)
if hasattr(GlobularCluster, "GlobularClusterPort"):
    probe("GlobularClusterPort", GlobularCluster.GlobularClusterPort)
gc_db = None
try:
    for nm in ("Omega Centauri", "NGC 5139", "omega Cen", "NGC5139", "Centauri"):
        d = DataManager.database().data(Data.Type.GlobularClusterType, nm)
        print("   DB '%s' → %s" % (nm, "found" if d is not None else "None"))
        if d is not None and gc_db is None:
            gc_db = (nm, d)
except Exception as e:
    print("   DB 조회 실패: %s" % e)

# ── 무대: 지상 남쪽 하늘 (남반구 관측지) ─────────────────────
print("=" * 60); print("ACT 1: 무대 (남반구 — 오메가 센타우리 남중)"); print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(-31.0, -71.0, 2400.0))    # 칠레 (남반구 천문대)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 5, 1, 3, 0, 0, tz, Anim(0.5))   # 5월 새벽 = 남중
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))

# 슬롯 성단 핸들 (표시 강조용)
gc = GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)
gc.setIntensity(1.0, Anim(0.0))
try:
    gc.setLabelIntensity(0.8, Anim(0.0))
except Exception:
    pass

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("오메가 센타우리 — 별 1천만 개의 구슬"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
# 성단 위치 포인터 (내장 포인터)
try:
    gc.setPointerType(Body.PointerType.Model2Bold)
    gc.setPointerIntensity(1.0, Anim(1.5))
    print("   성단 내장 포인터 ON")
except Exception as e:
    print("   포인터 스킵: %s" % e)
sleep(3.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 성단 속으로 (DB FadeTo → 줌) ─────────────────────────────
print("=" * 60); print("ACT 2: 성단 클로즈업 (FadeTo + 줌)"); print("=" * 60)
if gc_db is not None:
    nm, d = gc_db
    act = d.action(Action.Type.FadeTo)
    if act is None:
        act = d.action(Action.Type.GoTo)
    if act is not None:
        t1.setText("성단 속으로 — 별들이 촘촘한 도시"); t1.setIntensity(1.0, Anim(0.8))
        try:
            gc.setPointerIntensity(0.0, Anim(0.5))
        except Exception:
            pass
        act.trigger()
        sleep(6.0)
        try:
            p = cam.positionLBR
            print("   FadeTo 후 R=%.3e → 줌인" % p.z)
            # 매끄러운 줌 (선형+잘게)
            target = p.z * 0.15
            step = 0
            while cam.positionLBR.z > target * 1.2 and step < 30:
                r = max(cam.positionLBR.z * 0.6, target)
                cam.setPositionR(r, Anim(1.2), -1)
                sleep(1.25); step += 1
            print("   줌 완료 R=%.3e (%d단계)" % (cam.positionLBR.z, step))
        except Exception as e:
            print("   줌 실패: %s" % e)
        print("   ★ 성단이 커지며 개별 별이 보이나?")
        sleep(2.0)
        t1.setIntensity(0.0, Anim(0.8))
    else:
        print("   FadeTo/GoTo 미지원")
else:
    print("   DB 핸들 없음 → [PROBE]의 이름 확인 필요")

# ── ACT 3: setScale 로 그 자리 확대 (billboard 확대?) ────────
print("=" * 60); print("ACT 3: setScale 확대 시도"); print("=" * 60)
try:
    t1.setText("100억 년을 함께 돈 늙은 별들"); t1.setIntensity(1.0, Anim(0.8))
    orig = None
    try:
        orig = gc.scale
    except Exception:
        pass
    gc.setScale(5.0, Anim(3.0))
    sleep(4.0)
    print("   ★ setScale 로 성단이 커졌나?")
    if orig is not None:
        gc.setScale(orig, Anim(2.0))
    sleep(2.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   setScale 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("오메가 센타우리 — 우리은하가 삼킨 왜소은하의 심장?"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①[PROBE] DB 이름/포트 ②지상서 성단 보임+포인터 ③FadeTo 줌 R ④개별 별 보이나 ⑤setScale 확대")

# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  probe_ground_rocket.py — "지상에서 로켓이 왜 안 보이나" 판별 (약 1분 20초)
#
#  ⚠️ 나는 이걸 다섯 번 감으로 고쳤다(배율 5.5e4→3.6e3→50→150, 거리 333→6.6→11km,
#     조준 setOrientationH→heading 읽기). 전부 틀렸다. 이제 **한 번에 가른다.**
#
#  판별 설계 — 내 규칙대로 **패턴으로 갈리게** 만든다:
#    · 로켓을 **8방위에 동시에** 세운다. 어디를 보고 있든 **한두 개는 반드시 화면에 들어온다.**
#      → 하나도 안 보이면 = **조준 문제가 아니라 '지상에서 렌더 자체가 안 되는' 것.**
#      → 몇 개가 보이면 = **렌더는 되고 조준만 틀린 것.** 어느 방위인지도 같이 알 수 있다.
#    · **동서남북 표지를 켠다**(검증된 `Place2D.setCardinalPointsIntensity`).
#      → 스샷 한 장으로 **카메라가 어느 방위를 보고 있는지**가 그대로 읽힌다.
#
#  단계 A = **검증된 경로**(reset + 지상 재세팅). v10 에서 로켓이 보였던 그 경로다.
#  단계 B = **쇼가 실제로 쓰는 경로**(우주에서 R→0 수동 낙하, reset 없음).
#    → A 는 보이고 B 는 안 보이면 → **수동 낙하가 원인.** 쇼를 reset 경로로 되돌린다.
#    → 둘 다 보이면 → **조준만 문제.** B 스샷의 표지로 어느 방위인지 확정해서 그 자리에 놓는다.
#    → 둘 다 안 보이면 → **지상 Insert3D 렌더 불가.** 로켓을 포기하거나 Insert2D 로 대체한다.
#
#  ★ 사용자에게 필요한 것: **스샷 2장(A 끝, B 끝)**. 그리고 로그의 `[A]`/`[B]` 줄.
# ─────────────────────────────────────────────────────────────
from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "ariane5.osg"
LAT, LON = 5.2, -52.8            # 쿠루
ALT_M = 300.0
DIST_KM = 11.0
SCALE = 150.0                    # 높이 8.4 km — 11 km 앞이면 겉보기 앙각 0→37°
SLOTS = (20, 21, 22, 23, 24, 25, 26, 27)      # 8방위용 Insert3D 슬롯
AZ8 = (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0)   # 나침반 방위(북=0)
NAMES = ("북", "북동", "동", "남동", "남", "남서", "서", "북서")


def feat(o, fn, *a):
    try:
        getattr(o, fn)(*a)
        return True
    except Exception as e:
        print("   x %s: %s" % (fn, e))
        return False


def dark(sec=0.0):
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def load(slot):
    ins = Insert3D(Insert3D.Insert3DName(slot))
    feat(ins, "setModelFilename", MODEL)
    for _ in range(30):
        try:
            if str(ins.loadingStatus).find("Loaded") >= 0:
                break
        except Exception:
            pass
        sleep(0.4)
    return ins


def clear_all():
    for i in range(0, 40):
        try:
            Insert3D(Insert3D.Insert3DName(i)).setIntensity(0.0, Anim(0.0))
        except Exception:
            pass


def place_ring(rockets):
    """★ 8방위에 로켓을 동시에 세운다. 어디를 보든 몇 개는 화면에 들어와야 정상."""
    dd = DIST_KM / 6378.0                       # 지구반지름 단위 각거리
    coslat = max(0.2, math.cos(math.radians(LAT)))
    for i, r in enumerate(rockets):
        az = math.radians(AZ8[i])
        la = LAT + math.degrees(dd * math.cos(az))
        lo = LON + math.degrees(dd * math.sin(az) / coslat)
        feat(r, "setScale", SCALE, Anim(0.0))
        feat(r, "setShadowStrength", 0.0, Anim(0.0))
        feat(r, "setOrientationHPR", Vec(lo + 180.0, 90.0, 0.0), Anim(0.0))
        feat(r, "setParent", earth.portId(Planet.PlanetPort.EquatorialSynchronous))
        feat(r, "setPositionLBR", Vec(lo, la, 1.0), Anim(0.0))
        feat(r, "setIntensity", 1.0, Anim(0.0))


def ground_setup():
    """검증된 지상 세팅 — 대기 ON, 지면 ON(착지 장면이므로), 동서남북 표지 ON."""
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT_M))
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    feat(earth, "setElevationScale", 0.0)
    # ★ 동서남북 표지 — 스샷에서 '어느 방위를 보고 있나'를 그대로 읽으려고 켠다(검증된 세터)
    feat(Place2D(Place2D.Place2DName(0)), "setCardinalPointsIntensity", 1.0, Anim(0.0))
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2010, 6, 26, 15, 0, 0, tz, Anim(0.0))     # 쿠루 현지 정오 무렵 = 밝다


def report(tag):
    try:
        h = cam.orientationHPR
        print("[%s] orientationHPR = (%.2f, %.2f, %.2f)  → 이 값이 맞다면 방위 = %.1f"
              % (tag, h.x, h.y, h.z, 180.0 - h.x))
    except Exception as e:
        print("[%s] orientationHPR 읽기 실패: %s" % (tag, e))
    try:
        p = cam.positionLBR
        print("[%s] positionLBR = (%.3f, %.3f, %.5f)" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("[%s] positionLBR 읽기 실패: %s" % (tag, e))


txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 20, 0))
txt.setSize(0.05)
txt.setColor(Vec(1.0, 1.0, 0.5))
txt.setDistance(1.0, Anim(0.0))
txt.setIntensity(1.0, Anim(0.0))

print("=== probe_ground_rocket — 로켓 8개를 8방위에 세워 한 번에 가른다 ===")
print("    모델: %s / 배율 %.0f(높이 %.1f km) / 거리 %.1f km / 관측지 고도 %.0f m"
      % (MODEL, SCALE, 56.2 * SCALE / 1000.0, DIST_KM, ALT_M))

# ══ 단계 A : 검증된 경로 (reset + 지상 재세팅) ═══════════════════
try:
    dark()
    SceneGraph().reset(1)
    dark(1.5)
    clear_all()
    dark()
    ground_setup()
    rockets = [load(s) for s in SLOTS]
    place_ring(rockets)
    cam.setOrientationH(90.0, Anim(0.0))      # 동쪽
    dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    dark()
    txt.setText("A  reset 경로 - 8방위 로켓")
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    sleep(2.0)
    report("A")
    print("[A] ★ 지금 화면을 찍어 주세요 — 로켓이 몇 개 보이는지, 표지(동서남북) 어디에 있는지")
    sleep(14.0)
except Exception as e:
    print("A 오류:", e)

# ══ 단계 B : 쇼가 쓰는 경로 (우주에서 수동 낙하, reset 없음) ═════
try:
    txt.setText("B  낙하 경로 - 준비")
    dark()
    SceneGraph().reset(1)
    dark(1.5)
    clear_all()
    dark()
    ground_setup()                     # 지상 세팅은 미리(쇼와 동일)
    # 우주로 올라간다
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(20):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    sp = earth.portId(Planet.PlanetPort.EquatorialSynchronous)

    rockets = [load(s) for s in SLOTS]
    place_ring(rockets)

    cam.setPositionLBR(Vec(LON, LAT, 3.4), Anim(0.0), sp)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), sp)
    dark()
    txt.setText("B  낙하 경로 - 하강")
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    sleep(1.5)
    report("B-공중")

    # ★ 쇼와 똑같은 수동 낙하 (reset 없음)
    _h = 0.0
    try:
        _h = cam.orientationHPR.x
    except Exception:
        pass
    cam.setPositionLBR(Vec(LON, LAT, 1.05), Anim.cubic(5.0), -1)
    sleep(5.5)
    cam.setPositionLBR(Vec(LON, LAT, 0.0), Anim.cubic(6.0), -1)
    cam.setOrientationHPR(Vec(_h, 0.0, 0.0), Anim.cubic(6.0))
    sleep(7.0)

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT_M))
    cam.setTargetHeight(30.0, Anim(0.0))
    txt.setText("B  낙하 착지 - 조준 안 함")
    sleep(1.5)
    report("B-착지")
    print("[B] ★ 지금 화면을 찍어 주세요 — 로켓이 보이는지 / 표지가 어디에 있는지")
    sleep(12.0)

    # B-2 : 여기서 setOrientationH 가 먹는지 본다 (한 바퀴 돌려 본다)
    txt.setText("B2  setOrientationH 한 바퀴")
    for a in (0.0, 90.0, 180.0, 270.0, 0.0):
        cam.setOrientationH(a, Anim(1.6))
        sleep(2.0)
    report("B2")
    print("[B2] ★ 화면이 돌았습니까? 돌았으면 setOrientationH 는 살아 있다.")
    sleep(6.0)
except Exception as e:
    print("B 오류:", e)

txt.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(2.0))
sleep(2.5)
print("=== 끝. 스샷 2~3장(A 끝 / B 착지 / B2)과 로그의 [A][B][B2] 줄을 보내 주세요 ===")

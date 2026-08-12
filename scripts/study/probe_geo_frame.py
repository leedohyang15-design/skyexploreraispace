# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 이 파일이 검증 도구다. 화면에서 본 것이 곧 결과다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  [프로브] 정지궤도 쇼의 프레임을 확정한다 — 네 번 틀렸으니 이번엔 먼저 잰다
#
#  천리안 쇼가 돔에서 네 번 깨졌고, 그중 프레임 문제만 세 번이다:
#    · v2: 관성 프레임으로 **위치만** 옮기고 조준을 안 옮겨 화면이 통째로 비었다
#    · v3: 되돌렸더니 도킹 프레임(EquatorialSynchronous)이라 **지구가 멈추고 하늘이 돌았다**
#          ("지구는 가만히 두고 왜 우주를 돌리냐")
#    · v4: 거기에 위성을 손으로 밀면서 시간가속까지 걸어 **삼중 구동 → 급발진**
#
#  가설: 정지궤도 위성은 **동기 프레임(EquatorialSynchronous)** 에 놓는 게 맞다.
#        그 프레임의 경도 = 지구 경도이므로 **128.2 를 넣으면 한국 위에 자동으로 붙는다.**
#        손으로 밀 필요가 없고, 지구가 돌면 같이 돈다. RATE·tick 기계장치가 통째로 사라진다.
#        카메라는 **관성 프레임 + 재조준 두 줄**로 옮겨야 지구가 도는 게 보인다.
#
#  네 가지를 순서대로 본다 (약 100초)
#    A  관성 프레임 + 재조준 → **지구가 도는가**(하늘이 아니라)
#    B  동기 프레임 위성 → **한국 위에 있고 지구와 같이 도는가**
#    C  궤도선만 → **끊겨 보이는가**(v4 에서 "궤도 이상하게 끊겨있다"고 했다)
#    D  동기 프레임에서 위성으로 **진짜 줌인** → 중앙에 유지되는가
#
#  ⚠️ 자막은 우주 슬롯(5)만 쓰고 setSize 를 부르지 않는다(이걸로 두 번 죽었다).
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

RUN_A = True
RUN_B = True
RUN_C = True
RUN_D = True

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "chollian.osg"
EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M        # 6.611 지구반지름
KOREA_LON = 128.2                     # 천리안 1호의 정지궤도 경도
B_TOP, R_VIEW = 88.0, 8.0

txt = None
ip = None                             # 관성(EquatorialJ2000)
sp = None                             # 동기(EquatorialSynchronous)


def line(t):
    print("\n" + "=" * 68)
    print(t)
    print("=" * 68)


def dark(sec=0.0):
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


def sub():
    """우주 자막 — 슬롯 5. ⚠️ setSize 를 절대 부르지 않는다."""
    t = InsertText(InsertText.InsertTextName(5))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setColor(Vec(1.0, 1.0, 0.6))
    t.setDistance(20.0, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


def load_model(slot):
    ins = Insert3D(Insert3D.Insert3DName(slot))
    path = MODEL
    try:
        import os
        u = Configuration.configuration().localUserFolder
        if u:
            path = os.path.join(u, MODEL)
    except Exception:
        pass
    ins.setModelFilename(path)
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        try:
            if "Loaded" in str(ins.loadingStatus):
                return ins
        except Exception:
            pass
    print("   ⚠️ 모델 로드 실패 — %s" % path)
    return ins


def hud():
    try:
        p = cam.positionLBR
        print("   HUD  L=%.2f  B=%.2f  R=%.3f (%.0f km)"
              % (p.x, p.y, p.z, p.z * EARTH_R_M / 1000.0))
    except Exception as e:
        print("   HUD 읽기 실패:", e)


# ══ 진입 — FadeTo 지구 + 렌더 복구 ═════════════════════════════
dark()
SceneGraph().reset(1)
dark(1.5)
try:
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # 지구가 보이게 (지상 쇼가 껐을 수 있는 것들 복구)
    for fn, v in (("setIntensity", 1.0), ("setTerrainIntensity", 1.0),
                  ("setAtmosphereIntensity", 1.0), ("setCloudsIntensity", 0.35),
                  ("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    dark()

    ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
    sp = None
    for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
        try:
            sp = earth.portId(getattr(Planet.PlanetPort, nm))
            print("동기 프레임 포트 OK:", nm)
            break
        except Exception:
            continue
    if sp is None:
        print("⚠️ 동기 프레임 포트를 못 찾았다 — B/D 단계가 무의미해진다")

    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))   # 청주 정오 = 03:30 UTC
    dark()
    sleep(0.4)
    txt = sub()
except Exception as e:
    print("진입 오류:", e)


# ══ A. 관성 프레임 + 재조준 — 지구가 도는가 ════════════════════
if RUN_A:
    line("A. 관성 프레임 + 재조준 → 지구가 도는가 (하늘이 아니라)")
    try:
        dark()
        # ⚠️⚠️ 검증된 전환 레시피는 **두 줄**이다. v2 는 아래 두 번째 줄을 빠뜨려 화면을 날렸다.
        cam.setPositionLBR(Vec(0.0, B_TOP, R_VIEW), Anim(0.0), ip)
        feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), ip)
        dark()
        cam.setTargetHeight(30.0, Anim(0.0))
        dark()
        txt.setText("A — 지구가 도는가? (하늘이 아니라)")
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
        hud()
        # 반나절을 20초에 — 지구가 반 바퀴
        dm.setDateTime(2026, 8, 12, 15, 30, 0, tz, Anim(20.0))
        sleep(22.0)
        hud()
    except Exception as e:
        print("A 오류:", e)


# ══ B. 동기 프레임 위성 — 한국 위인가 ══════════════════════════
if RUN_B:
    line("B. 동기 프레임 위성 → 한국 위에 붙어 지구와 같이 도는가")
    try:
        ins = load_model(6)
        feat(ins, "setShadowStrength", 0.0, Anim(0.0))
        feat(ins, "setScale", 1.0e6, Anim(0.0))          # 반지름 약 5,270km
        feat(ins, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
        # ★ 핵심 — 동기 프레임의 경도 = 지구 경도. 128.2 를 넣으면 한국 위.
        if sp is not None:
            feat(ins, "setParent", sp)
            feat(ins, "setPositionLBR", Vec(KOREA_LON, 0.0, GEO_R), Anim(0.0))
        else:
            feat(ins, "setParent", ip)
            feat(ins, "setPositionLBR", Vec(0.0, 0.0, GEO_R), Anim(0.0))
        feat(ins, "setIntensity", 1.0, Anim(1.0))
        txt.setText("B — 위성이 한반도 위에 붙어 같이 도는가?")
        # 하루를 24초에 — 위성이 지구와 함께 한 바퀴 (손으로 밀지 않는다)
        dm.setDateTime(2026, 8, 13, 15, 30, 0, tz, Anim(24.0))
        sleep(26.0)
        hud()
    except Exception as e:
        print("B 오류:", e)


# ══ C. 궤도선 — 끊겨 보이는가 ══════════════════════════════════
if RUN_C:
    line("C. 궤도선만 → 끊겨 보이는가")
    try:
        o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(0))
        feat(o, "setParent", ip)
        feat(o, "setMeanMotion", 1.0027, Anim(0.0))
        feat(o, "setEccentricity", 0.0002, Anim(0.0))
        feat(o, "setInclination", 0.1, Anim(0.0))
        feat(o, "setAscendingNodeLongitude", 0.0, Anim(0.0))
        feat(o, "setArgumentOfPeriapsis", 0.0, Anim(0.0))
        feat(o, "setMeanAnomaly", 0.0, Anim(0.0))
        sleep(0.4)
        feat(o, "setOrbitColor", Vec(1.0, 0.78, 0.28))
        feat(o, "setOrbitThickness", 1.5)
        feat(o, "setOrbitIntensity", 1.0, Anim(1.0))

        txt.setText("C-1 — 궤도선 + 위성. 궤도가 끊겨 보이나?")
        sleep(8.0)
        # 위성을 끄고 궤도선만 — 끊김이 위성 가림 때문인지 가른다
        feat(ins, "setIntensity", 0.0, Anim(1.0))
        txt.setText("C-2 — 위성 끔. 이제도 끊겨 보이나?")
        sleep(8.0)
        feat(o, "setOrbitThickness", 3.0)
        txt.setText("C-3 — 굵기 3.0. 나아지나?")
        sleep(8.0)
        feat(ins, "setIntensity", 1.0, Anim(1.0))
    except Exception as e:
        print("C 오류:", e)


# ══ D. 진짜 줌인 — 동기 프레임에서 위성으로 다가간다 ═══════════
if RUN_D:
    line("D. 진짜 줌인 — 카메라가 위성 쪽으로 (setScale 확대가 아니라)")
    try:
        dark()
        if sp is not None:
            # 위성과 같은 경도·위도의 바깥쪽에 선다 → 위성이 카메라와 지구 사이에 놓인다
            cam.setPositionLBR(Vec(KOREA_LON, 0.0, 9.0), Anim(0.0), sp)
            feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), sp)
            dark()
            cam.setTargetHeight(30.0, Anim(0.0))
        dark()
        txt.setText("D — 지금 위성이 화면 가운데 있나?")
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
        hud()
        sleep(6.0)
        txt.setText("D — 다가간다 (12초)")
        if sp is not None:
            cam.setPositionLBR(Vec(KOREA_LON, 0.0, 7.6), Anim(12.0), sp)
        sleep(13.0)
        hud()
        txt.setText("D — 커졌나? 중앙에 남아 있나?")
        sleep(6.0)
        txt.setIntensity(0.0, Anim(1.5))
        sleep(1.5)
    except Exception as e:
        print("D 오류:", e)


line("프로브 종료 — 네 가지만 알려주세요")
print("A) 지구가 도는가 (하늘이 도는 게 아니라)")
print("B) 위성이 한반도 위에 붙어 지구와 같이 도는가")
print("C) 궤도선이 끊겨 보이는가 — C-1(위성 있음) / C-2(위성 끔) / C-3(굵게) 중 언제")
print("D) 위성이 화면 중앙에 있었고, 다가가면서 커졌는가")

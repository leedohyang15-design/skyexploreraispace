# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인(v5) — 돔 재생 4회 + 프레임 프로브 1회.
#    프로브(scripts/study/probe_geo_frame.py, 2026-08-12 사용자 확인)로 **확정된 것**:
#      ✅ A 관성 프레임 + **재조준 두 줄** → 지구가 돈다(하늘이 아니라)
#      ✅ B **동기 프레임 경도 128.2** 에 놓은 위성이 한반도 위에 붙어 지구와 함께 돈다
#      ✅ D 동기 프레임에서 위성으로 **진짜 줌인**이 된다(중앙 유지)
#      ❌ C **궤도선(OrbitalPlace)이 끊겨 보인다** — 위성을 꺼도, 굵기를 3.0 으로 올려도 끊긴다
#         → **원인 확정(2026-08-12)**: `setBstar`·`setEpochYears` 누락. 대기저항이 0 이 아니면
#           궤도가 감쇠하며 닫히지 않는 나선이 된다. 두 줄을 넣어 막5 에 되살렸다.
#    ⚠️ **v7 은 1인칭으로 다시 짰고, 아래 넷은 아직 돔에서 못 봤다**:
#       발사 고도 R=1.6 · 동쪽 표류(경도 애니) · 시각 역방향 흐름 · 막4 그림자 ON + 도시광.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "천리안 1호 — 여정과 마감"   (약 5분)
#
#  ★ 어린이·가족 관람객.  ★ 스크립트는 **무음** — 나레이션·음악은 오퍼레이터가 입힌다.
#    대본과 큐시트: docs/27_chollian_narration.md
#
#
#  ⚠️⚠️⚠️ 규칙 1 — 자막 슬롯을 절대 섞지 마라
#     지상 = `setSize(0.052)` + `setDistance(1.0)` / 우주 = **크기를 만지지 말고** `setDistance(20)`
#     ⚠️ 크기를 되돌리는 API 가 **없다.** 그래서 핵심은 '`setSize` 를 안 부르는 것'이 아니라
#        **'슬롯을 갈아타는 것'** 이다. 지상 슬롯을 우주에서 재사용하면 크기가 남아 자막이 사라진다.
#        (이걸로 두 번 죽었다.) → **지상 슬롯 1, 우주 슬롯 5. 끝.**
#
#  ⚠️⚠️⚠️ 규칙 2 — 프레임 세 개를 구분해서 쓴다 (프로브로 확정)
#     · **관성(EquatorialJ2000)** = 카메라의 집. 여기 있어야 **지구가 도는 게 보인다.**
#       FadeTo 도킹 프레임(EquatorialSynchronous)에 그냥 두면 카메라가 자전을 따라 돌아
#       **지구는 멈추고 하늘이 돈다**("지구는 가만히 두고 왜 우주를 돌리냐" — v3·v4 가 이랬다).
#     · ⚠️ 프레임 전환은 **반드시 두 줄**: `setPositionLBR(..., 포트)` **+
#       `setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, 포트)`**.
#       v2 는 두 번째 줄을 빠뜨려 지구·위성이 통째로 화면 밖으로 나갔다.
#     · **동기(EquatorialSynchronous)** = 위성의 집. 이 프레임의 경도 = 지구 경도라서
#       **128.2 를 넣으면 한반도 위에 자동으로 붙는다.** 손으로 밀 필요가 없다.
#       (v4 는 관성 프레임 경도 0 에 박아 두고 손으로 밀면서 시간가속까지 걸어 **삼중 구동 →
#        급발진**했다. 이제 `RATE`·`tick()` 기계장치가 통째로 없다.)
#
#
#  ⚠️⚠️⚠️ 규칙 3 — **이 쇼는 천리안의 1인칭이다** (v7, 사용자 지시)
#     v6 까지는 여섯 막 중 다섯 막이 "밖에서 천리안을 구경하는" 구도였다("너무 관조하는 느낌").
#     → **카메라 = 천리안 그 자체.** 관객은 위성에 올라타 있고, 화면은 위성이 보는 것이다.
#     · 1인칭 막에서는 **위성 모델을 끈다**(우리가 그것이므로 화면에 보이면 안 된다).
#     · 카메라의 집이 **동기 프레임(sp)** 으로 바뀐다 — 정지궤도 위성의 눈은 지구와 함께 돌기 때문에
#       **지구가 안 도는 게 정상이다.** 도는 것처럼 보이면 그건 관성 프레임(=3인칭)이다.
#     · 3인칭은 **막3 하나뿐** — "밖에서 본 우리". 모델을 보여주고 정지궤도를 설명하는 자리다.
#       (설명만은 밖에서 봐야 성립한다: 지구가 돌고 우리가 따라가는 그림.)
#
#  ══ v7 에서 바뀐 것 ══
#
#  ① **발사와 상승이 1인칭이다** — 지구가 발밑에서 멀어진다(R 1.6 → 6.611)
#  ② **동쪽 표류가 들어갔다** — 쿠루(-52.8°E)에서 한반도(128.2°E)까지 지구 위를 흘러간다.
#     ⚠️ 이건 연출이 아니라 실제 절차다(정지위성은 발사장 상공에서 제 자리로 표류해 간다).
#     표류 26초 동안 시각을 **12시간** 흘린다 → 태양이 지표 대비 180° 서쪽으로 가고
#     우리는 181° 동쪽으로 가므로 **낮이 우리를 따라온다**(계산이 맞아떨어진다).
#  ③ **막2·4 가 위성의 눈** — 지구는 안 돌고 구름과 낮밤만 지나간다. 그게 정지궤도의 그림이다
#  ④ **마감도 1인칭** — 우리가 올라간다(R 6.611 → 10.5). 지구가 작아진다. 그 다음에야 밖에서 본다
#  ⑤ 3인칭은 막3 하나로 몰았다 — 모델 클로즈업 + 정지궤도 설명
#
#  구성
#    막0  올려다보기 (관객의 눈)                     (~40초)
#    막1  ★1인칭 — 올라간다, 그리고 자리를 찾아간다  (~62초)
#    막2  ★1인칭 — 우리 눈으로 본 지구              (~58초)
#    막3  3인칭 — 밖에서 본 우리 (모델 + 정지궤도)   (~58초)
#    막4  ★1인칭 — 16년, 낮과 밤                    (~42초)
#    막5  ★1인칭 이탈 → 밖에서 본 자리              (~54초)
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "chollian.osg"

SLOT_GROUND = 1               # 지상 전용. setSize 를 거는 유일한 슬롯
SLOT_SPACE = 5                # 우주 전용. **영원히 setSize 를 부르지 않는다**

# ★ 자막을 통째로 끄는 스위치. 화면만 보고 싶을 때 False.
#   길이·타이밍은 그대로 유지된다(자막이 없어도 같은 박자로 흘러간다).
SHOW_TEXT = False

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
# 무덤궤도 — ⚠️ 실제는 정지궤도 300km 위(0.7% 차이 = 화면에서 안 보인다).
# "이탈할 때 너무 안 보인다"는 지적을 받아 **크게 과장**했다. 나레이션에서 고지한다.
GRAVE_R = 10.5                          # 지구반지름 단위(≈67,000km) — GEO 6.611 대비 59% 바깥
GRAVE_MM = 0.50                         # 그 반지름에 대응하는 평균운동(궤도선용)
KOREA_LON = 128.2                       # 천리안 1호의 정지궤도 경도
LON_2A, LON_2B = 133.0, 123.5           # ⚠️ 실제 2A·2B 도 128.2 부근이지만 겹쳐 보여서 벌렸다

B_TOP = 88.0                  # 북극 위. **각도는 건드리지 않는다**(프레이밍이 깨진 건 늘 각도였다)
R_ORBIT = 8.0                 # 막3 3인칭 조망
R_ZOOM_A, R_ZOOM_B = 10.0, 8.3  # 막3 모델 클로즈업 — 동기 프레임(위성과 같은 경도선 위)
#  ⚠️ 7.6 은 위성까지 6,300km 라 태양전지판 하나가 돔을 다 덮었다(돔 실측).
#     8.3 이면 10,800km — 위성이 화면 절반, 뒤로 지구도 들어온다.

# ★ 1인칭 좌표 — 전부 **동기 프레임(sp)**. 여기서 L = 지구 경도다.
KOURU_LON = -52.8             # 아리안5 발사장(기아나 쿠루). 여정의 출발점
R_LAUNCH = 1.6                # 상승 시작 고도(≈3,800km). 지구 각지름 84° = 발밑을 채운다
#   ⚠️ 첫 번째 조정 손잡이. 너무 가까워 지표가 뭉개지면 1.9~2.2 로 올릴 것.
DRIFT = (10.0, 70.0, KOREA_LON)   # 동쪽 표류 경유점. ⚠️ 한 번에 181° 를 주면
#   엔진이 어느 쪽으로 도는지 모호하다 → **60° 남짓씩 끊어** 방향을 못 박는다.
R_DIVE = 2.2                  # 막2 — 카메라로 당긴 지구(각지름 54°)
# ⚠️⚠️ [2026-08-12 지적 "닌 이게 한국이냐"] 위성은 **적도(위도 0)** 에 있어서
#   그 자리에서 지구를 보면 원반 한가운데가 128.2°E 적도 = **인도네시아 앞바다**다.
#   한국은 위쪽 가장자리로 밀린다. 물리적으론 맞지만 보여주려는 게 한국이니 틀린 그림이다.
#   → 당기면서 **위도를 32°까지 같이 올려** 한반도를 화면 한가운데로 가져온다.
B_DIVE = 32.0
R_NIGHT = 3.0                 # 막4 — 낮밤이 지나가는 걸 보기 좋은 거리(각지름 39°)
B_NIGHT = 25.0
R_BACK = 13.0                 # 막5 — 궤도 두 개가 다 들어오는 거리

SCALE_SAT = 1.0e6             # 반지름 5,270km — 처음에 고른 값(v4 의 5e5 는 "너무 작다")

H_SOUTH, TILT_SOUTH = 0.0, 40.0   # 청주에서 128.2°E 정지위성 = 고도 47.5°, 거의 정남

txt = None
ip = None                     # 관성 — 카메라의 집
sp = None                     # 동기 — 위성의 집
sat = None


def _dark(sec=0.0):
    """암전 클램프. reset/FadeTo 는 밝기를 1.0 으로 되돌리므로 한 번 눌러선 안 된다."""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 글자 수로 자동 계산(2초 + 글자당 0.1초)."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        sleep(hold)


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


class _NoText(object):
    """SHOW_TEXT=False 일 때 자막 자리에 들어가는 빈 껍데기 — 모든 호출을 삼킨다."""
    def __getattr__(self, n):
        def _f(*a, **k):
            return None
        return _f


def sub_ground():
    """지상 자막 — 슬롯 1. **여기서만** setSize 를 부른다."""
    if not SHOW_TEXT:
        return _NoText()
    t = InsertText(InsertText.InsertTextName(SLOT_GROUND))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setSize(0.052)
    t.setColor(Vec(1.0, 1.0, 0.55))
    t.setDistance(1.0, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


def sub_space():
    """우주 자막 — 슬롯 5. ⚠️ **setSize 를 절대 부르지 않는다**(부르면 화면에서 사라진다)."""
    if not SHOW_TEXT:
        return _NoText()
    t = InsertText(InsertText.InsertTextName(SLOT_SPACE))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setColor(Vec(1.0, 1.0, 0.55))
    t.setDistance(20.0, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


def fly(pos, seconds, port):
    """⚠️ 프레임을 옮기거나 그 안에서 움직일 때는 **반드시 두 줄**.
    조준을 같이 안 옮기면 카메라가 대상이 없는 쪽을 본다(v2 가 그렇게 화면을 날렸다)."""
    cam.setPositionLBR(pos, Anim(seconds), port)
    feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(seconds), port)


def stand(pos, port, target=30.0):
    """암전 중에 카메라를 어느 프레임의 어느 자리에 **즉시** 세운다.
    ⚠️ reset/FadeTo 뒤에는 밝기가 1.0 으로 되돌아오므로 단계마다 암전을 다시 누른다."""
    _dark()
    fly(pos, 0.0, port)
    _dark()
    cam.setTargetHeight(target, Anim(0.0))
    _dark()


def load_model(slot):
    """⚠️ 고정 sleep 으로 기다리면 Loading 인 채 지나간다(실측) — Loaded 뜰 때까지 폴링."""
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
    print("   ⚠️ 모델 로드 실패 — %s (유저 폴더에 있는지 확인)" % path)
    return ins


def place_sat(slot, lon, scale=SCALE_SAT):
    """★ 정지궤도 위성 하나 — **동기 프레임의 경도**에 놓는다.
    이 프레임의 경도 = 지구 경도라서 그 자리에 붙고, 지구가 돌면 같이 돈다.
    손으로 밀 필요가 없다(v4 의 '급발진'은 손으로 밀면서 시간가속까지 걸어서 났다)."""
    ins = load_model(slot)
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setScale", scale, Anim(0.0))
    feat(ins, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
    feat(ins, "setParent", sp if sp is not None else ip)
    feat(ins, "setPositionLBR", Vec(lon, 0.0, GEO_R), Anim(0.0))
    return ins


def ring(slot, mm, color, thick=3.0):
    """궤도선 — ⚠️ 가까이서는 끊겨 보인다(프로브 C). **마지막 장면(멀리서)에서만** 쓴다.
    사용자 요청: "궤도선 안 보이는데 마지막은 넣어줬으면". 굵게(3.0) 그린다."""
    o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(slot))
    feat(o, "setParent", ip)
    feat(o, "setMeanMotion", mm, Anim(0.0))
    feat(o, "setEccentricity", 0.0002, Anim(0.0))
    feat(o, "setInclination", 0.1, Anim(0.0))
    feat(o, "setAscendingNodeLongitude", 0.0, Anim(0.0))
    feat(o, "setArgumentOfPeriapsis", 0.0, Anim(0.0))
    feat(o, "setMeanAnomaly", 0.0, Anim(0.0))
    # ⚠️⚠️ [2026-08-12 원인 확정] **궤도가 나선으로 벌어져 안 닫히던 이유가 이 두 줄이 없어서다.**
    #   `setBstar` = 대기저항 항. 0 이 아니면 궤도가 감쇠하며 **닫히지 않는 나선**이 된다.
    #   `setEpochYears` 도 안 걸면 전파 구간이 길어져 더 벌어진다.
    #   검증된 예제(scripts/study/orbital_satellites.py)는 이 둘을 걸고 있었고 우리는 안 걸었다.
    feat(o, "setEpochYears", 2026.0, Anim(0.0))
    feat(o, "setBstar", 0.0, Anim(0.0))
    sleep(0.4)
    feat(o, "setOrbitColor", color)
    feat(o, "setOrbitThickness", thick)
    feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
    return o


def shadows(on):
    """지구 그림자 — 끄면 원반 전체가 밝고(운영 표준), 켜면 낮과 밤이 갈린다.
    ⚠️ 막4 는 **낮밤 자체가 주제**라 운영 표준(그림자 OFF)의 예외로 켠다(위상·일식과 같은 부류)."""
    if on:
        feat(earth, "setShadowStrength", 1.0, Anim(2.0))
        feat(earth, "setShadowContrast", 1.0, Anim(2.0))
        feat(earth, "setPlanetShineStrength", 0.05, Anim(2.0))
        feat(earth, "setNightLightsIntensity", 1.0, Anim(3.0))   # 밤면 도시광(호박색)
    else:
        feat(earth, "setShadowStrength", 0.0, Anim(1.0))
        feat(earth, "setShadowContrast", 0.0, Anim(1.0))
        feat(earth, "setPlanetShineStrength", 1.0, Anim(1.0))
        feat(earth, "setNightLightsIntensity", 0.0, Anim(1.0))


def enter_space():
    """FadeTo 지구 → 지구 렌더 복구 → 프레임 확보. 전 과정 암전.
    ⚠️ **카메라는 여기서 놓지 않는다** — 어디에 설지는 막마다 다르므로 각 막이 직접 fly 한다."""
    global ip, sp
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # ⚠️ 막0 이 지상 하늘 쇼를 위해 꺼 둔 것을 되살린다.
    #    안 하면 지구가 회색 공이 되고, 가까이 가면 그릴 표면이 없어 **아예 사라진다**(실측).
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))       # 구름은 막4 의 비트
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    _dark()

    ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
    for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
        try:
            sp = earth.portId(getattr(Planet.PlanetPort, nm))
            break
        except Exception:
            continue
    if sp is None:
        print("   ⚠️ 동기 프레임 포트를 못 찾았다 — 1인칭이 성립하지 않는다")
    _dark()


# ══ 막0 : 올려다보기 ═══════════════════════════════════════════
_dark()
try:
    SceneGraph().reset(1)
    _dark(1.5)

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))    # 지상 하늘 쇼 = 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))       #               + 지면 OFF
    earth.setElevationScale(0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    _dark()

    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 13, 0, 0, tz, Anim(0.0))    # 청주 22:00 KST = 13:00 UTC
    _dark()
    sleep(0.4)

    cam.setOrientationH(H_SOUTH, Anim(0.0))
    _dark()
    cam.setTargetHeight(TILT_SOUTH, Anim(0.0))
    _dark()

    txt = sub_ground()
    txt.setText("천리안 1호")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
    dm.setDateTime(2026, 8, 12, 15, 0, 0, tz, Anim(35.0))   # 별이 천천히 돈다
    sleep(4.0)
    say("2010년 6월 27일")
    say("남아메리카 쿠루에서 로켓 하나가 하늘로 올라갔다")
    say("우리가 만든 위성이 실려 있었다")
    say("천리안 1호")
    say("지금 남쪽 하늘 저 높이, 16년 동안 자리를 뜨지 않은 것이 있다")
    say("눈에는 안 보인다 — 36,000km 밖이니까")
    # ★ 1인칭으로 넘어가는 문. 여기서부터 관객은 천리안에 올라탄다.
    say("그 위에서는 무엇이 보였을까")
    say("우리가 그 눈이 되어 보자")
except Exception as e:
    print("막0 오류:", e)

# ══ 막1 : ★1인칭 — 올라간다, 그리고 자리를 찾아간다 ════════════
# ⚠️ 여기서부터 **카메라 = 천리안**이다. 그러므로 위성 모델은 화면에 없다(우리가 그것이다).
#    프레임은 **동기(sp)** — 정지위성의 눈은 지구와 함께 돌기 때문에, 이 프레임에서 보면
#    지구는 가만히 있고 우리가 그 위를 올라가고 흘러간다. 그게 물리적으로도 맞는 그림이다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.8))
    sleep(1.0)
    _dark()
    enter_space()

    dm.stop()
    sleep(0.2)
    # 2010-06-27 발사. 15:30 UTC = 쿠루(-52.8°E) 현지 정오 무렵 → 발밑이 낮이다
    dm.setDateTime(2010, 6, 27, 15, 30, 0, tz, Anim(0.0))
    _dark()
    sleep(0.4)

    sat = place_sat(5, KOREA_LON)       # 모델은 미리 올려두되 **꺼 둔다**(1인칭 구간)
    feat(sat, "setIntensity", 0.0, Anim(0.0))
    _dark()

    if sp is not None:
        stand(Vec(KOURU_LON, 0.0, R_LAUNCH), sp)    # ★ 발사 직후 — 남아메리카 상공
    txt = sub_space()                   # ★ 슬롯 5 — 크기를 한 번도 안 건드린 슬롯
    txt.setText("2010년 6월 27일")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
    say("우리는 지금 로켓 꼭대기에 실려 있다", 4.0)
    say("발밑에 보이는 게 남아메리카다", 4.0)

    if sp is not None:
        fly(Vec(KOURU_LON, 0.0, GEO_R), 18.0, sp)   # ★ 1인칭 상승 — 지구가 멀어진다
    say("올라간다", 4.0)
    say("지구가 점점 작아진다", 4.5)
    say("3,000km … 10,000km … 20,000km", 5.0)
    say("36,000km 에서 멈춘다", 5.0)

    # ★ 동쪽 표류 — 실제 절차다(쿠루 상공에서 128.2°E 까지 동쪽으로 흘러가 자리를 잡는다).
    #
    # ⚠️⚠️ **시각을 거꾸로 흘린다. 오타가 아니다 — 고치지 마라.**
    #   태양의 직하점 경도는 시간이 **앞으로** 갈 때 서쪽으로(=경도가 줄며) 간다: dλ/dt = −15°/h.
    #   우리는 **동쪽으로**(경도가 늘며) 181° 간다. 즉 앞으로 흘리면 태양과 우리가 서로 멀어져
    #   **표류 중간쯤에 지구 반대편 = 한밤중**을 지나게 된다(계산: 6시간 뒤 우리 37.7°E, 태양 −142.5°E).
    #   → 12시간을 **거꾸로** 흘리면 λ 태양이 +181° 이동해 우리와 나란히 간다 → **내내 정오** 위를 지난다.
    #   검산: 15:30 UTC 태양 −52.5°E(쿠루 정오) → 03:30 UTC 태양 127.5°E(한반도 정오). 도착도 낮이다.
    dm.setDateTime(2010, 6, 27, 3, 30, 0, tz, Anim(22.0))
    say("이제 자리를 찾아간다", 3.0)
    if sp is not None:
        fly(Vec(DRIFT[0], 0.0, GEO_R), 7.0, sp)
    say("지구 위를 동쪽으로 천천히 흘러간다", 7.0)
    if sp is not None:
        fly(Vec(DRIFT[1], 0.0, GEO_R), 7.0, sp)
    say("아프리카가 지나가고, 인도양이 지나가고", 7.0)
    if sp is not None:
        fly(Vec(DRIFT[2], 0.0, GEO_R), 7.0, sp)
    say("저 앞이 우리가 갈 곳이다 — 동경 128.2도, 한반도 위", 7.0)
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : ★1인칭 — 우리 눈으로 본 지구 ═════════════════════════
# ⚠️ 암전 없이 막1 에서 그대로 이어진다(도착했으니 시점을 끊을 이유가 없다).
#    ★ 이 막의 '줌'은 카메라가 내려가는 게 아니라 **관측 카메라로 당기는 것**이다 —
#      천리안이 실제로 하는 일이 그것이므로 1인칭이 깨지지 않는다.
try:
    say("도착했다. 여기가 16년 동안 우리 자리다", 4.5)
    say("여기서는 지구가 움직이지 않는다", 4.5)
    say("우리가 지구와 같은 속도로 돌기 때문이다 — 이걸 정지궤도라고 한다", 5.0)

    if sp is not None:
        # ★ 관측 카메라로 당긴다 + 위도를 올려 한반도를 화면 한가운데로
        fly(Vec(KOREA_LON, B_DIVE, R_DIVE), 15.0, sp)
    say("우리 눈은 카메라다. 당겨 보자", 5.0)
    say("한가운데가 우리나라다", 5.0)
    say("16년 동안 한 번도 놓치지 않은 그림이다", 5.0)

    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))    # 0→1 이 구름 렌더의 마스터
    feat(earth, "setCloudSpeed", 3.0)
    # ⚠️ 동기 프레임이라 시간이 흘러도 **지구는 안 돈다** — 구름만 흐른다
    dm.setDateTime(2010, 7, 2, 3, 30, 0, tz, Anim(32.0))
    say("바뀌는 건 구름뿐이다", 4.0)
    say("우리가 한 일은 세 가지였다", 4.0)
    say("첫째, 날씨 — 태풍이 어디로 갈지, 비가 언제 올지", 5.0)
    say("둘째, 통신을 이어 줬다", 4.0)
    say("셋째, 바다를 봤다 — 하루 여덟 번", 4.5)
    say("정지궤도에서 바다를 본 건 세계에서 우리가 처음이었다", 5.0)
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 3인칭 — 밖에서 본 우리 ═══════════════════════════════
# ★ 이 쇼에서 **유일한 3인칭**. 두 가지를 여기서 몰아 처리한다.
#    ① 우리 모습(모델 클로즈업) — 1인칭에서는 절대 볼 수 없는 것
#    ② 정지궤도의 원리 — 지구가 돌고 우리가 따라가는 그림은 **밖에서 봐야만** 성립한다
try:
    say("잠깐 밖에서 우리를 보자", 3.0)
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    if sp is not None:
        # 위성과 같은 경도·위도의 바깥쪽 → 위성이 카메라와 지구 사이에 놓인다
        stand(Vec(KOREA_LON, 0.0, R_ZOOM_A), sp)
    _dark()
    feat(sat, "setIntensity", 1.0, Anim(0.0))       # ★ 3인칭이므로 이제 우리가 보인다
    txt = sub_space()
    txt.setText("천리안 1호")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(1.8))
    sleep(2.5)

    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_ZOOM_B), 14.0, sp)    # ★ 진짜 줌인(모델 확대가 아니다)
    feat(sat, "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(26.0))   # 천천히 한 바퀴
    say("이게 우리 모습이다", 4.5)
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.0)
    say("여기서 만든 전기로 16년을 버텼다", 5.0)
    say("가운데 접시는 안테나, 그 옆이 아까 그 카메라다", 5.5)

    # ② 정지궤도의 원리 — **관성 프레임에서만** 지구가 도는 게 보인다
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    stand(Vec(0.0, B_TOP, R_ORBIT), ip)     # ★ 여기서만 지구가 돈다
    txt = sub_space()
    txt.setText("하루")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("이렇게 높은데 왜 안 떨어질까?", 4.0)
    say("떨어지고는 있다 — 다만 옆으로도 빨라서, 휘어진 지구에 영영 못 닿는다", 5.5)
    # ⚠️ 손으로 밀지 않는다. 시간만 흘리면 엔진이 위성을 데려간다(급발진의 원인이 손 구동이었다)
    dm.setDateTime(2010, 7, 3, 3, 30, 0, tz, Anim(28.0))
    say("하루를 28초로 돌려 보자", 5.0)
    say("지구가 한 바퀴 도는 동안", 6.0)
    say("천리안도 딱 한 바퀴 돈다", 6.0)
    say("그래서 늘 한반도 위다", 6.0)
except Exception as e:
    print("막3 오류:", e)

# ══ 막4 : ★1인칭 — 16년, 낮과 밤 ═══════════════════════════════
# ★ 다시 위성의 눈으로. 자리는 그대로인데 **시간만 흐른다** — 그게 16년의 그림이다.
# ⚠️ 이 막은 **낮밤 자체가 주제**라 운영 표준(그림자 OFF)의 예외로 그림자를 켠다.
#    밤면에 도시광까지 켜면 "우리가 지켜본 것"이 한 화면에 다 들어온다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    feat(sat, "setIntensity", 0.0, Anim(0.0))       # ★ 1인칭 복귀 = 우리는 안 보인다
    if sp is not None:
        stand(Vec(KOREA_LON, B_NIGHT, R_NIGHT), sp)
    shadows(True)
    _dark()
    txt = sub_space()
    txt.setText("16년")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("우리는 자리를 뜨지 않았다. 바뀐 건 시간뿐이었다", 4.0)
    dm.setDateTime(2010, 7, 5, 3, 30, 0, tz, Anim(30.0))
    say("낮이 지나가고", 5.5)
    say("밤이 오면 아래에 불이 켜진다", 6.0)
    say("저 불빛 하나하나가 사람이 사는 곳이다", 6.5)
    say("이걸 16년 동안 봤다", 6.0)
    say("설계 수명은 7년이었는데", 4.0)
    say("2010년에 태어난 아기가 고등학생이 될 때까지 일했다", 4.5)
except Exception as e:
    print("막4 오류:", e)

# ══ 막5 : ★1인칭 이탈 → 밖에서 본 자리 ═════════════════════════
# ⚠️ 마감도 1인칭으로 시작한다 — **우리가** 올라가고, 지구가 작아진다.
#    그 다음에야 밖으로 나와 궤도 두 개와 후계 위성을 보여준다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    shadows(False)                                   # 원반 전체를 다시 밝게(운영 표준)
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    if sp is not None:
        stand(Vec(KOREA_LON, 0.0, GEO_R), sp)        # 우리 자리로
    txt = sub_space()
    txt.setText("2025년 12월")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("2025년 12월, 임무가 끝났다", 4.0)
    say("남은 마지막 연료로 우리는 위로 올라간다", 4.0)
    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, GRAVE_R), 14.0, sp)  # ★ 1인칭 이탈 — 지구가 작아진다
    say("일하는 자리를 다음 위성에게 비켜 주는 것이다", 5.5)
    say("지구가 다시 작아진다", 5.0)
    say("여기가 우리가 머물 곳이다", 4.0)

    # ── 여기서 처음이자 마지막으로 밖에서 본다 ──
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    stand(Vec(0.0, B_TOP, R_BACK), ip)
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(0.0))
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    txt = sub_space()
    txt.setText("자리는 비지 않았다")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    # 궤도선 — 멀리서만 쓴다(가까이선 끊겨 보인다). 사용자 요청.
    r_geo = ring(0, 1.0027, Vec(1.0, 0.80, 0.30))
    feat(r_geo, "setOrbitIntensity", 0.95, Anim(4.0))
    r_grave = ring(1, GRAVE_MM, Vec(0.60, 0.60, 0.66), 2.5)
    feat(r_grave, "setOrbitIntensity", 0.85, Anim(3.0))
    say("금색 원이 일하던 자리, 회색 원이 지금 있는 곳이다", 5.5)
    say("(실제로는 아주 조금 위다. 보이라고 크게 그렸다)", 4.0)

    # ⚠️ 불은 꺼지되 **사라지지 않는다**("마지막엔 천리안 보여주지도 않는다"는 지적)
    feat(sat, "setIntensity", 0.35, Anim(6.0))
    say("그리고 전원을 껐다", 4.0)
    say("천리안 1호는 지금도 저기 있다", 4.0)

    # 후계 — 같은 자리에 둘이 더 (⚠️ 실제로도 128.2 부근이지만 겹쳐 보여 벌려 놨다)
    s2a = place_sat(6, LON_2A, SCALE_SAT * 0.8)
    feat(s2a, "setIntensity", 1.0, Anim(2.5))
    say("2018년, 천리안 2A 가 날씨를 이어받았고", 4.0)
    s2b = place_sat(7, LON_2B, SCALE_SAT * 0.8)
    feat(s2b, "setIntensity", 1.0, Anim(2.5))
    say("2020년, 2B 가 바다와 공기를 이어받았다", 4.0)
    feat(r_geo, "setOrbitIntensity", 1.0, Anim(2.0))
    say("7년만 버티면 되던 기계가, 16년을 벌어 준 자리다", 5.0)

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(3.0)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 천리안 1호, 여정과 마감")

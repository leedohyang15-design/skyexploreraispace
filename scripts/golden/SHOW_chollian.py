# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인(v5) — 돔 재생 4회 + 프레임 프로브 1회.
#    프로브(scripts/study/probe_geo_frame.py, 2026-08-12 사용자 확인)로 **확정된 것**:
#      ✅ A 관성 프레임 + **재조준 두 줄** → 지구가 돈다(하늘이 아니라)
#      ✅ B **동기 프레임 경도 128.2** 에 놓은 위성이 한반도 위에 붙어 지구와 함께 돈다
#      ✅ D 동기 프레임에서 위성으로 **진짜 줌인**이 된다(중앙 유지)
#      ❌ C **궤도선(OrbitalPlace)이 끊겨 보인다** — 위성을 꺼도, 굵기를 3.0 으로 올려도 끊긴다
#         → 이 구도에서는 못 쓴다. **v5 는 궤도선을 전부 걷어냈다.**
#    ⚠️ 이 배선으로 통짜 재생한 적은 아직 없다.
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
#  ══ v5 에서 바뀐 것 ══
#
#  ① **위성이 한국 위에 있다** — 동기 프레임 경도 128.2. 안테나도 늘 지구를 향한 채 함께 돈다
#  ② **지구가 돈다** — 관성 프레임 + 재조준. 시간가속을 걸면 지구가 돌고 위성이 따라간다
#     = 그게 곧 '정지궤도'의 설명이다(설명할 게 화면에 있다)
#  ③ **급발진이 없다** — 위성을 손으로 안 민다. 시간만 흐르고 엔진이 알아서 데려간다
#  ④ **진짜 줌인** — `setScale` 확대가 아니라 **카메라가 위성 쪽으로 날아간다**(동기 프레임)
#  ⑤ **궤도선을 걷어냈다** — 끊겨 보여서 못 쓴다(프로브 C). 위성 자체가 궤도를 보여준다
#  ⑥ **위성이 더 크다** — ×1e6(반지름 5,270km). 처음에 고르셨던 값으로 되돌렸다
#  ⑦ **끝까지 화면에 남는다** — 불은 꺼지되 사라지지 않는다
#
#  구성
#    막0  올려다보기                                 (~40초)
#    막1  우주로 — 지구에 다가간다                   (~52초)
#    막2  천리안을 가까이 — 진짜로 다가간다          (~62초)
#    막3  하루 — 지구가 돌고, 천리안은 따라간다      (~50초)
#    막4  무엇을 봤나 — 지구로 내려간다              (~52초)
#    막5  마감, 그리고 자리는 비지 않았다            (~44초)
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

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
GRAVE_R = 49840000.0 / EARTH_R_M        # 7.814 — 무덤궤도(과장. 실제는 300km 위)
KOREA_LON = 128.2                       # 천리안 1호의 정지궤도 경도
LON_2A, LON_2B = 133.0, 123.5           # ⚠️ 실제 2A·2B 도 128.2 부근이지만 겹쳐 보여서 벌렸다

B_TOP = 88.0                  # 북극 위. **각도는 건드리지 않는다**(프레이밍이 깨진 건 늘 각도였다)
R_FAR = 20.0                  # 막1 출발 — 지구가 점
R_ORBIT = 8.0                 # 막1 도착
R_ZOOM_A, R_ZOOM_B = 9.0, 7.6   # 막2 줌인 — 동기 프레임(위성과 같은 경도선 위)
R_DIVE = 3.2                  # 막4 지구 클로즈업
B_NEAR = 25.0
R_BACK = 9.0

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


def sub_ground():
    """지상 자막 — 슬롯 1. **여기서만** setSize 를 부른다."""
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


def enter_space():
    """FadeTo 지구 → 지구 렌더 복구 → 프레임 확보 → 관성 프레임에서 멀찍이. 전 과정 암전."""
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
        print("   ⚠️ 동기 프레임 포트를 못 찾았다 — 위성이 한국 위에 안 붙는다")
    _dark()

    fly(Vec(0.0, B_TOP, R_FAR), 0.0, ip)        # ★ 두 줄짜리 전환(fly 안에 재조준 포함)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
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
    say("우리나라가 처음 가진, 늘 같은 자리에 머무는 위성이다")
    say("지금, 남쪽 하늘 저 높이")
    say("16년 동안 한 번도 자리를 뜨지 않은 것이 있다")
    say("눈에는 안 보인다 — 36,000km 밖이니까")
    say("가서 보자")
except Exception as e:
    print("막0 오류:", e)

# ══ 막1 : 우주로 — 지구에 다가간다 ═════════════════════════════
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.8))
    sleep(1.0)
    _dark()
    enter_space()

    txt = sub_space()                   # ★ 슬롯 5 — 크기를 한 번도 안 건드린 슬롯
    txt.setText("지구")
    _dark()

    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))    # 한국이 낮 = 정면
    _dark()
    sleep(0.4)

    sat = place_sat(5, KOREA_LON)       # ★ 동기 프레임 경도 128.2 = 한반도 위
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
    say("저기 지구가 있다")
    say("우리가 방금 서 있던 곳이 저 안에 있다", 3.5)

    fly(Vec(0.0, B_TOP, R_ORBIT), 20.0, ip)     # ★ 보이는 접근
    say("다가가 보자", 4.5)
    say("점이던 게 커진다", 5.0)
    feat(sat, "setIntensity", 1.0, Anim(3.0))
    say("저기 하나가 떠 있다", 4.5)
    say("천리안 1호다", 4.0)
    say("한반도 바로 위, 36,000km 상공")
    say("무게 2.5톤, 펼친 길이 8.8m — 승용차 두 대쯤")
    say("(화면에서는 보이라고 아주 크게 그렸다)")
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : 천리안을 가까이 — 진짜로 다가간다 ════════════════════
# ⚠️ v4 는 '가까이 보자'면서 모델만 부풀렸다("줌인은 안 하고 뭔 확대를 하고 있냐").
#    이번엔 **카메라가 위성 쪽으로 날아간다** — 동기 프레임의 같은 경도선 위에 서서 R 을 줄인다.
try:
    say("가까이 가 보자", 2.5)
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    _dark()
    if sp is not None:
        # 위성과 같은 경도·위도의 바깥쪽 → 위성이 카메라와 지구 사이에 놓인다
        fly(Vec(KOREA_LON, 0.0, R_ZOOM_A), 0.0, sp)
        _dark()
        cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("천리안 1호")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(1.8))
    sleep(2.5)

    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_ZOOM_B), 14.0, sp)    # ★ 진짜 줌인
    feat(sat, "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(26.0))   # 천천히 한 바퀴
    say("가까이서 보면 이렇게 생겼다", 5.5)
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.5)
    say("여기서 만든 전기로 16년을 버텼다", 5.5)
    say("가운데 접시는 안테나", 4.5)
    say("이 접시는 늘 아래를 향한다 — 우리나라 쪽으로", 5.5)
    say("그 옆이 카메라다. 이걸로 우리를 봤다", 5.0)
    say("뒤로 보이는 게 지구다. 저 아래가 한반도다", 5.5)
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 하루 — 지구가 돌고, 천리안은 따라간다 ════════════════
# ★ 이 막이 '정지궤도'의 설명이다. 말이 아니라 화면이 설명한다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    _dark()
    fly(Vec(0.0, B_TOP, R_ORBIT), 0.0, ip)      # 관성 프레임으로 복귀 — 여기서만 지구가 돈다
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("하루")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("이렇게 높은데, 왜 안 떨어질까?", 4.0)
    say("사실은 떨어지고 있다 — 다만 옆으로도 아주 빠르게 달린다", 5.5)
    say("떨어지는 만큼 지구가 둥글게 휘어서, 영영 못 닿는다", 5.5)
    say("하루를 40초로 돌려 보자", 3.0)

    # ⚠️ 손으로 밀지 않는다. 시간만 흘리면 엔진이 위성을 데려간다(급발진의 원인이 손 구동이었다)
    dm.setDateTime(2026, 8, 13, 3, 30, 0, tz, Anim(40.0))
    say("지구가 돈다", 5.0)
    say("그런데 천리안은 한반도를 안 놓친다", 5.5)
    say("지구가 한 바퀴 도는 동안", 5.0)
    say("천리안도 딱 한 바퀴 돈다", 5.0)
    say("같은 속도로 도니까 늘 같은 자리다", 5.5)
    say("이런 자리를 정지궤도라고 부른다", 5.0)
except Exception as e:
    print("막3 오류:", e)

# ══ 막4 : 무엇을 봤나 — 지구로 내려간다 ════════════════════════
try:
    say("천리안은 거기서 무엇을 보고 있었을까", 3.0)
    feat(sat, "setIntensity", 0.0, Anim(6.0))
    fly(Vec(0.0, B_TOP, R_DIVE), 12.0, ip)      # ★ 보이는 하강
    say("내려가 보자", 4.5)
    say("천리안이 매일 보던 얼굴이다", 4.0)
    sleep(3.0)

    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    _dark()
    fly(Vec(0.0, B_NEAR, R_DIVE), 0.0, ip)      # 각도만 암전에서 바꾼다
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("천리안이 본 것")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)

    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))    # 0→1 이 구름 렌더의 마스터
    feat(earth, "setCloudSpeed", 3.0)
    dm.setDateTime(2026, 8, 16, 3, 30, 0, tz, Anim(35.0))
    say("구름이 몰려온다")
    say("천리안이 한 일은 세 가지였다")
    say("첫째, 날씨를 봤다")
    say("태풍이 어디로 갈지, 비가 언제 올지")
    say("둘째, 통신을 이어 줬다")
    say("그리고 셋째 — 바다를 봤다")
    say("하루 여덟 번, 한반도 둘레 바다를 찍었다")
    say("500m 크기까지 알아볼 만큼 또렷하게")
    say("정지궤도에서 바다를 관측한 건 세계에서 처음이었다")
    say("천리안 1호가 처음 한 일이다")
except Exception as e:
    print("막4 오류:", e)

# ══ 막5 : 마감, 그리고 자리는 비지 않았다 ══════════════════════
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    _dark()
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    fly(Vec(0.0, B_TOP, R_DIVE), 0.0, ip)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("16년")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    fly(Vec(0.0, B_TOP, R_BACK), 10.0, ip)      # ★ 보이는 후퇴
    feat(sat, "setIntensity", 1.0, Anim(6.0))
    say("설계 수명은 7년이었다", 4.0)
    say("7년만 버티면 되는 기계였다", 4.0)
    say("그런데 16년을 일했다", 4.0)
    say("2010년에 태어난 아기가 고등학생이 될 만큼")
    say("2025년 12월, 임무가 끝났다")

    # 무덤궤도 — 위성이 눈에 띄게 위로 올라간다 (궤도선 없이 위성만으로)
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(9.0))
    say("마지막 연료로 조금 더 위로 올라갔다", 4.0)
    say("일하는 자리를 다음 위성에게 비켜 준 것이다", 4.0)
    say("(실제로는 아주 조금 위다. 보이라고 크게 그렸다)", 4.0)

    # ⚠️ 불은 꺼지되 **사라지지 않는다**("마지막엔 천리안 보여주지도 않는다"는 지적)
    feat(sat, "setIntensity", 0.35, Anim(6.0))
    say("그리고 전원을 껐다", 3.5)
    say("천리안 1호는 지금도 저기 있다", 3.5)

    # 후계 — 같은 자리에 둘이 더 (⚠️ 실제로도 128.2 부근이지만 겹쳐 보여 벌려 놨다)
    s2a = place_sat(6, LON_2A, SCALE_SAT * 0.8)
    feat(s2a, "setIntensity", 1.0, Anim(2.5))
    say("2018년, 천리안 2A 가 올라가 날씨를 이어받았고")
    s2b = place_sat(7, LON_2B, SCALE_SAT * 0.8)
    feat(s2b, "setIntensity", 1.0, Anim(2.5))
    say("2020년, 2B 가 바다와 공기를 이어받았다")
    say("셋 다 천리안 1호가 처음 열어 둔 자리에 서 있다")
    say("7년만 버티면 되던 기계가, 16년을 벌어 준 자리다")

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(3.5)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 천리안 1호, 여정과 마감")

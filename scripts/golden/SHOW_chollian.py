# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인(v4) — 돔 재생 3회. 매번 다른 이유로 깨졌고 매번 내 실수였다.
#    v1: ① 우주 자막 4분간 실종 ② 지구에 색 없음 ③ 카메라가 안 움직임 ④ 궤도선 구분 불가
#        ⑤ 너무 멀어 지구가 점 ⑥ 막3 이 텅 빈 우주  — 전부 확인
#    v2: 자막은 떴으나, 관성 프레임으로 **위치만** 옮기고 조준을 안 옮겨
#        지구·궤도선·위성이 통째로 화면 밖으로 나갔다 → v3 에서 프레임 전환 철회
#    v3: ⑦ **본 자막이 또 안 뜸**(범례만 뜸 — 오염된 슬롯 재사용)
#        ⑧ ISS 가 한 스텝에 42°씩 점프 ⑨ 여전히 정적(전환을 전부 암전으로 가림)
#    v4: ⑦⑧⑨ 수정 + ISS·GPS 제거(사용자 지시). **미확인.**
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "천리안 1호 — 여정과 마감"   (약 5분)
#
#  2010년 6월 27일 쿠루에서 올라가, 적도 위 36,000km 동경 128.2도에 자리를 잡고
#  16년을 일한 뒤 2025년 12월에 임무를 마친 위성 이야기.
#  ★ 관람 대상 = 어린이·가족.  ★ 스크립트는 **무음** — 나레이션·음악은 오퍼레이터가 입힌다.
#    대본과 큐시트: docs/27_chollian_narration.md
#
#
#  ⚠️⚠️⚠️ 이 파일에서 가장 중요한 규칙 — 자막 슬롯을 절대 섞지 마라
#
#     자막 규칙은 프레임마다 **반대**다:
#       · 지상 = `setSize(0.052)` + `setDistance(1.0)`
#       · 우주 = **크기를 만지지 말고** `setDistance(20)`  ← 크기를 걸면 화면에서 사라진다
#
#     ⚠️ 크기를 되돌리는 API 가 **없다.** 그래서 규칙의 핵심은
#        '`setSize` 를 안 부르는 것'이 아니라 **'슬롯을 갈아타는 것'** 이다.
#        v3 는 `setSize` 호출만 피하고 **막0 이 크기를 걸어 둔 슬롯 1 을 그대로 재사용**해서
#        또 자막이 안 떴다(범례는 새 슬롯이라 떴고 본 자막만 안 떴다 — 돔 실측).
#
#     → **지상은 슬롯 1, 우주는 슬롯 5. 끝.** 우주 슬롯에는 영원히 setSize 를 부르지 않는다.
#
#
#  ══ v4 에서 바뀐 것 ══
#
#  ① **자막 슬롯 분리** — 위 규칙. 지상 SLOT_GROUND(1) / 우주 SLOT_SPACE(5)
#
#  ② **ISS·GPS 제거**(사용자 지시) — 파랑·초록 궤도와 그 위성을 들어냈다.
#     ⚠️ 한 스텝에 42°씩 점프하던 '너무 빠른 위성'이 바로 ISS 였다(revs 15.5).
#     남은 건 천리안 하나(revs 1.0 = 한 스텝 2.7°)라 매끄럽다.
#     막2 의 '다른 위성과 비교' 대사도 같이 들어내고 천리안 하나로 다시 썼다.
#
#  ③ **카메라가 눈앞에서 난다** — '정적'의 진짜 원인은 장면 전환을 **전부 암전 속에서**
#     한 것이었다. 검증된 '보이는 비행'은 **같은 프레임 안 R 애니메이션**인데 그걸 가려 왔다.
#     이제 세 번의 비행을 관객이 본다:
#       막1  R 20 → 8   (20초)  지구가 점에서 원반으로 = '우주로 나간다'
#       막3  R 8 → 3.2  (12초)  지구가 화면을 채운다 = '내려다본다'
#       막4  R 3.2 → 9  (10초)  물러나며 궤도가 다시 보인다 = '떠난다'
#     ⚠️ 전부 **선형 Anim**(cubic 아님 — 경계 감속이 없어야 매끄럽다), **B 는 안 건드린다**
#        (프레이밍이 깨진 건 세 번 다 각도였다).
#
#  ④ **천리안 클로즈업** — 모델을 만들어 놓고 한 번도 가까이 안 보여줬다.
#     카메라 대신 `setScale` 을 눈앞에서 램프하고 느리게 한 바퀴 돌린다(프레이밍 위험 0).
#
#  ══ 지킨 규약 ══
#    · 암전은 reset 보다 먼저 + 클램프 / 자막 홀드는 글자 수 자동(2초 + 글자당 0.1초)
#    · 가속·비행 구간은 ~5초마다 자막 교체 / 막마다 try/except
#    · 🔴 `OrbitalPlace` 는 궤도선 전용 — `setIntensity`·`setLabelIntensity` 가 없다
#
#  구성
#    막0  올려다보기 — 별이 천천히 돈다              (~40초)
#    막1  우주로 — 지구에 다가간다                   (~55초)
#    막2  천리안을 가까이 — 왜 안 떨어질까           (~60초)
#    막3  무엇을 봤나 — 지구로 내려간다              (~60초)
#    막4  마감 — 물러나며, 불이 꺼진다               (~55초)
#    막5  자리는 비지 않았다                         (~30초)
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "chollian.osg"        # 유저 폴더 상대. make_chollian_model.py 가 만든다

# ── 자막 슬롯 — 절대 섞지 않는다 (파일 상단 규칙 참조) ─────────
SLOT_GROUND = 1               # 지상 전용. setSize 를 거는 유일한 슬롯
SLOT_SPACE = 5                # 우주 전용. **영원히 setSize 를 부르지 않는다**

# ── 구도 ───────────────────────────────────────────────────────
#  B=88(북극 위)은 검증됐다. 각도는 건드리지 않고 R 만 움직인다.
B_TOP = 88.0
R_FAR = 20.0                  # 막1 출발 — 지구가 점(각지름 5.7°)
R_ORBIT = 8.0                 # 막1 도착 — 지구 14.3°, GEO 링 지름 80°
R_DIVE = 3.2                  # 막3 — 지구가 화면을 채운다
R_BACK = 9.0                  # 막4 복귀
B_NEAR = 25.0                 # 막3 만 각도를 바꾼다(암전 중)

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름
GRAVE_MM = 0.78                         # 무덤궤도 과장판
GRAVE_R = 49840000.0 / EARTH_R_M        # 7.814

SCALE_ORBIT = 5.0e5           # 궤도 위 위성 — 반지름 2,636km
SCALE_CLOSE = 4.0e6           # 클로즈업 — 반지름 21,000km (카메라~위성 66,000km 에서 약 18°)

H_SOUTH, TILT_SOUTH = 0.0, 40.0   # 청주에서 128.2°E 정지위성 = 고도 47.5°, 거의 정남

# ── 시계 ───────────────────────────────────────────────────────
#  모든 대기를 STEP 으로 쪼개 그동안 위성을 민다 — 화면이 멈추지 않게.
STEP = 0.3
RATE = 0.0                    # 위성 각속도(도/초). 막마다 갈아 끼운다
CLOCK = 0.0

txt = None
ip = None
sat = None
op_geo = None
ORBITS = []


def _dark(sec=0.0):
    """암전 클램프. reset/FadeTo 는 밝기를 1.0 으로 되돌리므로 한 번 눌러선 안 된다."""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def orbit_pos(u_deg, inc_deg, radius):
    """궤도면 위의 점 → 지구 적도좌표(경도·위도). 궤도선과 정확히 겹치게 하려는 것."""
    u = math.radians(u_deg)
    i = math.radians(inc_deg)
    lat = math.degrees(math.asin(math.sin(i) * math.sin(u)))
    lon = math.degrees(math.atan2(math.cos(i) * math.sin(u), math.cos(u)))
    return Vec(lon, lat, radius)


def tick(sec):
    """대기 — 그동안 위성을 민다."""
    global CLOCK
    n = max(int(round(sec / STEP)), 1)
    for _ in range(n):
        CLOCK += STEP
        if sat is not None and sat["on"] and RATE:
            sat["u"] += RATE * STEP
            try:
                # Anim 을 스텝보다 길게 → 다음 스텝이 겹쳐 들어가 매끄럽다
                sat["ins"].setPositionLBR(
                    orbit_pos(sat["u"], sat["inc"], sat["r"]), Anim(STEP * 1.5))
            except Exception:
                sat["on"] = False
        sleep(STEP)


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 글자 수로 자동 계산(2초 + 글자당 0.1초)."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        tick(hold)


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


def geo_view():
    """FadeTo 지구 → 지구 렌더 복구 → 멀찍이(R_FAR). 전 과정 암전."""
    global ip
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # ⚠️ 막0 이 지상 하늘 쇼를 위해 꺼 둔 것을 되살린다.
    #    안 하면 지구가 회색 공이 되고, 가까이 가면 그릴 표면이 없어 **아예 사라진다**(v1 실측).
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))       # 구름은 막3 의 비트
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    _dark()

    # ⚠️ 카메라는 FadeTo 도킹 프레임(track=-1)에 그대로 둔다.
    #    v2 에서 관성 프레임으로 옮겼다가 조준을 같이 안 옮겨 화면을 통째로 날렸다.
    #    ip 는 궤도선·위성을 **붙이는 용도로만** 쓴다(이 조합은 v1·v3 에서 렌더 확인).
    ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
    cam.setPositionLBR(Vec(0.0, B_TOP, R_FAR), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()


def orbit(slot, mm, ecc, inc, anomaly, color, thick=1.5):
    """지구 둘레 궤도선. 🔴 setIntensity 는 없다 — setOrbitIntensity 만."""
    o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(slot))
    feat(o, "setParent", ip)
    feat(o, "setMeanMotion", mm, Anim(0.0))
    feat(o, "setEccentricity", ecc, Anim(0.0))
    feat(o, "setInclination", inc, Anim(0.0))
    feat(o, "setAscendingNodeLongitude", 0.0, Anim(0.0))
    feat(o, "setArgumentOfPeriapsis", 0.0, Anim(0.0))
    feat(o, "setMeanAnomaly", anomaly, Anim(0.0))
    sleep(0.4)                              # 요소 반영에 한 프레임
    feat(o, "setOrbitColor", color)
    feat(o, "setOrbitThickness", thick)
    feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
    ORBITS.append(o)
    return o


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
    # 별이 천천히 돈다 — 지상 장면에도 움직임을 준다
    dm.setDateTime(2026, 8, 12, 15, 0, 0, tz, Anim(35.0))
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
    geo_view()

    txt = sub_space()                   # ★ 슬롯 5 — 크기를 한 번도 안 건드린 슬롯
    txt.setText("지구")
    _dark()

    # ⚠️ 시작 날짜는 위성을 켜기 전, 암전 중에 못 박는다(instant 날짜점프 = 궤도천체 순간이동)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 0, 0, 0, tz, Anim(0.0))
    _dark()
    sleep(0.4)

    op_geo = orbit(0, 1.0027, 0.0002, 0.1, 0.0, Vec(1.0, 0.78, 0.28))
    _dark()

    ins = load_model(5)
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setScale", SCALE_ORBIT, Anim(0.0))
    feat(ins, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
    feat(ins, "setPositionLBR", orbit_pos(0.0, 0.1, GEO_R), Anim(0.0))
    sat = {"ins": ins, "r": GEO_R, "inc": 0.1, "u": 0.0, "on": True}
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    RATE = 1.2
    tick(3.0)
    say("저기 지구가 있다")
    say("우리가 방금 서 있던 곳이 저 안에 있다")

    # ★ 보이는 접근 — 관객이 다가가는 걸 본다 (선형 Anim, B 는 안 건드림)
    cam.setPositionLBR(Vec(0.0, B_TOP, R_ORBIT), Anim(20.0), -1)
    say("다가가 보자", 4.5)
    say("점이던 게 커진다", 5.0)
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(3.0))
    say("이 노란 원이 천리안이 도는 길이다", 5.5)
    say("지구에서 36,000km — 적도 위, 동경 128.2도", 5.5)
    feat(sat["ins"], "setIntensity", 1.0, Anim(2.5))
    say("그리고 저기, 천리안 1호", 4.0)
    say("무게 2.5톤, 펼친 길이 8.8m — 승용차 두 대쯤")
    say("(화면에서는 보이라고 아주 크게 그렸다)")
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : 천리안을 가까이 — 왜 안 떨어질까 ═════════════════════
try:
    # ★ 클로즈업 — 카메라를 안 건드리고 모델만 키운다(프레이밍 위험 0)
    say("더 가까이 보자", 2.5)
    RATE = 0.0                                       # 키우는 동안엔 제자리에서 돌게
    feat(sat["ins"], "setScale", SCALE_CLOSE, Anim(8.0))
    feat(sat["ins"], "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(24.0))   # 한 바퀴
    say("이렇게 생겼다", 5.0)
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.5)
    say("가운데 접시는 안테나 — 지구를 향해 있다", 5.5)

    feat(sat["ins"], "setScale", SCALE_ORBIT, Anim(6.0))

    RATE = 1.2
    say("이렇게 높은데, 왜 안 떨어질까?")
    say("사실은 떨어지고 있다 — 다만 옆으로도 아주 빠르게 달린다")
    say("떨어지는 만큼 지구가 둥글게 휘어서, 영영 못 닿는다")

    # 하루를 40초로 — 천리안이 딱 한 바퀴 돈다(한 스텝 2.7°, 매끄럽다)
    say("하루를 40초로 돌려 보자", 3.0)
    RATE = 9.0
    dm.setDateTime(2026, 8, 13, 0, 0, 0, tz, Anim(40.0))
    say("천리안이 지구를 한 바퀴 돈다", 5.0)
    say("그 사이 지구도 정확히 한 바퀴 돈다", 5.0)
    say("같은 속도로 도니까", 4.5)
    say("아래에서 보면 늘 같은 자리에 멈춰 있다", 5.0)
    say("그래서 늘 한반도 위에 떠 있었다", 5.0)
    say("이런 자리를 정지궤도라고 부른다", 5.0)
    RATE = 1.2
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 무엇을 봤나 — 지구로 내려간다 ════════════════════════
try:
    say("천리안은 거기서 무엇을 보고 있었을까", 3.0)
    # ★ 보이는 다이브 — 궤도·위성을 뒤에 남기고 지구로 내려간다
    feat(op_geo, "setOrbitIntensity", 0.0, Anim(6.0))
    feat(sat["ins"], "setIntensity", 0.0, Anim(6.0))
    cam.setPositionLBR(Vec(0.0, B_TOP, R_DIVE), Anim(12.0), -1)
    say("내려가 보자", 4.5)
    say("천리안이 매일 보던 얼굴이다", 5.0)
    sat["on"] = False
    tick(3.0)

    # 각도만 암전에서 바꾼다(프레이밍이 깨지는 건 늘 각도였다)
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    _dark()
    for o in ORBITS:
        feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
    cam.setPositionLBR(Vec(0.0, B_NEAR, R_DIVE), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("천리안이 본 것")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    tick(2.5)

    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))    # 0→1 이 구름 렌더의 마스터
    feat(earth, "setCloudSpeed", 3.0)                    # 구름이 흐른다
    dm.setDateTime(2026, 8, 16, 0, 0, 0, tz, Anim(40.0))  # 사흘치 구름 이동
    say("구름이 몰려온다")
    say("천리안이 한 일은 세 가지였다")
    say("첫째, 날씨를 봤다")
    say("태풍이 어디로 갈지, 비가 언제 올지")
    say("둘째, 통신을 이어 줬다")
    say("그리고 셋째 — 바다를 봤다")
    say("하루 여덟 번, 한반도 둘레 바다를 찍었다")
    say("500m 크기까지 알아볼 만큼 또렷하게")
    say("녹조가 번지는지, 갯벌이 어떤지 — 색으로 알아챘다")
    say("정지궤도에서 바다를 관측한 건 세계에서 처음이었다")
    say("천리안 1호가 처음 한 일이다")
except Exception as e:
    print("막3 오류:", e)

# ══ 막4 : 마감 — 물러나며, 불이 꺼진다 ═════════════════════════
try:
    # 각도만 암전에서 되돌리고, **물러나는 건 눈앞에서** 한다
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    _dark()
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    cam.setPositionLBR(Vec(0.0, B_TOP, R_DIVE), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("16년")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    tick(2.0)

    # ★ 보이는 풀백
    cam.setPositionLBR(Vec(0.0, B_TOP, R_BACK), Anim(10.0), -1)
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(6.0))
    sat["on"] = True
    sat["r"] = GEO_R
    feat(sat["ins"], "setIntensity", 1.0, Anim(6.0))
    RATE = 1.6
    say("천리안 1호의 설계 수명은 7년이었다", 5.0)
    say("7년만 버티면 되는 기계였다", 4.5)
    say("그런데 16년을 일했다", 4.5)
    say("2010년에 태어난 아기가 고등학생이 될 만큼")
    say("2025년 12월, 임무가 끝났다")

    # 무덤궤도 — 나선으로 밀어 올린 뒤 불을 끈다
    op_grave = orbit(3, GRAVE_MM, 0.0002, 0.1, 0.0, Vec(0.55, 0.55, 0.6), 1.2)
    feat(op_grave, "setOrbitIntensity", 0.8, Anim(3.0))
    say("마지막 연료로 조금 더 위로 올라갔다", 0)
    n = int(6.5 / STEP)
    for k in range(n):
        sat["r"] = GEO_R + (GRAVE_R - GEO_R) * (k + 1.0) / n
        if k == int(n * 0.55):
            txt.setText("천천히, 아주 천천히")
        tick(STEP)
    say("일하는 자리를 다음 위성에게 비켜 준 것이다")
    say("이 회색 원이 그 자리 — 무덤 궤도라고 부른다")
    say("(실제로는 아주 조금 위다. 보이라고 크게 그렸다)")

    feat(op_geo, "setOrbitIntensity", 0.25, Anim(4.0))
    feat(sat["ins"], "setIntensity", 0.06, Anim(7.0))
    say("그리고 전원을 껐다", 3.5)
    say("천리안 1호는 지금도 저기서 돌고 있다", 4.0)
    say("불이 꺼진 채로, 조용히")
except Exception as e:
    print("막4 오류:", e)

# ══ 막5 : 자리는 비지 않았다 ═══════════════════════════════════
# ⚠️ 색은 따뜻한 계열로 통일한다 — 지워 낸 ISS·GPS(파랑·초록)처럼 보이면 안 된다
try:
    say("하지만 그 자리는 비지 않았다", 3.0)
    op_2a = orbit(4, 1.0027, 0.0002, 0.1, 60.0, Vec(1.0, 0.86, 0.42), 1.4)
    feat(op_2a, "setOrbitIntensity", 0.9, Anim(2.5))
    say("2018년, 천리안 2A 가 올라가 날씨를 이어받았고")

    op_2b = orbit(5, 1.0027, 0.0002, 0.1, 300.0, Vec(1.0, 0.66, 0.30), 1.4)
    feat(op_2b, "setOrbitIntensity", 0.9, Anim(2.5))
    say("2020년, 2B 가 바다와 공기를 이어받았다")
    say("둘 다 천리안 1호가 처음 열어 둔 자리에 서 있다")
    say("7년만 버티면 되던 기계가, 16년을 벌어 준 자리다")

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(4.5)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 천리안 1호, 여정과 마감")

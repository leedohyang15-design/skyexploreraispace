# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 부품(모델 로드·궤도선·북극 위 구도·배율)은 2026-08-12 프로브에서 각각 돔 확인했으나
#        **이 쇼를 통으로 돌린 적은 없다.** 특히 막3 의 프레이밍 전환(R 20↔3)과
#        막4 의 무덤궤도 상승이 화면에 실제로 보이는지가 미확인이다.
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "천리안 1호 — 여정과 마감"   (약 5분)
#
#  2010년 6월 27일 쿠루에서 올라가, 적도 위 36,000km 동경 128.2도에 자리를 잡고
#  16년을 일한 뒤 2025년 12월에 임무를 마친 위성 이야기.
#  골든 쇼 16편이 전부 자연현상이었는데, 이건 **사람이 만든 물건**이 주인공인 첫 쇼다.
#
#  ★ 관람 대상 = 어린이·가족. 짧은 문장, 질문으로 끌고 간다.
#  ★ 스크립트는 **무음**이다(이 빌드는 파이썬으로 소리를 못 낸다 — 확정).
#    나레이션·음악은 오퍼레이터가 입힌다. 대본과 큐시트는 docs/27_chollian_narration.md.
#
#  ⚠️ 2026-08-12 프로브 2회에서 실측한 것만 쓴다
#    ① **모델 단위 = 미터, setScale = 순수 배율.** chollian.osg 반지름 5.27m
#       (⚠️ modelRadius 는 원점 거리가 아니라 **바운딩박스 반대각선의 절반**이다)
#    ② **로딩은 폴링.** 고정 sleep 이면 Loading 인 채 지나가 '로드 실패'로 오판한다
#    ③ ⚠️⚠️ **궤도 물체는 크기보다 구도.** 검증된 궤도 조망(B=35,R=12)에서는
#       정지궤도 위성이 화면 밖으로 밀려 **안 보였다**. 사용자가 카메라를 돌려 찾은
#       **북극 위 B=88 / R=20** 이라야 GEO 링 전체가 한 화면에 들어온다.
#       → 안 보이면 배율부터 올리지 말고 **구도를 먼저 의심할 것**
#    ④ 배율은 ×1e6 (위성 반지름 5,272km = 지구의 0.83배) — 사용자가 고른 값
#    ⑤ 모델은 아직 **흰-은색**이다(조명이 켜져 있어 정점색이 무시된다).
#       실제 위성도 흰 단열재·은색이라 거짓은 아니다. 금색 태양전지판은 색 프로브 뒤에.
#
#  ⚠️ 지킨 규약 (골든 쇼 공통)
#    · 암전은 reset **보다 먼저**. reset/FadeTo 가 밝기를 1.0 으로 되돌리니 클램프로 눌러둔다
#    · 자막 홀드는 say() 가 글자 수로 자동 계산(2초 + 글자당 0.1초). 숫자를 박지 않는다
#    · 시간가속 구간은 ~9초마다 자막을 갈아준다(화면만 변하고 자막이 멈추면 비어 보인다)
#    · 막마다 try/except — 한 줄이 죽어도 다음 막이 나와야 한다
#    · 자막 거리: 지상 1.0 / 행성 프레임 20 (프레임 바뀔 때 갈아탄다)
#    · 🔴 OrbitalPlace 에는 setIntensity/setLabelIntensity 가 **없다**(AttributeError).
#      궤도선은 setOrbitIntensity, 이름표는 전부 InsertText 자막으로
#
#  구성
#    막0  올려다보기 — 남쪽 하늘 저 위               (~40초)
#    막1  지구 밖으로 — 그 자리                      (~45초)
#    막2  왜 안 움직일까 — 하루를 40초로             (~75초)
#    막3  무엇을 봤나 — 하루 여덟 번의 바다          (~60초)
#    막4  마감 — 불이 꺼진다                         (~55초)
#    막5  자리는 비지 않았다                         (~25초)
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "chollian.osg"        # 유저 폴더(D:/SkyExplorer-Data/user) 상대. make_chollian_model.py 가 만든다

# ── 궤도 조망 구도 — 사용자가 실측으로 찾은 값(B=90/R=131,247km) ──────────
B_TOP, R_TOP = 88.0, 20.0
# ── 지구 클로즈업(막3) — 표면·구름이 읽히려면 이만큼 당겨야 한다 ──────────
B_NEAR, R_NEAR = 25.0, 3.2

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
# 무덤궤도 — 실제는 정지궤도 300km 위지만 화면에서 0.7% 차이라 안 보인다.
# meanMotion 0.78 → 반지름 49,840km = 7.81 지구반지름. **과장이라는 걸 나레이션에서 밝힌다.**
GRAVE_MM = 0.78
GRAVE_R = 49840000.0 / EARTH_R_M

SCALE_ORBIT = 1.0e6                     # 위성 반지름 5,272km — 사용자 선택
SCALE_CLOSE = 6.0e6                     # 클로즈업은 카메라 대신 setScale 램프(구도를 안 건드린다)

# 청주에서 128.2°E 정지위성: cos γ = cos(36.64°)·cos(0.71°) = 0.8023 → 고도 47.5°, 거의 정남
H_SOUTH, TILT_SOUTH = 0.0, 40.0

txt = None
sat = None
op_geo = None


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


def sub(distance):
    """자막 슬롯. ⚠️ 거리는 프레임마다 다르다 — 지상 1.0 / 행성 20."""
    t = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setSize(0.052)
    t.setColor(Vec(1.0, 1.0, 0.55))
    t.setDistance(distance, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


def load_model(slot):
    """⚠️ 고정 sleep 으로 기다리면 Loading 인 채 지나간다(프로브 실측) — Loaded 뜰 때까지 폴링."""
    ins = Insert3D(Insert3D.Insert3DName(slot))
    path = MODEL
    try:
        import os
        u = Configuration.configuration().localUserFolder
        if u:
            path = os.path.join(u, MODEL)          # 절대경로가 더 확실하다
    except Exception:
        pass
    ins.setModelFilename(path)
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        try:
            if "Loaded" in str(ins.loadingStatus):
                print("   모델 로드 OK — radius %s m" % ins.modelRadius)
                return ins
        except Exception:
            pass
    print("   ⚠️ 모델 로드 실패 — %s (유저 폴더에 있는지 확인)" % path)
    return ins


def geo_view():
    """FadeTo 지구 → 북극 위 GEO 조망. 전 과정 암전."""
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):                    # FadeTo 가 도는 내내 눌러둔다
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)
    # 궤도 쇼는 그림자 OFF — 지구 반쪽이 어두우면 그쪽 궤도·위성이 안 보인다
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    _dark()
    cam.setPositionLBR(Vec(0.0, B_TOP, R_TOP), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()


def orbit(slot, mm, ecc, inc, anomaly, color, thick=1.5):
    """지구 둘레 궤도선 하나. 🔴 setIntensity 는 없다 — setOrbitIntensity 만."""
    o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(slot))
    feat(o, "setParent", earth.portId(Planet.PlanetPort.EquatorialJ2000))
    feat(o, "setMeanMotion", mm, Anim(0.0))
    feat(o, "setEccentricity", ecc, Anim(0.0))
    feat(o, "setInclination", inc, Anim(0.0))
    feat(o, "setAscendingNodeLongitude", 0.0, Anim(0.0))
    feat(o, "setArgumentOfPeriapsis", 0.0, Anim(0.0))
    feat(o, "setMeanAnomaly", anomaly, Anim(0.0))
    sleep(0.4)                              # 요소 반영에 한 프레임(Comet·Asteroid 와 같은 함정)
    feat(o, "setOrbitColor", color)
    feat(o, "setOrbitThickness", thick)
    return o


# ══ 막0 : 올려다보기 ═══════════════════════════════════════════
# ⚠️ 암전을 reset 보다 먼저 — 안 그러면 직전 쇼의 마지막 화면이 그대로 번쩍인다(돔 실측)
_dark()
try:
    SceneGraph().reset(1)
    _dark(1.5)

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
    earth.setIntensity(1.0, Anim(0.0))          # 지상 씬의 마스터 스위치
    earth.setAtmosphereIntensity(0.0, Anim(0.0))    # 하늘 쇼 = 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))       #           + 지면 OFF
    earth.setElevationScale(0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    _dark()

    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 13, 0, 0, tz, Anim(0.0))    # 청주 22:00 KST = 13:00 UTC
    _dark()
    sleep(0.4)

    cam.setOrientationH(H_SOUTH, Anim(0.0))         # 정남
    _dark()
    cam.setTargetHeight(TILT_SOUTH, Anim(0.0))      # 고도 47도를 프레임에 담는 틸트
    _dark()

    txt = sub(1.0)
    txt.setText("천리안 1호")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
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

# ══ 막1 : 지구 밖으로 ══════════════════════════════════════════
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.8))
    sleep(1.0)
    _dark()
    geo_view()

    txt = sub(20.0)                     # ⚠️ 행성 프레임 자막은 distance 20
    txt.setText("지구 — 북극 위에서")
    _dark()

    # ⚠️ 시작 날짜는 **위성을 켜기 전, 암전 중에** 못 박는다.
    #    궤도 천체가 보이는 상태에서 instant 로 날짜를 걸면 궤도상 위치가 뚝 순간이동한다(실측).
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 0, 0, 0, tz, Anim(0.0))
    _dark()
    sleep(0.4)

    op_geo = orbit(0, 1.0027, 0.0002, 0.1, 0.0, Vec(1.0, 0.78, 0.28))
    _dark()

    sat = load_model(5)
    feat(sat, "setIntensity", 0.0, Anim(0.0))
    feat(sat, "setShadowStrength", 0.0, Anim(0.0))
    feat(sat, "setParent", earth.portId(Planet.PlanetPort.EquatorialJ2000))
    feat(sat, "setPositionLBR", Vec(0.0, 0.0, GEO_R), Anim(0.0))
    feat(sat, "setScale", SCALE_ORBIT, Anim(0.0))
    feat(sat, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
    say("여기가 지구다")
    say("우리가 방금 서 있던 곳이 저 아래 어딘가")
    feat(op_geo, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(2.5))
    say("이 노란 원이 천리안이 도는 길이다")
    say("지구에서 36,000km — 적도 위, 동경 128.2도")
    say("지구를 한 바퀴 도는 데 딱 하루가 걸리는 높이다")
    feat(sat, "setIntensity", 1.0, Anim(2.5))
    say("저기 있다")
    say("천리안 1호")
    say("무게는 2.5톤, 펼친 길이는 8.8m — 승용차 두 대쯤")
    say("(화면에서는 보이라고 아주 크게 그렸다)")
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : 왜 안 움직일까 ═══════════════════════════════════════
try:
    say("이렇게 높은데, 왜 안 떨어질까?")
    say("사실은 떨어지고 있다 — 다만 옆으로도 아주 빠르게 달린다")
    say("떨어지는 만큼 지구가 둥글게 휘어서, 영영 못 닿는다")
    say("다른 위성들과 견줘 보자")

    op_iss = orbit(1, 15.50, 0.0003, 51.6, 40.0, Vec(0.45, 0.85, 1.0), 1.2)
    feat(op_iss, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(op_iss, "setOrbitIntensity", 0.85, Anim(2.0))
    say("파란 원 — 국제우주정거장. 지구에 딱 붙어 있다")

    op_gps = orbit(2, 2.005, 0.01, 55.0, 200.0, Vec(0.6, 1.0, 0.6), 1.2)
    feat(op_gps, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(op_gps, "setOrbitIntensity", 0.85, Anim(2.0))
    say("초록 원 — GPS 위성")
    say("이제 하루를 40초로 돌려 보자")

    # ⚠️ 가속 구간(40초)을 몇 개의 긴 홀드로 때우면 화면이 멈춘 것처럼 보인다.
    #    **짧은 자막을 자주 갈아주는 쪽**이 낫다 — 홀드는 전부 8초 미만으로 둔다.
    dm.setDateTime(2026, 8, 13, 0, 0, 0, tz, Anim(40.0))
    sleep(2.0)
    say("우주정거장은 쌩쌩 돈다", 5.0)
    say("90분에 한 바퀴", 4.5)
    say("GPS 는 반나절에 한 바퀴", 5.0)
    say("그럼 천리안은?", 4.5)
    say("거의 제자리다", 5.0)
    say("지구가 한 바퀴 도는 동안", 5.0)
    say("천리안도 딱 한 바퀴", 5.0)
    say("같은 속도로 도니까, 멈춰 있는 것처럼 보인다", 5.0)
    say("그래서 늘 한반도 위에 떠 있다")
    say("이런 자리를 정지궤도라고 부른다")
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 무엇을 봤나 ══════════════════════════════════════════
# ⚠️ 지구를 크게 봐야 구름·바다가 읽힌다 → R 20 → 3.2. 프레이밍이 바뀌므로 **암전 전환**.
try:
    say("그럼 천리안은 거기서 무엇을 보고 있었을까", 3.0)
    _dark()
    txt.setIntensity(0.0, Anim(0.6))
    sleep(0.8)
    _dark()

    for o in (op_geo,):
        feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(sat, "setIntensity", 0.0, Anim(0.0))
    _dark()

    cam.setPositionLBR(Vec(0.0, B_NEAR, R_NEAR), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()

    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))
    _dark()

    txt = sub(20.0)
    txt.setText("천리안이 본 것")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)

    say("이게 천리안이 보던 지구다")
    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))     # 0→1 페이드인이 구름 렌더의 마스터
    say("구름이 몰려온다")
    say("천리안이 한 일은 세 가지였다")
    say("첫째, 날씨를 봤다")
    say("태풍이 어디로 갈지, 비가 언제 올지")
    say("밤에도 낮에도 쉬지 않고 이 얼굴을 찍어 보냈다")
    say("둘째, 통신을 중계했다")
    say("그리고 셋째 — 바다를 봤다")
    say("하루 여덟 번, 한반도 둘레 바다를 찍었다")
    say("500m 크기까지 알아볼 만큼 또렷하게")
    say("바다 색이 바뀌면 알아챘다 — 녹조가 번지는지, 갯벌이 어떤지")
    say("정지궤도에서 바다를 관측한 건 세계에서 처음이었다")
    say("천리안 1호가 처음 한 일이다")
except Exception as e:
    print("막3 오류:", e)

# ══ 막4 : 마감 — 불이 꺼진다 ═══════════════════════════════════
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.6))
    sleep(0.8)
    _dark()

    feat(earth, "setCloudsIntensity", 0.35, Anim(0.0))
    cam.setPositionLBR(Vec(0.0, B_TOP, R_TOP), Anim(0.0), -1)      # 궤도 조망으로 복귀
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(0.0))
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    feat(sat, "setPositionLBR", Vec(0.0, 0.0, GEO_R), Anim(0.0))
    _dark()

    txt = sub(20.0)
    txt.setText("16년")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)

    say("천리안 1호의 설계 수명은 7년이었다")
    say("7년만 버티면 되는 기계였다")
    say("그런데 16년을 일했다")
    say("2010년에 태어난 아기가 고등학생이 될 만큼")
    say("2025년 12월, 임무가 끝났다")

    # 무덤궤도 — 눈에 띄게 올린 뒤 불을 끈다 (사용자 선택: 둘 다)
    op_grave = orbit(3, GRAVE_MM, 0.0002, 0.1, 0.0, Vec(0.55, 0.55, 0.6), 1.2)
    feat(op_grave, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(op_grave, "setOrbitIntensity", 0.8, Anim(3.0))
    feat(sat, "setPositionLBR", Vec(0.0, 0.0, GRAVE_R), Anim.cubic(9.0))
    say("마지막 연료로 조금 더 위로 올라갔다", 4.5)
    say("일하는 자리를 다음 위성에게 비켜 준 것이다", 4.5)
    say("이 회색 원이 그 자리 — 무덤 궤도라고 부른다")
    say("(실제로는 아주 조금 위다. 보이라고 크게 그렸다)")

    feat(op_geo, "setOrbitIntensity", 0.25, Anim(4.0))
    feat(sat, "setIntensity", 0.06, Anim(7.0))
    say("그리고 전원을 껐다", 4.0)
    say("천리안 1호는 지금도 저기서 돌고 있다", 4.5)
    say("불이 꺼진 채로, 조용히")
except Exception as e:
    print("막4 오류:", e)

# ══ 막5 : 자리는 비지 않았다 ═══════════════════════════════════
try:
    say("하지만 그 자리는 비지 않았다", 3.0)
    op_2a = orbit(4, 1.0027, 0.0002, 0.1, 60.0, Vec(1.0, 0.85, 0.4), 1.4)
    feat(op_2a, "setOrbitIntensity", 0.0, Anim(0.0))
    feat(op_2a, "setOrbitIntensity", 0.9, Anim(2.5))
    say("2018년, 천리안 2A 가 올라가 날씨를 이어받았고")

    op_2b = orbit(5, 1.0027, 0.0002, 0.1, 300.0, Vec(0.5, 0.9, 1.0), 1.4)
    feat(op_2b, "setOrbitIntensity", 0.0, Anim(0.0))
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

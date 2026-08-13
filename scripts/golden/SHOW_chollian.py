# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인(v5) — 돔 재생 4회 + 프레임 프로브 1회.
#    프로브(scripts/study/probe_geo_frame.py, 2026-08-12 사용자 확인)로 **확정된 것**:
#      ✅ A 관성 프레임 + **재조준 두 줄** → 지구가 돈다(하늘이 아니라)
#      ✅ B **동기 프레임 경도 128.2** 에 놓은 위성이 한반도 위에 붙어 지구와 함께 돈다
#      ✅ D 동기 프레임에서 위성으로 **진짜 줌인**이 된다(중앙 유지)
#      🛑 C **`OrbitalPlace` 궤도선은 못 쓴다 — 2026-08-13 판별 완료.**
#         판별 프로브의 A 단계가 **검증된 예제 코드 그대로**였는데 그것도 나선이었다
#         → 클래스 자체가 이 빌드에서 닫힌 원을 못 그린다(내 쇼의 버그가 아니다).
#      ✅✅ **대체 확정 (2026-08-13 사용자 스샷 4장)**: 궤도선 = **직접 구운 고리 모델**
#         (make_orbit_ring.py). **`RING_HPR = Vec(0,0,0)` 이 적도면에 눕는다**
#         (0,90,0 은 옆으로 섬 / 90,0,0 도 누움 — 같은 평면). **닫힌 원**으로 렌더되고,
#         **천리안이 그 고리 위에 정확히 얹힌다**(축척도 검증). 옆에서 보면 '선'이 된다.
#    ⚠️ **v9 에서 아직 돔에서 못 본 것**: 이륙 고도 R=1.6 · 랑데부 구도(막1) ·
#       막3 그림자 ON + 오블리크(B40) 낮밤 · 막5 이탈(금색→회색 건너가기).
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
#  ⚠️⚠️⚠️ 규칙 3 — 위성의 눈(1인칭)과 밖에서 보기(3인칭)를 **의도적으로** 나눈다
#     v6 까지는 여섯 막 중 다섯 막이 "밖에서 천리안을 구경하는" 구도였다("너무 관조하는 느낌").
#     · **1인칭 막에서는 위성 모델을 끈다**(우리가 그것이므로 화면에 보이면 안 된다).
#       카메라의 집이 **동기 프레임(sp)** — 정지궤도 위성의 눈은 지구와 함께 돌기 때문에
#       **지구가 안 도는 게 정상이다.** 도는 것처럼 보이면 그건 관성 프레임(=3인칭)이다.
#     · **3인칭이 꼭 필요한 것 두 가지**: ① 천리안의 모습(모델) ② 정지궤도의 원리
#       (지구가 돌고 위성이 따라가는 그림은 **밖에서 봐야만** 성립한다) ③ 궤도 이탈.
#
#  ══ v8 에서 바뀐 것 (2026-08-13 지시 5건) ══
#
#  ① **순서를 바꿨다** — 한반도를 보기 **전에** 천리안 모습부터 보여준다(막2 → 막4 순서 교체)
#  ② **쿠루·동쪽 표류를 뺐다** — 그냥 지구에서 이륙해 천리안 자리까지 올라가고,
#     올라가는 동안 **천리안이 화면에 들어온다**(랑데부). 카메라 경도를 12° 벌려 모델을 안 뚫는다
#  ③ **낮밤을 막3(같이 도는 장면)으로 옮겼다** — 끝에 있던 '16년 낮과 밤' 막은 없앴다.
#     정지궤도를 설명하는 그 자리에서 **지구가 돌며 낮밤이 두 번 지나간다** = 설명과 그림이 한 화면에
#  ④ **마감이 '정지궤도 → 폐기궤도 이탈'이다** — 금색·회색 원을 먼저 둘 다 켜고,
#     위성이 금색에서 회색으로 **14초에 걸쳐 건너간다**. 그게 막5 의 전부다
#  ⑤ **궤도선의 기계를 바꿨다(v9)** — `OrbitalPlace` 를 버리고 **직접 구운 고리 모델**로.
#     계산으로 그린 원이라 전파기가 없다 = 나선이 될 수가 없다. **돔에서 확인 완료**
#
#  구성
#    막0  올려다보기 (관객의 눈)                     (~38초)
#    막1  이륙 — 천리안을 만나러 올라간다            (~57초)
#    막2  천리안 모습 — 가까이서 한 바퀴             (~47초)
#    막3  같이 돈다 — 낮과 밤이 지나간다             (~62초)
#    막4  ★1인칭 — 천리안의 눈으로 한반도를 본다     (~53초)
#    막5  마감 — 정지궤도에서 폐기궤도로 떠난다      (~60초)
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

# ★ 궤도선 스위치. 보기 싫으면 이 한 줄만 False (길이·타이밍은 안 바뀐다).
SHOW_RINGS = True

# ⚠️⚠️⚠️ [2026-08-13 확정] **`OrbitalPlace` 는 이 빌드에서 닫힌 원을 못 그린다 — 버렸다.**
#   판별 프로브(probe_orbit_spiral.py)의 A 단계가 **검증된 예제(orbital_satellites.py) 코드 그대로**
#   였는데 **그것도 나선**이었다. 즉 내 쇼의 버그가 아니라 클래스 자체가 안 되는 것이다
#   (SkySurvey·VideoPlayer 와 같은 '호스트/엔진 소관' 부류).
#   ⚠️ 예전에 "궤도 렌더됨"으로 적어 둔 기록은 궤도 5개가 겹쳐 있어 나선인 걸 못 알아본 것이다.
#   → **궤도선을 직접 구운 3D 모델로 바꿨다**(scripts/study/make_orbit_ring.py).
#     계산으로 그린 원이라 **전파기가 없다 = 나선이 될 수가 없다.** ✅ 돔에서 확인됨.
#   ⚠️ 쇼를 돌리기 전에 **make_orbit_ring.py 를 한 번 돌려** 유저 폴더에 고리 파일을 만들어 둘 것.
RING_GOLD, RING_GRAY = "ring_gold.osg", "ring_gray.osg"
RING_HPR = Vec(0.0, 0.0, 0.0)   # ✅ **확정** (2026-08-13 probe_ring_model.py, 사용자 스샷)
#   (0,0,0) = 적도면에 눕는다 ✅ / (0,90,0) = 옆으로 선다 ✗ / (90,0,0) = 누움(같은 평면) ✅
#   같은 프로브에서 **천리안이 고리 위에 정확히 얹히는 것**까지 확인 = 축척도 맞다.
RING_SLOT_GOLD, RING_SLOT_GRAY = 41, 42

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
# 무덤궤도 — ⚠️ 실제는 정지궤도 300km 위(0.7% 차이 = 화면에서 안 보인다).
# "이탈할 때 너무 안 보인다"는 지적을 받아 **크게 과장**했다. 나레이션에서 고지한다.
GRAVE_R = 10.5                          # 지구반지름 단위(≈67,000km) — GEO 6.611 대비 59% 바깥
KOREA_LON = 128.2                       # 천리안 1호의 정지궤도 경도
LON_2A, LON_2B = 133.0, 123.5           # ⚠️ 실제 2A·2B 도 128.2 부근이지만 겹쳐 보여서 벌렸다

B_TOP = 88.0                  # 북극 위. **각도는 건드리지 않는다**(프레이밍이 깨진 건 늘 각도였다)
R_ZOOM_A, R_ZOOM_B = 10.0, 8.3  # 막2 모델 클로즈업 — 동기 프레임(위성과 같은 경도선 위)
#  ⚠️ 7.6 은 위성까지 6,300km 라 태양전지판 하나가 돔을 다 덮었다(돔 실측).
#     8.3 이면 10,800km — 위성이 화면 절반, 뒤로 지구도 들어온다.

# ★ 막1 이륙·랑데부 — 지구에서 곧장 천리안 자리까지 올라가며 **천리안을 보면서** 간다.
#   ⚠️ 카메라 경도를 위성보다 **12° 서쪽**에 둔다. 같은 경도선으로 올라가면 R=6.611 에서
#      모델을 뚫고 지나간다. 12° 벌리면 도착점(R=10)에서 위성이 지구 옆 **21.5°** 에 놓인다(계산).
LON_CLIMB = 116.0
R_LAUNCH = 1.6                # 이륙 고도(≈3,800km). 지구 각지름 84° = 발밑을 채운다
#   ⚠️ 첫 번째 조정 손잡이. 너무 가까워 지표가 뭉개지면 1.9~2.2 로 올릴 것.
R_MEET = 10.0                 # 랑데부 지점 — 위성(6.611) 바깥. 위성이 지구 앞에 놓인다
#   ⚠️ 올라가는 동안 위성은 처음엔 **뒤쪽**에 있다(저궤도에서 정지궤도는 지구 반대편).
#      R≈8 을 지나며 화면에 들어온다 — 물리적으로 맞는 그림이라 그대로 쓴다.

B_TOGETHER, R_TOGETHER = 40.0, 9.0   # 막3 '같이 돈다' — 오블리크라야 낮밤 경계가 보인다
R_DIVE = 2.2                  # 막4 — 카메라로 당긴 지구(각지름 54°)
# ⚠️⚠️ [2026-08-12 지적 "닌 이게 한국이냐"] 위성은 **적도(위도 0)** 에 있어서
#   그 자리에서 지구를 보면 원반 한가운데가 128.2°E 적도 = **인도네시아 앞바다**다.
#   한국은 위쪽 가장자리로 밀린다. 물리적으론 맞지만 보여주려는 게 한국이니 틀린 그림이다.
#   → 당기면서 **위도를 32°까지 같이 올려** 한반도를 화면 한가운데로 가져온다.
B_DIVE = 32.0
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


def load_model(slot, model=None):
    """⚠️ 고정 sleep 으로 기다리면 Loading 인 채 지나간다(실측) — Loaded 뜰 때까지 폴링."""
    ins = Insert3D(Insert3D.Insert3DName(slot))
    model = model or MODEL
    path = model
    try:
        import os
        u = Configuration.configuration().localUserFolder
        if u:
            path = os.path.join(u, model)
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


def ring(slot, model, radius_m):
    """궤도선 하나 — **직접 구운 고리 모델**을 지구 중심에 놓고 반지름만큼 키운다.

    ⚠️ `OrbitalPlace` 를 안 쓴다(위 주석 참조 — 이 빌드에서 닫힌 원을 못 그린다).
       고리는 반지름 1.0(미터) 짜리로 구워져 있으므로 `setScale(반지름[m])` 이 곧 궤도 반지름이다.
       정지궤도 42,164 km → setScale(4.2164e7).
    ⚠️ 부모는 **관성 프레임(ip)** — 궤도는 별에 대해 고정된 것이지 지면에 붙은 게 아니다."""
    if not SHOW_RINGS:
        return _NoText()
    ins = load_model(slot, model)
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))   # 그림자로 반쪽이 어두워지지 않게
    feat(ins, "setScale", radius_m, Anim(0.0))
    feat(ins, "setOrientationHPR", RING_HPR, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setPositionLBR", Vec(0.0, 0.0, 0.0), Anim(0.0))   # 지구 중심
    return ins


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
    # ★ 우주로 넘어가는 문. 막1~3 은 만나러 가서 보고, 막4 부터 관객이 천리안이 된다.
    say("직접 만나러 가 보자")
    say("이륙한다")
except Exception as e:
    print("막0 오류:", e)

# ══ 막1 : 이륙 — 천리안을 만나러 올라간다 ══════════════════════
# ⚠️ [2026-08-13 지시] 쿠루 발사장·동쪽 표류를 뺐다. **그냥 지구에서 이륙해 천리안 자리까지**
#    올라가고, 올라가는 동안 **천리안을 보면서** 간다. 랑데부다.
#    카메라 경도는 위성보다 12° 서쪽 — 같은 경도선이면 도중에 모델을 뚫고 지나간다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.8))
    sleep(1.0)
    _dark()
    enter_space()

    dm.stop()                       # ★ 궤도선을 만들기 전에 시계를 반드시 멈춘다
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))    # 한국이 낮
    _dark()
    sleep(0.4)

    sat = place_sat(5, KOREA_LON)   # 천리안은 제 자리(정지궤도)에 미리 놓는다
    feat(sat, "setIntensity", 0.0, Anim(0.0))

    # ★★ 궤도선을 **여기서 미리 만든다** — 시계가 완전히 멈춰 있고 아무 애니메이션도 없는 지금이
    #    유일하게 안전한 시점이다(막5 에서 만들면 앞 막의 시계 애니가 아직 돌고 있다).
    #    슬롯은 1·2 — 0번은 쓰지 않는다(프리셋 슬롯 의심). 켜는 건 막5 에서.
    r_geo = ring(RING_SLOT_GOLD, RING_GOLD, GEO_R * EARTH_R_M)
    r_grave = ring(RING_SLOT_GRAY, RING_GRAY, GRAVE_R * EARTH_R_M)
    _dark()

    if sp is not None:
        stand(Vec(LON_CLIMB, 0.0, R_LAUNCH), sp)    # ★ 이륙 지점 — 지구가 발밑을 채운다
    txt = sub_space()               # ★ 슬롯 5 — 크기를 한 번도 안 건드린 슬롯
    txt.setText("이륙")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
    say("우리는 지금 로켓 위에 있다", 4.0)
    say("발밑이 지구다", 3.5)

    if sp is not None:
        fly(Vec(LON_CLIMB, 0.0, R_MEET), 24.0, sp)  # ★ 이륙 → 정지궤도까지, 눈앞에서
    feat(sat, "setIntensity", 1.0, Anim(8.0))       # 올라가는 동안 서서히 드러난다
    say("올라간다", 4.0)
    say("지구가 점점 작아진다", 4.5)
    say("3,000km … 10,000km … 20,000km", 5.5)
    say("저 앞에 뭔가 보이기 시작한다", 5.5)
    say("36,000km — 다 왔다", 4.5)
    say("천리안 1호다", 4.0)
    say("한반도 바로 위, 이 자리에 16년을 있었다", 5.0)
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : 천리안 모습 — 가까이서 한 바퀴 ═══════════════════════
# ⚠️ [2026-08-13 지시] "한반도를 계속 보기 전에 천리안 모습부터 보여줘라" — 순서를 앞으로 당겼다.
#    카메라가 **위성 쪽으로 날아간다**(모델을 부풀리는 게 아니다).
try:
    say("가까이 가 보자", 2.5)
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    if sp is not None:
        # 위성과 같은 경도선 바깥쪽 → 위성이 카메라와 지구 사이에 놓인다
        stand(Vec(KOREA_LON, 0.0, R_ZOOM_A), sp)
    txt = sub_space()
    txt.setText("천리안 1호")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(1.8))
    sleep(2.5)

    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_ZOOM_B), 14.0, sp)    # ★ 진짜 줌인
    feat(sat, "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(26.0))   # 천천히 한 바퀴
    say("이렇게 생겼다", 4.5)
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.0)
    say("여기서 만든 전기로 16년을 버텼다", 5.0)
    say("가운데 접시는 안테나, 그 옆이 지구를 보는 카메라다", 5.5)
    say("무게 2.5톤, 펼친 길이 8.8m — 승용차 두 대쯤이다", 5.5)
    say("(화면에서는 보이라고 아주 크게 그렸다)", 4.5)
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 같이 돈다 — 낮과 밤이 지나간다 ═══════════════════════
# ⚠️ [2026-08-13 지시] "마지막 낮밤은 버리고 처음 같이 돌 때 낮밤 반복으로."
#    → 정지궤도를 설명하는 이 막에 낮밤을 얹었다. 여기서 두 가지가 한 화면에 있다:
#      **지구가 돌고(=낮밤이 지나가고) 천리안이 그걸 따라간다.**
# ⚠️ 프레임은 **관성(ip)** 이어야 한다 — 동기 프레임에서는 지구가 안 돌아 설명이 성립하지 않는다.
# ⚠️ 그림자를 켠다(이 막은 낮밤 자체가 주제라 운영 표준의 예외) + 오블리크(B40)라야 경계가 보인다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    stand(Vec(0.0, B_TOGETHER, R_TOGETHER), ip)
    shadows(True)
    _dark()
    txt = sub_space()
    txt.setText("하루")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("이렇게 높은데 왜 안 떨어질까?", 4.0)
    say("떨어지고는 있다 — 다만 옆으로도 빨라서, 휘어진 지구에 영영 못 닿는다", 5.5)
    say("시간을 빠르게 돌려 보자", 3.5)
    # ⚠️ 손으로 밀지 않는다. 시간만 흘리면 엔진이 위성을 데려간다(급발진의 원인이 손 구동이었다)
    dm.setDateTime(2026, 8, 14, 3, 30, 0, tz, Anim(42.0))    # 이틀 = 낮밤 두 번
    say("지구가 돈다 — 낮이 가고 밤이 온다", 6.0)
    say("밤이 되면 아래에 불이 켜진다", 6.0)
    say("저 불빛 하나하나가 사람이 사는 곳이다", 6.5)
    say("그런데 천리안은 한반도를 안 놓친다", 6.5)
    say("지구가 한 바퀴 도는 동안 천리안도 딱 한 바퀴", 6.5)
    say("같은 속도로 도니까 늘 같은 자리다 — 이걸 정지궤도라고 한다", 6.0)
except Exception as e:
    print("막3 오류:", e)

# ══ 막4 : ★1인칭 — 천리안의 눈으로 한반도를 본다 ═══════════════
# ★ 여기서부터 관객이 천리안이 된다. 동기 프레임 = 위성의 눈이라 **지구가 안 도는 게 정상**이다.
#   ⚠️ 위성은 적도(위도 0)에 있어서 그 자리에서 지구를 보면 원반 한가운데가 인도네시아 앞바다다.
#      → 당기면서 위도를 32°까지 같이 올려 한반도를 화면 한가운데로 가져온다.
try:
    say("이번엔 천리안의 눈으로 보자", 3.0)
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    shadows(False)                                  # 원반 전체를 밝게 — 한반도가 잘 보이게
    feat(sat, "setIntensity", 0.0, Anim(0.0))       # ★ 1인칭 = 우리가 그것이므로 안 보인다
    if sp is not None:
        stand(Vec(KOREA_LON, 0.0, GEO_R), sp)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))
    _dark()
    txt = sub_space()
    txt.setText("천리안이 본 것")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    say("여기가 16년 동안 우리 자리다", 4.0)
    if sp is not None:
        fly(Vec(KOREA_LON, B_DIVE, R_DIVE), 15.0, sp)   # ★ 당기면서 한반도를 한가운데로
    say("우리 눈은 카메라다. 당겨 보자", 5.0)
    say("한가운데가 우리나라다", 5.0)
    say("16년 동안 한 번도 놓치지 않은 그림이다", 5.0)

    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))    # 0→1 이 구름 렌더의 마스터
    feat(earth, "setCloudSpeed", 3.0)
    # ⚠️ 동기 프레임이라 시간이 흘러도 **지구는 안 돈다** — 구름만 흐른다
    dm.setDateTime(2026, 8, 17, 3, 30, 0, tz, Anim(30.0))
    say("바뀌는 건 구름뿐이다", 4.0)
    say("우리가 한 일은 세 가지였다", 4.0)
    say("첫째, 날씨 — 태풍이 어디로 갈지, 비가 언제 올지", 5.0)
    say("둘째, 통신을 이어 줬다", 4.0)
    say("셋째, 바다를 봤다 — 하루 여덟 번", 4.5)
    say("정지궤도에서 바다를 본 건 세계에서 우리가 처음이었다", 5.0)
except Exception as e:
    print("막4 오류:", e)

# ══ 막5 : 마감 — 정지궤도에서 폐기궤도로 떠난다 ════════════════
# ⚠️ [2026-08-13 지시] "정지궤도에 있다가 폐기궤도로 떠나는 걸 보여줘야지."
#    → 두 궤도선을 **먼저 둘 다** 켜서 어디서 어디로 가는지 보이게 한 뒤,
#      위성이 금색 원에서 회색 원까지 **14초에 걸쳐 건너간다**. 그게 이 막의 전부다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.4))
    sleep(0.5)
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    dm.stop()                       # ★ 궤도선을 켜기 전에 시계를 멈춘다
    sleep(0.2)
    stand(Vec(0.0, B_TOP, R_BACK), ip)
    # 위성을 제 자리(정지궤도)에 되돌려 놓고 다시 보이게 한다
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GEO_R), Anim(0.0))
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    txt = sub_space()
    txt.setText("2025년 12월")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    feat(r_geo, "setIntensity", 1.0, Anim(3.0))           # ★ 금색 = 일하던 자리
    say("천리안이 16년을 돈 자리다", 4.5)
    say("설계 수명은 7년이었는데", 4.0)
    say("2010년에 태어난 아기가 고등학생이 될 때까지 일했다", 5.0)
    say("2025년 12월, 임무가 끝났다", 4.5)

    feat(r_grave, "setIntensity", 0.9, Anim(3.0))         # ★ 회색 = 갈 곳
    say("저 바깥 회색 원이 갈 곳이다", 4.5)
    # ★★ 이 한 줄이 이 막의 핵심 — 금색에서 회색으로 건너간다
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(14.0))
    say("남은 마지막 연료로 위로 올라간다", 5.0)
    say("천천히, 아주 천천히", 5.0)
    say("일하던 자리를 다음 위성에게 비켜 주는 것이다", 5.5)
    say("(실제로는 아주 조금 위다. 보이라고 크게 그렸다)", 4.0)

    # ⚠️ 불은 꺼지되 **사라지지 않는다**("마지막엔 천리안 보여주지도 않는다"는 지적)
    feat(sat, "setIntensity", 0.35, Anim(6.0))
    say("그리고 전원을 껐다", 4.0)
    say("천리안 1호는 지금도 저기 있다", 4.0)

    # 후계 — 비워 준 그 금색 원 위에 둘이 더
    s2a = place_sat(6, LON_2A, SCALE_SAT * 0.8)
    feat(s2a, "setIntensity", 1.0, Anim(2.5))
    say("2018년, 천리안 2A 가 날씨를 이어받았고", 4.0)
    s2b = place_sat(7, LON_2B, SCALE_SAT * 0.8)
    feat(s2b, "setIntensity", 1.0, Anim(2.5))
    say("2020년, 2B 가 바다와 공기를 이어받았다", 4.0)
    say("7년만 버티면 되던 기계가, 16년을 벌어 준 자리다", 5.0)

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(3.0)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 천리안 1호, 여정과 마감")

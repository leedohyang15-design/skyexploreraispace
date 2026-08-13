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
#    ⚠️ **v9 에서 아직 돔에서 못 본 것**: Intro 하강(R 26→3.4) · Scene 1 이륙 고도 R=1.6 ·
#       Scene 3 돔 시계 HUD(우주 프레임에서의 distance 미검증) · Outro 도시 불빛 + 지상 복귀 ·
#       그리고 **디테일을 넣은 새 모델**(35조각 — 솔라세일·관측기 두 대·안테나 3종).
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "지구를 바라보는 하나의 눈 — 천리안 1호의 11년"   (약 5분)
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
#  ⚠️⚠️⚠️ 규칙 3 — 위성의 눈(동기 프레임)과 밖에서 보기(관성 프레임)를 **의도적으로** 나눈다
#     · **동기(sp)** 에 서면 지구가 안 도는 게 정상이다 — 정지궤도 위성이 보는 그림.
#     · **관성(ip)** 에 서야 지구가 도는 게 보인다 — 낮밤·정지궤도 설명은 여기서만 성립한다.
#
#  ══ v9 — 사용자 대본으로 전면 재구성 (2026-08-13) ══
#
#  대본 "지구를 바라보는 하나의 눈, 천리안 1호의 11년" 5장 구성을 그대로 옮겼다.
#
#  ⚠️⚠️ **사실 정정 — 16년이 아니라 11년이다.**
#     전 판은 "16년 / 2025년 12월 임무 종료"로 썼는데 **틀렸다.**
#     천리안 1호는 **2010-06-27 발사 → 2021년 4월 폐기궤도 이동**, 약 **11년** 운용이다.
#     (기상 임무는 2018년 2A, 해양은 2020년 2B 로 이관.) 대본이 맞고 내가 틀렸다.
#     → 스크립트·대본·패키지 문서의 연수와 날짜를 전부 11년/2021년 4월로 고쳤다.
#
#  ⚠️ **대본대로 못 하는 것 하나 — 로켓**: 발사대와 화염은 이 빌드에서 못 그린다
#     (지상 3D 자산이 없다). Scene 1 은 **로켓에 올라탄 시점의 상승**으로 대체했다.
#     실제로 로켓을 보여주려면 고리처럼 모델을 하나 더 구우면 된다(가능하다).
#
#  구성 (대본의 시간표를 따른다)
#    Intro    광활한 우주와 하나의 결심          0:00–0:40
#    Scene 1  쿠루 우주센터와 카운트다운          0:40–1:20
#    Scene 2  3만 6천 km 상공의 파수꾼           1:20–2:20
#    Scene 3  임무 연장과 헌신                   2:20–3:20
#    Scene 4  마지막 여정, 폐기궤도로의 이동      3:20–4:20
#    Outro    유산과 기억                        4:20–5:00
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
SLOT_SAT, SLOT_2A, SLOT_2B = 5, 6, 7    # Insert3D 슬롯 — 위성 세 대

# ★ 돔 시계 — Scene 3 의 '수명 7년 타임랩스'. 시간가속을 걸면 바늘이 실제로 돈다(검증됨).
#   ⚠️⚠️ **기본 끔** — 돔에서 두 번 다 이상하게 나왔다("시계 또 지랄이네").
#   지상 장면에서만 검증된 HUD 라 우주 프레임에서는 자리·크기가 안 맞는 것으로 보인다.
#   살려 보고 싶으면 True 로 하고 `clock_hud()` 의 setDistance 를 1.0 ↔ 20 으로 A/B 할 것.
SHOW_CLOCK = False

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
# 무덤궤도 — ⚠️ 실제는 정지궤도 300km 위(0.7% 차이 = 화면에서 안 보인다).
# "이탈할 때 너무 안 보인다"는 지적을 받아 **크게 과장**했다. 나레이션에서 고지한다.
GRAVE_R = 10.5                          # 지구반지름 단위(≈67,000km) — GEO 6.611 대비 59% 바깥
KOREA_LON = 128.2                       # 천리안 1호의 정지궤도 경도
LON_2A, LON_2B = 133.0, 123.5           # ⚠️ 실제 2A·2B 도 128.2 부근이지만 겹쳐 보여서 벌렸다

B_TOP = 88.0                  # 북극 위. **각도는 건드리지 않는다**(프레이밍이 깨진 건 늘 각도였다)

# ★ Intro — 딥 스페이스에서 한반도 상공으로 (동기 프레임 하나로 처리)
R_DEEP = 26.0                 # 지구가 먼 점. 은하수가 돔을 채운다
R_INTRO_END = 3.4             # 한반도 상공 탑뷰(각지름 약 35°)

# ★ Scene 1 — 쿠루에서 정지궤도까지
# ⚠️⚠️ **로켓 모델 자리 — 파일명만 넣으면 붙는다.**
#   지금은 None 이라 로켓 없이 '올라타서 올라가는' 상승만 나온다.
#   유저 폴더에서 후보를 찾으려면 `scripts/study/scan_rocket_models.py` 를 돌릴 것
#   (그 폴더에 모델이 1,282개 있고 우주선 계열만 151개다 — 이미 있을 가능성이 높다).
#   경로를 넣으면 Scene 1 에서 **로켓이 우리 옆에서 같이 솟아오른다.**
ROCKET_MODEL = None           # 예: "Metaspace/ariane5/ariane5.osg"
ROCKET_SLOT = 8
ROCKET_SCALE = 6.0e5          # 로켓 길이 ~50m 기준. 화면에서 너무 크면 3e5, 작으면 1e6
ROCKET_LON_OFF = -9.0         # 카메라 경도에서 이만큼 옆에 둔다(정면이면 화면을 다 덮는다)
KOURU_LON = -52.8             # 프랑스령 기아나 쿠루 발사장 경도
R_LAUNCH = 1.6                # 이륙 고도(≈3,800km). 지구가 발밑을 채운다
#   ⚠️ 1순위 조정 손잡이. 지표가 뭉개지거나 화면이 비면 1.9~2.2 로 올릴 것

# ★ Scene 2 — 파수꾼 (위성 옆에서 지구를 함께 본다)
R_WATCH_A, R_WATCH_B = 10.0, 8.3
#  ⚠️ 7.6 은 위성까지 6,300km 라 태양전지판 하나가 돔을 다 덮었다(돔 실측).
#     8.3 이면 10,800km — 위성이 화면 절반, 뒤로 지구도 들어온다

# ★ Scene 3 — 같이 돈다 (관성 프레임 오블리크라야 낮밤 경계가 보인다)
B_TOGETHER, R_TOGETHER = 40.0, 9.0

# ★ Scene 4 — 이탈
R_BACK = 13.0                 # 궤도 두 개가 다 들어오는 거리
R_OUT = 20.0                  # 줌아웃 도착점 — 지구가 멀어진다

# ★ Outro — 도시 불빛 → 세 위성 → 지상
B_CITY, R_CITY = 28.0, 3.4    # 한반도 밤 쪽을 내려다보는 자리(지구 각지름 ~35°, 불빛이 보인다)
#   ⚠️⚠️ 여기서는 **위성이 안 보이는 게 맞다** — 정지궤도(6.611)보다 안쪽이라 카메라 뒤에 있다.
#      (전 판은 이 자리에서 위성을 보여주려 했다. 기하학적으로 불가능했다.)
B_FINAL, R_FINAL_A, R_FINAL_B = 45.0, 14.0, 10.2
#   ★ 마지막 타블로 — 오블리크로 궤도면을 비스듬히 보고 **14 → 10.2 로 줌인**한다.
SCALE_FINAL = 2.2             # ⚠️ "마지막에 위성들 너무 작아" — 이 장면에서만 크게 키운다
R_LAND = 2.0                  # 지상 전환 직전까지 내려온다

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


def hide(ins, times=3):
    """⚠️ **끈 게 안 꺼지는 일이 있다** — 모델이 로드를 마치며 밝기를 되돌리는 것으로 보인다.
    (돔 실측: 켜지면 안 되는 장면에서 궤도선·위성이 보였다.)
    → 한 번 끄고 끝내지 말고 **프레임을 사이에 두고 몇 번 다시 누른다.**"""
    for _ in range(times):
        feat(ins, "setIntensity", 0.0, Anim(0.0))
        sleep(0.15)


def clear_leftovers():
    """⚠️⚠️⚠️ **앞 실행이 남긴 개체를 전부 끈다. 돔에서 두 가지가 이걸로 깨졌다.**

      ① **'분신술'** — 위성이 둘로 보였다. 앞 쇼가 켜 둔 2A·2B(Insert3D 슬롯)가 살아 있었다.
      ② **'궤도선이 옛날 것'** — 나선 호가 다시 나왔다. v9 코드에는 `OrbitalPlace` 가
         **한 줄도 없다** — 새로 만들어질 수가 없다. 즉 화면의 그 호는 전부
         **앞 판(v8)이 켜 두고 간 `OrbitalPlace`** 였다.

    ⚠️ 원인은 하나다: **`SceneGraph().reset(1)` 은 Insert3D·OrbitalPlace 슬롯을 안 비운다.**
       씬을 초기화해도 이 개체들은 제 슬롯에 그대로 남아 다음 실행 화면에 끼어든다.
    → 쇼 첫머리에서 **우리가 쓰는 슬롯 범위를 싹 꺼 놓고** 시작한다. 이건 매번 해야 한다."""
    n = m = 0
    for i in list(range(0, 12)) + list(range(38, 50)):
        try:
            Insert3D(Insert3D.Insert3DName(i)).setIntensity(0.0, Anim(0.0))
            n += 1
        except Exception:
            pass
    for i in range(0, 10):
        try:
            o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(i))
            o.setOrbitIntensity(0.0, Anim(0.0))     # ★ 옛 나선 궤도선을 끈다
            try:
                o.setIntensity(0.0, Anim(0.0))
            except Exception:
                pass
            m += 1
        except Exception:
            pass
    print("   앞 실행 잔여 정리 — Insert3D %d개 · OrbitalPlace %d개" % (n, m))


def place_sat(slot, lon, scale=SCALE_SAT):
    """★ 정지궤도 위성 하나 — **동기 프레임의 경도**에 놓는다.
    이 프레임의 경도 = 지구 경도라서 그 자리에 붙고, 지구가 돌면 같이 돈다.
    손으로 밀 필요가 없다(v4 의 '급발진'은 손으로 밀면서 시간가속까지 걸어서 났다)."""
    ins = load_model(slot)
    hide(ins)
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
    hide(ins)
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))   # 그림자로 반쪽이 어두워지지 않게
    feat(ins, "setScale", radius_m, Anim(0.0))
    feat(ins, "setOrientationHPR", RING_HPR, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setPositionLBR", Vec(0.0, 0.0, 0.0), Anim(0.0))   # 지구 중심
    return ins


def clock_hud():
    """돔 시계 HUD — 수명을 세는 시계. ⚠️ `setModelset` 을 안 걸면 아무것도 안 그려진다."""
    if not SHOW_CLOCK:
        return None
    try:
        c = Clock(Clock.ClockName.Clock001)
        feat(c, "setModelset", Clock.Modelset.SystemClock001)
        cam.addChild(c.id, Camera.CameraPort.FixedForeground)
        feat(c, "setPosition", Vec(0.0, 62.0, 0.0))
        feat(c, "setSize", 0.34)
        feat(c, "setDistance", 1.0)
        feat(c, "setDisplaySecondsHand", True)
        feat(c, "setSecondsHandColor", Vec(0.95, 0.35, 0.25))
        feat(c, "setIntensity", 0.9, Anim(1.5))
        return c
    except Exception as e:
        print("   시계 실패: %s" % e)
        return None


def ground_night():
    """우주 → 지상 복귀. ⚠️ 검증된 경로는 **암전 속 reset(1) 후 지상 전체 재세팅**이다
    (좌표만 바꾸면 카메라가 우주 프레임에 남는다)."""
    _dark()
    SceneGraph().reset(1)
    _dark(1.5)
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))    # 지상 하늘 쇼 = 대기 OFF
    feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))       #               + 지면 OFF
    feat(earth, "setElevationScale", 0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    _dark()
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 13, 0, 0, tz, Anim(0.0))     # 청주 22:00 KST
    _dark()
    sleep(0.4)
    cam.setOrientationH(H_SOUTH, Anim(0.0))
    _dark()
    cam.setTargetHeight(TILT_SOUTH, Anim(0.0))
    _dark()


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


# ══ Intro : 광활한 우주와 하나의 결심 (0:00–0:40) ══════════════
# 대본: "깊은 밤하늘과 은하수 → 시점이 서서히 한반도 상공으로 내려온다.
#        한반도 주변으로 어두운 구름이 밀려드는 연출. 딥 스페이스 뷰 → 한반도 탑뷰."
# ⚠️ 프레임 전환 없이 **동기 프레임 하나로** 처리한다 — 한반도 경도에 선 채 R 만 줄이면
#    '딥 스페이스에서 한반도 상공으로 내려오는' 하강이 그대로 된다(전환 슬루가 없어 깨끗하다).
try:
    _dark()
    SceneGraph().reset(1)
    _dark(1.5)
    clear_leftovers()        # ★ 앞 실행 잔여 정리 — 분신술·옛 나선 궤도선의 원인. reset 은 안 해 준다
    _dark()
    enter_space()

    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))    # 한반도가 낮
    _dark()
    sleep(0.4)

    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))   # 은하수
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))
    _dark()

    sat = place_sat(SLOT_SAT, KOREA_LON)     # 미리 올려두되 꺼 둔다
    feat(sat, "setIntensity", 0.0, Anim(0.0))
    r_geo = ring(RING_SLOT_GOLD, RING_GOLD, GEO_R * EARTH_R_M)     # 시계 멈춘 지금 만든다
    r_grave = ring(RING_SLOT_GRAY, RING_GRAY, GRAVE_R * EARTH_R_M)
    hide(r_geo)              # ⚠️ 궤도선은 **Scene 4 에서만** 켠다. 여기서 확실히 눌러 둔다
    hide(r_grave)
    _dark()

    if sp is not None:
        stand(Vec(KOREA_LON, 0.0, R_DEEP), sp)   # ★ 딥 스페이스 — 지구가 먼 점
    txt = sub_space()
    txt.setText("천리안 1호")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
    sleep(3.5)
    say("기상과 바다를 스스로 볼 수 없던 시절", 5.0)
    say("우리는 우주에 우리만의 눈을 가지려 했다", 5.0)

    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_INTRO_END), 20.0, sp)   # ★ 한반도 상공으로 하강
    feat(earth, "setCloudsIntensity", 0.85, Anim(8.0))    # 어두운 구름이 밀려든다
    feat(earth, "setCloudSpeed", 3.0)
    say("2010년 6월", 4.5)
    say("대한민국 첫 정지궤도 위성", 5.0)
    say("천리안 1호의 여정이 시작된다", 6.0)
except Exception as e:
    print("Intro 오류:", e)

# ══ Scene 1 : 쿠루 우주센터와 카운트다운 (0:40–1:20) ════════════
# 대본: "아리안 5호 발사 → 로켓을 따라 돔 최상단으로 고속 상승."
# ⚠️⚠️ **로켓 모델이 없다.** 발사대·화염은 이 빌드에서 못 그린다(지상 3D 자산이 없다).
#    → 대신 **로켓에 올라탄 시점**으로 간다: 쿠루 상공(-52.8°E) 저고도에서 정지궤도까지
#      22초에 걸쳐 솟아오른다. 관객이 보는 것은 '발밑의 지구가 멀어지는' 상승 그 자체다.
#    (로켓을 실제로 보여주려면 모델을 하나 더 구워야 한다 — 고리처럼 가능은 하다.)
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.6))
    sleep(0.8)
    feat(earth, "setCloudsIntensity", 0.35, Anim(0.0))
    hide(r_geo, 1)                      # ⚠️ 돔에서 Scene 2 에 궤도선이 보였다 — 장면마다 다시 누른다
    hide(r_grave, 1)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2010, 6, 26, 21, 41, 0, tz, Anim(0.0))   # 실제 발사 시각(UTC)
    _dark()
    sleep(0.4)
    if sp is not None:
        stand(Vec(KOURU_LON, 0.0, R_LAUNCH), sp)     # 쿠루 상공, 발밑이 지구

    # ★ 로켓 — ROCKET_MODEL 이 있을 때만. 우리 옆에서 같이 솟아오른다.
    #   ⚠️ 위성과 똑같은 방식이다(동기 프레임 경도에 놓고 R 을 애니메이션).
    #      카메라와 같은 경도에 두면 모델이 화면을 다 덮으므로 9° 옆에 둔다.
    rocket = None
    if ROCKET_MODEL:
        rocket = load_model(ROCKET_SLOT, ROCKET_MODEL)
        hide(rocket)
        feat(rocket, "setShadowStrength", 0.0, Anim(0.0))
        feat(rocket, "setScale", ROCKET_SCALE, Anim(0.0))
        feat(rocket, "setOrientationHPR", Vec(0.0, 0.0, 0.0), Anim(0.0))
        feat(rocket, "setParent", sp if sp is not None else ip)
        feat(rocket, "setPositionLBR",
             Vec(KOURU_LON + ROCKET_LON_OFF, 0.0, R_LAUNCH), Anim(0.0))
    txt = sub_space()
    txt.setText("2010년 6월 27일")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)
    if rocket:
        feat(rocket, "setIntensity", 1.0, Anim(1.5))
    say("2010년 6월 27일, 쿠루 우주센터", 5.0)
    say("아리안 5호가 화염을 뿜으며 하늘을 가른다", 5.5)

    if sp is not None:
        fly(Vec(KOURU_LON, 0.0, GEO_R), 22.0, sp)    # ★ 로켓을 따라 고속 상승
    if rocket:                                        # 로켓도 같이 솟아오른다
        feat(rocket, "setPositionLBR",
             Vec(KOURU_LON + ROCKET_LON_OFF, 0.0, GEO_R), Anim(22.0))
    say("그 정상에 천리안 1호가 실려 있다", 5.5)
    say("올라간다", 4.5)
    say("3,000km … 10,000km … 20,000km", 6.0)
    say("지구 상공 3만 6천 킬로미터", 6.0)
    say("정지궤도를 향한 도약이다", 5.0)
    if rocket:
        hide(rocket, 1)          # 도착하면 로켓은 분리돼 사라진다
except Exception as e:
    print("Scene 1 오류:", e)

# ══ Scene 2 : 3만 6천 km 상공의 파수꾼 (1:20–2:20) ══════════════
# 대본: "지구가 돔 중앙에 거대하게, 천리안이 태양전지판을 펼치며 서서히 회전.
#        위성 바로 옆에서 지구를 함께 바라보는 3인칭 광각 뷰."
# ★ 동기 프레임이라 **지구가 안 도는 게 정상**이다 — 정지궤도 위성이 보는 그림 그대로.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2011, 4, 1, 3, 30, 0, tz, Anim(0.0))    # 정규 서비스 시작 무렵, 한반도 낮
    hide(r_geo, 1)                      # ★ 이 장면에 궤도선이 보이면 안 된다(돔 실측으로 걸렸다)
    hide(r_grave, 1)
    _dark()
    if sp is not None:
        stand(Vec(KOREA_LON, 0.0, R_WATCH_A), sp)   # 위성이 카메라와 지구 사이
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    txt = sub_space()
    txt.setText("동경 128.2도")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)
    # ★ 태양전지판을 펼치듯 천천히 한 바퀴 (카메라를 안 건드려 프레이밍 위험 0)
    feat(sat, "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(30.0))
    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_WATCH_B), 16.0, sp)      # 위성 쪽으로 다가간다
    say("동경 128.2도", 4.0)
    say("지구가 도는 속도에 딱 맞춰 함께 돈다", 5.5)
    say("그래서 24시간 한반도를 내려다본다", 5.5)
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.5)
    say("반대편 막대 끝의 반사판이 그 힘을 받아 균형을 잡는다", 6.0)
    say("가운데 접시는 안테나, 아래 두 개가 관측기다", 5.5)

    feat(earth, "setCloudsIntensity", 1.0, Anim(6.0))
    dm.setDateTime(2011, 4, 6, 3, 30, 0, tz, Anim(26.0))   # 구름이 흐른다(지구는 안 돈다)
    say("기상 관측기가 구름을 읽고", 5.0)
    say("해양 관측기가 바다를 읽는다", 5.0)
    say("태풍의 길목을 미리 알리고, 적조와 기름 유출을 감시했다", 6.5)
    say("가장 높은 곳에서 우리를 지켜보는 눈이었다", 5.5)
except Exception as e:
    print("Scene 2 오류:", e)

# ══ Scene 3 : 임무 연장과 헌신 (2:20–3:20) ══════════════════════
# 대본: "수명 7년을 가리키는 시계 타임랩스. 2017년이 지나도 계속 도는 천리안.
#        2A·2B 가 등장해 바통을 넘겨받는다."
# ★ 돔 시계(Clock)는 검증된 HUD 다 — 시간가속을 걸면 바늘이 실제로 돈다.
# ★ 프레임을 **관성(ip)** 으로 바꾼다 — 여기서만 지구가 도는 게 보이고, 낮밤이 지나간다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    stand(Vec(0.0, B_TOGETHER, R_TOGETHER), ip)
    hide(r_geo, 1)
    hide(r_grave, 1)
    shadows(True)                       # 낮밤 — 이 막은 그림자가 주제라 운영 표준의 예외
    _dark()
    clk = clock_hud()                   # ★ 수명을 세는 시계
    txt = sub_space()
    txt.setText("설계 수명 7년")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)
    say("당초 설계된 수명은 7년", 4.5)
    say("2017년이면 끝났어야 할 기계다", 5.0)

    # ⚠️ 손으로 밀지 않는다. 시간만 흘리면 엔진이 위성을 데려간다
    dm.setDateTime(2011, 4, 8, 3, 30, 0, tz, Anim(48.0))   # 이틀 = 낮밤 두 번 + 시계 회전
    say("하지만 천리안 1호는 멈추지 않았다", 5.5)
    say("낮이 가고 밤이 오고, 다시 낮이 오는 동안", 6.0)
    say("한 자리에서 데이터를 계속 보냈다", 6.0)
    say("설계 수명을 넘긴 뒤로도 4년을 더", 5.5)
    say("모두 합쳐 11년", 5.0)

    s2a = place_sat(SLOT_2A, LON_2A, SCALE_SAT * 0.8)
    feat(s2a, "setIntensity", 1.0, Anim(2.5))
    say("2018년, 천리안 2A 가 기상을 이어받고", 5.0)
    s2b = place_sat(SLOT_2B, LON_2B, SCALE_SAT * 0.8)
    feat(s2b, "setIntensity", 1.0, Anim(2.5))
    say("2020년, 2B 가 해양과 환경을 이어받았다", 5.0)
    say("후배들에게 바통을 넘길 때까지, 제자리를 지켰다", 5.5)
except Exception as e:
    print("Scene 3 오류:", e)

# ══ Scene 4 : 마지막 여정, 폐기궤도로의 이동 (3:20–4:20) ════════
# 대본: "추진기가 미세하게 점화. 정지궤도 ring 을 벗어나 더 높은 폐기궤도로.
#        전원이 차례로 꺼지며 어두워진다. 지구가 멀어지는 줌아웃."
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    if clk:
        feat(clk, "setIntensity", 0.0, Anim(0.5))    # 시계는 여기서 내린다
    shadows(False)                                   # 원반 전체를 밝게 = 궤도가 잘 보인다
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    dm.stop()
    sleep(0.2)
    stand(Vec(0.0, B_TOP, R_BACK), ip)
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GEO_R), Anim(0.0))
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    txt = sub_space()
    txt.setText("2021년 4월")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)
    feat(r_geo, "setIntensity", 1.0, Anim(3.0))      # ★ 금색 = 11년을 돈 자리
    say("2021년 4월, 임무가 끝났다", 5.0)
    say("저 금색 원이 11년을 돈 자리다", 5.5)
    feat(r_grave, "setIntensity", 0.9, Anim(3.0))    # ★ 회색 = 갈 곳
    say("다른 위성과 부딪히지 않도록", 5.0)
    say("스스로 몸을 일으킨다", 4.5)

    # ★★ 이 한 줄이 이 장면의 핵심 — 금색에서 회색으로 건너간다
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(16.0))
    say("남은 연료를 모두 태우며", 5.5)
    say("정지궤도보다 높은 폐기궤도로", 5.5)
    say("천천히, 아주 천천히 올라간다", 5.5)
    say("(실제로는 300km 남짓 위다. 보이라고 크게 그렸다)", 5.0)

    feat(sat, "setIntensity", 0.30, Anim(7.0))       # 전원이 차례로 꺼진다
    if sp is not None or True:
        fly(Vec(0.0, B_TOP, R_OUT), 14.0, ip)        # ★ 지구가 멀어지는 줌아웃
    say("모든 통신을 차단하고", 5.0)
    say("11년의 임무를 마친 채", 5.0)
    say("영원한 우주의 휴식에 들어간다", 5.5)
except Exception as e:
    print("Scene 4 오류:", e)

# ══ Outro : 유산과 기억 (4:11–5:01) ════════════════════════════
# 대본: "폐기궤도에 잠든 천리안 아래로 2A·2B, 그리고 대한민국 도시의 불빛.
#        우주에서 지상으로 천천히 내려와 관객의 시선과 맞닿는 착륙 연출."
# ⚠️⚠️ **세 비트로 나눈다** — 도시 불빛과 세 위성은 **같은 자리에서 못 본다**(기하학적으로).
#    도시 불빛은 지구에 바짝 붙어야 보이고(R 3.4), 위성은 정지궤도 바깥에서 봐야 보인다(R 10+).
try:
    # ── ① 도시 불빛 (지구 가까이) ──────────────────────────────
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    shadows(True)                                    # ★ 밤면 = 도시 불빛
    hide(sat, 1)                                     # 이 자리에선 어차피 카메라 뒤다
    stand(Vec(KOREA_LON, B_CITY, R_CITY), sp)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 13, 0, 0, tz, Anim(0.0))   # 한반도 밤(22시 KST)
    _dark()
    txt = sub_space()
    txt.setText("그 길을 따라")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(2.5)
    say("저 아래 불빛 하나하나가 우리가 사는 곳이다", 6.0)
    say("천리안 1호가 열어 준 길을 따라", 5.5)

    # ── ② 세 위성 타블로 — ⚠️ "너무 작아"를 고친 자리 ────────────
    #    오블리크(B45)로 궤도면을 비스듬히 보고, **크게 키운 뒤 줌인**한다.
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    shadows(False)
    stand(Vec(0.0, B_FINAL, R_FINAL_A), ip)
    feat(sat, "setScale", SCALE_SAT * SCALE_FINAL, Anim(0.0))       # ★ 크게
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(0.0))
    feat(sat, "setIntensity", 0.32, Anim(0.0))                      # 불은 꺼진 채로
    for _s in (s2a, s2b):
        feat(_s, "setScale", SCALE_SAT * 0.8 * SCALE_FINAL, Anim(0.0))
        feat(_s, "setIntensity", 1.0, Anim(0.0))
    feat(r_geo, "setIntensity", 1.0, Anim(0.0))
    feat(r_grave, "setIntensity", 0.9, Anim(0.0))
    txt = sub_space()
    txt.setText("자리는 비지 않았다")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)

    fly(Vec(0.0, B_FINAL, R_FINAL_B), 12.0, ip)      # ★ 줌인 — 위성들이 커진다
    say("더 나은 위성들이 그 자리를 이어받고 있다", 6.0)
    say("바깥 회색 원에 천리안 1호가, 안쪽 금색 원에 2A 와 2B 가 있다", 6.5)
    say("우리 우주 역사의 첫 장을 연 이름 — 천리안 1호", 6.0)

    # ── ③ 지상으로 ────────────────────────────────────────────
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.8)
    ground_night()                                   # 청주 밤하늘 — 관객의 자리로
    txt = sub_ground()
    txt.setText("천리안 1호")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
    sleep(2.5)
    say("그 별은 지금도 저 높은 곳에서", 5.0)
    say("우리의 다음 도전을 내려다보고 있다", 5.5)

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(3.0)
except Exception as e:
    print("Outro 오류:", e)

print("쇼 종료 — 지구를 바라보는 하나의 눈, 천리안 1호의 11년")

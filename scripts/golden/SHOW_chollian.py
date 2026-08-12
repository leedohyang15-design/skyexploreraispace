# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인(v3) — 돔 재생 2회.
#        v1(1차): ① 우주 장면 4분 내내 자막이 안 뜸 ② 지구에 색이 없음 ③ 카메라가 안 움직임
#                 ④ 궤도선 구분 불가 ⑤ 너무 멀어 지구가 점 ⑥ 막3 이 텅 빈 우주 — 전부 확인.
#        v2(2차): **자막은 떴다(①  해결 확인)**. 그런데 카메라를 관성 프레임으로 옮기면서
#                 조준을 같이 안 옮겨 **지구·궤도선·위성이 통째로 화면 밖으로 나갔다.**
#        v3: 프레임 전환을 되돌렸다(track=-1, v1 에서 지구가 보이던 그 프레임). **미확인.**
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
#  ══ v1 돔 재생에서 깨진 것과 고친 방법 (2026-08-12) ══
#
#  ① ⚠️⚠️ **자막이 우주 장면에서 통째로 안 떴다** — 0:40 부터 4분간 글자가 하나도 없었다.
#     원인: `sub()` 헬퍼가 우주 프레임에서도 `setSize()` 를 불렀다.
#     지식베이스에 **이미 적혀 있던 규칙**이다 — "행성 프레임 자막은 setSize 호출 금지(기본값
#     유지) + setDistance(20)". 어기면 자막이 화면에서 사라진다(ISS v3 실패로 실측된 것).
#     → 헬퍼를 프레임별로 갈랐다. **헬퍼는 편한 만큼 규칙을 숨긴다.**
#
#  ② ⚠️⚠️ **지구에 색이 없었다.** 막0 이 지상 하늘 쇼를 위해 `setTerrainIntensity(0)`·
#     `setAtmosphereIntensity(0)` 을 끄는데 **우주로 나간 뒤 되살리는 곳이 없었다.**
#     멀리서는 회색 공, 가까이(막3, R=3.2)서는 **아예 안 보였다** — 그릴 표면이 없으니까.
#     → `geo_view()` 에서 지구 렌더를 통째로 복구한다.
#
#  ③ ⚠️ **카메라가 5분 내내 안 움직였다** — 카메라 호출 8개가 전부 `Anim(0.0)` 점프컷이었다.
#     → 긴 단일 Anim 으로 아주 느리게 민다(막1 밀어넣기, 막2 기울이기).
#     ⚠️⚠️ **v2 는 여기서 관성 프레임 전환까지 얹었다가 화면을 통째로 날렸다.**
#        검증된 전환 레시피는 `setPositionLBR(...,ip)` **+ `setOrientationSmoothXYZR(...,ip)`**
#        두 줄인데 위치만 옮겨 카메라가 지구가 없는 쪽을 봤다. → v3 에서 전환을 포기.
#        **움직임은 프레임이 아니라 위성을 직접 돌려서 만든다.**
#
#  ④ ⚠️ **궤도선을 구분할 수 없었다.** `OrbitalPlace` 는 궤도선 전용이라 본체도 라벨도 없다
#     — 40초 시간가속 동안 실제로 움직이는 게 **아무것도 없었다.**
#     → 위성을 `Insert3D` 모델로 **직접 궤도 위에서 돌리고**, 색 맞춘 범례 자막을 상시 띄운다.
#
#  ⑤ ⚠️ **너무 멀었다.** `R=20`(127,563km)에서 지구 각지름은 5.7° — 180° 돔에서 점이다.
#     "이게 어떻게 위에서 내려다보는 구도냐"는 지적이 나왔다. 카메라 각도(B=88)는 맞았고
#     **거리가 문제**였다. 북극 위에서는 링이 원형이라 R 을 줄여도 안 잘린다 → **R=10**.
#     (예전에 실패한 R=12 는 B=35 **비스듬**이라 링이 앞뒤로 늘어져 잘렸던 것.)
#
#  ⑥ ⚠️ **막3 이 텅 빈 우주에 궤도선 두 개**였다. ②에 더해, 막3 진입 때 노란 궤도선만 끄고
#     ISS·GPS 를 안 껐다. → 궤도선 핸들을 모듈 수준에 모아 **전부** 끈다.
#
#  ══ 지킨 규약 (골든 쇼 공통) ══
#    · 암전은 reset **보다 먼저**. reset/FadeTo 가 밝기를 1.0 으로 되돌리니 클램프로 눌러둔다
#    · 자막 홀드는 글자 수로 자동 계산(2초 + 글자당 0.1초)
#    · 자막 거리: **지상 = size 0.052 + distance 1.0 / 우주 = size 만지지 말 것 + distance 20**
#    · 시간가속 구간은 ~5초마다 자막을 갈아준다
#    · 막마다 try/except
#
#  구성
#    막0  올려다보기 — 남쪽 하늘 저 위               (~40초)
#    막1  지구 밖으로 — 그 자리                      (~45초)
#    막2  왜 안 움직일까 — 하루를 40초로             (~78초)
#    막3  무엇을 봤나 — 하루 여덟 번의 바다          (~57초)
#    막4  마감 — 불이 꺼진다                         (~53초)
#    막5  자리는 비지 않았다                         (~27초)
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

# ── 궤도 조망 구도 ─────────────────────────────────────────────
#  B=88(북극 위)은 v1 에서 맞았다. R 만 20 → 10 으로 당긴다.
#    R=20 → 지구 각지름 5.7°(점) / R=10 → 11.4°, GEO 링 지름 67° (계산값)
B_TOP, R_TOP = 88.0, 10.0
R_PUSH = 8.5                  # 막1 이 끝날 때까지 아주 느리게 밀어넣는 목표
B_TILT = 55.0                 # 막2 동안 천천히 기울일 목표 — 지구가 입체로 보인다
B_NEAR, R_NEAR = 25.0, 3.2    # 막3 지구 클로즈업

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름
GPS_R = 26560000.0 / EARTH_R_M          # 4.164 (평균운동 2.005 에 대응)
ISS_R = 6738000.0 / EARTH_R_M           # 1.056
GRAVE_MM = 0.78                         # 무덤궤도 과장판
GRAVE_R = 49840000.0 / EARTH_R_M        # 7.814

# 위성 배율 — v1 은 R=20 에서 ×1e6 이 보기 좋았다(사용자 선택).
# 이번엔 카메라가 절반 거리로 오므로 **같은 겉보기 크기를 유지하려면 배율도 절반**.
SCALE_ORBIT = 5.0e5           # 반지름 2,636km → 겉보기 지름 약 4.7° (v1 과 동일)
SCALE_SMALL = 2.5e5           # ISS·GPS 는 더 작게
SCALE_CLOSE = 3.0e6           # 클로즈업은 카메라 대신 배율로

# 청주에서 128.2°E 정지위성: cos γ = cos(36.64°)·cos(0.71°) = 0.8023 → 고도 47.5°, 거의 정남
H_SOUTH, TILT_SOUTH = 0.0, 40.0

# ── 시계 ───────────────────────────────────────────────────────
#  ⚠️ v1 의 '정적'을 고치는 핵심: **자막을 붙잡고 있는 동안에도 위성이 계속 돈다.**
#     그래서 모든 대기를 STEP 단위로 쪼개고, 매 틱마다 위성 위치를 민다.
STEP = 0.3
RATE = 0.0                    # 천리안의 각속도(도/초). 막마다 갈아 끼운다
CLOCK = 0.0

txt = None
ip = None                     # 지구 관성 프레임 포트
SATS = []
ORBITS = []
LEGEND = []


def _dark(sec=0.0):
    """암전 클램프. reset/FadeTo 는 밝기를 1.0 으로 되돌리므로 한 번 눌러선 안 된다."""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def orbit_pos(u_deg, inc_deg, radius):
    """궤도면 위의 점을 지구 적도좌표(경도·위도)로. 궤도선과 정확히 겹치게 하려는 것."""
    u = math.radians(u_deg)
    i = math.radians(inc_deg)
    lat = math.degrees(math.asin(math.sin(i) * math.sin(u)))
    lon = math.degrees(math.atan2(math.cos(i) * math.sin(u), math.cos(u)))
    return Vec(lon, lat, radius)


def tick(sec):
    """대기 — 그동안 위성을 민다. 화면이 절대 멈추지 않게 하는 장치."""
    global CLOCK
    n = max(int(round(sec / STEP)), 1)
    for _ in range(n):
        CLOCK += STEP
        for s in SATS:
            if s["on"]:
                s["u"] += RATE * s["revs"] * STEP
                try:
                    # ⚠️ Anim 을 스텝보다 길게 → 다음 스텝이 겹쳐 들어가 매끄럽다
                    s["ins"].setPositionLBR(
                        orbit_pos(s["u"], s["inc"], s["r"]), Anim(STEP * 1.5))
                except Exception:
                    s["on"] = False
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


def sub(distance, slot=1, height=14.0, color=(1.0, 1.0, 0.55)):
    """자막 슬롯.
    ⚠️⚠️ **우주 프레임에서 setSize 를 부르면 자막이 사라진다** (v1 이 정확히 이걸로 죽었다).
       지상 = size 0.052 + distance 1.0 / 우주 = size 를 만지지 않고 distance 20."""
    t = InsertText(InsertText.InsertTextName(slot))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, height, 0))
    if distance <= 1.5:
        t.setSize(0.052)
    t.setColor(Vec(color[0], color[1], color[2]))
    t.setDistance(distance, Anim(0.0))
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


def add_sat(slot, radius, inc, revs, scale, u0=0.0):
    """궤도 위를 도는 위성 모델 하나."""
    ins = load_model(slot)
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setScale", scale, Anim(0.0))
    feat(ins, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
    feat(ins, "setPositionLBR", orbit_pos(u0, inc, radius), Anim(0.0))
    s = {"ins": ins, "r": radius, "inc": inc, "revs": revs, "u": u0, "on": True}
    SATS.append(s)
    return s


def geo_view():
    """FadeTo 지구 → 지구 렌더 복구 → 관성 프레임 → 북극 위 조망. 전 과정 암전."""
    global ip
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # ⚠️⚠️ [v1 버그 ②] 막0 이 지상 하늘 쇼를 위해 꺼 둔 것을 여기서 되살린다.
    #    안 하면 지구가 회색 공이 되고, 가까이 가면 그릴 표면이 없어 **아예 사라진다.**
    feat(earth, "setIntensity", 1.0, Anim(0.0))            # 지구 렌더의 마스터 스위치
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))     # ★ 막0 이 0 으로 꺼 둔 것
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)   # 블루마블
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))  # 우주에서 본 푸른 대기 림
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))      # 구름은 막3 의 비트라 아직 끈다
    # 궤도 쇼는 그림자 OFF — 지구 반쪽이 어두우면 그쪽 궤도·위성이 안 보인다
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    _dark()

    # ⚠️⚠️ [v2 가 여기서 깨졌다 — 2026-08-12 2차 돔 재생]
    #   지구를 자전시키려고 카메라를 관성 프레임(EquatorialJ2000)으로 옮겼더니
    #   **화면에서 지구·궤도선·위성이 통째로 사라졌다**(HUD 는 정상: J2000 프레임, R=8.5, B=75.7).
    #   원인: 검증된 프레임 전환 레시피는 `setPositionLBR(..., ip)` **+ `setOrientationSmoothXYZR(
    #   Vec4(0,0,0,0), Anim, ip)`** 두 줄인데 **위치만 옮기고 조준을 안 옮겼다** →
    #   카메라가 지구가 없는 방향을 보고 있었다. 화면에 남은 건 화면고정 오버레이(범례)뿐.
    #   → **프레임 전환을 포기한다.** 지구 자전 하나 얻자고 검증 안 된 걸 쌓을 이유가 없다.
    #     카메라는 FadeTo 도킹 프레임(track=-1)에 그대로 둔다 — v1 에서 지구가 보였던 그 프레임이다.
    #     ⚠️ `ip` 는 궤도선·위성을 **붙이는 용도로만** 쓴다(v1 에서 이 조합은 렌더됐다).
    #     움직임은 프레임이 아니라 **위성을 직접 돌려서** 만든다(아래 tick()).
    ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
    cam.setPositionLBR(Vec(0.0, B_TOP, R_TOP), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()


def orbit(slot, mm, ecc, inc, anomaly, color, thick=1.5):
    """지구 둘레 궤도선. 🔴 setIntensity·setLabelIntensity 는 없다 — setOrbitIntensity 만."""
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
# ⚠️ 암전을 reset 보다 먼저 — 안 그러면 직전 쇼의 마지막 화면이 그대로 번쩍인다
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

    txt = sub(1.0)                                   # 지상 자막 = size 0.052 + distance 1.0
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

    txt = sub(20.0)                     # ⚠️ 우주 프레임 — setSize 를 부르지 않는다
    txt.setText("지구 — 북극 위에서")
    _dark()

    # ⚠️ 시작 날짜는 **위성을 켜기 전, 암전 중에** 못 박는다(instant 날짜점프 = 궤도천체 순간이동)
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 0, 0, 0, tz, Anim(0.0))
    _dark()
    sleep(0.4)

    op_geo = orbit(0, 1.0027, 0.0002, 0.1, 0.0, Vec(1.0, 0.78, 0.28))
    op_iss = orbit(1, 15.50, 0.0003, 51.6, 0.0, Vec(0.45, 0.85, 1.0), 1.2)
    op_gps = orbit(2, 2.005, 0.0100, 55.0, 0.0, Vec(0.6, 1.0, 0.6), 1.2)
    _dark()

    sat = add_sat(5, GEO_R, 0.1, 1.0, SCALE_ORBIT, 0.0)
    s_iss = add_sat(6, ISS_R, 51.6, 15.5, SCALE_SMALL, 120.0)
    s_gps = add_sat(7, GPS_R, 55.0, 2.0, SCALE_SMALL, 240.0)
    _dark()

    # 지구가 45도쯤 자전하도록 시간을 아주 느리게 흘린다 — 화면이 살아 있게
    RATE = 1.125                                   # 도/초 (3시간을 40초에)
    dm.setDateTime(2026, 8, 12, 3, 0, 0, tz, Anim(40.0))
    cam.setPositionLBR(Vec(0.0, B_TOP, R_PUSH), Anim(35.0), -1)   # 아주 느린 밀어넣기
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    tick(3.0)
    say("여기가 지구다")
    say("우리가 방금 서 있던 곳이 저 아래 어딘가")
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(2.5))
    say("이 노란 원이 천리안이 도는 길이다")
    say("지구에서 36,000km — 적도 위, 동경 128.2도")
    say("지구를 한 바퀴 도는 데 딱 하루가 걸리는 높이다")
    feat(sat["ins"], "setIntensity", 1.0, Anim(2.5))
    say("저기 있다")
    say("천리안 1호")
    say("무게는 2.5톤, 펼친 길이는 8.8m — 승용차 두 대쯤")
    say("(화면에서는 보이라고 아주 크게 그렸다)")
except Exception as e:
    print("막1 오류:", e)

# ══ 막2 : 왜 안 움직일까 ═══════════════════════════════════════
try:
    # 막2 내내 아주 천천히 기울인다 — 지구가 입체로 보이고 궤도가 타원으로 누워 보인다
    cam.setPositionLBR(Vec(0.0, B_TILT, R_PUSH), Anim(70.0), -1)

    say("이렇게 높은데, 왜 안 떨어질까?")
    say("사실은 떨어지고 있다 — 다만 옆으로도 아주 빠르게 달린다")
    say("떨어지는 만큼 지구가 둥글게 휘어서, 영영 못 닿는다")
    say("다른 위성들과 견줘 보자")

    # ⚠️ [v1 버그 ④] 궤도선에는 라벨 API 가 없다 → 색 맞춘 자막 범례를 상시 띄운다
    LEGEND.append(sub(20.0, 2, 62.0, (1.0, 0.80, 0.35)))
    LEGEND[-1].setText("노랑 — 천리안 1호")
    feat(op_iss, "setOrbitIntensity", 0.85, Anim(2.0))
    feat(s_iss["ins"], "setIntensity", 1.0, Anim(1.5))
    LEGEND.append(sub(20.0, 3, 56.0, (0.5, 0.88, 1.0)))
    LEGEND[-1].setText("파랑 — 국제우주정거장")
    say("파란 원 — 국제우주정거장. 지구에 딱 붙어 있다")

    feat(op_gps, "setOrbitIntensity", 0.85, Anim(2.0))
    feat(s_gps["ins"], "setIntensity", 1.0, Anim(1.5))
    LEGEND.append(sub(20.0, 4, 50.0, (0.6, 1.0, 0.6)))
    LEGEND[-1].setText("초록 — GPS 위성")
    say("초록 원 — GPS 위성")
    say("이제 하루를 40초로 돌려 보자")

    # ── 시간가속 40초. 위성 셋이 각자 속도로 돈다 ──────────────
    #  ⚠️ 자막 홀드는 전부 8초 미만 — 길게 잡으면 화면이 멈춘 것처럼 보인다
    RATE = 9.0                                     # 도/초 = 천리안 1바퀴 / 40초
    dm.setDateTime(2026, 8, 13, 0, 0, 0, tz, Anim(40.0))
    tick(2.0)
    say("우주정거장은 쌩쌩 돈다", 5.0)
    say("90분에 한 바퀴", 4.5)
    say("GPS 는 반나절에 한 바퀴", 5.0)
    say("그럼 천리안은?", 4.5)
    say("거의 제자리다", 5.0)
    say("지구가 한 바퀴 도는 동안", 5.0)
    say("천리안도 딱 한 바퀴", 5.0)
    say("같은 속도로 도니까, 멈춰 있는 것처럼 보인다", 4.0)

    RATE = 1.125
    say("그래서 늘 한반도 위에 떠 있다")
    say("이런 자리를 정지궤도라고 부른다")
except Exception as e:
    print("막2 오류:", e)

# ══ 막3 : 무엇을 봤나 ══════════════════════════════════════════
# ⚠️ [v1 버그 ⑥] 지구를 크게 봐야 구름·바다가 읽힌다 → R 을 3.2 로 당기고
#    **궤도선과 위성을 전부 끈다**(v1 은 노란 것만 꺼서 빈 우주에 파란·초록 호만 남았다).
try:
    say("그럼 천리안은 거기서 무엇을 보고 있었을까", 3.0)
    _dark()
    txt.setIntensity(0.0, Anim(0.6))
    for t in LEGEND:
        t.setIntensity(0.0, Anim(0.6))
    sleep(0.8)
    _dark()

    for o in ORBITS:
        feat(o, "setOrbitIntensity", 0.0, Anim(0.0))
    for s in SATS:
        feat(s["ins"], "setIntensity", 0.0, Anim(0.0))
        s["on"] = False
    _dark()

    cam.setPositionLBR(Vec(0.0, B_NEAR, R_NEAR), Anim(0.0), -1)
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()

    txt = sub(20.0)
    txt.setText("천리안이 본 것")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    tick(3.0)

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
    cam.setPositionLBR(Vec(0.0, 70.0, R_TOP), Anim(0.0), -1)   # 궤도 조망으로 복귀
    _dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    _dark()
    feat(op_geo, "setOrbitIntensity", 0.95, Anim(0.0))
    sat["on"] = True
    sat["r"] = GEO_R
    feat(sat["ins"], "setIntensity", 1.0, Anim(0.0))
    _dark()

    txt = sub(20.0)
    txt.setText("16년")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    RATE = 1.6
    tick(2.5)

    say("천리안 1호의 설계 수명은 7년이었다")
    say("7년만 버티면 되는 기계였다")
    say("그런데 16년을 일했다")
    say("2010년에 태어난 아기가 고등학생이 될 만큼")
    say("2025년 12월, 임무가 끝났다")

    # 무덤궤도 — 눈에 띄게 올린 뒤 불을 끈다 (사용자 선택: 둘 다)
    op_grave = orbit(3, GRAVE_MM, 0.0002, 0.1, 0.0, Vec(0.55, 0.55, 0.6), 1.2)
    feat(op_grave, "setOrbitIntensity", 0.8, Anim(3.0))
    say("마지막 연료로 조금 더 위로 올라갔다", 0)

    # ⚠️ 위치를 매 틱마다 다시 쓰므로 Anim 으로 올리면 덮어써진다.
    #    반지름을 틱마다 조금씩 늘려 **나선으로 밀어 올린다** — 실제 궤도 상승과 같은 모양이다.
    n = int(6.5 / STEP)
    for k in range(n):
        sat["r"] = GEO_R + (GRAVE_R - GEO_R) * (k + 1.0) / n
        if k == int(n * 0.55):                 # 상승 도중에 자막을 한 번 갈아 준다
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
try:
    say("하지만 그 자리는 비지 않았다", 3.0)
    op_2a = orbit(4, 1.0027, 0.0002, 0.1, 60.0, Vec(1.0, 0.85, 0.4), 1.4)
    feat(op_2a, "setOrbitIntensity", 0.9, Anim(2.5))
    say("2018년, 천리안 2A 가 올라가 날씨를 이어받았고")

    op_2b = orbit(5, 1.0027, 0.0002, 0.1, 300.0, Vec(0.5, 0.9, 1.0), 1.4)
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

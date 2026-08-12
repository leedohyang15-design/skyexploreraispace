# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인 (2026-08-10) — 구도(L=0 세로 / L=90 과녁)·밝기 1.2 를 돔 스샷으로 확정. v3 전체 재생은 미확인(막3 스윕 속도·R_SYSTEM=15 프레이밍)
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "누워서 도는 행성 — 천왕성"   v3   (약 2분 25초)
#
#  ⚠️ v1·v2 에서 배운 것 (2026-08-10 사용자 돔 실측 + 스샷 9장)
#    ① **'누운 자세'를 결정하는 건 B 가 아니라 L 이다.** (v1·v2 최대 오류)
#       황도 프레임(`PlanetPort.Ecliptic`) + **B=0** 으로 두고 L 만 바꾸면:
#         · **L=0   → 고리·궤도가 완전한 '세로 선'**  ★"누워서 돈다"를 한 방에
#         · **L=90  → 정면 '과녁'(동심원)**          ★고리가 가장 잘 보이는 구도
#         · L=135 등 중간값 → 대각선(어중간, 쓰지 않는다)
#       v1·v2 는 L 을 FadeTo 가 준 임의값으로 두고 B 만 만졌다 → 세로가 나올 수 없었다.
#    ② **황도 포트의 R 단위 = 행성 '지름'** (도킹 프레임의 반지름 단위와 2배 차이).
#       실측 R=3.2 → 163,773 km = 6.4 천왕성반지름. v2 의 R=28 은 56 반지름이었다(과했음).
#       → 위성 궤도(오베론 22.8 반지름)를 담으려면 **R ≈ 11.4 + 여유 = 15**.
#    ③ **FadeTo 클램프 6초는 짧다** — 도킹 애니가 아직 카메라를 끌어서 `Anim(0.0)` 이 씹힌다.
#       실측: 목표 L=45 로 보냈는데 L=4.5 에서 찍혔다. → **R 이 멈출 때까지 폴링**한 뒤 구도를 꽂는다.
#    ④ **고리는 주인공이 될 수 없다.** intensity 도 setScale 도 죽은 레버(양방향 실측 확정) —
#       고리가 보이는 건 오직 구도(L=90 정면)뿐이다. 밝기는 1.2(눈이 편한 값)로 고정.
#    ⑤ 그림자는 **끈다.** '밤면을 죽여 대비를 얻자'는 안은 A/B 에서 탈락했다.
#
#  구성
#    막0  지상에서                                   (~19초)
#    막1  접근 — 황도 프레임 · L=0 · B=0             (~13초)
#    막2  세로로 선 궤도                             (~24초)
#    막3  0→90° 열기 — 세로가 과녁이 된다            (~22초)
#    막4  시간가속 — 궤도를 도는 위성                (~60초)
#    막5  정면에서 본 고리                           (~22초)
#    막6  마무리                                     (~10초)
#
#  ⚠️ 자막 홀드는 `say()` 가 글자 수로 자동 계산한다(2초 + 글자당 0.1초).
#     숫자를 직접 박지 말 것 — 6~7초씩 붙잡으면 "인터벌이 길다"는 소리를 듣는다(실측 피드백).
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
UR = Planet(Planet.PlanetName.Uranus)

MOONS = ["Miranda", "Ariel", "Umbriel", "Titania", "Oberon"]

R_SYSTEM = 15.0        # 위성계 조망 (오베론 궤도 11.4 단위 + 여유)
R_RINGS = 3.2          # 고리 근접 (실측 확정값)
L_EDGE = 0.0           # 세로 — 고리면을 옆에서
L_FACE = 90.0          # 과녁 — 고리면을 정면에서

txt = None
ep = None


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 **글자 수로 자동 계산**(2초 + 글자당 0.1초).

    ⚠️ [2026-08-10 돔 피드백 "왜 이렇게 인터벌이 긴거야?"] 내가 쓰던 6~7.5초 홀드는
       두 배쯤 과했다. 한글 20자면 4초면 읽고도 여유가 있고, 그 이상 붙잡으면
       화면이 멈춘 것처럼 보인다. `hold=0` 은 기다리지 않음."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        sleep(hold)


def wait_settle(max_s=16.0):
    """FadeTo 도킹 애니가 카메라를 놓을 때까지 기다린다(암전 클램프 겸용).
       ⚠️ 이게 없으면 뒤따르는 setPositionLBR(Anim 0) 이 씹혀 엉뚱한 구도에서 화면이 켜진다(실측)."""
    prev = None
    stable = 0
    t = 0.0
    while t < max_s:
        uni.setGlobalIntensity(0.0, Anim(0.0))      # 클램프 — 한 번만 걸면 FadeTo 가 1.0 으로 되돌린다
        cur = None
        try:
            cur = cam.positionLBR.z
        except Exception:
            pass
        if cur is not None and prev is not None and abs(cur - prev) < 1e-4 * max(1.0, abs(cur)):
            stable += 1
            if stable >= 4:                          # 1초간 변화 없음 = 도킹 끝
                break
        else:
            stable = 0
        prev = cur
        sleep(0.25)
        t += 0.25
    print("도킹 안정화 완료, R =", prev)


def frame(L, B, R, anim=None):
    """황도 프레임 안에서만 움직인다 — 읽기·쓰기·재조준 프레임을 절대 섞지 않는다."""
    a = anim if anim else Anim(0.0)
    cam.setPositionLBR(Vec(L, B, R), a, ep)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), a, ep)


# ── 막0 : 지상에서 ────────────────────────────────────────────
try:
    SceneGraph().reset(1)
    for _ in range(7): uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(0.2)
    uni.setGlobalIntensity(0.0, Anim(0.0))

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))
    earth.setTerrainIntensity(0.0, Anim(0.0))
    earth.setElevationScale(0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))

    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))   # 청주 밤 22시 = 13 UTC
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.4)

    cam.setOrientationH(0.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0))

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setSize(0.052)
    txt.setColor(Vec(1.0, 1.0, 0.55))
    txt.setDistance(1.0, Anim(0.0))
    txt.setText("태양계에서 혼자만 '누워서' 도는 행성이 있다")
    txt.setIntensity(1.0, Anim(1.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(5.5)
    say("다른 행성들은 팽이처럼 선 채로 돈다")
    say("천왕성만 옆으로 쓰러진 채 돈다 — 자전축 98도")
    say("가서 확인해 보자")
except Exception as e:
    print("막0 오류:", e)

# ── 막1 : 접근 (황도 프레임 · L=0 · B=0) ──────────────────────
try:
    txt.setIntensity(0.0, Anim(1.0)); sleep(1.2)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.6)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    wait_settle()                                   # ★ 도킹이 끝난 뒤에 구도를 꽂는다

    # 밝기 = A/B 채택값. 올려도 고리 대비는 안 늘고 원반만 탄다.
    UR.setIntensity(1.2, Anim(0.0))
    UR.setShadowStrength(0.0, Anim(0.0))
    UR.setShadowContrast(0.0, Anim(0.0))
    UR.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # ★ 황도 프레임 + L=0 + B=0 — 이 셋이 다 맞아야 '세로'가 나온다
    ep = UR.portId(Planet.PlanetPort.Ecliptic)
    frame(L_EDGE, 0.0, R_SYSTEM)
    cam.setTargetHeight(30.0, Anim(0.0))

    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))   # 위성 켜기 전에 날짜 고정
    sleep(1.0)

    txt.setDistance(20.0, Anim(0.0))                # 행성 프레임 자막
    say("천왕성")
    txt.setIntensity(1.0, Anim(1.5))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.5)
except Exception as e:
    print("막1 오류:", e)

# ── 막2 : 세로로 선 궤도 ──────────────────────────────────────
try:
    say("다섯 개의 큰 위성이 있다")

    for nm in MOONS:
        try:
            s = Satellite(getattr(Satellite.SatelliteName, nm))
            s.setIntensity(1.0, Anim(1.5))
            s.setOrbitIntensity(1.0, Anim(1.5))     # ★ 궤도선이 '누운 자세'의 증거
            s.setLabelIntensity(1.0, Anim(1.5))
            s.setScale(14.0, Anim(1.5))
        except Exception as ex:
            print("   위성 실패", nm, ex)
    sleep(3.5)

    say("궤도가 '세로'로 서 있다")
    say("다른 행성이라면 이 각도에서 옆으로 누워 보인다")
    say("행성이 쓰러졌으니 위성도 함께 쓰러진 채 돈다")
    say("미란다 · 아리엘 · 움브리엘 · 티타니아 · 오베론")
except Exception as e:
    print("막2 오류:", e)

# ── 막3 : 0→90° 열기 (세로 → 과녁) ───────────────────────────
#   ⚠️ 포트 프레임 공전이므로 재조준 필수(track=-1 공전과 다르다).
try:
    say("천천히 돌아서 정면으로 가 보자")
    L = L_EDGE
    step = 0
    while L <= L_FACE:
        cam.setPositionLBR(Vec(L, 0.0, R_SYSTEM), Anim(0.9), ep)
        step += 1
        if step % 3 == 0:
            # ⚠️ 재조준은 '겹쳐서' 건다 — 뒤에 sleep 을 붙이면 그 순간 화면이 멈춘다(demo2 v1 실패 원인).
            cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.9), ep)
        sleep(0.6)                              # ★ sleep < anim = 겹쳐서 매끄럽게
        L += 4.5
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.8), ep)
    sleep(1.0)
    say("세로로 서 있던 궤도가 과녁처럼 열린다")
except Exception as e:
    print("막3 오류:", e)

# ── 막4 : 시간가속 ────────────────────────────────────────────
try:
    # ⚠️ [2026-08-10 "인터벌이 길다"] 20초 간격은 한 줄 읽고 15초가 빈다.
    #    자막은 읽는 시간 + 여백 4초 ≈ 9초 간격으로, 문장은 짧게 쪼갠다.
    say("14일을 1분으로 압축한다", 0)
    dm.setDateTime(2026, 10, 29, 13, 0, 0, tz, Anim(60.0))
    sleep(4.0)
    say("안쪽 미란다 — 1.4일에 한 바퀴")
    sleep(4.5)
    say("가장 안쪽이라 가장 빠르다")
    sleep(4.5)
    say("아리엘 2.5일, 움브리엘 4.1일")
    sleep(4.5)
    say("티타니아 8.7일")
    sleep(4.5)
    say("바깥 오베론은 13.5일")
    sleep(4.5)
    say("멀수록 느리다 — 케플러 법칙")
    sleep(4.0)
except Exception as e:
    print("막4 오류:", e)

# ── 막5 : 정면에서 본 고리 ────────────────────────────────────
#   ⚠️ 고리가 보이는 건 오직 이 구도(L=90 정면) 덕이다. 밝기를 올리지 마라 — 원반만 탄다.
try:
    say("이 행성에도 고리가 있다")
    cam.setPositionR(R_RINGS, Anim.cubic(6.0), ep)
    sleep(6.5)
    say("정면으로 마주 봐야 비로소 보인다 — 동심원 여러 겹")
    say("숯처럼 검은 얼음과 바위, 반사율 3%")
except Exception as e:
    print("막5 오류:", e)

# ── 막6 : 마무리 ──────────────────────────────────────────────
try:
    cam.setPositionR(R_SYSTEM, Anim.cubic(5.0), ep)
    sleep(5.5)
    say("누운 채로 도는 행성, 함께 누운 다섯 위성")
    txt.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("막6 오류:", e)

print("쇼 종료 — 누워서 도는 행성 (천왕성) v3")

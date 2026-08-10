# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  "누워서 도는 행성 — 천왕성"   (약 3분)
#
#  ★ 왜 이 소재인가 = 우리가 아직 안 해본 조합이다.
#    · 위성계 쇼는 목성(갈릴레이 4)·토성(7)까지 했지만 **천왕성 5위성은 미개척**.
#    · 천왕성 고리는 2026-07-30 에 '승격 확정'(B38+R3.2+intensity1.5)됐지만
#      **위성과 묶은 쇼로는 한 번도 안 만들었다.**
#    · 결정적으로 화면이 다르다 — 천왕성은 자전축이 98° 누워 있어
#      **고리도 위성 궤도도 '세로'로 돈다.** 목성·토성의 가로 배치와 한눈에 대비된다.
#
#  구성
#    막0  지상에서 — "맨눈으로 볼 수 있는 마지막 행성"        (~25초)
#    막1  접근 (암전 클램프 속에서 전부 정렬)                  (~15초)
#    막2  세로로 선 고리                                       (~35초)
#    막3  풀백 → 다섯 위성                                     (~30초)
#    막4  시간가속 — 세로로 도는 궤도                          (~78초)
#    막5  마무리                                               (~10초)
#
#  적용한 확정 규칙
#    · FadeTo 로 쇼를 시작하지 않는다(지상 인트로 먼저) — 안 그러면 오프닝이 검은 화면
#    · 암전은 '한 번'이 아니라 **클램프 루프** — FadeTo 가 밝기를 1.0 으로 되돌린다
#    · 위성 공전을 보려면 **관성 프레임(EquatorialJ2000)** 전환 필수(동기 프레임이면 하늘이 돈다)
#    · 시작 날짜(instant)는 **위성을 켜기 전** 암전 중에 고정(안 그러면 위성이 순간이동)
#    · 지상 자막 distance 1.0 / 행성 프레임 자막 distance 20
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone

URANUS = Planet(Planet.PlanetName.Uranus)
MOONS = [                                  # 천왕성 위성은 이 5개가 전부다
    ("Miranda",  "미란다",   1.41),
    ("Ariel",    "아리엘",   2.52),
    ("Umbriel",  "움브리엘", 4.14),
    ("Titania",  "티타니아", 8.71),
    ("Oberon",   "오베론",  13.46),
]

txt = None


def say(s, hold=0.0):
    if txt:
        txt.setText(s)
        if hold:
            sleep(hold)


def clamp_dark(seconds):
    """⚠️ FadeTo/reset 은 GlobalIntensity 를 1.0 으로 되돌린다.
       한 번 거는 걸론 안 되고 계속 찍어 눌러야 슬루가 안 보인다."""
    for _ in range(int(seconds / 0.2)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)


# ── 막0 : 지상에서 ────────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))     # 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))        # 지면 OFF (둘은 항상 세트)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))

    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))   # 청주 밤 22시 = 13 UTC
    sleep(0.4)

    cam.setOrientationH(0.0, Anim(0.0))               # 남쪽
    cam.setTargetHeight(30.0, Anim(0.0))

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setSize(0.052)                                # 지상 자막 표준
    txt.setColor(Vec(1.0, 1.0, 0.55))
    txt.setDistance(1.0, Anim(0.0))
    txt.setText("맨눈으로 볼 수 있는 마지막 행성")
    txt.setIntensity(1.0, Anim(1.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(5.5)
    say("6등급 — 아주 어두운 밤에, 아주 좋은 눈으로만", 6.0)
    say("1781년까지 아무도 '행성'인 줄 몰랐던 천왕성", 6.5)
    say("망원경으로 발견된 최초의 행성 — 가서 보자", 6.0)
except Exception as e:
    print("막0 오류:", e)

# ── 막1 : 접근 (전부 암전 속에서) ─────────────────────────────
try:
    txt.setIntensity(0.0, Anim(1.0)); sleep(1.2)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.6)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    clamp_dark(6.0)                                   # ★ 도착 + 내부 방향정렬 슬루가 끝날 때까지

    # 표면·고리를 보려면 그림자 OFF 3세터
    URANUS.setShadowStrength(0.0, Anim(0.0))
    URANUS.setShadowContrast(0.0, Anim(0.0))
    URANUS.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # 배경 검정 = 고리 대비

    # ★ 관성 프레임 — 이걸 빼면 위성이 도는 게 아니라 하늘이 돈다
    ip = URANUS.portId(Planet.PlanetPort.EquatorialJ2000)
    p = cam.positionLBR
    # 고리면 개방 B=38 + 근접 R=3.2 (2026-07-30 승격 확정 구도)
    cam.setPositionLBR(Vec(p.x, 38.0, 3.2), Anim(0.0), ip)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
    cam.setTargetHeight(30.0, Anim(0.0))
    URANUS.setIntensity(1.0, Anim(0.0))

    # ⚠️ 시작 날짜는 '위성을 켜기 전' 암전 중에 고정 — 안 그러면 위성이 궤도상 순간이동
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))
    sleep(1.0)

    txt.setDistance(20.0, Anim(0.0))                  # 행성 프레임 자막 표준
    txt.setSize(0.052)
    say("천왕성")
    txt.setIntensity(1.0, Anim(1.5))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))      # 정렬이 다 끝난 뒤에야 페이드인
    sleep(3.0)
except Exception as e:
    print("막1 오류:", e)

# ── 막2 : 세로로 선 고리 ──────────────────────────────────────
try:
    say("고리가 '세로'로 서 있다", 6.0)
    say("자전축이 98도 — 누운 채로 태양을 도는 행성이다", 7.0)

    # 고리는 본체 intensity 에 묶여 있다 — 1.0 → 1.5 A/B 로 또렷해지는 걸 보여준다
    say("본체를 조금 밝히면 고리가 드러난다")
    URANUS.setIntensity(1.5, Anim(3.0))               # 1.8 이상은 원반이 타서 금지
    sleep(5.0)
    say("얼음과 숯빛 암석 — 실제 반사율 3%의 어두운 고리", 8.0)
    say("13개의 고리가 있지만, 대부분은 이렇게 가늘다", 7.0)
    say("1977년, 별을 가리는 순간에 우연히 발견됐다", 7.0)
    sleep(3.0)
except Exception as e:
    print("막2 오류:", e)

# ── 막3 : 풀백 → 다섯 위성 ────────────────────────────────────
try:
    say("이 행성에는 다섯 개의 큰 위성이 있다")
    # 풀백은 '보여줄 움직임' — 암전하지 않는다.
    # 오베론 궤도가 22.8 천왕성반지름이라 R 은 그보다 넉넉히.
    cam.setPositionR(28.0, Anim.cubic(6.0), ip)
    sleep(6.5)

    for eng, kor, period in MOONS:
        try:
            s = Satellite(getattr(Satellite.SatelliteName, eng))
            s.setIntensity(1.0, Anim(1.0))
            s.setOrbitIntensity(0.75, Anim(1.0))      # 궤도선
            s.setLabelIntensity(1.0, Anim(1.0))       # 이름표
            s.setScale(9.0, Anim(1.0))                # 멀리서도 보이게
        except Exception as ex:
            print("   위성 실패", eng, ex)
    sleep(2.0)

    say("미란다 · 아리엘 · 움브리엘 · 티타니아 · 오베론", 7.0)
    say("셰익스피어와 포프의 등장인물에서 이름을 따왔다", 6.5)
except Exception as e:
    print("막3 오류:", e)

# ── 막4 : 시간가속 — 세로로 도는 궤도 ─────────────────────────
try:
    say("14일을 1분으로 — 궤도가 '세로'로 돈다")
    dm.setDateTime(2026, 10, 29, 13, 0, 0, tz, Anim(78.0))    # +14일을 78초에
    sleep(26.0)
    say("안쪽 미란다는 1.4일에 한 바퀴")
    sleep(26.0)
    say("바깥 오베론은 13.5일 — 멀수록 느리다 (케플러)")
    sleep(26.0)
except Exception as e:
    print("막4 오류:", e)

# ── 막5 : 마무리 ──────────────────────────────────────────────
try:
    say("누워서 도는 행성, 그리고 함께 누운 다섯 위성", 6.0)
    say("태양계에서 이렇게 도는 행성은 여기 하나뿐이다", 6.5)
    txt.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
    URANUS.setIntensity(1.0, Anim(2.0))               # 원래 밝기로 복귀
    sleep(2.0)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 누워서 도는 행성 (천왕성)")

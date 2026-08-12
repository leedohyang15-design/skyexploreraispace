# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인 (2026-08-10) — 관성 프레임 전환·위성 표시·풀백 R=40(HUD 2.86Gm) 돔 확인, 네 궤도 다 잡힘. ⚠️ 자막 템포가 길다는 지적으로 홀드 자동계산 + 가속 60초로 재조정 → 그 수정본은 미확인
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "갈릴레이의 밤 — 목성과 네 위성"   (약 2분 20초)
#
#  1610년 겨울, 갈릴레이가 자작 망원경으로 목성 곁의 별 네 개를 봤다.
#  며칠 지켜보니 그 별들이 목성을 '돌고' 있었다 — 모든 것이 지구를 도는 게 아니라는 첫 증거.
#  이 쇼는 그 관측을 시간가속으로 며칠치 압축해 보여준다.
#
#  ⚠️ 이 쇼에 반영한 것 (2026-08-10 천왕성 건에서 배운 것 + 이전 목성 시안 피드백)
#    ① **시간가속을 늦췄다.** 이전 시안은 같은 구간을 ~30초에 돌려 "너무 빠르다"는 지적을 받았다.
#       칼리스토 공전이 16.7일이므로 **17일을 60초**에 흘려 바깥 위성도 한 바퀴가 눈에 잡히게 한다.
#    ② **막마다 try/except.** 이전 시안은 통짜 try 하나라 한 줄이 죽으면 뒤가 통째로 날아갔다.
#    ③ **도킹은 고정 sleep 이 아니라 폴링으로 기다린다.** 도킹 애니가 R 을 계속 끌어당기는데
#       그때 `cam.positionLBR` 을 읽으면 수렴 중인 먼 값이 고정돼 목성이 작게 잡힌다(천왕성 실측).
#    ④ **FadeTo 로 쇼를 열지 않는다.** 클램프 암전이 그대로 '검은 오프닝'이 되므로 지상 인트로를 먼저 둔다.
#
#  ⚠️ 프레임 주의
#    · 도킹(EquatorialSynchronous)은 카메라가 목성 자전을 따라 돈다 → 위성이 아니라 하늘이 도는 것처럼 보인다.
#      **관성 프레임(EquatorialJ2000)으로 전환**해야 위성 공전이 깔끔하다.
#    · 전환은 **같은 L/B/R 로** 넘기면 카메라가 안 움직인다(둘 다 적도계라 R 단위가 같다).
#      ⚠️ 황도 포트(Ecliptic)는 R 단위가 '지름'이라 다르다 — 거기로는 이 값을 그대로 넘기지 말 것.
#
#  구성
#    막0  지상에서 — 1610년의 그 별                (~21초)
#    막1  접근 — 목성 곁으로                       (~14초)
#    막2  네 개의 위성 (풀백으로 궤도 공개)        (~30초)
#    막3  시간가속 — 17일을 60초로                 (~60초)
#    막4  마무리                                   (~11초)
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
JU = Planet(Planet.PlanetName.Jupiter)

# 갈릴레이 위성 — 궤도 반지름(목성반지름 단위)과 공전주기(일)
#   이오 5.9 / 1.77d · 유로파 9.4 / 3.55d · 가니메데 15.0 / 7.15d · 칼리스토 26.3 / 16.7d
GALILEAN = ["Io", "Europa", "Ganymede", "Callisto"]
PULLBACK = 8.0          # 도킹 R(≈5 목성반지름) × 8 = 40 → 칼리스토 26.3 이 여유 있게 담긴다
ACCEL_DAYS = 17         # 칼리스토 1주기(16.7일)보다 살짝 길게
ACCEL_SEC = 60.0        # 30초(너무 빠름) → 80초(느려서 빔) → 60초. 칼리스토 1주기 = 60초

txt = None
ip = None
base_r = None          # 막1에서 잰 도킹 R — 막2의 풀백이 이걸 기준으로 삼는다


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 **글자 수로 자동 계산**한다.

    ⚠️⚠️ [2026-08-10 돔 피드백 "왜 이렇게 인터벌이 긴거야?"]
      내가 쓰던 6.5~7.5초 홀드는 **두 배쯤 과했다.** 한글 자막은
      대략 `2초 + 글자당 0.1초`면 읽고도 여유가 있다(20자 ≈ 4초).
      자막을 오래 붙잡으면 화면이 멈춘 것처럼 보인다 — 특히 배경이
      거의 안 변하는 우주 장면에서는 그대로 '죽은 시간'이 된다.
      `hold=0` 은 '기다리지 않음'(다음 줄이 바로 이어짐)."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        sleep(hold)


def wait_dock(max_s=18.0):
    """도킹 애니가 카메라를 놓을 때까지 대기(암전 클램프 겸용).
       ⚠️ 고정 sleep 금지 — 천왕성 실측에서 6초 뒤에도 R 이 653,188 → 163,773 km 로 수렴 중이었다."""
    prev, stable, t = None, 0, 0.0
    while t < max_s:
        uni.setGlobalIntensity(0.0, Anim(0.0))      # 한 번만 걸면 FadeTo 가 1.0 으로 되돌린다
        cur = None
        try:
            cur = cam.positionLBR.z
        except Exception:
            pass
        if cur is not None and prev is not None and abs(cur - prev) < 1e-4 * max(1.0, abs(cur)):
            stable += 1
            if stable >= 4:
                break
        else:
            stable = 0
        prev = cur
        sleep(0.25)
        t += 0.25
    print("도킹 안정화, R =", prev)
    return prev


# ── 막0 : 지상에서 — 1610년의 그 별 ──────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))     # 지상 하늘 쇼 = 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))        #                + 지면 OFF
    earth.setElevationScale(0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))

    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 3, 20, 13, 0, 0, tz, Anim(0.0))    # 청주 밤 22시 = 13 UTC
    sleep(0.4)

    cam.setOrientationH(0.0, Anim(0.0))              # 남쪽
    cam.setTargetHeight(30.0, Anim(0.0))

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setSize(0.052)
    txt.setColor(Vec(1.0, 1.0, 0.55))
    txt.setDistance(1.0, Anim(0.0))                  # 지상 자막 = distance 1.0
    txt.setText("1610년 겨울, 파도바")
    txt.setIntensity(1.0, Anim(1.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
    say("갈릴레이가 자기가 만든 망원경을 목성에 겨눴다")
    say("목성 옆에 작은 별 네 개가 나란히 있었다")
    say("며칠 뒤 다시 보니 — 자리가 바뀌어 있었다")
    say("그 별들은 목성을 돌고 있었다")
except Exception as e:
    print("막0 오류:", e)

# ── 막1 : 접근 ────────────────────────────────────────────────
try:
    txt.setIntensity(0.0, Anim(1.0)); sleep(1.2)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.6)

    DataManager.database().data(Data.Type.PlanetType, "Jupiter").action(Action.Type.FadeTo).trigger()
    dock_r = wait_dock()                             # ★ 폴링 — 이 값이 도킹 R(≈5)

    # 클로즈업 표준: 그림자 OFF (터미네이터로 반쪽이 어두워지면 줄무늬가 반만 보인다)
    JU.setShadowStrength(0.0, Anim(0.0))
    JU.setShadowContrast(0.0, Anim(0.0))
    JU.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))

    # 관성 프레임으로 — 같은 L/B/R 이라 카메라는 안 움직이고 '기준'만 바뀐다
    # ⚠️⚠️ [2026-08-10 실측 버그] 여기서 풀백을 '먼저' 걸고 곧바로 positionLBR 을 읽어 프레임에
    #   넘겼더니, 읽은 값이 아직 풀백 전(도킹 R=5)이라 **풀백이 자기 자신에게 덮어씌워졌다**
    #   (HUD 357,460km = 5.0 목성반지름으로 확인). setPositionLBR 은 Anim(0.0) 이어도 즉시 반영이
    #   아니다 → **'쓰고 바로 읽기'를 하지 마라.** 순서를 뒤집어 프레임부터 잡고, 풀백은 막2에서
    #   눈에 보이게 한다(연출적으로도 이쪽이 낫다 — 목성이 작아지며 궤도가 드러난다).
    p = cam.positionLBR
    base_r = dock_r if dock_r else p.z
    ip = JU.portId(Planet.PlanetPort.EquatorialJ2000)
    cam.setPositionLBR(Vec(p.x, p.y, base_r), Anim(0.0), ip)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.8)
    print("프레임 전환 후 R =", cam.positionLBR.z, "(도킹 R =", base_r, ")")

    dm.setDateTime(2026, 3, 20, 13, 0, 0, tz, Anim(0.0))   # 위성 켜기 전에 날짜 고정
    sleep(0.8)

    txt.setDistance(20.0, Anim(0.0))                 # 행성 프레임 자막 = distance 20
    say("목성")
    txt.setIntensity(1.0, Anim(1.5))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.5)
except Exception as e:
    print("막1 오류:", e)

# ── 막2 : 네 개의 위성 ────────────────────────────────────────
try:
    say("갈릴레이가 본 네 개")

    for nm in GALILEAN:
        try:
            s = Satellite(getattr(Satellite.SatelliteName, nm))
            s.setIntensity(1.0, Anim(1.5))
            s.setOrbitIntensity(0.9, Anim(1.5))
            s.setLabelIntensity(1.0, Anim(1.5))
            s.setScale(8.0, Anim(1.5))               # 멀리서도 점이 보이게
        except Exception as ex:
            print("   위성 실패", nm, ex)
    sleep(2.0)

    say("이오 · 유로파 · 가니메데 · 칼리스토")

    # ★ 풀백을 '보이게' 한다 — 목성이 작아지며 바깥 두 위성의 궤도가 화면에 들어온다.
    #   ⚠️ 절대값으로 지정한다(읽어서 곱하지 않는다). 읽기는 아직 반영 안 된 값을 줄 수 있다.
    #      칼리스토 궤도가 26.3 목성반지름이라 R=40 은 돼야 담긴다 —
    #      도킹 R=5 그대로 두면 이오·유로파만 보이고 나머지는 화면 밖이다(실측).
    say("네 개가 다 들어오게 뒤로 물러나 보자")
    cam.setPositionR((base_r or 5.0) * PULLBACK, Anim.cubic(7.0), ip)   # 막1이 죽어도 도킹 기본값으로
    sleep(7.5)
    print("풀백 후 R =", cam.positionLBR.z)          # ⚠️ HUD(km) 와 대조 — 40 목성반지름이어야 한다

    say("맨눈으로는 절대 안 보인다 — 망원경이 있어야 보인다")
    say("이것이 지동설의 첫 증거가 되었다")
except Exception as e:
    print("막2 오류:", e)

# ── 막3 : 시간가속 ────────────────────────────────────────────
#   ⚠️ 이 막이 쇼의 본론이다.
#   ⚠️⚠️ [2026-08-10 "인터벌이 길다"] 이전 판은 60초 가속에 자막을 20초 간격으로 넣었다.
#     한 줄 읽고 나면 **15초씩 빈 화면**이 남는다 — 위성이 도는 게 보이긴 해도 '멈춘 것 같다'.
#     → 자막은 **읽는 시간(약 4~5초) + 여백 4초 ≈ 9초 간격**으로 촘촘히, 대신 문장을 짧게 쪼갠다.
#     가속 자체도 80 → 60초. (칼리스토 1주기가 60초 = 이오는 8초에 한 바퀴 = 충분히 보인다.)
try:
    say("17일을 1분으로 압축한다", 0)
    dm.setDateTime(2026, 4, 6, 13, 0, 0, tz, Anim(ACCEL_SEC))
    sleep(4.0)
    say("갈릴레이가 며칠에 걸쳐 본 것을")
    sleep(4.0)
    say("안쪽 이오 — 1.8일에 한 바퀴")
    sleep(4.5)
    say("눈에 띄게 빠르다")
    sleep(4.5)
    say("유로파 3.6일, 가니메데 7.2일")
    sleep(4.5)
    say("바깥 칼리스토는 16.7일")
    sleep(4.5)
    say("느릿하게 딱 한 바퀴")
    sleep(4.5)
    say("멀수록 느리다")
    sleep(4.0)
    say("케플러가 나중에 법칙으로 정리한다")
    sleep(3.0)
except Exception as e:
    print("막3 오류:", e)

# ── 막4 : 마무리 ──────────────────────────────────────────────
try:
    say("작은 망원경 하나가 세계관을 바꿨다")
    say("목성과 네 위성 — 하늘에 있는 또 하나의 태양계")
    txt.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("막4 오류:", e)

print("쇼 종료 — 갈릴레이의 밤 (목성과 네 위성)")

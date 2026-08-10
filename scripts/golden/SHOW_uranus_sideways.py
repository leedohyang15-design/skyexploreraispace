# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  "누워서 도는 행성 — 천왕성"   v2   (약 2분 50초)
#
#  ⚠️ v1 에서 배운 것 (2026-08-10 사용자 돔 실측 + 스샷 4장)
#    ① **고리는 주인공이 될 수 없다.** 반사율 3% 라 원래 어둡고, 밝히려면 본체
#       `setIntensity` 를 올려야 하는데(고리 전용 세터 없음) 1.5 면 **원반이 새하얗게 타서
#       눈이 아프다**. 고리는 살짝 보일 뿐인데 화면은 눈부신, 최악의 교환이었다.
#    ② **진짜 주인공은 위성 궤도선이었다.** 스샷에서 노란 궤도선은 아주 밝고 뚜렷했고,
#       '누워 있다'는 이야기를 고리보다 훨씬 잘 전달했다.
#    ③ **프레임을 바꿔야 기울기가 보인다.** FadeTo 도킹(EquatorialSynchronous)·EquatorialJ2000 은
#       천왕성 자신의 적도가 기준이라 98° 기울기를 흡수해 고리가 늘 '가로'로 눕는다.
#       → **`Planet.PlanetPort.Ecliptic`(황도 프레임)** 이어야 기울어진 모습이 드러난다.
#
#  → v2 설계: **궤도선이 주인공, 고리는 곁들이. 원반은 어둡게(그림자 ON) 눈부심 제거.**
#     그림자 OFF 3세터는 '표면을 다 보여줄 때' 규칙이지, 여기선 오히려 해가 된다.
#
#  구성
#    막0  지상에서                                   (~24초)
#    막1  접근 — 황도 프레임 + 눈 안 아픈 밝기        (~14초)
#    막2  다섯 위성과 기울어진 궤도                   (~40초)
#    막3  시간가속 — 궤도를 따라 도는 위성            (~78초)
#    막4  고리 한 번 (곁들이)                         (~20초)
#    막5  마무리                                      (~14초)
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
txt = None
ep = None


def say(s, hold=0.0):
    if txt:
        txt.setText(s)
        if hold:
            sleep(hold)


def clamp_dark(seconds):
    """FadeTo 는 GlobalIntensity 를 1.0 으로 되돌린다 — 계속 눌러야 슬루가 안 보인다."""
    for _ in range(int(seconds / 0.2)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)


def gentle_planet():
    """밝기 = 2026-08-10 사용자 A/B 채택값(4조합 중 2번).
       ⚠️ 내가 먼저 제안한 '그림자 ON 으로 밤면 죽이기'(3·4번)는 **탈락**했다 —
          반쪽이 어두워지는 대신 볼 게 줄어 오히려 나빴다. 그림자는 끈 채로 둔다.
       ⚠️ intensity 1.5 는 원반이 탄다. 1.2 가 눈이 편한 상한."""
    UR.setIntensity(1.2, Anim(1.5))
    UR.setShadowStrength(0.0, Anim(1.5))
    UR.setShadowContrast(0.0, Anim(1.5))
    UR.setPlanetShineStrength(1.0, Anim(1.5))


# ── 막0 : 지상에서 ────────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))
    earth.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))

    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))   # 청주 밤 22시 = 13 UTC
    sleep(0.4)

    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))

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
    say("다른 행성들은 팽이처럼 선 채로 돈다", 6.0)
    say("천왕성만 옆으로 쓰러진 채 돈다 — 자전축 98도", 6.5)
    say("가서 확인해 보자", 4.5)
except Exception as e:
    print("막0 오류:", e)

# ── 막1 : 접근 (황도 프레임 + 눈 안 아픈 밝기) ────────────────
try:
    txt.setIntensity(0.0, Anim(1.0)); sleep(1.2)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.6)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    clamp_dark(6.0)

    gentle_planet()                                   # 원반 어둡게 = 눈부심 제거
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # ★ 황도 프레임 — 이걸 써야 '누운 자세'가 드러난다(적도 프레임은 기울기를 흡수)
    ep = UR.portId(Planet.PlanetPort.Ecliptic)
    p = cam.positionLBR
    # 위성 궤도가 주인공이므로 처음부터 넉넉히 뒤로 (오베론 궤도 22.8 천왕성반지름)
    cam.setPositionLBR(Vec(p.x, 38.0, 28.0), Anim(0.0), ep)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ep)
    cam.setTargetHeight(30.0, Anim(0.0))

    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))   # 위성 켜기 전에 날짜 고정
    sleep(1.0)

    txt.setDistance(20.0, Anim(0.0))                  # 행성 프레임 자막
    say("천왕성")
    txt.setIntensity(1.0, Anim(1.5))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.0)
except Exception as e:
    print("막1 오류:", e)

# ── 막2 : 다섯 위성과 기울어진 궤도 (주인공) ──────────────────
try:
    say("다섯 개의 큰 위성이 있다", 3.5)

    for nm in MOONS:
        try:
            s = Satellite(getattr(Satellite.SatelliteName, nm))
            s.setIntensity(1.0, Anim(1.5))
            s.setOrbitIntensity(1.0, Anim(1.5))       # ★ 궤도선이 이 쇼의 주인공 — 최대로
            s.setLabelIntensity(1.0, Anim(1.5))
            s.setScale(14.0, Anim(1.5))               # 멀리서도 점이 보이게
        except Exception as ex:
            print("   위성 실패", nm, ex)
    sleep(3.0)

    say("미란다 · 아리엘 · 움브리엘 · 티타니아 · 오베론", 7.0)
    say("궤도가 '기울어' 있다 — 다른 행성계와 다르다", 7.5)
    say("행성이 누웠으니, 위성도 함께 누운 채로 돈다", 7.5)
    say("셰익스피어와 포프의 등장인물에서 이름을 땄다", 6.5)
except Exception as e:
    print("막2 오류:", e)

# ── 막3 : 시간가속 ────────────────────────────────────────────
try:
    say("14일을 1분으로 — 궤도를 따라가 보자")
    dm.setDateTime(2026, 10, 29, 13, 0, 0, tz, Anim(78.0))
    sleep(26.0)
    say("안쪽 미란다는 1.4일에 한 바퀴")
    sleep(26.0)
    say("바깥 오베론은 13.5일 — 멀수록 느리다 (케플러)")
    sleep(26.0)
except Exception as e:
    print("막3 오류:", e)

# ── 막4 : 고리 한 번 (곁들이) ─────────────────────────────────
#   ⚠️ 고리는 어둡다. 오래 붙잡지 말고 '있다'만 보여주고 넘어간다.
try:
    say("이 행성에도 고리가 있다 — 아주 어둡지만")
    cam.setPositionR(3.2, Anim.cubic(5.0), ep)        # 확정 근접값(절대값으로 지정)
    sleep(5.5)
    # ⚠️ 여기서 intensity 를 올리지 않는다. 원반만 타고 고리 대비는 안 늘기 때문
    #    (사용자 관찰 — 4조합에서 고리 밝기 자체는 다 같아 보였다).
    #    고리를 보이게 하는 건 밝기가 아니라 구도(B=38 고리면 개방 + R=3.2 근접)다.
    say("숯처럼 검은 얼음과 바위, 반사율 3%", 7.0)
    sleep(2.5)
except Exception as e:
    print("막4 오류:", e)

# ── 막5 : 마무리 ──────────────────────────────────────────────
try:
    cam.setPositionR(28.0, Anim.cubic(5.0), ep)       # 다시 위성계 조망으로
    sleep(5.5)
    say("누운 채로 도는 행성, 함께 누운 다섯 위성", 6.0)
    txt.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("막5 오류:", e)

print("쇼 종료 — 누워서 도는 행성 (천왕성) v2")

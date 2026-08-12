# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 검증된 레시피(scripts/study/meteor_shower.py, 사용자 확인)를 기반으로 짰으나
#        이 쇼 자체는 돔에서 본 기록이 없다. 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "오늘 밤, 페르세우스"  (약 2분 20초)
#
#  ★ 2026년 8월 12~13일 = 페르세우스 유성우 극대. **오늘 밤 바로 쓸 수 있는 쇼.**
#  ★ 올해 조건이 유난히 좋다: 극대일 달 조도 **2%(거의 삭)** — 달빛 방해가 사실상 없다.
#    (유성우는 달이 최대 변수다. 보름과 겹치면 밝은 유성 몇 개만 남는다.)
#
#  검증된 레시피(scripts/study/meteor_shower.py, 사용자 확인)를 골든 쇼로 다듬은 것.
#    · `setReferential(RaDec)` + `setRainGradientPoint(Vec2(적경47, 적위58))`
#      = 복사점을 **진짜 페르세우스자리에 하늘 고정** → 유성이 그 한 점에서 방사된다.
#    · ⚠️ **ZHR 내부 저장 = ZHR/60(분당 개수)** — 실제값 100 을 넣으면 돔에서 거의 안 보인다.
#      볼만한 쇼 = **800~1500**, 폭풍 연출 = 3000. (실측 확정)
#    · `setRainSeed(1)` = 재생 / `0` = 정지.
#
#  ⚠️ 오늘 배운 규칙 반영
#    · 자막 홀드는 `say()` 가 글자 수로 자동 계산(2초 + 글자당 0.1초). 숫자를 직접 박지 않는다.
#    · 지상 하늘 쇼 = 대기 OFF **+ 지면 OFF**.
#    · 지상 Sky View 에서는 **위치 명령 금지** — 조준은 `setOrientationH` + `setTargetHeight` 두 줄뿐.
#    · 시각은 UTC. **청주 8/13 새벽 2시 = 8/12 17:00 UTC** (UTC = KST − 9h).
#
#  구성
#    막0  해가 지고                                  (~26초)
#    막1  복사점 — 페르세우스자리                     (~28초)
#    막2  유성우 시작                                 (~40초)
#    막3  극대 — 쏟아진다                             (~30초)
#    막4  마무리                                      (~16초)
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

# 페르세우스 복사점 (적경 47°, 적위 58°) — 실측 확정값
RADIANT_RA, RADIANT_DEC = 47.0, 58.0
# 북동 하늘. ⚠️ 환산은 H = 180 − 나침반방위 → 북동(45°) = H 135
H_NORTHEAST = 135.0
TILT = 22.0            # 복사점이 이 시각 저~중고도 → 틸트를 낮춰 잡는다

txt = None
ss = None


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 글자 수로 자동 계산(2초 + 글자당 0.1초)."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        sleep(hold)


def pick(cls, *names):
    """enum 멤버 이름이 빌드마다 다를 수 있어 있는 것을 골라 쓴다."""
    for n in names:
        if hasattr(cls, n):
            return getattr(cls, n)
    return None


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


# ── 막0 : 해가 지고 ───────────────────────────────────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))

    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 800.0))   # 청주(고도 800m 산지)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))     # 지상 하늘 쇼 = 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))        #                + 지면 OFF
    earth.setElevationScale(0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))          # 여름 은하수

    dm.stop(); sleep(0.2)
    # ★ 청주 8/13 새벽 2시(극대·페르세우스 고도 충분) = 8/12 17:00 UTC
    dm.setDateTime(2026, 8, 12, 17, 0, 0, tz, Anim(0.0))
    sleep(0.4)

    cam.setOrientationH(H_NORTHEAST, Anim(0.0))      # 북동
    cam.setTargetHeight(TILT, Anim(0.0))

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setSize(0.052)
    txt.setColor(Vec(1.0, 1.0, 0.55))
    txt.setDistance(1.0, Anim(0.0))                  # 지상 자막 = distance 1.0
    txt.setText("8월 13일 새벽 2시, 청주")
    txt.setIntensity(1.0, Anim(1.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
    sleep(3.5)
    say("오늘 밤은 달이 거의 없다 — 조도 2%")
    say("유성우를 보기에 이보다 좋은 조건은 드물다")
    say("북동쪽 하늘을 보자")
except Exception as e:
    print("막0 오류:", e)

# ── 막1 : 복사점 — 페르세우스자리 ─────────────────────────────
try:
    per = Constellation(Constellation.ConstellationName.Per)
    per.setLinesIntensity(0.8, Anim(2.0))
    per.setLabelIntensity(0.9, Anim(2.0))
    sleep(2.5)

    say("페르세우스자리")
    say("유성은 여기 한 점에서 뻗어 나온다")
    say("그 점을 복사점이라고 부른다")
    say("지구가 혜성이 남긴 부스러기 띠로 돌진하는 방향이다")
    say("스위프트-터틀 혜성이 133년마다 뿌려 놓은 먼지다")
except Exception as e:
    print("막1 오류:", e)

# ── 막2 : 유성우 시작 ─────────────────────────────────────────
try:
    ss = ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)

    _mdl = pick(ShootingStar.Model, "Gradient")
    if _mdl is not None:
        feat(ss, "setRepresentationType", _mdl)
    _ref = pick(ShootingStar.Referential, "RaDec")
    if _ref is not None:
        feat(ss, "setReferential", _ref)             # ★ 복사점을 하늘에 고정 = 진짜 페르세우스에서 방사

    feat(ss, "setRainGradientPoint", Vec2(RADIANT_RA, RADIANT_DEC))
    feat(ss, "setRainChaosGradientPoint", 12.0)      # 방사 산포 12°
    feat(ss, "setRainSpeed", 1.0)
    feat(ss, "setBrightness", 1.0)
    feat(ss, "setTrailLength", 0.7)

    # ⚠️ ZHR 내부 저장 = ZHR/60(분당 개수). 실제 페르세우스 ZHR 은 100 이지만
    #    그 값을 넣으면 30초에 한 개꼴이라 돔에서는 '아무 일도 안 일어난다'.
    feat(ss, "setZenithalHourlyRate", 900.0)
    feat(ss, "setRainSeed", 1)                       # ★ 재생 시작

    say("시작한다", 0)
    sleep(6.0)
    say("한 줄기")
    sleep(5.0)
    say("또 한 줄기")
    sleep(5.0)
    say("전부 같은 곳에서 뻗어 나오는 게 보이나")
    sleep(5.0)
    say("평행하게 쏟아지는 먼지가 원근 때문에 한 점에서 퍼져 보인다")
    sleep(4.0)
except Exception as e:
    print("막2 오류:", e)

# ── 막3 : 극대 — 쏟아진다 ─────────────────────────────────────
try:
    say("극대 시각이다", 0)
    feat(ss, "setZenithalHourlyRate", 2400.0)        # 폭풍 연출(실제보다 크게 — 돔 가시성)
    sleep(5.0)
    say("한 시간에 백 개 — 실제로는 이 정도 속도다")
    sleep(5.0)
    say("대부분 모래알보다 작다")
    sleep(5.0)
    say("초속 59km 로 대기와 부딪혀 타 버린다")
    sleep(5.0)
    say("빛나는 건 돌이 아니라 데워진 공기다")
    sleep(4.0)
except Exception as e:
    print("막3 오류:", e)

# ── 막4 : 마무리 ──────────────────────────────────────────────
try:
    feat(ss, "setZenithalHourlyRate", 700.0)         # 진정
    say("내년 이맘때 지구는 같은 자리를 다시 지난다")
    say("그때도 이 먼지는 거기 있을 것이다")
    sleep(3.0)
    feat(ss, "setRainSeed", 0)                       # 유성우 정지
    txt.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("막4 오류:", e)

print("쇼 종료 — 오늘 밤, 페르세우스")

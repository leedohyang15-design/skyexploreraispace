# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 규칙 검사는 통과했으나 돔에서 본 기록이 없다. 기하(프레임·L/B·R 단위)는 정적 검사로 안 잡히니 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 ④ — "사라진 밤하늘"  (약 7분)
#  Q1. 도시에서 별이 몇 개나 보이나?  → 광공해 단계별 감광
#  Q2. 그럼 원래는 어떻게 보였나?     → 어두운 곳으로 이동(관측지 이름 이동)
#  Q3. 우리가 잃은 건 뭔가?           → 은하수 + 별색 + 유성
#
#  태우는 규칙: 관측지 이름 이동(CityType/MountainType) + 좌표 안정 폴링 ·
#              광공해는 Stars/Galaxy 를 직접 감광(setLightPollutionIntensity 만으론 안 됨) ·
#              별 채도 · 유성우 · 끊김 없는 복귀
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()
t1  = None

# ═══ 검증된 공통 헬퍼 (2026-07-30 실측 규칙) ═══════════════════
def say(text, hold=0.0):
    if t1 is not None:
        t1.setText(text); t1.setIntensity(1.0, Anim(0.8))
    if hold: sleep(hold)

def dark(sec=1.2):
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(sec)

def light(sec=2.0):
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(sec)

def clamp_dark(sec):
    """★ reset()/FadeTo 는 GlobalIntensity 를 1.0 으로 되돌린다 → 0 을 계속 찍어 눌러야 함"""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(0.2)

CAPTION_H = 12          # ★ 자막 기본 높이 (사용자 확정) — 25 는 천체와 겹쳤다. 더 아래로.


def make_caption(dist=1.0, height=None):
    """자막 생성/재배치.
       ⚠️ 이전 자막을 반드시 끈다 — 안 끄면 옛 자막이 그 자리에 남아 '안 내려간 것처럼' 보인다(실측 사고).
       ⚠️ 행성 프레임은 distance 20 + setSize 금지 / 지상은 distance 1.0 + setSize 0.052."""
    global t1
    if height is None:
        height = CAPTION_H
    if t1 is not None:
        try: t1.setIntensity(0.0, Anim(0.0))      # ★ 옛 자막 끄기
        except Exception: pass
    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, height, 0))
    if dist == 1.0:
        t1.setSize(0.052)                          # 행성 프레임에선 setSize 금지
    t1.setColor(Vec(1.0, 1.0, 0.55))
    t1.setDistance(dist, Anim(0.0))
    t1.setIntensity(0.0, Anim(0.0))



def goto_place(dtype, name, caption, during=None, fade=10.0):
    """관측지 이동. ★ during 을 주면 **이동하는 동안 동시에** 그 변화를 진행시킨다.
       (실측 지적: 도시에 '도착한 뒤' 별을 끄면 작위적으로 보임 →
        이동과 감광이 함께 일어나야 '가까워질수록 하늘이 흐려지는' 것처럼 자연스럽다)"""
    h = db.data(getattr(Data.Type, dtype), name)
    if h is None:
        print("   ⚠️ %s '%s' 조회 실패" % (dtype, name)); return False
    say(caption)
    h.action(Action.Type.GoTo).trigger()
    if during:
        during(fade)                     # ★ 이동이 진행되는 '동안' 긴 Anim 으로 함께 변화
    pos = wait_place_settle()
    cam.setTargetHeight(30.0, Anim(1.0))
    if pos: print("   → %s: %.3f / %.3f / %.0fm" % ((name,) + pos))
    return True


# ── 막0 : 원래의 밤하늘부터 (어두운 곳에서 시작) ─────────────
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night_slow(y=2026, mo=8, d=1, h=13, mw=0.9)     # 여름밤, 은하수 가득
make_caption(1.0)
stars  = Stars(Stars.StarsName.StarrySky)
galaxy = Galaxy(Galaxy.GalaxyName.MilkyWay)
earth  = Planet(Planet.PlanetName.Earth)

stars.setIntensity(1.0, Anim(0.0))
galaxy.setExposure(1.9, Anim(0.0))
try: earth.setLightPollutionIntensity(0.0, Anim(0.0))
except Exception as ex: print("   lightPollution:", ex)
light(3.0)

say("불빛이 없는 곳의 여름밤", 5.0)
say("이게 — 원래 밤하늘이다", 6.0)

stars.setPointSaturation(4.5, Anim(4.0))               # 별 색이 드러남
sleep(5.0)
say("자세히 보면 별에는 색이 있다", 6.0)
say("하늘을 가로지르는 저 띠가 우리 은하 — 은하수", 7.0)

# ── 막1 : Q1 — 에베레스트로 (가장 맑은 하늘) ─────────────────
print("\n[막1] 가장 맑은 하늘")
say("질문. 지금도 이런 하늘이 남아 있나?", 5.0)
goto_place("MountainType", "Everest", "에베레스트 — 해발 8,800m")
sleep(6.0)
say("공기가 얇을수록 별은 더 또렷해진다", 6.0)
galaxy.setExposure(2.2, Anim(3.0)); sleep(4.0)

# ── 막2 : 그 하늘이 주는 것 ──────────────────────────────────
print("\n[막2] 유성")

# 유성 하나
try:
    ss = ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)
    ss.setRepresentationType(ShootingStar.Model.Gradient)
    ss.setBrightness(1.0, Anim(0.0))
    ss.setTrailLength(1.2, Anim(0.0))
    ss.setStartPosition(Vec2(40.0, 70.0))
    ss.setArrivalPosition(Vec2(-30.0, 25.0))
    say("그리고 가끔, 이런 것도")
    ss.setAdvancing(0.0, Anim(0.0)); sleep(0.4)
    ss.setAdvancing(1.0, Anim(2.5)); sleep(3.5)
except Exception as ex:
    print("   유성:", ex)
sleep(2.0)

# ── 막3 : Q2 — 도시로 다가가며 하늘이 사라진다 ───────────────
#    ★ 실측 지적 반영: '도착 후 별 끄기'는 작위적 → **이동하는 동안 함께 흐려지게**
print("\n[막3] 도시로 — 이동하며 하늘이 사라진다")
say("두 번째 질문. 그럼 우리 대부분은 어떤 하늘을 보고 있나?", 6.0)


def fade_to_suburb(sec):
    """이동하는 동안 서서히 흐려짐 — 시골 수준"""
    try: earth.setLightPollutionIntensity(0.35, Anim(sec))
    except Exception: pass
    stars.setIntensity(0.80, Anim(sec))
    galaxy.setIntensity(0.40, Anim(sec))
    galaxy.setExposure(1.4, Anim(sec))


def fade_to_city(sec):
    """이동하는 동안 더 흐려짐 — 대도시 수준"""
    try: earth.setLightPollutionIntensity(1.0, Anim(sec))
    except Exception: pass
    stars.setIntensity(0.40, Anim(sec))
    galaxy.setIntensity(0.05, Anim(sec))
    galaxy.setExposure(1.0, Anim(sec))


# 산 → 작은 도시(런던)로 가면서 서서히 흐려짐
goto_place("CityType", "London", "산을 내려와, 도시 쪽으로",
           during=fade_to_suburb, fade=12.0)
sleep(4.0)
say("도시가 가까워질수록 하늘이 옅어진다", 6.0)

# → 대도시(도쿄)로 가면서 은하수가 완전히 사라짐
goto_place("CityType", "Tokyo", "그리고 대도시 한복판으로",
           during=fade_to_city, fade=12.0)
sleep(4.0)

say("같은 하늘, 같은 시각인데", 5.0)
say("은하수는 사라졌다", 6.0)
say("세계 인구의 3분의 1은 평생 은하수를 못 본다", 7.0)
say("잃어버린 건 별이 아니라 — 어둠이다", 7.0)
t1.setIntensity(0.0, Anim(2.0)); sleep(2.5)
print("\n=== 쇼 종료 ===")

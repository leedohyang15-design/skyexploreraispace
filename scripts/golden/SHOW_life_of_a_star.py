# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 ② — "별의 일생"  (약 8분)
#  Q1. 별은 다 같은 별인가?   → 색이 곧 온도 (리겔 vs 베텔게우스)
#  Q2. 그럼 별은 어디서 오나?  → 별의 요람 (오리온 대성운 M42)
#  Q3. 별은 어떻게 끝나나?     → 조용한 죽음(고양이눈) vs 폭발(게성운 M1)
#  A.  그리고 그 잔해가 다시 별이 된다
#
#  태우는 규칙: 딥스카이 3단(NEBULA GoTo) · 도착 폴링 · 줌 2대원칙 ·
#              별 색 채도(setPointSaturation) · 개별 별 포인터/라벨 · 끊김 없는 복귀
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



def travel_nebula(names, caption, zoom=True):
    """딥스카이(NEBULA 패널) 여행. ⚠️ 이름 후보를 순회해 'GoTo 가 살아있는' 것을 고른다.
       (M번호가 엉뚱한 개체로 매칭되는 사고 방지 — 실측: 'M1' 이 구상성단으로 갔음)"""
    picked = None
    for nm in names:
        try:
            h = db.data(Data.Type.NebulaType, nm)
        except Exception:
            h = None
        if h is None:
            continue
        try:
            if h.action(Action.Type.GoTo) is not None:
                picked = (nm, h); break
        except Exception:
            pass
    if picked is None:
        print("   ⚠️ 여행 가능한 이름 없음: %s" % (names,)); return False
    nm, h = picked
    print("   대상 확정: '%s'" % nm)
    say(caption)
    h.action(Action.Type.GoTo).trigger()
    wait_arrival(max_sec=70, dock_r=None)        # 딥스카이는 dock_r 없이
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    if zoom: zoom_in()
    return True


# ── 막0 : 겨울 오리온 ─────────────────────────────────────────
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night_slow(y=2026, mo=1, d=15, h=12)
make_caption(1.0)
stars = Stars(Stars.StarsName.StarrySky)
light(2.5)
say("겨울, 오리온자리", 4.0)

ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.8, Anim(2.0))
sleep(3.0)

# ── 막1 : Q1 — 별은 다 같은 별인가? (색 = 온도) ───────────────
print("\n[막1] 별의 색 = 온도")
say("질문. 저 별들은 다 같은 별인가?", 5.0)

rigel = IndividualStar(IndividualStar.IndividualStarName.Rigel)
bet   = IndividualStar(IndividualStar.IndividualStarName.Betelgeuse)
rigel.setPointerIntensity(1.0, Anim(1.5)); rigel.setLabelIntensity(1.0, Anim(1.5))
say("리겔 — 푸른 별")
sleep(4.5)
bet.setPointerIntensity(1.0, Anim(1.5)); bet.setLabelIntensity(1.0, Anim(1.5))
say("베텔게우스 — 붉은 별")
sleep(4.5)

say("색을 진하게 해보면")
stars.setPointSaturation(4.5, Anim(3.0))       # 색 채도 ↑ = 온도 차가 눈에 보임
sleep(4.5)
say("푸를수록 뜨겁고, 붉을수록 차갑다 — 색이 곧 온도다", 6.0)
say("리겔 11,000도 / 베텔게우스 3,500도", 5.0)

rigel.setPointerIntensity(0.0, Anim(1.0)); bet.setPointerIntensity(0.0, Anim(1.0))
sleep(1.5)

# ── 막2 : Q2 — 별은 어디서 오나? (별의 요람) ──────────────────
print("\n[막2] 별의 탄생 — M42")
say("두 번째 질문. 그럼 저 별들은 어디서 왔나?", 5.0)
say("오리온의 허리 아래, 뿌연 자리 하나")
sleep(3.0)

lines_off(ori)                                  # ★ 확대 전 별자리 선 OFF (복잡함 방지)
if travel_nebula(["M42", "NGC 1976"], "오리온 대성운 — 별들의 요람"):
    sleep(3.0)
    say("가스와 먼지가 뭉쳐 스스로 불을 켠다", 6.0)
    say("지금도 이 안에서 새 별이 태어나는 중", 5.0)

# ── 막3 : Q3 — 별은 어떻게 끝나나? ───────────────────────────
print("\n[막3] 별의 죽음 — 조용한 끝")
hard_reset_to_ground(y=2026, mo=7, d=15, h=13)   # 여름밤(용자리)
light(2.0)
say("세 번째 질문. 그럼 별은 어떻게 끝나나?", 5.0)
say("가벼운 별은 — 조용히", 3.5)

if travel_nebula(["NGC 6543"], "고양이눈 성운"):
    sleep(3.0)
    say("바깥 껍질을 벗어던지고, 중심엔 하얀 심장만 남는다", 6.0)

print("\n[막3-b] 별의 죽음 — 폭발")
hard_reset_to_ground(y=2026, mo=1, d=15, h=12)   # 겨울(황소자리)
light(2.0)
say("무거운 별은 — 폭발로", 4.0)
# (별자리 선은 켜지 않는다 — 딥스카이 확대 시 복잡해짐)

# ⚠️ 실측 사고: "M1" 로 조회하면 **구상성단으로 이동**했다(엉뚱한 매칭).
#    UI NEBULA 패널 표기가 'M1 / NGC 1952 (Crab Nebula)' 이므로 **NGC 번호를 우선**으로.
if travel_nebula(["NGC 1952", "Crab", "Crab Nebula", "M1"],
                 "게성운 — 서기 1054년의 초신성"):
    sleep(3.0)
    say("송나라 기록에 '낮에도 보이는 별'로 남았다", 6.0)

# ── 막4 : 그리고 다시 ────────────────────────────────────────
print("\n[막4] 순환")
hard_reset_to_ground(y=2026, mo=1, d=15, h=12)
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.5, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky)
stars.setPointSaturation(4.0, Anim(0.0))
light(3.0)

say("흩어진 잔해는 다시 구름이 되고", 5.0)
say("그 구름에서 또 별이 태어난다", 5.0)
say("우리 몸의 원소도 그렇게 만들어졌다", 6.0)
say("우리는 별의 먼지다", 6.0)
t1.setIntensity(0.0, Anim(2.0)); sleep(2.5)
print("\n=== 쇼 종료 ===")

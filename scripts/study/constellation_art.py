# -*- coding: utf-8 -*-
"""
constellation_art.py — 밤하늘 신화: 별자리 그림 (2026-07-15, 미사용 코드 중심)
★ 거의 안 써본 Constellation 코드:
  setArtIntensity(별자리 '그림' = 신화 속 인물/동물 아트) · setLinesIntensity(선) · setLabelIntensity(이름).
  → 별을 잇는 선 위에 실제 신화 그림(백조·전갈·페가수스 등)이 겹쳐 뜬다.
★ 지상 밤하늘(여름밤 청주)에서 하늘에 떠 있는 별자리들의 그림을 켠다.
  ⚠️ 지평선 아래 별자리는 안 뜸 — 그 시각에 '위에 떠 있는' 것만 그림이 보인다(정상).
  ⚠️ DefaultTimeZone=UTC → KST 밤은 UTC 로 -9h (여름밤 22시 KST = UTC 13시).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
CN = Constellation.ConstellationName


def con(nm):
    """이름(IAU 3자)로 Constellation 안전 생성. 없으면 None."""
    try:
        return Constellation(getattr(CN, nm))
    except Exception as e:
        print("   ✗ %s 없음: %s" % (nm, e)); return None


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args); return True
    except Exception as e:
        print("   ✗ %s.%s 실패: %s" % (getattr(obj, "__class__", type(obj)).__name__, fn, e)); return False


# ── 무대: 여름밤 하늘 ───────────────────────────────────────
print("무대: 여름밤 하늘")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(PN.Earth).setIntensity(1.0, Anim(0.0))
try:
    Planet(PN.Earth).setAtmosphereIntensity(0.0, Anim(0.0))   # 대기광 끔 = 검은 하늘(그림 잘 보임)
except Exception:
    pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.9, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))       # 은하수(백조자리 관통)
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.5)); sleep(1.0)        # = KST 22:00 여름밤
cam.setTargetHeight(50.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))   # 하늘 높이(남중~천정)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 58, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("밤하늘 신화 — 별자리 그림"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 여름~가을밤 위에 떠 있는 별자리 큐레이션 (IAU 3자) ──────
#   Cyg 백조, Lyr 거문고, Aql 독수리, Her 헤르쿨레스, Boo 목동, CrB 왕관,
#   Sco 전갈, Sgr 궁수, Oph 뱀주인, Peg 페가수스, And 안드로메다, Cas 카시오페이아, Aqr 물병
NAMES = ["Cyg", "Lyr", "Aql", "Her", "Boo", "CrB", "Sco", "Sgr", "Oph", "Peg", "And", "Cas", "Aqr"]
cons = [(nm, con(nm)) for nm in NAMES]
cons = [(nm, c) for nm, c in cons if c is not None]
print("   생성된 별자리: %s" % [nm for nm, _ in cons])

# ── 1) 별자리 '선' 먼저 (별을 잇는 골격) ───────────────────
narr("별을 선으로 잇는다 — 별자리의 골격", 3.0)
for nm, c in cons:
    feat(c, "setLinesIntensity", 0.7, Anim(2.0))
sleep(3.0)

# ── 2) ★ 별자리 '그림'(아트) 페이드인 = 신화 속 형상 ───────
narr("그 위에 신화의 그림이 떠오른다 — setArtIntensity", 3.0)
for nm, c in cons:
    feat(c, "setArtIntensity", 0.85, Anim(3.0))
sleep(3.5)

# ── 3) 이름표 = 그림을 잠깐 흐리게 하고 이름을 띄운다 ────────
#   ✅ 실측: setLabelIntensity 는 렌더됨. 단 화려한 art(0.85) 위에선 '가려져' 안 보임(사용자 확인).
#   → 이름을 볼 땐 그림을 0.2 로 낮춰 대비를 준다(그러면 라벨이 또렷).
narr("이름을 확인 — 그림을 잠깐 흐리게 하면 이름이 뜬다", 2.0)
for nm, c in cons:
    feat(c, "setArtIntensity", 0.2, Anim(1.5))          # 그림 흐리게 → 라벨이 안 묻힘
for nm, c in cons:
    feat(c, "setLabelIntensity", 1.0, Anim(1.5))        # 뜬 별자리 전부 이름표
sleep(4.5)
narr("이름과 그림 — 다시 그림을 진하게", 2.0)
for nm, c in cons:
    feat(c, "setArtIntensity", 0.85, Anim(1.5))         # 그림 복귀(라벨은 유지)
sleep(1.5)

# ── 신화 해설(대표 몇 개) ───────────────────────────────────
narr("백조자리(Cyg) — 은하수를 가르며 나는 제우스의 백조", 4.5)
narr("전갈자리(Sco) — 오리온을 쏜 전갈, 붉은 안타레스가 심장", 4.5)
narr("페가수스(Peg) — 하늘을 나는 날개 달린 말, 큰 사각형", 4.5)
narr("안드로메다(And) — 사슬에 묶인 공주, 옆엔 안드로메다 은하", 4.5)

# ── 4) 그림만 남기고 선/이름 정리 (그림 감상) ──────────────
narr("선을 지우고 — 그림만 남긴다", 1.5)
for nm, c in cons:
    feat(c, "setLinesIntensity", 0.0, Anim(2.5))
sleep(3.0)
narr("고대인이 올려다본 하늘 — 그림으로 가득한 밤", 4.0)

# ── 정리 ────────────────────────────────────────────────────
for nm, c in cons:
    feat(c, "setArtIntensity", 0.0, Anim(2.5))
    feat(c, "setLabelIntensity", 0.0, Anim(2.0))
t1.setText("밤하늘 신화 — 별과 그림"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. ★setArtIntensity(신화 그림)·setLabelIntensity(이름표) 둘 다 동작 확정. "
      "이름표는 art 에 가려지므로 볼 땐 art 0.2 로 낮춤(사용자 확인). "
      "리포트: 그림 흐리게 했을 때 이름표가 또렷이 뜨나 확인.")

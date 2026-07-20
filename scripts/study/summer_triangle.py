# -*- coding: utf-8 -*-
"""
summer_triangle.py — 여름철 대삼각형과 은하수 (2026-07-16, 지상 밤하늘)
★ 여름밤 머리 위: 직녀성(베가·거문고), 견우 근처 알타이르(독수리), 데네브(백조)가 이루는 큰 삼각형.
  그 사이로 은하수가 백조자리를 관통해 흐른다. 여름 하늘의 대표 풍경.
★ 위성계 코드 말고 '별하늘' 조합: Constellation 선(Lyr/Cyg/Aql) + 개별 별 포인터/라벨(Vega/Deneb/Altair) +
  Galaxy(은하수) 노출/밝기. 전부 확정 API. 위험한 카메라 무빙 없음(지상 고정).
★ 시간: 청주 여름밤 22:00 KST = 13:00 UTC (UTC=KST-9). 대삼각형이 머리 위 → 하늘 높이 올려다봄.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
LON, LAT, ALT = 127.49, 36.64, 400.0
earth = Planet(Planet.PlanetName.Earth)
stars = Stars(Stars.StarsName.StarrySky)
mw = Galaxy(Galaxy.GalaxyName.MilkyWay)

# (별 enum, 한글, 별자리 약어, 별자리 한글)
TRIANGLE = [
    ("Vega",   "직녀성(베가)",   "Lyr", "거문고자리"),
    ("Deneb",  "데네브",         "Cyg", "백조자리"),
    ("Altair", "알타이르",       "Aql", "독수리자리"),
]


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def make_star(nm):
    IN = IndividualStar.IndividualStarName
    if hasattr(IN, nm):
        try: return IndividualStar(getattr(IN, nm))
        except Exception as e: print("   %s 생성 실패: %s" % (nm, e))
    else:
        print("   ⚠️ IndividualStarName 에 %s 없음" % nm)
    return None


def con_lines(abbr, inten=0.8):
    CN = Constellation.ConstellationName
    if hasattr(CN, abbr):
        try: feat(Constellation(getattr(CN, abbr)), "setLinesIntensity", inten, Anim(1.5), label="(%s 선)" % abbr)
        except Exception as e: print("   %s 선 실패: %s" % (abbr, e))
    else:
        print("   ⚠️ ConstellationName 에 %s 없음" % abbr)


# ── 무대(지상 여름밤) ───────────────────────────────────────
print("무대: 청주 여름밤 (대삼각형 머리 위)")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 어두운 시골 밤)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
mw.setIntensity(1.0, Anim(0.0))
feat(mw, "setExposure", 1.8, Anim(0.0), label="(은하수 노출 ↑ = 풍성)")
feat(stars, "setPointSaturation", 2.5, Anim(0.0), label="(별 색 살짝)")

# 관측지 + 시각(청주 22시 = 13 UTC) + 머리 위 조준
Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 22:00 KST
cam.setOrientationH(0.0, Anim(0.0))         # 남 기준
cam.setTargetHeight(18.0, Anim(0.0))        # 하늘 높이(고도~72) 올려다봄 = 머리 위 대삼각형

# ── 자막(지상 가독성 표준) ──────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 1.0, 0.55))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("여름밤, 머리 위를 올려다보면", 3.0)

# ── 은하수 먼저 ─────────────────────────────────────────────
narr("은하수가 하늘을 가로질러 흐른다", 3.5)

# ── 세 별 지목 + 별자리 선 ─────────────────────────────────
made = []
for nm, ko, abbr, cko in TRIANGLE:
    s = make_star(nm)
    con_lines(abbr)
    if s is not None:
        feat(s, "setPointerIntensity", 1.0, Anim(1.0), label="(%s)" % ko)
        feat(s, "setLabelIntensity", 1.0, Anim(1.0), label="(%s 라벨)" % ko)
        made.append((ko, cko))
    narr("%s — %s의 으뜸별" % (ko, cko), 3.2)

# ── ★ 대삼각형을 '선으로' 잇기 = 성군(Asterism) 프리셋 (신규 발견) ──
#   Constellation.ConstellationName 에 ASTERISM_STr(Summer Triangle) 내장 → setLinesIntensity 로 그림.
t1.setText("이 세 별이 여름철 '대삼각형'을 이룬다"); t1.setIntensity(1.0, Anim(1.0))
if hasattr(Constellation.ConstellationName, "ASTERISM_STr"):
    feat(Constellation(Constellation.ConstellationName.ASTERISM_STr), "setLinesIntensity", 1.0, Anim(2.5),
         label="(★ 대삼각형 성군 선)")
else:
    print("   ⚠️ ASTERISM_STr 없음 — dir 확인 필요")
sleep(4.0)
narr("은하수는 백조자리를 따라 그 사이로 흐른다", 4.0)
narr("백조의 부리 근처에서 은하수가 둘로 갈라진다 — '거대 균열'", 4.5)

# ── 은하수 대비 A/B (노출) ─────────────────────────────────
narr("도시의 불빛이 없다면, 이렇게 보인다", 2.0)
feat(mw, "setExposure", 2.4, Anim(3.0), label="(은하수 더 밝게)")
sleep(3.2)

# ── 정리 ────────────────────────────────────────────────────
narr("직녀와 견우, 그리고 그 사이 은하수 — 여름밤의 하늘", 4.5)
t1.setText("여름철 대삼각형 — 베가 · 데네브 · 알타이르"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
feat(mw, "setExposure", 1.0, Anim(2.0), label="(노출 원복)")
feat(stars, "setPointSaturation", 1.0, Anim(1.5), label="(채도 원복)")
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①청주 여름밤(검은 하늘)에 대삼각형이 머리 위에 담기나(안 담기면 H/TargetHeight 조정) "
      "②은하수가 하늘을 가로질러 보이나(노출 1.8→2.4 로 더 풍성해지나) "
      "③세 별(베가/데네브/알타이르) 포인터+라벨 + 별자리 선(거문고/백조/독수리) 뜨나 ④구도/시간 조정?")

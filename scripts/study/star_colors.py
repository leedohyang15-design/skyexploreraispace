# -*- coding: utf-8 -*-
"""
star_colors.py — 별의 색은 온도다 (2026-07-15, 오리온자리)
★ 별의 색 = 표면온도. 파란 별(리겔 ~12000K)은 뜨겁고, 붉은 별(베텔게우스 ~3500K)은 차갑다.
  오리온자리엔 둘이 한 별자리에 있어 대비가 완벽 → 색=온도를 한눈에.
★ 지상 밤하늘 장면(위험한 카메라 무빙 없음, 안정). 미사용 조합:
  IndividualStar 내장 포인터(setPointerIntensity)+라벨(setLabelIntensity) 로 개별 별 지목 +
  Stars.setPointSaturation 로 별 색 채도를 확 올려(0↔4.5 확정) 색이 눈에 띄게.
★ 시간: 겨울 저녁 오리온 남중. 청주 21:00 KST = 12:00 UTC (UTC=KST-9 규칙).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
LON, LAT, ALT = 127.49, 36.64, 200.0
stars = Stars(Stars.StarsName.StarrySky)
earth = Planet(Planet.PlanetName.Earth)

# 오리온 주요 별 (이름, 한글, 색, 온도K) — 색=온도 설명용
STARS = [
    ("Rigel",      "리겔",     "청백(뜨겁다)",  12100),
    ("Betelgeuse", "베텔게우스", "붉음(차갑다)",   3500),
    ("Bellatrix",  "벨라트릭스", "청백",          22000),
    ("Belltrix",   "벨라트릭스", "청백",          22000),   # 철자 폴백
]


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def make_star(nm):
    IN = IndividualStar.IndividualStarName
    if hasattr(IN, nm):
        try:
            return IndividualStar(getattr(IN, nm))
        except Exception as e:
            print("   %s 생성 실패: %s" % (nm, e))
    else:
        print("   ⚠️ IndividualStarName 에 %s 없음" % nm)
    return None


def con_lines(abbr, inten=0.8):
    """별자리 선 켜기 (IAU 3자 약어). 없으면 조용히 패스."""
    CN = Constellation.ConstellationName
    if hasattr(CN, abbr):
        try:
            feat(Constellation(getattr(CN, abbr)), "setLinesIntensity", inten, Anim(1.5), label="(%s 선)" % abbr)
        except Exception as e:
            print("   %s 선 실패: %s" % (abbr, e))
    else:
        print("   ⚠️ ConstellationName 에 %s 없음" % abbr)


# ── 무대(지상 밤) ───────────────────────────────────────────
print("무대: 청주 겨울 저녁 (오리온 남중)")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 검은 하늘, 별색 대비)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))

# 관측지 + 시각(청주 21시 = 12 UTC) + 남쪽 조준
Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 2, 1, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 21:00 KST
cam.setOrientationH(0.0, Anim(0.0))       # 남
cam.setTargetHeight(37.0, Anim(0.0))      # 오리온 남중 고도~53 중심

# 원본 채도 읽어두기(복귀용)
try:
    ORIG_SAT = stars.pointSaturation
except Exception:
    ORIG_SAT = 1.0
print("   원본 pointSaturation=%s" % ORIG_SAT)

# ── 자막 ────────────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
# 자막 개선: 크게(0.052) + 위치 올림(높이 25 = 프레임 하단이지만 지평선 위) + 밝은 노랑(검은 하늘에 잘 뜸)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 1.0, 0.55))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("별의 색은 온도를 말한다", 3.5)

# ── 오리온 별자리 선 ────────────────────────────────────────
ori = Constellation(Constellation.ConstellationName.Ori)
feat(ori, "setLinesIntensity", 0.8, Anim(1.5), label="(오리온 선)")
sleep(1.5)
narr("오리온자리 — 겨울 하늘의 사냥꾼", 3.0)

# ── 채도 부스트: 별 색이 확 살아나게 (0↔4.5 확정) ──────────
narr("별들의 색을 진하게", 1.5)
feat(stars, "setPointSaturation", 4.2, Anim(3.0), label="(채도 ↑ = 색 선명)")
sleep(3.2)

# ── 개별 별 지목: 리겔(파랑) vs 베텔게우스(빨강) ────────────
made = {}
for nm, ko, col, K in STARS:
    if nm in ("Belltrix",) and "Bellatrix" in made:
        continue
    s = make_star(nm)
    if s is not None:
        made[nm] = s

rigel = made.get("Rigel")
if rigel is not None:
    feat(rigel, "setPointerIntensity", 1.0, Anim(1.0), label="(리겔 지목)")
    feat(rigel, "setLabelIntensity", 1.0, Anim(1.0), label="(리겔 라벨)")
narr("리겔 — 청백색. 표면 12,000도의 뜨거운 별", 4.0)

bet = made.get("Betelgeuse")
if bet is not None:
    feat(bet, "setPointerIntensity", 1.0, Anim(1.0), label="(베텔게우스 지목)")
    feat(bet, "setLabelIntensity", 1.0, Anim(1.0), label="(베텔게우스 라벨)")
narr("베텔게우스 — 붉은색. 3,500도로 '식은' 초거성", 4.0)
narr("같은 별자리, 정반대의 온도 — 색이 그 증거다", 4.0)

# ── 시리우스(큰개자리 CMa) — 별자리 선도 같이 켜기 ─────────
sirius = make_star("Sirius")
if sirius is not None:
    con_lines("CMa")                 # 큰개자리 선
    feat(sirius, "setPointerIntensity", 1.0, Anim(1.0), label="(시리우스)")
    feat(sirius, "setLabelIntensity", 1.0, Anim(1.0), label="(시리우스 라벨)")
narr("시리우스 — 큰개자리, 밤하늘에서 가장 밝은 별. 희게 빛난다", 4.0)

# ── 알데바란(황소자리 Tau) — 별자리 선도 같이 켜기 ─────────
ald = make_star("Aldebaran")
if ald is not None:
    con_lines("Tau")                 # 황소자리 선
    feat(ald, "setPointerIntensity", 1.0, Anim(1.0), label="(알데바란)")
    feat(ald, "setLabelIntensity", 1.0, Anim(1.0), label="(알데바란 라벨)")
narr("알데바란 — 황소자리의 눈, 주황빛 거성", 4.0)
narr("파랑→흰색→노랑→주황→빨강, 뜨거운 별에서 차가운 별로", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("별을 보면 그 온도가 보인다", 4.0)
t1.setIntensity(0.0, Anim(1.5))
feat(stars, "setPointSaturation", ORIG_SAT, Anim(2.0), label="(채도 원복)")
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①청주 밤(검은 하늘)에 오리온이 남쪽에 떠서 화면에 담기나(아니면 H/TargetHeight 조정) "
      "②채도 부스트(4.2)로 별 색이 눈에 띄게 진해지나(리겔 파랑/베텔게우스 빨강) "
      "③개별 별 포인터+라벨(리겔/베텔게우스/시리우스/알데바란) 뜨나 ④구도/시간 조정?")

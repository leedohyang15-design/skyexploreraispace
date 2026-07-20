# -*- coding: utf-8 -*-
"""
constellation_boundaries.py — 하늘의 지도: 별자리는 '그림'이 아니라 '영역'이다 (2026-07-16, 안 쓴 API=별자리 경계선)
★ 안 쓴 코드: 별자리 '경계선(boundaries)' — IAU 가 1930년 하늘 전체를 88조각으로 나눈 공식 경계.
  별을 잇는 '선(lines)'·신화 '그림(art)'은 해봤지만, 하늘을 빈틈없이 나누는 '경계(영역)'는 처음.
  ★★ v4 찾음: 경계선 세터 = **`Constellation.setLimitsIntensity`** (RSA Cosmos 는 경계를 'limits/limites'라 부름 →
     bound/frontier 키워드에 안 걸렸던 것. v3 전체 덤프로 발견). 16개 별자리 전부 setLimitsIntensity 로 켠다.
  ⚠️ v1/v2/v3 경로: DB BoundaryOn 은 트리거돼도 안 그려짐 / Planet엔 경계 없음 → 정답은 Constellation.setLimitsIntensity.
     신화그림(art)은 16개 전부(v2 는 5개만 = 사용자 지적).
★ 구성: 겨울 남쪽 하늘(오리온·황소·큰개 등 풍부) → 별 → 선 → 신화그림 → ★경계선(하늘을 88조각으로) → 일주 회전.
★ 시각: 청주 겨울 저녁 21:00 KST = 12:00 UTC. 남쪽(H=0) Target 30.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
LON, LAT, ALT = 127.49, 36.64, 300.0
earth = Planet(Planet.PlanetName.Earth)
stars = Stars(Stars.StarsName.StarrySky)

# 겨울 남쪽 하늘 풍부한 별자리(IAU 약어)
WINTER = ["Ori", "Tau", "Gem", "CMa", "CMi", "Aur", "Mon", "Lep",
          "Eri", "Cet", "Ari", "Per", "Tri", "And", "Cnc", "Leo"]
ART = ["Ori", "Tau", "Gem", "CMa", "Aur"]   # 신화 그림 얹을 대표들


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def con(abbr):
    CN = Constellation.ConstellationName
    return Constellation(getattr(CN, abbr)) if hasattr(CN, abbr) else None


# ── ★ 경계선 API 탐색 (v1 결론: Constellation 엔 없음 / DB BoundaryOn 안 그려짐) ──
#   가설: 좌표 그리드처럼 '하늘 전체 레이어' = Planet(지구) 글로벌 세터. 로그로 훑고 유력 후보 직접 호출.
def probe_boundary_api():
    """v3: 키워드 필터로 놓칠까봐 '메서드 전체'를 덤프 — 이름이 예상 밖이어도 눈으로 잡게."""
    print("   ── 경계선 API 전체 덤프 ──")
    c = con("Ori")
    if c is not None:
        cm = [m for m in dir(c) if m.startswith("set")]
        print("   [Constellation set* 전체(%d)] %s" % (len(cm), cm))
    pm = [m for m in dir(earth) if m.startswith("set")]
    print("   [Planet set* 전체(%d)] %s" % (len(pm), pm))
    # DB 에 '경계' 전용 Data.Type 이 따로 있나 훑기
    dts = [t for t in dir(Data.Type) if not t.startswith("__")]
    hit = [t for t in dts if any(k in t.lower() for k in ("bound", "frontier", "constell"))]
    print("   [Data.Type 중 경계/별자리류] %s (전체 %d종)" % (hit if hit else "(전용 타입 없음)", len(dts)))


_GBND = None   # 글로벌 경계 세터 이름(찾으면)


def boundary_all(val=1.0, dur=2.0):
    """경계선 켜기 — 글로벌 Planet 세터 후보 순차 시도."""
    global _GBND
    cands = ["setConstellationBoundariesIntensity", "setConstellationsBoundariesIntensity",
             "setConstellationBoundaryIntensity", "setBoundariesIntensity", "setBoundaryIntensity",
             "setConstellationFrontiersIntensity", "setFrontiersIntensity", "setContourIntensity",
             "setDelimitationIntensity", "setZoneIntensity", "setAreaIntensity", "setPerimeterIntensity"]
    for nm in cands:
        if hasattr(earth, nm):
            if feat(earth, nm, val, Anim(dur), label="(★ 글로벌 경계 = %s)" % nm):
                _GBND = nm; return True
    return False


def boundary_db_all():
    """DB Action.Type.BoundaryOn 을 '전 별자리'에 (약어→풀네임 순으로) 다시 시도."""
    FULL = {"Ori": "Orion", "Tau": "Taurus", "Gem": "Gemini", "CMa": "Canis Major",
            "CMi": "Canis Minor", "Aur": "Auriga", "Mon": "Monoceros", "Lep": "Lepus",
            "Eri": "Eridanus", "Cet": "Cetus", "Ari": "Aries", "Per": "Perseus",
            "Tri": "Triangulum", "And": "Andromeda", "Cnc": "Cancer", "Leo": "Leo"}
    on = 0
    for ab in WINTER:
        done = False
        for nm in (ab, FULL.get(ab, ab)):
            try:
                h = DataManager.database().data(Data.Type.ConstellationType, nm)
                if h is not None:
                    a = h.action(Action.Type.BoundaryOn)
                    if a is not None:
                        a.trigger(); on += 1; done = True; break
            except Exception:
                pass
        if not done:
            print("   ✗ %s 경계 DB 경로 없음" % ab)
    print("   DB BoundaryOn 트리거 = %d/%d" % (on, len(WINTER)))
    return on


# ── 무대: 청주 겨울 저녁, 남쪽 (대기 OFF = 검은 하늘) ────────
print("무대: 청주 겨울 저녁, 하늘의 지도 — 별자리 경계선")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF)")
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(지면 OFF)")
feat(earth, "setElevationScale", 0.0, label="(평탄)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 2.5, Anim(0.0), label="(별 색)")

Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 21:00 KST
cam.setOrientationH(0.0, Anim(0.0))      # 남쪽
cam.setTargetHeight(30.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("겨울 남쪽 하늘 — 수많은 별", 3.5)

# ── ① 선(lines): 별을 이어 그림을 그리다 ──────────────────
narr("옛사람들은 별을 이어 그림을 그렸다", 3.5)
nc = 0
for ab in WINTER:
    c = con(ab)
    if c is not None and feat(c, "setLinesIntensity", 0.7, Anim(1.5)):
        nc += 1
print("   별자리 선 ON = %d" % nc)
sleep(2.0)
narr("오리온, 황소, 큰개, 쌍둥이... 겨울의 별자리들", 4.0)

# ── ② 신화 그림(art): '모든' 별자리에 이야기를 입힌다 (v3: 16개 전부) ──
narr("그리고 모든 별그림에 신화를 입혔다", 3.0)
ac = 0
for ab in WINTER:                       # ★ 5개만이 아니라 16개 전부 art
    c = con(ab)
    if c is not None and feat(c, "setArtIntensity", 0.85, Anim(2.0), label="(%s 그림)" % ab):
        ac += 1
print("   신화그림 ON 시도 = %d/%d (그림 에셋 없는 별자리는 안 뜰 수 있음)" % (ac, len(WINTER)))
sleep(2.5)
narr("오리온·황소·마차부·페르세우스·안드로메다... 하늘 가득 신화", 4.5)

# ── ③ ★ 경계선(boundaries) = Constellation.setLimitsIntensity ─
#   ★★ 찾음(v3 전체 덤프): RSA Cosmos 는 별자리 '경계'를 'limits(limites)'라 부름 → 키워드 bound/frontier 엔
#   안 걸렸던 것. Constellation 객체의 `setLimitsIntensity(강도, Anim)` 가 바로 경계선. 16개 전부 켠다.
narr("하지만 오늘날 별자리는 '그림'이 아니라 '영역'이다", 4.0)
# 그림은 살짝만 낮춰 경계선이 도드라지게(끄지 않음)
for ab in WINTER:
    c = con(ab)
    if c is not None: feat(c, "setArtIntensity", 0.35, Anim(1.5))
sleep(1.2)
lc = 0
for ab in WINTER:
    c = con(ab)
    if c is not None and feat(c, "setLimitsIntensity", 1.0, Anim(2.5), label="(%s 경계선)" % ab):
        lc += 1
print("   ★ 경계선(limits) ON = %d/%d" % (lc, len(WINTER)))
sleep(2.8)
narr("1930년, 천문학자들은 하늘 전체를 88조각으로 나눴다", 4.5)
narr("빈틈없는 경계선 — 하늘의 모든 점은 한 별자리에 속한다", 4.5)

# ── ④ 일주 회전: 경계 지도가 별과 함께 돈다(하늘에 고정) ────
narr("하룻밤을 빨리 감으면 — 이 지도는 별과 함께 돈다", 3.5)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 16, 0, 0, tz, Anim(26.0)); sleep(27.0)   # +4h 일주(부드러움)
dm.stop()
narr("경계선은 별하늘에 붙어 있다 — 지구가 돌 뿐", 4.0)

# ── 정리 ────────────────────────────────────────────────────
narr("하늘의 지도 — 88개의 별자리, 빈틈없는 경계", 4.0)
feat(stars, "setPointSaturation", 1.0, Anim(1.5), label="(채도 원복)")
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v4 경계선=setLimitsIntensity 발견): "
      "①★★이제 별자리 경계선(하늘을 조각내는 다각형 격자)이 뜨나 — setLimitsIntensity 로 찾음, 핵심 "
      "②16개 그림도 다 나오나(경계 볼 때 art 0.35 로 살짝만 낮춤 — 안 끔) "
      "③경계선이 여러 별자리에 다 떠서 '지도'처럼 맞물리나 ④일주 회전 때 경계가 별과 함께 도나 ⑤밝기/구도 조정?")

# -*- coding: utf-8 -*-
"""
bukdu_polaris.py — 북두칠성으로 북극성 찾기 + 일주운동 (2026-07-16, 지상 북쪽 하늘)
★ 항법의 기본: 북두칠성(큰 국자) 그릇 앞 두 별(메라크→두베)을 5배 연장하면 '북극성'.
  북극성은 천구 북극에 있어 밤새 거의 안 움직이고, 나머지 별은 그 둘레를 돈다(일주운동).
★ 방금 확인한 성군 프리셋 활용: `ASTERISM_BDr`(북두칠성) 한 줄로 그림 + IndividualStar(Polaris) 포인터 +
  UMa/UMi 별자리 선 + 시간가속 일주운동(celestial_rotation 확정 — 시/일 단위는 부드러움).
★ 시각: 청주 봄 저녁(북두칠성 높이 뜸) 22:00 KST = 13:00 UTC. 북쪽(H=180) 조준, 북극성 고도≈위도 36.6.
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


def body_id(obj):
    for a in ("id", "osgId"):
        try:
            v = getattr(obj, a)
            if v:
                return int(v)
        except Exception:
            pass
    return None


def con(abbr, fn, *args, label=""):
    CN = Constellation.ConstellationName
    if hasattr(CN, abbr):
        try: return feat(Constellation(getattr(CN, abbr)), fn, *args, label=label)
        except Exception as e: print("   %s.%s 실패: %s" % (abbr, fn, e))
    else:
        print("   ⚠️ ConstellationName 에 %s 없음" % abbr)
    return False


# ── 무대(지상 봄밤, 북쪽) ───────────────────────────────────
print("무대: 청주 봄 저녁, 북쪽 하늘")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 검은 하늘)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 2.2, Anim(0.0), label="(별 색 살짝)")

Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 5, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 22:00 KST
cam.setOrientationH(180.0, Anim(0.0))     # 북쪽
cam.setTargetHeight(45.0, Anim(0.0))      # 북극성(고도~37)이 하단-중앙, 북두칠성은 그 위

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 1.0, 0.55))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("북쪽 하늘 — 길잡이 별을 찾아보자", 3.0)

# ── 북두칠성 (성군 프리셋) ─────────────────────────────────
con("ASTERISM_BDr", "setLinesIntensity", 1.0, Anim(2.0), label="(★ 북두칠성)")
con("UMa", "setLinesIntensity", 0.35, Anim(2.0), label="(큰곰자리 희미하게)")
sleep(2.2)
narr("북두칠성 — 큰곰자리의 국자 일곱 별", 3.5)

# ── 그릇 앞 두 별(메라크·두베) + 북두칠성 7별 준비 ──────────
narr("국자 그릇 앞의 두 별을 봐 — 메라크와 두베", 3.5)
DIPPER = ["Dubhe", "Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid"]
dip = {}
for nm in DIPPER:
    s = make_star(nm)
    if s is not None:
        dip[nm] = s
merak, dubhe = dip.get("Merak"), dip.get("Dubhe")
for nm, ko in (("Merak", "메라크"), ("Dubhe", "두베")):
    if dip.get(nm) is not None:
        feat(dip[nm], "setPointerIntensity", 1.0, Anim(1.0), label="(%s)" % ko)
        feat(dip[nm], "setLabelIntensity", 1.0, Anim(1.0), label="(%s 라벨)" % ko)
narr("이 둘을 이어 다섯 배 늘이면...", 3.0)

# ── 북극성 지목 ─────────────────────────────────────────────
polaris = make_star("Polaris")
if polaris is not None:
    feat(polaris, "setPointerIntensity", 1.0, Anim(1.2), label="(★ 북극성 지목)")
    feat(polaris, "setLabelIntensity", 1.0, Anim(1.2), label="(북극성 라벨)")

# ── ★ 지시선 = 두베→북극성 '직결' + 5등분 (사용자 제안: 끝점을 북극성으로 = 정확히 닿음) ──
#   끝점 body 를 북극성으로 지정 → 선이 반드시 북극성에서 끝남(연장 배수 추정 불필요). 그걸 5등분해 '다섯 칸'.
if dubhe is not None and polaris is not None:
    try:
        ln = Line(Line.LineName.Line001)
        sid, eid = body_id(dubhe), body_id(polaris)
        ln.setStartPoint(sid); ln.setEndPoint(eid)   # ★ 끝점=북극성 → 선이 북극성에 정확히 닿음
        # ★ divisor=5 → 눈금 단위 = (두베-북극성)/5. advancement=5 → 5단위(=전체) 그림 → 정확히 5칸으로 북극성까지.
        #   (divisor 만 주면 advancement 기본 1 = 1/5 길이만 그려짐 = '1칸' 버그. 둘을 같은 값으로.)
        try: ln.setAdvancementDivisor(5)
        except Exception as e: print("   divisor: %s" % e)
        try: ln.setAdvancement(5.0, Anim(0.0))       # ★ 5칸 다 그리기
        except Exception as e: print("   advancement: %s" % e)
        try: ln.setGraduationSize(4.0, Anim(0.0))    # 칸 눈금 크게
        except Exception as e: print("   graduation: %s" % e)
        try: ln.setLineColor(Vec3(1.0, 0.75, 0.2), Anim(0.0))
        except Exception as e: print("   lineColor: %s" % e)
        try: ln.setLineThickness(2.5, Anim(0.0))
        except Exception as e: print("   thickness: %s" % e)
        ln.setIntensity(1.0, Anim(1.5))
        print("   ✓ 지시선 Line: 두베→북극성 직결 + 5등분 (start=%s end=%s)" % (sid, eid))
    except Exception as e:
        print("   ✗ Line(지시선) 실패: %s" % e)

con("UMi", "setLinesIntensity", 0.6, Anim(2.0), label="(작은곰자리 = 작은 국자)")
narr("북극성 — 작은곰자리 꼬리 끝의 별", 4.0)
narr("북극성은 언제나 정북(正北)을 가리킨다", 4.0)

# ── ★ 일주운동: 별들이 북극성 둘레를 돈다 (궤적 ON) ─────────
narr("하룻밤을 빨리 감아보면", 2.5)
# ★ 별 궤적 ON = '북두칠성만' 이 아니라 밤하늘 밝은 별 전체가 북극성 둘레로 호를 그림(일주운동)
BRIGHT = ["Vega", "Deneb", "Altair", "Capella", "Arcturus", "Aldebaran", "Betelgeuse", "Rigel",
          "Sirius", "Procyon", "Pollux", "Castor", "Regulus", "Spica", "Antares", "Kochab",
          "Schedar", "Caph", "Mirfak", "Alderamin", "Rasalhague", "Denebola", "Hamal",
          "Bellatrix", "Elnath", "Fomalhaut", "Alphard", "Algol", "Polaris"]
tcount = 0
for nm in list(dip.keys()):                       # 북두칠성 7별
    if feat(dip[nm], "setTrajectoryIntensity", 0.9, Anim(1.5)):
        tcount += 1
for nm in BRIGHT:                                 # 주요 밝은 별 전체
    s = make_star(nm)
    if s is not None and feat(s, "setTrajectoryIntensity", 0.9, Anim(1.5)):
        tcount += 1
print("   ★ 궤적 ON 별 수 = %d (하늘 가득 일주운동 호)" % tcount)
sleep(1.5)
narr("모든 별이 북극성을 중심으로 돈다 — 북극성만 제자리", 3.0)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 5, 1, 17, 0, 0, tz, Anim(30.0)); sleep(31.0)   # +4시간(22시→새벽2시) 천천히 = 일주운동
dm.stop()

narr("이것이 지구의 자전 — 북극성은 자전축이 하늘에 닿는 점", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("북두칠성을 찾으면, 밤하늘에서 길을 잃지 않는다", 4.5)
t1.setText("북두칠성과 북극성 — 밤하늘의 나침반"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
feat(stars, "setPointSaturation", 1.0, Anim(1.5), label="(채도 원복)")
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★[Line 지시선] 이제 divisor5+advancement5 로 두베→북극성 '전체'가 그려지고 '정확히 5칸'인가 "
      "(1칸 stub 버그 해결됐나) ②선 끝이 북극성에 딱 닿나 ③하늘 가득 별 궤적(호) OK ④이제 이거 완성?")

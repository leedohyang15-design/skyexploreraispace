# -*- coding: utf-8 -*-
"""
line_probe.py — Line(연결선) 눈금/5칸 표시 실측 프로브 (2026-07-16)
★ bukdu_polaris 에서 Line 5등분이 화면에 안 나옴 → 정확한 사용법 채굴.
  문서(LinkingLine): 눈금 모드 기본 'Segment' = 눈금 간격 = 시작-끝 두 별 거리.
  정석 = 메라크→두베(국자 1칸)에 Advancement=6 → 눈금이 국자 간격마다 = 북극성까지 5~6칸.
★ 이 프로브가 하는 것:
  ① Line 인스턴스의 '실제 메서드 전체' dir 덤프(그라듀에이션/모드 관련 숨은 세터 확인)
  ② LineMode enum 위치 탐색(global LineMode / Line.LineMode / bool)
  ③ 후보 3개를 라벨과 함께 순차 표시 → 어느 게 '5칸 눈금'을 그리는지 눈으로 판정
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def body_id(obj):
    for a in ("id", "osgId"):
        try:
            v = getattr(obj, a)
            if v: return int(v)
        except Exception: pass
    return None


def star(nm):
    IN = IndividualStar.IndividualStarName
    return IndividualStar(getattr(IN, nm)) if hasattr(IN, nm) else None


# ── 무대: 청주 북쪽 밤 ──────────────────────────────────────
print("Line 프로브")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(0.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 5, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.5)
cam.setOrientationH(180.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

merak, dubhe, polaris = star("Merak"), star("Dubhe"), star("Polaris")
Constellation(Constellation.ConstellationName.ASTERISM_BDr).setLinesIntensity(0.8, Anim(0.0))
for s in (merak, dubhe, polaris):
    if s is not None: s.setPointerIntensity(1.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.05); t1.setColor(Vec(1, 1, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)


def label(s): t1.setText(s); t1.setIntensity(1.0, Anim(0.4))


# ── ① dir 덤프: Line 실제 메서드/속성 전체 ─────────────────
ln = Line(Line.LineName.Line001)
ms = [m for m in dir(ln) if not m.startswith("__")]
print("=== Line 인스턴스 메서드/속성 전체 (%d) ===" % len(ms))
print("  " + ", ".join(ms))
print("=== graduation/mode/dash/label 관련만 ===")
print("  " + ", ".join([m for m in ms if any(k in m.lower() for k in ("grad", "mode", "dash", "label", "advance", "represent", "type"))]))

# ── ② LineMode enum 위치 탐색 ──────────────────────────────
print("=== LineMode 탐색 ===")
for path in ("Line.LineMode", "LineMode"):
    try:
        obj = eval(path)
        print("  %s = %s" % (path, [m for m in dir(obj) if not m.startswith("__")]))
    except Exception as e:
        print("  %s 없음 (%s)" % (path, type(e).__name__))


def try_set(l, fn, *a):
    try:
        getattr(l, fn)(*a); print("   ✓ %s%s" % (fn, tuple(str(x)[:12] for x in a))); return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e)); return False


def set_mode_2d(l):
    # LineMode 를 2D 로: enum 후보 → 없으면 bool True 시도
    done = False
    for path, cand in (("Line.LineMode", ("Mode2D", "Line2D", "TwoD", "Angular", "Dome2D")),):
        try:
            enum = eval(path)
            for c in cand:
                if hasattr(enum, c):
                    done = try_set(l, "setLineMode", getattr(enum, c)); break
        except Exception:
            pass
    if not done:
        try_set(l, "setLineMode", True)   # bool 폴백(True=2D)


# ── ③ 후보 A: 메라크→두베 + Advancement=6 (문서 정석) ──────
sid_m, eid_d, eid_p = body_id(merak), body_id(dubhe), body_id(polaris)
print("=== ids: merak=%s dubhe=%s polaris=%s ===" % (sid_m, eid_d, eid_p))
label("A: 메라크→두베, 6배 연장 (Segment 눈금)")
lnA = Line(Line.LineName.Line001)
try_set(lnA, "setStartPoint", sid_m); try_set(lnA, "setEndPoint", eid_d)
set_mode_2d(lnA)
try_set(lnA, "setAdvancement", 6.0, Anim(0.0))
try_set(lnA, "setGraduationSize", 4.0, Anim(0.0))
try_set(lnA, "setLineColor", Vec3(1.0, 0.75, 0.2), Anim(0.0))
try_set(lnA, "setLineThickness", 2.5, Anim(0.0))
try_set(lnA, "setLabelIntensity", 1.0, Anim(0.0))
lnA.setIntensity(1.0, Anim(1.0)); sleep(9.0)
lnA.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── 후보 B: 두베→북극성 + Divisor=5 ───────────────────────
label("B: 두베→북극성, 5등분 (Divisor)")
lnB = Line(Line.LineName.Line002)
try_set(lnB, "setStartPoint", eid_d); try_set(lnB, "setEndPoint", eid_p)
set_mode_2d(lnB)
try_set(lnB, "setAdvancementDivisor", 5)
try_set(lnB, "setGraduationSize", 4.0, Anim(0.0))
try_set(lnB, "setLineColor", Vec3(0.3, 0.8, 1.0), Anim(0.0))
try_set(lnB, "setLineThickness", 2.5, Anim(0.0))
lnB.setIntensity(1.0, Anim(1.0)); sleep(9.0)
lnB.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ── 후보 C: 메라크→두베 + Advancement=6, 3D 모드 ──────────
label("C: 메라크→두베 6배, 3D 모드")
lnC = Line(Line.LineName.Line003)
try_set(lnC, "setStartPoint", sid_m); try_set(lnC, "setEndPoint", eid_d)
try_set(lnC, "setLineMode", False)   # 3D
try_set(lnC, "setAdvancement", 6.0, Anim(0.0))
try_set(lnC, "setGraduationSize", 4.0, Anim(0.0))
try_set(lnC, "setLineColor", Vec3(0.4, 1.0, 0.4), Anim(0.0))
lnC.setIntensity(1.0, Anim(1.0)); sleep(9.0)

label("판정: A / B / C 중 '5칸 눈금'이 북극성까지 그려진 건?")
sleep(3.0)
t1.setIntensity(0.0, Anim(1.0)); uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트: ①위 'Line 메서드 전체' 목록 붙여줘(숨은 그라듀에이션/모드 세터 확인) "
      "②LineMode 탐색 결과(enum 있나/bool 먹나) ③후보 A/B/C 중 '메라크에서 북극성까지 5칸 눈금선'이 제대로 그려진 게 어느 것? "
      "(색: A=노랑 B=파랑 C=초록) ④아무것도 눈금 안 나오면 = 눈금은 SPC 전용일 수도")

# -*- coding: utf-8 -*-
"""
night_guide_tour_v3.py — 그리드 전용 수정판 (2026-07-07)
v2 실측: 포인터 매핑 확정(az = 180-방위 — setOrientationH 와 동일 공식! / 높이 = Target 좌표),
        고유운동 선 추적 확인(선이 별을 따라 일그러짐). 그리드만 미해결 → 이번엔 그리드만.

★ v3 의 핵심 발견 (레퍼런스 재수색):
  지상 좌표 그리드의 '본명령'은 Mark 가 아니라 **Place2D 의 그리드 속성**이었다!
   - setAzimuthGridIntensity      (방위/고도 그리드 — 우리가 원하던 것)
   - setMeridianIntensity         (자오선)
   - setCardinalPointsIntensity   (동서남북 방위표지) + setCardinalPointsRepresentation(레벨)
   - setHourAngleGridIntensity / setHourAngleMeridianIntensity (시간각 그리드)
  행성 하늘 좌표 그리드는 Planet 쪽:
   - setEquatorialGridIntensity / setEclipticGridIntensity / setEquatorialJ2000GridIntensity
  Mark 는 '커스텀 눈금 원' 전용 개체로 추정 — 부모 바인딩(setParent/addChild)이 없어서
  안 보였을 가능성 → ACT C 에서 바인딩 실험.

리포트 포인트: 각 ACT 자막과 함께 그리드가 보이는지 + [MARK-PRESET] 덤프 줄 복사!
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 청주 겨울밤 (동일) ──────────────────────────────────
print("무대 세팅: 청주 2026-01-15 23:00 KST")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))

earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)


def show(setter_name, fn, dur=6.0):
    """그리드 세터 하나 켰다 끄기 + 자막 + 결과 print"""
    try:
        t1.setText("[GRID] %s — 보이나요?" % setter_name)
        t1.setIntensity(1.0, Anim(0.3))
        fn(0.9)
        print("   %s(0.9) ON — %d초" % (setter_name, dur))
        sleep(dur)
        fn(0.0)
        sleep(1.2)
        t1.setIntensity(0.0, Anim(0.3))
    except Exception as e:
        print("   %s 실패: %s" % (setter_name, e))


# ══════════════════════════════════════════════════════════════
# ACT A — Place2D 그리드 4종 (본명령 추정 — 이번 회차의 본편!)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT A: Place2D 그리드 — 방위그리드/자오선/방위표지/시간각")
print("=" * 60)
try:
    print("   현재값: azGrid=%.2f meridian=%.2f cardinal=%.2f hourGrid=%.2f"
          % (place.azimuthGridIntensity, place.meridianIntensity,
             place.cardinalPointsIntensity, place.hourAngleGridIntensity))
except Exception as e:
    print("   현재값 읽기 실패: %s" % e)

show("Place2D.setAzimuthGridIntensity (방위/고도 그리드)",
     lambda v: place.setAzimuthGridIntensity(v, Anim(1.5)), 7.0)
show("Place2D.setMeridianIntensity (자오선)",
     lambda v: place.setMeridianIntensity(v, Anim(1.5)), 5.0)
try:
    # 방위표지는 표현 레벨도 함께 (Level2 = 8방위 추정)
    reps = [m for m in dir(Place2D.CardinalPointRepresentation) if not m.startswith("_")]
    print("   CardinalPointRepresentation 멤버: %s" % reps)
    for r in reps:
        if "2" in r:
            place.setCardinalPointsRepresentation(getattr(Place2D.CardinalPointRepresentation, r))
            print("   representation=%s 적용" % r)
            break
except Exception as e:
    print("   CardinalPointRepresentation 실패: %s" % e)
show("Place2D.setCardinalPointsIntensity (동서남북 표지)",
     lambda v: place.setCardinalPointsIntensity(v, Anim(1.5)), 5.0)
show("Place2D.setHourAngleGridIntensity (시간각 그리드)",
     lambda v: place.setHourAngleGridIntensity(v, Anim(1.5)), 5.0)

# ══════════════════════════════════════════════════════════════
# ACT B — Planet(지구) 하늘 좌표 그리드 2종
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT B: Planet 그리드 — 적도/황도 좌표계")
print("=" * 60)
show("Planet(Earth).setEquatorialGridIntensity (적도 그리드)",
     lambda v: earth.setEquatorialGridIntensity(v, Anim(1.5)), 6.0)
show("Planet(Earth).setEclipticGridIntensity (황도 그리드)",
     lambda v: earth.setEclipticGridIntensity(v, Anim(1.5)), 5.0)

# ══════════════════════════════════════════════════════════════
# ACT C — Mark 부모 바인딩 실험 (안 보였던 원인 후보)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT C: Mark 재도전 — 부모 바인딩 (Place2D 포트에 addChild)")
print("=" * 60)
try:
    ports = [m for m in dir(Place2D.Place2DPort) if not m.startswith("_")
             and m not in ("name", "names", "values") and "Invalid" not in m
             and not m.endswith("Count")]
    print("   [PROBE] Place2DPort 멤버: %s" % ports)
except Exception as e:
    ports = []
    print("   Place2DPort 프로브 실패: %s" % e)

try:
    wg = Mark(Mark.MarkName.Mark051_WelcomeGrid)
    print("[MARK-PRESET] parent=%s posType=%s repType=%s radius=%s meridian=%s parallel=%s "
          "az[%s~%s] h[%s~%s] lineW=%s textSize=%s intensity=%.2f"
          % (wg.parent, wg.positionType, wg.representationType, wg.radius,
             wg.meridianCount, wg.parallelCount, wg.minAzimuth, wg.maxAzimuth,
             wg.minHeight, wg.maxHeight, wg.lineWidth, wg.textSize, wg.intensity))
except Exception as e:
    wg = None
    print("   프리셋 덤프 실패: %s" % e)

try:
    mk = Mark(Mark.MarkName.Mark001)
    mk.setPositionType(Mark.PositionType.InfiniteGrid)
    mk.setRepresentationType(Mark.RepresentationType.Grid)   # 텍스트 없이 기하만 — 단순화
    mk.setMinAzimuth(0.0); mk.setMaxAzimuth(360.0)
    mk.setMinHeight(0.0);  mk.setMaxHeight(90.0)
    mk.setMeridianCount(12); mk.setParallelCount(9)
    mk.setRadius(50.0)
    mk.setLineWidth(3.0)
    mk.setColor(Vec(1.0, 0.2, 0.2))                          # 빨강 — 놓칠 수 없게
    # 부모 바인딩: Place2D 첫 포트에 addChild (InsertText→Camera 패턴의 유추)
    bound = False
    for pn in ports:
        try:
            place.addChild(mk.id, getattr(Place2D.Place2DPort, pn))
            print("   place.addChild(mk, %s) 성공" % pn)
            bound = True
            break
        except Exception as e:
            print("   addChild(%s) 실패: %s" % (pn, e))
    if not bound:
        print("   포트 바인딩 전부 실패 → 바인딩 없이 켜기만")
    t1.setText("[C] Mark 빨간 그리드 — 보이나요?"); t1.setIntensity(1.0, Anim(0.3))
    mk.setIntensity(1.0, Anim(1.5))
    print("   Mark001 ON (7초)")
    sleep(7.0)
    mk.setIntensity(0.0, Anim(1.0))
    sleep(1.0)
    t1.setIntensity(0.0, Anim(0.3))
except Exception as e:
    print("   Mark 실험 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("v3 끝 — 어떤 그리드가 보였는지 + [MARK-PRESET] 줄 복사 부탁!")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("v3 종료.")

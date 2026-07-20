# -*- coding: utf-8 -*-
"""
zodiac_sun.py — 황도 12궁: 태양이 1년간 12별자리를 지나간다 (2026-07-16, v8 지상 MotionAnalemma)
★ v3~v6(우주 줌락) 전부 실패로 폐기. v7(지상 MotionAnnual)은 '태양이 움직여' 화면 밖으로 나감(사용자 확인).
★ v8(확정 도구): 지상 `setMotionType(MotionAnalemma)` = 하루 자전(일주) 상쇄 + 태양을 '제자리(8자)'에 붙잡음.
  카메라를 남쪽에 '한 번만' 고정 → 1년 시간가속 하면 태양은 남쪽 8자 자리에 머물고, 대기 OFF 라 보이는
  별 배경이 ~1바퀴 돌며(아날렘마 노트: 1년=하늘 1바퀴) 12궁이 태양 뒤를 하나씩 통과 = '태양이 별자리를 지남'.
  (아날렘마 쇼는 대기 ON 으로 별을 가려 8자만 봤지만, 여기선 대기 OFF 로 그 배경 회전=12궁 통과를 보여줌.)
  추적·줌락 불필요 = 견고. + 태양 궤적선 OFF(사용자 요청).
★ 시각: 청주 정오(태양 남중=자오선) = 03:30 UTC, 춘분(3/20, 태양이 물고기↔양 경계)에서 시작해 1년.
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
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
stars = Stars(Stars.StarsName.StarrySky)

ZODIAC = [
    ("Ari", "양"), ("Tau", "황소"), ("Gem", "쌍둥이"), ("Cnc", "게"),
    ("Leo", "사자"), ("Vir", "처녀"), ("Lib", "천칭"), ("Sco", "전갈"),
    ("Sgr", "궁수"), ("Cap", "염소"), ("Aqr", "물병"), ("Psc", "물고기"),
]


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대: 지상 (대기 OFF = 검은 하늘 → 낮에도 별·12궁이 보임) ─
print("무대: 청주, 지상 MotionAnnual — 황도 12궁")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))                                   # 지상 마스터 스위치
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 검은 하늘)")
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(지면 OFF)")
feat(earth, "setElevationScale", 0.0, label="(지형 평탄)")
sun.setIntensity(1.0, Anim(0.0)); feat(sun, "setScale", 3.0, label="(태양 크게)")
feat(sun, "setTrajectoryIntensity", 0.0, Anim(0.0), label="(★ 태양 궤적선 OFF — 사용자 요청)")
stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 3.0, Anim(0.0), label="(별 색 ↑ = 별자리 구분)")

# ── 12궁 별자리 선 + 이름 + 황도 그리드(태양이 지나는 길) ──
zc = 0
for abbr, ko in ZODIAC:
    CN = Constellation.ConstellationName
    if hasattr(CN, abbr):
        c = Constellation(getattr(CN, abbr))
        feat(c, "setLinesIntensity", 0.6, Anim(0.0)); feat(c, "setLabelIntensity", 0.9, Anim(0.0)); zc += 1
    else:
        print("   ⚠️ ConstellationName 에 %s 없음" % abbr)
print("   황도 12궁 ON = %d" % zc)
feat(earth, "setEclipticGridIntensity", 0.45, Anim(0.0), label="(황도 그리드 = 12궁이 놓인 띠)")

# ── 관측지 + 시각(춘분 청주 정오 = 03:30 UTC) + 남쪽 조준 ──
Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 3, 20, 3, 30, 0, tz, Anim(0.0)); sleep(0.6)     # 청주 정오, 태양 남중
cam.setOrientationH(0.0, Anim(0.0))          # H=180-방위(180)=0 → 남쪽(정오 태양 방향)
cam.setTargetHeight(37.0, Anim(0.0))         # 아날렘마 확정 레시피값. 태양은 남쪽 8자 자리에 머묾(±23° 오르내림)

# ── 자막(지상 표준: size 0.052 / pos(0,25,0) / 노랑 / distance 1.0) ──
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("황도 12궁 — 태양이 1년에 걸쳐 지나는 하늘의 길", 4.0)
narr("대기를 걷어내면, 대낮에도 태양 뒤의 별자리가 보인다", 4.0)
narr("남쪽 하늘, 태양과 그 뒤로 늘어선 12별자리", 4.0)

# ── ★ 아날렘마 모드 = 하루 자전(일주) 상쇄 → 태양은 '제자리(8자)', 별·12궁이 배경으로 지나감 ──
#   v7 교훈: MotionAnnual 은 '태양이 움직여' 화면 밖으로 나감(사용자 확인). → 태양을 제자리에 붙잡고
#   '별자리가 지나가게' 하는 MotionAnalemma(확정 동작)로 교체. 아날렘마 노트: 1년 가속 시 하늘이 365바퀴가
#   아니라 ~1바퀴만 돎 = 별 배경의 연주 회전 → 그 1바퀴 동안 12궁이 태양 뒤를 하나씩 통과.
_mm = None
for n in ("MotionAnalemma", "MotionAnnual"):
    if hasattr(DateManager.MotionType, n):
        _mm = getattr(DateManager.MotionType, n); print("   모션 = %s" % n); break
if _mm is not None:
    feat(dm, "setMotionType", _mm, label="(★ 일주 상쇄 = 태양 고정·하늘 회전)")
else:
    print("   ⚠️ 모션 미발견 — MotionType 멤버: %s"
          % [m for m in dir(DateManager.MotionType) if not m.startswith("__")])

narr("1년을 빨리 감아본다 — 태양은 자리를 지키고, 별자리가 흐른다", 3.5)

# ── ★ 시간가속 1년 → 태양이 12궁을 한 바퀴 ─────────────────
dm.stop(); sleep(0.3)
dm.setDateTime(2027, 3, 20, 3, 30, 0, tz, Anim(42.0)); sleep(43.0)
dm.stop()

narr("봄엔 물고기·양, 여름엔 쌍둥이·게... 한 바퀴를 돌았다", 4.5)
narr("당신의 별자리 = 태어난 날, 태양이 머물던 바로 그 자리", 4.5)

# ── 정리 ────────────────────────────────────────────────────
if hasattr(DateManager.MotionType, "MotionDiurnal"):
    feat(dm, "setMotionType", DateManager.MotionType.MotionDiurnal, label="(모션 원복)")
feat(stars, "setPointSaturation", 1.0, Anim(1.5), label="(채도 원복)")
narr("황도 12궁 — 하늘을 한 바퀴 도는 태양의 1년", 4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v8 MotionAnalemma — 태양 고정·하늘 회전): "
      "①태양 궤적선 꺼졌나 ②★MotionAnalemma 로 이제 태양이 '남쪽 제자리에 머무나'(v7 처럼 화면 밖으로 안 나가나) — 핵심 "
      "③1년 가속 때 별 배경(12궁)이 ~1바퀴 천천히 돌며 태양 뒤를 하나씩 지나가나 — 핵심 "
      "④하늘이 미친듯 안 돌고 부드럽나 ⑤12궁 선/이름/황도띠 보이나 "
      "⑥태양이 8자로 위아래 좀 오르내리는 건 정상(계절). 더 다듬을 점?")

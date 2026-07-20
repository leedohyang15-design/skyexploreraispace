# -*- coding: utf-8 -*-
"""
night_guide_tour_final.py — 밤하늘 가이드 투어 완성판 (2026-07-07, SPC 변환용)
v1~v4 실측으로 확정한 이번 예제의 모든 기술을 하나의 쇼로:

 ① Stars.setTwinklingAmplitude       — 반짝임 증폭 (기본 1.0 → 3.0 → 원본 복귀)     [v1 ✅]
 ② Place2D/Planet 그리드 (본명령)     — 방위/적도/시간각 그리드 + 동서남북 표지      [v3 ✅]
    · 풀돔 표출 = Target 0 (사용자 운영 확정. Target 30 은 돔 하단이 지평선 아래라 잘림)
    · Target 재정렬 슬루는 암전 속에서 (표준)
 ③ DomePointer                        — 확정 매핑: az = 180−방위(=setOrientationH 공식),
    height = 돔 Target 좌표 (관람 구도에서 오리온 부근 ≈ 85)                         [v2 ✅]
 ④ Constellation.setArtIntensity      — 오리온 선/라벨/그림                           [v1 ✅]
 ⑤ Stars 고유운동                     — setProperMotion + OffsetInYears,
    +50,000년/20초 저속(멀미 방지), 벡터 OFF, 선이 별을 따라 일그러짐                  [v1/v2 ✅]

무대: 청주(36.64, 127.49) 2026-01-15 23:00 KST(=14:00 UT) — 오리온 남중.
"""

from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone      # 실측: UTC 로 해석됨 (KST 아님!)

# ══════════════════════════════════════════════════════════════
# 무대 세팅 — 지상 씬 체크리스트 (암전 속에서 전부)
# ══════════════════════════════════════════════════════════════
print("무대: 청주 2026-01-15 23:00 KST — 오리온 남중")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))          # reset 이 gi 를 되살릴 수 있어 재암전

earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))              # ★ 지상 마스터 스위치
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))     # 청주
dm.stop(); sleep(0.3)                            # ★ 순서: stop → setDateTime
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)

cam.setTargetHeight(30.0, Anim(0.0))            # 🎯 관람 표준 30 으로 시작
cam.setOrientationH(0.0, Anim(0.0))             # H = 180 − 오리온 방위(180) = 0 → 남쪽
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0))                  # ★ 지상 자막 = size 0.035 + distance 1.0
t1.setColor(Vec(0.8, 0.9, 1.0))

uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("밤하늘 가이드 투어 — 청주, 1월의 밤")
t1.setIntensity(1.0, Anim(1.5))
print(">>> 오프닝 (6초)")
sleep(6.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# ① 별 반짝임 — 대기의 일렁임
# ══════════════════════════════════════════════════════════════
print(">>> ① 반짝임 증폭")
tw0 = 1.0
try:
    tw0 = st.twinklingAmplitude                 # ★ 원본 먼저 읽기 (복귀용)
except Exception:
    pass
t1.setText("별이 반짝이는 이유 — 대기의 일렁임"); t1.setIntensity(1.0, Anim(0.8))
st.setTwinklingAmplitude(3.0, Anim(2.0))
sleep(6.0)
st.setTwinklingAmplitude(tw0, Anim(2.0))        # 복귀 = 읽어둔 원본값
sleep(2.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# ② 그리드 쇼 — 암전 → Target 0(전천) → 3장면 → 암전 → Target 30 복귀
# ══════════════════════════════════════════════════════════════
print(">>> ② 그리드 쇼 @ Target 0 (전천 구도)")
uni.setGlobalIntensity(0.0, Anim(1.2)); sleep(1.5)
cam.setTargetHeight(0.0, Anim(0.0))             # ★ 전천 구도 = Target 0 (사용자 운영 확정)
sleep(0.8)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

t1.setText("하늘의 주소판 — 방위와 고도"); t1.setIntensity(1.0, Anim(0.5))
place.setAzimuthGridIntensity(0.9, Anim(2.0))
place.setCardinalPointsIntensity(0.9, Anim(2.0))
sleep(8.0)
place.setAzimuthGridIntensity(0.0, Anim(1.5))
place.setCardinalPointsIntensity(0.0, Anim(1.5))
sleep(1.7)

t1.setText("적도 좌표 그리드 — 북극성이 축")
earth.setEquatorialGridIntensity(0.9, Anim(2.0))
sleep(7.0)

t1.setText("시간각 그리드 — 하늘의 시계")
place.setHourAngleGridIntensity(0.9, Anim(2.0))
sleep(6.0)
earth.setEquatorialGridIntensity(0.0, Anim(1.5))
place.setHourAngleGridIntensity(0.0, Anim(1.5))
sleep(1.7)
t1.setIntensity(0.0, Anim(0.5))

print("   Target 30 복귀 (암전 속)")
uni.setGlobalIntensity(0.0, Anim(1.2)); sleep(1.5)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.8)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ══════════════════════════════════════════════════════════════
# ③ 돔 포인터 — 확정 매핑으로 오리온 서클링
# ══════════════════════════════════════════════════════════════
print(">>> ③ 포인터 — 오리온 (az=180−방위180=0, h≈85=관람 구도 중앙 부근)")
dp = DomePointer(DomePointer.DomePointerName.DomePointer001)
try:
    dp.setPointerType(Body.PointerType.Model1Bold)
except Exception as e:
    print("   setPointerType 스킵: %s" % e)
dp.setColor(Vec(1.0, 0.35, 0.2))
dp.setApparentSize(5.0)
dp.setPosition(Vec(0.0, 30.0, 0.0))             # 남쪽 낮은 곳에서 등장
dp.setPointerIntensity(1.0, Anim(1.0))
t1.setText("포인터를 따라가 보세요 — 오리온자리"); t1.setIntensity(1.0, Anim(0.8))
sleep(1.5)
dp.setHeight(85.0, Anim.cubic(3.0))             # 오리온 위치(돔 중앙 부근)로 상승
sleep(3.5)
# 서클링: h=85 고정, az 한 바퀴 = 돔 중앙(오리온) 주위 반경 5° 원
for i in range(13):
    dp.setAzimuth(360.0 * i / 12.0, Anim(0.55))
    sleep(0.6)
sleep(0.5)

# ══════════════════════════════════════════════════════════════
# ④ 오리온 — 선, 라벨, 그리고 그림
# ══════════════════════════════════════════════════════════════
print(">>> ④ 오리온 선/라벨/아트")
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.8, Anim(2.0))
ori.setLabelIntensity(0.6, Anim(2.0))
sleep(3.0)
t1.setText("사냥꾼 오리온 — 그리스의 하늘 그림")
ori.setArtIntensity(0.9, Anim(3.0))
sleep(8.0)
ori.setArtIntensity(0.0, Anim(2.0))
sleep(2.0)
dp.setPointerIntensity(0.0, Anim(1.5))          # 포인터 퇴장 (선은 다음 장면용으로 유지)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# ⑤ 고유운동 — 5만 년 시간여행 (저속·벡터 없음, 선이 함께 일그러짐)
# ══════════════════════════════════════════════════════════════
print(">>> ⑤ 고유운동 +50,000년/20초")
t1.setText("50,000년 후 — 별자리는 영원하지 않다"); t1.setIntensity(1.0, Anim(0.8))
st.setProperMotion(True)
sleep(1.0)
st.setProperMotionOffsetInYears(50000.0, Anim(20.0))
sleep(20.5)
t1.setText("그리고 다시, 오늘 밤의 하늘로")
st.setProperMotionOffsetInYears(0.0, Anim(6.0))
sleep(6.5)
st.setProperMotion(False)
sleep(1.0)

# ══════════════════════════════════════════════════════════════
# 피날레
# ══════════════════════════════════════════════════════════════
print(">>> 피날레")
ori.setLinesIntensity(0.0, Anim(2.0))
ori.setLabelIntensity(0.0, Anim(2.0))
t1.setText("밤하늘 가이드 투어 — 끝")
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("쇼 종료 (총 약 2분 40초).")

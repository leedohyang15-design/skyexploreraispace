# -*- coding: utf-8 -*-
"""
night_guide_tour_v2.py — v1 실패 3건 집중 수정 (2026-07-07)
v1 실측 결과: 반짝임 ✅ / 별자리 아트 ✅ / 고유운동 동작 ✅(어지러움) /
             그리드 ❌(안 보임) / 포인터 ❌(오리온 조준 실패, 중앙 기준 왕복만)

이번 v2 수정 3건:
 ① Mark 그리드 — v1 프로브로 원인 확정: 빈 슬롯은 posType/repType/radius/카운트가 전부 0/Invalid.
    → (A) 시스템 프리셋 Mark051_WelcomeGrid 를 켜고 파라미터 덤프('정답 레시피' 채굴)
      (B) Mark001 을 수동 풀구성(InfiniteGrid + GraduatedGridWithText)으로 직접 그리기
 ② DomePointer — 좌표 매핑 캘리브레이션: az 0/90/180/-90 + 높이 스윕을 자막과 함께.
    각 정지점에서 화면 어디에 있는지 리포트해주면 매핑 공식을 확정할 수 있음.
 ③ 고유운동 — 모션 벡터 OFF + 속도 절반(+5만 년/20초 = 2,500년/초)으로 멀미 완화.
    오리온 선 ON 유지 — "선이 별을 따라 일그러지는가?"가 관찰 포인트.

무대는 v1 과 동일: 청주 2026-01-15 23:00 KST, 남쪽에 오리온.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def dump_mark(tag, m):
    """Mark 파라미터 전체 덤프 — 프리셋 해부용"""
    try:
        print("[MARK-%s] posType=%s repType=%s radius=%s lineWidth=%s" %
              (tag, m.positionType, m.representationType, m.radius, m.lineWidth))
        print("[MARK-%s] meridian=%s(grad %s/sub %s) parallel=%s(grad %s/sub %s)" %
              (tag, m.meridianCount, m.meridianGraduationCount, m.meridianSubGraduationCount,
               m.parallelCount, m.parallelGraduationCount, m.parallelSubGraduationCount))
        print("[MARK-%s] az[%s~%s] h[%s~%s] gradSize=%s subGradSize=%s textSize=%s" %
              (tag, m.minAzimuth, m.maxAzimuth, m.minHeight, m.maxHeight,
               m.graduationSize, m.subGraduationSize, m.textSize))
        print("[MARK-%s] parent=%s textOriMode=%s intensity=%.2f" %
              (tag, m.parent, m.textOrientationMode, m.intensity))
    except Exception as e:
        print("[MARK-%s] 덤프 실패: %s" % (tag, e))


# ══════════════════════════════════════════════════════════════
# 무대: 청주 겨울밤 (v1 과 동일)
# ══════════════════════════════════════════════════════════════
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

# 오리온 기준선 — 포인터 캘리브레이션의 참조물
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.8, Anim(1.5))
ori.setLabelIntensity(0.6, Anim(1.5))
sleep(2.0)


# ══════════════════════════════════════════════════════════════
# ACT A — Mark 그리드 재도전
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT A-1: 프리셋 Mark051_WelcomeGrid 해부 (정답 레시피 채굴)")
print("=" * 60)
try:
    wg = Mark(Mark.MarkName.Mark051_WelcomeGrid)
    print("   WelcomeGrid id=%s" % wg.id)
    dump_mark("PRESET", wg)                      # ★ 이 덤프가 이번 실행 최대 수확
    t1.setText("[A-1] 프리셋 WelcomeGrid — 보이나요?"); t1.setIntensity(1.0, Anim(0.5))
    wg.setIntensity(0.8, Anim(2.0))
    sleep(7.0)
    wg.setIntensity(0.0, Anim(1.5))
    sleep(1.5)
    t1.setIntensity(0.0, Anim(0.5))
except Exception as e:
    print("   WelcomeGrid 실패: %s" % e)

print("=" * 60)
print("ACT A-2: Mark001 수동 풀구성 (v1 원인 = 빈 슬롯이라 기하 없음)")
print("=" * 60)
try:
    mk = Mark(Mark.MarkName.Mark001)
    mk.setPositionType(Mark.PositionType.InfiniteGrid)           # 하늘 전체 그리드
    mk.setRepresentationType(Mark.RepresentationType.GraduatedGridWithText)
    mk.setMinAzimuth(0.0);   mk.setMaxAzimuth(360.0)
    mk.setMinHeight(0.0);    mk.setMaxHeight(90.0)
    mk.setMeridianCount(12)                                      # 자오선 30° 간격
    mk.setParallelCount(9)                                       # 고도선 10° 간격
    mk.setMeridianGraduationCount(9)
    mk.setParallelGraduationCount(12)
    mk.setGraduationSize(1.0)
    mk.setSubGraduationSize(0.5)
    mk.setTextSize(1.0)                                          # 단위 미상 — 프리셋 덤프와 대조!
    mk.setRadius(100.0)                                          # Infinite 에선 무의미할 수도
    mk.setLineWidth(1.5)
    mk.setColor(Vec(0.3, 0.7, 1.0))
    mk.setTextColor(Vec(0.6, 0.85, 1.0))
    mk.setTextOrientationMode(Mark.TextOrientationMode.Zenith)
    dump_mark("MANUAL", mk)
    t1.setText("[A-2] 수동 구성 그리드 — 보이나요?"); t1.setIntensity(1.0, Anim(0.5))
    mk.setIntensity(0.8, Anim(2.0))
    sleep(8.0)
    mk.setIntensity(0.0, Anim(1.5))
    sleep(1.5)
    t1.setIntensity(0.0, Anim(0.5))
except Exception as e:
    print("   Mark001 수동 구성 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT B — DomePointer 좌표 캘리브레이션
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT B: 포인터 캘리브레이션 — 각 정지점의 화면 위치를 리포트해줘!")
print("=" * 60)
try:
    dp = DomePointer(DomePointer.DomePointerName.DomePointer001)
    try:
        dp.setPointerType(Body.PointerType.Model1Bold)
    except Exception as e:
        print("   setPointerType 스킵: %s" % e)
    dp.setColor(Vec(1.0, 0.35, 0.2))
    dp.setApparentSize(5.0)
    dp.setPosition(Vec(0.0, 30.0, 0.0))
    dp.setPointerIntensity(1.0, Anim(1.0))
    sleep(1.5)

    stops = [(0.0,   "az=0, h=30    ← 어느 방향? (남쪽 지평선 위라면 az0=조준방향)"),
             (90.0,  "az=90, h=30   ← 왼쪽? 오른쪽?"),
             (180.0, "az=180, h=30  ← 등 뒤(북쪽)?"),
             (-90.0, "az=-90, h=30")]
    for az, memo in stops:
        t1.setText("[B] 포인터 %s" % memo.split("←")[0].strip()); t1.setIntensity(1.0, Anim(0.3))
        dp.setAzimuth(az, Anim.cubic(2.0))
        print("   포인터 → %s" % memo)
        sleep(4.0)

    print("   높이 스윕: az=0 고정, h 30→85 (85=돔 꼭대기 근처?)")
    t1.setText("[B] 높이 스윕 h 30 → 85")
    dp.setAzimuth(0.0, Anim(1.0)); sleep(1.2)
    dp.setHeight(85.0, Anim.cubic(4.0))
    sleep(5.0)
    print("   ★ 오리온(삼태성)에 가장 가까웠던 정지점이 어디였는지 리포트!")
    dp.setPointerIntensity(0.0, Anim(1.0))
    sleep(1.0)
    t1.setIntensity(0.0, Anim(0.5))
except Exception as e:
    print("   DomePointer 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT C — 고유운동 순한맛: 벡터 OFF + 속도 절반
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT C: 고유운동 +50,000년 / 20초 (벡터 없음)")
print("=" * 60)
try:
    t1.setText("50,000년 후 — 오리온이 천천히 일그러진다"); t1.setIntensity(1.0, Anim(0.8))
    st.setProperMotion(True)                     # 벡터는 켜지 않음 (v1 멀미 원인 후보 제거)
    sleep(1.0)
    st.setProperMotionOffsetInYears(50000.0, Anim(20.0))
    for i in range(6):
        sleep(3.0)
        try:
            print("   offsetYears=%.0f" % st.properMotionOffsetInYears)
        except Exception:
            pass
    sleep(2.5)
    print("   ★ 관찰: ①어지러움이 줄었나 ②오리온 '선'이 별을 따라 움직였나(선도 일그러짐?)")
    t1.setText("다시 오늘 밤으로")
    st.setProperMotionOffsetInYears(0.0, Anim(6.0))
    sleep(6.5)
    st.setProperMotion(False)
except Exception as e:
    print("   고유운동 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# 피날레
# ══════════════════════════════════════════════════════════════
ori.setLinesIntensity(0.0, Anim(1.5))
ori.setLabelIntensity(0.0, Anim(1.5))
t1.setText("v2 끝 — [MARK-PRESET] 덤프와 포인터 위치 리포트 부탁!")
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("v2 종료.")

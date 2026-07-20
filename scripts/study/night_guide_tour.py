# -*- coding: utf-8 -*-
"""
night_guide_tour.py — 미연습 API 실측 예제 v1 (2026-07-07)
"밤하늘 가이드 투어": 해설자가 그리드를 띄우고, 포인터로 별자리를 가리키고,
별자리 그림을 보여준 뒤, 10만 년 시간여행으로 별들의 고유운동을 보여주는 쇼.

★ 이번에 처음 연습하는 API (core_api_reference.txt 로 시그니처 확인 완료):
 ① Mark            — 좌표 그리드/눈금 원. ⚠️ 생성 enum 이 레퍼런스에 없음 → dir() 프로브로 탐색!
 ② DomePointer     — 돔 화면 좌표 포인터(레이저). DomePointer001~010, Body.PointerType.Model1~10(Bold)
 ③ Constellation.setArtIntensity — 별자리 그림(아트). 선/라벨은 연습했지만 아트는 처음.
 ④ Stars 고급      — setTwinklingAmplitude(반짝임), setProperMotion+setProperMotionOffsetInYears(고유운동),
                     setMotionVectorIntensity(별 이동 궤적 벡터)

무대: 청주(36.64, 127.49) 2026-01-15 23:00 KST = 14:00 UT — 오리온이 남쪽 하늘 정중앙(방위≈180, 고도≈55).
조준: Sky View 확정 레버 = setTargetHeight(30) + setOrientationH(180-방위=0).

⚠️ 실측 확인 포인트 (실행 후 콘솔/화면 리포트 부탁):
 - [PROBE] 줄들: Mark 의 생성 enum 멤버 이름 (이게 이번 실험의 핵심 수확!)
 - DomePointer 위치 (0, 50) 이 화면 어디에 찍히는지 — 오리온과의 상대 위치
 - 고유운동 타임랩스 때 별자리 '선'이 별을 따라 일그러지는지, 선은 그대로인지
"""

from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone      # 실측: UTC 로 해석됨


def probe(title, obj):
    """dir() 프로브 — 실행 로그가 곧 API 지도"""
    try:
        members = [m for m in dir(obj) if not m.startswith("_")]
        print("[PROBE] %s (%d개): %s" % (title, len(members), ", ".join(members)))
        return members
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e))
        return []


# ══════════════════════════════════════════════════════════════
# ACT 0 — 프로브: Mark 생성 enum 을 모른다 → dir() 로 찾는다
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 0: API 프로브 (Mark / DomePointer / Stars)")
print("=" * 60)

mark_members = probe("Mark 클래스", Mark)
mark = None
try:
    # 관례상 '...Name' 으로 끝나는 중첩 enum 이 생성자 인자 (Nebula.NebulaName 패턴)
    name_enums = [m for m in mark_members if m.lower().endswith("name") and m != "name"]
    print("[PROBE] Mark 의 Name 계열 enum 후보: %s" % name_enums)
    for ne in name_enums:
        enum_cls = getattr(Mark, ne)
        vals = probe("Mark.%s 멤버" % ne, enum_cls)
        # Invalid/Count 를 뺀 첫 실멤버로 생성 시도 (id=-1 이면 null — Nebula 실측 교훈)
        for v in vals:
            if "Invalid" in v or "Count" in v:
                continue
            try:
                cand = Mark(getattr(enum_cls, v))
                print("[PROBE] Mark(%s.%s) → id=%s" % (ne, v, cand.id))
                if cand.id != -1:
                    mark = cand
                    break
            except Exception as e:
                print("[PROBE] Mark(%s.%s) 생성 실패: %s" % (ne, v, e))
        if mark is not None:
            break
except Exception as e:
    print("[PROBE] Mark 탐색 전체 실패: %s" % e)

if mark is not None:
    # 하위 enum 도 지도에 추가 (PositionType / RepresentationType — 멤버 미확인)
    for sub in ("PositionType", "RepresentationType", "TextOrientationMode"):
        if sub in mark_members:
            probe("Mark.%s" % sub, getattr(Mark, sub))
    try:
        print("[PROBE] Mark 기본값: intensity=%.2f radius=%s meridian=%s parallel=%s posType=%s repType=%s"
              % (mark.intensity, mark.radius, mark.meridianCount, mark.parallelCount,
                 mark.positionType, mark.representationType))
    except Exception as e:
        print("[PROBE] Mark 기본값 읽기 실패: %s" % e)

# Stars 고급 속성 기본값 (복구용으로 반드시 원본을 읽어둠 — setScale 사고의 교훈)
try:
    tw0 = st.twinklingAmplitude
    print("[PROBE] Stars: twinklingAmplitude=%.3f isTwinklingActive=%s properMotion=%s offsetYears=%.1f"
          % (tw0, st.isTwinklingActive, st.properMotion, st.properMotionOffsetInYears))
except Exception as e:
    tw0 = 1.0
    print("[PROBE] Stars 속성 읽기 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT 1 — 무대: 청주 겨울밤 (지상 씬 체크리스트 전부)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 1: 청주 겨울밤 세팅 (2026-01-15 23:00 KST)")
print("=" * 60)

uni.setGlobalIntensity(0.0, Anim(0.0))          # 암전 먼저 (FadeTo 안 쓰므로 클램프 루프 불필요)
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))          # reset 이 gi 를 되살릴 수 있어 재암전

earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))              # ★ 지상 마스터 스위치 (꺼지면 대기까지 통째 꺼짐)
earth.setAtmosphereIntensity(1.0, Anim(0.0))    # 밤이라 대기 ON 이어도 별 보임 (자연스러운 지평선)
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))     # 청주
dm.stop(); sleep(0.3)                            # ★ 순서: stop → setDateTime (실측 함정)
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))   # 14 UT = 23시 KST — 오리온 남중
sleep(1.0)

cam.setTargetHeight(30.0, Anim(0.0))            # 🎯 관람 표준 틸트 30
cam.setOrientationH(0.0, Anim(0.0))             # H = 180 - 오리온 방위(180) = 0 → 남쪽 조준
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setText("밤하늘 가이드 투어 — 청주, 1월의 밤")
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0))                  # ★ 지상 자막 = size 0.035 + distance 1.0 (v19/v21 확정)
t1.setColor(Vec(0.8, 0.9, 1.0))

uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setIntensity(1.0, Anim(1.5))
print(">>> 페이드인 — 남쪽 하늘에 오리온 (6초 감상)")
sleep(6.0)
t1.setIntensity(0.0, Anim(0.8))


# ══════════════════════════════════════════════════════════════
# ACT 2 — 반짝임: setTwinklingAmplitude (신규 ①)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 2: 별 반짝임 증폭 (setTwinklingAmplitude %.2f → 3.0)" % tw0)
print("=" * 60)
try:
    t1.setText("별이 반짝이는 이유 — 대기의 일렁임"); t1.setIntensity(1.0, Anim(0.8))
    st.setTwinklingAmplitude(3.0, Anim(2.0))    # 범위 미확인 — 3.0 체감 여부가 실측 포인트
    sleep(6.0)
    st.setTwinklingAmplitude(tw0, Anim(2.0))    # ★ 복구는 읽어둔 원본값 (1.0 하드코딩 금지)
    sleep(2.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   반짝임 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT 3 — Mark 그리드 (신규 ②): 프로브로 찾은 개체를 화면에
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 3: Mark 좌표 그리드")
print("=" * 60)
if mark is not None:
    try:
        t1.setText("하늘의 주소 — 방위와 고도"); t1.setIntensity(1.0, Anim(0.8))
        mark.setColor(Vec(0.3, 0.7, 1.0))
        mark.setTextColor(Vec(0.6, 0.85, 1.0))
        mark.setLineWidth(1.5)
        mark.setIntensity(0.7, Anim(2.5))       # 그리드 페이드인
        print("   그리드 ON (8초) — 화면에 눈금 원/자오선이 보이는지 확인!")
        sleep(8.0)
        mark.setIntensity(0.0, Anim(2.0))
        sleep(2.0)
        t1.setIntensity(0.0, Anim(0.8))
    except Exception as e:
        print("   Mark 조작 실패: %s" % e)
else:
    print("   Mark 생성 실패 → 스킵 (PROBE 로그로 enum 이름 확인 후 v2 에서 재도전)")


# ══════════════════════════════════════════════════════════════
# ACT 4 — DomePointer (신규 ③): 포인터로 오리온 가리키기
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 4: 돔 포인터 — 오리온 서클링")
print("=" * 60)
dp = None
try:
    dp = DomePointer(DomePointer.DomePointerName.DomePointer001)
    print("   DomePointer001 id=%s" % dp.id)
    try:
        dp.setPointerType(Body.PointerType.Model1Bold)   # Body 가 import 안 됐으면 except 로
    except Exception as e:
        print("   setPointerType 스킵: %s" % e)
    dp.setColor(Vec(1.0, 0.35, 0.2))
    dp.setApparentSize(4.0)
    dp.setPosition(Vec(0.0, 80.0, 0.0))         # 천정 근처에서 등장
    dp.setPointerIntensity(1.0, Anim(1.0))
    t1.setText("포인터를 따라가 보세요 — 오리온자리"); t1.setIntensity(1.0, Anim(0.8))
    sleep(1.5)

    # 오리온 위치(화면좌표 실험): az 0 = 조준 방향(남쪽) 가정, 고도 50 으로 하강
    dp.setPosition(Vec(0.0, 50.0, 0.0), Anim.cubic(3.0))
    sleep(3.5)
    print("   ★ 확인: 포인터 (az0, h50) 가 오리온 근처인가? (화면좌표↔하늘좌표 관계 실측)")

    # 반지름 6° 원 그리기 — 별자리 서클링 (12스텝)
    for i in range(13):
        th = 2.0 * math.pi * i / 12.0
        dp.setAzimuth(6.0 * math.sin(th), Anim(0.45))
        dp.setHeight(50.0 + 6.0 * math.cos(th), Anim(0.45))
        sleep(0.5)
    sleep(0.5)
except Exception as e:
    print("   DomePointer 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT 5 — 별자리 아트 (신규 ④): setArtIntensity
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 5: 오리온 — 선, 그리고 그림(아트)")
print("=" * 60)
ori = Constellation(Constellation.ConstellationName.Ori)
try:
    ori.setLinesIntensity(0.8, Anim(2.0))
    ori.setLabelIntensity(0.6, Anim(2.0))
    sleep(3.0)
    t1.setText("사냥꾼 오리온 — 그리스의 하늘 그림")
    ori.setArtIntensity(0.9, Anim(3.0))         # ★ 처음 써보는 아트 — 그림이 뜨는지 확인!
    print("   아트 페이드인 (8초 감상)")
    sleep(8.0)
    ori.setArtIntensity(0.0, Anim(2.0))
    sleep(2.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   별자리 아트 실패: %s" % e)
if dp is not None:
    try:
        dp.setPointerIntensity(0.0, Anim(1.5))  # 포인터 퇴장
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
# ACT 6 — 고유운동 10만 년 타임랩스 (신규 ⑤): 별자리는 영원하지 않다
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 6: 고유운동 — 10만 년 후의 오리온")
print("=" * 60)
try:
    t1.setText("100,000년 후 — 별자리는 영원하지 않다"); t1.setIntensity(1.0, Anim(0.8))
    st.setProperMotion(True)
    st.setMotionVectorIntensity(0.7, Anim(2.0))     # 별 이동 궤적 벡터 (신규 — 보이는지 확인)
    sleep(2.0)
    print("   +100,000년 진행 (15초) — 오리온 선이 별을 따라오는지 관찰!")
    st.setProperMotionOffsetInYears(100000.0, Anim(15.0))
    for i in range(5):                               # 텔레메트리 3초 간격
        sleep(3.0)
        try:
            print("   offsetYears=%.0f" % st.properMotionOffsetInYears)
        except Exception:
            pass
    sleep(2.0)
    print("   현재로 복귀 (8초)")
    t1.setText("그리고 다시, 오늘 밤의 하늘로")
    st.setProperMotionOffsetInYears(0.0, Anim(8.0))
    sleep(8.5)
    st.setMotionVectorIntensity(0.0, Anim(2.0))
    st.setProperMotion(False)
    sleep(2.0)
except Exception as e:
    print("   고유운동 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# 피날레 — 정리 + 페이드아웃
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("피날레")
print("=" * 60)
try:
    ori.setLinesIntensity(0.0, Anim(2.0))
    ori.setLabelIntensity(0.0, Anim(2.0))
except Exception:
    pass
t1.setText("밤하늘 가이드 투어 — 끝"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("쇼 종료. [PROBE] 줄들과 각 ACT 체감 리포트 부탁!")

# -*- coding: utf-8 -*-
"""
comet_halley_complete.py — 핼리 혜성 완성쇼 (2026-07-09, 사용자 3확인 반영)
처음 만든 comet_halley.py(조망→궤도→시간가속) 구조에, 6판까지의 실측을 전부 적용한 결정판.

확정 지식 (전부 실측):
 · 궤도선은 지상(지구 하늘) 시점에서만 렌더 → 궤도 조망은 지상에서.
 · 슬롯 혜성(Comet001) 궤도 6요소: 모델 먼저 → 요소 → 프레임 대기(sleep). 날짜는 근일점 근처
   (2024는 원일점이라 본체 안 보임). 모델 Halley3D(코마 렌더 확인).
 · 혜성 클로즈업+시간가속 = DB FadeTo → 'Std Ecliptic J2000' 프레임(자전 없음):
   setPositionR(읽은값×배율, -1)로 당기고, 그 프레임서 시간가속하면 부드럽게 근일점 통과.

3막 구성:
 [1] 지상 궤도 조망 — 긴 타원 궤도 + 혜성 + 기하 해설
 [2] 혜성 클로즈업 — FadeTo 로 혜성 곁, 더 당겨 확대
 [3] 근일점 통과 — 황도 프레임 시간가속(2061-03→09), 꼬리 성장
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# DB 핸들 선확보 (여행 중 조회 None 방지)
halley_db = None
try:
    halley_db = DataManager.database().data(Data.Type.CometType, "1P/Halley")
except Exception as e:
    print("   DB 핸들 실패: %s" % e)

# ── 무대: 지상 하늘, 2061-03 (근일점 전 — 혜성 활동적) ─────────
print("무대: 지상 하늘 / 2061-03")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(0.8, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2061, 3, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 76년 주기의 방문자"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# [1] 지상 궤도 조망 (슬롯 혜성 — 모델 먼저 → 요소 → 대기)
# ══════════════════════════════════════════════════════════════
print("[1] 궤도 조망")
comet = Comet(Comet.CometName.Comet001)
try:
    comet.setStandardModelName(Comet.CometModelSet.Halley3D)
except Exception:
    comet.setStandardModelName(Comet.CometModelSet.Basic)
comet.setModelScale(30.0)
comet.setIntensity(1.0, Anim(0.0))
sleep(0.3)
comet.setEccentricity(0.967, Anim(0.0))
comet.setInclination(162.3, Anim(0.0))
comet.setLongitudeOfAscendingNode(58.42, Anim(0.0))
comet.setArgumentOfPeriapsis(111.33, Anim(0.0))
comet.setDistanceToPeriapsis(0.586, Anim(0.0))
comet.setTimeOfLastPeriapsis(2446470.5, Anim(0.0))
comet.setLabelNameOverride("1P/Halley")
sleep(0.3)
t1.setText("긴 타원 궤도 — 태양을 초점으로"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.5))
comet.setLabelIntensity(0.8, Anim(2.0))
try:
    comet.setPointerType(Body.PointerType.Model2Bold)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception:
    pass
sleep(6.0)
for text, dur in [
    ("이심률 0.97 — 극단적으로 긴 타원", 4.5),
    ("궤도 경사 162° — 행성과 반대로 도는 역행", 4.5),
    ("근일점 0.59 AU · 원일점은 해왕성 너머", 4.5),
]:
    t1.setText(text); t1.setIntensity(1.0, Anim(0.6))
    sleep(dur)
    t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

# ══════════════════════════════════════════════════════════════
# [2] 혜성 클로즈업 (DB FadeTo → 당기기)
# ══════════════════════════════════════════════════════════════
print("[2] 혜성 클로즈업")
if halley_db is not None:
    act = halley_db.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("혜성 곁으로 다가간다"); t1.setIntensity(1.0, Anim(0.8))
        comet.setPointerIntensity(0.0, Anim(0.5))
        act.trigger()
        sleep(6.0)                                  # 혜성 프레임 안착
        # 더 당기기 (Std Ecliptic 프레임 R 애니, track=-1)
        try:
            p = cam.positionLBR
            print("   FadeTo 후 R=%.3f AU → 당기기" % p.z)
            t1.setText("코마와 꼬리 — 얼음이 태양빛에 증발한다")
            cam.setPositionR(p.z * 0.45, Anim.cubic(5.0), -1)
            sleep(6.0)
        except Exception as e:
            print("   당기기 실패: %s" % e)
        t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)
    else:
        print("   FadeTo 미지원")

# ══════════════════════════════════════════════════════════════
# [3] 근일점 통과 (황도 프레임 시간가속 — 자전 없이 부드럽게)
# ══════════════════════════════════════════════════════════════
print("[3] 근일점 통과 시간가속")
try:
    t1.setText("시간을 빠르게 — 2061년 7월, 근일점"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2061, 9, 1, 0, 0, 0, tz, Anim(22.0))   # 6개월을 22초에
    for i in range(4):
        sleep(5.5)
        try:
            print("   JD=%.1f R=%.3f" % (dm.julianDate, cam.positionLBR.z))
        except Exception:
            pass
    t1.setText("태양을 스치고 — 꼬리는 늘 태양 반대편으로")
    sleep(4.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   시간가속 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 다음 만남은 2061년"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 3막: 궤도 조망 → 클로즈업 → 근일점 통과 시간가속. 완성?")

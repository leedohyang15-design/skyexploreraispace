# -*- coding: utf-8 -*-
"""
comet_halley_show5.py — 궤도 조망 → 혜성 클로즈업 (2026-07-09)
show4 실측(스크린샷): Halley3D 혜성이 궤도선 근처에 '뿌연 덩어리'로 떴음(3D 모델 렌더 성공!).
단 전천 시점이라 작게 보임. 지상 Sky View 는 setZoomFov 무효 → 그 자리 확대 불가.
→ 혜성을 크게 = **DB 1P/Halley 로 FadeTo(혜성 곁으로 근접 프레이밍)**.

2단 구성:
 [1] 지상 하늘: 슬롯 혜성(Comet001)으로 궤도선+본체 조망 (전체 궤도 이해).
 [2] 혜성 클로즈업: DB 1P/Halley FadeTo → 혜성이 화면 가득(궤도선은 전환 중 사라짐 — 정상).

날짜 2061-04(근일점 근처, 혜성 활동적). 모델 먼저(확정 순서).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# DB 핸들은 미리 확보 (여행 중 조회 None 방지 — 여행 데모 교훈)
halley_db = None
try:
    halley_db = DataManager.database().data(Data.Type.CometType, "1P/Halley")
    print("   DB 1P/Halley 핸들 확보=%s" % (halley_db is not None))
except Exception as e:
    print("   DB 핸들 실패: %s" % e)

# ── 무대 ──────────────────────────────────────────────────────
print("무대: 지상 하늘 / 2061-04")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(0.7, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2061, 4, 20, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 2061년의 귀환"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# [1] 궤도 조망 (슬롯 혜성)
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
t1.setText("긴 타원 궤도 — 76년의 여정"); t1.setIntensity(1.0, Anim(0.8))
comet.setOrbitThickness(2.0)
comet.setOrbitIntensity(0.9, Anim(2.5))
comet.setLabelIntensity(0.8, Anim(2.0))
try:
    comet.setPointerType(Body.PointerType.Model2Bold)
    comet.setPointerIntensity(1.0, Anim(1.5))
except Exception:
    pass
print(">>> 궤도 조망 (7초)")
sleep(7.0)
t1.setText("이심률 0.97 · 역행 162° · 근일점 0.59 AU")
sleep(4.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.8)

# ══════════════════════════════════════════════════════════════
# [2] 혜성 클로즈업 (DB FadeTo — 혜성 곁으로)
# ══════════════════════════════════════════════════════════════
print("[2] 혜성 클로즈업 (DB FadeTo)")
if halley_db is not None:
    try:
        act = halley_db.action(Action.Type.FadeTo)
        if act is not None:
            t1.setText("혜성에 다가간다 — 코마와 꼬리"); t1.setIntensity(1.0, Anim(0.8))
            sleep(1.5)
            comet.setPointerIntensity(0.0, Anim(0.5))   # 슬롯 포인터 정리
            act.trigger()
            print("   1P/Halley FadeTo → 근접 프레이밍 (7초)")
            sleep(7.0)
            print("   ★ 혜성 본체가 화면 가득 크게 보이나? (코마/꼬리?)")
            t1.setText("태양풍에 밀려 태양 반대로 뻗는 꼬리")
            sleep(5.0)
            t1.setIntensity(0.0, Anim(0.8))
        else:
            print("   FadeTo 액션 미지원")
    except Exception as e:
        print("   FadeTo 실패: %s" % e)
else:
    print("   DB 핸들 없음 → 클로즈업 스킵")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 다음 만남은 2061년"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: [1] 궤도 조망 OK? [2] FadeTo 클로즈업서 혜성이 크게(꼬리?) 보였나?")

# -*- coding: utf-8 -*-
"""
comet_halley_show6.py — 혜성 프레임에서 당겨보고 + 시간가속 (2026-07-09)
show5 스크린샷: FadeTo 로 "Comet 6, Std Ecliptic J2000" 프레임(R=6.68 AU) 진입, 코마 보임.
단 혜성이 작고 구석. 사용자 통찰: "가속은 지상/이 뷰에서 될 것 같다" → 맞음.

핵심: **FadeTo 후의 'Std Ecliptic J2000' 프레임은 황도 기준 = 지구 자전 없음** →
      이 프레임에서 시간가속하면 긴 기간도 어지럽지 않고 혜성 이동/코마 변화가 보여야 함.
      (지상 뷰 가속도 원래 됨 — cheongju_day_night/eclipse 로 증명. 어지러웠던 건 37년 극단점프 탓.)

이번 검증 2가지:
 ① FadeTo 혜성 프레임에서 '더 가까이 당기기' (setPositionR 읽은값×배율, track=-1 = 현 프레임 유지).
 ② 그 프레임에서 시간가속 (2061-03 → 2061-09, 근일점 전후 6개월) → 부드럽게 움직이나?

날짜 시작 2061-03(근일점 7/28 전). DB 핸들 선확보.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

halley_db = None
try:
    halley_db = DataManager.database().data(Data.Type.CometType, "1P/Halley")
    print("   DB 1P/Halley 핸들=%s" % (halley_db is not None))
except Exception as e:
    print("   DB 핸들 실패: %s" % e)

# ── 무대 ──────────────────────────────────────────────────────
print("무대: 2061-03 (근일점 전)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2061, 3, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.0)

# ── FadeTo 혜성 프레임 ────────────────────────────────────────
print("FadeTo 1P/Halley")
if halley_db is not None:
    act = halley_db.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("핼리 혜성 곁으로"); t1.setIntensity(1.0, Anim(1.0))
        act.trigger()
        sleep(6.0)                      # 혜성 프레임 안착 대기
        t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)
    else:
        print("   FadeTo 미지원")
else:
    print("   DB 핸들 없음 → 종료")

# ── ① 더 가까이 당기기 (혜성 프레임 R 애니, track=-1) ─────────
print("① 혜성으로 당기기 (R 읽은값×배율)")
try:
    p = cam.positionLBR
    print("   현재 R=%.3f (AU 추정)" % p.z)
    t1.setText("가까이 — 코마와 꼬리"); t1.setIntensity(1.0, Anim(0.8))
    cam.setPositionR(p.z * 0.45, Anim.cubic(5.0), -1)   # 더 가까이 (6.68→3 AU 정도)
    sleep(6.0)
    try:
        print("   당긴 후 R=%.3f" % cam.positionLBR.z)
    except Exception:
        pass
    print("   ★ 혜성이 더 커졌나?")
    sleep(1.0)
    t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)
except Exception as e:
    print("   당기기 실패: %s" % e)

# ── ② 이 프레임에서 시간가속 (근일점 전후 6개월) ─────────────
print("② 시간가속 2061-03 → 2061-09 (황도 프레임 = 자전 없음, 부드러워야)")
try:
    t1.setText("시간을 빠르게 — 근일점 통과"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2061, 9, 1, 0, 0, 0, tz, Anim(20.0))   # 6개월을 20초에
    for i in range(4):
        sleep(5.0)
        try:
            print("   JD=%.1f  R=%.3f" % (dm.julianDate, cam.positionLBR.z))
        except Exception:
            pass
    print("   ★★ 핵심: 화면이 안 돌고(황도 프레임) 혜성 코마/꼬리가 변했나? 근일점서 밝아졌나?")
    sleep(1.0)
    t1.setText("태양을 스치며 — 꼬리가 자란다")
    sleep(4.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   시간가속 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("핼리 혜성 — 2061"); t1.setIntensity(1.0, Anim(1.0))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①당겨서 커졌나 ②시간가속이 이 프레임선 부드러웠나+혜성 움직임/꼬리 변화")

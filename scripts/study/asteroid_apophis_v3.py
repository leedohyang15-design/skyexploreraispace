# -*- coding: utf-8 -*-
"""
asteroid_apophis_v3.py — FadeTo 말고 GoTo 로 날아가기 (2026-07-09)
v2 실패: 지상 Sky View 에서 setPositionLBR(소행성 포트)로 줌 시도 = 아예 안 됨.
원인: **지상 관측자 바인딩 → 위치 명령 무효** (CLAUDE.md 확정 함정). 혜성이 됐던 건
      FadeTo 로 프레임을 먼저 잡은 뒤 R 을 줄였기 때문.

★ FadeTo 아닌 '다가가는' 방법 = **GoTo** (페이드 없는 연속 비행 — 우주선 여행 연출).
   `d.action(Action.Type.GoTo).trigger()` → 현 위치에서 소행성까지 실제 비행.
   도착 후 목표 프레임에서 `setPositionR(읽은값×배율, -1)` 로 추가 줌 가능.
 ⚠️ GoTo 함정(travel 데모): ①비행 시간 가변 → 움직임→정지 폴링으로 도착 감지
   ②도착 후 Target 을 0 으로 남김 → setTargetHeight(30) 필수 ③비행 중 DB 조회 None → 핸들 선확보.

DB "Apophis" 로 GoTo. 지원 액션 먼저 확인(None 체크).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── DB 핸들 선확보 + 지원 액션 확인 ──────────────────────────
apophis = None
try:
    apophis = DataManager.database().data(Data.Type.AsteroidType, "Apophis")
    print("   DB Apophis=%s" % (apophis is not None))
    if apophis is not None:
        for an in ("GoTo", "StraightGoTo", "ConnectTo", "FadeTo"):
            try:
                a = apophis.action(getattr(Action.Type, an))
                print("   액션 %s = %s" % (an, "지원" if a is not None else "None"))
            except Exception as e:
                print("   액션 %s 조회 예외: %s" % (an, e))
except Exception as e:
    print("   DB 실패: %s" % e)

# ── 무대 (우주 여행이라 지상 체크리스트 최소) ────────────────
print("무대")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2029, 4, 10, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.85, 0.6))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("아포피스로 — FadeTo 없이 날아간다"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)


def wait_arrival(max_s=30.0):
    """R 변화(움직임)→정지 3연속 감지로 도착 판정 (출발 초반 정지 오판 방지)."""
    moved = False; still = 0; t = 0.0
    try:
        prev = cam.positionLBR.z
    except Exception:
        prev = None
    while t < max_s:
        sleep(0.5); t += 0.5
        try:
            cur = cam.positionLBR.z
        except Exception:
            continue
        if prev is not None:
            d = abs(cur - prev)
            if d > 1e-4:
                moved = True; still = 0
            elif moved:
                still += 1
                if still >= 3:
                    print("   도착 감지 (t=%.1fs, R=%.3f)" % (t, cur))
                    return cur
        prev = cur
    print("   도착 타임아웃 (%.1fs, R=%.3f)" % (t, prev if prev else -1))
    return prev

# ── GoTo 비행 ─────────────────────────────────────────────────
print("=" * 60); print("GoTo 비행 (페이드 없는 연속 접근)"); print("=" * 60)
if apophis is not None:
    act = apophis.action(Action.Type.GoTo)
    if act is None:
        act = apophis.action(Action.Type.StraightGoTo)
        print("   GoTo 미지원 → StraightGoTo 대체")
    if act is not None:
        t1.setText("비행 중 — 소행성에 접근"); t1.setIntensity(1.0, Anim(0.8))
        act.trigger()
        r = wait_arrival(30.0)
        # 도착 후: Target 재고정(GoTo 는 0 으로 남김) + 추가 줌
        try:
            cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)
        except Exception as e:
            print("   TH 스킵: %s" % e)
        t1.setText("더 가까이 — 표면으로")
        try:
            for i, factor in enumerate([0.5, 0.5]):
                p = cam.positionLBR
                cam.setPositionR(p.z * factor, Anim.cubic(5.0), -1)
                print("   추가 줌 %d: R %.3f → %.3f" % (i + 1, p.z, p.z * factor))
                sleep(5.5)
        except Exception as e:
            print("   추가 줌 실패: %s" % e)
        print("   ★ 페이드 없이 날아가서 소행성이 커졌나?")
        sleep(2.0)
        t1.setIntensity(0.0, Anim(0.8))
    else:
        print("   GoTo/StraightGoTo 둘 다 미지원")
else:
    print("   DB 핸들 없음")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("아포피스 — 2029, 지구와의 랑데부"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①GoTo 지원됐나(액션 로그) ②페이드 없이 비행하며 커졌나 ③도착 R 값")

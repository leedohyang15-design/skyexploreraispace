# -*- coding: utf-8 -*-
"""
asteroid_apophis_v5.py — ConnectTo 줌: 거리까지 끝까지 (2026-07-09)
v4 실측: ConnectTo + setPositionR = 흔들림 없이 R 매끄럽게 감소 확정(48.7M→19.5M→...→1.9M).
문제: **시작 R = 4,869만(소행성 반지름 단위) = 실제 지상→아포피스 거리**. ×0.4 ×4 로는
     아직 195만이라 여전히 까마득 → 안 커 보임. → **도킹(R≈8)까지 여러 단계 연속 줌**.

★ 해법: R 이 작아질 때까지 반복하는 '적응형 지오메트릭 줌'. 각 단계 ×0.16, R<12 되면 정지.
   4,869만 → 8 은 ×0.16 로 약 9단계 = 30초 연속 접근(멀리서 소행성까지 쭉).
   ✅ ConnectTo+setPositionR 정석(읽은값×배율, track=-1)이 초대형 범위서도 매끄러움 = 확정.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

apophis = None
try:
    apophis = DataManager.database().data(Data.Type.AsteroidType, "Apophis")
    print("   DB Apophis=%s" % (apophis is not None))
except Exception as e:
    print("   DB 실패: %s" % e)

# ── 무대 ──────────────────────────────────────────────────────
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
t1.setText("아포피스 — 4,800만 반지름 밖에서 출발"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ConnectTo (암전 속) ──────────────────────────────────────
print("=" * 60); print("ConnectTo → 도킹까지 연속 줌"); print("=" * 60)
if apophis is not None:
    act = apophis.action(Action.Type.ConnectTo)
    if act is not None:
        uni.setGlobalIntensity(0.0, Anim(0.8)); sleep(1.0)
        act.trigger()
        sleep(1.5)
        try:
            cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.3)
        except Exception:
            pass
        try:
            print("   ConnectTo 후 R=%.1f" % cam.positionLBR.z)
        except Exception:
            pass
        uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

        # ── 적응형 지오메트릭 줌: R<12 될 때까지 ×0.16 ────────
        t1.setText("다가간다 — 흔들림 없이, 계속"); t1.setIntensity(1.0, Anim(0.8))
        # ⚠️ Recording9 해독: cubic 스텝은 매 경계서 가감속 → '끊김'. 선형+잘게 = 매끄러움.
        target_R = 8.0
        step = 0
        try:
            p = cam.positionLBR.z
            while p > target_R * 1.2 and step < 40:
                newR = max(p * 0.55, target_R)      # ★ 큰 비율(0.55)=작은 스텝 + 선형
                cam.setPositionR(newR, Anim(1.2), -1)  # ★ Anim(선형), 짧게 → 경계 끊김 최소
                sleep(1.25)
                p = cam.positionLBR.z
                step += 1
            print("   ★ 도킹 근처 R=%.2f (%d단계). 매끄러운가?" % (p, step))
        except Exception as e:
            print("   줌 루프 실패: %s" % e)
        t1.setText("아포피스 — 지름 340 m 의 돌덩이")
        sleep(4.0)
        t1.setIntensity(0.0, Anim(0.8))
    else:
        print("   ConnectTo 미지원")
else:
    print("   DB 핸들 없음")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("아포피스 — 2029, 지구와의 랑데부"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①몇 단계에 도킹(R) 도달 ②멀리서 소행성까지 매끄럽게 커졌나 ③최종 형체")

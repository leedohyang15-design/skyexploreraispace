# -*- coding: utf-8 -*-
"""
asteroid_apophis_v4.py — 흔들림 없는 줌인: ConnectTo + R 애니 (2026-07-09)
v3 실측: GoTo 동작하나 '중간에 한 번 흔들림' = GoTo 내장 '비행 중 자세 회전'(제거 불가, docs/16).
사용자: 흔들림 없이. → **ConnectTo** (v3 로그서 지원 확인!).

★ ConnectTo = 비행 없이 카메라 프레임만 대상 트랙으로 전환 (순간, 자세 회전 無 = 흔들림 없음).
   전환 자체는 순간이라 짧은 암전으로 감추고, **보이는 부분은 setPositionR 연속 줌만** →
   페이드-순간이동(FadeTo)과 달리 '다가가는' 줌은 온전히 보임. GoTo 와 달리 중간 회전 없음.
 절차: ① 짧은 암전 ② ConnectTo 트리거 + Target 정리 ③ 페이드인 ④ R 읽고 ×배율로 연속 줌.
 ⚠️ CLAUDE.md 경고: 'ConnectTo 후 수동 R 하강이 느린 드리프트'였던 전례 있음 → 이번에 재검증.
   (그땐 절대값/기하 하강이었을 수 있음. 이번은 읽은값×배율, track=-1 정석으로.)
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
t1.setText("아포피스 — 흔들림 없이 다가간다"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ConnectTo (프레임 전환, 비행 없음) → 암전 속에서 ─────────
print("=" * 60); print("ConnectTo 프레임 전환"); print("=" * 60)
if apophis is not None:
    act = apophis.action(Action.Type.ConnectTo)
    if act is not None:
        uni.setGlobalIntensity(0.0, Anim(0.8)); sleep(1.0)   # 짧은 암전(순간 전환 감춤)
        act.trigger()
        sleep(1.5)
        try:
            cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.3)
        except Exception as e:
            print("   TH 스킵: %s" % e)
        try:
            r0 = cam.positionLBR.z
            print("   ConnectTo 후 R=%.3f" % r0)
        except Exception:
            r0 = None
        uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

        # ── 연속 줌 (읽은값×배율, track=-1) — 흔들림 없어야 ─────
        t1.setText("다가간다 — 페이드도 흔들림도 없이"); t1.setIntensity(1.0, Anim(0.8))
        try:
            for i, factor in enumerate([0.4, 0.4, 0.5, 0.5]):
                p = cam.positionLBR
                cam.setPositionR(p.z * factor, Anim.cubic(5.0), -1)
                print("   줌 %d: R %.3f → %.3f" % (i + 1, p.z, p.z * factor))
                sleep(5.5)
            print("   ★ 흔들림 없이 소행성이 점점 커졌나?")
        except Exception as e:
            print("   줌 실패: %s" % e)
        sleep(2.0)
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
print("종료. 리포트: ①ConnectTo 후 R 값 ②흔들림 없이 연속 줌 됐나(GoTo 대비) ③소행성 커졌나")

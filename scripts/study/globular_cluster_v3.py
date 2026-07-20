# -*- coding: utf-8 -*-
"""
globular_cluster_v3.py — 말머리 방식으로 성단 속 비행 (2026-07-09)
확정: AdvancedCamera 비행(zoom/takeOffOn)은 스크립트 무효(R 불변). = 죽은 길.
★ 사용자 통찰: '말머리 예제처럼' → 정답! 말머리 성운은 AdvancedCamera 가 아니라
  **성운 포트 프레임에 카메라 배치(setPositionLBR) + setPositionR 로 R 감소 = 날아듦**.
  성단도 portId(Galactic) 있으니 동일 적용. FadeTo(R=0) 대신 R 을 우리가 제어.

말머리 레시피:
 ① reset(1) 관측자 바인딩 해제 ② 성단 포트에 setPositionLBR(Vec(0,0,R_START))
 ③ setOrientationSmoothXYZR(Vec4 0, 포트) 조준 ④ setTargetHeight(30) ⑤ 암전서 페이드인
 ⑥ setPositionR(R_VIEW, Anim.cubic, 포트) = 성단 속으로 비행
R 단위 미상(성단반지름/pc 추정) → 값 넣고 로그로 확인, 필요시 조정.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

R_START = 60.0     # 멀리서 출발
R_VIEW  = 3.0      # 성단 근처(속으로)
FLY_SEC = 9.0

# ── 씬: 심우주 (관측자 바인딩 해제) ──────────────────────────
print("씬 세팅 (reset 로 바인딩 해제)")
try:
    SceneGraph().reset(1)
    sleep(2.0)
except Exception as e:
    print("   reset: %s" % e)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 1, 0, 0, 0, tz, Anim(0.0))
sleep(0.5)

gc = GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)
gc.setIntensity(1.0, Anim(0.0))
try:
    gc.setScale(8.0, Anim(0.0))          # 살짝 키워 대상 확보
except Exception:
    pass

# ── 성단 포트 프레임에 카메라 배치 (말머리 ①②③④) ──────────
gport = -1
try:
    gport = gc.portId(GlobularCluster.GlobularClusterPort.Galactic)
    print("   성단 Galactic 포트=%s" % gport)
    cam.setPositionLBR(Vec(0.0, 0.0, R_START), Anim(), gport)          # 위치
    cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), gport)  # 조준
    cam.setTargetHeight(30.0, Anim(1.0))
    sleep(1.5)
    print("   배치 후 R=%.3f" % cam.positionLBR.z)
except Exception as e:
    print("   배치 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("오메가 센타우리 — 별 1천만 개의 공"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# ── 성단 속으로 비행 (말머리 ⑥ setPositionR) ─────────────────
print("=" * 55); print("성단 속으로 비행 (setPositionR)"); print("=" * 55)
if gport != -1:
    try:
        t1.setText("성단 속으로 — 날아 들어간다")
        print("   비행 전 R=%.3f" % cam.positionLBR.z)
        cam.setPositionR(R_VIEW, Anim.cubic(FLY_SEC), gport)      # ★ R 감소 = 비행
        for i in range(5):
            sleep(FLY_SEC / 5.0)
            print("   비행 중 R=%.3f" % cam.positionLBR.z)
        # 조준 재정렬
        cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(2.0), gport)
        cam.setTargetHeight(29.9, Anim(0.3)); sleep(0.4)
        cam.setTargetHeight(30.0, Anim(0.5)); sleep(1.5)
        print("   ★ 성단 속으로 날아 들어갔나? (R 감소 + 별들이 다가옴?)")
    except Exception as e:
        print("   비행 실패: %s" % e)
    t1.setText("100억 년을 함께 돈 늙은 별들의 심장부")
    sleep(4.0)
    t1.setIntensity(0.0, Anim(0.8))
else:
    print("   포트 없음 → 비행 불가")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("오메가 센타우리"); t1.setIntensity(1.0, Anim(1.0))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①배치 후/비행 중 R 값 ②성단으로 날아 들어가는 게 보이나(말머리처럼)")

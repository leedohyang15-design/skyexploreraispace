# -*- coding: utf-8 -*-
"""
globular_cluster_v4.py — R 스케일 찾기 (2026-07-09)
v3 결과: R=3 에서 성단이 개별 별로 완전히 풀림(별밭이 돔 가득) = '성단 속' 도달 성공!
문제: R_START=60 이 이미 별밭이라 '멀리서 다가가는' 비행이 안 보임.
→ 멀리서 성단이 '작은 공'으로 보이는 R 을 스윕으로 찾는다. 그 R 이 진짜 출발점(R_START).

각 R 에서 3.5초 정지 — 어느 R 에서 성단이 '멀리 있는 공/뿌연 덩어리'로 보이는지 리포트.
그 값(R_START) → R=3(속) 로 비행하면 진짜 접근 연출 완성.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

try:
    SceneGraph().reset(1); sleep(2.0)
except Exception:
    pass
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 1, 0, 0, 0, tz, Anim(0.0))
sleep(0.5)

gc = GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)
gc.setIntensity(1.0, Anim(0.0))

gport = gc.portId(GlobularCluster.GlobularClusterPort.Galactic)
print("   Galactic 포트=%s" % gport)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.85, 0.9, 1.0))

# 첫 위치(제일 먼 곳)에서 페이드인
cam.setPositionLBR(Vec(0.0, 0.0, 200000.0), Anim(), gport)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), gport)
cam.setTargetHeight(30.0, Anim(0.0))
sleep(1.0)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(2.0)

# ── R 스윕: 큰 값 → 작은 값 (성단이 '공'으로 보이는 R 찾기) ──
for R in (200000.0, 50000.0, 10000.0, 2000.0, 400.0, 80.0, 15.0, 3.0):
    t1.setText("R = %.0f km" % R); t1.setIntensity(1.0, Anim(0.3))
    try:
        cam.setPositionLBR(Vec(0.0, 0.0, R), Anim.cubic(2.0), gport)
        cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), gport)
        sleep(2.5)
        print("   R 요청=%.0f → 실제=%.3f" % (R, cam.positionLBR.z))
    except Exception as e:
        print("   R=%.0f 실패: %s" % (R, e))
    sleep(1.0)
    t1.setIntensity(0.0, Anim(0.2)); sleep(0.3)

print("   ★ 어느 R 에서 성단이 '멀리 있는 공/뿌연 덩어리'로 보였나? (그게 출발점)")
t1.setText("어느 R 에서 성단이 작은 공으로 보였나요?"); t1.setIntensity(1.0, Anim(0.8))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: R 200000~3 중 성단이 '먼 공'→'별밭'으로 바뀐 R 구간은?")

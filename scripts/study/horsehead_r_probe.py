# -*- coding: utf-8 -*-
"""
horsehead_r_probe.py — R 계단 probe: 말머리가 '그림처럼' 잡히는 거리 찾기
====================================================================
실측: R=1.94pc(기존 설계값)는 성운 아트 '내부' — 구름 속에 파묻힘.
  → 줌 락(조준은 엔진이 유지)을 켠 채 R 을 계단식으로 빼면서 프레이밍 관찰.

보는 법: STEP1~6 각 5초. **말머리 기둥이 배경(붉은 IC434) 위에 제일 예쁘게
  잡히는 STEP 번호**만 알려줘. 그 R 로 최종판 확정.
"""
from skyExplorer import *
from studio import *
from Initialization import *

PC = 3.086e13          # 1 파섹(km)

# ── 초기화 + 콘텐츠 ─────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
smoothReset(False)
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(1.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(1.0, Anim(1.0))
horse = Nebula(Nebula.NebulaName.HORSEHEAD)
horse.setIntensity(1.0, Anim(1.0))
Nebula(Nebula.NebulaName.ORION).setIntensity(0.4, Anim(1.0))

# ── 카메라: 정면 + 줌 락 (조준 유지는 엔진 몫) ──────────────
cam = Camera(Camera.CameraName.MainCamera)
track = horse.portId(Nebula.NebulaPort.LineOfSightLocal)
cam.setPositionLBR(Vec(0.0, 0.0, 2.0 * PC), Anim(), track)
AdvancedCamera().setModeFreeFly()
cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
cam.setZoomFov(72.0, Anim())
cam.setZoomPosition(Vec(0.0, 0.0, 0.0), track, Anim(1.0), Camera.PositionMode.XYZ)
sleep(1.5)

# ── ★ R 계단: 2pc(내부) → 점점 밖으로 ──────────────────────
steps = [
    ("STEP1", 2.0),     # 기존 설계값 — 구름 속 (기준점)
    ("STEP2", 5.0),
    ("STEP3", 10.0),
    ("STEP4", 20.0),
    ("STEP5", 50.0),
    ("STEP6", 120.0),   # 지구에서 본 크기에 근접(실거리 ~400pc)
]
for name, rpc in steps:
    cam.setPositionR(rpc * PC, Anim.cubic(2.0), track)
    print(">>> %s  R = %.0f pc" % (name, rpc))
    sleep(5.0)

print(">>> 끝. 말머리가 제일 예쁘게 잡힌 STEP 번호 알려줘 → 그 R 로 최종판 확정.")

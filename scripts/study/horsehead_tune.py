# -*- coding: utf-8 -*-
"""
horsehead_tune.py — [v4] 마지막 조각: 추적 상태에서 TargetHeight 로 돔 중앙 올리기
====================================================================
port probe 판독: 조준은 이미 완벽 — 성운이 돔 '하단 가장자리'에 걸려 있었음.
  돔 투영에서 Target 0° = 정면 = 가장자리 / 90° = 천정 = 돔 중앙.
  → '가운데 안 옴'도 '누워 보임'도 전부 타깃 고도 문제였던 것!
  그리고 HUD 타이틀에 'Barnard 33' = 트랙볼이 B33 을 정식 추적 중 —
  행성 때 setTargetHeight(90) 이 먹혔던 바로 그 조건.

이 스크립트: 273 위치 + 295 정렬(검증) → TH 0→30→60→90 (각 5초)
  → 성운이 가장자리에서 중앙으로 '떠오르며' 자세도 같이 서는지 관찰.
  마지막에 TH=90 고정하고 8초 감상.
"""
from skyExplorer import *
from studio import *
from Initialization import *

PC = 3.086e13
R_VIEW = 20.0 * PC

# ── 리셋 + 콘텐츠 ───────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
smoothReset(False)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
horse = Nebula(Nebula.NebulaName.HORSEHEAD)
horse.setIntensity(1.0, Anim(0.0))
Nebula(Nebula.NebulaName.ORION).setIntensity(0.5, Anim(0.0))

# ── 위치(273) + 정렬(295) — port probe 에서 확인된 상태 재현 ──
cam = Camera(Camera.CameraName.MainCamera)
los = horse.portId(Nebula.NebulaPort.LineOfSightLocal)
cam.setPositionLBR(Vec(0.0, 0.0, R_VIEW), Anim(), los)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.5), los)
sleep(2.0)
print(">>> 시작 상태: 성운이 돔 하단 가장자리 (port probe 와 동일해야 함)")
sleep(3.0)

# ── ★ TargetHeight 사다리: 가장자리 → 중앙으로 ──────────────
for i, th in enumerate((0.0, 30.0, 60.0, 90.0), 1):
    try:
        cam.setTargetHeight(th, Anim(2.0))
        print(">>> TH%d = %.0f도 — 성운 높이/자세 관찰" % (i, th))
    except Exception as e:
        print(">>> setTargetHeight 실패:", repr(e)[:80])
        break
    sleep(5.0)

print(">>> TH=90 유지, 8초 감상 — 말머리가 중앙에 서 있나?")
sleep(8.0)
print(">>> 끝. ①TH 올라가며 성운이 떠올랐나 ②어느 TH 에서 제일 보기 좋았나 ③자세(누움)는?")

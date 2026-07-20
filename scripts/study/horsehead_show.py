# -*- coding: utf-8 -*-
"""
horsehead_show.py — [v2 최종] 암전 세팅 → 오리온자리 → 말머리 확대 (검증 조각 조립)
====================================================================
실측으로 확정된 조각들:
  · 위치 = setPositionLBR(track=LOSLocal portId)     [273]
  · 조준/세우기 = setOrientationSmoothXYZR(Vec4 0, track) [295 — 원본의 look]
  · Target 정렬 = setTargetHeight(30) ← 🎯운영 표준(관람 정위치). 90=천정(기하 중앙)은 관람 부적합
  · 프레이밍 거리 = 20pc (STEP4)  /  인트로 = 400pc(지구 실거리)
  · 슬루 숨김 = GlobalIntensity 0 에서 전부 세팅 후 페이드인

흐름: 암전(조준·TH 완료) → 페이드인: 오리온자리 → 18초 비행(400→20pc)
      → 도착 재정렬 → 자막 → (옵션) 정면 스윙 ±25°
"""
from skyExplorer import *
from studio import *
from Initialization import *

PC        = 3.086e13
R_START   = 400.0 * PC     # 인트로: 지구 실거리 (오리온자리 그림)
R_VIEW    = 10.0 * PC      # 프레이밍 — 더 근접(STEP3). 아트 내부(2pc) 주의
FLY_SEC   = 18.0           # 비행 시간
ORBIT_DEG = 360.0          # ★ 한 방향 풀 공전 (0 = 공전 없음)
ORBIT_SEC = 36.0           # 공전 시간 (한 바퀴)
#  ※ docs/13 실측: 근접 360°는 중간에 성운 '뒷면'(어두운 실루엣) 구간을 지남 — 연출로 감안

# ── 0) 하드 리셋 + 암전 ─────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
smoothReset(False)
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))          # ★ 관객: 검은 화면

# ── 1) 콘텐츠 (암전 뒤에서) ─────────────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
horse = Nebula(Nebula.NebulaName.HORSEHEAD)
horse.setIntensity(1.0, Anim(0.0))
Nebula(Nebula.NebulaName.ORION).setIntensity(0.5, Anim(0.0))
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setArtIntensity(0.8, Anim(0.0))              # ★ 별자리 그림(아트)으로
ori.setLabelIntensity(0.5, Anim(0.0))

# ── 2) ★ 카메라 전부 세팅 (암전 중 — 슬루는 관객이 못 봄) ────
cam = Camera(Camera.CameraName.MainCamera)
los = horse.portId(Nebula.NebulaPort.LineOfSightLocal)
cam.setPositionLBR(Vec(0.0, 0.0, R_START), Anim(), los)              # 위치(273)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), los)  # 조준(295)
cam.setTargetHeight(30.0, Anim(1.0))                                  # 🎯관람 정위치(운영 표준 30)
sleep(4.0)                                        # 조준/TH 슬루 완전히 끝나길 대기

# ── 3) 페이드인: 지구에서 본 오리온자리 (완성된 구도로 시작) ──
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인: 오리온자리 (6초 감상)")
sleep(6.0)

# ── 4) 비행: 오리온 속으로 400 → 20pc (18초) ────────────────
print(">>> 말머리로 비행 (%.0f초)" % FLY_SEC)
ori.setArtIntensity(0.0, Anim(4.0))              # 별자리 그림은 비행 시작하며 아웃
ori.setLabelIntensity(0.0, Anim(4.0))
cam.setPositionR(R_VIEW, Anim.cubic(FLY_SEC), los)
sleep(FLY_SEC + 0.5)

# 도착 재정렬 (비행 중 미세 드리프트 정리)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(2.0), los)
cam.setTargetHeight(29.9, Anim(0.3)); sleep(0.4)  # 같은값 no-op 우회
cam.setTargetHeight(30.0, Anim(0.5)); sleep(2.0)

# ── 5) 자막 ─────────────────────────────────────────────────
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setText("말머리 성운 Horsehead (Barnard 33)")
txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045)
txt.setColor(Vec(0.9, 0.6, 0.65)); txt.setIntensity(1.0, Anim(1.5))
sleep(3.0)

# ── 6) ★ 풀 공전: 한 방향 360° — 스텝마다 재조준으로 중앙 유지 ──
if ORBIT_DEG > 0:
    print(">>> 풀 공전 %.0f° (%.0f초, 한 방향)" % (ORBIT_DEG, ORBIT_SEC))
    step_dt = 0.5
    n = int(ORBIT_SEC / step_dt)
    for i in range(1, n + 1):
        L = ORBIT_DEG * i / float(n)
        cam.setPositionLBR(Vec(L, 0.0, R_VIEW), Anim(step_dt), los)
        if i % 4 == 0:                            # 2초마다 재조준(중앙 유지)
            cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(step_dt), los)
        sleep(step_dt)

print(">>> 쇼 끝. (1)페이드인 (2)비행 (3)도착 중앙+자세 (4)공전 한 바퀴 — 어땠어?")

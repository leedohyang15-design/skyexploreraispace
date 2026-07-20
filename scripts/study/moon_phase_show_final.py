# -*- coding: utf-8 -*-
"""
moon_phase_show_final.py — [최종·v3 실측 확정판] 달의 위상 쇼
====================================================================
실측 확정 (v1~v3):
  · 인트로 = 암전 + FadeTo(SatelliteType/"Moon") + ★클램프 루프★ + TH90 → 페이드인
    (reset/FadeTo 직후 gi 가 1.0 으로 남는 프레임이 있어 0.2초 간격 재암전 필요 — v3 실측)
  · 줌 = setPositionR(읽은 R × 배율, Anim, -1) — 화면 고정 확인
  · 그림자 = setPlanetShineStrength (0.0 = 칠흑)
  · ⚠️ 쇼 끝에 setManualMoonPhase(False) 복귀 금지 — 자동 위상과 싸우며
    그림자가 깜빡임(실측 리포트). 수동 유지한 채 끝낸다 (다음 쇼는 reset 으로 시작).

파라미터만 바꿔서 재활용:
"""
from skyExplorer import *
from studio import *
from Initialization import *

SHADOW      = 0.0     # 지구조(그늘 밝기): 0.0=그림자 최강(칠흑) ~ 1.0=기본
PHASE_SEC   = 15.0    # 위상 타임랩스 시간 (신월→보름→그믐)
ZOOM_SCALE  = 0.5     # 줌 배율 (0.5 = 2배 확대)
ZOOM_SEC    = 5.0
ORBIT_DEG   = 90.0    # 스텝 오빗 각도 (0 = 오빗 없음)
ORBIT_SEC   = 12.0

# ── 0) 리셋 + ★ 암전 (도착·정렬 슬루를 관객이 못 보게) ───────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

# ── 1) 달 준비 (암전 속) ─────────────────────────────────────
moon = None
for name in ("Moon", "MOON", "Luna"):
    try:
        moon = Satellite(getattr(Satellite.SatelliteName, name))
        break
    except Exception:
        pass
if moon is None:
    print("달 객체 실패 — 멤버:", [n for n in dir(Satellite.SatelliteName)
                                   if not n.startswith("_")][:30])

obj = DataManager.database().data(Data.Type.SatelliteType, "Moon")   # v3 실측 확정
obj.action(Action.Type.FadeTo).trigger()
for _ in range(25):                             # ★ 클램프 루프: FadeTo 5초 내내 재암전
    uni.setGlobalIntensity(0.0, Anim(0.0))      #   (첫 프레임 gi=1.0 잔존 — v3 실측)
    sleep(0.2)

cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(30.0, Anim(1.5))            # 🎯관람 정위치(운영 표준 30, 암전 속)
for _ in range(10):                             # 정렬 중에도 클램프
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

if moon is not None:
    moon.setManualMoonPhase(True)
    moon.setMoonAge(6.0, Anim(0.0))             # 초승 위상으로 시작 (그림자 잘 보임)
    moon.setPlanetShineStrength(SHADOW, Anim(0.0))   # 그림자 강도

# ── 2) 페이드인 — 처음부터 돔 중앙에 정렬된 달 ────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
print(">>> 페이드인: 달이 처음부터 중앙에 (재정렬 슬루 없음!)")
sleep(4.0)

# ── 3) 자막 ─────────────────────────────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("달의 위상 The Phases of the Moon")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045)
    txt.setColor(Vec(0.85, 0.85, 1.0)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass
sleep(2.0)

# ── 4) 위상 타임랩스 (그림자 강화 상태) ──────────────────────
if moon is not None:
    print(">>> 위상 타임랩스 %.0f초 (신월→보름→그믐)" % PHASE_SEC)
    moon.setMoonAge(0.0, Anim(1.0)); sleep(1.2)
    moon.setMoonAge(29.5, Anim(PHASE_SEC)); sleep(PHASE_SEC + 0.5)
    moon.setMoonAge(14.8, Anim(2.0)); sleep(2.5)    # 보름달로 마무리

# ── 5) 화면 고정 줌인 (v2 확정 — R만 변경) ───────────────────
p = cam.positionLBR
print(">>> 줌인 R %.2f → %.2f (%.0f초)" % (p.z, p.z * ZOOM_SCALE, ZOOM_SEC))
cam.setPositionR(p.z * ZOOM_SCALE, Anim.cubic(ZOOM_SEC), -1)
sleep(ZOOM_SEC + 0.5)

# ── 6) 스텝 오빗 (v1 확인 — track=-1 + TH 재조준) ────────────
if ORBIT_DEG > 0:
    print(">>> 스텝 오빗 %.0f° (%.0f초)" % (ORBIT_DEG, ORBIT_SEC))
    step_dt = 0.5
    n = int(ORBIT_SEC / step_dt)
    p = cam.positionLBR
    L0, B0, R0 = p.x, p.y, p.z
    for i in range(1, n + 1):
        L = L0 + ORBIT_DEG * i / float(n)
        cam.setPositionLBR(Vec(L, B0, R0), Anim(step_dt), -1)
        if i % 4 == 0:
            cam.setTargetHeight(29.9, Anim(0.1))
            cam.setTargetHeight(30.0, Anim(0.2))
        sleep(step_dt)

# ── 7) 마무리 — 보름달 유지한 채 종료 ────────────────────────
#  ⚠️ setManualMoonPhase(False) 로 자동 복귀시키면 수동/자동 위상이 싸우며
#     그림자가 깜빡임(실측) — 수동 유지. 원상 복구는 다음 쇼의 reset 이 담당.
print(">>> 쇼 끝! (그림자 깜빡임이 사라졌는지 확인해줘)")

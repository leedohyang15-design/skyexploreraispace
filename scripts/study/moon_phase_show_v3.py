# -*- coding: utf-8 -*-
"""
moon_phase_show_v3.py — [v3] 암전이 새는 범인 확정 + 억제
====================================================================
final 판에서도 정렬 과정이 보임 → 가설: Action.Type.FadeTo 가 자기 페이드 연출로
GlobalIntensity 를 도로 올린다 (말머리 쇼는 FadeTo 없이 포트 직접 배치라 암전 완벽).

이번 판:
  ★A FadeTo 진행 중 0.2초마다 GlobalIntensity 를 읽고 → 0 으로 계속 눌러 암전 유지
     (읽은 값을 출력 — 범인 확정 증거)
  ★B 다음 판을 위한 포트 프로브 (FadeTo 없이 직접 배치하는 말머리식 대비)

확인해줘: (a) 페이드인 전까지 화면이 완전 검은색이었나?
          (b) ★A 줄에 gi 값이 0보다 크게 찍혔나? (c) ★B 포트 목록
"""
from skyExplorer import *
from studio import *
from Initialization import *

SHADOW     = 0.0
PHASE_SEC  = 10.0
ZOOM_SCALE = 0.5

# ── 0) 리셋 + 암전 ──────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    print("★A 시작 gi =", uni.globalIntensity)
except Exception:
    print("★A globalIntensity 읽기 불가")

moon = None
for name in ("Moon", "MOON", "Luna"):
    try:
        moon = Satellite(getattr(Satellite.SatelliteName, name))
        break
    except Exception:
        pass

# ── 1) FadeTo + ★ 암전 억제 루프 (범인 실측) ─────────────────
for tname in ("SatelliteType", "MoonType", "PlanetType", "SolarSystemType"):
    try:
        obj = DataManager.database().data(getattr(Data.Type, tname), "Moon")
        if obj.id != -1:
            obj.action(Action.Type.FadeTo).trigger()
            print("★A FadeTo 발동 (%s) — 5초간 암전 강제 유지" % tname)
            break
    except Exception:
        pass

leaked = 0.0
for i in range(25):                      # 5초간 0.2초 간격
    try:
        gi = uni.globalIntensity
        if gi > 0.02:
            leaked = max(leaked, gi)
            print("★A %.1f초: gi=%.3f ← FadeTo 가 밝기를 올림! 다시 0으로" % (i * 0.2, gi))
    except Exception:
        pass
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)
print("★A 억제 루프 끝 — 최대 누출 gi=%.3f (0이면 FadeTo 는 gi 무죄 → 다른 채널)" % leaked)

# ── 2) 돔 중앙 정렬 (계속 암전) + 달 세팅 ────────────────────
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(90.0, Anim(1.5))
for i in range(10):                      # 정렬 중에도 암전 유지
    uni.setGlobalIntensity(0.0, Anim(0.0))
    sleep(0.2)

if moon is not None:
    moon.setManualMoonPhase(True)
    moon.setMoonAge(6.0, Anim(0.0))
    moon.setPlanetShineStrength(SHADOW, Anim(0.0))

# ── 3) ★B 다음 판 대비: 포트 프로브 (FadeTo 없는 직접 배치용) ──
try:
    ports = [n for n in dir(Satellite.SatellitePort) if not n.startswith("_")]
    print("★B SatellitePort:", ports)
    if moon is not None:
        for pname in ports[:4]:
            try:
                pid = moon.portId(getattr(Satellite.SatellitePort, pname))
                print("★B portId(%s) = %s" % (pname, pid))
            except Exception as e:
                print("★B portId(%s) 실패: %s" % (pname, repr(e)[:40]))
    p = cam.positionLBR
    print("★B 현재(트랙 후) positionLBR = (%.2f, %.2f, %.3f)" % (p.x, p.y, p.z))
except Exception as e:
    print("★B 프로브 실패:", repr(e)[:80])

# ── 4) 페이드인 — 여기서 처음으로 화면이 밝아져야 정상 ────────
print(">>> 페이드인! (이 직전까지 완전 검은 화면이었어야 함)")
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
sleep(4.0)

# ── 5) 짧은 쇼: 자막 + 위상 + 줌 ─────────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("달의 위상 The Phases of the Moon")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045)
    txt.setColor(Vec(0.85, 0.85, 1.0)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass

if moon is not None:
    moon.setMoonAge(0.0, Anim(1.0)); sleep(1.2)
    moon.setMoonAge(29.5, Anim(PHASE_SEC)); sleep(PHASE_SEC + 0.5)
    moon.setMoonAge(14.8, Anim(2.0)); sleep(2.5)

p = cam.positionLBR
cam.setPositionR(p.z * ZOOM_SCALE, Anim.cubic(5.0), -1)
sleep(5.5)

if moon is not None:
    moon.setPlanetShineStrength(1.0, Anim(3.0))
    moon.setManualMoonPhase(False)
print(">>> v3 끝! (a)페이드인 전 완전 암전? (b)★A gi 누출값 (c)★B 포트 줄들 — 보내줘")

# -*- coding: utf-8 -*-
"""
moon_phase_show_v2.py — [v2] 그림자 강화 + 줌 화면고정 3방식 비교
====================================================================
v1 피드백:
  · 줌 중 화면 이동 (setPositionR 로도!) → ★A/★B/★C 세 방식 비교 실험
  · 그림자 더 강하게 → setPlanetShineStrength(지구조=지구 반사광) 발견!
    어두운 면을 비추는 지구조를 끄면(0.0) 그림자가 진짜 검어질 것 — 3단계 시연

콘솔 ★ 줄 + 아래 질문 답을 보내줘:
  (a) 그림자: 1.0 / 0.5 / 0.0 중 어느 게 좋았나?
  (b) 줌 A(FOV)/B(스텝R)/C(줌락) 중 화면이 '고정'된 것은?
"""
from skyExplorer import *
from studio import *
from Initialization import *

# ── 0) 리셋 + 달 FadeTo (v1 프로브 유지) ────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])

cam = Camera(Camera.CameraName.MainCamera)

moon = None
for name in ("Moon", "MOON", "Luna"):
    try:
        moon = Satellite(getattr(Satellite.SatelliteName, name))
        print("★0 달 객체: %s (id=%s)" % (name, moon.id))
        break
    except Exception:
        pass
if moon is None:
    print("★0 달 객체 실패 — 멤버:", [n for n in dir(Satellite.SatelliteName)
                                      if not n.startswith("_")][:30])

for tname in ("SatelliteType", "MoonType", "PlanetType", "SolarSystemType"):
    try:
        obj = DataManager.database().data(getattr(Data.Type, tname), "Moon")
        if obj.id != -1:
            obj.action(Action.Type.FadeTo).trigger()
            print("★0 FadeTo: Data.Type.%s" % tname)
            break
    except Exception:
        pass
sleep(4.0)

cam.setTargetHeight(90.0, Anim(2.0))            # 돔 중앙
sleep(2.5)

# ── 1) ★★ 그림자 강화 — 지구조(planetshine) 3단계 ───────────
#     지구조 = 지구 반사광이 달의 '어두운 면'을 은은히 비추는 것.
#     이걸 줄이면 위상 그림자가 검고 강해진다.
if moon is not None:
    try:
        moon.setManualMoonPhase(True)
        moon.setMoonAge(6.0, Anim(1.0))          # 초승~반달 (그림자 잘 보이는 위상)
        sleep(1.5)
        try:
            print("★1 현재 planetShineStrength =", moon.planetShineStrength)
        except Exception:
            print("★1 planetShineStrength 읽기 불가 (세터만 시도)")
        print("★1 그림자 단계 1/3 — 지구조 1.0 (기본·밝은 그늘) 4초")
        moon.setPlanetShineStrength(1.0, Anim(1.0)); sleep(4.0)
        print("★1 그림자 단계 2/3 — 지구조 0.4 (중간) 4초")
        moon.setPlanetShineStrength(0.4, Anim(1.5)); sleep(4.0)
        print("★1 그림자 단계 3/3 — 지구조 0.0 (그림자 최강·칠흑) 4초")
        moon.setPlanetShineStrength(0.0, Anim(1.5)); sleep(4.0)
        print("★1 어느 단계가 좋았어? (이후 0.0 유지)")
    except Exception as e:
        print("★1 지구조 제어 실패:", repr(e)[:80])

    # 위상 타임랩스 (그림자 최강 상태로 다시 감상)
    try:
        print("★2 위상 스윕 12초 (그림자 강화판)")
        moon.setMoonAge(0.0, Anim(1.0)); sleep(1.2)
        moon.setMoonAge(29.5, Anim(12.0)); sleep(12.5)
        moon.setMoonAge(6.0, Anim(2.0)); sleep(2.5)   # 다시 초승 (그림자 보이게)
    except Exception as e:
        print("★2 위상 스윕 실패:", repr(e)[:60])

# ── 2) 줌 화면고정 3방식 비교 ────────────────────────────────
R0 = cam.positionLBR.z
print("★줌 실험 시작 — 기준 R = %.3f" % R0)

# [A] FOV 줌 — 카메라 이동 없음(광학 줌). 화면 고정 최유력.
try:
    f0 = None
    try:
        f0 = cam.zoomFov
        print("★A 현재 zoomFov =", f0)
    except Exception:
        print("★A zoomFov 읽기 불가 — 기본 110 가정")
    f0 = f0 or 110.0
    print("★A FOV 줌인 %.0f→%.0f (4초) — 화면 고정?" % (f0, f0 * 0.6))
    cam.setZoomFov(f0 * 0.6, Anim.cubic(4.0)); sleep(5.0)
    print("★A 복귀")
    cam.setZoomFov(f0, Anim(2.0)); sleep(2.5)
except Exception as e:
    print("★A FOV 줌 실패:", repr(e)[:80])

# [B] 스텝 R 줌 + TH 재조준 — 오빗에서 쓰던 재조준 트릭을 줌에 적용
try:
    print("★B 스텝 R 줌 (0.5초×12, 4스텝마다 TH 재조준) — 화면 고정?")
    r = R0
    for i in range(1, 13):
        r *= 0.94                                 # 12스텝 ≈ ×0.48
        cam.setPositionR(r, Anim(0.5), -1)
        if i % 4 == 0:
            cam.setTargetHeight(89.9, Anim(0.1))
            cam.setTargetHeight(90.0, Anim(0.2))
        sleep(0.5)
    sleep(1.0)
    print("★B 끝 R = %.3f — 복귀" % cam.positionLBR.z)
    cam.setPositionR(R0, Anim(2.0), -1); sleep(2.5)
except Exception as e:
    print("★B 스텝 줌 실패:", repr(e)[:80])

# [C] 줌 락(setZoomPosition) + FOV — 말머리에서 검증된 조합을 달에 이식
try:
    ports = [n for n in dir(Satellite.SatellitePort) if not n.startswith("_")]
    print("★C SatellitePort 멤버:", ports[:10])
    track = None
    for pname in ("EquatorialSynchronous", "Equatorial", "Ecliptic"):
        if pname in ports:
            track = moon.portId(getattr(Satellite.SatellitePort, pname))
            print("★C 트랙: %s (portId=%s)" % (pname, track))
            break
    if track is not None and track != -1:
        cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
        cam.setZoomPosition(Vec(0.0, 0.0, 0.0), track, Anim(1.5), Camera.PositionMode.XYZ)
        sleep(2.0)
        print("★C 줌 락 ON → FOV 줌인 (4초) — 엔진이 중앙 자동 유지?")
        cam.setZoomFov(70.0, Anim.cubic(4.0)); sleep(5.0)
        cam.setZoomFov(110.0, Anim(2.0)); sleep(2.5)
        print("★C 끝 — TH 상태와 충돌(화면 튐)이 있었는지도 알려줘")
    else:
        print("★C 트랙 포트 못 찾음 — 위 멤버 목록 알려줘")
except Exception as e:
    print("★C 줌 락 실패:", repr(e)[:100])

# ── 3) 자막 ─────────────────────────────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("달의 위상 The Phases of the Moon")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045)
    txt.setColor(Vec(0.85, 0.85, 1.0)); txt.setIntensity(1.0, Anim(1.5))
except Exception:
    pass

print(">>> v2 끝! (a)그림자 1.0/0.4/0.0 어느 게 좋았나 "
      "(b)줌 A/B/C 중 화면 고정된 것 (c)★C에서 화면 튐 여부 — 알려줘!")

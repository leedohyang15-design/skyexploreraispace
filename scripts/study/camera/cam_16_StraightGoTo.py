# -*- coding: utf-8 -*-
# [카메라 16] StraightGoTo — '즉시 도착' (2026-07-30 실측 확정)
#   · GoTo 와 **같은 도킹 위치**(암석행성 R≈5 반지름 · 북극상공 B=90)로 비행/페이드 없이 순간이동
#   · 화성 실측: HUD R=16,981km = 5.0 화성반지름 (정상 도킹 확인)
#   ⚠️ GoTo 와 마찬가지로 **Target 이 0 으로 남아 대상이 화면 아래 가장자리에 걸림**
#      → 도착 직후 setTargetHeight(30) 필수! (이거 안 하면 "행성이 바닥에 깔림")
#
# 쓸모: 20초 비행(GoTo)도 페이드(FadeTo)도 없이 곧바로 행성 앞에 서고 싶을 때 = 가장 빠른 전환.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# ── 지상 밤에서 출발 ─────────────────────────────────────────────
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
sleep(2.0)
print("지상 밤하늘에서 출발")

# ── ① StraightGoTo = 즉시 화성 도착 ────────────────────────────
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
act = None if h is None else h.action(Action.Type.StraightGoTo)
if act is None:
    print("⚠️ StraightGoTo 미지원 — 중단"); raise SystemExit
print("① StraightGoTo 실행 (비행 없이 즉시 도착)")
act.trigger()
sleep(3.0)                                  # 순간이동이라 짧게

# ── ② ★필수: Target 30 — 안 하면 화성이 화면 아래 가장자리에 걸림 ──
print("② setTargetHeight(30) — 화성을 관람 정위치(중앙)로  ★이게 핵심")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.5)

# ── ③ 표면 잘 보이게: 그림자 OFF 3세터 (운영 표준) ──────────────
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(1.0))
mars.setShadowContrast(0.0, Anim(1.0))
mars.setPlanetShineStrength(1.0, Anim(1.0))
sleep(1.5)
print("③ 그림자 OFF — 표면 전체가 밝게 (반쪽 어두움 제거)")

# ── ④ 줌인: 읽은값 ÷ 배율 (배율 클수록 확대) ────────────────────
#    ⚠️ positionLBR.z 숫자는 프레임마다 단위가 달라 '절대 거리'로 해석 금지.
#       비율로만 쓴다.
for zoom in [1.6, 1.6]:
    p = cam.positionLBR
    cam.setPositionR(p.z / zoom, Anim.cubic(3.5), -1)
    print("④ 줌인 ÷%.1f" % zoom); sleep(4.0)

print("\n완료 — 화성이 화면 중앙에 크게? (StraightGoTo = 가장 빠른 행성 도착)")
print("  레시피: StraightGoTo → setTargetHeight(30) → 그림자OFF → setPositionR(p.z/배율)")

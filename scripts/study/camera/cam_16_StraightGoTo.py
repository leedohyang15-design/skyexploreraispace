# -*- coding: utf-8 -*-
# [카메라 16] StraightGoTo — '즉시 도착' (2026-07-30 실측 확정)
#   · GoTo 와 **같은 도킹 위치**(암석행성 R≈5 반지름 · 북극상공 B=90)로 비행/페이드 없이 순간이동
#   · 화성 실측: HUD R=16,981km = 5.0 화성반지름 (정상 도킹 확인)
#   ⚠️⚠️ **암석행성은 도킹이 '북극 상공(B=90)' = 카메라가 행성 위에서 내려다보는 자세**
#        → Target 30(위를 봄)이면 행성이 '발밑'이라 화면 아래 가장자리에 걸린다!(사용자 실측)
#        → **해결: B 를 90 → 20 으로 내려 '옆에서 보는' 자세로 바꿀 것** (가스행성은 원래 옆 도킹이라 불필요)
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

# ── ② ★핵심: B 90 → 20 (북극 상공 → 옆에서 보기) ────────────────
#    암석행성 도킹은 B=90(행성 위) → 행성이 발밑이라 화면 아래에 걸린다.
#    B 를 낮춰 '옆'으로 가야 화성이 화면 중앙에 온다. (가스행성은 처음부터 B=20 이라 생략 가능)
p = cam.positionLBR
print("② B %.0f → 20 (북극상공 → 옆에서 보기)  ★이게 핵심" % p.y)
cam.setPositionLBR(Vec(p.x, 20.0, p.z), Anim.cubic(4.0), -1); sleep(4.5)
cam.setTargetHeight(30.0, Anim.cubic(1.5)); sleep(2.0)   # 관람 표준 정렬

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
print("  ★암석행성 확정 레시피:")
print("    StraightGoTo → setPositionLBR(Vec(L, 20, R))[B를 90→20] → setTargetHeight(30)")
print("    → 그림자 OFF 3세터 → setPositionR(p.z/배율) 줌")
print("  (가스행성 목성·토성은 도킹이 이미 옆(B=20)이라 B 조정 생략 가능)")

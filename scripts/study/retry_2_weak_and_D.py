# -*- coding: utf-8 -*-
# 재도전 ② — "렌더는 되는데 약했던" 것들 최대로 밀어붙이기 (F) + 표면디테일 극단줌(D)
# 이건 화면으로 보는 게 핵심. 단계마다 6초 홀드하니 눈으로 A/B 비교.
from skyExplorer import *
from studio import *
from Initialization import *

def hr(t): print("\n========== %s ==========" % t)
dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# ── F-1) 무지개 : 태양고도·반대편 조준 최적화 + 세기 0↔1 A/B ────────────────
hr("F-1) 무지개 최대치")
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception: pass
cam = Camera(Camera.CameraName.MainCamera)
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))   # 무지개는 대기 ON(낮)
Planet(Planet.PlanetName.Earth).setTerrainIntensity(0.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
# 태양 저각(무지개 아치 높이 ↑) = 이른 아침. 청주 아침 8시=23 UTC(전날)
dm.setDateTime(2026, 6, 1, 22, 30, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))  # 태양 반대편(서쪽 조준은 H로 조정)
try:
    earth.setRainbowIntensity(0.0, Anim(0.0)); sleep(1.0)
    print("  무지개 OFF (기준) — 6초"); sleep(6.0)
    earth.setRainbowIntensity(1.0, Anim(2.0)); sleep(2.5)
    print("  무지개 ON 최대 — 6초 (아치 보이나?)"); sleep(6.0)
    print("  [판정] OFF↔ON 차이가 눈에 확 들어오면 성공. 여전히 흐릿하면 SDK 한계(F 유지).")
except Exception as e:
    print("  rainbow 예외:", e)

# ── F-2) 토성 고리 카시니 간극 : 고리면 정면 + DefaultRing↔BasicRing 하드컷 ──
hr("F-2) 토성 고리 모델 A/B (카시니 간극)")
try:
    SceneGraph().reset(1); sleep(1.5)
    cam = Camera(Camera.CameraName.MainCamera)
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))  # 배경 검정
    DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
    sleep(4.5)
    sat = Planet(Planet.PlanetName.Saturn)
    sat.setShadowStrength(0.0, Anim(0.0)); sat.setShadowContrast(0.0, Anim(0.0))
    sat.setPlanetShineStrength(1.0, Anim(0.0))
    p = cam.positionLBR
    # 고리면 정면(B 크게=위에서) + 적당 줌
    cam.setPositionLBR(Vec(p.x, 75.0, max(3.2, p.z*0.7)), Anim.cubic(4.0), -1); sleep(4.5)
    cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)
    for md, nm in [("DefaultRing","기본"),("BasicRing","베이직"),("Asteroids","소행성"),("DefaultRing","기본복귀")]:
        try:
            sat.setRingModel(getattr(Planet.RingModel, md))
            print("  RingModel = %s(%s) — 6초 홀드" % (md, nm)); sleep(6.0)
        except Exception as e:
            print("  RingModel %s 예외: %s" % (md, e))
    print("  [판정] 카시니 간극(고리 중간 검은 틈)이 모델마다 다르게 보이면 성공. 다 똑같으면 F 유지.")
except Exception as e:
    print("  토성 예외:", e)

# ── F-3) 천왕성 고리 : 본체 intensity 1.5 스위트스팟 + 근접·고리면 개방 ─────
hr("F-3) 천왕성 고리 본체 intensity 1.5")
try:
    SceneGraph().reset(1); sleep(1.5)
    cam = Camera(Camera.CameraName.MainCamera)
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    sleep(4.5)
    ur = Planet(Planet.PlanetName.Uranus)
    ur.setShadowStrength(0.0, Anim(0.0)); ur.setShadowContrast(0.0, Anim(0.0)); ur.setPlanetShineStrength(1.0, Anim(0.0))
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 3.2), Anim.cubic(4.0), -1); sleep(4.5)  # 근접 R≈3.2, 고리면 개방 B38
    cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)
    for iv in [1.0, 1.5, 1.8]:
        ur.setIntensity(iv, Anim(1.5)); print("  본체 intensity = %.1f — 6초 (고리 또렷해지나?)" % iv); sleep(6.5)
    ur.setIntensity(1.0, Anim(1.0)); sleep(1.2)
    print("  [판정] intensity 1.5 근처에서 고리가 은은히 또렷하면 성공(원반 안 타는 선). 2+는 하얗게 탐.")
except Exception as e:
    print("  천왕성 예외:", e)

# ── D) 표면 디테일 극단줌 (강수/암벽/식생) — Terrain View 없이 궤도 최대 접근 ─
hr("D) 지구 표면 디테일 극단줌 (강수/암벽/식생)")
try:
    SceneGraph().reset(1); sleep(1.5)
    cam = Camera(Camera.CameraName.MainCamera)
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
    DataManager.database().data(Data.Type.PlanetType, "Earth").action(Action.Type.FadeTo).trigger()
    sleep(4.5)
    e = Planet(Planet.PlanetName.Earth)
    e.setShadowStrength(0.0, Anim(0.0)); e.setShadowContrast(0.0, Anim(0.0)); e.setPlanetShineStrength(1.0, Anim(0.0))
    try: e.setTerrainModel(Planet.TerrainModel.PlanetObserverDEM30)  # DEM(고도 데이터)
    except Exception as ex: print("  terrainModel 예외:", ex)
    e.setTerrainIntensity(1.0, Anim(0.0)); e.setElevationScale(12.0, Anim(0.0))
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 22.0, 1.08), Anim.cubic(5.0), -1); sleep(5.5)  # 표면 바짝(오블리크)
    cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)
    for fn in ["setRockyCliffIntensity","setTreeIntensity","setCloudRaininess"]:
        try:
            getattr(e, fn)(1.0, Anim(1.0)); print("  %s(1.0) 호출 — 6초 (뭔가 표면에 나타나나?)" % fn); sleep(6.0)
        except Exception as ex:
            print("  %s 예외: %s" % (fn, ex))
    print("  [판정] 궤도 극단줌서도 무변화면 = Terrain View(오퍼레이터) 전용 확정. 뭔가 뜨면 대박.")
except Exception as e:
    print("  지구표면 예외:", e)

print("\n>>> 끝. F-1/F-2/F-3/D 각각 화면에서 '차이가 보였는지' 알려주세요.")

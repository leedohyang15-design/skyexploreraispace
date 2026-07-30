# -*- coding: utf-8 -*-
# ═══ [정답 예제 1] 화성 클로즈업 ═══
# 대응 프롬프트: "화성으로 가서 표면을 크게 보여줘"
#
# 이 예제가 지키는 오늘의 확정 규칙:
#   ① StraightGoTo = 비행/페이드 없이 즉시 도착 (GoTo 와 같은 도킹 R≈5)
#   ② 도킹이 남긴 B 를 건드리지 않는다 (암석행성 B≈90 이 관람 정위치)
#   ③ 프레이밍은 Target(고도) 로만 — 표준 30
#   ④ 그림자 OFF 3세터 = 표면 전체가 밝게 (터미네이터로 반쪽 어두워지는 것 방지)
#   ⑤ 줌 2대 원칙: 절대타겟(p0 한 번만 읽기) + 선형 Anim + 겹치기(sleep < anim)
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 지상 밤하늘에서 출발 ──────────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))      # 대기 OFF
earth.setTerrainIntensity(0.0, Anim(0.0))         # 지면 OFF
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)         # 밤 21시 = 12 UTC
cam.setTargetHeight(30.0, Anim(0.0))
sleep(2.0)

# 자막
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("붉은 행성, 화성으로"); t1.setIntensity(1.0, Anim(1.0))
sleep(2.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── ① StraightGoTo = 즉시 도착 ───────────────────────────────
DataManager.database().data(Data.Type.PlanetType, "Mars") \
    .action(Action.Type.StraightGoTo).trigger()
sleep(4.0)

# ── ③ Target 30 (프레이밍은 이걸로만. ② B 는 건드리지 않음) ──
cam.setTargetHeight(30.0, Anim.cubic(1.5))
sleep(2.0)

# ── ④ 그림자 OFF 3세터 = 표면 전체 밝게 ──────────────────────
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(1.0))
mars.setShadowContrast(0.0, Anim(1.0))
mars.setPlanetShineStrength(1.0, Anim(1.0))
sleep(1.5)

# ── ⑤ 줌: 절대타겟 + 선형 + 겹치기 (끊김 방지) ───────────────
p0 = cam.positionLBR.z                       # ★ 한 번만 읽는다
for zoom in (1.35, 1.8, 2.3, 2.8, 3.2, 3.6): # 목표는 전부 p0 기준 절대값
    cam.setPositionR(p0 / zoom, Anim(1.4), -1)   # 선형 Anim
    sleep(1.05)                                   # anim 보다 짧게 = 겹침
sleep(1.5)

# ── 표면 지도 교체(탐사선 지도) + 마무리 자막 ────────────────
mars.setTerrainModel(Planet.TerrainModel.Viking)
sleep(2.0)
t1.setText("바이킹 탐사선이 본 화성 표면"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

# -*- coding: utf-8 -*-
# ═══ [정답 예제 1] 화성 클로즈업 (v2 — 줌 폭발 수정) ═══
# 대응 프롬프트: "화성으로 가서 표면을 크게 보여줘"
#
# ⚠️⚠️ v1 실패 원인 (사용자 실측): **StraightGoTo 프레임에서는 줌을 하면 안 된다.**
#   그 프레임의 `positionLBR.z` 는 105,609 로 읽히는데(HUD 실제는 16,981km),
#   그 값을 setPositionR 로 되쓰면 엔진이 다른 단위로 해석 → **R 이 수천~1만 Gm 으로 폭발**
#   (카메라가 태양계 밖으로 날아가 태양만 점으로 보임).
#   → **줌을 할 거면 반드시 `FadeTo`** — FadeTo 프레임은 R 이 '반지름 단위'(≈5.0)로 읽혀
#      읽기/쓰기가 일치한다(토성 5.000→2.500→1.250 실측 검증).
#   → StraightGoTo 는 '그냥 빨리 도착만' 할 때(뒤에 카메라 조작 없음) 쓸 것.
#
# 이 예제가 지키는 규칙:
#   ① FadeTo 로 도킹 (줌하려면 이것)         ② 도킹이 남긴 B 를 건드리지 않는다
#   ③ 프레이밍은 Target(고도) 30 으로만       ④ 그림자 OFF 3세터 = 표면 전체 밝게
#   ⑤ 줌 2대 원칙: 절대타겟(p0 한 번만) + 선형 Anim + 겹치기(sleep < anim)
#   ⑥ 안전장치: p0 가 비정상 범위면 줌을 건너뛴다(폭발 방지)
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

# ── ① FadeTo 로 도킹 (★줌을 하려면 StraightGoTo 말고 이것) ───
DataManager.database().data(Data.Type.PlanetType, "Mars") \
    .action(Action.Type.FadeTo).trigger()
sleep(5.0)

# ── ③ Target 30 (② B 는 건드리지 않는다 — 도킹 기본값이 관람 정위치) ──
cam.setTargetHeight(30.0, Anim.cubic(1.5))
sleep(2.0)

# ── ④ 그림자 OFF 3세터 = 표면 전체 밝게 ──────────────────────
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(1.0))
mars.setShadowContrast(0.0, Anim(1.0))
mars.setPlanetShineStrength(1.0, Anim(1.0))
sleep(1.5)

# ── ⑤⑥ 줌: 절대타겟 + 선형 + 겹치기 (+ 폭발 방지 가드) ───────
p0 = cam.positionLBR.z
print("도킹 R = %.3f  (FadeTo 정상이면 5 안팎의 '반지름 단위' 값이어야 함)" % p0)
if p0 > 100.0 or p0 <= 0.0:
    # 프레임이 이상해 읽기/쓰기 단위가 안 맞는 상태 → 줌하면 카메라가 날아간다
    print("⚠️ R 값이 비정상 범위 → 줌 생략(폭발 방지). FadeTo 로 다시 진입할 것")
else:
    for zoom in (1.35, 1.8, 2.3, 2.8, 3.2, 3.6):   # 목표는 전부 p0 기준 절대값
        cam.setPositionR(p0 / zoom, Anim(1.4), -1) # 선형 Anim
        sleep(1.05)                                 # anim 보다 짧게 = 겹침
    print("줌 완료 R = %.3f" % cam.positionLBR.z)
sleep(1.5)

# ── 표면 지도 교체(탐사선 지도) + 마무리 자막 ────────────────
mars.setTerrainModel(Planet.TerrainModel.Viking)
sleep(2.0)
t1.setText("바이킹 탐사선이 본 화성 표면"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

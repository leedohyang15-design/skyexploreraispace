# -*- coding: utf-8 -*-
# [카메라 08] setZoomFormula + setZoomPosition = '줌 락'(이동 중 대상 중앙 자동 유지).
# 되는 곳: ② 우주 / ③ 성운. 🛑 지상 무효. 엔진이 재조준을 내부 처리 → 카메라가 어디로 가든 중앙.
# 데모: 목성 도킹 → 줌락 걸고 → 카메라를 옆으로(L) 크게 이동해도 목성이 화면 중앙에 유지.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.3, Anim(0.0))
DataManager.database().data(Data.Type.PlanetType, "Jupiter").action(Action.Type.FadeTo).trigger()
sleep(4.5)
jup = Planet(Planet.PlanetName.Jupiter)
jup.setShadowStrength(0.0, Anim(0.0)); jup.setShadowContrast(0.0, Anim(0.0)); jup.setPlanetShineStrength(1.0, Anim(0.0))
sleep(1.0)

# ★ 줌 락: 공식 GreatCircle + 대상 오프셋 0 으로 락
try:
    ip = jup.portId(Planet.PlanetPort.EquatorialJ2000)
    cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
    cam.setZoomPosition(Vec(0, 0, 0), ip, Anim(1.0), Camera.PositionMode.XYZ)
    print("줌 락 설정 완료 — 이제 카메라를 옆으로 옮겨도 목성이 중앙 유지")
    sleep(1.5)
except Exception as e:
    print("줌락 설정 예외:", e)

# 카메라를 옆으로 크게 이동 → 락 덕에 목성이 화면 중앙에 남는지 확인
p = cam.positionLBR
for dL in [70.0, 140.0]:
    cam.setPositionLBR(Vec(p.x + dL, p.y, p.z), Anim.cubic(4.0), -1)
    print("  카메라 L +%.0f 이동 (목성 중앙 유지되나?)" % dL); sleep(4.5)
print("완료 — 줌락이 걸리면 이동해도 대상 중앙. 줌인은 setZoomFov 로 병행. ⚠️ 지상에선 무반응.")

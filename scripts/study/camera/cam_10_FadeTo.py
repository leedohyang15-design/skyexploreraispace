# -*- coding: utf-8 -*-
# [카메라 10] Action.FadeTo — 페이드 전환(비행 아님! Fade out→순간이동→Fade in).
# 도착: 행성 R=5 도킹 / 성운·성단 R=0. 프레임 간 전환(지상↔행성)의 기본기.
# 데모: 지상 밤하늘 → 화성으로 페이드 전환 → 그림자 끄고 표면 보기.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
print("FadeTo Mars — 페이드로 화성 프레임 진입")
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
if h is None or h.action(Action.Type.FadeTo) is None:
    print("⚠️ FadeTo 미지원")
else:
    h.action(Action.Type.FadeTo).trigger()
    sleep(5.0)
    mars = Planet(Planet.PlanetName.Mars)
    mars.setShadowStrength(0.0, Anim(1.0)); mars.setShadowContrast(0.0, Anim(1.0)); mars.setPlanetShineStrength(1.0, Anim(1.0))
    cam.setTargetHeight(30.0, Anim(1.0)); sleep(2.0)
    try: print("도착 R =", cam.positionLBR.z, "(행성은 ≈5 도킹)")
    except Exception: pass
print("완료 — FadeTo=페이드 전환. 슬루 숨기려면 GlobalIntensity 0 에서 실행 후 페이드인.")

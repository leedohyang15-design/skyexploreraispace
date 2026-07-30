# -*- coding: utf-8 -*-
# [카메라 11] Action.GoTo — 연속 비행(우주선 여행). 현 위치→대상까지 실제로 날아감.
# 도착 R≈5. ⚠️ 비행 중 자세회전 1회 흔들림 내장. 도착 후 setTargetHeight(30) 필수.
# ⚠️ action 이 None 이면 그 데이터는 GoTo 미지원(그땐 FadeTo/ConnectTo).
# 데모: 지상 → 토성으로 GoTo 비행.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))
print("GoTo Saturn — 연속 비행 시작")
h = DataManager.database().data(Data.Type.PlanetType, "Saturn")
act = None if h is None else h.action(Action.Type.GoTo)
if act is None:
    print("⚠️ GoTo 미지원(action None) — FadeTo 로 대체해야 함")
else:
    act.trigger()
    sleep(24.0)                       # GoTo 비행 시간(대상까지 수십 초)
    cam.setTargetHeight(30.0, Anim(2.0)); sleep(2.5)   # ★ 도착 후 필수(안 하면 바닥에 깔림)
    sat = Planet(Planet.PlanetName.Saturn)
    sat.setShadowStrength(0.0, Anim(1.0)); sat.setShadowContrast(0.0, Anim(1.0)); sat.setPlanetShineStrength(1.0, Anim(1.0))
    try: print("도착 R =", cam.positionLBR.z)
    except Exception: pass
print("완료 — GoTo=비행(FadeTo=페이드와 다름). 도착 후 setTargetHeight(30) 잊지 말 것.")

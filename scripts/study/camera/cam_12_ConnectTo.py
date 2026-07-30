# -*- coding: utf-8 -*-
# [카메라 12] Action.ConnectTo — 카메라 이동 없이 '프레임만' 순간 전환(흔들림 無).
# 되는 곳: 흔들림 없는 줌인의 정답 = ConnectTo(암전 속) 로 프레임 잡고 → setPositionR 줌.
# 데모: 지상 → 화성 ConnectTo(프레임 전환) → 그 프레임에서 R 줌인.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))

h = DataManager.database().data(Data.Type.PlanetType, "Mars")
act = None if h is None else h.action(Action.Type.ConnectTo)
if act is None:
    print("⚠️ ConnectTo 미지원(action None)")
else:
    print("ConnectTo — 프레임 전환(내부 Look-at 슬루가 보이니 암전 권장)")
    uni.setGlobalIntensity(0.0, Anim(0.8)); sleep(1.0)   # 슬루 숨기기
    act.trigger(); sleep(4.5)
    cam.setTargetHeight(30.0, Anim(0.0))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.5)
    # 프레임 잡혔으니 이제 R 줌인 (읽은값×배율)
    for f in [0.5, 0.5]:
        p = cam.positionLBR
        cam.setPositionR(p.z * f, Anim(3.0), -1)
        print("  줌인 R %.1f → %.1f" % (p.z, p.z*f)); sleep(3.5)
print("완료 — ConnectTo=이동 없는 프레임 전환. GoTo(흔들림)와 달리 깔끔. 줌은 setPositionR 로.")

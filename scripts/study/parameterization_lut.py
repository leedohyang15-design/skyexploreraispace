# -*- coding: utf-8 -*-
"""
parameterization_lut.py — ParameterizationLut v4 (2026-07-22, 확실한 판정)
★ v3 확인: setEnabled(True) 후 **1초 프레임 대기하면 enabled=True 로 붙음**(활성화는 됨). automatic 3인자 오버로드는 실패(2인자만).
  하지만 별밭 밝기 변화가 애매("잘 모르겠는데") → 이번엔 극단·정지로 확실히 판정.
★ v4: 밀키웨이 OFF(별만) + 입력 0 으로 내려 **5초 홀드**(별이 전부 사라져야 함) → 1 로 올려 5초 홀드(전부 복귀).
  enabled=True 확정 후 구동. 별이 확 사라지면 = 파라미터화 성공(속성 자동화 확정), 그대로면 = piloting 무효(가시효과 없음).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:90])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:40]


print("무대: ParameterizationLut v4 — 확실판정(별만, 홀드)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))   # ★ 밀키웨이 OFF = 별만
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


AN = ParameterizationLut.AttributeName
KT = ParameterizationLut.KeyType
handler = int(rd(stars, "osgId"))
print("   Stars handler=%s" % handler)

plut = ParameterizationLut(ParameterizationLut.ParameterizationLutName.ParameterizationLut001)
feat(plut, "clearTargetAttributes"); feat(plut, "clearKey")
feat(plut, "setInternalValue", 1.0, Anim(0.0))
feat(plut, "addKey", 0.0, Vec4(0, 0, 0, 0), KT.Double, label="(input0 → 밝기0)")
feat(plut, "addKey", 1.0, Vec4(1, 0, 0, 0), KT.Double, label="(input1 → 밝기1)")
feat(plut, "addTargetAttribute", handler, AN.Intensity, label="(별밭 Intensity)")
feat(plut, "setEnabled", True)
sleep(1.2)   # ★ 프레임 대기 = enabled 붙는 시간
print("   [enabled] = %s" % rd(plut, "enabled"))

narr("지금부터 별밭 밝기를 LUT가 조종", 3.0)

# 입력 0 → 5초 홀드 (별이 다 사라져야 함)
narr("입력 = 0  →  별이 전부 사라져야 함", 1.0)
feat(plut, "setInternalValue", 0.0, Anim(2.5)); sleep(2.6)
narr("★ 지금 별이 없나? (5초 정지)", 5.0)

# 입력 1 → 5초 홀드 (별 전부 복귀)
narr("입력 = 1  →  별이 전부 돌아와야 함", 1.0)
feat(plut, "setInternalValue", 1.0, Anim(2.5)); sleep(2.6)
narr("★ 지금 별이 가득한가? (5초 정지)", 5.0)

# 한 번 더 왕복 (확인)
narr("다시 입력 0 → 소등", 1.0)
feat(plut, "setInternalValue", 0.0, Anim(2.0)); sleep(3.0)
narr("입력 1 → 점등", 1.0)
feat(plut, "setInternalValue", 1.0, Anim(2.0)); sleep(3.0)

# 정리
feat(plut, "restore"); feat(plut, "setEnabled", False)
stars.setIntensity(1.0, Anim(1.0))

narr("ParameterizationLut — 속성 자동화 엔진", 2.5)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v4). ★리포트(딱 하나): "
      "'입력=0 (5초 정지)' 구간에서 **별이 전부 사라졌다가**, '입력=1 (5초 정지)' 에서 **다시 가득 찼나**? "
      "→ ①확실히 그랬다(=성공) / ②전혀 안 변하고 별 그대로(=piloting 무효) / ③미묘하게 조금만. "
      "(로그 '[enabled] = True' 는 이미 확인됨.)")

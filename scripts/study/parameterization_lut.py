# -*- coding: utf-8 -*-
"""
parameterization_lut.py — ParameterizationLut (속성 자동화 LUT) (2026-07-22, 완본 미개척)
★ ParameterizationLut = '어떤 개체의 속성(밝기/색/투명도…)을 LUT 곡선으로 자동 구동'하는 강력한 파라미터화 엔진.
  핵심 메서드: addTargetAttribute(대상핸들, AttributeName)=구동할 속성 지정 · addKey(위치0~1, Vec4, KeyType)=LUT 곡선 키 ·
  setEnabled(True) · setInternalValue(0~1, Anim)=수동 입력(슬라이더처럼 구동) · restore()=제어 반환 · setSourceSunHeight()=태양고도로 자동구동.
  AttributeName: Intensity/Opacity/Color/LinesColor/Position/AzimuthHeight/ManualIntensity/TrackingIntensity 등.
  ⚡ **프리셋 슬롯 존재**(바인딩 미리 배선됨): 051_AllConstellationLines / 055_SliderConstellationLines /
  059_StarrySkyAutoExposure / 061_WeatherEffectRain / 062_WeatherEffectSnow 등 → 만들어서 setInternalValue 만 흔들면 됨.
★ 전략: ①프리셋 '별자리 선 슬라이더' 를 켜고 internalValue 0→1→0 → 전 별자리 선이 슬라이더로 페이드(높은 성공확률).
  ②직접(커스텀): Lut001 로 오리온 Intensity 를 키(0→0,1→1)로 구동. 로그로 attributeList/piloted 확인.
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
        print("   ✗ %s 실패: %s" % (fn, str(e)[:100])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:40]


# ── 무대: 검은 하늘 + 별자리 선 ─────────────────────────────
print("무대: ParameterizationLut — 속성 자동화")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.35, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(20.0, Anim(0.0))

# 여러 별자리 선 ON (슬라이더로 구동할 대상)
cons = []
for nm in ("Ori", "UMa", "Cas", "Cyg", "Leo", "Tau", "Gem"):
    if hasattr(Constellation.ConstellationName, nm):
        c = Constellation(getattr(Constellation.ConstellationName, nm))
        c.setLinesIntensity(1.0, Anim(0.0))
        cons.append((nm, c))
ori = Constellation(Constellation.ConstellationName.Ori)

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── dir() 덤프 ──────────────────────────────────────────────
narr("속성 자동화 LUT — ParameterizationLut", 2.5)
try:
    probe = ParameterizationLut(ParameterizationLut.ParameterizationLutName.ParameterizationLut001)
    print("   [PLut dir()] %s" % [m for m in dir(probe) if not m.startswith("__")])
    print("   [AttributeName] %s" % [m for m in dir(ParameterizationLut.AttributeName) if not m.startswith("__") and "Invalid" not in m])
    print("   [KeyType] %s" % [m for m in dir(ParameterizationLut.KeyType) if not m.startswith("__") and "Invalid" not in m])
except Exception as e:
    print("   PLut 프로브 실패: %s" % str(e)[:100])


# ── ① 프리셋: 별자리 선 슬라이더 (바인딩 미리 배선) ─────────
narr("① 프리셋 슬라이더로 별자리 선 페이드", 2.5)
slider = None
for nm in ("ParameterizationLut055_SliderConstellationLines", "ParameterizationLut051_AllConstellationLines"):
    if hasattr(ParameterizationLut.ParameterizationLutName, nm):
        try:
            slider = ParameterizationLut(getattr(ParameterizationLut.ParameterizationLutName, nm))
            print("   프리셋 = %s" % nm); break
        except Exception as e:
            print("   %s 실패: %s" % (nm, str(e)[:60]))
if slider is not None:
    feat(slider, "setEnabled", True)
    print("   piloted=%s enabled=%s" % (rd(slider, "pilotedAttributeList"), rd(slider, "enabled")))
    narr("슬라이더 0 → 별자리 선 사라짐", 1.0)
    feat(slider, "setInternalValue", 0.0, Anim(3.0)); sleep(3.2)
    narr("슬라이더 1 → 별자리 선 나타남", 1.0)
    feat(slider, "setInternalValue", 1.0, Anim(3.0)); sleep(3.2)
    narr("슬라이더 0.5 → 반투명", 1.0)
    feat(slider, "setInternalValue", 0.5, Anim(2.0)); sleep(2.5)
    narr("① 별자리 선이 슬라이더로 조절됐나?", 3.5)
    feat(slider, "setInternalValue", 1.0, Anim(1.0)); sleep(1.2)
    feat(slider, "restore"); feat(slider, "setEnabled", False)
else:
    narr("프리셋 슬라이더 없음 — 커스텀만", 2.0)


# ── ② 커스텀: 오리온 Intensity 를 키로 구동 ─────────────────
narr("② 커스텀 — 오리온 밝기를 LUT로 구동", 2.5)
try:
    plut = ParameterizationLut(ParameterizationLut.ParameterizationLutName.ParameterizationLut001)
    # 대상 핸들: osgId 우선, 실패 시 id
    handler = None
    for h in ("osgId", "id"):
        hv = rd(ori, h)
        if isinstance(hv, int):
            handler = hv; print("   오리온 handler(%s)=%s" % (h, hv)); break
    AN = ParameterizationLut.AttributeName
    KT = ParameterizationLut.KeyType
    if handler is not None:
        feat(plut, "clearTargetAttributes")
        feat(plut, "clearKey")
        feat(plut, "addTargetAttribute", handler, AN.Intensity, label="(오리온 Intensity 구동)")
        # LUT 곡선: 입력 0 → 밝기 0, 입력 1 → 밝기 1
        feat(plut, "addKey", 0.0, Vec4(0, 0, 0, 0), KT.Double, label="(key@0=0)")
        feat(plut, "addKey", 1.0, Vec4(1, 0, 0, 0), KT.Double, label="(key@1=1)")
        feat(plut, "setEnabled", True)
        print("   piloted=%s attrs=%s" % (rd(plut, "pilotedAttributeList"), rd(plut, "attributeList")))
        narr("입력 0 → 오리온 어두워짐", 1.0)
        feat(plut, "setInternalValue", 0.0, Anim(3.0)); sleep(3.2)
        narr("입력 1 → 오리온 밝아짐", 1.0)
        feat(plut, "setInternalValue", 1.0, Anim(3.0)); sleep(3.2)
        narr("② 오리온만 LUT로 밝기 변했나?", 3.5)
        feat(plut, "restore"); feat(plut, "setEnabled", False)
    else:
        narr("오리온 handler 획득 실패", 2.5)
except Exception as e:
    print("   커스텀 실패: %s" % str(e)[:100]); narr("커스텀 LUT 실패 — 로그 확인", 3.0)

narr("ParameterizationLut — 속성 자동화 엔진", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(PLut 판별). ★리포트: "
      "①★프리셋 슬라이더 구간(①)에서 별자리 선들이 internalValue 0→1→0.5 따라 '사라졌다 나타났다 반투명' 됐나 (됐다/미미/전혀) "
      "②★커스텀 구간(②)에서 '오리온만' 어두워졌다 밝아졌나 (됐다/전혀) "
      "③로그 '[PLut dir()]' '[AttributeName]' '[KeyType]' 목록 + 'piloted=..' 값 붙여줘 "
      "④둘 다 전혀면 = 파라미터화도 시스템/오퍼레이터 소관으로 판정")

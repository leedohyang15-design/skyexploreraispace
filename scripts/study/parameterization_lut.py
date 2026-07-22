# -*- coding: utf-8 -*-
"""
parameterization_lut.py — ParameterizationLut v3 (2026-07-22, enabled=False 공략)
★ v2 결과: setEnabled(True) 호출은 성공하나 **enabled 읽으면 계속 False** → 파라미터화가 실제로 안 켜짐(무변화).
  프리셋(055)도, 커스텀(Stars Intensity)도 동일. = 활성화가 안 붙는 게 근본 문제.
★ v3 공략: ①`addTargetAttribute(handler, attr, True)` **automatic=True 오버로드**(자동관리 플래그) ·
  ②값(internalValue) 먼저 세팅 → 키 → **setEnabled 를 맨 마지막 + 프레임 대기(sleep)** → enabled 재확인 ·
  ③각 단계 enabled 를 여러 번 읽어 언제 켜지는지 추적. 타겟 = 별밭(항상 보임).
★ enabled 가 끝내 False 면 = 파라미터화도 쇼엔진/오퍼레이터 소관(스크립트 창 미지원)으로 확정.
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


# ── 무대: 검은 하늘 + 별밭 ──────────────────────────────────
print("무대: ParameterizationLut v3 — enabled 공략")
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
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(40.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


AN = ParameterizationLut.AttributeName
KT = ParameterizationLut.KeyType
handler = rd(stars, "osgId")
print("   Stars handler(osgId)=%s" % handler)

plut = ParameterizationLut(ParameterizationLut.ParameterizationLutName.ParameterizationLut001)


def chk(tag):
    print("   [enabled after %s] = %s" % (tag, rd(plut, "enabled")))


# ── 구성: 값 먼저 → 키 → automatic 타겟 → enable 마지막 ──────
narr("파라미터화 구성 (automatic + enable 마지막)", 2.5)
feat(plut, "clearTargetAttributes"); feat(plut, "clearKey")
feat(plut, "setInternalValue", 1.0, Anim(0.0), label="(값 먼저 1.0)")
feat(plut, "addKey", 0.0, Vec4(0, 0, 0, 0), KT.Double, label="(key@0=0)")
feat(plut, "addKey", 1.0, Vec4(1, 0, 0, 0), KT.Double, label="(key@1=1)")
# automatic=True 3인자 오버로드 (자동관리)
if not feat(plut, "addTargetAttribute", int(handler), AN.Intensity, True, label="(automatic=True)"):
    feat(plut, "addTargetAttribute", int(handler), AN.Intensity, label="(2인자 폴백)")
chk("target")
feat(plut, "setEnabled", True, label="(맨 마지막)")
chk("setEnabled 직후")
sleep(1.0); chk("+1.0s 프레임대기")
# 혹시 몇 번 더 눌러야 켜지나
for i in range(3):
    feat(plut, "setEnabled", True); sleep(0.4)
chk("setEnabled x3 후")

# ── 구동: internalValue 1→0→1 (별밭 밝기 따라오나) ──────────
narr("입력 1 → 0 : 별밭 어두워지나?", 1.0)
feat(plut, "setInternalValue", 0.0, Anim(3.0)); sleep(3.2); chk("internal=0")
narr("입력 0 → 1 : 별밭 밝아지나?", 1.0)
feat(plut, "setInternalValue", 1.0, Anim(3.0)); sleep(3.2)
narr("별밭 밝기가 입력 따라 변했나?", 3.5)

# 정리
feat(plut, "restore"); feat(plut, "setEnabled", False)
stars.setIntensity(1.0, Anim(1.0))

narr("ParameterizationLut — 속성 자동화", 2.5)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v3). ★리포트: "
      "①★로그의 '[enabled after ...] = ' 값들 — 어느 시점에서든 True 로 바뀌었나, 끝까지 False 인가 "
      "②★별밭이 입력 1→0→1 따라 어두워졌다 밝아졌나 (됐다/전혀) "
      "③'addTargetAttribute (automatic=True)' 가 성공했나(✓) 아니면 폴백으로 갔나 "
      "④enabled 끝까지 False + 무변화면 = 파라미터화는 쇼엔진/오퍼레이터 소관으로 확정하고 접음")

# -*- coding: utf-8 -*-
"""
earth_extras_globe.py — 지구 미검증 렌더러블 스윕 (2026-07-22, C-①)
★ Planet(Earth) 의 안 눌러본 세터들을 FadeTo 지구(외부 globe) 프레임에서 하나씩 켜 화면 변화 판별:
  setMagnetosphereIntensity(자기권) · setPolarCircleIntensity(극권) · setCloudRaininess(강수) ·
  setRockyCliffIntensity(암벽) · setTreeIntensity(나무). 각 hasattr 로 존재 확인 + 켜고 홀드 + 로그.
★ 지형/암벽/나무는 표면 근접이 필요할 수 있어 중간에 줌인. 그림자 OFF(운영표준)로 전체 밝게.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    if not hasattr(obj, fn):
        print("   – %s 없음(메서드 부재)" % fn); return False
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:100])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception:
        return "?"


# ── FadeTo 지구(외부) ───────────────────────────────────────
print("무대: 지구 globe 렌더러블 스윕")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
h = DataManager.database().data(Data.Type.PlanetType, "Earth")
if h is not None and h.action(Action.Type.FadeTo) is not None:
    h.action(Action.Type.FadeTo).trigger(); print("   FadeTo Earth")
sleep(4.0)
earth = Planet(Planet.PlanetName.Earth)
cam.setTargetHeight(30.0, Anim(0.0))
# 그림자 OFF (표면 다 보이게)
feat(earth, "setShadowStrength", 0.0, Anim(0.0))
feat(earth, "setShadowContrast", 0.0, Anim(0.0))
feat(earth, "setPlanetShineStrength", 1.0, Anim(0.0))
feat(earth, "setIntensity", 1.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 20, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── ① 자기권 ────────────────────────────────────────────────
narr("① 자기권 — setMagnetosphereIntensity", 2.5)
feat(earth, "setMagnetosphereIntensity", 1.0, Anim(1.5), label="(자기권)")
sleep(1.5); narr("★ 지구 둘레에 자기권(장) 보이나?", 5.0)
feat(earth, "setMagnetosphereIntensity", 0.0, Anim(1.0)); sleep(1.2)

# ── ② 극권 라인 ─────────────────────────────────────────────
narr("② 극권 — setPolarCircleIntensity", 2.5)
feat(earth, "setPolarCircleIntensity", 1.0, Anim(1.5), label="(극권선)")
sleep(1.5); narr("★ 남/북 극권 원(선) 보이나?", 5.0)
feat(earth, "setPolarCircleIntensity", 0.0, Anim(1.0)); sleep(1.2)

# ── ③ 구름 + 강수 ───────────────────────────────────────────
narr("③ 구름 강수 — setCloudRaininess", 2.5)
feat(earth, "setCloudsIntensity", 1.0, Anim(1.0), label="(구름 ON 먼저)")
sleep(1.2)
feat(earth, "setCloudRaininess", 1.0, Anim(1.5), label="(강수↑)")
sleep(1.5); narr("★ 구름에 비(강수) 표현 보이나?", 5.0)
feat(earth, "setCloudRaininess", 0.0, Anim(1.0)); sleep(1.0)

# ── 줌인 (표면 근접) → 암벽/나무 ────────────────────────────
narr("표면으로 줌인 (암벽/나무 보려고)", 2.0)
p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, 25.0, p.z * 0.35), Anim.cubic(4.0), -1); sleep(4.2)
feat(earth, "setElevationScale", 8.0, label="(기복 과장)")

narr("④ 암벽 — setRockyCliffIntensity", 2.5)
feat(earth, "setRockyCliffIntensity", 1.0, Anim(1.5), label="(암벽)")
sleep(1.5); narr("★ 산악/암벽 질감 보이나?", 5.0)

narr("⑤ 나무 — setTreeIntensity", 2.5)
feat(earth, "setTreeIntensity", 1.0, Anim(1.5), label="(나무)")
sleep(1.5); narr("★ 지표에 나무(식생) 보이나?", 5.0)

narr("지구 globe 렌더러블 스윕 끝", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(지구 globe 스윕). ★리포트(각각 보였나/안보였나): "
      "①자기권 ②극권선 ③구름강수 ④암벽 ⑤나무 — 5개 중 화면에 뭐가 '실제로 보였는지'만 알려줘. "
      "(로그에 '✗ 실패' 나 '– 없음' 뜬 것도 있으면 표시됨.)")

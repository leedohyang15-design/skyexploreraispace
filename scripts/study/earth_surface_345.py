# -*- coding: utf-8 -*-
"""
earth_surface_345.py — 지구 표면 근접: 구름강수/암벽/나무 재판별 (2026-07-22, C-① v2)
★ v1: ①자기권 ②극권 = 보임. ③구름강수 ④암벽 ⑤나무 = 불명(멀어서). → 지표면에 바짝 줌인해 재시도.
★ 표면 디테일용: DEM 지형모델(PlanetObserverDEM30/Topography) + setTerrainIntensity(1) + setElevationScale 크게 +
  R 을 지구반지름 ~1.1배(아주 근접) + 오블리크(B~15). 그림자 OFF. 3/4/5 각각 크게 켜고 홀드.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    if not hasattr(obj, fn):
        print("   – %s 없음" % fn); return False
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:100])); return False


print("무대: 지구 표면 근접 3/4/5")
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
cam.setTargetHeight(28.0, Anim(0.0))
feat(earth, "setShadowStrength", 0.0, Anim(0.0))
feat(earth, "setShadowContrast", 0.0, Anim(0.0))
feat(earth, "setPlanetShineStrength", 1.0, Anim(0.0))
feat(earth, "setIntensity", 1.0, Anim(0.0))
# 지형 데이터셋(DEM) + 지형 렌더 ON
for tm in ("PlanetObserverDEM30", "Topography", "PlanetObserver"):
    if hasattr(Planet.TerrainModel, tm):
        feat(earth, "setTerrainModel", getattr(Planet.TerrainModel, tm), label="(%s)" % tm); break
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
feat(earth, "setElevationScale", 14.0, label="(기복 크게)")

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 18, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 표면으로 아주 바짝 줌인 (2단계) ─────────────────────────
narr("지표면으로 바짝 줌인", 2.0)
p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, 20.0, p.z * 0.32), Anim.cubic(4.0), -1); sleep(4.2)
p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, 14.0, p.z * 0.42), Anim.cubic(4.0), -1); sleep(4.2)   # R ≈ 1.1 지구반지름
print("   현재 R=%.3f (지구반지름 단위)" % cam.positionLBR.z)

# ── ③ 구름 강수 ─────────────────────────────────────────────
narr("③ 구름 + 강수 (표면 근접)", 2.5)
feat(earth, "setCloudsIntensity", 1.0, Anim(1.0))
feat(earth, "setCloudModel", getattr(Planet.CloudModel, "Volumetric", None), label="(입체구름)")
feat(earth, "setCloudRaininess", 1.0, Anim(1.5), label="(강수 최대)")
sleep(1.8); narr("★ 구름 아래 비(강수 줄기) 보이나?", 6.0)
feat(earth, "setCloudRaininess", 0.0, Anim(0.5)); feat(earth, "setCloudsIntensity", 0.15, Anim(1.0)); sleep(1.2)

# ── ④ 암벽 ──────────────────────────────────────────────────
narr("④ 암벽 — setRockyCliffIntensity (근접)", 2.5)
feat(earth, "setRockyCliffIntensity", 1.0, Anim(1.5))
sleep(1.8); narr("★ 산악 암벽/절벽 질감 보이나?", 6.0)

# ── ⑤ 나무 ──────────────────────────────────────────────────
narr("⑤ 나무 — setTreeIntensity (근접)", 2.5)
feat(earth, "setTreeIntensity", 1.0, Anim(1.5))
sleep(1.8); narr("★ 지표에 나무/식생 보이나?", 6.0)

narr("표면 근접 3/4/5 끝", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(표면 345). ★리포트: 근접 줌인 상태에서 ③구름강수 ④암벽 ⑤나무 중 '실제로 보인' 게 있나 "
      "(로그 '현재 R=' 값도 — 얼마나 근접했는지). 그래도 안 보이면 = Terrain View(오퍼레이터 비행) 전용으로 판정.")

# -*- coding: utf-8 -*-
"""
moon_terrain.py — 달 지형 클로즈업 (2026-07-15, 미사용 코드 중심)
★ 달(Satellite)에선 처음 쓰는 지형 코드 (우린 달은 '위상'만 해봤음):
  setTerrainModel(Satellite.TerrainModel) — 탐사선별 달 지도(Clementine/LRO 등) ·
  setElevationScale(고도 과장) · setTerrainIntensity.
★ 운영 표준 적용: 지형 보여줄 땐 그림자 OFF (setShadowStrength/Contrast 0 + setPlanetShineStrength 1)
  = 근면 전체가 밝게(보름달 룩) → 바다(어두운 현무암)·크레이터 광조(Tycho 등)가 다 보임.
  접근/줌 = FadeTo(SatelliteType "Moon") → setPositionR(읽은값×배율), 중앙 고정.
  TerrainModel enum 은 dir() 프로브.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
moon = Satellite(Satellite.SatelliteName.Moon)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(fn, *args, label=""):
    try:
        getattr(moon, fn)(*args)
        print("   ✓ %s%s %s" % (fn, tuple(str(a)[:18] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def probe_enum(name, cls):
    try:
        mem = [m for m in dir(cls) if not m.startswith("_") and not m.islower() and "Invalid" not in m]
        print("[enum] %s: %s" % (name, mem)); return mem
    except Exception as e:
        print("[enum] %s 실패: %s" % (name, e)); return []


# ── enum 프로브 ─────────────────────────────────────────────
terrain_models = probe_enum("Satellite.TerrainModel", getattr(Satellite, "TerrainModel", None)) if hasattr(Satellite, "TerrainModel") else []

# ── 무대(지상) & 인트로 ─────────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
try:
    moon.setIntensity(1.0, Anim(0.0))
except Exception:
    pass
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.9, 0.95))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("달 — 가장 가까운 세계의 표면"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 달로: reset + FadeTo (SatelliteType "Moon") ─────────────
narr("달로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.SatelliteType, "Moon")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Moon")
else:
    print("   ⚠️ FadeTo Moon 미지원")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
feat("setIntensity", 1.0, Anim(0.0))
# ★ 운영 표준: 지형 보여줄 땐 그림자 OFF = 근면 전체가 밝게(보름달 룩)
feat("setShadowStrength", 0.0, Anim(1.0), label="(그림자 OFF)")
feat("setShadowContrast", 0.0, Anim(1.0), label="(그림자 대비 0)")
feat("setPlanetShineStrength", 1.0, Anim(1.0), label="(그늘면도 밝게)")
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)

# ── 줌인 (중앙 고정, 읽은 R × 배율) ─────────────────────────
narr("표면이 보이게 — 가운데 그대로 크게", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.55), Anim.cubic(4.5), -1); sleep(4.7)
    rlog("줌 후")
except Exception as e:
    print("   줌 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)

# ── ★ 탐사선별 달 지도 (미사용 setTerrainModel) ─────────────
#   ⚠️ 실측: Satellite 엔 setTerrainIntensity 없음(Planet 전용) → setTerrainModel 로 바로 교체.
narr("탐사선이 만든 달 지도 — setTerrainModel", 2.5)
if terrain_models:
    t2 = InsertText(InsertText.InsertTextName(2))
    cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
    t2.setPosition(Vec(0, 18, 0)); t2.setSize(0.04); t2.setDistance(1.0, Anim(0.0))
    t2.setColor(Vec(0.85, 0.9, 1.0))
    for tm in terrain_models:
        if feat("setTerrainModel", getattr(Satellite.TerrainModel, tm), Anim(1.5), label="(TerrainModel=%s)" % tm):
            t2.setText("TerrainModel: %s" % tm); t2.setIntensity(1.0, Anim(0.5))
            sleep(4.5)
    t2.setIntensity(0.0, Anim(1.0))
else:
    print("   ⚠️ Satellite.TerrainModel enum 비어있음 — [enum] 로그 확인")

# ── 크레이터 안내 (내레이션) ────────────────────────────────
narr("어두운 '바다' — 고대 용암이 굳은 현무암 평원", 4.0)
narr("밝은 광조 크레이터 — 티코, 코페르니쿠스", 4.0)

# ── ★ 고도 과장 (미사용 setElevationScale) — 근접 A/B ──────
narr("고도를 과장 — 크레이터 가장자리가 솟는다", 2.0)
for es in (1.0, 12.0, 1.0, 12.0):
    feat("setElevationScale", es, Anim(3.0), label="(고도 ×%.0f)" % es); sleep(3.3)
feat("setElevationScale", 1.0, Anim(2.5), label="(고도 원복)"); sleep(2.7)

# ── 정리 ────────────────────────────────────────────────────
narr("맨눈으로도 보이는, 우리의 유일한 자연 위성", 3.5)
t1.setText("달 — 38만 km 밖의 이웃"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①Satellite.TerrainModel enum 멤버 뭐뭐였나([enum] 로그) ②setTerrainModel 로 달 표면 지도가 바뀌나 "
      "③그림자 OFF 로 근면 전체(바다·광조) 밝게 보이나 ④중앙 고정(이동 없음)인가 "
      "⑤setElevationScale 로 크레이터 기복(가장자리)이 보이나 ⑥R/구도 조정?")

# -*- coding: utf-8 -*-
"""
mars_terrain.py — 화성 지형 클로즈업 (2026-07-15, 미사용 코드 중심)
★ 행성에선 처음 쓰는 지형 코드 (Pluto 에서만 써봄):
  setTerrainModel(Planet.TerrainModel) — 표면 모델 · setTerrainIntensity — 지형 표시 ·
  setElevationScale(고도 과장) — 산·협곡을 부풀려 3D 기복을 극대화(핵심 실험).
★ 접근/줌 = 확정된 암석행성 레시피: reset → FadeTo Mars(북극 도킹 R=4) → setPositionR(읽은값×배율) 줌.
  TerrainModel enum 은 dir() 로 프로브해 로그로 학습. 고도 과장 = 1→8 스윕(Pluto 서 8배 동작 확인).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
mars = Planet(PN.Mars)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(fn, *args, label=""):
    try:
        getattr(mars, fn)(*args)
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
terrain_models = probe_enum("TerrainModel", getattr(Planet, "TerrainModel", None)) if hasattr(Planet, "TerrainModel") else []

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
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.7, 0.5))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("화성 — 붉은 행성의 지형"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 화성으로: reset + FadeTo (암석행성 = 북극 도킹 R=4) ──────
narr("화성으로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Mars")
else:
    print("   ⚠️ FadeTo Mars 미지원")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
mars.setIntensity(1.0, Anim(0.0))
# ★ 지형을 보여줄 땐 '그림자(야간면) OFF' = 전체 표면이 밝게 (사용자 요청)
#   setShadowStrength(0)+setShadowContrast(0) = 낮/밤 경계(터미네이터) 제거, setPlanetShineStrength(1)=야간면 발광.
feat("setShadowStrength", 0.0, Anim(1.0), label="(그림자 OFF)")
feat("setShadowContrast", 0.0, Anim(1.0), label="(그림자 대비 0)")
feat("setPlanetShineStrength", 1.0, Anim(1.0), label="(야간면도 밝게)")
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)

# ── 줌인 (중앙 고정 — B 안 바꿈) ────────────────────────────
#   ⚠️ 사용자 지적: 그림자만 끄면 표면 다 보이는데 비스듬히 기울여 화성을 옆으로 옮긴 건 불필요.
#   → B(시점 위도)는 그대로 두고 R 만 당겨 '가운데 그대로, 크게만'. (그림자 OFF 라 표면 전체가 밝음.)
narr("표면이 보이게 — 가운데 그대로 크게", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.55), Anim.cubic(4.5), -1); sleep(4.7)   # R 4→2.2 (중앙 유지)
    rlog("줌 후(중앙)")
except Exception as e:
    print("   줌 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.2)); sleep(1.3)

# ── ★ 지형 모델 (미사용 setTerrainModel) ───────────────────
narr("표면 모델 — 처음 쓰는 setTerrainModel", 2.5)
feat("setTerrainIntensity", 1.0, Anim(2.0), label="(지형 표시 ON)"); sleep(2.0)
if terrain_models:
    t2 = InsertText(InsertText.InsertTextName(2))
    cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
    t2.setPosition(Vec(0, 18, 0)); t2.setSize(0.04); t2.setDistance(1.0, Anim(0.0))
    t2.setColor(Vec(1.0, 0.8, 0.6))
    for tm in terrain_models:
        if feat("setTerrainModel", getattr(Planet.TerrainModel, tm), Anim(1.5), label="(TerrainModel=%s)" % tm):
            t2.setText("TerrainModel: %s" % tm); t2.setIntensity(1.0, Anim(0.5))
            sleep(4.5)
    t2.setIntensity(0.0, Anim(1.0))
else:
    print("   ⚠️ TerrainModel enum 비어있음 — [enum] 로그 확인")

# ── ★★ 고도 과장 (미사용 setElevationScale) — 근접 줌에서 '티 남'(사용자 확인) ────
#   ⚠️ 그림자 OFF 라 기복 그림자는 안 생김 → 고도 과장은 주로 '가장자리(limb) 실루엣'이 울퉁불퉁해지며 보임.
#   중앙 고정 유지(이동 안 함) + DEM 모델 + 1↔크게 A/B. (원반 전체가 보이는 R 이라 limb 울퉁불퉁이 드러남.)
narr("고도 데이터(DEM) 모델 — 가장자리가 울퉁불퉁", 2.0)
for cand in ("Topography", "Geoid", "PlanetObserverDEM30", "MOC", "CTX", "Themis"):
    if cand in terrain_models:
        if feat("setTerrainModel", getattr(Planet.TerrainModel, cand), Anim(1.5), label="(DEM=%s)" % cand):
            print("   DEM 모델=%s" % cand); break
sleep(2.0)
narr("고도를 과장 — 가장자리 지형이 솟아오른다", 2.0)
# 중앙 그대로(이동 없음). 1 ↔ 크게 A/B 로 limb 실루엣 변화를 눈에.
for es in (15.0, 1.0, 15.0, 1.0, 15.0):
    feat("setElevationScale", es, Anim(3.0), label="(고도 ×%.0f)" % es); sleep(3.3)
narr("올림푸스 몬스 — 태양계에서 가장 높은 화산(에베레스트 3배)", 4.0)
feat("setElevationScale", 1.0, Anim(2.5), label="(고도 원복)"); sleep(2.7)

# ── 정리 ────────────────────────────────────────────────────
narr("붉은 먼지 아래 잠든 거대한 지형", 3.0)
t1.setText("화성 — 언젠가 우리가 밟을 땅"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 확정: ①그림자 OFF 로 화성 전체 표면이 밝게(중앙 고정, 이동 없음) ②TerrainModel 20종 교체 동작 "
      "③setElevationScale = 중앙뷰+그림자OFF 에선 limb(가장자리) 실루엣으로 기복 보임(내부 그림자는 없음). "
      "이동 없이 가운데 그대로인가 + limb 울퉁불퉁 A/B 보이나 확인.")

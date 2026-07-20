# -*- coding: utf-8 -*-
"""
climate_zones.py — 지구의 기후대: 적도·회귀선·극권 (2026-07-16, 안 쓴 라인레이어 API)
★ 안 쓴 코드: 지구 위도선 레이어 — `setEquatorialSyncTropicsIntensity`(남·북 회귀선 ±23.4°) ·
  `setEquatorialSyncPolarCirclesIntensity`(남·북 극권 ±66.5°) · `setEquatorialSyncGraticuleIntensity`(위경도 격자).
  (FadeTo 프레임 = EquatorialSync → 이 'EquatorialSync*' 라인들이 지구본 표면에 딱 그려짐.)
★ 자전축이 23.4° 기울어서 생기는 지도의 기준선들:
  · 적도(0°) · 회귀선(±23.4°) = 태양이 '머리 바로 위(천정)'까지 오는 한계 · 극권(±66.5°) = 백야/극야가 생기는 한계.
★ 카메라: FadeTo Earth(외부 도킹) + 그림자 OFF(전체 밝게) + 오블리크 틸트(라인이 지구를 감는 링으로 보이게).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
earth = Planet(PN.Earth)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def rlog(tag):
    try:
        p = cam.positionLBR; print("   [%s] L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] %s" % (tag, e))


def dark_clamp(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(step); t += step


# ── 위도선 API 프로브 ───────────────────────────────────────
zl = [m for m in dir(earth) if any(k in m.lower() for k in ("tropic", "polarcircle", "graticule", "circle", "equatorialsync"))]
print("   [기후대/위도선 메서드] %s" % zl)

# ── 무대: 우주(지구로) ──────────────────────────────────────
print("무대: 우주 — 지구의 기후대")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))

# ── FadeTo 지구 ─────────────────────────────────────────────
h = DataManager.database().data(Data.Type.PlanetType, "Earth")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); dark_clamp(4.5); print("   FadeTo Earth")
cam.setTargetHeight(30.0, Anim(0.0))
rlog("FadeTo 후")

# ── 지구 렌더: 그림자 OFF(전체 밝게) + 블루마블 + 구름 살짝 ─
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(대기)")
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0), label="(지표)")
for tm in ("BMNG_Ocean", "BMNG_Seasons"):
    if hasattr(Planet.TerrainModel, tm):
        if feat(earth, "setTerrainModel", getattr(Planet.TerrainModel, tm), label="(블루마블)"): break
feat(earth, "setShadowStrength", 0.0, Anim(0.0), label="(그림자 OFF)")
feat(earth, "setShadowContrast", 0.0, Anim(0.0))
feat(earth, "setPlanetShineStrength", 1.0, Anim(0.0), label="(전체 밝게)")

# ── 오블리크 틸트 + 바짝 줌인(위도 링이 또렷하게 = v2: R 크게) ─
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 22.0, p.z * 0.45), Anim.cubic(4.5), -1); dark_clamp(4.7)  # B90→B22, R4→1.8 지구 크게
    rlog("오블리크 후")
except Exception as e:
    print("   오블리크 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setColor(Vec(1.0, 0.95, 0.6)); t1.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("우주에서 본 지구 — 지도 위엔 보이지 않는 선들이 있다", 4.0)

# ── ① 위경도 격자 ──────────────────────────────────────────
narr("먼저 위도와 경도 — 지구를 나누는 그물", 3.5)
feat(earth, "setEquatorialSyncGraticuleIntensity", 0.5, Anim(2.0), label="(위경도 격자)")
sleep(2.2)

# ── ② 적도(적도 그리드로 강조) ─────────────────────────────
narr("한가운데 굵은 선 — 적도(0°), 가장 더운 곳", 4.0)
feat(earth, "setEquatorialGridIntensity", 0.4, Anim(2.0), label="(적도면 강조)")
sleep(2.0)

# ── ③ ★ 회귀선(±23.4°) ─────────────────────────────────────
narr("적도 위아래로 두 선 — 남·북 회귀선(±23.4°)", 4.0)
feat(earth, "setEquatorialSyncTropicsIntensity", 1.0, Anim(2.5), label="(★ 회귀선)")
sleep(2.6)
narr("태양이 '머리 바로 위'까지 오는 한계 — 자전축이 23.4° 기운 증거", 5.0)

# ── ④ ★ 극권(±66.5°) ───────────────────────────────────────
narr("극에 가까운 두 원 — 남·북 극권(±66.5°)", 4.0)
feat(earth, "setEquatorialSyncPolarCirclesIntensity", 1.0, Anim(2.5), label="(★ 극권)")
sleep(2.6)
narr("이 안쪽에선 여름엔 해가 안 지고(백야), 겨울엔 안 뜬다(극야)", 5.0)

# ── ⑤ 자전축 = 이 모든 선의 원인 ───────────────────────────
narr("이 모든 선의 원인 — 23.4° 기울어진 자전축", 4.0)
feat(earth, "setEquatorialPolePointerIntensity", 1.0, Anim(2.0), label="(자전축 극 포인터)")
sleep(2.2)
narr("기울어졌기에 계절이 있고, 회귀선과 극권이 생긴다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("적도·회귀선·극권 — 하늘이 땅에 그린 기후의 지도", 4.5)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v2 바짝 줌인): ①(확인)위도선/그리드 다 뜸 ②★이번엔 지구가 커져서(R2.8→1.8) 회귀선·극권 링이 "
      "또렷하게 읽히나 — 핵심 ③선 색/굵기로 회귀선↔극권↔격자 구분되나 ④자전축 극 포인터 OK ⑤더 키울까/이대로 완성?")

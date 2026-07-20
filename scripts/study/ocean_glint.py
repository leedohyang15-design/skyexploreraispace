# -*- coding: utf-8 -*-
"""
ocean_glint.py — 바다의 윤슬: 태양이 비친 바다 (2026-07-16, 안 쓴 API=setWaterSpecularIntensity)
★ 안 쓴 코드: `setWaterSpecularIntensity`(바다 정반사=윤슬) + `setWaterSpecularShininess`(반짝임 날카로움).
  우주에서 지구 바다에 햇빛이 거울처럼 반사돼 생기는 밝은 점(sun glint) — ISS 사진의 그 효과.
★ 은근할 수 있어 'specular 0→1 A/B'로 확 켜지는 대조 + 지구 미세 자전으로 반짝점이 바다 위 미끄러짐.
★ ⚠️ 윤슬은 '태양 방향 정반사'라 실제 조명(그림자 ON)이 있어야 형성됨 → 그림자 OFF(전체 균일밝기) 아님!
  대신 낮면(햇빛 받는 바다)이 화면에 오도록 위상 살짝 맞춤. 구름은 낮춰 바다가 보이게.
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
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
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


# ── 윤슬/바다 메서드 프로브 ─────────────────────────────────
wm = [m for m in dir(earth) if any(k in m.lower() for k in ("water", "specular", "sea"))]
print("   [바다/윤슬 메서드] %s" % wm)

# ── 무대: 우주(지구로) ──────────────────────────────────────
print("무대: 우주 — 바다의 윤슬")
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

# ── 지구 렌더: 그림자 ON(실제 조명=윤슬 형성) + 바다 + 구름↓ ─
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(대기)")
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0), label="(지표)")
for tm in ("BMNG_Ocean", "BMNG_Seasons"):
    if hasattr(Planet.TerrainModel, tm):
        if feat(earth, "setTerrainModel", getattr(Planet.TerrainModel, tm), label="(블루마블)"): break
feat(earth, "setCloudsIntensity", 0.2, Anim(0.0), label="(구름 낮춤=바다 보이게)")
# ── ★ v2: 바다 렌더링 모드 = 반사 모드라야 윤슬(specular)이 켜질 수 있음 ──
if hasattr(Planet, "SeaLevelRenderingMode"):
    print("   [SeaLevelRenderingMode enum] %s"
          % [m for m in dir(Planet.SeaLevelRenderingMode) if not m.startswith("__") and m[0].isupper()])
    for md in ("Specular", "Reflective", "Realistic", "Advanced", "Ocean", "Water", "Default"):
        if hasattr(Planet.SeaLevelRenderingMode, md):
            if feat(earth, "setSeaLevelRenderingMode", getattr(Planet.SeaLevelRenderingMode, md), label="(★ 바다 렌더 모드=%s)" % md): break
# ★ 그림자 ON (윤슬은 태양 방향 정반사라 실제 조명 필요) + 밤면 더 어둡게(윤슬 대비 ↑)
feat(earth, "setShadowStrength", 1.0, Anim(0.0), label="(그림자 ON=조명)")
feat(earth, "setShadowContrast", 1.0, Anim(0.0), label="(명암 대비 ↑ = 터미네이터 선명)")
feat(earth, "setPlanetShineStrength", 0.1, Anim(0.0), label="(밤면 어둡게 = 윤슬 대비)")

# ── 오블리크 틸트 + 줌인 ────────────────────────────────────
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 16.0, p.z * 0.55), Anim.cubic(4.0), -1); dark_clamp(4.2)   # B16, R4→2.2
    rlog("오블리크 후")
except Exception as e:
    print("   오블리크 실패: %s" % e)

# ── 낮면(햇빛 받는 바다)이 화면에 오게 위상 살짝 (자전 정지+날짜) ─
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial"):
    try:
        ip = earth.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(0.0), ip)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 16, 12, 0, 0, tz, Anim(0.0)); sleep(0.5)
feat(earth, "setRotationSpeedScale", 0.0, label="(자전 정지=위상만)")

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setColor(Vec(0.8, 0.95, 1.0)); t1.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("우주에서 본 지구 — 낮과 밤의 경계, 그 바다", 4.0)
# 낮면이 앞에 오도록 태양각 살짝(자전 정지라 표면 안 어지럽고 위상만 이동)
dm.setDateTime(2026, 7, 18, 12, 0, 0, tz, Anim(8.0)); sleep(8.3)   # 태양각 조금 이동 → 낮 바다 앞으로

# ── ★ 윤슬 A/B: specular 0 → 1 (확 켜지는 대조) ─────────────
narr("바다는 거울이다 — 햇빛을 정면으로 되쏜다", 3.5)
feat(earth, "setWaterSpecularIntensity", 0.0, Anim(0.5), label="(윤슬 OFF)")
sleep(1.0)
feat(earth, "setWaterSpecularShininess", 1.0, Anim(0.5), label="(반짝임 날카롭게)")
feat(earth, "setWaterSpecularIntensity", 1.0, Anim(4.0), label="(★★ 윤슬 ON = 바다에 태양 반짝점)")
sleep(4.3)
narr("저 밝은 점 — 태양이 바다에 비친 '윤슬(sun glint)'", 4.5)

# ── ★ 미세 자전: 반짝점이 바다 위를 미끄러진다 ─────────────
narr("지구가 돌면, 반짝이는 점도 바다 위를 미끄러진다", 3.5)
feat(earth, "setRotationSpeedScale", 4.0, label="(자전 배율 — 날짜Δ 최소로)")
dm.setDateTime(2026, 7, 18, 20, 0, 0, tz, Anim(24.0)); sleep(25.0)   # +8h × 4 = ~1.3바퀴, 별 거의 고정
dm.stop()
feat(earth, "resetRotationSpeedScale", label="(자전 원복)")
narr("바람이 잔잔한 바다일수록, 윤슬은 더 또렷하다", 4.0)

# ── 정리 ────────────────────────────────────────────────────
narr("바다의 윤슬 — 창백한 푸른 점이 반짝이는 순간", 4.5)
feat(earth, "setWaterSpecularIntensity", 0.0, Anim(3.0))
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v2 바다 렌더모드): ①★★이번엔 바다 렌더 모드를 반사로 바꿔서 윤슬 A/B(0→1) 때 반짝점이 생기나 — 핵심 "
      "②★★로그 [SeaLevelRenderingMode enum] 을 보내줘 — 어떤 모드들이 있는지(내가 고른 게 맞았나) "
      "③밤면 어둡게+대비↑ 로 윤슬이 더 도드라지나 ④자전 때 미끄러지나 "
      "⑤그래도 안 보이면 이 효과는 '근접 지표 뷰' 전용일 수 있음(우주 원반선 미지원) — 그때는 접고 다음으로")

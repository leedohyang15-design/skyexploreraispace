# -*- coding: utf-8 -*-
# [AI 생성 테스트] 요청: "청주 밤하늘에 여름 대삼각형 + 별 크고 반짝이게"
# → AI_SYSTEM_PROMPT.md 만 참고해 생성 (골격A + ASTERISM_STr + Stars 반짝임 + Lut + 자막B)
from skyExplorer import *
from studio import *
from Initialization import *

# ── 골격(A): 청주 밤하늘 ───────────────────────────────────
cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(1.5)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
earth.setElevationScale(0.0)
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 22, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)   # 여름 밤 22시(=13 UTC)
# 여름 대삼각형은 여름밤 천정 부근 → 하늘 위쪽을 봄
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(60.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)

# ── 자막(B) ────────────────────────────────────────────────
t = InsertText(InsertText.InsertTextName(1))
cam.addChild(t.id, Camera.CameraPort.FixedForeground)
t.setPosition(Vec(0, 18, 0)); t.setSize(0.052); t.setColor(Vec(1.0, 1.0, 0.55)); t.setDistance(1.0, Anim(0.0))


def narr(s, d=3.0):
    t.setText(s); t.setIntensity(1.0, Anim(1.0)); sleep(d)


# ── 별을 크고 반짝이게 (Stars + Lut) ───────────────────────
narr("청주 여름 밤하늘", 3.0)
orig_amp = stars.twinklingAmplitude
stars.setTwinklingAmplitude(2.0, Anim(2.0))              # 반짝임 증폭(운영권장 ~1.2 이상)
stars.setPointSaturation(3.0, Anim(2.0))                 # 별색 채도 ↑
lut = Lut(Lut.LutName.Lut001)
orig_ss = lut.spriteScale
lut.setSpriteScale(2.2, Anim(2.0))                       # 별 크게(과하면 하얘지니 2.2)
sleep(2.2)

# ── 여름 대삼각형 (성군 프리셋) ────────────────────────────
narr("여름 대삼각형 — 베가·데네브·알타이르", 3.0)
tri = Constellation(Constellation.ConstellationName.ASTERISM_STr)
tri.setLinesIntensity(1.0, Anim(1.5))
tri.setLabelIntensity(0.9, Anim(1.5))
sleep(2.0)
# 삼각형 꼭짓점 세 별 이름표
for nm in ("Vega", "Deneb", "Altair"):
    if hasattr(IndividualStar.IndividualStarName, nm):
        s = IndividualStar(getattr(IndividualStar.IndividualStarName, nm))
        s.setPointerIntensity(1.0, Anim(1.0)); s.setLabelIntensity(1.0, Anim(1.0))
narr("세 별을 이으면 거대한 삼각형", 4.5)

# ── 감상 (선만 남기고 자막 내림) ───────────────────────────
narr("여름철 밤하늘의 길잡이", 4.0)
t.setIntensity(0.0, Anim(1.5)); sleep(1.6)
narr(" ", 3.0)

# ── 정리 (원복) ────────────────────────────────────────────
stars.setTwinklingAmplitude(float(orig_amp) if isinstance(orig_amp, (int, float)) else 1.0, Anim(1.0))
lut.setSpriteScale(float(orig_ss) if isinstance(orig_ss, (int, float)) else 6.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("[AI 생성 테스트] 여름 대삼각형 — 정제 프롬프트만으로 생성. 별 크기/반짝임/삼각형 선·라벨 확인 요망.")

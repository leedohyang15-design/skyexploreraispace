# -*- coding: utf-8 -*-
"""
clouds_weather.py — 살아있는 지구: 구름과 날씨 (2026-07-16, 안 쓴 구름 상세 API 클러스터)
★ 안 쓴 코드(구름 상세): `setCloudModel` · `setCloudCoverage`(구름량) · `setCloudSpeed`(흐름 속도) ·
  `setCloudThickness`(두께) · `setCloudAltitude`(고도) · `setCloudRaininess`(강수) · `setCloudDirection`(방향).
  (setCloudsIntensity 는 earth_city_lights 에서 렌더 검증됨 → 그 위에 '상세+움직임'을 얹는다.)
★ 무지개(흐릿) 대신 '확실히 보이는' 걸로: 우주 지구 클로즈업 + 그림자 OFF(전체 밝게 = 구름 다 보임) +
  setCloudSpeed↑ & 시간가속 → 구름이 소용돌이치며 흐름(움직임이라 눈에 확 들어옴).
★ 카메라: FadeTo Earth(외부 도킹). 추적/줌락 불필요 = 견고.
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


def cset(fn, val, dur=2.0, label=""):
    """구름 세터 — 시그니처 불명이라 (val,Anim)→(val) 순으로 시도."""
    last = None
    for args in ((val, Anim(dur)), (val,)):
        try:
            getattr(earth, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
        except Exception as e:
            last = e
    print("   ✗ %s 실패: %s" % (fn, last)); return False


def rlog(tag):
    try:
        p = cam.positionLBR; print("   [%s] L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] %s" % (tag, e))


def dark_clamp(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(step); t += step


# ── 구름 API 프로브 ─────────────────────────────────────────
cm = [m for m in dir(earth) if "cloud" in m.lower()]
print("   [구름 메서드] %s" % cm)
cmodels = [m for m in dir(Planet.CloudModel) if not m.startswith("__")] if hasattr(Planet, "CloudModel") else []
print("   [CloudModel enum] %s" % cmodels)

# ── 무대: 우주(지구로) ──────────────────────────────────────
print("무대: 우주 — 살아있는 지구, 구름과 날씨")
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

# ── 지구 렌더: 그림자 OFF(전체 밝게=구름 다 보임) + 지표 ────
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(대기 = 푸른 림)")
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0), label="(지표)")
for tm in ("BMNG_Ocean", "BMNG_Seasons"):
    if hasattr(Planet.TerrainModel, tm):
        if feat(earth, "setTerrainModel", getattr(Planet.TerrainModel, tm), label="(블루마블)"): break
# 그림자 OFF (운영 표준 클로즈업 — 구름/지표 전체가 보이게)
feat(earth, "setShadowStrength", 0.0, Anim(0.0), label="(그림자 OFF)")
feat(earth, "setShadowContrast", 0.0, Anim(0.0))
feat(earth, "setPlanetShineStrength", 1.0, Anim(0.0), label="(전체 밝게)")

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setColor(Vec(0.8, 0.9, 1.0)); t1.setDistance(20.0, Anim(0.0))


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)
narr("우주에서 본 지구 — 푸른 바다와 흰 구름의 행성", 3.5)

# ── ★ 지구로 줌인 (크게 = 구름 변화가 보이게) — v1 지구 작아서 안 보였음 ──
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.5), Anim.cubic(5.0), -1); sleep(5.3)   # R 4→2, 지구 2배 크게
    rlog("줌인 후")
except Exception as e:
    print("   줌인 실패: %s" % e)

# ── ★ 구름 '없음→가득' 페이드인 (밀려오는 게 눈에 보이게) ──
#   ⚠️ v2 교훈: setCloudCoverage 램프는 화면 변화 미미(사용자 "잘 모르겠다"). 커버리지는 미리 최대로 두고,
#   '구름 렌더 마스터'인 setCloudsIntensity 를 0→1 로 페이드인 → 구름이 없다가 나타나 뒤덮임(확실히 보임).
narr("맑은 하늘에서 시작해 — 구름이 밀려온다", 3.0)
cset("setCloudCoverage", 1.0, 0.5, "(구름량 최대로 미리)")
cset("setCloudsIntensity", 0.0, 0.5, "(구름 숨김)")
sleep(0.8)
cset("setCloudsIntensity", 1.0, 5.5, "(★ 구름 0→1 페이드인 = 밀려와 뒤덮임)")
sleep(5.8)
narr("구름이 지구를 뒤덮는다 — 날씨가 만들어지는 층", 4.0)

# ── ★ 구름 '모델' A/B (룩이 바뀌는 게 보이게 — enum 에 Volumetric 有) ─
narr("구름 모델을 바꿔본다 — 평면에서 입체로", 3.0)
for tm, ko in [("DefaultCloud", "기본 구름"), ("Volumetric", "볼류메트릭 — 입체 구름"),
               ("VolumetricLowRes", "볼류메트릭(저해상)")]:
    if hasattr(Planet.CloudModel, tm):
        feat(earth, "setCloudModel", getattr(Planet.CloudModel, tm), label="(모델=%s)" % tm)
        narr("구름 모델: %s" % ko, 3.8)

# ── 두께/고도 최대 ──────────────────────────────────────────
cset("setCloudThickness", 1.0, 2.5, "(두께 최대)")
cset("setCloudAltitude", 1.0, 2.5, "(고도 최대)")
sleep(2.0)

# ── ★ 흐름: setCloudSpeed↑ + 큰 시간가속(+14일) = 구름 이동 ─
narr("시간을 크게 흘리면 — 구름이 살아 움직인다", 3.0)
cset("setCloudSpeed", 3.0, 1.5, "(★ 흐름 빠르게)")
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 9, 15, 12, 0, 0, tz, Anim(30.0)); sleep(31.0)   # +14일 = 구름 크게 이동/생성
dm.stop()
narr("고기압과 저기압, 태풍의 소용돌이 — 끊임없이 바뀐다", 4.5)

# ── ★ 폭풍(강수) 강조 ───────────────────────────────────────
narr("구름이 두꺼워지면 비가 된다", 3.0)
cset("setCloudRaininess", 1.0, 2.5, "(★ 강수 ↑ = 폭풍)")
sleep(3.0)
narr("이 얇은 대기의 소용돌이가, 지구의 모든 날씨다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("살아있는 지구 — 구름에 덮인 창백한 푸른 점", 4.0)
cset("setCloudRaininess", 0.0, 2.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v3 페이드인+모델A/B): ①(확인)모델 A/B 기본↔Volumetric 확 바뀜=하이라이트 "
      "②★이번엔 '구름 없음→가득' 페이드인(setCloudsIntensity 0→1)이 '밀려오는' 걸로 보이나 — 커버리지 대신 이걸로 교체 "
      "③+14일 가속 때 구름 흐르나 ④강수 티 나나 ⑤이제 완성인가?")

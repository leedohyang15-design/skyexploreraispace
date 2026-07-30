# -*- coding: utf-8 -*-
# 재도전 ③ — "아직도 안 되던 것들"을 '완전히 다른 각도'로 (ParameterizationLut / 지구표면D / SkySurvey)
# 각 항목 [판정] + 화면 확인. 특히 A의 WeatherEffectRain/Snow 가 되면 '날씨(비/눈)'까지 얻음.
from skyExplorer import *
from studio import *
from Initialization import *

def hr(t): print("\n========== %s ==========" % t)
dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# 공통 지상 밤하늘
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception: pass
uni = Universe(Universe.UniverseName.MainUniverse); uni.setGlobalIntensity(1.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
Constellation(Constellation.ConstellationName.Ori).setLinesIntensity(0.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))

# ── A) ParameterizationLut '프리셋 슬롯' 구동 (수동타겟 대신 미리 배선된 것) ──
hr("A) ParameterizationLut 프리셋 슬롯 (날씨 비/눈 포함)")
# A-0) 먼저 enum 에 어떤 프리셋 이름이 있는지 덤프
preset_names = []
try:
    for n in dir(ParameterizationLut.ParameterizationLutName):
        if not n.startswith("__"):
            preset_names.append(n)
    print("  슬롯 이름 목록:", preset_names)
except Exception as e:
    print("  이름 덤프 예외:", e)

# A-1) 관심 프리셋(있으면) 구동: 날씨 비→눈, 별자리선, 슬라이더
def try_preset(match_kw, label):
    hit = None
    for n in preset_names:
        if match_kw.lower() in n.lower():
            hit = n; break
    if not hit:
        print("  [%s] 매칭 슬롯 없음(kw=%s)" % (label, match_kw)); return
    try:
        pl = ParameterizationLut(getattr(ParameterizationLut.ParameterizationLutName, hit))
        pl.setEnabled(True); sleep(1.2)
        print("  [%s] 슬롯=%s enabled=%s → internalValue 0→1 스윕(6초)" % (label, hit, getattr(pl,"enabled","?")))
        pl.setInternalValue(0.0, Anim(0.0)); sleep(0.6)
        pl.setInternalValue(1.0, Anim(4.0)); sleep(5.0)
        print("    [판정-%s] 화면에 %s 효과가 나타났나? (비/눈이 내리거나, 별자리선이 켜지거나)" % (label, label))
        try: pl.restore()
        except Exception: pass
    except Exception as e:
        print("  [%s] 구동 예외: %s" % (label, e))

try_preset("Rain",  "비(Rain)")
try_preset("Snow",  "눈(Snow)")
try_preset("ConstellationLines", "별자리선")

# ── B) 지구 표면 D : 각 효과의 '전제조건'을 깔고 재시도 ──────────────────────
hr("B) 지구 표면 디테일 (전제조건 세팅 후)")
try:
    SceneGraph().reset(1); sleep(1.5)
    cam = Camera(Camera.CameraName.MainCamera)
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
    DataManager.database().data(Data.Type.PlanetType, "Earth").action(Action.Type.FadeTo).trigger()
    sleep(4.5)
    e = Planet(Planet.PlanetName.Earth)
    e.setShadowStrength(0.0, Anim(0.0)); e.setShadowContrast(0.0, Anim(0.0)); e.setPlanetShineStrength(1.0, Anim(0.0))
    # B-1) 비(raininess): 구름을 Volumetric 으로 먼저 켜야 강수가 붙을 수 있음
    try:
        e.setCloudsIntensity(1.0, Anim(0.0))
        e.setCloudModel(Planet.CloudModel.Volumetric)
        e.setCloudCoverage(1.0, Anim(0.0)); sleep(1.0)
        e.setCloudRaininess(1.0, Anim(1.0)); print("  구름ON+Volumetric+coverage 후 raininess(1.0) — 6초"); sleep(6.0)
        print("    [판정-비] 구름 아래 강수(빗줄기)가 보이나?")
    except Exception as ex: print("  raininess 세트 예외:", ex)
    # B-2) 절벽/식생: DEM 지형 + 표면 초근접(R 1.03) + 오블리크
    try:
        e.setCloudsIntensity(0.0, Anim(0.0))
        e.setTerrainModel(Planet.TerrainModel.PlanetObserverDEM30)
        e.setTerrainIntensity(1.0, Anim(0.0)); e.setElevationScale(15.0, Anim(0.0))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, 18.0, 1.03), Anim.cubic(5.0), -1); sleep(5.5)  # 표면 초근접
        cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.2)
        e.setRockyCliffIntensity(1.0, Anim(1.0)); print("  DEM 초근접서 rockyCliff(1.0) — 6초"); sleep(6.0)
        e.setTreeIntensity(1.0, Anim(1.0)); print("  tree(1.0) — 6초"); sleep(6.0)
        print("    [판정-절벽/식생] 표면에 암벽 질감/나무가 돋아나나? 무변화면 Terrain View 전용 死 확정.")
    except Exception as ex: print("  절벽/식생 예외:", ex)
except Exception as e:
    print("  지구표면 예외:", e)

# ── C) SkySurvey 마지막 창의적 한 방: 다른 밝은 HiPS + 지상 아닌 우주배경 ──────
hr("C) SkySurvey 최후 시도 (밝은 HiPS)")
try:
    SceneGraph().reset(1); sleep(1.2)
    Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(0.0, Anim(0.0))
    Planet(Planet.PlanetName.Earth).setTerrainIntensity(0.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # 별도 꺼서 서베이만 남는지
    ss = SkySurvey(SkySurvey.SkySurveyName.SkySurvey001)
    for url in ["https://alasky.u-strasbg.fr/DSS/DSSColor",
                "https://alasky.u-strasbg.fr/AllWISE/RGB-W4-W2-W1"]:
        ss.setUrl(url); ss.setIntensity(1.0, Anim(0.0)); sleep(2.5)
        ss.setIntensity(1.0, Anim(0.0)); sleep(2.0)
        print("  URL=%s → 하늘에 뭔가 뜨나? (5초 홀드)" % url); sleep(5.0)
    print("    [판정-서베이] 별·은하수 다 껐는데 하늘에 뿌연 영상이 뜨면 부활. 완전 검정이면 死 최종.")
except Exception as e:
    print("  SkySurvey 예외:", e)

print("\n>>> 끝. A(비/눈/별자리선) · B(비/절벽/식생) · C(서베이) 각각 화면 결과 알려주세요.")

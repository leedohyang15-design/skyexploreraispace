# -*- coding: utf-8 -*-
# 재도전 ④ — 날씨(비/눈) 집중. 가설: Rain/Snow 는 'ATMOSPHERE 패널' 소속 → 대기 ON 이어야 켜짐.
# 지난번 실패 원인 추정 = setAtmosphereIntensity(0)(밤하늘). 이번엔 대기 ON + restore 안 함(파란불 확인용).
from skyExplorer import *
from studio import *
from Initialization import *

def hr(t): print("\n========== %s ==========" % t)
dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# 지상 + 대기 ON (낮/흐린 하늘이라야 빗줄기·눈이 배경에 보임)
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception: pass
uni = Universe(Universe.UniverseName.MainUniverse); uni.setGlobalIntensity(1.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))          # ★ 핵심: 대기 ON (날씨 렌더 전제)
earth.setTerrainIntensity(0.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
# 청주 낮(하늘 밝게 = 빗줄기 대비 잘 보임). 정오=03:30 UTC → 오전 10시쯤=01:30 UTC
dm.setDateTime(2026, 6, 1, 1, 30, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
sleep(1.0)

def drive(kw, label, hold=8.0):
    hit = None
    for n in dir(ParameterizationLut.ParameterizationLutName):
        if kw.lower() in n.lower() and not n.startswith("__"):
            hit = n; break
    if not hit:
        print("  [%s] 슬롯 없음" % label); return None
    try:
        pl = ParameterizationLut(getattr(ParameterizationLut.ParameterizationLutName, hit))
        pl.setEnabled(True); sleep(1.5)
        en = getattr(pl, "enabled", "?")
        print("  [%s] 슬롯=%s enabled=%s → internalValue=1.0 로 세우고 %.0f초 홀드(restore 안 함)" % (label, hit, en, hold))
        pl.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
        pl.setInternalValue(1.0, Anim(2.0)); sleep(hold)
        print("    [판정-%s] ① 오퍼레이터 패널의 %s 버튼에 파란불 들어왔나  ② 화면에 %s 내리나" % (label, label, label))
        return pl
    except Exception as e:
        print("  [%s] 예외: %s" % (label, e)); return None

hr("비 (WeatherEffectRain, 대기 ON)")
rain = drive("Rain", "비")

hr("눈 (WeatherEffectSnow, 대기 ON) — 비 끄고")
if rain is not None:
    try: rain.setInternalValue(0.0, Anim(1.0)); rain.setEnabled(False); sleep(1.5)
    except Exception: pass
snow = drive("Snow", "눈")

print("\n>>> 끝. 파란불/화면 결과 알려주세요.")
print("    파란불 O + 비/눈 O = 날씨 효과 획득! / 파란불 O 인데 화면 X = 렌더는 오퍼레이터뷰 전용")
print("    파란불 X = enable 이 프리셋에 안 먹음(다른 구동 필요)")

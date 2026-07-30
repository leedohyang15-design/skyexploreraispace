# -*- coding: utf-8 -*-
# 재도전 ① — "안 되던 클래스" 새 각도 프로브 (B·C 카테고리)
# 각 항목마다 [판정] 을 콘솔에 찍음. 화면도 같이 보면서 확인.
from skyExplorer import *
from studio import *
from Initialization import *

def hr(t): print("\n========== %s ==========" % t)

# 공통: 겨울 밤하늘(장미성운 NGC2237 은 겨울철 외뿔소자리 = 이때 지평선 위)
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception: pass
uni = Universe(Universe.UniverseName.MainUniverse); uni.setGlobalIntensity(1.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)
dm = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)   # 겨울밤
cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))

# ── C-1) NGC : '카메라 접근' 말고 '제자리 ON' (Nebula 처럼 하늘에 켜지나?) ─────
hr("C-1) NGC 제자리 ON (장미성운 NGC2237)")
try:
    ngc = NGC(NGC.NGCName.NGC2237)
    ngc.setIntensity(1.0, Anim(0.0))
    try:
        o = ngc.scale; ngc.setScale(o*8.0, Anim(0.0)); print("  setScale %.3f→%.3f" % (o, o*8.0))
    except Exception as e: print("  setScale 예외:", e)
    try:
        ngc.setLabelIntensity(1.0, Anim(0.0))
        ngc.setPointerType(Body.PointerType.Model1); ngc.setPointerIntensity(1.0, Anim(0.0))
    except Exception as e: print("  pointer/label 예외:", e)
    print("  NGC id =", getattr(ngc, "id", "?"))
    print("  [판정] 화면에 장미성운/포인터/라벨이 하늘 어딘가 뜨면 = '제자리 ON' 성공(접근만 못했던 것)")
    print("         아무것도 안 뜨면 = NGC 렌더 자체 死 (기존 결론 유지)")
except Exception as e:
    print("  NGC 생성/호출 예외:", e)

# ── C-1b) NGC 를 어느 Data.Type 이 '살아있는 액션'으로 주나 전수 스캔 ──────
hr("C-1b) 'NGC 2237' 살아있는 DB 액션 스캔")
cands = ["NgcType","NebulaType","DeepSkyObjectType","AsterismType","MessierType","GalaxyType"]
names = ["NGC 2237","NGC2237","Rosette","Rosette Nebula"]
found = []
for tp in cands:
    dtype = getattr(Data.Type, tp, None)
    if dtype is None:
        print("  Data.Type.%s 없음" % tp); continue
    for nm in names:
        try:
            h = DataManager.database().data(dtype, nm)
            if h is None: continue
            act = h.action(Action.Type.FadeTo)
            alive = act is not None
            print("  %-18s / '%s' → handle=%s, FadeTo=%s" % (tp, nm, "O", "살아있음★" if alive else "None(死)"))
            if alive: found.append((tp, nm))
        except Exception as e:
            pass
print("  [판정] '살아있음★' 조합이 하나라도 있으면 = 그 타입/이름으로 접근 가능! 없으면 死 확정.")
print("         찾은 것:", found if found else "없음")

# ── B-1) ParameterizationLut : 이번엔 'enable 후 프레임 대기' 하고 구동 ──────
hr("B-1) ParameterizationLut (프레임 대기 후 재구동)")
try:
    pl = ParameterizationLut(ParameterizationLut.ParameterizationLutName.ParameterizationLut001)
    pl.setEnabled(True)
    sleep(1.5)   # ★ 새 변수: enable 반영에 프레임 필요 → 넉넉히 대기
    print("  enabled 읽기:", getattr(pl, "enabled", "?"))
    # Stars intensity 를 타겟으로 (osgId 핸들)
    try:
        handler = stars.osgId
    except Exception:
        handler = getattr(stars, "id", 0)
    try:
        pl.addTargetAttribute(int(handler), ParameterizationLut.AttributeName.Intensity)
        pl.addKey(0.0, Vec4(0.0,0,0,0), ParameterizationLut.KeyType.Double)
        pl.addKey(1.0, Vec4(1.0,0,0,0), ParameterizationLut.KeyType.Double)
        print("  타겟/키 설정 완료 (handler=%s). internalValue 1→0 스윕 (별 어두워지나?)" % handler)
        pl.setInternalValue(1.0, Anim(0.0)); sleep(1.0)
        pl.setInternalValue(0.0, Anim(3.0)); sleep(3.5)
        print("  [판정] 별밭이 어두워졌으면 = ParameterizationLut 부활! 무변화면 = 여전히 死")
        pl.setInternalValue(1.0, Anim(1.0)); sleep(1.2)
        try: pl.restore()
        except Exception: pass
    except Exception as e:
        print("  타겟/키/구동 예외:", e)
except Exception as e:
    print("  ParameterizationLut 예외:", e)

# ── B-2) SkySurvey : 엔진 은하수 끄고 서베이만 (재확인, 빠르게) ──────────────
hr("B-2) SkySurvey 재확인 (엔진 은하수 OFF)")
try:
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))  # 엔진 은하수 OFF = 기준 제거
    ss = SkySurvey(SkySurvey.SkySurveyName.SkySurvey001)
    ss.setUrl("https://alasky.u-strasbg.fr/MellingerRGB")
    ss.setIntensity(1.0, Anim(0.0)); sleep(2.0)
    ss.setIntensity(1.0, Anim(0.0)); sleep(1.5)   # setUrl 뒤 intensity 재확인
    print("  url 읽기:", getattr(ss, "url", "?"))
    print("  [판정] 엔진 은하수 껐는데도 하늘에 뿌연 서베이가 남으면 = 렌더됨! 검은하늘이면 死(기존 결론).")
except Exception as e:
    print("  SkySurvey 예외:", e)

print("\n>>> 끝. 각 [판정] 줄 + 화면 상태를 알려주세요.")

# -*- coding: utf-8 -*-
"""
sun_closeup.py — 태양 클로즈업 (2026-07-14, 미연습 코드 중심)
★ 전부 처음 쓰는 IndividualStar 태양 표면 기능:
  setCoronaIntensity(코로나) · setPhotosphereIntensity(광구) · setMagnetogramIntensity(자기장지도=흑점) ·
  setMagneticLinesIntensity(자기력선) · setFilter(H-알파 등=홍염) · setModel/setInternalRepresentation/setCycle ·
  setSaturationFactor · setScale(확대, 일식서 검증).
★ 접근: FadeTo(StarType "Sun") 시도 → 외부 도킹. 실패 시 setScale 로 그 자리 확대(일식 방식).
  enum(Filter/Model/InternalRepresentation/Cycle)은 dir() 로 프로브해 로그로 학습.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def probe_enum(name, cls):
    try:
        print("[enum] %s: %s" % (name, ", ".join([m for m in dir(cls) if not m.startswith("_")])))
    except Exception as e:
        print("[enum] %s 실패: %s" % (name, e))


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(fn, *args, label=""):
    """IndividualStar 태양 기능 호출 + 성공/실패 로그(미연습이라 존재 확인 겸)."""
    try:
        getattr(sun, fn)(*args)
        print("   ✓ %s%s %s" % (fn, args, label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


# ── enum 프로브(학습) ───────────────────────────────────────
for nm, attr in (("Filter", "Filter"), ("Model", "Model"),
                 ("InternalRepresentation", "InternalRepresentation"), ("Cycle", "Cycle")):
    try:
        probe_enum(nm, getattr(IndividualStar, attr))
    except Exception as e:
        print("[enum] IndividualStar.%s 없음: %s" % (attr, e))

# ── 무대(지상, 어두운 배경) ─────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
# 코로나·자기력선이 잘 보이게 하늘 어둡게(지구 대기/지표 off)
for fn in ("setAtmosphereIntensity", "setTerrainIntensity"):
    try:
        getattr(Planet(PN.Earth), fn)(0.0, Anim(0.0))
    except Exception:
        pass
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)     # 정오(태양 남중)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

# GoTo/FadeTo 핸들 (StarType) 선확보
h_sun = None
for dt, nm in (("StarType", "Sun"), ("StarType", "Sol"), ("IndividualStarType", "Sun")):
    try:
        cand = DataManager.database().data(getattr(Data.Type, dt), nm)
        if cand is not None:
            h_sun = cand; print("   태양 DB 핸들 = %s/%s" % (dt, nm)); break
    except Exception:
        pass

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.85, 0.4))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("태양 — 가장 가까운 별을 들여다본다"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.5); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); sleep(dur)


# ── 태양으로 접근: FadeTo 시도 → 실패 시 setScale ───────────
narr("태양에 다가간다", 1.0)
approached = False
if h_sun is not None:
    act = h_sun.action(Action.Type.FadeTo)
    if act is not None:
        uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
        act.trigger(); sleep(4.5)
        cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.2)
        uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
        rlog("FadeTo 후"); approached = True; print("   FadeTo Sun")
if not approached:
    print("   FadeTo 미지원 → setScale 로 그 자리 확대(일식 방식)")

# ★ FadeTo 가 태양 '안'(R=0.2)에 넣음 → 밖으로 빼서 원반이 보이게(setScale 대신 R 풀백)
try:
    orig_scale = sun.scale
    print("   원본 scale=%s" % orig_scale)
except Exception:
    orig_scale = 1.0
narr("태양으로 더 다가간다", 1.0)
# ⚠️ R 단위 = AU! 태양 반지름 0.00465 AU. FadeTo R=0.2AU(≈45반지름, 작은 원반) → 더 당겨야 큰 원반.
#   R≈0.03 AU ≈ 6.5 태양반지름 = 원반이 돔에 크게 + 코로나 여유.
try:
    cam.setPositionR(0.03, Anim.cubic(6.0), -1); sleep(6.3)
    rlog("접근 후")
except Exception as e:
    print("   접근 실패: %s" % e)
cam.setTargetHeight(75.0, Anim.cubic(1.5)); sleep(1.6)             # 돔 중앙으로

# ★ SDO(태양관측위성) 모델 = 표면 영상 렌더 (이게 있어야 광구/흑점/필터가 보임)
narr("SDO 위성이 본 태양", 1.0)
mdl = None
for cand in ("SDO", "Photosphere", "HDR", "Visible"):
    if hasattr(IndividualStar.Model, cand):
        mdl = getattr(IndividualStar.Model, cand)
        if feat("setModel", mdl, Anim(2.0), label="(%s)" % cand):
            print("   Model=%s" % cand); break
sleep(2.5)

def clear_overlays():
    """장면 전환 전 오버레이 끄기(겹침 방지)."""
    for fn in ("setMagnetogramIntensity", "setMagneticLinesIntensity", "setCoronaIntensity"):
        try:
            getattr(sun, fn)(0.0, Anim(1.0))
        except Exception:
            pass


VIS = getattr(IndividualStar.Filter, "Filter_Visible", None)
F304 = getattr(IndividualStar.Filter, "Filter_304", None)
INT = getattr(IndividualStar.Filter, "Filter_Intensitygram", None)

# ── 제1장: 광구 + 흑점(자기 활동영역) ───────────────────────
#   ⚠️ 이 SDK는 흑점을 '어두운 점'으로 렌더 안 함(연속광=밋밋한 흰 원반). 흑점=magnetogram 색깔 활동영역으로 표현.
narr("제1장 — 태양의 얼굴, 광구", 1.5)
for cand in ("Cycle_2232", "Cycle_2165", "Cycle_2097"):           # 활동 극대기 = 활동영역 많음
    if hasattr(IndividualStar.Cycle, cand):
        if feat("setCycle", getattr(IndividualStar.Cycle, cand), Anim(2.0), label="(활동기 %s)" % cand):
            break
if VIS is not None:
    feat("setFilter", VIS, Anim(2.0), label="(가시광=질감 있는 광구)")
feat("setPhotosphereIntensity", 1.0, Anim(2.0)); sleep(2.0)
narr("흑점 — 강한 자기장이 억누른 활동영역", 1.0)
feat("setMagnetogramIntensity", 1.0, Anim(2.5), label="(흑점=자기 활동영역)")
narr("색은 자기극성 — 초록·파랑 N극, 빨강·노랑 S극", 3.5)
# 시간가속으로 자전(활동영역이 표면을 가로지름)
narr("태양도 자전한다 — 흑점을 따라가 보자", 0.5)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 14, 12, 0, 0, tz, Anim(14.0)); sleep(15.0)  # +13일 ≈ 자전 반바퀴
dm.stop(); sleep(0.3)

# ── 제2장: 자기력선 (코로나 루프) ───────────────────────────
narr("제2장 — 태양을 휘감는 자기력선", 1.5)
feat("setMagneticLinesIntensity", 1.0, Anim(2.5), label="(코로나 루프)")
narr("흑점 사이를 아치로 잇는 자기장의 고리", 3.5)

# ── 제3장: 홍염 (304Å 자외선) ───────────────────────────────
narr("제3장 — 304Å 자외선으로 보면", 1.5)
clear_overlays()                                                   # 자기장 끔(304 붉은 화면 깨끗하게)
if F304 is not None:
    feat("setFilter", F304, Anim(2.5), label="(304Å)")
narr("붉은 채층과 가장자리로 솟는 홍염", 4.0)

# ── 제4장: 코로나 ────────────────────────────────────────────
narr("제4장 — 백만 도의 바깥 대기, 코로나", 1.5)
feat("setCoronaIntensity", 1.0, Anim(3.0))
feat("setSaturationFactor", 1.3, Anim(2.0), label="(채도)")
for cand in ("Cycle_2165", "Cycle_2232", "Cycle_2097"):           # 활동 극대기 프리셋
    if hasattr(IndividualStar.Cycle, cand):
        if feat("setCycle", getattr(IndividualStar.Cycle, cand), Anim(3.0), label="(%s)" % cand):
            break
sleep(3.5)

# ── 정리 ────────────────────────────────────────────────────
narr("우리 모든 빛과 생명의 근원", 3.0)
for fn in ("setMagnetogramIntensity", "setMagneticLinesIntensity", "setCoronaIntensity"):
    feat(fn, 0.0, Anim(2.0))
dm.stop()
t1.setText("태양 — 8분 19초 거리의 별"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.5); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①FadeTo Sun 됐나(로그) ②setScale×25 확대되나 "
      "③광구/흑점(magnetogram)/자기력선/코로나 각각 보이나 ④H-알파 필터 멤버 뭐였나([enum] 로그) "
      "⑤시간가속으로 흑점이 표면 가로지르나(태양 자전) ⑥배율/구도 조정 필요?")

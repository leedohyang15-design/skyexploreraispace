# -*- coding: utf-8 -*-
"""
earth_city_lights.py — 밤의 지구, 도시의 불빛 (2026-07-16, v2 위상 스윕; 안 쓴 Planet 렌더 3종)
★ 지금까지 한 번도 '주역'으로 안 쓴 Planet 렌더 코드:
  · `setNightLightsIntensity` = 밤면(그늘) 도시광 = 호박색(실제 나트륨등 색) — 이 쇼의 하이라이트
  · `setCloudsIntensity`      = 구름층
  · `setTerrainModel(BMNG_*)` = 블루마블(지구 실측 지표 텍스처) 교체
★ 이번엔 '그림자 ON' 이 맞음 (위상·일식처럼 그림자가 주제) — 낮/밤 경계(터미네이터)를 만들어야 밤면 도시광이 보임.
  운영 표준(그림자 OFF)의 명시적 예외. + planetShine 낮춰 밤면을 어둡게 → 도시광이 도드라짐.
★ 카메라: FadeTo Earth(외부 도킹, R=4) = 추적/줌락 불필요(견고). 자전은 확정 레시피(관성 프레임 + setRotationSpeedScale).
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
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:18] for a in args), label)); return True
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


# ── 무대: 우주 (지구로) ─────────────────────────────────────
print("무대: 우주 — 밤의 지구, 도시의 불빛")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))

# ── FadeTo 지구 (외부 도킹) ─────────────────────────────────
h = DataManager.database().data(Data.Type.PlanetType, "Earth")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); dark_clamp(4.5); print("   FadeTo Earth(외부)")
cam.setTargetHeight(30.0, Anim(0.0))
rlog("FadeTo 후")

# ── 시각 고정(자전 시작 전, 암전 중) ────────────────────────
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 9, 1, 12, 0, 0, tz, Anim(0.0)); sleep(0.5)

# ── ★ 지구 렌더 구성 (밤/도시광/구름/블루마블) ─────────────
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(대기 = 푸른 림 글로우)")
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0), label="(지표 ON)")
# 블루마블 지표 텍스처(있으면) — 없으면 로그만
for tm in ("BMNG_Ocean", "BMNG_Seasons", "BMNG_Summer"):
    if hasattr(Planet.TerrainModel, tm):
        if feat(earth, "setTerrainModel", getattr(Planet.TerrainModel, tm), label="(블루마블 %s)" % tm):
            break
feat(earth, "setCloudsIntensity", 1.0, Anim(0.0), label="(★ 구름층)")
feat(earth, "setNightLightsIntensity", 1.0, Anim(0.0), label="(★★ 밤면 도시광 = 호박색)")
# ★ 그림자 ON (밤면을 만들어야 도시광이 보임 — 운영 그림자OFF 규칙의 명시적 예외)
feat(earth, "setShadowStrength", 1.0, Anim(0.0), label="(그림자 ON = 낮/밤 경계)")
feat(earth, "setShadowContrast", 1.0, Anim(0.0), label="(명암 대비 ↑)")
feat(earth, "setPlanetShineStrength", 0.05, Anim(0.0), label="(밤면 어둡게 → 도시광 도드라짐)")

# ── 자막(우주 프레임: distance 20) ─────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setColor(Vec(1.0, 0.85, 0.5)); t1.setDistance(20.0, Anim(0.0))


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 오블리크로 기울여 지구를 옆에서 (B90 극 → B18 측면) ─────
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 18.0, p.z), Anim.cubic(3.5), -1); dark_clamp(3.7)
    rlog("오블리크 후")
except Exception as e:
    print("   오블리크 실패: %s" % e)

uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)
narr("우주에서 본 지구", 3.5)
narr("지금 보이는 쪽은 '밤' — 도시의 불빛만 호박색으로 빛난다", 4.0)

# ── ★ 위상 스윕 = 자전 멈추고 '태양 각도'만 흘려 밤→경계→낮 ──
#   v1 문제(사용자): 도킹 각도가 '밤면(태양 반대=신월 위상)'이라 도시광 말고 다 어두웠음(낮면이 반대편).
#   → 카메라 L 공전(암석행성 불안정)에 안 기대고: 관성 프레임 + setRotationSpeedScale(0)(자전 정지) +
#     날짜를 ~6개월 흘림 → 태양 방향이 반구를 쓸며 밤→터미네이터(도시 켜짐)→낮(구름·바다·대기)이 드러남.
narr("시간을 흘려 태양 쪽으로 돌려 본다...", 3.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); dark_clamp(1.3)          # 관성 전환 숨김
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = earth.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(0.0), ip)          # 현재 L,B,R 유지(안 움직임)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
dark_clamp(0.4)
dm.stop(); sleep(0.2)
feat(earth, "setRotationSpeedScale", 0.0, label="(★ 자전 정지 → 태양 각도만 변화 = 위상)")
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

narr("낮과 밤의 경계 — 저녁을 맞은 도시들이 하나둘 불을 켠다", 3.5)
# ★ ~3개월만 흘려 '터미네이터(반쪽 낮/반쪽 밤)'에서 멈춤 = 도시광 + 낮면을 한 화면에 (아이코닉 샷)
dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(20.0)); sleep(21.0)
dm.stop()
narr("한쪽은 도시의 호박색 불빛, 한쪽은 흰 구름과 푸른 바다", 5.0)   # 경계에서 홀드 = 최고 구도
narr("지구의 낮과 밤이 한 화면에 — 이 경계선이 '저녁'이다", 5.0)

# 마무리로 낮면까지 마저 밝힘
dm.setDateTime(2027, 3, 1, 12, 0, 0, tz, Anim(14.0)); sleep(15.0)      # 경계 → 낮면
dm.stop()
feat(earth, "resetRotationSpeedScale", label="(자전 배율 원복)")

narr("햇빛을 받는 낮의 지구 — 흰 구름, 푸른 바다, 얇은 대기의 띠", 4.5)
narr("낮과 밤이 공존하는 하나의 행성 — 우리가 사는 곳", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("밤의 지구 — 도시의 불빛", 4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v3 터미네이터 홀드): ①(확인)도시광 + 낮면(구름·블루마블·대기 림) 둘 다 나옴 "
      "②★이번엔 중간에 '터미네이터(반쪽 낮/반쪽 밤+도시광)'에서 멈춰 홀드하나 — 낮과 밤이 한 화면에 잡히나(최고 구도) "
      "③경계에서 도시광이 잘 보이나(3개월 지점이 딱 반쪽인가 / 아니면 기간 미세조정) ④마무리로 낮면까지 밝아지나 "
      "⑤홀드 위상이 어긋나면(너무 낮/너무 밤) 중간 날짜(현재 12/1)만 앞뒤로 조정")

# -*- coding: utf-8 -*-
"""
zodiacal_light.py — 황도광 (2026-07-15, 미사용 코드 중심)
★ 처음 쓰는 IndividualStar(태양) 코드:
  setZodiacalLightIntensity(황도광=행성간 먼지가 햇빛 산란) · setZodiacalLightScatteringIntensity(산란 세기).
  → 해 진 직후 서쪽 지평선에서 '황도'를 따라 비스듬히 솟는 희미한 빛 삼각뿔('가짜 새벽/황혼').
★ 구도: 봄 저녁(황도가 서쪽에 가파름) 청주, 서쪽 지평선 저각. 대기 끈 어두운 하늘 + 황도 그리드로
  '빛이 황도를 따라간다'를 보여줌. ⚠️ 은근한 현상 → 안 보이면 실측으로 기록(미미/미지원).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
earth = Planet(PN.Earth)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:16] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


# ── 무대: 봄 저녁 황혼 (해 진 직후 서쪽) ─────────────────────
print("무대: 봄 저녁 황혼")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기광 OFF = 어두운 하늘)")
sun.setIntensity(1.0, Anim(0.0))                                  # 지평선 아래(황혼)
Stars(Stars.StarsName.StarrySky).setIntensity(0.55, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.3, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
# ⚠️ DefaultTimeZone=UTC. 봄(춘분경) 저녁 = 황도가 서쪽에 가파름(황도광 삼각뿔이 곧게 섬).
#   KST 20:00(해 진 뒤 ~1.5h) = UTC 11:00. (KST=UTC+9)
dm.setDateTime(2026, 3, 21, 11, 0, 0, tz, Anim(0.5)); sleep(1.0)
# 서쪽 지평선 저각(해가 진 방향, 황도광이 솟는 곳). az=서(270) → H=180-270=-90. target 저각.
cam.setTargetHeight(15.0, Anim(0.0)); cam.setOrientationH(-90.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 60, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.85, 0.6))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("황도광 — 해가 진 뒤에도 남는 빛"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── ★ 황도광 ON (미사용 setZodiacalLightIntensity) ─────────
narr("서쪽 지평선 — 해가 진 자리", 3.0)
narr("행성간 먼지가 햇빛을 산란한다 — 황도광", 2.5)
feat(sun, "setZodiacalLightIntensity", 1.0, Anim(4.0), label="(황도광 ON)")
feat(sun, "setZodiacalLightScatteringIntensity", 1.0, Anim(4.0), label="(산란 세기)")
sleep(4.5)

# ── 황도 그리드로 '빛이 황도를 따라간다' 보여줌 ─────────────
narr("이 빛은 '황도'를 따라 비스듬히 솟는다", 2.5)
for fn in ("setEclipticGridIntensity",):
    feat(earth, fn, 0.6, Anim(3.0), label="(황도 그리드)")
sleep(3.5)
narr("태양·달·행성이 지나는 길 — 그 길을 먼지가 밝힌다", 4.0)

# ── 세기 A/B (있는지/보이는지 대비) ─────────────────────────
narr("세기를 올렸다 내렸다 — 대비", 1.5)
for iv in (0.0, 1.0, 0.0, 1.0):
    feat(sun, "setZodiacalLightIntensity", iv, Anim(2.5), label="(황도광 %.1f)" % iv); sleep(2.7)

# ── 정리 ────────────────────────────────────────────────────
narr("가장 어두운 하늘에서만 보이는 빛", 3.0)
feat(earth, "setEclipticGridIntensity", 0.0, Anim(2.0))
feat(sun, "setZodiacalLightIntensity", 0.0, Anim(2.5))
t1.setText("황도광 — 태양계 먼지가 만든 빛"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★setZodiacalLightIntensity 로 서쪽 지평선에 비스듬한 빛 삼각뿔이 뜨나 — 핵심 "
      "②setZodiacalLightScatteringIntensity 로 산란감 바뀌나 ③황도 그리드와 빛의 방향이 나란한가 "
      "④세기 0↔1 A/B 로 있고 없고가 대비되나 ⑤안 보이면 미미/미지원으로 기록(구도·시각 조정 후보 알려줘)")

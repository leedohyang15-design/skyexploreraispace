# -*- coding: utf-8 -*-
"""
milky_way.py — 은하수 (2026-07-15, 미사용 코드 중심)
★ 처음 쓰는 Galaxy 코드: setExposure(은하수 노출/블룸). + 확정된 별하늘 노브(Stars)와 합쳐 연출.
  Galaxy(MilkyWay).setIntensity/setExposure + Stars.setExposure/setPointSaturation/setTwinklingAmplitude.
★ 구도: 어두운 시골 여름밤(대기 OFF), 은하 중심(궁수자리, 남쪽)이 뜬 시각. 남쪽 하늘을 올려다봄.
  ⚠️ DefaultTimeZone=UTC → 여름밤 KST 22:30 = UTC 13:30.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
stars = Stars(Stars.StarsName.StarrySky)
galaxy = Galaxy(Galaxy.GalaxyName.MilkyWay)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:16] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def rd(obj, prop, default):
    try:
        v = getattr(obj, prop); print("   원본 %s=%s" % (prop, v)); return v
    except Exception:
        return default


# ── 무대: 어두운 시골 여름밤 ────────────────────────────────
print("무대: 시골 여름밤")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(PN.Earth).setIntensity(1.0, Anim(0.0))
feat(Planet(PN.Earth), "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기광 OFF=칠흑 하늘)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
galaxy.setIntensity(0.8, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(37.5, 128.7, 1400.0))     # 강원 산간(고도 1400m, 빛공해 적음)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 13, 30, 0, tz, Anim(0.5)); sleep(1.0)          # = KST 22:30 (은하 중심 남중 무렵)
cam.setTargetHeight(40.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))  # 남쪽 하늘 위(은하수 아치)

o_gexp = rd(galaxy, "exposure", None)
o_sexp = rd(stars, "exposure", 5.68)
o_ssat = rd(stars, "pointSaturation", 1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 58, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("은하수 — 우리 은하를 안에서 본 모습"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 별을 먼저 살린다 (확정 노브) ────────────────────────────
narr("가장 어두운 하늘 — 수천 개의 별", 3.0)
feat(stars, "setExposure", o_sexp * 1.5, Anim(3.0), label="(별 노출 ↑=은하수 배경 별 살아남)")
feat(stars, "setPointSaturation", 3.0, Anim(3.0), label="(별 색 채도 ↑)")
feat(stars, "setTwinklingAmplitude", 1.2, Anim(2.0), label="(반짝임)")
sleep(3.0)

# ── ★ 은하수 노출/세기 (미사용 Galaxy.setExposure) ─────────
narr("은하수 — 수천억 별이 뭉쳐 만든 띠", 3.0)
feat(galaxy, "setIntensity", 1.0, Anim(3.0), label="(은하수 밝게)"); sleep(3.0)
narr("노출을 올리면 — 희미한 성간 구름까지", 1.5)
feat(galaxy, "setExposure", (o_gexp or 1.0) * 2.2, Anim(4.0), label="(★ 은하수 노출 ↑)"); sleep(4.2)
# 노출 A/B (있는지/보이는지)
narr("노출 낮췄다 올렸다 — 대비", 1.0)
for mul in (0.5, 2.2, 0.5, 2.2):
    feat(galaxy, "setExposure", (o_gexp or 1.0) * mul, Anim(2.5), label="(노출 ×%.1f)" % mul); sleep(2.7)
if o_gexp is not None:
    feat(galaxy, "setExposure", o_gexp, Anim(2.0), label="(노출 원복)")

# ── 은하 중심 안내 ──────────────────────────────────────────
narr("가장 밝고 두꺼운 곳 — 궁수자리 방향, 은하의 중심", 4.0)
narr("그 너머 2만 6천 광년 — 초대질량 블랙홀 궁수자리 A*", 4.5)

# ── 시간가속: 은하수가 하늘을 가로지른다 ────────────────────
narr("시간을 흘리면 — 은하수도 하늘을 가로지른다", 2.0)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 16, 30, 0, tz, Anim(18.0)); sleep(19.0)        # +3h → 은하수 서편으로 기욺
dm.stop()

# ── 정리 ────────────────────────────────────────────────────
narr("우리는 이 은하의 변두리에서 안을 들여다본다", 3.5)
feat(stars, "setPointSaturation", o_ssat, Anim(2.0))
feat(stars, "setExposure", o_sexp, Anim(2.0))
t1.setText("은하수 — 우리 집, 우리 은하"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①은하수 아치가 남쪽 하늘에 뜨나(고도 1400m 어두운 하늘) ②★Galaxy.setExposure 노출 A/B 로 "
      "은하수 밝기/블룸이 바뀌나 — 핵심(미사용) ③별 노출/채도로 배경 별이 풍성해지나 ④시간가속으로 은하수가 "
      "하늘을 가로지르나 ⑤원본 exposure 읽혔나(로그) ⑥구도/시각 조정?")

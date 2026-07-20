# -*- coding: utf-8 -*-
"""
light_pollution.py — 빛공해: 도시 vs 진짜 밤하늘 (2026-07-09, 밝기 사용자 확정 Recording13)
새 주제: 관객 공감 100% — '내가 사는 도시의 밤하늘이 왜 이럴까'.
새 API: Planet(Earth).setLightPollutionIntensity — 지구의 광공해 맵 강도(0=청정, 1=대도시).
       보조: setScatteringIntensity(대기 산란), setCloudLightPollution(구름 반사광).

구성: 진짜 밤하늘(청정, 은하수 보임) → 빛공해 단계별 상승(교외→도시→대도시)로 별이 사라짐 →
     다시 청정으로 (대비). 같은 하늘·같은 시각, 오직 빛공해만 변화.

무대: 지상 밤하늘 (은하수 잘 보이는 여름밤).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 청정 지상 밤하늘 ───────────────────────────────────
print("무대: 청정 밤하늘 (은하수 보임)")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
try:
    earth.setLightPollutionIntensity(0.0, Anim(0.0))     # ★ 청정 (빛공해 0)
except Exception as e:
    print("   setLightPollutionIntensity 초기화: %s" % e)
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st = Stars(Stars.StarsName.StarrySky)
st.setIntensity(1.0, Anim(0.0))
mw = Galaxy(Galaxy.GalaxyName.MilkyWay)
mw.setIntensity(0.8, Anim(0.0))                          # 은하수 뚜렷
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))            # 청주 근교
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 14, 0, 0, tz, Anim(0.5))     # 여름밤 23시 KST(=14 UT), 은하수 남중
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("진짜 밤하늘 — 청정 지역, 은하수가 흐른다"); t1.setIntensity(1.0, Anim(1.5))
print(">>> 청정 밤하늘 감상 (7초)")
sleep(7.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)


def stage(label, lp, star_i, mw_i, dur=6.0):
    """빛공해 단계.
    ⚠️ setLightPollutionIntensity 는 대기 스카이글로만 — 별/은하수(독립 레이어)는 안 깎음.
    → '별이 사라지는' 효과는 Stars/Galaxy intensity 를 직접 같이 낮춰야 함(실측 확정).
    """
    print("=" * 50); print("%s (lp=%.2f, stars=%.2f, mw=%.2f)" % (label, lp, star_i, mw_i))
    t1.setText(label); t1.setIntensity(1.0, Anim(0.6))
    try:
        earth.setLightPollutionIntensity(lp, Anim(3.0))   # 대기 스카이글로(있으면 오렌지빛)
    except Exception as e:
        print("   lp 실패: %s" % e)
    # ★ 진짜 '별이 사라짐' = 별/은하수 레이어 밝기를 광공해 단계에 맞춰 직접 낮춤
    st.setIntensity(star_i, Anim(3.0))
    mw.setIntensity(mw_i, Anim(3.0))
    sleep(dur)
    t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)


# ── 빛공해 단계별 상승 (별/은하수도 함께 사라짐) ─────────────
#   (lp, 별 밝기, 은하수 밝기) — 단계가 오를수록 별·은하수 함께 감광.
stage("교외 — 별이 조금씩 줄어든다 (Bortle 4)", 0.3, 0.80, 0.35)
stage("도시 외곽 — 은하수가 사라진다 (Bortle 6)", 0.6, 0.60, 0.10)
stage("대도시 한복판 — 밝은 별 몇 개뿐 (Bortle 9)", 1.0, 0.40, 0.0, dur=7.0)

# ── 다시 청정으로 (극적 대비) ────────────────────────────────
print("=" * 50); print("다시 청정으로")
t1.setText("불을 끄면 — 하늘이 돌아온다"); t1.setIntensity(1.0, Anim(0.8))
try:
    earth.setLightPollutionIntensity(0.0, Anim(5.0))    # 대기 스카이글로 원복
except Exception as e:
    print("   복귀 실패: %s" % e)
st.setIntensity(1.0, Anim(5.0))                         # ★ 별 돌아옴
mw.setIntensity(0.8, Anim(5.0))                         # ★ 은하수 돌아옴
sleep(6.0)
t1.setText("은하수는 늘 거기 있었다 — 빛에 가려졌을 뿐")
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8))

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("빛공해 — 우리가 잃어버린 밤하늘"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①빛공해 올릴수록 별/은하수 사라지나 ②단계별 체감 ③복귀 시 별 돌아오나")

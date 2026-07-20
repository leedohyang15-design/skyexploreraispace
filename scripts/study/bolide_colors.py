# -*- coding: utf-8 -*-
"""
bolide_colors.py — 화구 색 비교 (2026-07-09)
지난 실측 확정: ColoredFireball 모델 = 정답(주황 Sodium "진짜 운석 떨어지듯이" 확인).
이번엔 혼란 없이 색만 비교 — **전부 ColoredFireball 로 고정**하고 원소만 바꾼다.
→ 5발 전부 보여야 정상! (모델 없음/Chelyabinsk 처럼 '안 뜨는' 경우 없음)

원소별 색 (유성 스펙트럼):
  Sodium=주황·노랑 / Magnesium=청록 / Iron=노랑 / Calcium=보라 / NitrogenOxygen=적색
경로·속도 전부 동일(play 15 ≈ 10초 크로싱) — 오직 색만 다름.

무대: 청주 2026-12-14 23:00 KST.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 ──────────────────────────────────────────────────────
print("무대: 청주 2026-12-14 23:00 KST")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 14, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.9, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)


def fire(elem, subtitle, custom_color=None, wait=10.0):
    """전부 ColoredFireball 고정, 원소(색)만 바꿈. play 15 ≈ 10초 크로싱."""
    print("=" * 60)
    print("화구: ColoredFireball + %s" % elem)
    print("=" * 60)
    bo = Bolide(Bolide.BolideName.Bolide001)          # 매 발 새 핸들
    t1.setText(subtitle); t1.setIntensity(1.0, Anim(0.5))
    try:
        bo.setModel(Bolide.ModelID.ColoredFireball, "")           # ★ 확정 정답 모델
        col = Vec3(*custom_color) if custom_color is not None else Vec3(0.0, 0.0, 0.0)
        bo.setElement(getattr(Bolide.Element, elem), col, Anim(0.0))
        bo.setIntensity(1.0, Anim(0.0))
        bo.set(-30.0, 70.0, 100000.0, 50.0, 15.0, 30000.0, 1.0)   # set speed 1.0 고정
        sleep(0.3)
        bo.play(15.0)
        print("   발사! element 읽음=%s" % getattr(bo, "element", "?"))
    except Exception as e:
        print("   실패: %s" % e)
    sleep(wait)
    t1.setIntensity(0.0, Anim(0.5))
    sleep(1.5)


# ── 색 5발 (전부 보여야 정상) ─────────────────────────────────
fire("Sodium",         "① 나트륨 — 주황빛 (가장 흔한 유성 색)")
fire("Magnesium",      "② 마그네슘 — 청록빛")
fire("Iron",           "③ 철 — 노란빛")
fire("Calcium",        "④ 칼슘 — 보랏빛")
fire("NitrogenOxygen", "⑤ 질소·산소 — 붉은빛 (대기 발광)")

# 보너스: Custom 원소 + 커스텀 색 (원하는 RGB 직접 지정)
fire("Custom",         "⑥ 커스텀 — 청백색 (원하는 색 지정)",
     custom_color=(0.5, 0.7, 1.0))

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("화구 색 비교 끝 — 6발 다 보였나? 어떤 색이 제일 좋아?")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: ①~⑥ 각 색이 구분됐는지 / 전부 보였는지")

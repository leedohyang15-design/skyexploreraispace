# -*- coding: utf-8 -*-
"""
constellation_art_tour.py — 별자리 신화 그림 투어 (2026-07-13, 새 주제)
새 API 중점: Constellation.setArtIntensity (별자리 신화 그림/성화) — 지금껏 페이드인만 살짝 확인,
            제대로 된 '그림 투어'는 처음. 보조: setLinesIntensity / setLabelIntensity.

컨셉: 겨울 저녁 밤하늘엔 오리온·황소·쌍둥이·큰개 등 유명 별자리가 한데 모임.
      선 → 신화 그림 순으로 얹고, 전천(Target 0)에서 천천히 팬하며 하늘의 신화를 감상.

무대: 한국 겨울 저녁 (오리온 남중 무렵). 카메라 고정 — 그림을 '빛'으로 하나씩 조명.
 ⚠️ setOrientationH 방위 스윕은 돔 전체가 회전(시계/반시계)해 하늘이 통째로 도는 느낌 → 투어 부적합.
    → 카메라 고정 + setArtIntensity 스포트라이트로 시선을 이끈다.
설계 근거(CLAUDE.md):
 · 지상 전천 그리드/구도 = Target 0 (사용자 운영 확정). 관람 복귀는 30.
 · 별자리 enum 627개 = 난잡 → 유명 IAU 15~20개 큐레이션, 라벨 5개 이내.
 · setArtIntensity 동작 확정(0.9 페이드인). 선/라벨/그림 각각 (intensity, Anim).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 겨울 저녁 밤하늘 (오리온권이 남쪽에) ────────────────
print("무대: 겨울 저녁 밤하늘")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))            # 청주
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 11, 0, 0, tz, Anim(0.5))    # 1/15 20시 KST(=11 UT), 오리온 남중권
sleep(1.0)
# 전천 구도 = Target 0 (지상 전천 표준). 좌우 방위는 남쪽(오리온) 향해 출발.
cam.setTargetHeight(0.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))                     # H≈180-방위, 0 = 남쪽 정면

# ── 자막 준비 ────────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))

# ── 큐레이션: 겨울 저녁에 뜨는 유명 별자리 (IAU 3자 약어) ─────
#   art = 신화 그림 얹을 대상 / label = 이름표 (5개 이내만)
ART = ["Ori", "Tau", "Gem", "CMa", "Aur", "Per", "And", "Cas", "Peg", "Ari", "Leo", "UMa"]
LABELS = ["Ori", "Tau", "Gem", "CMa", "Leo"]            # 라벨은 5개만

cons = {}
for name in set(ART + LABELS):
    try:
        cons[name] = Constellation(getattr(Constellation.ConstellationName, name))
    except Exception as e:
        print("   %s 생성 실패: %s" % (name, e))

# ── ① 페이드인 + 선 켜기 ─────────────────────────────────────
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("겨울 밤하늘 — 별들을 잇는 옛사람들의 이야기"); t1.setIntensity(1.0, Anim(1.5))
print(">>> 별자리 선 켜기")
for name in ART:
    c = cons.get(name)
    if c is None:
        continue
    try:
        c.setLinesIntensity(0.7, Anim(2.5))
    except Exception as e:
        print("   %s 선 실패: %s" % (name, e))
sleep(4.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ② 신화 그림(setArtIntensity) 얹기 ────────────────────────
print(">>> 신화 그림 페이드인 (setArtIntensity)")
t1.setText("하늘에 새겨진 신화 — 사냥꾼, 황소, 쌍둥이"); t1.setIntensity(1.0, Anim(1.0))
for name in ART:
    c = cons.get(name)
    if c is None:
        continue
    try:
        c.setArtIntensity(0.75, Anim(3.0))
    except Exception as e:
        print("   %s 그림 실패: %s" % (name, e))
sleep(4.0)
# 라벨 5개
for name in LABELS:
    c = cons.get(name)
    if c is None:
        continue
    try:
        c.setLabelIntensity(0.8, Anim(2.0))
    except Exception as e:
        print("   %s 라벨 실패: %s" % (name, e))
sleep(3.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ③ 신화 그림 스포트라이트 — 카메라 고정, 빛으로 하나씩 조명 ──
#   ⚠️ setOrientationH 방위 스윕은 '돔 전체가 회전'(시계/반시계)해 하늘이 통째로 도는 느낌 → 투어 부적합.
#   대신 카메라 고정하고 각 별자리 그림을 하나씩 밝혀 관객 시선을 이끈다(미술관 스포트라이트).
print(">>> 신화 그림 스포트라이트 (카메라 고정)")
for name in ART:                                        # 전부 살짝 낮춰 배경으로
    c = cons.get(name)
    if c is None:
        continue
    try:
        c.setArtIntensity(0.18, Anim(1.5))
    except Exception:
        pass
sleep(1.8)

SPOT = [
    ("Ori", "오리온 — 바다의 신이 낳은 거인 사냥꾼"),
    ("Tau", "황소자리 — 제우스가 변신한 흰 소"),
    ("Gem", "쌍둥이자리 — 카스토르와 폴룩스 형제"),
    ("CMa", "큰개자리 — 오리온의 사냥개, 시리우스"),
    ("Aur", "마차부자리 — 전차를 발명한 왕"),
    ("Cas", "카시오페이아 — 허영에 빠진 왕비"),
]
prev = None
for name, myth in SPOT:
    c = cons.get(name)
    if c is None:
        continue
    t1.setText(myth); t1.setIntensity(1.0, Anim(0.6))
    # ★ 이전 것을 '동시에' 배경으로 낮추며(크로스페이드) 현재 것만 밝힘 → 항상 하나만 강조
    if prev is not None:
        pc = cons.get(prev)
        if pc is not None:
            try:
                pc.setArtIntensity(0.18, Anim(1.5)); pc.setLinesIntensity(0.5, Anim(1.5))
                pc.setLabelIntensity(0.0, Anim(1.0))
            except Exception:
                pass
    try:
        c.setArtIntensity(0.95, Anim(1.5)); c.setLinesIntensity(0.95, Anim(1.5))
        c.setLabelIntensity(0.9, Anim(1.0))
    except Exception as e:
        print("   %s 스포트 실패: %s" % (name, e))
    prev = name
    sleep(3.2)
    t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)
print("   ★ 카메라 고정 상태에서 그림이 하나씩 밝아지며 시선이 이동했나?")

# ── ④ 관람 복귀 (Target 30) + 오리온 클로즈업 ───────────────
print(">>> 관람 구도 복귀 (Target 30)")
t1.setText("가장 유명한 사냥꾼 — 오리온"); t1.setIntensity(1.0, Anim(0.8))
try:
    cam.setOrientationH(0.0, Anim.cubic(2.5))            # 남쪽(오리온) 정면
    cam.setTargetHeight(30.0, Anim.cubic(3.0))           # 관람 표준
    sleep(3.5)
    # 오리온만 강조: 다른 그림 살짝 낮추고 오리온 그림/선 올림
    for name in ART:
        if name == "Ori":
            continue
        c = cons.get(name)
        if c is None:
            continue
        try:
            c.setArtIntensity(0.25, Anim(2.0)); c.setLinesIntensity(0.3, Anim(2.0))
        except Exception:
            pass
    ori = cons.get("Ori")
    if ori is not None:
        ori.setArtIntensity(0.95, Anim(2.5)); ori.setLinesIntensity(0.9, Anim(2.5))
    sleep(4.0)
except Exception as e:
    print("   복귀/강조 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("별자리 — 인류가 하늘에 그린 가장 오래된 그림"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①선/신화그림 켜지나 ②setArtIntensity 로 그림 뜨나(어느 별자리?) "
      "③방위 스윕으로 여러 그림 지나가나 ④오리온 강조/라벨 보이나")

# -*- coding: utf-8 -*-
# ═══ 천왕성 — 눈 안 아프면서 고리가 보이는 밝기 찾기 (4구도, 약 60초) ═══
#
# 배경 (2026-08-10 사용자 스샷):
#   · 프레임 프로브 결과 확정 — **황도 프레임(PlanetPort.Ecliptic)에서만 기울기가 보인다.**
#     적도동기/EquatorialJ2000 은 천왕성 자신의 적도가 기준이라 고리가 늘 '가로'로 눕는다.
#   · 그런데 `setIntensity(1.5)` 로 고리를 살리니 **원반이 새하얗게 타서 눈이 아프다**(사용자).
#
# ⚠️ 확정 사실: **고리만 따로 밝히는 API 는 없다.**
#   고리 밝기는 본체 `setIntensity` 에 묶여 있다(= 올리면 원반도 같이 탄다).
#   → 눈부심을 줄이는 진짜 레버는 **그림자를 되살려 원반의 절반을 어둡게** 하는 것.
#     `setShadowStrength(1)` + `setPlanetShineStrength(낮게)` = 밤면이 어두워져 글레어가 확 준다.
#     (그림자 OFF 3세터는 '표면을 다 보여줄 때' 규칙이지, 고리 대비에는 오히려 해가 된다.)
#
# 네 조합을 차례로 띄운다. 눈이 편하면서 고리가 보이는 걸 고르면 된다.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
UR = Planet(Planet.PlanetName.Uranus)

HOLD = 13.0

# ── 접근 (암전 클램프) ────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))
    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))
    sleep(0.4)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    for _ in range(30):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # ★ 황도 프레임 — 기울기가 보이는 유일한 프레임(2026-08-10 스샷 확정)
    ep = UR.portId(Planet.PlanetPort.Ecliptic)
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 3.2), Anim(0.0), ep)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ep)
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.8)

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setDistance(20.0, Anim(0.0))
    txt.setColor(Vec(1.0, 1.0, 0.6))
    txt.setIntensity(1.0, Anim(0.0))
except Exception as e:
    print("접근 오류:", e)

# ── 참고: 고리 관련 API 가 정말 없는지 한 번 더 확인 ──────────
try:
    ring_api = [m for m in dir(UR) if "ring" in m.lower()]
    print("고리 관련 메서드/속성:", ring_api)
    print("  → setRingIntensity 류가 없으면 '고리만 밝히기'는 확정 불가.")
except Exception as e:
    print("dir 실패:", e)

# ── 네 조합 ───────────────────────────────────────────────────
#   (본체 intensity, shadowStrength, planetShine, 설명)
CASES = [
    (1.5, 0.0, 1.0, "1) intensity 1.5 + 그림자 OFF   (지금 쇼 — 원반이 탄다)"),
    (1.2, 0.0, 1.0, "2) intensity 1.2 + 그림자 OFF"),
    (1.2, 1.0, 0.15, "3) intensity 1.2 + 그림자 ON    (밤면 어둡게)"),
    (1.0, 1.0, 0.10, "4) intensity 1.0 + 그림자 ON    (가장 은은)"),
]

for inten, shadow, shine, label in CASES:
    try:
        UR.setIntensity(inten, Anim(1.2))
        UR.setShadowStrength(shadow, Anim(1.2))
        UR.setShadowContrast(shadow, Anim(1.2))
        UR.setPlanetShineStrength(shine, Anim(1.2))
        txt.setText(label)
        print(">>>", label)
        sleep(HOLD)
    except Exception as e:
        print("조합 오류:", label, e)

# ── 마무리 ────────────────────────────────────────────────────
try:
    txt.setText("눈이 편하면서 고리가 보이는 번호를 고르세요")
    sleep(5.0)
    txt.setIntensity(0.0, Anim(1.5))
    sleep(1.5)
except Exception as e:
    print("마무리 오류:", e)

print("=" * 62)
print("· 2~4 가 1 보다 편하면 → 쇼의 밝기를 그 값으로 교체.")
print("· 그림자 ON 이 고리를 너무 죽이면 → planetShine 을 0.3~0.5 로 올려 재시도.")
print("=" * 62)

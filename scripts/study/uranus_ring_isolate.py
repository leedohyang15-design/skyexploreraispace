# -*- coding: utf-8 -*-
# ═══ 천왕성 고리 — "intensity 가 정말 고리 레버인가?" 판별 (약 75초) ═══
#
# 사용자 관찰 (2026-08-10, 밝기 4조합 A/B 후):
#   "2번이 제일 나은데, **고리 밝기는 다 똑같고** 그냥 행성이 밝아서 좀 더 밝아 보이는 게 아닐까"
#
# 이게 맞으면 CLAUDE.md 의 확정 항목이 틀린 것이다:
#   기존 기록 = "본체 setIntensity 를 올리면 고리도 같이 밝아짐 → 1.5 가 균형"
#   → 실제로는 **화면 전체 게인**만 올라가고 고리/원반 대비는 그대로일 수 있다.
#     (그러면 원반이 먼저 타므로 intensity 를 올리는 건 순손해다.)
#
# ⚠️ 4조합 프로브로는 판별이 안 된다 — 전부 '밝히는' 방향이라 둘이 같이 움직였다.
#    **어둡게** 해봐야 갈린다:
#      · 원반이 어두워질 때 고리도 같이 사라진다 → 고리는 intensity 에 묶여 있다(기존 기록 맞음).
#      · 원반만 어두워지고 고리는 그대로다 → 고리는 독립이다.
#        그러면 **대비의 정답은 '낮은 intensity'** — 지금까지와 정반대가 된다.
#
# 볼 것 (딱 하나): **원반이 어두워질 때 고리가 같이 사라지는가, 남는가.**
#
# ══ 결과 (2026-08-10 사용자 판정) ══════════════════════════════════
#   A) 어둡히면 **고리도 같이 어두워진다** — 둘은 연동("아 아니네 둘이 연관이 있는듯").
#      → 고리는 본체 intensity 에 비례. **비율이 고정이라 어느 방향으로 돌려도 대비가 안 변한다.**
#        올리면 원반만 타고, 내리면 고리가 같이 죽는다 = 양방향 다 죽은 레버.
#      → intensity 는 '눈이 편한 노출' 고르기용일 뿐. **1.2 채택**("밝기 측면에는 괜찮은 거 같다").
#   C) `setScale` ×2.5·×5 = **체감 없음**("크기는 모르겠다"). 고리와 원반이 같이 커져 비율이 그대로.
#   → **천왕성 고리에 남은 레버는 구도(B38·R3.2)뿐이고 이미 최대치다. 더 파지 말 것.**
# ═══════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
UR = Planet(Planet.PlanetName.Uranus)

HOLD = 9.0
txt = None
orig_scale = None


def say(s):
    if txt:
        txt.setText(s)
    print(">>>", s)


# ── 접근 ──────────────────────────────────────────────────────
#   구도는 채택된 2번과 동일하게 고정한다(황도 프레임 · B=38 · R=3.2 · 그림자 OFF · 배경 검정).
#   ⚠️ 이 프로브 내내 구도는 손대지 않는다 — 변수를 하나만 움직여야 판별이 된다.
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
    UR.setShadowStrength(0.0, Anim(0.0))
    UR.setShadowContrast(0.0, Anim(0.0))
    UR.setPlanetShineStrength(1.0, Anim(0.0))

    ep = UR.portId(Planet.PlanetPort.Ecliptic)
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 3.2), Anim(0.0), ep)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ep)
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.8)

    # ⚠️ 원본 scale 은 1.0 이 아닐 수 있다 — 반드시 읽어두고 '원본×배율'로 쓴다.
    try:
        orig_scale = UR.scale
        print("천왕성 원본 scale =", orig_scale)
    except Exception as ex:
        print("scale 읽기 실패:", ex)

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setDistance(20.0, Anim(0.0))
    txt.setColor(Vec(1.0, 1.0, 0.6))
    txt.setIntensity(1.0, Anim(0.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))     # ← 암전과 짝. 빠지면 전체가 검은 화면.
    sleep(2.2)
except Exception as e:
    print("접근 오류:", e)

# ── A. intensity 를 '내리는' 스윕 (판별 구간) ─────────────────
#   1.2(채택값)에서 시작해 계단으로 낮춘다. 고리가 같이 죽는지만 본다.
try:
    for inten, label in ((1.2, "A1) intensity 1.2  ← 채택값(기준)"),
                         (0.8, "A2) intensity 0.8"),
                         (0.5, "A3) intensity 0.5"),
                         (0.25, "A4) intensity 0.25  ← 고리가 남아있나?")):
        UR.setIntensity(inten, Anim(1.2))
        say(label)
        sleep(HOLD)
except Exception as e:
    print("A 구간 오류:", e)

# ── B. 대비 확인 — 되돌렸을 때 고리가 '돌아오는가' ───────────
try:
    UR.setIntensity(1.2, Anim(1.5))
    say("B) 다시 1.2 — A4 보다 고리가 뚜렷해졌나?")
    sleep(HOLD)
except Exception as e:
    print("B 구간 오류:", e)

# ── C. 밝기 말고 '크기' 레버 — setScale ───────────────────────
#   고리가 어두운 게 아니라 '가늘어서' 안 보이는 것일 수도 있다.
#   확대하면 고리가 차지하는 화소가 늘어 밝기를 안 올리고도 읽힐 수 있다.
try:
    if orig_scale:
        for mul, label in ((2.5, "C1) 밝기 그대로 + 크기 ×2.5"),
                           (5.0, "C2) 밝기 그대로 + 크기 ×5")):
            UR.setScale(orig_scale * mul, Anim.cubic(2.5))
            say(label)
            sleep(HOLD)
        UR.setScale(orig_scale, Anim(1.5))           # 원본값으로 복귀(1.0 하드코딩 금지)
    else:
        say("C) scale 을 못 읽어 크기 실험은 건너뜀")
        sleep(2.0)
except Exception as e:
    print("C 구간 오류:", e)

# ── 마무리 ────────────────────────────────────────────────────
try:
    txt.setText("고리가 A4(어두울 때)에도 남아 있었나요?")
    sleep(5.0)
    txt.setIntensity(0.0, Anim(1.5))
    sleep(1.5)
except Exception as e:
    print("마무리 오류:", e)

print("=" * 66)
print("판정법")
print(" · A4(0.25)에서 고리도 같이 사라졌다 → 고리는 본체 intensity 에 묶여 있다.")
print("     = 기존 기록이 맞다. 단 대비는 안 늘므로 '1.5 가 균형'은 여전히 틀린 말.")
print(" · A4 에서 원반만 어두워지고 고리는 남았다 → 고리는 독립이다.")
print("     = 대비의 정답은 오히려 '낮은 intensity'. 기존 기록을 뒤집어야 한다.")
print(" · C1/C2 에서 고리가 읽히기 시작했다 → 진짜 레버는 밝기가 아니라 '크기(setScale)'다.")
print("=" * 66)

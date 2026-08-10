# -*- coding: utf-8 -*-
# ═══ 천왕성 '세우기' — 고리/궤도가 세로로 서는 L(경도) 찾기 (약 85초) ═══
#
# 미해결로 남아 있던 것 (2026-08-10 사용자 최초 지적): **"우선 세로로 안 써져있거든?"**
#   · 1차로 밝혀낸 것: 도킹(EquatorialSynchronous)·EquatorialJ2000 은 **천왕성 자신의 적도면**이 기준이라
#     98° 기울기를 프레임이 흡수한다 → 어느 B 를 줘도 고리가 '가로'로 눕는다.
#     **황도 프레임(`Planet.PlanetPort.Ecliptic`)** 이어야 기울기가 드러난다(스샷 확정).
#   · ⚠️ 하지만 거기서 멈췄다. **프레임만 바꾸고 L 은 FadeTo 가 준 값을 그대로 썼다** —
#     그건 임의값이라 '세로'가 나올 이유가 없다. B 만 움직이면 기울어진 타원일 뿐 서지 않는다.
#
# 기하 (왜 L 이 열쇠인가):
#   천왕성 자전축은 황도면에 거의 **누워** 있다(98°). 고리·위성궤도는 그 축과 직각인 적도면에 있으므로
#   **고리면이 황도면과 거의 수직** = 고리면이 황도북극 방향을 품고 있다.
#   → 황도면 안(B=0)에서 보면:
#       · 시선이 **자전축과 직각**인 L  → 고리를 옆에서 봄 = **세로 선으로 섬** ★우리가 원하는 그림
#       · 시선이 **자전축과 나란한** L  → 고리를 정면에서 봄 = **동심원 과녁**  (이것도 그림은 좋다)
#   축이 황도경도 어디를 향하는지는 이 빌드의 렌더 기준을 모르므로 **재서 찾는다.**
#
# 볼 것: 어느 L 에서 고리와 위성 궤도선이 **세로**로 서는가 (또는 과녁이 되는가).
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
UR = Planet(Planet.PlanetName.Uranus)

R_NEAR = 3.2          # 고리 확정 근접값
HOLD = 11.0
txt = None
ep = None


def say(s):
    if txt:
        txt.setText(s)
    print(">>>", s)


def clamp_dark(seconds):
    for _ in range(int(seconds / 0.2)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)


def frame(L, B, R):
    """황도 프레임 안에서만 움직인다 — 읽기·쓰기·재조준 프레임을 절대 섞지 않는다."""
    cam.setPositionLBR(Vec(L, B, R), Anim(0.0), ep)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ep)
    cam.setTargetHeight(30.0, Anim(0.0))


# ── 접근 ──────────────────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))
    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))
    sleep(0.4)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    clamp_dark(6.0)

    # 밝기 = 확정값(2026-08-10 A/B 채택). 올려도 고리 대비는 안 늘고 원반만 탄다.
    UR.setIntensity(1.2, Anim(0.0))
    UR.setShadowStrength(0.0, Anim(0.0))
    UR.setShadowContrast(0.0, Anim(0.0))
    UR.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # 위성 궤도선 — 고리보다 밝아서 '기울기'를 훨씬 잘 보여준다(판정용 기준선).
    for nm in ("Ariel", "Titania"):
        try:
            s = Satellite(getattr(Satellite.SatelliteName, nm))
            s.setIntensity(1.0, Anim(0.0))
            s.setOrbitIntensity(1.0, Anim(0.0))
            s.setScale(10.0, Anim(0.0))
        except Exception as ex:
            print("위성", nm, ex)

    ep = UR.portId(Planet.PlanetPort.Ecliptic)

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setDistance(20.0, Anim(0.0))
    txt.setColor(Vec(1.0, 1.0, 0.6))
    txt.setIntensity(1.0, Anim(0.0))
except Exception as e:
    print("접근 오류:", e)

# ── A. 황도면 안(B=0)에서 L 을 90° 씩 — 어디서 서는가 ────────
#   고리면은 180° 주기라 0/45/90/135 면 한 바퀴를 다 덮는다.
#   ⚠️ 구도 점프는 자세 변경이므로 암전 속에서 하고, 정렬이 끝난 뒤 페이드인한다.
try:
    for L in (0.0, 45.0, 90.0, 135.0):
        uni.setGlobalIntensity(0.0, Anim.cubic(1.0)); sleep(1.2)
        frame(L, 0.0, R_NEAR)
        sleep(0.6)
        say("A) 황도면 안 · L=%g°  — 세로인가? 과녁인가? 비스듬인가?" % L)
        uni.setGlobalIntensity(1.0, Anim.cubic(1.2))
        sleep(HOLD)
except Exception as e:
    print("A 구간 오류:", e)

# ── B. 연속 스윕 — 서는 지점을 눈으로 훑는다 ──────────────────
#   ⚠️ 포트 프레임 공전이므로 **재조준 필수**(track=-1 공전과 달리 빠지면 대상이 흘러나간다).
#      3스텝마다 setOrientationSmoothXYZR 을 다시 건다.
try:
    say("B) L 을 0→180° 로 천천히 — 서는 각도를 찾으세요")
    step = 0
    L = 0.0
    while L <= 180.0:
        cam.setPositionLBR(Vec(L, 0.0, R_NEAR), Anim(0.5), ep)
        step += 1
        if step % 3 == 0:
            cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.5), ep)
        sleep(0.5)
        L += 6.0
except Exception as e:
    print("B 구간 오류:", e)

# ── C. 참고 — B 를 올리면 어떻게 무너지는가 ───────────────────
#   지금 쇼가 쓰는 B=38 이 '세로'를 얼마나 망치는지 대조군으로 본다.
try:
    uni.setGlobalIntensity(0.0, Anim.cubic(1.0)); sleep(1.2)
    frame(90.0, 38.0, R_NEAR)
    sleep(0.6)
    say("C) 같은 L=90° 인데 B=38 — 지금 쇼의 구도(세로가 무너지나?)")
    uni.setGlobalIntensity(1.0, Anim.cubic(1.2))
    sleep(HOLD)
except Exception as e:
    print("C 구간 오류:", e)

# ── 마무리 ────────────────────────────────────────────────────
try:
    txt.setText("세로로 선 구간의 L 값을 알려주세요")
    sleep(5.0)
    txt.setIntensity(0.0, Anim(1.5))
    sleep(1.5)
except Exception as e:
    print("마무리 오류:", e)

print("=" * 66)
print("판정법")
print(" · A 네 컷 중 고리·궤도가 '세로 선'이면 → 그 L 이 정답(축과 직각).")
print(" · '동심원 과녁'이면 → 그 L 은 축 방향. 세로는 거기서 L±90° 다.")
print(" · B 스윕에서 서는 순간의 L 을 읽어도 된다(0 에서 6° 씩, 0.5초 간격).")
print(" · C 가 A 보다 눕는다면 → 쇼의 B=38 을 낮춰야 한다(세로 우선이면 B=0).")
print("=" * 66)

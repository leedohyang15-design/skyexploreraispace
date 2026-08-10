# -*- coding: utf-8 -*-
# ═══ 천왕성 '누운 자세'가 보이는 프레임 찾기 (A/B/C/D 4구도, 약 70초) ═══
#
# 문제 (2026-08-10 사용자 실측): SHOW_uranus_sideways.py 에서 고리가 **세로로 안 보였다**.
#
# 원인 가설:
#   FadeTo 도킹 프레임(EquatorialSynchronous)과 EquatorialJ2000 은 둘 다
#   **천왕성 자신의 적도면**을 기준으로 한다. 고리는 그 적도면에 놓여 있으므로
#   어떤 프레임이든 B 를 열면 '토성처럼 가로로 누운 타원'이 된다.
#   자전축 98° 기울기는 **프레임이 같이 기울어 있어 상쇄**된다.
#   → 기울기를 보려면 **황도(궤도면) 기준 = PlanetPort.Ecliptic** 이어야 한다.
#
# 이 프로브가 답할 것: 네 구도 중 어디서 고리/궤도가 '세로'로 보이는가.
#   A) EquatorialSynchronous, B=38   ← 지금 쇼가 쓰는 것 (가로로 보였음)
#   B) Ecliptic,              B=38
#   C) Ecliptic,              B=0    ← 황도면 '안'에서 보기
#   D) Ecliptic,              B=75   ← 황도 북쪽 위에서 내려다보기
#
# 판정: 각 구도가 뜰 때 자막에 이름이 나온다. 어느 화면에서 고리가 세로로 섰는지만 보면 된다.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
UR = Planet(Planet.PlanetName.Uranus)

HOLD = 14.0          # 구도당 관찰 시간

# ── 접근 (암전 클램프) ────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
    uni.setGlobalIntensity(0.0, Anim(0.0))
    dm.stop(); sleep(0.2)
    dm.setDateTime(2026, 10, 15, 13, 0, 0, tz, Anim(0.0))
    sleep(0.4)

    DataManager.database().data(Data.Type.PlanetType, "Uranus").action(Action.Type.FadeTo).trigger()
    for _ in range(30):                       # 6초 — 내부 방향정렬 슬루가 끝날 때까지
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    UR.setShadowStrength(0.0, Anim(0.0))
    UR.setShadowContrast(0.0, Anim(0.0))
    UR.setPlanetShineStrength(1.0, Anim(0.0))
    UR.setIntensity(1.5, Anim(0.0))           # 고리는 본체 intensity 에 묶임
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # 위성 2개만 — 궤도선 방향까지 같이 보기 위함(많으면 지저분)
    for nm in ("Ariel", "Titania"):
        try:
            s = Satellite(getattr(Satellite.SatelliteName, nm))
            s.setIntensity(1.0, Anim(0.0))
            s.setOrbitIntensity(0.9, Anim(0.0))
            s.setScale(9.0, Anim(0.0))
        except Exception as ex:
            print("위성", nm, ex)

    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 12, 0))
    txt.setDistance(20.0, Anim(0.0))
    txt.setColor(Vec(1.0, 1.0, 0.6))
    txt.setIntensity(1.0, Anim(0.0))
except Exception as e:
    print("접근 오류:", e)

# ── 사용 가능한 포트 확인 ─────────────────────────────────────
ports = {}
for nm in ("EquatorialSynchronous", "EquatorialJ2000", "Ecliptic"):
    try:
        ports[nm] = UR.portId(getattr(Planet.PlanetPort, nm))
        print("포트 OK:", nm, "→", ports[nm])
    except Exception as ex:
        print("포트 실패:", nm, ex)

# ── 네 구도를 차례로 ──────────────────────────────────────────
#   ⚠️ 구도 전환은 '자세 변경'이라 암전 속에서 하고, 정렬이 끝난 뒤 페이드인한다.
CASES = [
    ("A", "EquatorialSynchronous", 38.0, 3.2, "A) 적도동기 프레임 · B=38  (지금 쇼가 쓰는 구도)"),
    ("B", "Ecliptic",              38.0, 3.2, "B) 황도 프레임 · B=38"),
    ("C", "Ecliptic",               0.0, 3.2, "C) 황도 프레임 · B=0  (황도면 안에서)"),
    ("D", "Ecliptic",              75.0, 3.2, "D) 황도 프레임 · B=75  (황도 위에서)"),
]

for tag, port_name, b, r, label in CASES:
    if port_name not in ports:
        print("건너뜀:", tag, port_name, "포트 없음")
        continue
    try:
        pid = ports[port_name]
        uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)

        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, b, r), Anim(0.0), pid)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), pid)
        cam.setTargetHeight(30.0, Anim(0.0))
        sleep(0.8)

        txt.setText(label)
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
        print(">>> 구도", tag, port_name, "B=%.0f R=%.1f" % (b, r))
        sleep(HOLD)
    except Exception as e:
        print("구도", tag, "오류:", e)

# ── 마무리 ────────────────────────────────────────────────────
try:
    txt.setText("어느 구도에서 고리가 '세로'로 섰는지 확인")
    sleep(5.0)
    txt.setIntensity(0.0, Anim(1.5))
    UR.setIntensity(1.0, Anim(1.5))
    sleep(2.0)
except Exception as e:
    print("마무리 오류:", e)

print("=" * 60)
print("판정: A(적도 프레임)에서 가로 / B~D(황도 프레임) 중 하나가 세로면 가설 확정.")
print("      전부 가로면 → 이 빌드는 고리를 '항상 적도 기준'으로 그린다는 뜻이고,")
print("      그때는 '세로' 연출을 포기하고 쇼의 설명 문구를 바꿔야 한다.")
print("=" * 60)

# -*- coding: utf-8 -*-
"""
venus_phases.py — 금성의 위상 (2026-07-15)
★ 1610년 갈릴레이의 두 번째 결정타: 금성이 초승달→반달→보름달처럼 '위상'이 변한다 →
  금성이 태양을 돈다는 증거(천동설론 프톨레마이오스 모델론 설명 불가). 목성 위성과 함께 지동설 확정.
★ 재활용: FadeTo 암석행성 도킹 + 관성 프레임 전환(위성계와 동일) + 시간가속.
  ⚠️⚠️ 이번엔 '그림자가 주제' → 운영 그림자OFF 규칙의 예외. 오히려 **밤면을 칠흑으로**(planetShine 0)
       + 그림자 대비 최대로 해서 터미네이터(명암경계)를 선명하게 = 위상이 또렷.
  ⚠️ 위상 변화는 금성 공전(225일)에 따라 태양-금성-관측자 각이 변해서 생김 →
     관성 프레임으로 카메라를 별에 고정하고 시간가속하면 태양각이 돌며 위상이 순환(공전 ~0.8바퀴 = 위상 한 사이클 거의).
  ⚠️ 적도 옆에서 봐야(B 낮게) 터미네이터가 세로 = 초승달 모양. 극에서 보면 파이조각처럼 보임.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
venus = Planet(PN.Venus)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:14] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


# ── 무대(지상) & 인트로 ─────────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 3, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.9, 0.7))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("금성의 위상 — 갈릴레이의 두 번째 증거"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 금성으로: reset + FadeTo ────────────────────────────────
narr("금성으로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Venus")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Venus")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
venus.setIntensity(1.0, Anim(0.0))

# ── ★ 위상이 주제 = 그림자 강조(운영 그림자OFF 규칙의 예외) ──
#   밤면을 칠흑으로(planetShine 0) + 그림자 대비 최대 → 터미네이터 선명 = 위상 또렷.
feat(venus, "setPlanetShineStrength", 0.0, Anim(1.0), label="(밤면 칠흑 = 위상 선명)")
feat(venus, "setShadowStrength", 1.0, Anim(1.0), label="(그림자 최강)")
feat(venus, "setShadowContrast", 1.0, Anim(1.0), label="(명암경계 대비 최대)")
feat(venus, "setAtmosphereIntensity", 0.3, Anim(1.0), label="(금성 두꺼운 대기 살짝)")
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)

# ── 적도 옆·근접: 터미네이터가 세로(초승달)로 보이게 B 낮춤 + R 살짝 당김 ─
narr("적도 옆에서 — 명암의 경계를 본다", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 6.0, p.z * 0.8), Anim.cubic(5.0), -1); sleep(5.3)   # B→6(적도 옆), R 살짝 근접
    rlog("적도뷰 후")
except Exception as e:
    print("   적도뷰 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.2)); sleep(1.3)

# ── ★ 관성 프레임 전환 (별 고정 → 공전에 따라 태양각만 돌아 위상 순환) ─
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = venus.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim.cubic(1.5), ip); sleep(1.8)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim.cubic(1.5), ip); sleep(1.7)
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)

# ── ★ 시간가속: 금성이 태양을 돌며 위상이 변한다 ──────────
narr("반년을 흘린다 — 금성이 태양을 돈다", 2.2)
narr("초승달에서 보름달로, 그리고 다시", 2.2)
dm.stop(); sleep(0.3)
# ⚠️ reset 이 날짜를 오늘로 되돌림(실측) → 시작 날짜를 여기서 '명시적으로' 다시 건다.
dm.setDateTime(2026, 1, 1, 12, 0, 0, tz, Anim(0.0)); sleep(1.2)       # 시작 위상 고정
dm.setDateTime(2026, 9, 1, 12, 0, 0, tz, Anim(26.0)); sleep(27.0)     # +243일 ≈ 금성 공전 1.08바퀴 = 위상 한 사이클 전부
dm.stop()

narr("천동설로는 설명할 수 없는 위상 변화", 4.0)

# ── 정리 ────────────────────────────────────────────────────
narr("금성은 태양을 돈다 — 지동설의 결정적 증거", 4.0)
t1.setText("금성 — 지구의 쌍둥이, 지옥의 세계"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①FadeTo Venus 도킹되나(posLBR 로그) ②밤면 칠흑+그림자로 '위상(초승달/반달)'이 또렷한가 "
      "③적도 옆(B6) 뷰라 터미네이터가 세로(초승달 모양)인가 ④관성 프레임 전환 됐나 "
      "⑤시간가속으로 위상이 변하나(초승달↔보름달) — 핵심 ⑥안 변하면: 프레임/시간축 어디서 막혔나(로그) 구도조정?")

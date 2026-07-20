# -*- coding: utf-8 -*-
"""
uranus_system.py — 천왕성: 옆으로 누운 행성 (2026-07-15)
★ 태양계의 괴짜: 자전축이 98° 기울어 '옆으로 누워' 공을 굴리듯 태양을 돈다.
  → 위성이 적도면(=자전면)을 도는데 그 면이 궤도에 거의 수직 → 어떤 시기엔 위성 궤도가
    '정면 과녁(bullseye)'처럼 동심원으로 보인다. (보이저2호 1986 상징 뷰.)
  ⚠️ 천왕성 고리는 극히 희미(암흑) → 이 엔진/스케일에선 사실상 안 보임 → 고리는 연출/내레이션서 제외(위성·기울기 집중).
★ 재활용: 가스행성 위성계 레시피(jupiter/saturn 확정) — FadeTo → 풀백 → 관성 프레임 → 위성 ON → 시간가속.
  차이: 천왕성 위성(미란다·아리엘·움브리엘·티타니아·오베론) + 옆으로 누운 기하가 저절로 과녁 뷰를 만듦.
  ⚠️ 오베론 궤도 ~23 천왕성반지름 → 풀백 R~26 이면 다 담김. 희미한 청록 원반이라 배경 별은 낮춰 대비 확보.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
uranus = Planet(PN.Uranus)
SN  = Satellite.SatelliteName

# 천왕성 5대 위성(안→밖) + 공전주기(일)
MOONS = [
    ("Miranda",   1.41),
    ("Ariel",     2.52),
    ("Umbriel",   4.14),
    ("Titania",   8.71),
    ("Oberon",   13.46),
]


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


# ── 위성 프로브 ─────────────────────────────────────────────
SAT = []
for nm, per in MOONS:
    if hasattr(SN, nm):
        try:
            SAT.append((nm, per, Satellite(getattr(SN, nm)))); print("   위성 OK: %s (%.2f일)" % (nm, per))
        except Exception as e:
            print("   위성 %s 생성 실패: %s" % (nm, e))
    else:
        print("   ⚠️ SatelliteName 에 %s 없음" % nm)

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
Stars(Stars.StarsName.StarrySky).setIntensity(0.4, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.7, 0.95, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("천왕성 — 옆으로 누운 얼음 거인"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 천왕성으로: reset + FadeTo (가스행성 도킹) ──────────────
narr("천왕성으로 다가간다 — 태양에서 29억 km", 1.2)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Uranus")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Uranus")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
uranus.setIntensity(1.0, Anim(0.0))
# ★ [운영 규칙] 행성 자세히 보기 = 그림자 OFF (암전 중에 미리 세팅 → 터미네이터 없이 온전한 원반)
feat(uranus, "setShadowStrength", 0.0, Anim(1.0), label="(그림자 OFF)")
feat(uranus, "setShadowContrast", 0.0, Anim(1.0), label="(명암경계 OFF)")
feat(uranus, "setPlanetShineStrength", 1.0, Anim(1.0), label="(밤면까지 밝힘)")
# 고리: 천왕성 고리는 이 엔진서 렌더 안 됨(프로브 확정, setRingModel 무효) → 연출 제외.
# ★★ 시작 날짜를 '지금(암전 중, 위성 켜기 전)' 고정 → 나중에 위성 보일 때 instant 날짜점프=순간이동 방지
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
narr("자전축이 98° — 공을 굴리듯 태양을 돈다", 3.5)

# ── 풀백: 위성 궤도가 다 담기게 (오베론 ~23 천왕성반지름). 한 번의 매끄러운 cubic 로만. ─
narr("뒤로 물러나 — 위성들의 과녁을 본다", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 30.0, p.z * 5.2), Anim.cubic(8.0), -1); sleep(8.3)   # R 5→26, B 20→30 한 번에
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)

# ── ★ 관성 프레임 전환 = '암전 속에서'(전환 점프 숨김, 우리 표준). 재조준 슬루 최소화. ─
narr("...", 0.2)
uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)     # 암전 → 아래 프레임 점프 안 보이게
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = uranus.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(0.0), ip)                 # 같은 L/B/R = 안 움직임(암전이라 어차피 안 보임)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)     # 페이드인 = 정렬 끝난 안정된 화면

# ── 위성 5개 ON + 궤도선 + 라벨 + 확대 ─────────────────────
narr("미란다 · 아리엘 · 움브리엘 · 티타니아 · 오베론", 3.0)
for nm, per, moon in SAT:
    feat(moon, "setIntensity", 1.0, Anim(1.0), label="(%s ON)" % nm)
    feat(moon, "setOrbitIntensity", 1.0, Anim(1.5), label="(%s 궤도선)" % nm)
    feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(%s 라벨)" % nm)
    feat(moon, "setScale", 9.0, Anim(1.5), label="(%s 확대)" % nm)
sleep(2.0)

# ── ★ 시간가속: 위성들이 옆으로 누운 채 돈다 ───────────────
narr("보름을 흘린다 — 위성들이 세로로 돈다", 2.2)
narr("미란다는 1.4일, 오베론은 13일", 2.2)
dm.stop(); sleep(0.3)
# 시작 날짜(8/01)는 위에서 이미 고정 → 여기선 '매끄러운 가속'만(instant 점프 없음 = 순간이동 없음)
dm.setDateTime(2026, 8, 15, 12, 0, 0, tz, Anim(26.0)); sleep(27.0)    # 8/01→8/15 +14일 → 미란다 ~10바퀴, 오베론 ~1바퀴
dm.stop()

narr("미란다 — 20km 높이의 절벽을 가진 위성", 4.0)

# ── 정리 ────────────────────────────────────────────────────
narr("천왕성 — 27개의 달을 거느린 얼음 거인", 3.0)
t1.setText("천왕성 — 태양계에서 가장 기울어진 세계"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v3): ①★위성 순간이동이 사라졌나(instant 날짜점프 제거) "
      "②그림자 꺼져 원반이 온전한가 ③★[고리 프로브] 위 로그의 '고리 관련 메서드/RingModel enum' 목록 알려줘 "
      "— setRingModel 시도 후 천왕성에 고리가 조금이라도 보이나(보이면 다음 버전서 살림) "
      "④위성들 다 뜨고 도나(미란다 빠름/오베론 느림) ⑤관성 전환 끊김 줄었나")

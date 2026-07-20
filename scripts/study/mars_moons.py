# -*- coding: utf-8 -*-
"""
mars_moons.py — 화성과 두 위성 포보스·데이모스 (2026-07-16)
★ 암석행성 중 유일하게 위성을 가진 화성. 감자처럼 생긴 두 위성(붙잡힌 소행성으로 추정).
  · 포보스: 화성에 너무 가까워 7.6시간에 한 바퀴 — 화성 하루(24.6h)보다 빨라 '서에서 떠 동으로' 짐.
    조석으로 매년 ~2cm 씩 다가와 ~5천만 년 뒤 부서져 고리가 되거나 추락할 운명.
  · 데이모스: 더 멀고 느림(30시간).
★ 재활용: 위성계 확정 레시피(외행성) + 모든 수정 반영(그림자OFF / 날짜 위성 켜기 전 암전 / 관성 프레임).
  ⚠️ 두 위성 궤도 매우 가까움(포보스 2.8·데이모스 6.9 화성반지름) → 풀백 R~9 면 충분(화성 크게 보임).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
mars = Planet(PN.Mars)
SN  = Satellite.SatelliteName

MOONS = [
    ("Phobos", "포보스", 0.319),   # 7.65시간
    ("Deimos", "데이모스", 1.263),  # 30.3시간
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
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 위성 프로브 ─────────────────────────────────────────────
SAT = []
for nm, ko, per in MOONS:
    if hasattr(SN, nm):
        try:
            SAT.append((nm, ko, per, Satellite(getattr(SN, nm)))); print("   위성 OK: %s (%s)" % (nm, ko))
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
    try: Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.4, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.045); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.7, 0.5))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("화성과 두 개의 달"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 화성으로: reset + FadeTo ────────────────────────────────
narr("붉은 행성으로", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Mars")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
mars.setIntensity(1.0, Anim(0.0))
# ★ 그림자 OFF (운영 규칙)
feat(mars, "setShadowStrength", 0.0, Anim(1.0), label="(그림자 OFF)")
feat(mars, "setShadowContrast", 0.0, Anim(1.0), label="(명암경계 OFF)")
feat(mars, "setPlanetShineStrength", 1.0, Anim(1.0), label="(밤면까지 밝힘)")
# ★ 시작 날짜 위성 켜기 전 암전에 고정 (순간이동 방지)
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
narr("화성 — 지구의 절반 크기, 붉은 사막의 세계", 3.5)

# ── 풀백: 두 위성 궤도(데이모스 6.9 화성반지름)가 담기게 ────
narr("두 개의 작은 달을 본다", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 1.8), Anim.cubic(6.0), -1); sleep(6.3)   # R 5→9
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)

# ── ★ 관성 프레임 전환 (암전 속) ───────────────────────────
narr("...", 0.2)
uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = mars.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(0.0), ip)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── 위성 ON + 궤도선 + 라벨 + 확대 (아주 작아 크게) ─────────
narr("포보스와 데이모스 — 감자처럼 생긴 두 위성", 3.0)
for nm, ko, per, moon in SAT:
    feat(moon, "setIntensity", 1.0, Anim(1.0), label="(%s ON)" % ko)
    feat(moon, "setOrbitIntensity", 1.0, Anim(1.5), label="(%s 궤도선)" % ko)
    feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(%s 라벨)" % ko)
    feat(moon, "setScale", 12.0, Anim(1.5), label="(%s 확대)" % ko)
sleep(2.0)

# ── ★ 시간가속: 포보스가 미친듯이 빠르게 ───────────────────
narr("이틀을 흘린다 — 잘 봐", 2.2)
narr("포보스는 7.6시간에 한 바퀴 — 화성의 하루보다 빠르다", 3.0)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 3, 12, 0, 0, tz, Anim(26.0)); sleep(27.0)     # +2일 → 포보스 ~6바퀴/데이모스 ~1.6바퀴
dm.stop()

narr("포보스는 화성 하늘을 '서에서 떠 동으로' 가로지른다", 4.0)
narr("조석으로 매년 다가와 — 언젠가 부서져 고리가 된다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("화성 — 붉은 행성과 그 두 조각", 3.0)
t1.setText("포보스 · 데이모스 — 붙잡힌 두 소행성"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①포보스/데이모스 생성/표시되나([위성 OK] 로그) ②풀백 R=9 로 두 궤도가 담기고 화성 크게 보이나 "
      "③그림자 꺼져 화성 원반 온전한가 ④★시간가속 때 포보스가 '매우 빠르게'(데이모스보다 훨씬) 도나 — 핵심 "
      "⑤위성 순간이동 없나 ⑥구도 조정?")

# -*- coding: utf-8 -*-
"""
neptune_triton.py — 해왕성과 트리톤의 역행 (2026-07-15) — 외행성 투어 완성
★ 교육 포인트: 트리톤은 태양계 큰 위성 중 '유일하게 역행(거꾸로) 공전' → 원래 카이퍼벨트 천체가
  해왕성 중력에 붙잡힌 것으로 추정. 안쪽 위성 프로테우스(정행)와 '반대 방향'으로 도는 게 대비된다.
★ 재활용: 가스/얼음행성 위성계 레시피(목성·토성·천왕성 확정) + 천왕성에서 잡은 수정 전부 반영:
  · FadeTo 직후 그림자 OFF (운영 규칙, 위상 아님)
  · 시작 날짜는 '위성 켜기 전 암전 중'에 instant 세팅 → 위성 순간이동 방지
  · 관성 프레임 전환은 암전 속에서 (전환 점프 숨김)
  ⚠️ 트리톤 궤도 ~14 해왕성반지름 → 풀백 R~18. 네레이드(223반지름)는 너무 멀어 제외.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
neptune = Planet(PN.Neptune)
SN  = Satellite.SatelliteName

# 실측(2026-07-16): 해왕성은 SatelliteName 에 '트리톤'만 존재(안쪽 위성 전부 없음) → 트리톤 단독.
# '역행'은 정행 위성 대비가 불가 → 투어 맥락(목·토·천왕성 위성=정행, 트리톤만 역행)으로 전달.
MOONS = [
    ("Triton", "트리톤", 5.88, "역행"),
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
for nm, ko, per, d in MOONS:
    if hasattr(SN, nm):
        try:
            SAT.append((nm, ko, per, d, Satellite(getattr(SN, nm)))); print("   위성 OK: %s (%s, %.2f일, %s)" % (nm, ko, per, d))
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
t1.setColor(Vec(0.6, 0.75, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("해왕성 — 태양계 끝의 푸른 거인"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 해왕성으로: reset + FadeTo ──────────────────────────────
narr("해왕성으로 — 태양에서 45억 km", 1.2)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Neptune")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Neptune")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
neptune.setIntensity(1.0, Anim(0.0))
# ★ 그림자 OFF (운영 규칙, 위상 아님)
feat(neptune, "setShadowStrength", 0.0, Anim(1.0), label="(그림자 OFF)")
feat(neptune, "setShadowContrast", 0.0, Anim(1.0), label="(명암경계 OFF)")
feat(neptune, "setPlanetShineStrength", 1.0, Anim(1.0), label="(밤면까지 밝힘)")
# ★ 시작 날짜를 위성 켜기 전 암전에 고정 (순간이동 방지)
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
narr("가장 바람이 센 행성 — 초속 600m의 폭풍", 3.5)

# ── 풀백: 트리톤 궤도(~14 해왕성반지름)가 담기게 ───────────
narr("뒤로 물러나 트리톤의 궤도를 본다", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 28.0, p.z * 3.4), Anim.cubic(8.0), -1); sleep(8.3)   # R 5→17
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)

# ── ★ 관성 프레임 전환 (암전 속에서 = 전환 점프 숨김) ──────
narr("...", 0.2)
uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = neptune.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim(0.0), ip)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
sleep(0.6)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── 트리톤 ON + 궤도선 + 라벨 + 확대 ───────────────────────
narr("트리톤 — 해왕성 유일의 큰 위성", 3.0)
for nm, ko, per, d, moon in SAT:
    feat(moon, "setIntensity", 1.0, Anim(1.0), label="(%s ON)" % ko)
    feat(moon, "setOrbitIntensity", 1.0, Anim(1.5), label="(%s 궤도선)" % ko)
    feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(%s 라벨)" % ko)
    feat(moon, "setScale", 10.0, Anim(1.5), label="(%s 확대)" % ko)
sleep(2.0)

# ── ★ 시간가속: 트리톤의 공전 (역행은 투어 맥락으로 전달) ──
narr("목성·토성·천왕성의 달은 모두 '정방향'으로 돌았다", 3.5)
narr("이제 트리톤을 봐 — 방향이 반대다", 2.5)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 25, 12, 0, 0, tz, Anim(28.0)); sleep(29.0)     # +24일 → 트리톤 ~4바퀴(역행) 천천히 관찰
dm.stop()

narr("트리톤은 '거꾸로' 돈다 — 유일하게 역행하는 큰 위성", 4.0)
narr("원래 카이퍼벨트의 천체가 해왕성에 붙잡힌 것", 4.0)
narr("표면 -235도, 태양계에서 가장 차가운 곳. 질소 간헐천이 뿜어진다", 4.5)
narr("역행 궤도는 점점 줄어 — 언젠가 해왕성에 부서져 고리가 된다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("해왕성 — 태양계의 마지막 행성", 3.0)
t1.setText("외행성 투어 완성 — 목성에서 해왕성까지"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①트리톤(단독) 생성/표시되나 ②풀백 R=17 로 트리톤 궤도가 담기고 해왕성이 아까보다 큰가 "
      "③그림자 꺼져 원반 온전한가 ④시간가속으로 트리톤이 매끄럽게 공전하나(순간이동 없이) "
      "⑤내레이션(역행/트리톤 이야기) 흐름 OK — 정행 위성 없어 대비는 투어 맥락으로 처리함")

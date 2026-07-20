# -*- coding: utf-8 -*-
"""
saturn_rings.py — 토성 고리 클로즈업 (2026-07-15, 미사용 코드 중심)
★ 전부 처음 쓰는 Planet 코드:
  setRingModel(Planet.RingModel) — 고리 표현 모델 교체 (⚠️ setRingIntensity 는 없음, CLAUDE.md 확정) ·
  setScatteringIntensity — 대기 산란 · setPointSaturation — 색 채도 · setCloudDirection(가스행성 띠).
★ 접근/줌 = 확정된 가스행성 레시피(zoom_saturn.py): reset → FadeTo Saturn(옆 도킹, 고리 보임) →
  positionLBR 읽어 R×배율 줌 (절대값 금지). RingModel enum 은 dir() 로 프로브해 로그로 학습.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
saturn = Planet(PN.Saturn)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(fn, *args, label=""):
    try:
        getattr(saturn, fn)(*args)
        print("   ✓ %s%s %s" % (fn, tuple(str(a)[:20] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def probe_enum(name, cls):
    try:
        mem = [m for m in dir(cls) if not m.startswith("_") and not m.islower() and "Invalid" not in m]
        print("[enum] %s: %s" % (name, mem)); return mem
    except Exception as e:
        print("[enum] %s 실패: %s" % (name, e)); return []


# ── enum 프로브(학습) ───────────────────────────────────────
ring_models = probe_enum("RingModel", getattr(Planet, "RingModel", None)) if hasattr(Planet, "RingModel") else []

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
Stars(Stars.StarsName.StarrySky).setIntensity(0.7, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.25, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 22, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(1.0, 0.92, 0.75))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("토성 — 태양계에서 가장 아름다운 고리"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 토성으로: reset + FadeTo (가스행성 = 옆 도킹, 고리가 기울어 보임) ──
narr("토성으로 다가간다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Saturn")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Saturn")
else:
    print("   ⚠️ FadeTo Saturn 미지원")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
saturn.setIntensity(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)

# ── 줌인 — 읽은 R × 배율 (절대값 금지, 확정 레시피) ──────────
#   ⚠️ 실측(v1): ×0.55 → ×0.6 겹쳐서 R 5→1.65 = 너무 가까워 행성·고리가 화면 밖(사용자 "아무것도 안보여").
#   고리 바깥 지름 ≈ 4.6 토성반지름 → R 을 3 아래로 내리면 고리가 잘림. FadeTo 기본 R=5 가 이미 고리 다 보임.
#   → 딱 한 번, 약하게(×0.65 → R≈3.25) 만 당겨 '살짝 크게 + 고리 전체'.
narr("고리가 보이게 — 살짝 더 가까이", 1.0)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.65), Anim.cubic(5.0), -1); sleep(5.2)
    rlog("줌(×0.65)")
except Exception as e:
    print("   줌 실패: %s" % e)

# ── ★ 고리를 활짝 + 고리면에 가깝게 (띠 구조/입자가 보여야 모델 차이가 드러남) ──
#   ⚠️ v1/v2: B=20~45 라 고리 디테일이 안 잡혀 "바뀌는데 차이 모르겠다"(사용자).
#   → B=58(더 활짝) + R 을 살짝 더 당겨(×0.85) 고리 띠가 화면을 크게 차지하게.
narr("고리면에 바짝 — 띠 구조를 본다", 1.5)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 58.0, p.z * 0.85), Anim.cubic(5.0), -1); sleep(5.2)
    rlog("고리면 근접(B=58)")
except Exception as e:
    print("   틸트 실패: %s" % e)

# ── ★ 고리 모델 교체 (미사용 setRingModel) — 하드컷 + 길게 홀드 + '뭘 볼지' 설명 ──
narr("이제 고리 모델을 바꿔 본다 — setRingModel", 2.5)
t2 = InsertText(InsertText.InsertTextName(2))
cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
t2.setPosition(Vec(0, 18, 0)); t2.setSize(0.04); t2.setDistance(1.0, Anim(0.0))
t2.setColor(Vec(1.0, 0.85, 0.4))

# 모델별 '뭘 보면 되는지' 설명 (차이 포인트)
RING_DESC = {
    "DefaultRing":   "DefaultRing — 카시니 간극·띠 구조 (정밀 텍스처)",
    "BasicRing":     "BasicRing — 밋밋한 균일 띠 (간극/구조 없음)",
    "Asteroids":     "Asteroids — 알갱이/입자 느낌",
    "Asteroids_3_0": "Asteroids_3_0 — 알갱이 (다른 버전)",
}


def show_ring(rm, dur=6.0):
    val = getattr(Planet.RingModel, rm)
    if not feat("setRingModel", val, label="(하드컷 %s)" % rm):    # Anim 없이 = 하드컷
        feat("setRingModel", val, Anim(0.0), label="(%s, anim0)" % rm)
    t2.setText(RING_DESC.get(rm, "RingModel: %s" % rm)); t2.setIntensity(1.0, Anim(0.5))
    sleep(dur)


if ring_models:
    for rm in ring_models:
        show_ring(rm, 6.0)
    # ★★ 고리에 줌인 쫙 (사용자 요청) — 고리면을 거의 위에서(B=80) + R 바짝 → 띠/간극 구조가 크게.
    #   여기서 DefaultRing(카시니 간극·구조) ↔ BasicRing(밋밋) A/B 하면 차이가 제일 잘 보임.
    narr("고리에 줌인 — 바짝 당겨 띠 구조를 본다", 1.5)
    try:
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, 80.0, p.z * 0.62), Anim.cubic(6.0), -1); sleep(6.3)
        rlog("고리 줌인(B=80)")
    except Exception as e:
        print("   고리 줌인 실패: %s" % e)
    # 제일 다른 쌍 = 정밀(DefaultRing) ↔ 밋밋(BasicRing) 을 이 근접에서 번갈아 A/B
    if "DefaultRing" in ring_models and "BasicRing" in ring_models:
        narr("정밀 vs 밋밋 — 번갈아 보며 비교", 1.5)
        for _ in range(3):
            show_ring("DefaultRing", 3.0)
            show_ring("BasicRing", 3.0)
    t2.setIntensity(0.0, Anim(1.0))
else:
    print("   ⚠️ RingModel enum 비어있음 — 로그의 [enum] 확인")

# ── 대기/렌더 미세조정 (미사용 코드) ────────────────────────
narr("가스 행성의 띠와 색을 매만진다", 1.5)
feat("setScatteringIntensity", 1.0, Anim(2.0), label="(대기 산란)")
feat("setPointSaturation", 1.3, Anim(2.0), label="(색 채도 ↑)")
try:
    saturn.setCloudDirection(1.0); print("   ✓ setCloudDirection(1.0)")   # 가스 띠 방향(Anim 없음)
except Exception as e:
    print("   ✗ setCloudDirection: %s" % e)
sleep(2.5)

# ── 정리 ────────────────────────────────────────────────────
narr("고리는 얼음과 바위의 수십억 조각", 3.5)
t1.setText("토성 — 46억 년의 얼음 고리"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.5); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①B=45 로 고리가 활짝 열려 보이나(고리면 디테일) ②setRingModel 하드컷으로 "
      "4모델(Asteroids/Asteroids_3_0/BasicRing/DefaultRing)이 각각 다르게 보이나 — 특히 DefaultRing↔Asteroids A/B "
      "③어떻게 다른지(예: 알갱이/입자 vs 매끈한 띠, 색, 카시니 간극) ④산란/채도 효과 ⑤줌/구도 OK?")

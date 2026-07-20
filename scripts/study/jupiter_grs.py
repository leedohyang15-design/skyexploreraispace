# -*- coding: utf-8 -*-
"""
jupiter_grs.py — 목성: 대적점과 줄무늬 (2026-07-16, 비(非)지구 클로즈업 — 목성 자전 연출)
★ 지구 쇼가 연달아 많아 이번엔 목성(태양계 최대 행성, 지구 11배 지름):
  · 가로 줄무늬(벨트/존) = 초고속 제트기류 · 대적점(Great Red Spot) = 지구 2~3배 크기의 300년 넘은 폭풍.
  · 목성은 태양계에서 가장 빨리 자전(~9.9시간) → 시간가속하면 줄무늬·대적점이 빠르게 쓸려 흐름.
★ 재활용(확정): 가스행성 FadeTo(옆 도킹 R=5,B20) + 그림자 OFF(전체 밝게=줄무늬 온전) + 관성 프레임(EquatorialJ2000)
  + setRotationSpeedScale + 시간가속. 새 시도: setCloudModel(CassiniJuno)=목성/가스행성 구름 룩(있으면).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN  = Planet.PlanetName
jup = Planet(PN.Jupiter)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def rlog(tag):
    try:
        p = cam.positionLBR; print("   [%s] L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] %s" % (tag, e))


def dark_clamp(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(step); t += step


# ── 무대: 우주(목성으로) ────────────────────────────────────
print("무대: 우주 — 목성, 대적점과 줄무늬")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))

# ── FadeTo 목성 (가스행성 옆 도킹) ──────────────────────────
h = DataManager.database().data(Data.Type.PlanetType, "Jupiter")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); dark_clamp(4.5); print("   FadeTo Jupiter")
cam.setTargetHeight(30.0, Anim(0.0))
rlog("FadeTo 후")

# ── 목성 렌더: 그림자 OFF(전체 밝게=줄무늬 온전) ────────────
jup.setIntensity(1.0, Anim(0.0))
feat(jup, "setShadowStrength", 0.0, Anim(0.0), label="(그림자 OFF)")
feat(jup, "setShadowContrast", 0.0, Anim(0.0))
feat(jup, "setPlanetShineStrength", 1.0, Anim(0.0), label="(전체 밝게)")
# 새 시도: 가스행성 구름 모델(있으면)
if hasattr(Planet, "CloudModel") and hasattr(Planet.CloudModel, "CassiniJuno"):
    feat(jup, "setCloudModel", Planet.CloudModel.CassiniJuno, label="(구름 모델 CassiniJuno)")

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setColor(Vec(1.0, 0.85, 0.6)); t1.setDistance(20.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.1)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("태양계에서 가장 큰 행성 — 목성", 4.0)
narr("지구 1300개가 들어가는 거대한 가스 덩어리", 4.0)

# ── 줌인(줄무늬가 화면 가득) ────────────────────────────────
narr("가로 줄무늬 — 초속 수백 km 의 제트기류", 3.5)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.6), Anim.cubic(5.0), -1); sleep(5.3)   # R 5→3, 목성 크게
    rlog("줌인 후")
except Exception as e:
    print("   줌인 실패: %s" % e)
narr("밝은 띠(존)와 어두운 띠(벨트)가 반대 방향으로 흐른다", 4.5)

# ── 관성 프레임 전환 (자전 준비, 암전 속) ───────────────────
narr("대적점 — 지구 두세 개 크기의 300년 된 폭풍", 4.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.3)); dark_clamp(1.4)
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = jup.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, 5.0, p.z), Anim(0.0), ip)     # 적도 옆(B5) = 자전축 세로·줄무늬 가로
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.0), ip)
        cam.setTargetHeight(30.0, Anim(0.0))
        INERTIAL = ip; print("   ★ 관성 프레임=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
dark_clamp(0.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── ★ 자전: 목성이 9.9시간에 한 바퀴 (관성프레임+배율↑+날짜Δ최소) ─
#   ⚠️ v1 버그: reset 은 날짜를 '오늘(7/16)'로 맞추는데 setDateTime(6/17)로 넣어 사실상 −29일 되감음 →
#   그 29일치 하늘이 통째로 돌아 '배경 별 미친 회전'(사용자), 목성 자전이 그 속에 묻힘.
#   → CLAUDE.md 규칙: 관성 프레임 + '배율↑ + 날짜Δ 최소'. 배율 6 × +6h = ~3.6바퀴(9.9h주기), 날짜 6h치라 별 거의 고정.
narr("목성은 태양계에서 가장 빨리 돈다 — 단 9.9시간에 한 바퀴", 4.0)
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 16, 12, 0, 0, tz, Anim(0.0)); sleep(0.6)     # ★ 시작 날짜 instant 고정(오늘 근처)
feat(jup, "setRotationSpeedScale", 6.0, label="(자전 배율 ↑ = 날짜 조금만 흘려도 여러 바퀴)")
dm.setDateTime(2026, 7, 16, 18, 0, 0, tz, Anim(28.0)); sleep(29.0)   # +6h × 배율6 = ~3.6바퀴, 별 거의 고정
dm.stop()
feat(jup, "resetRotationSpeedScale", label="(자전 배율 원복)")
narr("줄무늬가 쓸려 흐르고, 대적점이 돌아 나온다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("목성 — 실패한 별, 태양이 되지 못한 거인", 4.5)
narr("대적점과 줄무늬 — 끝없이 몰아치는 폭풍의 세계", 4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v2 날짜버그 수정): ①(확인)줄무늬 뚜렷·대적점 보임·CassiniJuno ✓ "
      "②★★이번엔 배경 별이 '거의 고정'되나(날짜 +6h 로 최소화 — v1은 -29일 되감아 별이 미쳐 돌았음) — 핵심 "
      "③★별이 고정된 채 목성만 자전(~3.6바퀴)해서 '줄무늬·대적점이 도는 게' 이제 보이나 "
      "④그래도 별이 돌면 배율 더↑/날짜Δ 더↓ 로 미세조정")

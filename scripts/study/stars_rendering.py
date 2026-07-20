# -*- coding: utf-8 -*-
"""
stars_rendering.py — 별하늘의 여러 얼굴 (2026-07-15, 미사용 코드 중심)
★ 전부 처음 쓰는 Stars 렌더링 노브 (전천이 확 바뀌어서 '차이'가 확실히 보임):
  setExposure(노출=전체 밝기/블룸) · setContrast(대비=희미한 별 컷오프) ·
  setPointSaturation(별 색 채도) · setModelset(별 렌더링 모델셋) · setTwinklingAmplitude(반짝임, 기존).
★ 지상 밤하늘에서 하늘만 보며 노브를 하나씩 큰 폭으로 스윕 → 차이가 뚜렷.
  Modelset enum 은 dir() 로 프로브. 원본값은 읽어서 복귀(하드코딩 금지).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
stars = Stars(Stars.StarsName.StarrySky)
galaxy = Galaxy(Galaxy.GalaxyName.MilkyWay)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:18] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def rd(obj, prop, default):
    try:
        v = getattr(obj, prop)
        print("   원본 %s.%s = %s" % (type(obj).__name__, prop, v)); return v
    except Exception as e:
        print("   %s 못읽음(%s) → 기본 %s" % (prop, e, default)); return default


def probe_enum(name, cls):
    try:
        mem = [m for m in dir(cls) if not m.startswith("_") and not m.islower() and "Invalid" not in m]
        print("[enum] %s: %s" % (name, mem)); return mem
    except Exception as e:
        print("[enum] %s 실패: %s" % (name, e)); return []


# ── enum 프로브 ─────────────────────────────────────────────
modelsets = probe_enum("Modelset", getattr(Stars, "Modelset", None)) if hasattr(Stars, "Modelset") else []

# ── 무대: 지상 밤하늘 ───────────────────────────────────────
print("무대: 지상 밤하늘")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
# 밤하늘을 새까맣게: 지구 본체는 켜되 대기 글로우 OFF(검은 하늘), 태양은 밤이라 지평선 아래
Planet(PN.Earth).setIntensity(1.0, Anim(0.0))
try:
    Planet(PN.Earth).setAtmosphereIntensity(0.0, Anim(0.0))   # ★ 대기광 끔 = 별이 잘 보이는 검은 하늘
except Exception:
    pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
galaxy.setIntensity(0.7, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주 근교
dm.stop(); sleep(0.3)
# ⚠️⚠️ DefaultTimeZone = UTC! (실측 확정) — 청주 KST=UTC+9 이므로 '밤 23:30(KST)' = UTC 14:30.
#   (v1 버그: 23:30 을 그대로 넣어 23:30 UTC=KST 08:30=대낮 → 별 안 보이고 지형만 밝음)
dm.setDateTime(2026, 8, 1, 14, 30, 0, tz, Anim(0.5)); sleep(1.0)          # = KST 23:30 (깊은 밤)
cam.setTargetHeight(55.0, Anim(0.0)); cam.setOrientationH(30.0, Anim(0.0))  # 하늘 위쪽(지형 덜 보이게)

# 원본값 읽어두기(복귀용)
o_exp = rd(stars, "exposure", 1.0)
o_con = rd(stars, "contrast", 1.0)
o_sat = rd(stars, "pointSaturation", 1.0)
o_twk = rd(stars, "twinklingAmplitude", 1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("별하늘의 여러 얼굴 — 같은 하늘, 다른 렌더링"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 제1장: 노출(Exposure) — 전체 밝기/블룸 ──────────────────
narr("제1장 — 노출: 하늘 전체의 밝기", 3.0)
feat(stars, "setExposure", o_exp * 2.6, Anim(4.0), label="(노출 ↑ = 밝고 별이 부풀음)"); sleep(4.2)
narr("노출을 낮추면 — 밝은 별만 또렷", 1.0)
feat(stars, "setExposure", o_exp * 0.45, Anim(4.0), label="(노출 ↓)"); sleep(4.2)
feat(stars, "setExposure", o_exp, Anim(2.5), label="(노출 원복)"); sleep(2.7)

# ── 제2장: 대비(Contrast) — 희미한 별 컷오프 ───────────────
narr("제2장 — 대비: 희미한 별을 살릴까 지울까", 3.0)
feat(stars, "setContrast", o_con * 0.4, Anim(4.0), label="(대비 ↓ = 희미한 별까지 촘촘)"); sleep(4.2)
narr("대비를 올리면 — 밝은 별만 남고 배경이 깨끗", 1.0)
feat(stars, "setContrast", o_con * 2.4, Anim(4.0), label="(대비 ↑)"); sleep(4.2)
feat(stars, "setContrast", o_con, Anim(2.5), label="(대비 원복)"); sleep(2.7)

# ── 제3장: 채도(PointSaturation) — 별의 색 ─────────────────
#   ⚠️ v1: ×2.2 는 별이 대부분 흰색이라 색 변화가 은근(사용자 "채도는 애매"). → 0 ↔ 4.5 로 크게 + 길게 홀드.
narr("제3장 — 채도: 별의 색을 살린다", 3.0)
feat(stars, "setPointSaturation", 0.0, Anim(3.5), label="(채도 0 = 완전 흑백)"); sleep(4.5)
narr("채도를 확 올리면 — 청백(뜨거운 별)·주황(차가운 별)", 1.5)
feat(stars, "setPointSaturation", 4.5, Anim(4.0), label="(채도 ×4.5 = 색 확 뜸)"); sleep(6.0)
# 흑백↔풀컬러 직접 A/B 로 대비 부각
narr("흑백 ↔ 컬러 — 번갈아 보기", 1.0)
for _ in range(2):
    feat(stars, "setPointSaturation", 0.0, Anim(1.5)); sleep(2.2)
    feat(stars, "setPointSaturation", 4.5, Anim(1.5)); sleep(2.2)
feat(stars, "setPointSaturation", o_sat, Anim(2.5), label="(채도 원복)"); sleep(2.7)

# ── 제4장: 모델셋(Modelset) — 렌더링 스타일 교체 ───────────
if modelsets:
    narr("제4장 — 모델셋: 별 렌더링 방식 자체를 바꾼다", 3.0)
    t2 = InsertText(InsertText.InsertTextName(2))
    cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
    t2.setPosition(Vec(0, 18, 0)); t2.setSize(0.045); t2.setDistance(1.0, Anim(0.0))
    t2.setColor(Vec(0.8, 0.9, 1.0))
    for ms in modelsets:
        if feat(stars, "setModelset", getattr(Stars.Modelset, ms), label="(Modelset=%s)" % ms):
            t2.setText("Modelset: %s" % ms); t2.setIntensity(1.0, Anim(0.5))
            sleep(4.5)
    t2.setIntensity(0.0, Anim(1.0))
else:
    print("   ⚠️ Modelset enum 비어있음 — 로그 확인")

# ── 보너스: 반짝임 ──────────────────────────────────────────
narr("그리고 반짝임 — 대기가 만든 깜빡임", 2.0)
feat(stars, "setTwinklingAmplitude", 2.5, Anim(3.0), label="(반짝임 ↑)"); sleep(3.2)
feat(stars, "setTwinklingAmplitude", o_twk, Anim(2.0), label="(원복)"); sleep(2.2)

# ── 정리 ────────────────────────────────────────────────────
narr("같은 별, 다른 얼굴 — 렌더링이 하늘을 결정한다", 3.5)
t1.setText("별하늘 — 노출·대비·채도·모델셋"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①노출 ↑↓ 로 하늘 밝기/블룸 바뀌나 ②대비 ↓ 로 희미한 별이 촘촘/↑ 로 깨끗해지나 "
      "③채도 0(흑백)↔↑(색) 별색 바뀌나 ④Modelset enum 멤버 뭐뭐였나 + 모델셋마다 렌더링 다른가 "
      "⑤원본값 읽기 됐나(로그 '원본 ...') ⑥어느 노브가 제일 효과 큰가")

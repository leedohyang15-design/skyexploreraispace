# -*- coding: utf-8 -*-
"""
lut_stars.py — Lut(별 스프라이트/점확산함수) 렌더 튜닝 (2026-07-22, 완본 미개척)
★ Lut = 별(점광원)을 스프라이트로 그리는 방식의 LUT. 등급(magnitude)→크기/색 매핑.
  메서드: createPSF(샘플수, 등급min, 등급max, 크기max)=점확산함수 생성 · setSpriteScale/setDiameterScale=별 크기 배율 ·
  setSpriteSizeLimit/setSmoothSizeLimit/setTransitionBandWidth · setSpriteTexture(스프라이트 이미지)=별 글로우 모양 · setColorPalette(파일,등급).
  Lut001~005 슬롯(고정). 별 렌더러가 특정 슬롯을 읽는지(자동적용) vs 바인딩 필요한지 = 이번에 판별.
★ 미디어/하드웨어(영상·오디오·DMX)는 별도 호스트라 죽었음 → 이번엔 '렌더 오브젝트'라 창에서 보일 가능성.
★ 전략: dir() 덤프로 바인딩/기본값 확인 + 밝은 별밭에서 스프라이트 배율을 크게 스윕 → 별이 커지/변하면 자동적용.
  Lut001~005 전 슬롯에 같은 설정을 걸어 어느 슬롯이 활성인지도 커버.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:90])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:30]


# ── 무대: 밝은 별밭 (효과 잘 보이게) ────────────────────────
print("무대: Lut — 별 스프라이트 렌더 튜닝")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky)
stars.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(20.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── Lut 생성 + dir() 덤프 ───────────────────────────────────
narr("별 스프라이트 LUT — Lut", 2.5)
lut = None
try:
    lut = Lut(Lut.LutName.Lut001); print("   Lut001 생성")
except Exception as e:
    print("   Lut 생성 실패: %s" % str(e)[:90])

if lut is not None:
    meths = [m for m in dir(lut) if not m.startswith("__")]
    print("   [Lut dir()] %s" % meths)
    # 바인딩 후보(별에 적용/타겟) 있나
    binders = [m for m in meths if any(k in m.lower() for k in ("apply", "bind", "target", "set", "assign", "active"))]
    print("   [바인딩 후보] %s" % binders)
    for p in ("gamma", "diameterScale", "spriteScale", "spriteSizeLimit", "smoothSizeLimit", "transitionBandWidth", "points"):
        print("   기본값 %s = %s" % (p, rd(lut, p)))

# 모든 슬롯에 동일 설정(어느 슬롯이 활성인지 커버)
def all_luts():
    out = []
    for i in range(1, 6):
        try:
            out.append(Lut(Lut.LutName(i)))
        except Exception:
            pass
    return out


luts = all_luts()
print("   활성 시도 슬롯 수 = %d" % len(luts))


def apply_all(fn, *args):
    for l in luts:
        try:
            getattr(l, fn)(*args)
        except Exception as e:
            print("   (%s 슬롯 실패: %s)" % (fn, str(e)[:40]))


if lut is not None:
    # ① PSF 생성 (별 등급→크기 곡선). 등급 -1~6, 최대크기 크게.
    narr("① 점확산함수(PSF) 생성", 2.5)
    feat(lut, "createPSF", 256, -1.5, 6.5, 40.0, label="(sample256, mag -1.5~6.5, sizeMax40)")
    apply_all("createPSF", 256, -1.5, 6.5, 40.0)
    sleep(2.0)

    # ② 스프라이트/지름 배율 크게 스윕 → 별이 커지나?
    narr("② 별 크게 — spriteScale ↑↑", 2.0)
    feat(lut, "setSpriteScale", 6.0, Anim(3.0), label="(×6)")
    apply_all("setSpriteScale", 6.0, Anim(3.0))
    sleep(3.2)
    narr("③ diameterScale ↑↑", 2.0)
    feat(lut, "setDiameterScale", 6.0, Anim(3.0), label="(×6)")
    apply_all("setDiameterScale", 6.0, Anim(3.0))
    sleep(3.2)

    # ④ 크기 제한 완화 (큰 별 더 크게)
    narr("④ 크기 상한 완화 — sizeLimit ↑", 2.0)
    feat(lut, "setSpriteSizeLimit", 60.0, Anim(2.0)); apply_all("setSpriteSizeLimit", 60.0, Anim(2.0))
    feat(lut, "setSmoothSizeLimit", 60.0, Anim(2.0)); apply_all("setSmoothSizeLimit", 60.0, Anim(2.0))
    sleep(2.5)
    narr("⑤ 별이 커졌나? (원복 전 관찰)", 4.0)

    # ⑥ 원복
    narr("원래대로 — ×1", 2.0)
    feat(lut, "setSpriteScale", 1.0, Anim(2.0)); apply_all("setSpriteScale", 1.0, Anim(2.0))
    feat(lut, "setDiameterScale", 1.0, Anim(2.0)); apply_all("setDiameterScale", 1.0, Anim(2.0))
    sleep(2.5)
    narr("Lut — 별 스프라이트 렌더 LUT", 3.0)
else:
    narr("Lut 생성 실패 — 로그 확인", 4.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Lut 판별). ★리포트: "
      "①★②~④ 단계에서 하늘의 '별들이 눈에 띄게 커지거나 모양/글로우가 변했나' (커졌다 / 미미하다 / 전혀 안 변함) "
      "②로그 '[Lut dir()]' 와 '[바인딩 후보]' 목록 붙여줘 — 별에 '적용/바인딩'하는 메서드가 따로 있는지 확인용 "
      "③로그 '기본값 spriteScale/diameterScale = ..' 값도 (원본 배율 파악) "
      "④전혀 안 변하면 = Lut 는 자동적용이 아니라 별도 바인딩/시스템 소관 → dir() 보고 다음 방법 결정")

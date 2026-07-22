# -*- coding: utf-8 -*-
"""
lut_texture_palette.py — Lut 스프라이트/팔레트 v2 (2026-07-22, 결정적 재검증)
★ v1: 스프라이트가 기본 별과 비슷(십자+코어)해서 바뀌었는지 구분 안 됨 + 팔레트 무변(사용자 "안 바뀐 거 같애").
★ v2 결정판: ①스프라이트 = **밝은 링(도넛)** = 기본 별과 완전 달라 → 별이 고리로 바뀌면 100% 적용 확인.
  ②팔레트 = **극단 초록→빨강** + 가로/세로 두 파일 순차 시도(포맷/방향 문제 판별). 색 안 바뀌면 팔레트는 이 빌드서 무효.
★ 파일 3개 유저폴더(D:/SkyExplorer-Data/user): star_ring.png / star_palette2.png(가로) / star_palette2v.png(세로).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

base = None
try:
    base = str(Configuration.configuration().localUserFolder).rstrip("/\\")
    print("★ 유저폴더 = %r" % base)
except Exception as e:
    print("Configuration 실패: %s" % e)


def P(name):
    return (base + "/" + name) if base else name


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:110])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:40]


# ── 무대: 밝은 별밭 ─────────────────────────────────────────
print("무대: Lut v2 — 링 스프라이트 + 극단 팔레트")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 3.0, Anim(0.0), label="(채도↑)")
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.25, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


lut = Lut(Lut.LutName.Lut001)
orig_sprite = rd(lut, "spriteTexture")
orig_ss = rd(lut, "spriteScale")
print("   원본: spriteTexture=%r spriteScale=%s" % (orig_sprite, orig_ss))

# ── ① 링 스프라이트 = 기본 별과 완전 다른 모양 (결정적) ─────
narr("① 별 모양 = 밝은 링(도넛)?", 2.5)
# 밝은 별이 크게 보이도록 스케일↑ + 크기상한 완화
feat(lut, "setSpriteScale", 18.0, Anim(0.0), label="(크게)")
feat(lut, "setSpriteSizeLimit", 60.0, Anim(0.0))
feat(lut, "setSmoothSizeLimit", 60.0, Anim(0.0))
feat(lut, "setSpriteTexture", P("star_ring.png"), Anim(1.0), label="(star_ring.png)")
print("   적용후 spriteTexture=%r" % rd(lut, "spriteTexture"))
sleep(2.0)
narr("★ 밝은 별들이 '동그란 고리(링)' 모양인가?", 6.0)

# ── ② 극단 팔레트 (가로) ────────────────────────────────────
narr("② 색 = 밝은별 초록 / 어두운별 빨강? (가로파일)", 2.5)
feat(lut, "setColorPalette", P("star_palette2.png"), -1.5, 6.5, label="(가로 초록→빨강)")
sleep(2.0)
narr("★ 별 색이 초록~빨강으로 갈렸나?", 5.0)

# ── ②b 세로 파일로 재시도 (방향 문제 판별) ─────────────────
narr("②b 세로 파일로 재시도", 2.0)
feat(lut, "setColorPalette", P("star_palette2v.png"), -1.5, 6.5, label="(세로)")
sleep(2.0)
narr("★ 이번엔 색이 갈렸나? (세로파일)", 5.0)

# ── 원복 ────────────────────────────────────────────────────
narr("원래대로", 2.0)
if isinstance(orig_sprite, str) and orig_sprite:
    feat(lut, "setSpriteTexture", orig_sprite, Anim(1.0), label="(원본 스프라이트)")
feat(lut, "setSpriteScale", float(orig_ss) if isinstance(orig_ss, (int, float)) else 6.0, Anim(1.5))
feat(lut, "setDiameterScale", 1.38, Anim(1.5))
sleep(1.8)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Lut v2). ★리포트: "
      "①★★스프라이트 구간(①)에서 밝은 별들이 '동그란 링/고리' 모양으로 보였나 (링 보임=setSpriteTexture 확정 / 그냥 점=미적용) "
      "②★팔레트 가로(②)·세로(②b) 중 별 색이 '초록~빨강'으로 갈린 게 있나 (있음=포맷 정답 / 둘 다 무변=팔레트 무효) "
      "③로그 '원본 spriteTexture=' / '적용후 spriteTexture=' 값 붙여줘(경로 반영됐나 확인)")

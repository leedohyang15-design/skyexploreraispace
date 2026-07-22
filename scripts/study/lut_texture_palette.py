# -*- coding: utf-8 -*-
"""
lut_texture_palette.py — Lut 스프라이트/팔레트 v3 (2026-07-22, 배율 정상화)
★ v2 결과: 링 스프라이트 + spriteScale 18 → 별이 거대 링이 돼 수천개 겹쳐 **하늘 전체 하양**(=setSpriteTexture 확정 적용, 배율 과함).
★ v3: spriteScale 을 **작게(1.2→2.5)** 로 낮춰 개별 별이 '작은 링'으로 보이게. 그 상태에서 팔레트(가로/세로) 색 판별.
★ 파일(유저폴더): star_ring.png / star_palette2.png / star_palette2v.png (이미 넣어둠).
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


print("무대: Lut v3 — 링 스프라이트(작게) + 팔레트")
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
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


lut = Lut(Lut.LutName.Lut001)
orig_sprite = rd(lut, "spriteTexture")
print("   원본: spriteTexture=%r" % orig_sprite)

# ── ① 링 스프라이트 작게 = 개별 별이 작은 링 ────────────────
narr("① 링 스프라이트 (배율 작게)", 2.5)
# ⚠️ 크기 상한 낮게 + 배율 작게 = 별이 서로 안 겹치게
feat(lut, "setSpriteSizeLimit", 3.0, Anim(0.0))
feat(lut, "setSmoothSizeLimit", 3.0, Anim(0.0))
feat(lut, "setSpriteTexture", P("star_ring.png"), Anim(1.0), label="(star_ring.png)")
feat(lut, "setSpriteScale", 1.2, Anim(1.0), label="(1.2 작게)")
sleep(2.0)
narr("★ 별들이 '작은 링/고리'로 보이나?", 5.0)
narr("조금 키움 (2.5)", 1.0)
feat(lut, "setSpriteScale", 2.5, Anim(2.0)); sleep(2.5)
narr("★ 밝은 별이 링 모양 뚜렷?", 4.0)

# ── ② 팔레트 (가로 → 세로) ──────────────────────────────────
narr("② 색 팔레트 — 가로파일 (초록↔빨강)", 2.5)
feat(lut, "setColorPalette", P("star_palette2.png"), -1.5, 6.5, label="(가로)")
sleep(2.0)
narr("★ 별 색이 초록~빨강으로 갈렸나? (가로)", 4.5)
narr("②b 세로파일로 재시도", 2.0)
feat(lut, "setColorPalette", P("star_palette2v.png"), -1.5, 6.5, label="(세로)")
sleep(2.0)
narr("★ 이번엔 색이 갈렸나? (세로)", 4.5)

# ── 원복 ────────────────────────────────────────────────────
narr("원래대로", 2.0)
if isinstance(orig_sprite, str) and orig_sprite:
    feat(lut, "setSpriteTexture", orig_sprite, Anim(1.0))
feat(lut, "setSpriteScale", 6.0, Anim(1.5)); feat(lut, "setSpriteSizeLimit", 2.346, Anim(1.0))
feat(lut, "setSmoothSizeLimit", 0.621, Anim(1.0))
sleep(1.8)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Lut v3). ★리포트: "
      "①★배율 낮춘 상태에서 별들이 '작은 링(고리)' 모양으로 보였나 (v2 는 배율18로 하얗게 탐 = 적용은 확정) "
      "②★팔레트 가로/세로 중 별 색이 초록~빨강으로 갈린 게 있나 (있음=팔레트도 성공 / 둘 다 무변=팔레트 무효) ")

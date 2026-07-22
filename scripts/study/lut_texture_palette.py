# -*- coding: utf-8 -*-
"""
lut_texture_palette.py — Lut 스프라이트 텍스처 + 등급별 색 팔레트 (2026-07-22, Lut 미검증 명령 2종)
★ 오늘 검증한 Lut 의 남은 두 명령: setSpriteTexture(별 글로우 '모양' 이미지 교체) · setColorPalette(등급→'색' 매핑).
  Lut 은 자동적용(바인딩 불필요)이라 값만 걸면 전천 별 렌더에 반영됨(실측 확정).
★ 파일 2개(유저폴더 D:/SkyExplorer-Data/user 에):
  · star_sprite.png = 회절 스파이크(십자) + 소프트 코어 별 모양 → 모든 별이 '스파이크 별'로 변함.
  · star_palette.png = 가로 그라데이션(밝은별 청백 → 어두운별 적색) → 별이 등급별 색으로.
★ 흐름: 기본 점 별 → 스프라이트 교체(스파이크) → 색 팔레트(등급색) → 원복(기본값 spriteScale=6.0/diameterScale=1.38).
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
SPRITE = (base + "/star_sprite.png") if base else "star_sprite.png"
PALETTE = (base + "/star_palette.png") if base else "star_palette.png"


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
print("무대: Lut — 스프라이트 텍스처 + 색 팔레트")
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
feat(stars, "setPointSaturation", 2.5, Anim(0.0), label="(색 채도 ↑ = 팔레트 잘 보이게)")
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.3, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── Lut 준비 + 원본값 보관 ──────────────────────────────────
lut = Lut(Lut.LutName.Lut001)
orig_sprite = rd(lut, "spriteTexture")
orig_ss = rd(lut, "spriteScale")
orig_ds = rd(lut, "diameterScale")
print("   원본: spriteTexture=%r spriteScale=%s diameterScale=%s" % (orig_sprite, orig_ss, orig_ds))

narr("기본 별 (점광원)", 4.0)

# ── ① 스프라이트 텍스처 = 별 모양 교체 (스파이크 별) ────────
narr("① 별 모양 교체 — 회절 스파이크", 2.5)
feat(lut, "setSpriteTexture", SPRITE, Anim(1.0), label="(star_sprite.png)")
feat(lut, "setSpriteScale", 14.0, Anim(2.0), label="(스파이크 크게)")
feat(lut, "setSpriteSizeLimit", 40.0, Anim(1.0))
sleep(2.5)
narr("★ 모든 별이 십자 스파이크로 변했나?", 5.0)

# ── ② 색 팔레트 = 등급별 색 ─────────────────────────────────
narr("② 등급별 색 — 밝은별 청백 / 어두운별 적색", 2.5)
feat(lut, "setColorPalette", PALETTE, -1.5, 6.5, label="(mag -1.5~6.5)")
sleep(2.5)
narr("★ 별들이 밝기(등급)에 따라 색이 달라졌나?", 5.0)

# 스파이크 조금 줄여 색이 더 잘 보이게
feat(lut, "setSpriteScale", 9.0, Anim(2.0)); sleep(2.2)
narr("스파이크 + 등급색 = 화려한 밤하늘", 4.0)

# ── 원복 (기본값으로 — 하드코딩 1.0 금지) ───────────────────
narr("원래대로 복귀", 2.0)
if isinstance(orig_sprite, str) and orig_sprite:
    feat(lut, "setSpriteTexture", orig_sprite, Anim(1.0), label="(원본 스프라이트)")
feat(lut, "setSpriteScale", float(orig_ss) if isinstance(orig_ss, (int, float)) else 6.0, Anim(1.5))
feat(lut, "setDiameterScale", float(orig_ds) if isinstance(orig_ds, (int, float)) else 1.38, Anim(1.5))
sleep(1.8)

narr("Lut — 별 모양·색 커스터마이즈", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Lut 텍스처/팔레트). ★리포트: "
      "①★스프라이트 교체(①)에서 모든 별이 '십자 스파이크(회절)' 모양으로 변했나 (변함/미미/무변) "
      "②★색 팔레트(②)에서 별들이 등급(밝기)별로 색(청백~적색)이 달라졌나 (변함/무변) "
      "③로그 '원본: spriteTexture=..' 값(기본 스프라이트 경로) 붙여줘 "
      "④둘 다 무변이면 = setSpriteTexture/setColorPalette 는 파일경로/포맷 더 파야 함")

# -*- coding: utf-8 -*-
"""
clock_textures.py — Clock 커스텀 문자판/바늘 텍스처 (2026-07-22, C-⑤ 마지막)
★ Clock 의 미검증 텍스처 세터: setBackgroundTexture(문자판) · setForegroundTexture(눈금) ·
  setHoursHandTexture / setMinutesHandTexture / setSecondsHandTexture(바늘 이미지). 경로=유저폴더.
★ 오늘 Lut.setSpriteTexture 가 됐으니 이미지 세터 계열은 될 가능성 높음. 기본 스위스 시계 → 커스텀(남색+금테 별 문자판 + 주황 바늘)로 바뀌면 확정.
★ 파일(유저폴더 D:/SkyExplorer-Data/user): clock_face.png / clock_hand.png.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone

base = None
try:
    base = str(Configuration.configuration().localUserFolder).rstrip("/\\")
    print("★ 유저폴더 = %r" % base)
except Exception as e:
    print("Configuration 실패: %s" % e)


def P(name):
    return (base + "/" + name) if base else name


def feat(obj, fn, *args, label=""):
    if not hasattr(obj, fn):
        print("   – %s 없음" % fn); return False
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:100])); return False


# ── 무대: 밤하늘 + 시계 HUD ─────────────────────────────────
print("무대: Clock 커스텀 텍스처")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 68, 0)); txt.setSize(0.045); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 기본 시계 (스위스 철도) ─────────────────────────────────
narr("기본 시계 (스위스 철도)", 2.5)
clk = Clock(Clock.ClockName.Clock001)
feat(clk, "setModelset", Clock.Modelset.SystemClock001, label="(모델셋)")
cam.addChild(clk.id, Camera.CameraPort.FixedForeground)
feat(clk, "setPosition", Vec(0, 40, 0))
feat(clk, "setSize", 0.6)
feat(clk, "setDistance", 1.0)
feat(clk, "setDisplaySecondsHand", True)
feat(clk, "setIntensity", 1.0, Anim(0.0))
sleep(3.0)

# ── ① 문자판 (background=뒤판 + foreground=앞 눈금/숫자 레이어) ──
narr("① 문자판 — background + foreground 둘 다", 2.5)
feat(clk, "setBackgroundTexture", P("clock_face.png"), label="(뒤판=남색별)")
feat(clk, "setForegroundTexture", P("clock_fg.png"), label="(앞 눈금/숫자=금테)")
sleep(2.0); narr("★ 눈금/숫자가 '금테+숫자'로 바뀌었나? (전경)", 5.0)

# ── ② 바늘 텍스처 교체 (경로만) ─────────────────────────────
narr("② 바늘 교체 — 시/분/초침 텍스처", 2.5)
feat(clk, "setHoursHandTexture", P("clock_hand.png"), label="(시침)")
feat(clk, "setMinutesHandTexture", P("clock_hand.png"), label="(분침)")
feat(clk, "setSecondsHandTexture", P("clock_hand.png"), label="(초침)")
sleep(2.0); narr("★ 바늘이 '주황 다이아' 모양으로 바뀌었나?", 5.0)

# ── 시간가속으로 바늘 회전 확인 ─────────────────────────────
narr("시간가속 — 바늘 도나?", 2.0)
dm.setDateTime(2026, 7, 23, 13, 0, 0, tz, Anim(8.0)); sleep(4.0)
narr("★ 커스텀 시계로 하루가 도나?", 4.0)

narr("Clock — 커스텀 문자판/바늘", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Clock 텍스처). ★리포트: "
      "①문자판이 '남색+금테+별' 판으로 바뀌었나 (바뀜/그대로 스위스흰판) "
      "②바늘이 '주황 다이아' 모양으로 바뀌었나 (바뀜/그대로) "
      "③로그에 '✗ 실패'나 '– 없음' 뜬 세터 있으면 표시됨. 둘 다 그대로면 = 텍스처 세터는 미지원.")

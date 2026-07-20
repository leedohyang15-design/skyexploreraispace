# -*- coding: utf-8 -*-
"""
drawable_probe.py — DrawableInsert2D 프로브: 돔에 자유 그리기 되나? (2026-07-20, 완본 미개척)
★ DrawableInsert = 돔/화면에 붓으로 자유 드로잉(beginDraw→setBrushPosition 연속→endDraw). 슬롯 DrawableInsert2D001~003.
★ ⚠️ 위험: BrushType enum 이 'InvalidBrushType' 뿐(유효 붓 없음) → 붓 타입을 못 줌 = 안 그려질 수 있음(Bolide 모델 함정류).
  → 이번엔 '기본 붓만으로 그어지나' 최소 프로브: 굵고 밝은 원 + 대각선 하나. 뭐라도 뜨면 성공, 아니면 접음.
★ API: beginDraw() / endDraw() / setBrushColor(Vec3) / setBrushSize(float) / setBrushPosition(Vec3) / setBrushType(enum) /
  setIntensity / setParent / undo/redo/clearAll/save/load. 좌표계 미지수 → 화면(az,h) 도 컨벤션으로 시도.
"""

from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: DrawableInsert2D 프로브")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
feat(Planet(Planet.PlanetName.Earth), "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(Planet(Planet.PlanetName.Earth), "setTerrainIntensity", 0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.9, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── DrawableInsert2D 생성 ───────────────────────────────────
narr("돔에 직접 그릴 수 있을까? — DrawableInsert 프로브", 3.5)
d = None
for nm in ("DrawableInsert2D001", "DrawableInsert001", "DrawableInsert2D1"):
    if hasattr(DrawableInsert.DrawableInsertName, nm):
        try: d = DrawableInsert(getattr(DrawableInsert.DrawableInsertName, nm)); print("   DrawableInsert enum=%s" % nm); break
        except Exception as e: print("   %s 실패: %s" % (nm, e))
if d is None:
    try: d = DrawableInsert(DrawableInsert.DrawableInsertName(1)); print("   DrawableInsert(1)")
    except Exception as e: print("   생성 실패: %s" % e)

if d is not None:
    # ★ v3: 화면 HUD 부착 = addChild(FixedForeground) (InsertText/Clock/Chart2D 와 동일 패턴).
    #   v1/v2 는 setParent(cam.id) 로 붙였는데 그건 화면 오버레이가 아니라 안 그려졌을 수 있음.
    try:
        cam.addChild(d.id, Camera.CameraPort.FixedForeground); print("   ✓ addChild(FixedForeground)")
    except Exception as e:
        print("   ✗ addChild 실패: %s → setParent 폴백" % e); feat(d, "setParent", cam.id)
    # ★ v2 버그픽스: BrushType = ['Eraser','Pen'] 인데 v1 이 bts[0]='Eraser'(지우개!) 를 골라 아무것도 안 그려짐.
    #   → 'Pen'(그리기) 을 명시적으로 선택.
    bts = [m for m in dir(DrawableInsert.BrushType) if not m.startswith("__") and "Invalid" not in m and m[0].isupper()]
    print("   [BrushType 유효값] %s" % (bts or "없음(기본 붓만)"))
    pen = "Pen" if hasattr(DrawableInsert.BrushType, "Pen") else (bts[-1] if bts else None)
    if pen:
        feat(d, "setBrushType", getattr(DrawableInsert.BrushType, pen), label="(★ 붓=%s)" % pen)
    feat(d, "setBrushColor", Vec(1.0, 0.85, 0.3), label="(노랑)")
    feat(d, "setBrushSize", 2.0, label="(굵기 2.0)")
    feat(d, "setIntensity", 1.0, Anim(0.0))

    # ── 그리기 1: 큰 원 (화면 az/h 좌표, 중심 0/45, 반경 15) ──
    narr("① 큰 원을 그린다", 2.5)
    feat(d, "beginDraw", label="(beginDraw)")
    for a in range(0, 361, 12):
        r = math.radians(a)
        try: d.setBrushPosition(Vec(15.0 * math.cos(r), 45.0 + 15.0 * math.sin(r), 0.0))
        except Exception as e:
            if a == 0: print("   setBrushPosition 실패: %s" % e)
        sleep(0.04)
    feat(d, "endDraw", label="(endDraw)")
    sleep(1.5)

    # ── 그리기 2: 대각선 ────────────────────────────────────
    narr("② 대각선을 긋는다", 2.5)
    try:
        d.beginDraw()
        for t in range(0, 21):
            f = t / 20.0
            d.setBrushPosition(Vec(-18.0 + 36.0 * f, 30.0 + 30.0 * f, 0.0)); sleep(0.05)
        d.endDraw()
    except Exception as e:
        print("   대각선 실패: %s" % e)
    sleep(1.5)

    narr("뭐라도 그려졌나? (노란 원/선)", 4.0)
else:
    narr("DrawableInsert 생성 실패 — 로그 확인", 4.0)

# ── 정리 ────────────────────────────────────────────────────
if d is not None:
    feat(d, "clearAll", Anim(1.0), label="(지우기)")
    feat(d, "setIntensity", 0.0, Anim(1.0))
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v3 addChild). ★프로브 리포트: ①★이번엔 addChild(FixedForeground)로 붙였으니 노란 원/대각선이 그려지나 "
      "(v1=Eraser, v2=setParent 로 안 됐음 → v3 는 Pen + 화면HUD 부착) "
      "②원이 이상한 위치/모양이면 좌표계 조정 ③그래도 안 그려지면 DrawableInsert 접고 Ephemeris 로 넘어감")

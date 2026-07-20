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

    # ── ★ v4: 방위각-등거리(fisheye) 보정 = 진짜 정원 ─────────
    #   돔 = 천정(h=90)이 화면중심, 지평(h=0)이 가장자리 → 화면반지름 r=90-h, 화면각도=az.
    #   화면 직교좌표(X,Y)에서 원/선을 만들고 az/h 로 역변환하면 등거리 투영에서 '정원'이 됨.
    #   (v3 는 az/h 를 평면 취급해 계란형으로 찌그러졌음 — 사용자 지적.)
    def put(X, Y):
        r = math.hypot(X, Y)                       # 화면반지름 = 천정각(deg)
        th = math.degrees(math.atan2(Y, X))        # 화면각도 = 방위(deg)
        try: d.setBrushPosition(Vec(th, 90.0 - r, 0.0))
        except Exception: pass

    # 원 중심: 방위 0(남), 고도 50 → 화면 직교 중심 (Xc,Yc)
    CX_AZ, CY_H, R = 0.0, 50.0, 16.0
    rc = 90.0 - CY_H
    Xc, Yc = rc * math.cos(math.radians(CX_AZ)), rc * math.sin(math.radians(CX_AZ))

    narr("① 화면좌표 보정으로 '정원'을 그린다", 3.0)
    feat(d, "beginDraw", label="(정원)")
    for i in range(0, 61):
        t = 2.0 * math.pi * i / 60.0
        put(Xc + R * math.cos(t), Yc + R * math.sin(t)); sleep(0.03)
    feat(d, "endDraw", label="(endDraw)")
    sleep(1.2)

    # ② 십자선(가로/세로 지름) — 원이 진짜 둥근지 눈금 확인
    narr("② 십자선(지름) — 가로세로 길이가 같으면 정원", 3.0)
    for (x0, y0, x1, y1) in ((Xc - R, Yc, Xc + R, Yc), (Xc, Yc - R, Xc, Yc + R)):
        try:
            d.beginDraw()
            for j in range(0, 25):
                f = j / 24.0; put(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f); sleep(0.04)
            d.endDraw()
        except Exception as e:
            print("   선 실패: %s" % e)
    sleep(1.5)

    narr("이번엔 계란이 아니라 둥근 원인가?", 4.0)
else:
    narr("DrawableInsert 생성 실패 — 로그 확인", 4.0)

# ── 정리 ────────────────────────────────────────────────────
if d is not None:
    feat(d, "clearAll", Anim(1.0), label="(지우기)")
    feat(d, "setIntensity", 0.0, Anim(1.0))
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v4 곡면보정). ★리포트: ①★이번 원이 계란형이 아니라 '둥근 원'으로 보이나 (화면 직교좌표→az/h 역변환으로 등거리 투영 보정) "
      "②십자선 가로 길이 ≈ 세로 길이인가(정원 확인) ③아직도 눌려있으면 = 투영이 등거리 아님(orthographic 등) → 알려주면 r=sin() 등으로 재보정")

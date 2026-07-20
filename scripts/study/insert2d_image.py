# -*- coding: utf-8 -*-
"""
insert2d_image.py — Insert2D 로 로컬 이미지 표시 (2026-07-20, Patch 대체)
★ Patch 는 이미지 표시가 아니라 '프로젝션 워핑/블렌딩 패치'로 추정(position 세터 없음 → 창 Sky View 에서 안 뜸).
  → 진짜 이미지 표시 클래스 = **Insert2D**: setTexture(경로) + setPosition/setSize/setIntensity/setDistance (+setType).
★ 유저폴더 = D:/SkyExplorer-Data/user (localUserFolder 로 확인됨). patch_test.png 를 그 폴더에 넣고 실행.
  경로 후보를 절대(/)·절대(\\)·상대 순으로 각각 시도해 어느 게 뜨는지 한 번에 판별.
★ ⚠️ 전제: patch_test.png 가 'D:\\SkyExplorer-Data\\user\\patch_test.png' 에 실제로 있어야 함(탐색기로 확인).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

IMG_NAME = "patch_test.png"

# 유저폴더 자동탐색 → 경로 후보들
paths = []
try:
    folder = str(Configuration.configuration().localUserFolder)
    print("★ localUserFolder = %r" % folder)
    base = folder.rstrip("/\\")
    paths.append(("절대(/)", base + "/" + IMG_NAME))
    paths.append(("절대(\\)", base.replace("/", "\\") + "\\" + IMG_NAME))
except Exception as e:
    print("Configuration 실패: %s" % e)
paths.append(("상대", IMG_NAME))
print("★ 시도 경로들: %s" % [p for _, p in paths])


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: Insert2D — 로컬 이미지 표시")
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
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── Insert2D 생성 + HUD 부착 ────────────────────────────────
narr("로컬 이미지를 돔에 — Insert2D", 3.0)
ins = None
try:
    ins = Insert2D(Insert2D.Insert2DName.Insert2D001); print("   Insert2D001 생성")
except Exception as e:
    print("   생성 실패: %s" % e)

if ins is not None:
    try:
        cam.addChild(ins.id, Camera.CameraPort.FixedForeground); print("   ✓ addChild(FixedForeground)")
    except Exception as e:
        print("   ✗ addChild 실패: %s → setParent" % e); feat(ins, "setParent", cam.id)
    feat(ins, "setPosition", Vec(0, 45, 0), Anim(0.0), label="(중앙)")
    feat(ins, "setDistance", 1.0, Anim(0.0))
    feat(ins, "setSize", 0.6, Anim(0.0), label="(크기 0.6)")
    feat(ins, "setIntensity", 1.0, Anim(0.0))

    # 경로 후보를 하나씩 시도 (어느 게 로드되는지 육안 판별)
    for name, path in paths:
        narr("경로 시도: %s" % name, 2.0)
        feat(ins, "setTexture", path, label="(%s = %s)" % (name, path))
        sleep(3.5)
        narr("[%s] 과녁 이미지 떴나?" % name, 4.5)
    # 마지막: 크기 키워서 크게
    feat(ins, "setSize", 0.9, Anim(2.0)); sleep(2.2)
    narr("Insert2D — 돔에 얹은 로컬 이미지", 4.0)
    feat(ins, "setIntensity", 0.0, Anim(2.0)); sleep(2.2)
else:
    narr("Insert2D 생성 실패 — 로그 확인", 4.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. ★리포트: ①★★먼저 확인 — 파일이 실제로 'D:\\SkyExplorer-Data\\user\\patch_test.png' 에 있나(탐색기로) "
      "②과녁 이미지가 떴나 — 떴으면 '절대(/)'/'절대(\\)'/'상대' 중 어느 구간 "
      "③전혀 안 뜨면 = 파일이 그 폴더에 없거나 파일명이 다름(대소문자/확장자) → 정확한 파일명 알려줘")

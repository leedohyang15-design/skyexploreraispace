# -*- coding: utf-8 -*-
"""
patch_show.py — Patch 클래스: 로컬 이미지를 돔에 (2026-07-20, 완본 미개척 — 사용자 제공 파일)
★ Patch = 'live patch' 이미지 레이어. setFilename(텍스처) + setOpacity + setKeyColor(크로마키)/setHsv/setGamma/setVibrance.
  ⚠️ position/parent/addChild 세터가 없음(속성에 위치 없음) → 생성+setFilename+setOpacity 로 자동 표시(전체화면 추정).
★ 파일: 클로드가 만든 patch_test.png (과녁 링 + 'SKY EXPLORER' + 컬러바) 를 사용자가 Studio '유저폴더'에 넣음.
  → setFilename("patch_test.png") (유저폴더 상대경로). 다른 위치면 IMG_PATH 만 바꾸면 됨.
★ 흐름: 밤하늘 → 이미지 페이드인(opacity 0→1) → 색보정(hsv/vibrance/gamma) → 크로마키(배경 남색 제거→링만 하늘 위) → 아웃.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

IMG_NAME = "patch_test.png"        # 유저폴더에 넣은 파일명
IMG_REL  = IMG_NAME                 # 상대경로 후보
IMG_ABS  = None                     # 절대경로 후보(유저폴더 + 파일명)

# ★★ 유저폴더 위치를 '직접' 알아낸다 (Configuration.localUserFolder) → 로그에 찍힘 = 어디 넣을지 확정
try:
    cfg = Configuration.configuration()
    folder = cfg.localUserFolder
    print("★★ [유저폴더] localUserFolder = %r" % folder)
    try: print("   [참고] igUserFolder(0) = %r" % cfg.igUserFolder(0))
    except Exception as e: print("   igUserFolder(0) 실패: %s" % e)
    if folder:
        s = str(folder)
        sep = "" if s.endswith(("\\", "/")) else ("/" if "/" in s and "\\" not in s else "\\")
        IMG_ABS = s + sep + IMG_NAME
        print("★★ [절대경로 후보] = %r" % IMG_ABS)
except Exception as e:
    print("Configuration 실패: %s (상대경로만 시도)" % e)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: Patch — 로컬 이미지(patch_test.png)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

# 자막
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── Patch 생성 + 이미지 로드 ────────────────────────────────
narr("로컬 이미지를 돔에 띄운다 — Patch", 3.5)
p = None
for nm in ("Patch001", "Patch01", "Patch1"):
    if hasattr(Patch.PatchName, nm):
        try: p = Patch(getattr(Patch.PatchName, nm)); print("   Patch enum=%s" % nm); break
        except Exception as e: print("   %s 실패: %s" % (nm, e))
if p is None:
    try: p = Patch(Patch.PatchName(1)); print("   Patch(1)")
    except Exception as e: print("   생성 실패: %s" % e)

if p is not None:
    # 혹시 화면부착이 필요하면 시도(대개 불필요 — 실패해도 무시)
    try: cam.addChild(p.id, Camera.CameraPort.FixedForeground); print("   ✓ addChild(FixedForeground)")
    except Exception as e: print("   (addChild 없음/실패 — 정상일 수 있음: %s)" % str(e)[:40])
    feat(p, "setOpacity", 1.0, Anim(0.0))
    # ★ 절대경로 → 상대경로 순서로 각각 시도(어느 게 뜨는지 한 번에 판별)
    cand = [("절대경로", IMG_ABS)] if IMG_ABS else []
    cand += [("상대경로", IMG_REL)]
    for name, path in cand:
        narr("경로 시도: %s" % name, 2.0)
        feat(p, "setFilename", path, label="(%s = %s)" % (name, path))
        sleep(3.5)
        narr("[%s] 과녁 이미지 떴나?  %s" % (name, path), 5.0)

    # ② 색 보정 (hsv / vibrance / gamma)
    narr("② 색 보정 — 색상/채도/감마", 3.0)
    feat(p, "setHsv", Vec(0.5, 1.2, 1.0), Anim(2.0), label="(색상 회전)"); sleep(2.2)
    feat(p, "setVibrance", 1.6, Anim(1.5), label="(채도↑)"); sleep(1.7)
    feat(p, "setGamma", Vec(1.4, 1.4, 1.4), Anim(1.5), label="(감마)"); sleep(1.7)
    feat(p, "setHsv", Vec(0.0, 1.0, 1.0), Anim(1.0)); feat(p, "setGamma", Vec(1, 1, 1), Anim(1.0)); sleep(1.2)

    # ③ 크로마키 — 배경 남색 제거 → 링만 하늘 위
    narr("③ 크로마키 — 남색 배경을 지운다 → 링만 별 위에", 3.5)
    feat(p, "setKeyColor", Vec4(0.03, 0.05, 0.12, 0.25), Anim(2.0), label="(배경 남색 키아웃)"); sleep(2.5)
    narr("배경이 사라지고 별 위에 링만 떠 있나?", 4.5)

    # ── 정리 ──
    narr("Patch — 돔에 얹는 로컬 이미지 레이어", 4.0)
    feat(p, "setOpacity", 0.0, Anim(2.0)); sleep(2.2)
else:
    narr("Patch 생성 실패 — 로그 확인", 4.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v2 유저폴더 자동탐색). ★리포트: "
      "①★★로그 맨 위 '[유저폴더] localUserFolder = ...' 경로를 알려줘 — 거기가 파일 넣을 곳 "
      "②'절대경로' 시도 때 vs '상대경로' 시도 때 중 어느 쪽에서 과녁 이미지가 떴나 "
      "③둘 다 안 떴으면 = patch_test.png 를 그 localUserFolder 경로에 넣고 다시 실행(지금 다른 폴더에 있을 것) "
      "④떴으면 색보정/크로마키도 됐나")

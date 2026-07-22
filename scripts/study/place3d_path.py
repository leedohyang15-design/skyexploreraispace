# -*- coding: utf-8 -*-
"""
place3d_path.py — Place3D (3D 경로/궤적 선) 판별 (2026-07-22, 완본 미개척)
★ Place3D = TSV 파일의 위치키를 이어 '3D 경로 선/궤적(Trail)'을 공간에 그림. 우주선 항적/궤도 트레일 연출용.
  메서드: load(TSV) · setShowPath(bool) · setIntensity · setLineColor(Vec3) · setLineThickness(px) ·
  setLineDrawingMode(DrawingMode.Lines/Trail/Default) · setPlayMode(Simulation/Live/Play/ConstantSpeed) · setEvolution(0~1).
★ ⚠️ TSV 컬럼 포맷이 문서에 없음 → **스크립트가 유저폴더에 여러 포맷 후보 TSV 를 직접 써서** 하나씩 load,
  에러 메시지/showPath 로 어느 포맷이 맞는지 판별(에러가 컬럼을 알려줄 수 있음). Python 파일쓰기 가능 전제.
★ 판별용 로그 위주 — 화면에 '빛나는 곡선'이 뜨는 포맷을 찾는 게 목표.
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
        print("   ✗ %s 실패: %s" % (fn, str(e)[:110])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:40]


# 유저폴더
base = None
try:
    base = str(Configuration.configuration().localUserFolder).rstrip("/\\")
    print("★ 유저폴더 = %r" % base)
except Exception as e:
    print("Configuration 실패: %s" % e)


def write_tsv(name, rows, header=None):
    """유저폴더에 TSV 파일 생성. 성공 시 (상대명, 절대경로) 반환."""
    if base is None:
        return None
    path = base + "/" + name
    try:
        with open(path, "w") as f:
            if header:
                f.write("\t".join(header) + "\n")
            for r in rows:
                f.write("\t".join("%.5f" % v for v in r) + "\n")
        print("   [TSV 생성] %s (%d행)" % (name, len(rows)))
        return (name, path)
    except Exception as e:
        print("   [TSV 생성 실패] %s: %s" % (name, str(e)[:80]))
        return None


# ── 후보 포맷들 생성 (곡선 = 나선/원호, 넓게) ───────────────
N = 40
fmtA = [(i / (N - 1.0), math.cos(i * 0.3) * 0.5, math.sin(i * 0.3) * 0.5, i / (N - 1.0) - 0.5) for i in range(N)]   # t x y z
fmtB = [(math.cos(i * 0.3) * 0.5, math.sin(i * 0.3) * 0.5, i / (N - 1.0) - 0.5) for i in range(N)]                   # x y z
fmtC = [(i / (N - 1.0), i * 9.0, 45.0 + 20 * math.sin(i * 0.3), 1.0) for i in range(N)]                              # t az h r
fmtD = [(i / (N - 1.0), i * 9.0, 20 + i, 100.0) for i in range(N)]                                                   # t lon lat alt

candidates = []
for nm, rows in (("p3d_txyz.tsv", fmtA), ("p3d_xyz.tsv", fmtB), ("p3d_tazhr.tsv", fmtC), ("p3d_lonlatalt.tsv", fmtD)):
    c = write_tsv(nm, rows)
    if c:
        candidates.append(c)


# ── 무대 ────────────────────────────────────────────────────
print("무대: Place3D — 3D 경로 선")
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
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(45.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── Place3D dir() ───────────────────────────────────────────
narr("3D 경로 선 — Place3D", 2.5)
DM = Place3D.DrawingMode
PM = Place3D.PlayMode
try:
    probe = Place3D(Place3D.Place3DName.Place3D001)
    print("   [Place3D dir()] %s" % [m for m in dir(probe) if not m.startswith("__")])
    print("   [DrawingMode] %s" % [m for m in dir(DM) if not m.startswith("__") and "Invalid" not in m])
except Exception as e:
    print("   Place3D 프로브 실패: %s" % str(e)[:100])


# ── 후보 포맷 하나씩 load ───────────────────────────────────
slot = 1
for name, path in candidates:
    narr("포맷 시도: %s" % name, 1.5)
    try:
        p3 = Place3D(Place3D.Place3DName(slot)); slot += 1
    except Exception as e:
        print("   슬롯 생성 실패: %s" % str(e)[:60]); continue
    print("   ── load(%r) ──" % path)
    ok = feat(p3, "load", path, label="(%s)" % name)          # 절대경로
    if not ok:
        feat(p3, "load", name, label="(상대 폴백)")            # 상대명 폴백
    feat(p3, "setShowPath", True)
    feat(p3, "setIntensity", 1.0, Anim(0.0))
    feat(p3, "setLineColor", Vec(0.2, 1.0, 0.4), Anim(0.0), label="(초록)")
    feat(p3, "setLineThickness", 6.0, Anim(0.0))
    for dmn in ("Trail", "Lines", "Default"):
        if hasattr(DM, dmn):
            feat(p3, "setLineDrawingMode", getattr(DM, dmn), label="(%s)" % dmn); break
    if hasattr(PM, "Play"):
        feat(p3, "setPlayMode", PM.Play)
    feat(p3, "setEvolution", 1.0, Anim(0.0))
    sleep(0.5)
    print("   [%s] showPath=%s intensity=%s evolution=%s" % (name, rd(p3, "showPath"), rd(p3, "intensity"), rd(p3, "evolution")))
    narr("[%s] 초록 곡선이 떴나?" % name, 4.0)

narr("Place3D — 3D 경로/궤적 선", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(Place3D 판별). ★리포트: "
      "①★4개 포맷(p3d_txyz/xyz/tazhr/lonlatalt) 시도 중 화면에 '초록 곡선/궤적'이 뜬 게 있나 — 어느 포맷 "
      "②로그 '[Place3D dir()]' 와 각 'load ✓/✗' + 에러 메시지(있으면 컬럼 힌트) 붙여줘 "
      "③로그 '[name] showPath=.. intensity=.. evolution=..' 값도 "
      "④전부 안 뜨고 load 도 실패면 = TSV 포맷/프레임 더 파야 함(에러 메시지가 열쇠)")

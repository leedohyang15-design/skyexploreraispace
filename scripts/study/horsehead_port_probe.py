# -*- coding: utf-8 -*-
"""
horsehead_port_probe.py — 원본 레시피 재현: 273 위치 + 295 포트정렬 (줌 락 없이)
====================================================================
원본 SPC 재해독으로 확정한 비법:
  · 줌 락 안 씀. 조준·세우기 = **cmd295 = setOrientation*(Vec4(0,0,0,0), Anim, track=포트)**
    → "포트 좌표계에 방향 0으로 정렬" — 포트의 up 축에 맞춰 아트가 '자동으로 섬'.
  · 포트를 둘 구분(SWITCH용 vs 여행/공전용) — 포트마다 프레임이 다름.

이 probe:
  ① NebulaPort 전체 멤버 + portId 를 콘솔에 출력 (포트 지도 확보)
  ② 카메라를 LOSLocal 20pc 에 고정
  ③ 각 포트로 295 정렬을 6초씩 순회 → **말머리가 '중앙+똑바로' 선 PORT 번호** 찾기
"""
from skyExplorer import *
from studio import *
from Initialization import *

PC = 3.086e13
R_VIEW = 20.0 * PC

# ── 리셋 + 콘텐츠 ───────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
smoothReset(False)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
horse = Nebula(Nebula.NebulaName.HORSEHEAD)
horse.setIntensity(1.0, Anim(0.0))
Nebula(Nebula.NebulaName.ORION).setIntensity(0.5, Anim(0.0))

# ── ① 포트 지도 출력 ────────────────────────────────────────
ports = [n for n in dir(Nebula.NebulaPort)
         if not n.startswith("_") and "Count" not in n and "Invalid" not in n
         and n[0].isupper() and not n.islower()]
print("=== NebulaPort 지도 ===")
pids = {}
for n in ports:
    try:
        pid = horse.portId(getattr(Nebula.NebulaPort, n))
        pids[n] = pid
        print("  %-28s portId=%d" % (n, pid))
    except Exception as e:
        print("  %-28s (portId 실패)" % n)

# ── ② 카메라 위치: LOSLocal 20pc (FreeFly 안 씀 — 원본 방식) ──
cam = Camera(Camera.CameraName.MainCamera)
los = getattr(Nebula.NebulaPort, "LineOfSightLocal", None)
pos_track = horse.portId(los) if los else list(pids.values())[0]
cam.setPositionLBR(Vec(0.0, 0.0, R_VIEW), Anim(), pos_track)
sleep(1.5)


def orient_to(track_id, dur):
    """cmd295 재현: 포트 프레임에 방향 0 정렬. Smooth → HPRD 순 시도."""
    for nm in ("setOrientationSmoothXYZR", "setOrientationHPRD", "setOrientationXYZR"):
        if hasattr(cam, nm):
            try:
                getattr(cam, nm)(Vec4(0.0, 0.0, 0.0, 0.0), Anim(dur), track_id)
                return nm
            except Exception:
                pass
    return None


# ── ③ 포트별 295 정렬 순회 ──────────────────────────────────
print("=== 포트별 정렬 — '중앙+똑바로' 선 PORT 번호는? ===")
for i, n in enumerate(ports, 1):
    if n not in pids:
        continue
    used = orient_to(pids[n], 1.5)
    print(">>> PORT%d: %s (%s)" % (i, n, used or "정렬 실패"))
    sleep(6.0)

print(">>> 끝. ①포트 지도(콘솔 위쪽) 복사해주고 ②제일 좋았던 PORT 번호 알려줘.")

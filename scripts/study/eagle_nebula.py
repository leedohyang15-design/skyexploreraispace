# -*- coding: utf-8 -*-
"""
eagle_nebula.py — 독수리 성운, 창조의 기둥 (2026-07-16, 새 천체 / 확정 성운 레시피 재사용)
★ 최근 '안 쓴 코드'가 다 화면상 애매(무지개·윤슬·HiPS) → 확실히 렌더되는 성운 빌보드 코드로,
  '한 번도 안 다룬 천체' = 독수리 성운(M16)을 신선하게. 별이 태어나는 거대한 가스 기둥('창조의 기둥').
★ 레시피 = horsehead_show.py 로 확정된 성운 빌보드 안무 그대로(확실히 보임):
  · 위치 setPositionLBR(track=LOSLocal portId) · 조준 setOrientationSmoothXYZR(Vec4 0) · Target 30 · 암전 세팅 후 페이드인.
  · 인트로 프레이밍 → 기둥 속으로 비행(R 축소) → 자막 → 정면 스윙(±25°, 뒷면 실루엣 회피).
"""

from skyExplorer import *
from studio import *
from Initialization import *

PC       = 3.086e13
R_START  = 55.0 * PC       # 인트로 프레이밍(성운 전체 + 여백)
R_VIEW   = 13.0 * PC       # 기둥 근접 (아트 내부 ~2pc 주의 → 그 위로)
FLY_SEC  = 16.0
SWING_DEG = 46.0           # 정면 스윙(±23°) — 근접 360°는 뒷면 실루엣 지남(horsehead 실측)
SWING_SEC = 20.0


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 0) 하드 리셋 + 암전 ─────────────────────────────────────
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
smoothReset(False)
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

# ── 1) 콘텐츠 (암전 뒤에서) ─────────────────────────────────
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))

# 독수리 성운 확보(enum → DB 폴백)
NN = Nebula.NebulaName
neb = None
for nm in ("EAGLE", "M16", "EAGLE_NEBULA", "M16_EAGLE"):
    if hasattr(NN, nm):
        try: neb = Nebula(getattr(NN, nm)); print("   성운 enum = %s" % nm); break
        except Exception as e: print("   %s 실패: %s" % (nm, e))
if neb is None:
    print("   ⚠️ EAGLE enum 없음 → NebulaName 목록 일부: %s"
          % [m for m in dir(NN) if not m.startswith("__")][:30])
    # DB 폴백(이름)
    for dbn in ("M16", "Eagle", "Eagle Nebula", "NGC 6611"):
        h = DataManager.database().data(Data.Type.NebulaType, dbn)
        if h is not None:
            a = h.action(Action.Type.FadeTo)
            if a is not None:
                a.trigger(); sleep(4.0); print("   DB FadeTo %s" % dbn); break

cam = Camera(Camera.CameraName.MainCamera)
los = None
if neb is not None:
    neb.setIntensity(1.0, Anim(0.0))
    for pn in ("LineOfSightLocal", "LOSLocal", "LineOfSightEcliptic"):
        try:
            los = neb.portId(getattr(Nebula.NebulaPort, pn)); print("   성운 포트 = %s" % pn); break
        except Exception as e:
            print("   포트 %s 실패: %s" % (pn, e))

# ── 2) 카메라 세팅 (암전 중 = 슬루 안 보임) ─────────────────
if los is not None:
    cam.setPositionLBR(Vec(0.0, 0.0, R_START), Anim(), los)
    cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), los)
    cam.setTargetHeight(30.0, Anim(1.0))
    sleep(4.0)

# ── 3) 페이드인 + 자막 ──────────────────────────────────────
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045); txt.setColor(Vec(0.7, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.2)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("독수리 성운 — 6500광년 밖, 별들의 요람", 4.0)
narr("가스와 먼지가 뭉쳐 새 별이 태어나는 곳", 4.0)

# ── 4) 기둥 속으로 비행 (R 축소) ────────────────────────────
narr("그 한가운데로 — '창조의 기둥'", 3.0)
if los is not None:
    cam.setPositionR(R_VIEW, Anim.cubic(FLY_SEC), los); sleep(FLY_SEC + 0.5)
    cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(2.0), los)
    cam.setTargetHeight(29.9, Anim(0.3)); sleep(0.4)
    cam.setTargetHeight(30.0, Anim(0.5)); sleep(1.6)
narr("수 광년 높이의 가스 기둥 — 그 끝에서 별이 잉태된다", 4.5)

# ── 5) 정면 스윙(±23°) — 입체감 ────────────────────────────
narr("천천히 돌아 기둥의 입체를 본다", 2.5)
if los is not None:
    step_dt = 0.5
    n = int(SWING_SEC / step_dt)
    for i in range(1, n + 1):
        L = SWING_DEG * (i / float(n)) - SWING_DEG / 2.0   # -23° → +23°
        cam.setPositionLBR(Vec(L, 0.0, R_VIEW), Anim(step_dt), los)
        if i % 4 == 0:
            cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(step_dt), los)
        sleep(step_dt)

narr("우리를 이룬 원소도, 이런 성운에서 시작됐다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("독수리 성운 — 창조의 기둥", 4.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★독수리 성운(빌보드 아트)이 화면에 확실히 뜨나 — 로그 '성운 enum/포트' 확인 "
      "②페이드인→기둥 속 비행(R 55→13pc)→정면 스윙 안무 자연스럽나 ③자막/구도 OK "
      "④EAGLE enum 없으면 로그의 NebulaName 목록/DB 폴백 결과 알려줘(정확한 이름으로 교체)")

# -*- coding: utf-8 -*-
"""
messier_m42_frame.py — M42 프레이밍 완성 (2026-07-13)
★ 돌파구(스크린샷 확인): 조준 액션(LookAt/ConnectTo/GoTo)이 M42 를 '말머리와 같은 LOS Local
  프레임'(R≈412pc = 지구 거리)에 진입시킴! 성운이 풀컬러로 렌더. = setScale 이 아니라 '말머리 레시피'가 정답.
문제: 성운이 돔 '아래쪽'에 치우침(Target 30 틸트).
해결(말머리 레시피, CLAUDE.md): 성운 LOS 프레임 = Target 90 이 돔 중앙 → 센터링.
  + R 을 412pc → ~30pc 로 줄여 접근(setPositionR, track=-1) = 성운 속으로 '비행'.

절차: 조준 진입 → Target 90 센터링 → R 감소 접근. (setScale 불필요 — R 이 프레이밍/접근을 담당)
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 ─────────────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

mdb = None
try:
    mdb = DataManager.database().data(Data.Type.NebulaType, "M42")
    print("NebulaType 'M42' 핸들=%s" % (mdb is not None))
except Exception as e:
    print("DB 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("오리온 대성운(M42) — 별의 요람으로"); t1.setIntensity(1.0, Anim(1.2))
sleep(3.0)

# ── 1) 조준 진입 (LOS Local 프레임 확보) ────────────────────
print("=" * 55); print("1) 조준 진입")
nav_used = None
if mdb is not None:
    for aname in ("LookAt", "ConnectTo", "GoTo"):
        at = getattr(Action.Type, aname, None)
        a = mdb.action(at) if at is not None else None
        if a is not None:
            print("   조준 액션 = %s" % aname)
            a.trigger(); nav_used = aname
            sleep(6.0)
            break
try:
    R0 = cam.positionLBR.z
except Exception:
    R0 = 0.0
print("   진입 후 R=%.2f (LOS Local 이면 ~412pc 기대)" % R0)

# ── 2) Target 90 센터링 (성운 LOS 프레임 = 90 이 돔 중앙) ────
print("2) Target 90 센터링")
t1.setText("성운을 돔 중앙으로")
try:
    cam.setTargetHeight(90.0, Anim.cubic(3.5))
    sleep(4.0)
except Exception as e:
    print("   Target 센터링 실패: %s" % e)

# ── 3) R 감소 접근 (초대형 R → 적응형 지오메트릭 줌 = 성운 속으로 비행) ──
#   ⚠️ ConnectTo R 은 트랙반지름 단위라 초대형 → ×배율을 '많이' 반복해야 체감(아포피스 교훈).
#   매끄러운 줌 = Anim(선형) + 큰 비율(0.6) + 짧게(1.4초) + 다수(18스텝) 반복.
print("3) R 감소 적응형 접근 (setPositionR, track=-1)")
t1.setText("가까이 — 붉은 수소 구름 속으로")
if R0 > 1.0:
    try:
        for i in range(18):
            p = cam.positionLBR
            cam.setPositionR(p.z * 0.60, Anim(1.4), -1)
            sleep(1.5)
            if i % 3 == 2:
                print("   step%2d R=%.3e" % (i + 1, cam.positionLBR.z))
        print("   ★ 성운이 중앙에서 돔 가득 다가왔나? (부족/과하면 스텝수 조절)")
    except Exception as e:
        print("   접근 실패: %s" % e)
else:
    print("   R≈0 → 접근 불가(프레임 확인 필요)")
    sleep(3.0)
t1.setText("오리온 대성운 — 1,300광년 밖 별들의 탄생지")
sleep(4.0)
t1.setIntensity(0.0, Anim(0.8))

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("M42 — 겨울 밤하늘, 맨눈에도 보이는 별의 요람"); t1.setIntensity(1.0, Anim(1.0))
sleep(4.5)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.5))
sleep(4.0)
print("종료. 리포트: ①Target 90 으로 성운이 중앙 왔나(아니면 몇도가 좋아?) "
      "②18스텝 접근 중 '돔 가득 찬' 시점이 몇 step 쯤? (그 전에 지나쳐 사라지면 그 step) "
      "③조준=%s / 시작R=%.2e" % (nav_used, R0))

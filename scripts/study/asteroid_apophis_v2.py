# -*- coding: utf-8 -*-
"""
asteroid_apophis_v2.py — FadeTo 없이 소행성 줌인 (2026-07-09)
v1 실측: 궤도요소 7개 전부 반영(OK), DB "Apophis" 발견, FadeTo 클로즈업 동작.
사용자 요청: **FadeTo 말고** 소행성으로 줌인.

★ 방법: FadeTo(페이드-순간이동) 대신 **소행성 자체 포트에 카메라를 놓고 R 을 줄이는 연속 줌**
   (토성/혜성 줌과 동일 원리 — '같은 프레임 R 애니'가 유일하게 완전 제어되는 비행).
   ① ast_port = ast.portId(Asteroid.AsteroidPort.Synchronous)  # 소행성 고정 프레임
   ② cam.setPositionLBR(Vec(0, 20, 큰R), Anim, ast_port)       # 소행성 프레임으로 진입(원거리)
   ③ p=cam.positionLBR; cam.setPositionR(p.z*배율, Anim, -1)   # ★ R 줄이며 연속 접근(페이드 없음)
   ※ R 단위 = 트랙 대상(소행성) 반지름. 절대값 금지, 읽은값×배율. track=-1 = 현 프레임 유지.

포트 2종 실험: Synchronous(자전 고정=표면 접근) / EclipticJ2000(황도). 로그의 R 로 단위 파악.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 + 슬롯 소행성 (v1 확정 세팅) ─────────────────────────
print("무대 + 아포피스 궤도요소")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(0.9, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2029, 3, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.2)

ast = Asteroid(Asteroid.AsteroidName.Asteroid001)
ast.setIntensity(1.0, Anim(0.0)); sleep(0.2)
ast.setSemiMajorAxis(0.9224, Anim(0.0))
ast.setEccentricity(0.1914, Anim(0.0))
ast.setInclination(3.339, Anim(0.0))
ast.setLongitudeOfAscendingNode(204.0, Anim(0.0))
ast.setArgumentOfPeriapsis(126.7, Anim(0.0))
ast.setMeanAnomaly(180.0, Anim(0.0))
ast.setEpoch(2459396.5, Anim(0.0))
ast.setLabelNameOverride("99942 Apophis")
sleep(0.3)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.85, 0.6))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))

# 지상 궤도 조망 (짧게)
try:
    ast.setOrbitColor(Vec(1.0, 0.5, 0.2), Anim(0.0))
except Exception:
    pass
ast.setOrbitThickness(2.0)
ast.setOrbitIntensity(0.9, Anim(2.0))
ast.setLabelIntensity(0.8, Anim(2.0))
try:
    ast.setPointerType(Body.PointerType.Model3Bold)
    ast.setPointerIntensity(1.0, Anim(1.5))
except Exception:
    pass
t1.setText("아포피스 — 이제 FadeTo 없이 다가간다"); t1.setIntensity(1.0, Anim(1.0))
print(">>> 지상 궤도 조망 (5초)")
sleep(5.0)
t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)

# ══════════════════════════════════════════════════════════════
# 줌인 (FadeTo 없이) — 소행성 포트 + R 애니
# ══════════════════════════════════════════════════════════════
def get_port(name):
    try:
        pid = ast.portId(getattr(Asteroid.AsteroidPort, name))
        print("   port %s = %s" % (name, pid))
        return pid
    except Exception as e:
        print("   port %s 실패: %s" % (name, e)); return -1

print("=" * 60); print("줌인: 소행성 포트 + R 애니 (페이드 없음)"); print("=" * 60)
ast_port = get_port("Synchronous")
if ast_port == -1:
    ast_port = get_port("EclipticJ2000")

if ast_port != -1:
    try:
        # ① 소행성 프레임으로 진입 (원거리에서) — 포인터는 정리
        ast.setPointerIntensity(0.0, Anim(0.5))
        t1.setText("소행성 프레임으로 진입"); t1.setIntensity(1.0, Anim(0.8))
        cam.setPositionLBR(Vec(0.0, 20.0, 400.0), Anim.cubic(4.0), ast_port)
        sleep(4.5)
        try:
            print("   진입 후 R=%.3f" % cam.positionLBR.z)
        except Exception:
            pass
        # ② 연속 줌인 = R 을 단계적으로 줄임 (읽은값×배율, track=-1)
        t1.setText("다가간다 — R 을 줄이며 연속 접근")
        for i, factor in enumerate([0.25, 0.35, 0.4]):
            p = cam.positionLBR
            target = p.z * factor
            cam.setPositionR(target, Anim.cubic(5.0), -1)
            print("   줌 %d: R %.3f → %.3f (×%.2f)" % (i + 1, p.z, target, factor))
            sleep(5.5)
        try:
            print("   최종 R=%.3f" % cam.positionLBR.z)
        except Exception:
            pass
        print("   ★ 페이드 없이 소행성이 점점 커졌나? 표면/형체가 보이나?")
        t1.setText("아포피스 표면 — 지름 340 m 의 돌덩이"); t1.setIntensity(1.0, Anim(0.8))
        sleep(4.0)
        t1.setIntensity(0.0, Anim(0.6)); sleep(0.6)
    except Exception as e:
        print("   줌인 실패: %s" % e)
else:
    print("   포트 확보 실패 → 줌인 스킵")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("아포피스 — 2029, 지구와의 랑데부"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①진입/줌 R 값 ②페이드 없이 연속으로 커졌나 ③표면 보이나(모델 없으면 점?)")

# -*- coding: utf-8 -*-
"""
globular_cluster_final.py — 오메가 센타우리 완성쇼 (2026-07-09, 한계 반영 최종)
전체 여정 확정:
 · ⚠️⚠️ 지상(빌보드) setScale 확대는 무효 — 확대는 FadeTo '후'(성단 중앙)에서만 보임(실측).
 · 확대/'날아듦' = FadeTo(줌인+한바퀴 스핀 내장) 로 별밭 진입 → 그 안에서 setScale 램프(원본×배율).
 · ⚠️ 성단 별밭은 R 로 확대 안 됨(고정 투영, R 20만~3 동일) → 말머리식 R-비행 불가
   (성단 포트가 Ecliptic/Galactic 뿐, 말머리의 LineOfSight 프레임이 없음).
   AdvancedCamera 비행도 스크립트 무효. → 접근 연출은 FadeTo(줌+스핀) + 내부 setScale 이 정답.
 · 내부 둘러보기는 시선(setOrientationHPR) 회전 (위치/R 무효).

구성: 지상 식별(센타우리자리+포인터) → FadeTo 별밭 진입 → 내부 둘러보기 → 피날레.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

gc_db = None
try:
    gc_db = DataManager.database().data(Data.Type.GlobularClusterType, "Omega Centauri")
except Exception as e:
    print("   DB 실패: %s" % e)

# ── ① 지상 식별 (센타우리자리 + 포인터 + setScale 확대) ─────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(-31.0, -71.0, 2400.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 5, 1, 3, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

gc = GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)
gc.setIntensity(1.0, Anim(0.0))
try:
    orig_scale = gc.scale
except Exception:
    orig_scale = 1.0

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("오메가 센타우리 — 남쪽 하늘의 뿌연 별 하나"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0)

cen = Constellation(Constellation.ConstellationName.Cen)
try:
    cen.setLinesIntensity(0.8, Anim(2.0)); cen.setLabelIntensity(0.6, Anim(2.0))
except Exception as e:
    print("   센타우리자리 실패: %s" % e)
t1.setText("센타우리자리 안 — 맨눈엔 별 하나")
sleep(4.0)
try:
    gc.setPointerType(Body.PointerType.Model2Bold)
    gc.setPointerIntensity(1.0, Anim(1.5))
except Exception:
    pass
# ── 별자리 선 켠 상태에서 그 자리 확대 (setScale) ──────────────
#   지상 확대는 약할 수 있음(먼 거리) — 진짜 확대는 FadeTo 후. scale 은 property 라 유지됨.
t1.setText("사실은 별 1천만 개의 공 — 확대해 보면")
try:
    print("   [지상확대] orig_scale=%s → %s" % (orig_scale, orig_scale * 30.0))
    gc.setScale(orig_scale * 30.0, Anim.cubic(4.0))
    sleep(4.5)
    try:
        print("   [지상확대] 후 scale=%s" % gc.scale)
    except Exception:
        pass
except Exception as e:
    print("   지상 확대 실패: %s" % e)
t1.setText("성단 속으로 들어가 보자")
sleep(2.5)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ② FadeTo → 별밭 속 진입 (개별 별로 풀림) ─────────────────
print("FadeTo → 성단 속(별밭)")
gport = -1
if gc_db is not None:
    act = gc_db.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("성단 속으로"); t1.setIntensity(1.0, Anim(0.8))
        try:
            gc.setPointerIntensity(0.0, Anim(0.5))
            cen.setLinesIntensity(0.0, Anim(1.0)); cen.setLabelIntensity(0.0, Anim(1.0))
        except Exception:
            pass
        # FadeTo = '줌인+한바퀴 스핀' 내장 → 별밭 속으로 날아드는 접근이 여기서 일어남.
        act.trigger()
        sleep(6.0)
        try:
            gport = gc.portId(GlobularCluster.GlobularClusterPort.Galactic)
            print("   FadeTo 후 R=%.3f" % cam.positionLBR.z)
        except Exception:
            pass
        t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

        # ── ②-b 확대 = FadeTo 후(성단 중앙)에서 setScale = 확정 동작 경로! ──
        #   ⚠️ 지상 빌보드 setScale 은 무효였음. 확대는 반드시 '중앙 진입 후'.
        #   ⚠️ 절대값 금지 — 원본 × 배율. ★ 한방에 쭉: 원본×700 을 단일 애니로.
        t1.setText("별들이 점점 다가온다 — 성단 심장부로"); t1.setIntensity(1.0, Anim(0.8))
        try:
            print("   [확대] orig=%s × 700 = %s (한방)" % (orig_scale, orig_scale * 700.0))
            gc.setScale(orig_scale * 700.0, Anim.cubic(14.0))
            sleep(14.5)
            try:
                print("   [확대] 후 scale=%s" % gc.scale)
            except Exception:
                pass
            print("   ★ 한방에 700배까지 별밭이 다가오며 깊이 파고들었나?")
        except Exception as e:
            print("   확대 실패: %s" % e)
        t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

# ── ③ 내부 회전 = Z축(시선축) roll = 별밭이 화면 중심축으로 팽이처럼 돎 ────
#   ⚠️ 별밭은 위치/R 에 반응 안 함(고정 투영) → 회전은 '시선(orientation)'을 돌려야 함.
#   HPR = (Heading, Pitch, Roll). H 스윕 = 좌우 팬(시계/반시계 느낌).
#   Z축 회전(팽이 스핀) = 세 번째 값 Roll 을 돌린다.
print("내부 회전 (Z축 roll 스핀)")
t1.setText("사방이 별 — 100억 년을 함께 돈 늙은 별들의 도시")
t1.setIntensity(1.0, Anim(0.8))
try:
    b = cam.orientationHPR
    bh, bp, br = b.x, b.y, b.z
except Exception:
    bh, bp, br = 0.0, 0.0, 0.0
try:
    # ★ 말머리처럼 원큐 — 360° 를 단일 애니로 한 번에 스핀.
    cam.setOrientationHPR(Vec(bh, bp, br + 360.0), Anim.cubic(16.0))
    sleep(16.5)
    print("   ★ Roll(Z축)로 별밭이 한 번에 360° 팽이 스핀했나?")
except Exception as e:
    print("   Z축 회전 실패: %s → 홀드" % e)
    sleep(6.0)
t1.setText("중심으로 갈수록 별이 촘촘 — 별들의 심장부")
sleep(3.5)
t1.setIntensity(0.0, Anim(0.8))

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("오메가 센타우리 — 우리은하가 삼킨 왜소은하의 심장?"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
try:
    gc.setScale(orig_scale, Anim(2.0))   # 확대 원복 (다음 쇼 대비)
except Exception:
    pass
sleep(4.5)
print("종료. 구상성단 완성쇼 (지상 식별 → FadeTo 별밭 진입 → 내부 둘러보기).")

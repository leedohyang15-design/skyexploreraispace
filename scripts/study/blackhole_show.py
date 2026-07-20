# -*- coding: utf-8 -*-
"""
blackhole_show.py — 블랙홀 (궁수자리 A*) v1 (2026-07-09)
새 주제: Insert3D(3D 모델 삽입) — study_blackhole.py 학습노트를 완성 쇼로.
SPC 실측 확정 경로: blackholeAccretionSharp.osg (강착원반 3D 모델).

★ 처음 시도하는 Insert3D 기능:
 · setModelFilename(경로) — .osg 3D 모델 로드 (SPC 확정 경로 사용)
 · setParent(port) — 모델을 좌표 홀더(Place2D=은하중심)에 부착
 · setOrientationHPR / setScale / setIntensity
 · ★★ getIntrospection() + introspectionOutput — 모델의 애니메이션/유니폼 노드 탐색(신규!)
 · setAnimationName / setAnimationEvolution — 강착원반 회전 애니(있으면)
 · modifyUniform — 셰이더 파라미터(색/강도 등, 있으면)

카메라: 블랙홀 위치(Place2D)의 프레임에서 조준+접근 (study_blackhole 패턴).
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e)); return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

MODEL = "..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg"

# ── 프로브 ────────────────────────────────────────────────────
print("=" * 60); print("ACT 0: Insert3D 프로브"); print("=" * 60)
probe("Insert3D 클래스", Insert3D)
if hasattr(Insert3D, "Insert3DName"):
    names = probe("Insert3D.Insert3DName", Insert3D.Insert3DName)

# ── 무대: 심우주 (은하 중심, 태양 없음) ──────────────────────
print("=" * 60); print("ACT 1: 심우주 세팅"); print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.7, Anim(0.0))
milkyway = Galaxy(Galaxy.GalaxyName.MilkyWay)
milkyway.setIntensity(0.4, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2020, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

# ── 블랙홀 위치 홀더 (은하 중심에) ──────────────────────────
print("블랙홀 위치 = 은하중심 (2.47e20 m ≈ 2.6만 광년)")
bh_place = Place2D(Place2D.Place2DName(0))
bh_place.setPosition(Vec(0.0, 0.0, 2.468542e20))
try:
    bh_place.setParent(milkyway.portId(Galaxy.GalaxyPort.EquatorialSynchronous))
    print("   은하 프레임에 부착 OK")
except Exception as e:
    print("   부착 실패: %s" % e)

# ── Insert3D 강착원반 모델 로드 ──────────────────────────────
print("=" * 60); print("ACT 2: 강착원반 3D 모델 로드"); print("=" * 60)
bh = Insert3D(Insert3D.Insert3DName(0))
print("   Insert3D#0 id=%s" % bh.id)
bh.setIntensity(1.0, Anim(0.0))
bh.setModelFilename(MODEL)
print("   setModelFilename(...blackholeAccretionSharp.osg)")
sleep(1.0)                                    # 로드 대기
try:
    print("   loadingStatus=%s modelRadius=%s" % (bh.loadingStatus, bh.modelRadius))
except Exception as e:
    print("   상태 읽기: %s" % e)
try:
    bh.setParent(bh_place.portId(Place2D.Place2DPort.EquatorialSynchronous))
except Exception as e:
    print("   setParent 실패: %s" % e)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))   # 원반을 옆에서 보이게 기울임
try:
    bh.setScale(1.0, Anim(0.0))
except Exception as e:
    print("   setScale 스킵: %s" % e)

# ── ★ introspection: 모델의 애니메이션/유니폼 노드 탐색 ──────
print("=" * 60); print("ACT 2b: 모델 introspection (애니 노드 찾기)"); print("=" * 60)
try:
    bh.getIntrospection(); sleep(0.5)
    out = bh.instrospectionOutput      # (레퍼런스 철자 그대로: instrospectionOutput)
    print("[INTROSPECT] %s" % str(out)[:800])
except Exception as e:
    print("[INTROSPECT] 실패: %s" % e)

# ── 카메라: 블랙홀 프레임서 조준 + 접근 ──────────────────────
print("=" * 60); print("ACT 3: 카메라 접근"); print("=" * 60)
bh_port = -1
try:
    bh_port = bh_place.portId(Place2D.Place2DPort.EquatorialSynchronous)
    cam.setPositionLBR(Vec(-100.0, 0.0, 5e-14), Anim(0.0), bh_port)   # 블랙홀 프레임 진입(원거리 조준)
    sleep(1.0)
    print("   블랙홀 프레임 진입 R=%s" % (cam.positionLBR.z))
except Exception as e:
    print("   프레임 진입 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("궁수자리 A* — 우리은하 중심의 초대질량 블랙홀"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# 접근 (블랙홀 프레임 안에서 위치 애니)
try:
    t1.setText("강착원반 — 빨려드는 물질이 마찰로 백만 도까지")
    cam.setPositionLBR(Vec(5.0, 5.0, 0.0), Anim.cubic(6.0), bh_port)
    sleep(6.5)
    print("   ★ 강착원반이 보이나? 접근 됐나?")
except Exception as e:
    print("   접근 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── ★ 강착원반 회전 애니 (introspection 결과 있으면) ────────
print("=" * 60); print("ACT 4: 원반 회전 애니"); print("=" * 60)
try:
    t1.setText("사건의 지평선 — 빛조차 탈출 못 하는 경계"); t1.setIntensity(1.0, Anim(0.8))
    # 전체 애니 제어(빈 문자열=모든 애니) + evolution 0→1 반복 시도
    bh.setAnimationName("")
    for cyc in range(2):
        bh.setAnimationEvolution(0.0, Anim(0.0)); sleep(0.1)
        bh.setAnimationEvolution(1.0, Anim(6.0))
        sleep(6.2)
    print("   ★ 원반이 회전했나? (애니 노드 있으면)")
except Exception as e:
    print("   애니 실패(모델에 애니 없을 수 있음): %s" % e)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.8)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①모델 로드됐나(loadingStatus/화면) ②[INTROSPECT] 출력 ③접근 됐나 ④원반 회전 애니")

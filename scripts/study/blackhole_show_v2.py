# -*- coding: utf-8 -*-
"""
blackhole_show_v2.py — 포트 수정 + 시간가속 회전 (2026-07-09)
v1 실측: ✅ 모델 로드됨(loadingStatus=Loaded, modelRadius=4,850만) ✅ introspection 동작.
        ❌ setParent/카메라 실패 = 포트 이름 오류(GalaxyPort/Place2DPort 에 EquatorialSynchronous 없음).
★ introspection 발견: 강착원반은 셰이더 유니폼 `u_simulationTime`(원점=JD)로 구동
  → **시간가속(setDateTime)하면 원반이 회전**. setAnimationEvolution 불필요.

이번 v2:
 ① GalaxyPort / Place2DPort 를 프로브해서 '유효한 포트'로 부착·카메라.
 ② 시간가속으로 강착원반 회전.
 ③ modifyUniform 로 발광 강도(u_emissiveIntensity) 조절 시도(introspection 에서 확인된 유니폼).
"""

from skyExplorer import *
from studio import *
from Initialization import *


def first_valid_port(port_enum, prefer=("Equatorial", "Ecliptic", "Galactic")):
    """포트 enum 에서 유효 멤버 하나 선택(선호 이름 우선)."""
    ms = [m for m in dir(port_enum) if not m.startswith("_")
          and m not in ("name", "names", "values") and "Invalid" not in m]
    print("   [PORT] 후보: %s" % ms)
    for pref in prefer:
        for m in ms:
            if pref.lower() in m.lower():
                return m
    return ms[0] if ms else None


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
MODEL = "..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg"

# ── 포트 프로브 ───────────────────────────────────────────────
print("=" * 60); print("ACT 0: 포트 프로브"); print("=" * 60)
print("GalaxyPort:")
gport_name = first_valid_port(Galaxy.GalaxyPort)
print("PlaceDPort:")
pport_name = first_valid_port(Place2D.Place2DPort)
print("   선택 → Galaxy:%s / Place2D:%s" % (gport_name, pport_name))

# ── 무대: 심우주 ─────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))
milkyway = Galaxy(Galaxy.GalaxyName.MilkyWay)
milkyway.setIntensity(0.4, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2020, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

# ── 블랙홀 위치 홀더 + 모델 ──────────────────────────────────
bh_place = Place2D(Place2D.Place2DName(0))
bh_place.setPosition(Vec(0.0, 0.0, 2.468542e20))            # 은하중심 거리
try:
    bh_place.setParent(milkyway.portId(getattr(Galaxy.GalaxyPort, gport_name)))
    print("   Place2D→Galaxy(%s) 부착 OK" % gport_name)
except Exception as e:
    print("   Galaxy 부착 실패: %s" % e)

bh = Insert3D(Insert3D.Insert3DName(0))
bh.setIntensity(1.0, Anim(0.0))
bh.setModelFilename(MODEL)
sleep(1.0)
print("   loadingStatus=%s modelRadius=%s" % (bh.loadingStatus, bh.modelRadius))
pport = -1
try:
    pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
    bh.setParent(pport)
    print("   Insert3D→Place2D(%s) 부착 OK (portId=%s)" % (pport_name, pport))
except Exception as e:
    print("   Place2D 부착 실패: %s" % e)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))
try:
    bh.setScale(1.0, Anim(0.0))
except Exception:
    pass

# ── 카메라: 블랙홀 프레임 진입 ───────────────────────────────
print("=" * 60); print("ACT 1: 카메라 진입"); print("=" * 60)
if pport != -1:
    try:
        # 홀더 프레임에서 블랙홀을 바라봄. R 은 modelRadius 근처 스케일로.
        cam.setPositionLBR(Vec(0.0, 10.0, bh.modelRadius * 6.0), Anim(0.0), pport)
        sleep(1.0)
        print("   진입 R=%.3e" % cam.positionLBR.z)
    except Exception as e:
        print("   진입 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("궁수자리 A* — 우리은하 중심의 초대질량 블랙홀"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# 접근 (블랙홀 프레임서 R 줄이기)
if pport != -1:
    try:
        t1.setText("강착원반 — 백만 도로 달궈진 물질의 소용돌이")
        for factor in (0.4, 0.4, 0.5):
            p = cam.positionLBR
            cam.setPositionR(p.z * factor, Anim(1.5), -1)
            sleep(1.6)
        print("   접근 후 R=%.3e" % cam.positionLBR.z)
    except Exception as e:
        print("   접근 실패: %s" % e)
sleep(1.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.6)

# ── ★ 시간가속으로 강착원반 회전 (u_simulationTime 구동) ─────
print("=" * 60); print("ACT 2: 시간가속 = 원반 회전"); print("=" * 60)
try:
    t1.setText("사건의 지평선 — 빛조차 탈출 못 하는 경계"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2020, 1, 2, 0, 0, 0, tz, Anim(15.0))     # 하루를 15초에 (원반 도는지)
    sleep(15.5)
    print("   ★ 원반이 회전했나? (u_simulationTime 구동)")
    t1.setIntensity(0.0, Anim(0.8)); sleep(0.6)
except Exception as e:
    print("   시간가속 실패: %s" % e)

# ── modifyUniform: 발광 강도 펄스 (introspection 유니폼) ─────
print("=" * 60); print("ACT 3: modifyUniform 발광"); print("=" * 60)
try:
    t1.setText("빛나는 죽음의 소용돌이"); t1.setIntensity(1.0, Anim(0.8))
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(3.0, 0.0, 0.0, 0.0), Anim(3.0))
    sleep(3.5)
    print("   ★ 원반이 더 밝아졌나?")
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(1.0, 0.0, 0.0, 0.0), Anim(2.0))
    sleep(2.5)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   modifyUniform 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("블랙홀 — 시공간이 무너지는 곳"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①[PORT] 유효포트 ②부착 OK? ③화면에 원반 보이나 ④시간가속 회전 ⑤발광 변화")

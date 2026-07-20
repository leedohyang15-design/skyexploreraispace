# -*- coding: utf-8 -*-
"""
blackhole_show_v3.py — 카메라를 원반 '중심'에 (2026-07-09)
v2 실측: 부착 OK(Galaxy Galactic / Place2D CenteredPort), 카메라 진입 OK — 그래도 안 보임.
원인 확정: **카메라를 모델에서 너무 멀리** 놓음(R=2.9억, 모델반지름 4,850만의 6배).
          원본 study_blackhole SPC 는 **R=5e-14 (≈0) = 원반 한가운데**.
          → 이 블랙홀 모델은 '바깥 조망'이 아니라 **중심에 앉아 둘러보는** 구도(거대 원반이 카메라를 감쌈).

이번 v3: 원본 SPC 패턴 그대로 — 카메라 R≈0, 중심에서 방향만 바꿔 둘러봄.
 + introspection 발견 활용: 시간가속(u_simulationTime) 회전 / modifyUniform 발광.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def first_valid_port(port_enum, prefer=("Galactic", "Centered", "Equatorial", "Ecliptic")):
    ms = [m for m in dir(port_enum) if not m.startswith("_")
          and m not in ("name", "names", "values") and "Invalid" not in m
          and not m[0].islower()]     # 유효 포트는 대문자 시작
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

gport_name = first_valid_port(Galaxy.GalaxyPort)
pport_name = first_valid_port(Place2D.Place2DPort, prefer=("Centered", "Galactic", "Equatorial"))
print("포트: Galaxy=%s / Place2D=%s" % (gport_name, pport_name))

# ── 무대 ──────────────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
milkyway = Galaxy(Galaxy.GalaxyName.MilkyWay)
milkyway.setIntensity(0.3, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2020, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

# ── 위치 홀더 + 모델 ─────────────────────────────────────────
bh_place = Place2D(Place2D.Place2DName(0))
bh_place.setPosition(Vec(0.0, 0.0, 2.468542e20))
try:
    bh_place.setParent(milkyway.portId(getattr(Galaxy.GalaxyPort, gport_name)))
except Exception as e:
    print("   Galaxy 부착 실패: %s" % e)

bh = Insert3D(Insert3D.Insert3DName(0))
bh.setIntensity(1.0, Anim(0.0))
bh.setModelFilename(MODEL)
sleep(1.0)
print("   loadingStatus=%s modelRadius=%.0f" % (bh.loadingStatus, bh.modelRadius))
pport = -1
try:
    pport = bh_place.portId(getattr(Place2D.Place2DPort, pport_name))
    bh.setParent(pport)
    print("   Insert3D 부착 OK portId=%s" % pport)
except Exception as e:
    print("   부착 실패: %s" % e)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))   # 원반 옆으로 세움
try:
    bh.setScale(1.0, Anim(0.0))
except Exception:
    pass

# ── ★ 카메라를 원반 '중심'에 (R≈0, 원본 SPC 패턴) ───────────
print("=" * 60); print("카메라를 원반 중심에 (R≈0)"); print("=" * 60)
if pport != -1:
    try:
        cam.setPositionLBR(Vec(-100.0, 0.0, 5e-14), Anim(0.0), pport)   # 중심, L=-100 응시
        sleep(1.0)
        print("   진입 R=%.3e" % cam.positionLBR.z)
    except Exception as e:
        print("   진입 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(1.0, 0.6, 0.3))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("궁수자리 A* — 강착원반 한가운데"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# 중심에서 방향만 바꿔 둘러보기 (원본: Vec(5,5,0) 로 이동)
if pport != -1:
    try:
        t1.setText("사방을 둘러싼 백만 도의 소용돌이")
        cam.setPositionLBR(Vec(5.0, 5.0, 0.0), Anim.cubic(6.0), pport)
        sleep(6.5)
        print("   ★ 원반이 보이나? (중심 시점)")
    except Exception as e:
        print("   둘러보기 실패: %s" % e)
t1.setIntensity(0.0, Anim(0.8)); sleep(0.6)

# ── 시간가속 = 원반 회전 ─────────────────────────────────────
print("시간가속 회전")
try:
    t1.setText("사건의 지평선 — 빛도 탈출 못 하는 경계"); t1.setIntensity(1.0, Anim(0.8))
    dm.setDateTime(2020, 1, 1, 12, 0, 0, tz, Anim(12.0))   # 12시간을 12초에
    sleep(12.5)
    print("   ★ 원반 회전했나?")
    t1.setIntensity(0.0, Anim(0.8)); sleep(0.6)
except Exception as e:
    print("   시간가속 실패: %s" % e)

# ── modifyUniform 발광 ───────────────────────────────────────
try:
    t1.setText("빛나는 죽음의 소용돌이"); t1.setIntensity(1.0, Anim(0.8))
    bh.modifyUniform("root/u_emissiveIntensity", Vec4(3.0, 0.0, 0.0, 0.0), Anim(3.0))
    sleep(3.5)
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
print("종료. 리포트: 이번엔 원반이 보이나(중심 R≈0 시점)? / 회전 / 발광")

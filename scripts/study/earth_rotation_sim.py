# -*- coding: utf-8 -*-
"""
earth_rotation_sim.py — 지구 자전 시뮬레이션 (2026-07-14 v4 완성)
★ 확정된 사실(실측):
  · GoTo 지구 = 홈(지표면 R=0) → 밖 안 나감. **reset + FadeTo = 지구 외부(R=4, 북극 위 B=90)**. ✅
  · FadeTo 프레임 자체가 자전을 보여줌(관성 프레임 전환 불필요 — 그게 오히려 '화면 빠짐' 유발). ✅
  · 자전 속도 = **setRotationSpeedScale(배율) × 날짜Δ** 이중이라 배율40+큰점프 = 너무 빠름.
    → 배율 6 + 날짜 +6h(0.25일) = 약 1.5바퀴/22초 (보기 좋은 속도).
미연습 코드: setRotationSpeedScale/reset, 자전축(setEquatorialPoleAxisIntensity/PolePointer),
  setNightLightsIntensity, setCloudsIntensity.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
earth = Planet(PN.Earth)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] pos 실패: %s" % (tag, e))


# ── 무대(지상) & 인트로 ─────────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.35, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.92, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("지구 자전 시뮬레이션 — 밖에서 보는 푸른 행성"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.0); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); sleep(dur)


# ── 지구를 '외부에서': reset + FadeTo ────────────────────────
narr("지구를 우주에서 바라본다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
SceneGraph().reset(1); sleep(1.5)                                 # 관측자 바인딩 해제
h = DataManager.database().data(Data.Type.PlanetType, "Earth")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Earth")
else:
    print("   ⚠️ FadeTo Earth 미지원")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
rlog("FadeTo 후")
# ★★ 핵심: 동기(Sync) 프레임 → 관성 프레임(EquatorialJ2000) 전환.
#    Sync = 카메라가 지구 표면 한 점에 붙어 같이 돎 → 지구 멈추고 하늘이 돎(실측 확인).
#    관성 = 카메라가 별에 고정 → 지구가 그 자리서 자전, 별 고정.
#    (카메라 위치는 그대로 = 이동 없음. R 보존 실측됨.)
INERTIAL = -1
for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
    try:
        ip = earth.portId(getattr(Planet.PlanetPort, pn))
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim.cubic(1.5), ip); sleep(1.8)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim.cubic(2.0), ip); sleep(2.2)
        INERTIAL = ip
        print("   ★ 관성 프레임=%s (R=%.3g)" % (pn, cam.positionLBR.z))
        break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))
# ★ 북극 위(B90)면 자전축을 정면으로 봄(팽이) → 적도 옆(B5)으로 옮겨 자전축이 '세로' = 옆으로 도는 지구본
#   + R 을 줄여 지구를 더 크게(도시광·구름 잘 보이게)
if INERTIAL != -1:
    try:
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, 5.0, p.z * 0.55), Anim.cubic(4.0), INERTIAL); sleep(4.3)
        print("   적도 뷰 + 확대 (B→5, R×0.55)")
    except Exception as e:
        print("   적도 이동 실패: %s" % e)
cam.setTargetHeight(75.0, Anim.cubic(1.5)); sleep(1.6)             # 지구를 돔 중앙 쪽으로 올림
rlog("관성 전환 후")
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
# ⚠️ 날짜 baseline 강제 리셋 제거 — 인트로 날짜(2026-08-01 12:00) 유지(그림자 갑자기 쓸림 방지)

# ── 지구 외형 + 자전축(미연습) ──────────────────────────────
narr("푸른 대기와 바다, 흰 구름", 1.0)
for fn, val in (("setAtmosphereIntensity", 1.0), ("setTerrainIntensity", 1.0), ("setCloudsIntensity", 1.0)):
    try:
        getattr(earth, fn)(val, Anim(2.5)); print("   %s(%.1f)" % (fn, val))
    except Exception as e:
        print("   %s 실패: %s" % (fn, e))
sleep(3.0)
narr("자전축 — 23.4° 기울기", 1.0)
for fn in ("setEquatorialPoleAxisIntensity", "setEquatorialPolePointerIntensity"):
    try:
        getattr(earth, fn)(1.0, Anim(2.0)); print("   %s(1.0)" % fn)
    except Exception as e:
        print("   %s 실패: %s" % (fn, e))
sleep(3.0)


def spin_to(y, mo, d, hh, mm, dur, scale=2.0):
    """자전 = 관성 프레임에서 **날짜를 흘림**. 관성 프레임은 별에 고정이라 시간이 흘러도
    별은 그대로, 지구만 자전축으로 돎. 회전량 = 배율 × 날짜Δ(일).
    배율 2 × +12h(0.5일) = 1바퀴. (배율은 setRotationSpeedScale 미연습 코드 시연 겸.)"""
    dm.stop(); sleep(0.5)                                        # ★ 시간 먼저 완전정지(막 회전 방지)
    try:
        earth.setRotationSpeedScale(scale); print("   setRotationSpeedScale(%.0f)" % scale)
    except Exception as e:
        print("   scale 실패: %s" % e)
    sleep(0.4)                                                   # 배율 안정 후 시작
    try:
        j0 = dm.julianDate
    except Exception:
        j0 = 0.0
    dm.setDateTime(y, mo, d, hh, mm, 0, tz, Anim(dur)); sleep(dur + 0.8)
    try:
        print("   자전 JD Δ=%.4f일 (배율 %.0f → 약 %.1f바퀴)" % (dm.julianDate - j0, scale, (dm.julianDate - j0) * scale))
    except Exception:
        pass


# ── ★ 자전 (느린 속도) ──────────────────────────────────────
narr("밤이 된 면 — 도시의 불빛", 1.0)                            # 자전 전에 도시광 켜둠(밤면에 나타나게)
try:
    earth.setNightLightsIntensity(1.0, Anim(2.0)); print("   setNightLightsIntensity(1.0)")
except Exception as e:
    print("   nightLights 실패: %s" % e)
sleep(2.0)
narr("지구를 그 자리서 자전시킨다 — 별은 그대로", 1.0)
narr("낮과 밤이 지나간다", 0.5)
spin_to(2026, 8, 2, 0, 0, 24.0, scale=2.0)                       # 12:00→+12h ×2 = 1바퀴 (관성=별 고정)
spin_to(2026, 8, 2, 12, 0, 22.0, scale=2.0)                      # +12h 더 = 1바퀴

# ── 정리 ────────────────────────────────────────────────────
narr("자전 속도를 원래대로", 1.0)
try:
    earth.resetRotationSpeedScale(); print("   resetRotationSpeedScale()")
except Exception as e:
    print("   reset 실패: %s" % e)
dm.stop()
try:
    earth.setEquatorialPoleAxisIntensity(0.0, Anim(1.5))
    earth.setEquatorialPolePointerIntensity(0.0, Anim(1.5))
except Exception:
    pass
sleep(2.0)
t1.setText("하루에 한 바퀴 — 우리는 이 위에 서 있다"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.5); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①자전 속도 적당한가(배율6=약1.5바퀴/22초, 로그 '약 N바퀴' 확인) "
      "②중간에 화면 빠짐 없나(프레임 전환 제거함) ③자전축/구름/도시광 보이나 ④더 느리게/빠르게?")

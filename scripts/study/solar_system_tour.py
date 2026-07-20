# -*- coding: utf-8 -*-
"""
solar_system_tour.py — 태양계 그랜드 투어 (2026-07-13 v7)
★ v7 반영(사용자 요청):
  ① 행성간 직접 비행: 첫 홉만 지구 출발, 목성→토성→화성은 리셋 없이 이어 비행.
     (wait_arrival 버그 수정 후라 도킹 기대. 실패=R≥100 이면 자동으로 지상 폴백해 재비행 → 안 끊김.)
     ⚠️ 행성 프레임에선 DataManager.data() 가 None → **핸들은 시작 때 지상에서 선확보**.
  ② 행성 한 바퀴: 도킹 후 L +360° 공전(그 자리서 한 바퀴) → 그 다음 이동.
  ③ 갈릴레이 위성 확대: setScale(원본×배율) — 너무 작아서 안 보이던 것 키움.
  ④ 궤도선 먼저: 출발 직전(비행 중) 켬 — 도착 후가 아니라.
★ 골격(검증됨): wait_arrival 은 R<100 도킹 스케일 안정까지 대기(중간멈춤 오판·GoTo 락 끊김 방지).
  그림자 off = setShadowContrast/Strength(0)+setPlanetShineStrength(1).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName


def kill_shadow(p):
    for fn, val in (("setShadowContrast", 0.0), ("setShadowStrength", 0.0),
                    ("setPlanetShineStrength", 1.0)):
        try:
            getattr(p, fn)(val, Anim(0.0))
        except Exception:
            pass


def orbit_lines_on():
    for i in range(8):
        try:
            Planet(PN(i)).setOrbitIntensity(0.55, Anim(2.0))
        except Exception:
            pass


def reset_ground():
    uni.setGlobalIntensity(0.0, Anim(0.0))
    SceneGraph().reset(1); sleep(2.0)
    uni.setGlobalIntensity(0.0, Anim(0.0))
    for i in range(8):
        try:
            pl = Planet(PN(i)); pl.setIntensity(1.0, Anim(0.0)); kill_shadow(pl)
        except Exception:
            pass
    for fn in ("setAtmosphereIntensity", "setAtmosphereHaloIntensity",
               "setScatteringIntensity", "setTerrainIntensity"):   # ★ 파란 하늘+밝은 지표면 전부 끔
        try:
            getattr(Planet(PN.Earth), fn)(0.0, Anim(0.0))
        except Exception:
            pass
    IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.35, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.5)); sleep(1.0)   # 낮이어도 대기/지형 off 라 깨끗
    cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))


# ── 무대 & 핸들 선확보(지상) ─────────────────────────────────
reset_ground()
PRE = {}                                              # 행성 프레임에선 data()=None → 지상서 선확보
for nm in ("Jupiter", "Saturn", "Mars"):
    try:
        PRE[nm] = DataManager.database().data(Data.Type.PlanetType, nm)
    except Exception:
        PRE[nm] = None
    print("   핸들 선확보 %s=%s" % (nm, PRE[nm] is not None))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.95, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("태양계 그랜드 투어 — 우주선 여행"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.5)
t1.setText("지구를 떠나, 행성에서 행성으로"); sleep(3.5)
t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def wait_arrival(maxs=50, docked_R=100.0):
    """R 이 도킹 스케일(<100)로 떨어져 안정될 때까지 도착으로 안 침(GoTo 락 안 끊음)."""
    prev = None; r = 0.0
    for k in range(maxs):
        sleep(1.0)
        try:
            r = cam.positionLBR.z
        except Exception:
            continue
        if k % 3 == 0:
            print("   ...비행중 R=%.4g" % r)
        if 0 < r < docked_R and prev is not None and 0 < prev < docked_R:
            if abs(r - prev) / prev < 0.01:
                print("   도킹 완료 R=%.4f" % r); return r
        prev = r
    print("   ⚠️ 타임아웃 R=%.4g" % r)
    return r


def _dock_finish(nm, R):
    cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.2)
    try:
        kill_shadow(Planet(getattr(PN, nm)))
    except Exception:
        pass
    print("   도킹 R=%.4f" % R)                            # ★ 카메라 조정 없음(화성은 시간가속 자전으로 돎)


def goto_planet(nm, chapter, inter=False):
    """inter=False: 지상 출발(암전 리셋). inter=True: 현 행성 프레임에서 바로 다음 행성으로 비행.
    ④ 궤도선은 GoTo 트리거 직전(비행 중 보이게) 켬."""
    print("=" * 55); print("%s (%s, inter=%s)" % (nm, chapter, inter))
    if not inter:
        t1.setText("지구에서 출발"); t1.setIntensity(1.0, Anim(0.8)); sleep(1.2)
        uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
        reset_ground()
        h = DataManager.database().data(Data.Type.PlanetType, nm)   # 지상서 재조회
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
    else:
        h = PRE.get(nm)                                             # 선확보 핸들(프레임 무관)
    ga = h.action(Action.Type.GoTo) if h is not None else None
    if ga is None:
        print("   GoTo 미지원 → 스킵"); return False
    orbit_lines_on()                                               # ④ 비행 전에 궤도선 ON
    try:
        Planet(PN.Earth).setTerrainIntensity(1.0, Anim(2.0))       # ★ 떠날 때 지구 globe 는 지표면 ON(푸른 지구)
    except Exception:
        pass
    t1.setText(chapter); t1.setIntensity(1.0, Anim(1.0))
    ga.trigger()
    R = wait_arrival()
    if R >= 100.0 and inter:                                        # 행성간 도킹 실패 → 지상 폴백
        print("   ⚠️ 행성간 도킹 실패 → 지상 폴백 재비행")
        uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
        reset_ground()
        h2 = DataManager.database().data(Data.Type.PlanetType, nm)
        ga2 = h2.action(Action.Type.GoTo) if h2 is not None else None
        orbit_lines_on()
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5))
        if ga2 is not None:
            ga2.trigger(); R = wait_arrival()
    if R >= 100.0:
        print("   ⚠️ 도킹 실패 → 챕터 스킵"); return False
    _dock_finish(nm, R)
    return True


def zoom_to(ratio, steps=1):
    try:
        r = cam.positionLBR.z
        per = ratio ** (1.0 / steps)
        for j in range(steps):
            r *= per
            cam.setPositionR(r, Anim.cubic(3.2), -1)
            sleep(3.6 if j == steps - 1 else 2.0)
        print("   zoom R=%.4f (×%.2f)" % (cam.positionLBR.z, ratio))
    except Exception as e:
        print("   zoom 실패: %s" % e)


def _angdiff(a, b):
    return abs(((a - b + 180.0) % 360.0) - 180.0)


def orbit_once(label="", dur=15.0, steps=8):
    """도킹 프레임에서 행성 둘레 한 바퀴 = **L(경도) 스윕**(수직 Y축 중심, +X 방향).
    목성/토성/화성 전부 동일 코드 — 카메라가 행성 옆을 돌며 중앙 고정으로 모든 면을 봄.
    (특별 처리·재조준 없음. 화성도 B=20 도킹이면 그대로 J/S 와 똑같이 돎 — 로그의 시작 B 로 확인.)"""
    try:
        p = cam.positionLBR
        L0, B0, R = p.x, p.y, p.z
        print("   [orbit %s] 시작 L=%.2f B=%.2f R=%.4f" % (label, L0, B0, R))
        if abs(B0) > 45.0:
            print("   [orbit %s] ⚠️ B=%.1f 극점 도킹 — L 스윕이 제자리 스핀일 수 있음" % (label, B0))
        per = max(dur / steps, 1.5)
        for i in range(1, steps + 1):
            cam.setPositionLBR(Vec(L0 + 360.0 * i / steps, B0, R), Anim(per), -1); sleep(per)
        print("   [orbit %s] L 한 바퀴 완료 (끝 L=%.2f)" % (label, cam.positionLBR.x))
    except Exception as e:
        print("   orbit %s 실패: %s" % (label, e))


def rotate_planet_inertial(label, y2, mo2, d2, hh2, scale=2.0, dur=22.0):
    """★ 지구 자전 시뮬(earth_rotation_sim) 확정 방식을 화성에 적용:
    Sync 프레임(카메라가 행성 자전 따라감=행성 멈춰 보임) → **관성 프레임(EquatorialJ2000) 전환**
    → 적도 옆(B5, 자전축 세로)로 → **setRotationSpeedScale + 날짜 흐름 = 행성이 그 자리서 자전(별 고정)**.
    화성=북극 도킹이라 카메라로 도는 건 불가 → 이 방식이 정답."""
    print("   [rotate %s] 관성 프레임 전환" % label)
    INERTIAL = -1
    for pn in ("EquatorialJ2000", "Equatorial", "Ecliptic"):
        try:
            ip = Planet(getattr(PN, label)).portId(getattr(Planet.PlanetPort, pn))
            p = cam.positionLBR
            cam.setPositionLBR(Vec(p.x, p.y, p.z), Anim.cubic(1.5), ip); sleep(1.8)
            cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim.cubic(2.0), ip); sleep(2.2)
            INERTIAL = ip; print("   [rotate %s] 관성=%s (R=%.3g)" % (label, pn, cam.positionLBR.z)); break
        except Exception as e:
            print("   [rotate %s] %s 실패: %s" % (label, pn, e))
    if INERTIAL != -1:                                    # 적도 옆(자전축 세로) + 확대
        try:
            p = cam.positionLBR
            cam.setPositionLBR(Vec(p.x, 5.0, p.z * 0.6), Anim.cubic(4.0), INERTIAL); sleep(4.3)
        except Exception as e:
            print("   [rotate %s] 적도이동 실패: %s" % (label, e))
    cam.setTargetHeight(75.0, Anim.cubic(1.5)); sleep(1.6)
    try:
        Planet(getattr(PN, label)).setRotationSpeedScale(scale); print("   setRotationSpeedScale(%.0f)" % scale)
    except Exception as e:
        print("   scale 실패: %s" % e)
    dm.stop(); sleep(0.4)
    try:
        j0 = dm.julianDate
    except Exception:
        j0 = 0.0
    dm.setDateTime(y2, mo2, d2, hh2, 0, 0, tz, Anim(dur)); sleep(dur + 0.8)
    try:
        print("   [rotate %s] 자전 JD Δ=%.4f일" % (label, dm.julianDate - j0))
    except Exception:
        pass
    try:
        Planet(getattr(PN, label)).resetRotationSpeedScale()
    except Exception:
        pass
    dm.stop()


def narr(text, dur=3.5):
    t1.setText(text); sleep(dur)


# ── ① 목성 (지구 출발) ──────────────────────────────────────
if goto_planet("Jupiter", "제1행성 — 목성, 가스 거인", inter=False):
    narr("태양계에서 가장 큰 행성 — 지구 1300개가 들어간다", 3.5)
    narr("소용돌이 구름 띠 — 300년을 부는 폭풍, 대적점", 0.5)
    try:
        Planet(PN.Jupiter).setCloudsIntensity(1.0, Anim(3.0))
    except Exception:
        pass
    sleep(3.5)
    t1.setText("갈릴레이 위성 넷 — 궤도선과 함께, 크게")
    on = []
    for mn in ("Io", "Europa", "Ganymede", "Callisto"):            # ③ 위성 확대 + 궤도선
        try:
            sat = Satellite(getattr(Satellite.SatelliteName, mn))
            sat.setIntensity(1.0, Anim(1.0))
            try:
                o = sat.scale
            except Exception:
                o = 1.0
            sat.setScale(o * 12.0, Anim(2.0))                      # ×12 (더 키움)
            kill_shadow(sat)                                      # ★ 위성 그림자 off(잘 보이게)
            try:
                sat.setOrbitIntensity(0.6, Anim(2.0))             # 위성 궤도선
            except Exception:
                pass
            on.append(mn)
        except Exception:
            pass
    print("   위성 확대+궤도선 ON: %s" % (on or "없음"))
    sleep(3.5)
    zoom_to(0.7)
    narr("목성 주위를 한 바퀴 돈다", 0.5)
    orbit_once("Jupiter", 15.0)                                    # ② 한 바퀴
    t1.setIntensity(0.0, Anim(1.0)); sleep(0.5)

# ── ② 토성 (목성→토성 직접 비행!) ───────────────────────────
if goto_planet("Saturn", "제2행성 — 토성으로, 행성간 비행", inter=True):
    for cand in ("Realistic", "Detailed", "Default", "Standard"):
        try:
            Planet(PN.Saturn).setRingModel(getattr(Planet.RingModel, cand))
            print("   RingModel=%s" % cand); break
        except Exception:
            pass
    narr("수천 개의 얼음과 바위 띠 — 폭 28만km, 두께는 겨우 10m", 4.0)
    zoom_to(0.7)
    narr("고리를 따라 한 바퀴 돈다", 0.5)
    orbit_once("Saturn", 15.0)
    t1.setIntensity(0.0, Anim(1.0)); sleep(0.5)

# ── ③ 화성 (★ 지구 자전 방식 = 관성 프레임 + 자전. 화성은 북극 도킹이라 카메라 공전 불가) ──
if goto_planet("Mars", "제3행성 — 화성, 붉은 행성", inter=False):
    narr("산화철로 붉게 물든 사막의 세계", 3.0)
    t1.setText("지형을 과장해 본다 — 올림푸스 화산과 협곡")
    try:
        Planet(PN.Mars).setElevationScale(8.0, Anim(4.0)); sleep(3.5)   # 지형 과장(도킹 상태)
        print("   setElevationScale(8)")
    except Exception:
        pass
    narr("올림푸스 — 태양계에서 가장 높은 화산", 3.0)
    narr("화성을 그 자리서 자전시킨다 — 별은 그대로", 1.0)
    # ★ 관성 프레임 전환 + 자전(카메라 이동으로 도는 게 아니라 화성 자체가 돎). 화성 자전주기 24.6h≈1일.
    rotate_planet_inertial("Mars", 2026, 8, 2, 1, scale=2.0, dur=22.0)   # 13:00→+12h ×2 = 1바퀴
    t1.setIntensity(0.0, Anim(1.0)); sleep(0.5)

# ── 피날레 (지상 복귀) ───────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
reset_ground()
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("여덟 행성, 하나의 태양 — 우리 태양계"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.5)
t1.setText("우리는 다시, 이 작은 지구로 돌아왔다"); sleep(4.5)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①목성→토성→화성 '행성간 직접 비행'이 이어졌나(폴백 로그 떴나) "
      "②각 행성 한 바퀴 도는 게 자연스럽나(어지럽나) ③갈릴레이 위성 커져 보이나 "
      "④궤도선이 비행 중 미리 보이나 ⑤화성 지형 크게/그림자 없이 보이나")

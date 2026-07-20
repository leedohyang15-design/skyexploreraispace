# -*- coding: utf-8 -*-
"""
earth_moon_size_closeup.py — 지구 크게 → 달 크게 (따로따로 클로즈업) (2026-07-15)
★ 목표 = '크기'. 각 천체를 돔 가득 채워 크게 본다. (그림자/궤도/일식 없음 — 순수 크기)
★ 방법 = FadeTo/take off 말고 '완전 수동' (docs/05_face_earth.md 확정):
    smoothReset(False) → cam.setPositionLBR(Vec(L, B, R), Anim, 천체.portId(포트))
    ✅ R 단위 = 천체 반지름, 작을수록 크게 (R≈2 → 돔 가득). FadeTo 바인딩 없어 R 자유.
    ✅ B=90 + target height≈110~120 = 돔 중앙 정렬(docs/05 실측).
  달이 지구 60배 거리라 '둘 다 한 화면에 크게'는 불가 → 지구 클로즈업 후 달 클로즈업으로 분리.
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
moon = Satellite(Satellite.SatelliteName.Moon)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:20] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def port(obj, *names):
    """여러 포트 후보 중 처음 되는 것의 portId 반환 (클래스마다 포트 이름 다름)."""
    cls = type(obj)
    for grp in ("PlanetPort", "SatellitePort"):
        if hasattr(cls, grp):
            enum = getattr(cls, grp)
            for nm in names:
                if hasattr(enum, nm):
                    try:
                        pid = obj.portId(getattr(enum, nm))
                        print("   포트=%s.%s" % (grp, nm)); return pid
                    except Exception:
                        pass
    print("   ⚠️ 포트 못 찾음 → -1"); return -1


# ── 무대: 우주 배경 ─────────────────────────────────────────
print("무대 준비")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    smoothReset(False); sleep(1.8); print("   smoothReset(False)")
except Exception as e:
    print("   smoothReset 실패(%s) → SceneGraph reset" % e); SceneGraph().reset(1); sleep(1.8)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
sun.setIntensity(1.0, Anim(0.0))
moon.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.6, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.25, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.85, 0.92, 1.0))


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ══════════════════════════════════════════════════════════
# PART 1 — 지구 클로즈업 (돔 가득 크게)
# ══════════════════════════════════════════════════════════
EARTH_R = 2.2      # 지구반지름. 작을수록 큼. 2.2 ≈ 돔에 크게. (1.5=더 큼, 3=좀 작게)
ep = port(earth, "EquatorialSynchronous", "Equatorial", "Ecliptic")
try:
    cam.setTarget(Vec2(0.0, 115.0), Anim(0.0))                  # 중앙 정렬(B90 기준 height≈115)
    cam.setPositionLBR(Vec(10.0, 90.0, EARTH_R), Anim.cubic(3.0), ep); sleep(3.3)
    rlog("지구 클로즈업 배치")
except Exception as e:
    print("   지구 배치 실패: %s" % e)
# 지구 외형(크게 보이니 디테일 켬)
for fn, val in (("setAtmosphereIntensity", 1.0), ("setTerrainIntensity", 1.0),
                ("setCloudsIntensity", 1.0), ("setNightLightsIntensity", 1.0)):
    feat(earth, fn, val, Anim(1.5))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
narr("지구 — 돔 가득 크게", 4.0)
narr("R 값 하나로 크기를 정한다 (작을수록 크게)", 3.5)
# 크기 조절 시연: 더 크게 → 원래대로 (R 로만 크기 바뀜을 보여줌)
narr("더 크게 (R 2.2 → 1.5)", 1.0)
try:
    cam.setPositionLBR(Vec(10.0, 90.0, 1.5), Anim.cubic(4.0), ep); sleep(4.3); rlog("R=1.5")
except Exception as e:
    print("   확대 실패: %s" % e)
narr("다시 원래 크기 (R 1.5 → 2.5)", 1.0)
try:
    cam.setPositionLBR(Vec(10.0, 90.0, 2.5), Anim.cubic(4.0), ep); sleep(4.3); rlog("R=2.5")
except Exception as e:
    print("   축소 실패: %s" % e)
narr("이게 지구다", 3.0)

# ── 전환 (암전) ─────────────────────────────────────────────
t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(2.5)); sleep(2.8)

# ══════════════════════════════════════════════════════════
# PART 2 — 달 클로즈업 (돔 가득 크게)
# ══════════════════════════════════════════════════════════
MOON_R = 2.4       # 달반지름 단위. 작을수록 큼.
mp = port(moon, "EquatorialSynchronous", "Equatorial", "NoonEcliptic")
try:
    cam.setTarget(Vec2(0.0, 115.0), Anim(0.0))
    cam.setPositionLBR(Vec(0.0, 90.0, MOON_R), Anim.cubic(3.0), mp); sleep(3.3)
    rlog("달 클로즈업 배치")
except Exception as e:
    print("   달 배치 실패: %s" % e)
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
narr("달 — 같은 방법으로 돔 가득 크게", 4.0)
# 위상(명암) 연출 — 보너스: 수동 위상으로 신월→보름 스윕
if feat(moon, "setManualMoonPhase", True, label="(수동 위상)"):
    feat(moon, "setPlanetShineStrength", 0.2, Anim(1.0), label="(그늘면 어둡게)")
    narr("빛과 그림자 — 위상이 지나간다", 1.0)
    feat(moon, "setMoonAge", 0.0, Anim(0.0))
    feat(moon, "setMoonAge", 29.5, Anim(14.0), label="(신월→보름→그믐)"); sleep(15.0)
narr("이게 달이다 — 지구에서 지구 60개 거리 저편", 3.5)

# ── 정리 ────────────────────────────────────────────────────
t1.setText("지구 그리고 달 — 각각 크게"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.0); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①지구 클로즈업 크게 나오나(R=2.2, 로그 posLBR 확인) "
      "②R 1.5↔2.5 로 크기 바뀌는 게 보이나 ③달 클로즈업도 크게 나오나(수동 배치 R=2.4 먹히나) "
      "④달 위상 스윕 보이나 ⑤중앙 정렬(height 115) 맞나 — 치우치면 값 알려줘")

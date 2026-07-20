# -*- coding: utf-8 -*-
"""
moon_phase_show.py — [v1] 신규 객체 실험: Satellite(달) + DomePointer
====================================================================
이번에 처음 써보는 것:
  · Satellite            — 달! setManualMoonPhase / setMoonAge(0~29.5) = 위상 수동 제어
  · DomePointer          — 화면(돔) 좌표 포인터 (azimuth/height/apparentSize)
검증 겸하는 것:
  · setPositionR 화면고정 줌 (이번에 예제를 바꾼 방식 — 달에서도 화면 안 움직이는지!)
  · 행성 프레임 스텝 오빗 (track=-1 + TH 재조준) — 성운에선 확정, 행성계는 첫 실험

흐름: 리셋 → 달 FadeTo → 돔 중앙 → 줌인 → ★위상 타임랩스(신월→보름) →
      스텝 오빗 90° → DomePointer 데모
콘솔의 ★/힌트 줄을 그대로 보내줘 — 다음 버전에 반영할게.
"""
from skyExplorer import *
from studio import *
from Initialization import *

# ── 0) 리셋 ─────────────────────────────────────────────────
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])

cam = Camera(Camera.CameraName.MainCamera)

# ── 1) [프로브] Satellite 이름 enum 확인 ─────────────────────
print("★1 SatelliteName 멤버:", [n for n in dir(Satellite.SatelliteName)
                                 if not n.startswith("_")][:30])
moon = None
for name in ("Moon", "MOON", "Luna"):
    try:
        moon = Satellite(getattr(Satellite.SatelliteName, name))
        print("★1 달 객체 OK: %s (id=%s)" % (name, moon.id))
        break
    except Exception as e:
        print("   %s 실패: %s" % (name, repr(e)[:50]))
if moon is None:
    print("★1 달 못 찾음 — 위 멤버 목록에서 이름 알려줘!")

# ── 2) 달 FadeTo (타입 프로브: Satellite/Moon/Planet) ────────
ok = False
for tname in ("SatelliteType", "MoonType", "PlanetType", "SolarSystemType"):
    try:
        t = getattr(Data.Type, tname)
        obj = DataManager.database().data(t, "Moon")
        if obj.id != -1:
            obj.action(Action.Type.FadeTo).trigger()
            print("★2 FadeTo OK: Data.Type.%s / 'Moon'" % tname)
            ok = True
            break
        print("   %s: id=-1" % tname)
    except Exception as e:
        print("   %s 실패: %s" % (tname, repr(e)[:50]))
if not ok:
    print("★2 FadeTo 실패 — Data.Type 후보:",
          [n for n in dir(Data.Type) if "atel" in n or "oon" in n or "olar" in n])
sleep(4.0)

# ── 3) 돔 중앙 + 화면고정 줌 (검증된 레시피 + 새 줌 방식) ─────
cam.setTargetHeight(90.0, Anim(2.0))
sleep(2.5)                                   # 조준 완전 종료 후 줌
p = cam.positionLBR
print("★3 도착 R = %.3f (단위: 달 반지름)" % p.z)
cam.setPositionR(p.z * 0.5, Anim.cubic(4.0), -1)   # R만 변경 — 화면 움직이면 알려줘!
sleep(4.5)
print("★3 줌인 후 R = %.3f  (줌 중 화면이 움직였는지 확인!)" % cam.positionLBR.z)

# ── 4) ★★ 달 위상 타임랩스 (Satellite 첫 실험) ───────────────
if moon is not None:
    try:
        moon.setManualMoonPhase(True)
        print("★4 수동 위상 모드 ON")
        moon.setMoonAge(0.0, Anim(0.0))      # 신월부터
        sleep(1.0)
        moon.setMoonAge(29.5, Anim(15.0))    # 15초 동안 한 달치 위상 스윕
        print("★4 위상 스윕 시작 (신월→보름→그믐, 15초) — 위상이 변하는지!")
        sleep(15.5)
        moon.setMoonAge(14.8, Anim(2.0))     # 보름달로 마무리
        sleep(2.5)
        moon.setManualMoonPhase(False)       # 원상 복구 (실제 날짜 위상으로)
        print("★4 위상 스윕 끝, 자동 모드 복귀")
    except Exception as e:
        print("★4 위상 제어 실패:", repr(e)[:80])

# ── 5) 스텝 오빗 90° — 행성 프레임 변형 첫 실험 ──────────────
#     (성운 LOS 프레임에선 확정. 행성/위성 FadeTo 프레임에선 track=-1 +
#      TH 재조준(89.9→90 no-op 우회)이 우리 가설 — 이게 실험 포인트)
print("★5 스텝 오빗 90° 시작 (달이 화면 중앙에 유지되는지!)")
try:
    step_dt = 0.5
    n = 24                                   # 12초 / 90°
    p = cam.positionLBR
    L0, B0, R0 = p.x, p.y, p.z
    for i in range(1, n + 1):
        L = L0 + 90.0 * i / float(n)
        cam.setPositionLBR(Vec(L, B0, R0), Anim(step_dt), -1)
        if i % 4 == 0:                       # 2초마다 TH 재조준 (no-op 우회)
            cam.setTargetHeight(89.9, Anim(0.1))
            cam.setTargetHeight(90.0, Anim(0.2))
        sleep(step_dt)
    print("★5 오빗 끝 — 중앙 유지? / 화면이 레코드판처럼 돌았는지?")
except Exception as e:
    print("★5 오빗 실패:", repr(e)[:80])

# ── 6) [프로브] DomePointer — 화면 좌표 포인터 첫 실험 ────────
try:
    enum_names = [n for n in dir(DomePointer) if "Name" in n]
    print("★6 DomePointer enum 후보:", enum_names)
    name_enum = getattr(DomePointer, enum_names[0])
    members = [m for m in dir(name_enum) if not m.startswith("_")]
    print("★6 %s 멤버:" % enum_names[0], members[:10])
    dp = DomePointer(getattr(name_enum, members[0]))     # 첫 멤버로 생성
    print("★6 생성 OK: %s (id=%s)" % (members[0], dp.id))
    dp.setColor(Vec(1.0, 0.75, 0.3), Anim(0.0))
    dp.setPosition(Vec(0.0, 80.0, 0.0), Anim(0.0))     # 달 근처(천정 부근)
    dp.setApparentSize(6.0, Anim(0.0))
    dp.setPointerIntensity(1.0, Anim(1.0))
    print("★6 포인터 ON (주황 원이 달 근처에 보이는지!)")
    sleep(2.0)
    dp.setPosition(Vec(0.0, 88.0, 0.0), Anim(2.0))     # 달 쪽으로 슬라이드
    dp.setApparentSize(3.0, Anim(2.0))                 # 조여들기
    sleep(3.0)
    dp.setPointerIntensity(0.0, Anim(1.5))
    print("★6 포인터 데모 끝")
except Exception as e:
    print("★6 DomePointer 실패:", repr(e)[:100])
    print("   힌트 dir(DomePointer):",
          [n for n in dir(DomePointer) if not n.startswith("_")][:20])

# ── 7) 자막 ─────────────────────────────────────────────────
try:
    txt = InsertText(InsertText.InsertTextName(1))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setText("달의 위상 The Phases of the Moon")
    txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045)
    txt.setColor(Vec(0.85, 0.85, 1.0)); txt.setIntensity(1.0, Anim(1.5))
except Exception as e:
    print("자막 실패:", repr(e)[:60])

print(">>> 쇼 끝! ★1~★6 콘솔 줄 + (a)줌 중 화면 고정? (b)위상 변화 보임? "
      "(c)오빗 중앙 유지? (d)포인터 보임? 알려줘")

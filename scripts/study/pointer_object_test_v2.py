# -*- coding: utf-8 -*-
"""
pointer_object_test_v2.py — 목성 포인터 미표시 원인 검증 (2026-07-07)
v1 실측: 베텔게우스 ①내장 ②PointerOn 모두 성공 / M42 PointerOn 미지원 / 목성 PointerOn 안 보임.

★ 가설: v1 의 베텔게우스는 ①에서 setPointerType(Model1Bold) 을 미리 해둔 상태라 ②도 보였고,
  목성은 타입 설정 없이 PointerOn 만 해서 **기본 pointerType=Invalid → 그릴 모델이 없어** 안 보인 것.
  (Mark 빈 슬롯과 같은 '기본값 Invalid' 패턴. 목성은 2026-01-10 충 직후라 지평선 위 확실.)

검증 순서:
  A. 목성 pointerType 기본값 읽기(프로브) → 타입 없이 PointerOn (v1 재현 — 안 보여야 가설 지지)
  B. setPointerType(Model1Bold) 후 → 보이는지 (가설 확정 지점!)
  C. 대조군: 리겔을 '타입 설정 없이' PointerOn — 안 보이면 가설 이중 확정
  D. M42 대안: Messier 클래스엔 포인터 API 자체가 없음(레퍼런스 확인) → Nebula 경유
     (NebulaName 에 ORION 계열 있는지 프로브 + DB NebulaType 이름 검색)
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 무대 (동일: 청주 2026-01-15 23:00 KST) ────────────────────
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 14, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0))    # 남쪽 — 목성(쌍둥이자리, 충 직후)도 이 근처
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

jup = Planet(Planet.PlanetName.Jupiter)
jup.setIntensity(1.0, Anim(0.0))

# ── A. 기본 타입 프로브 + 타입 없이 PointerOn (v1 재현) ───────
print("=" * 60)
print("A. 목성 pointerType 기본값 + 타입 없이 PointerOn")
print("=" * 60)
try:
    print("[PROBE] 목성 기본 pointerType=%s pointerIntensity=%.2f"
          % (jup.pointerType, jup.pointerIntensity))
except Exception as e:
    print("[PROBE] 읽기 실패: %s" % e)
try:
    d = DataManager.database().data(Data.Type.PlanetType, "Jupiter")
    a = d.action(Action.Type.PointerOn) if d is not None else None
    if a is not None:
        t1.setText("A. 목성 PointerOn (타입 설정 없음) — 안 보이면 가설 지지")
        t1.setIntensity(1.0, Anim(0.5))
        a.trigger()
        sleep(5.0)
except Exception as e:
    print("   A 실패: %s" % e)

# ── B. 타입 설정 후 — 가설 확정 지점 ─────────────────────────
print("=" * 60)
print("B. setPointerType(Model1Bold) 후 — 이제 보여야 함!")
print("=" * 60)
try:
    jup.setPointerType(Body.PointerType.Model1Bold)
    jup.setPointerIntensity(1.0, Anim(1.0))
    try:
        print("[PROBE] 설정 후 pointerType=%s intensity=%.2f"
              % (jup.pointerType, jup.pointerIntensity))
    except Exception:
        pass
    t1.setText("B. 목성 — 타입 설정 후 (동남쪽 하늘 확인!)")
    print("   ★ 목성 포인터가 이제 보이나? (쌍둥이자리 부근, 남동쪽)")
    sleep(8.0)
    jup.setPointerIntensity(0.0, Anim(1.0))
    sleep(1.2)
    t1.setIntensity(0.0, Anim(0.3))
except Exception as e:
    print("   B 실패: %s" % e)

# ── C. 대조군: 리겔 (타입 설정 없이 PointerOn) ────────────────
print("=" * 60)
print("C. 대조군 리겔 — 타입 없이 PointerOn (안 보이면 가설 이중 확정)")
print("=" * 60)
try:
    rig = IndividualStar(IndividualStar.IndividualStarName.Rigel)
    print("[PROBE] 리겔 기본 pointerType=%s" % rig.pointerType)
    d = DataManager.database().data(Data.Type.StarType, "Rigel")
    a = d.action(Action.Type.PointerOn) if d is not None else None
    if a is not None:
        t1.setText("C. 리겔 PointerOn (타입 없음) — 보이나요?"); t1.setIntensity(1.0, Anim(0.5))
        a.trigger()
        sleep(5.0)
        a_off = d.action(Action.Type.PointerOff)
        if a_off is not None:
            a_off.trigger()
    sleep(1.0)
    t1.setIntensity(0.0, Anim(0.3))
except Exception as e:
    print("   C 실패: %s" % e)

# ── D. M42 대안: Nebula 클래스 경유 ───────────────────────────
print("=" * 60)
print("D. M42 — Messier 는 포인터 API 없음(레퍼런스) → Nebula 경유")
print("=" * 60)
try:
    neb_names = [m for m in dir(Nebula.NebulaName) if not m.startswith("_")
                 and m not in ("name", "names", "values")]
    ori_cands = [n for n in neb_names if "ORI" in n.upper() or "M42" in n.upper()]
    print("[PROBE] NebulaName 오리온 후보: %s (전체 %d개)" % (ori_cands, len(neb_names)))
    target = None
    for n in ori_cands:
        neb = Nebula(getattr(Nebula.NebulaName, n))
        if neb.id != -1:
            target = (n, neb)
            break
    if target is not None:
        n, neb = target
        neb.setPointerType(Body.PointerType.Model2Bold)
        neb.setPointerIntensity(1.0, Anim(1.0))
        t1.setText("D. 성운 내장 포인터 — %s" % n); t1.setIntensity(1.0, Anim(0.5))
        print("   %s 내장 포인터 ON — 오리온 허리 아래(검) 확인!" % n)
        sleep(7.0)
        neb.setPointerIntensity(0.0, Anim(1.0))
        sleep(1.2)
        t1.setIntensity(0.0, Anim(0.3))
    else:
        print("   enum 에 오리온 성운 없음 → DB 이름 검색 폴백")
        for nm in ("M 42", "M42", "Orion Nebula", "NGC 1976"):
            d = DataManager.database().data(Data.Type.NebulaType, nm)
            if d is not None:
                print("   DB 발견: NebulaType '%s' → PointerOn 시도" % nm)
                a = d.action(Action.Type.PointerOn)
                if a is not None:
                    a.trigger(); sleep(5.0)
                    off = d.action(Action.Type.PointerOff)
                    if off is not None:
                        off.trigger()
                break
except Exception as e:
    print("   D 실패: %s" % e)

# ── 정리 ──────────────────────────────────────────────────────
try:
    d = DataManager.database().data(Data.Type.PlanetType, "Jupiter")
    if d is not None:
        off = d.action(Action.Type.PointerOff)
        if off is not None:
            off.trigger()
except Exception:
    pass
t1.setText("v2 끝 — A(안 보임?)/B(보임?)/C(안 보임?)/D 리포트!")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("v2 종료. [PROBE] 줄들(기본 pointerType 값!)을 꼭 복사해줘.")

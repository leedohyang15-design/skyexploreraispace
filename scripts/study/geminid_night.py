# -*- coding: utf-8 -*-
"""
geminid_night.py — 쌍둥이자리 유성우의 밤 v1 (2026-07-07)
새 예제: 이번에 처음 연습하는 클래스 2종 실측.

 ① ShootingStar — 유성/유성우 (레퍼런스로 시그니처 확인, 실행은 처음):
    단발 = setStartPosition/setArrivalPosition(Vec2 az,h 화면좌표) + setAdvancing(0→1, Anim)
    유성우 = setRainGradientPoint(복사점 Vec2) + setRainChaosGradientPoint(반경°) +
             setZenithalHourlyRate(ZHR) + setRainSpeed + setRainSeed(0=정지, 그 외=생성)
    setReferential: TargetedForeground(돔 화면공간, 기본) / RaDec(하늘 고정 — 진짜 복사점!)
 ② Bolide — 화구(불덩이 유성): set(시작az,h,고도m, 끝az,h,고도m, 속도) → play(속도)
    setElement(원소, 색) — 유성 색 = 조성 연출 추정 (enum 프로브)

무대: 청주 2026-12-14 23:00 KST(=14:00 UT) — 쌍둥이자리 유성우 극대일.
복사점(카스토르 부근): 방위 ≈75°(동북동), 고도 ≈45° → 카메라 H = 180−75 = 105.
⚠️ 좌표계 미확정 지점(이번 실측 포인트): ShootingStar 의 화면좌표가 DomePointer 규약
   (az=180−방위, h=Target값)과 같은지 / RaDec 모드의 Vec2 가 (적경°, 적위°)인지.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
st  = Stars(Stars.StarsName.StarrySky)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d개): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e))
        return []


# ══════════════════════════════════════════════════════════════
# ACT 0 — 프로브: 생성 enum / Referential / Bolide.Element
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 0: ShootingStar / Bolide 프로브")
print("=" * 60)
ss_members = probe("ShootingStar 클래스", ShootingStar)
name_enum = None
for m in ss_members:
    if m.lower().endswith("name"):
        vals = probe("ShootingStar.%s" % m, getattr(ShootingStar, m))
        real = [v for v in vals if "Invalid" not in v and not v.endswith("Count")]
        if real:
            name_enum = (m, real[0])
            break
if "Referential" in ss_members:
    probe("ShootingStar.Referential", ShootingStar.Referential)

ss = None
try:
    if name_enum is not None:
        en, first = name_enum
        ss = ShootingStar(getattr(getattr(ShootingStar, en), first))
        print("[PROBE] ShootingStar(%s.%s) → id=%s" % (en, first, ss.id))
    if ss is not None and ss.id != -1:
        print("[PROBE] 기본값: ZHR=%s rainSpeed=%s brightness=%s trailLength=%s referential=%s"
              % (ss.zenithalHourlyRate, ss.rainSpeed, ss.brightness,
                 ss.trailLength, ss.referential))
except Exception as e:
    print("[PROBE] ShootingStar 생성/기본값 실패: %s" % e)

probe("Bolide.Element", Bolide.Element) if hasattr(Bolide, "Element") else print("[PROBE] Bolide.Element 없음")


# ══════════════════════════════════════════════════════════════
# ACT 1 — 무대: 청주, 쌍둥이자리 유성우 극대일 밤
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 1: 무대 — 2026-12-14 23:00 KST, 복사점(동북동 45°) 조준")
print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))

earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
st.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 60.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 14, 14, 0, 0, tz, Anim(0.5))    # 14 UT = 23시 KST
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0))
cam.setOrientationH(105.0, Anim(0.0))                    # H = 180 − 복사점 방위(75)
sleep(0.5)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035)
t1.setDistance(1.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("쌍둥이자리 유성우 — 12월 14일, 극대의 밤")
t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# 쌍둥이 별자리 + 복사점 별 포인터 (확정 레시피: 타입 지정은 습관적으로 항상)
gem = Constellation(Constellation.ConstellationName.Gem)
gem.setLinesIntensity(0.8, Anim(2.0))
gem.setLabelIntensity(0.6, Anim(2.0))
try:
    radiant_star = None
    for cand in ("Castor", "Pollux"):
        if hasattr(IndividualStar.IndividualStarName, cand):
            radiant_star = IndividualStar(getattr(IndividualStar.IndividualStarName, cand))
            radiant_star.setPointerType(Body.PointerType.Model1Bold)
            radiant_star.setPointerIntensity(1.0, Anim(1.5))
            print("   복사점 마커: %s 내장 포인터 ON" % cand)
            break
except Exception as e:
    radiant_star = None
    print("   복사점 포인터 실패: %s" % e)
t1.setText("복사점 — 카스토르 곁, 여기서 유성이 뻗어 나온다")
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)


# ══════════════════════════════════════════════════════════════
# ACT 2 — 단발 유성 3발 (수동 발사: setAdvancing 0→1)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 2: 단발 유성 — setStartPosition→setArrivalPosition + setAdvancing")
print("=" * 60)
if ss is not None:
    try:
        ss.setRepresentationType(ShootingStar.Model.Gradient)
        ss.setBrightness(1.5)
        ss.setTrailLength(1.0)
        ss.setIntensity(1.0, Anim(0.0)) if hasattr(ss, "setIntensity") else None
        t1.setText("하나… 둘… 셋 — 소원을 준비하세요"); t1.setIntensity(1.0, Anim(0.5))
        shots = [((-20.0, 80.0), (40.0, 35.0)),
                 ((10.0, 75.0), (-50.0, 30.0)),
                 ((30.0, 70.0), (70.0, 25.0))]
        for i, (s0, s1_) in enumerate(shots):
            ss.setAdvancing(0.0, Anim(0.0))
            ss.setStartPosition(Vec2(s0[0], s0[1]))
            ss.setArrivalPosition(Vec2(s1_[0], s1_[1]))
            sleep(0.3)
            ss.setAdvancing(1.0, Anim(1.2))          # ★ 0→1 = 유성 비행 (가설 — 실측 포인트!)
            print("   %d발: (%.0f,%.0f)→(%.0f,%.0f)" % (i + 1, s0[0], s0[1], s1_[0], s1_[1]))
            sleep(2.5)
        t1.setIntensity(0.0, Anim(0.5))
    except Exception as e:
        print("   단발 유성 실패: %s" % e)
else:
    print("   ShootingStar 핸들 없음 → 스킵")


# ══════════════════════════════════════════════════════════════
# ACT 3 — 유성우: 돔 공간 → RaDec(하늘 고정 복사점) 2단계
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 3: 유성우 (ZHR 800 → 1500)")
print("=" * 60)
# ⚠️ Recording7 실측: ZHR 는 내부 '분당' 저장(ZHR/60). 120 = 분당 2개 = 30초에 1개라 돔에선
#    거의 안 보임 → v1 '애매함'의 정체. 볼만한 유성우는 ZHR 800~1500 으로 크게.
if ss is not None:
    try:
        # 3a. 기본 referential(돔 화면공간): 복사점을 돔 좌표 (0, 60) — 화면 위쪽 중앙 부근
        t1.setText("유성우 — 별똥별이 쏟아진다"); t1.setIntensity(1.0, Anim(0.5))
        ss.setRainGradientPoint(Vec2(0.0, 60.0))
        ss.setRainChaosGradientPoint(15.0)           # 복사점 원 반경 15°
        ss.setRainSpeed(1.0)
        ss.setZenithalHourlyRate(800.0)              # 분당 ≈13개 — 눈에 확 띄는 밀도
        ss.setRainSeed(1)                            # ★ 0 이 아닌 값 = 생성 시작
        print("   3a: 돔공간 복사점 (0,60), ZHR 800(분당13) — 밀도 확인! (12초)")
        sleep(12.0)

        # 3b. RaDec 모드: 진짜 복사점(카스토르 RA≈113°, Dec≈+32°) — 하늘에 고정
        ref_members = [m for m in dir(ShootingStar.Referential) if not m.startswith("_")]
        radec = None
        for m in ref_members:
            if "radec" in m.lower() or "ra_dec" in m.lower():
                radec = getattr(ShootingStar.Referential, m)
                break
        if radec is not None:
            t1.setText("복사점을 하늘에 고정 — 쌍둥이자리에서 뻗는 유성")
            ss.setReferential(radec)
            ss.setRainGradientPoint(Vec2(113.0, 32.0))   # (RA°, Dec°) — Recording7 로 좌표 규약 확정
            ss.setZenithalHourlyRate(1500.0)             # 분당 25개
            print("   3b: RaDec 복사점 (113,32), ZHR 1500(분당25) — 쌍둥이자리에서 방사되는지! (14초)")
            sleep(14.0)
        else:
            print("   RaDec 멤버 못 찾음 (Referential: %s) → 3b 스킵" % ref_members)
        t1.setIntensity(0.0, Anim(0.5))
    except Exception as e:
        print("   유성우 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT 4 — 화구(Bolide) 한 발
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 4: 화구 — Bolide.set() + play()")
print("=" * 60)
try:
    bo = Bolide(Bolide.BolideName.Bolide001)
    print("   Bolide001 id=%s" % bo.id)
    # ✅ 화구 확정 레시피 (2026-07-09 실측, bolide_fireball_test_v2):
    #   ① setModel(ColoredFireball, "") — 모델 없으면 안 그려짐. Chelyabinsk 는 이 빌드서 렌더 실패.
    #      ⚠️ filename "" 필수(내장도).  ② setElement(원소, Vec3, Anim) — 3인자 전부 필수.
    #      Sodium=주황 불덩이(사용자 "진짜 운석 떨어지듯이" 확인).
    #   ③ set() speed 는 1.0 고정(바꾸면 안 보임), 재생은 play() — 크로싱 = 148/play 초.
    bo.setModel(Bolide.ModelID.ColoredFireball, "")
    bo.setElement(Bolide.Element.Sodium, Vec3(0.0, 0.0, 0.0), Anim(0.0))
    bo.setIntensity(1.0, Anim(0.0))
    t1.setText("화구(火球) — 커다란 불덩이 하나"); t1.setIntensity(1.0, Anim(0.5))
    bo.set(-30.0, 70.0, 100000.0, 50.0, 15.0, 30000.0, 1.0)
    sleep(0.3)
    bo.play(15.0)                                # ≈ 10초 크로싱 (묵직한 불덩이)
    print("   화구 발사! ColoredFireball + Sodium, play(15) ≈ 10초")
    sleep(11.0)
    t1.setIntensity(0.0, Anim(0.5))
except Exception as e:
    print("   Bolide 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# ACT 5 — 폭풍 피날레 → 정지
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 5: 유성 폭풍 (ZHR 3000, 10초) → 고요")
print("=" * 60)
if ss is not None:
    try:
        t1.setText("1833년의 기억 — 유성 폭풍"); t1.setIntensity(1.0, Anim(0.5))
        ss.setZenithalHourlyRate(3000.0, Anim(3.0))
        sleep(10.0)
        t1.setText("그리고, 다시 고요한 밤")
        ss.setZenithalHourlyRate(60.0, Anim(4.0))
        sleep(5.0)
        ss.setRainSeed(0)                            # ★ 0 = 정지
        sleep(2.0)
        t1.setIntensity(0.0, Anim(0.8))
    except Exception as e:
        print("   폭풍 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
gem.setLinesIntensity(0.0, Anim(2.0))
gem.setLabelIntensity(0.0, Anim(2.0))
if radiant_star is not None:
    try:
        radiant_star.setPointerIntensity(0.0, Anim(1.5))
    except Exception:
        pass
t1.setText("쌍둥이자리 유성우의 밤 — 끝"); t1.setIntensity(1.0, Anim(1.0))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("쇼 종료. 리포트 포인트: ①단발 3발 보였나 ②3a 돔 유성우 ③3b 쌍둥이 복사점 방사 ④화구 ⑤[PROBE] 줄들")

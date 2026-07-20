# -*- coding: utf-8 -*-
"""
comet_halley.py — 핼리 혜성 궤도 그리기 v1 (2026-07-09)
새 예제: 처음 연습하는 Comet 클래스 — 궤도 6요소로 혜성을 '직접' 만든다.

★ 이번에 처음 쓰는 API (레퍼런스로 시그니처 확인):
 · 궤도 요소: setEccentricity / setInclination / setLongitudeOfAscendingNode /
   setArgumentOfPeriapsis / setDistanceToPeriapsis / setTimeOfLastPeriapsis
 · 표시: setIntensity / setOrbitIntensity / setOrbitThickness / setModelScale / setLabelIntensity
 · 모델: setStandardModelName(CometModelSet) — Basic/Generic3D/Halley3D/HaleBopp3D/
   Hyakutake3D/McNaught3D/Bradfield3D (⚠️ 3D 모델은 에셋 필요할 수 있음 — Basic 우선)

핼리 혜성 궤도 요소 (J2000, 실제값):
 이심률 0.967 / 경사 162.3°(역행) / 승교점경도 58.42° / 근일점편각 111.33°
 근일점거리 0.586 AU / 마지막 근일점 1986-02-09 (JD 2446470.5)
⚠️ distanceToPeriapsis·timeOfLastPeriapsis 의 단위는 미확정(AU/JD 가설) — 이번 실측 포인트.

우주 조망: 태양 Ecliptic 포트 기준 카메라(태양계 내행성 시점). 지상 아님.
시간가속: 2024 → 2061(다음 근일점)까지 DateManager 로 흘려 혜성이 궤도를 도는 걸 관찰.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d개): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e))
        return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ══════════════════════════════════════════════════════════════
# ACT 0 — 프로브: Comet 생성 enum / CometModelSet / CometPort
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 0: Comet 프로브")
print("=" * 60)
comet_members = probe("Comet 클래스", Comet)
name_enum = None
for m in comet_members:
    if m.lower().endswith("name"):
        vals = probe("Comet.%s" % m, getattr(Comet, m))
        real = [v for v in vals if "Invalid" not in v and not v.endswith("Count")]
        if real:
            name_enum = (m, real[0])
        break
if hasattr(Comet, "CometModelSet"):
    probe("Comet.CometModelSet", Comet.CometModelSet)
if hasattr(Comet, "CometPort"):
    probe("Comet.CometPort", Comet.CometPort)

# ══════════════════════════════════════════════════════════════
# ACT 1 — 우주 조망 세팅 (태양계 내행성 시점)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 1: 태양계 조망 세팅")
print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))

Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.0))

dm.stop(); sleep(0.3)
dm.setDateTime(2024, 1, 1, 0, 0, 0, tz, Anim(0.5))
sleep(1.0)

# 태양 Ecliptic 포트 기준으로 카메라 배치 (복합 데모 확정 프레이밍)
sun_port = -1
try:
    sun_port = sun.portId(IndividualStar.IndividualStarPort.Ecliptic)
    print("   sun ecliptic port=%s" % sun_port)
except Exception as e:
    print("   sun port 실패(track=-1 폴백): %s" % e)
try:
    cam.setPositionLBR(Vec(0.0, 55.0, 40.0), Anim(3.0), sun_port)   # 황도 위 비스듬히 조망
    sleep(3.5)
except Exception as e:
    print("   카메라 배치 실패: %s" % e)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0))
t1.setDistance(20.0, Anim(0.0))         # ★ 우주/행성 프레임 자막 = distance 20 (기본 size)
t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("핼리 혜성 — 76년 만의 귀환"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ══════════════════════════════════════════════════════════════
# ACT 2 — 혜성 생성 + 궤도 요소 주입
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 2: 핼리 궤도 요소 주입")
print("=" * 60)
comet = None
try:
    if name_enum is not None:
        en, first = name_enum
        comet = Comet(getattr(getattr(Comet, en), first))
        print("   Comet(%s.%s) → id=%s" % (en, first, comet.id))
except Exception as e:
    print("   Comet 생성 실패: %s" % e)

if comet is not None and comet.id != -1:
    try:
        comet.setEccentricity(0.967)
        comet.setInclination(162.3)
        comet.setLongitudeOfAscendingNode(58.42)
        comet.setArgumentOfPeriapsis(111.33)
        comet.setDistanceToPeriapsis(0.586)              # AU 가설
        comet.setTimeOfLastPeriapsis(2446470.5)          # JD 1986-02-09 가설
        comet.setModelScale(3.0)
        print("   궤도 요소 주입 완료")
        # 읽기 검증
        try:
            print("   읽음: e=%.3f i=%.1f node=%.1f peri=%.1f q=%.3f"
                  % (comet.eccentricity, comet.inclination, comet.longitudeOfAscendingNode,
                     comet.argumentOfPeriapsis, comet.distanceToPeriapsis))
        except Exception:
            pass

        # 모델: Basic 우선(안전). 3D 는 에셋 이슈 가능 → 별도 실측.
        try:
            comet.setStandardModelName(Comet.CometModelSet.Basic)
            print("   setStandardModelName(Basic) OK")
        except Exception as e:
            print("   모델 설정 실패: %s" % e)

        t1.setText("궤도를 그린다 — 태양을 향한 긴 타원")
        t1.setIntensity(1.0, Anim(0.8))
        comet.setOrbitThickness(2.0)
        comet.setOrbitIntensity(0.9, Anim(2.0))          # 궤도선 페이드인
        comet.setIntensity(1.0, Anim(2.0))               # 혜성 본체
        comet.setLabelIntensity(0.8, Anim(2.0))
        # 포인터로 혜성 지목 (개체 직결 — 타입 지정 습관)
        try:
            comet.setPointerType(Body.PointerType.Model2Bold)
            comet.setPointerIntensity(1.0, Anim(1.5))
        except Exception as e:
            print("   포인터 실패: %s" % e)
        print("   ★ 궤도선/혜성/라벨이 보이는지 확인 (8초)")
        sleep(8.0)
        t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)
    except Exception as e:
        print("   궤도 요소 주입 실패: %s" % e)
else:
    print("   Comet 핸들 없음 → 이후 스킵 ([PROBE] 로 생성 enum 확인 필요)")

# ══════════════════════════════════════════════════════════════
# ACT 3 — 시간가속: 2024 → 2061 근일점 (혜성이 궤도를 돈다)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("ACT 3: 시간가속 2024 → 2061 (다음 근일점)")
print("=" * 60)
if comet is not None and comet.id != -1:
    try:
        t1.setText("시간을 빠르게 — 2061년 근일점으로")
        t1.setIntensity(1.0, Anim(0.8))
        # 37년을 25초에 흘림 (DateManager 시간가속 확정 동작)
        dm.setDateTime(2061, 7, 28, 0, 0, 0, tz, Anim(25.0))
        for i in range(5):
            sleep(5.0)
            try:
                print("   JD=%.2f" % dm.julianDate)
            except Exception:
                pass
        print("   ★ 혜성이 궤도를 따라 이동했나? 근일점(태양 근처)에서 밝아졌나?")
        sleep(1.0)
        t1.setText("태양을 스치고 — 다시 먼 우주로")
        sleep(4.0)
        t1.setIntensity(0.0, Anim(0.8))
    except Exception as e:
        print("   시간가속 실패: %s" % e)

# ══════════════════════════════════════════════════════════════
# 피날레
# ══════════════════════════════════════════════════════════════
t1.setText("핼리 혜성 — 다음 만남은 2061년")
t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①[PROBE] Comet 생성 enum/모델셋 ②궤도선·혜성 보였나 ③시간가속 이동/근일점 밝아짐")

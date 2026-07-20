# -*- coding: utf-8 -*-
"""
comet_halley_v2.py — 혜성 '안 보임' 진단 + DB 경로 (2026-07-09)
v1 실측: 궤도 요소 setter 호출은 예외 없이 통과했으나 **읽기값이 전부 0** (e=0 i=0 q=0) →
        혜성이 태양 중심 점으로 뭉개져 안 보임. 요소가 반영 안 됨이 근본 원인.

이번 v2 두 갈래:
 [A] 왜 0 인지 진단 — 모델 먼저 설정 + Anim(0.0) 명시 + 각 setter 뒤 sleep + 재읽기.
     (Mark 빈 슬롯처럼 Comet001 이 '미활성 슬롯'이라 요소를 무시하는지 확인)
 [B] DB 경로 — Data.Type.CometType 존재 확인됨! 성운처럼 실제 혜성을 이름으로 FadeTo.
     enum 슬롯이 안 먹으면 이게 정답 경로(성운 Barnard 33 우회로와 동일 패턴).

무대: 우주 조망(태양계). 지상 아님.
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

# ── 무대 ──────────────────────────────────────────────────────
print("무대: 태양계 조망")
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

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.8, 0.9, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.5)


# ══════════════════════════════════════════════════════════════
# [A] 궤도 요소 진단 — 모델 먼저 + Anim(0.0) + sleep + 재읽기
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("[A] 궤도 요소 진단 (Comet001)")
print("=" * 60)
comet = Comet(Comet.CometName.Comet001)
print("   Comet001 id=%s" % comet.id)
try:
    # ① 모델·스케일 먼저 (Mark 처럼 슬롯 초기화가 필요할 수 있어 순서 변경)
    comet.setStandardModelName(Comet.CometModelSet.Basic)
    comet.setModelScale(5.0)
    comet.setIntensity(1.0, Anim(0.0))
    sleep(0.5)
    # ② 요소를 Anim(0.0) 명시로 하나씩 + 각각 뒤 sleep 후 재읽기
    def set_read(name, setter, val):
        try:
            setter(val, Anim(0.0))
            sleep(0.3)
            got = getattr(comet, name)
            print("   %s: 넣음=%.3f 읽음=%.3f %s" % (name, val, got, "OK" if abs(got-val) < 0.01 else "❌0/미반영"))
        except Exception as e:
            print("   %s 실패: %s" % (name, e))
    set_read("eccentricity",             comet.setEccentricity,             0.967)
    set_read("inclination",              comet.setInclination,              162.3)
    set_read("longitudeOfAscendingNode", comet.setLongitudeOfAscendingNode, 58.42)
    set_read("argumentOfPeriapsis",      comet.setArgumentOfPeriapsis,      111.33)
    set_read("distanceToPeriapsis",      comet.setDistanceToPeriapsis,      0.586)
    set_read("timeOfLastPeriapsis",      comet.setTimeOfLastPeriapsis,      2446470.5)
    comet.setOrbitThickness(2.0)
    comet.setOrbitIntensity(0.9, Anim(1.5))
    comet.setLabelIntensity(0.8, Anim(1.5))
    t1.setText("[A] 슬롯 혜성 — 궤도선이 보이나?"); t1.setIntensity(1.0, Anim(0.5))
    print("   ★ [A] 궤도선/혜성이 보이는지 (7초)")
    sleep(7.0)
    t1.setIntensity(0.0, Anim(0.5)); sleep(1.0)
except Exception as e:
    print("   [A] 실패: %s" % e)


# ══════════════════════════════════════════════════════════════
# [B] DB 경로 — 실제 혜성을 이름으로 FadeTo (성운 우회로 패턴)
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("[B] DB CometType — 실제 혜성 FadeTo")
print("=" * 60)
# 여러 표기를 시도 (DB 명칭 미확정 — 성공하는 첫 이름 사용)
candidates = ["1P/Halley", "Halley", "Halley's Comet", "1P",
              "C/1995 O1 (Hale-Bopp)", "Hale-Bopp", "Hale Bopp",
              "C/2020 F3 (NEOWISE)", "NEOWISE"]
found = None
try:
    db = DataManager.database()
    for nm in candidates:
        try:
            d = db.data(Data.Type.CometType, nm)
            if d is not None:
                print("   DB 발견: CometType '%s'" % nm)
                found = (nm, d)
                break
            else:
                print("   '%s' → None" % nm)
        except Exception as e:
            print("   '%s' 조회 예외: %s" % (nm, e))
except Exception as e:
    print("   DB 접근 실패: %s" % e)

if found is not None:
    nm, d = found
    try:
        # 지원 액션 확인 후 FadeTo (없으면 On)
        act = d.action(Action.Type.FadeTo)
        if act is None:
            act = d.action(Action.Type.On)
        if act is not None:
            t1.setText("[B] %s — 실제 궤도" % nm); t1.setIntensity(1.0, Anim(0.5))
            act.trigger()
            print("   %s FadeTo/On 트리거 → 혜성 프레임으로 (6초)" % nm)
            sleep(6.0)
            # 시간가속으로 이동 관찰
            t1.setText("[B] 시간가속 — 궤도를 따라")
            dm.setDateTime(2035, 1, 1, 0, 0, 0, tz, Anim(12.0))
            sleep(13.0)
            t1.setIntensity(0.0, Anim(0.8))
        else:
            print("   FadeTo/On 액션 미지원")
    except Exception as e:
        print("   [B] 트리거 실패: %s" % e)
else:
    print("   DB 에서 혜성 못 찾음 → 위 후보 외 이름 필요 (로그의 None/예외 참고)")

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("혜성 진단 끝 — [A]요소 재읽기 / [B]DB 이름 리포트!")
t1.setIntensity(1.0, Anim(0.5))
sleep(4.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0))
sleep(3.5)
print("종료. 리포트: [A] 각 요소 'OK/❌' 줄 + 궤도선 보임? / [B] 어느 이름이 발견됐고 혜성 떴나?")

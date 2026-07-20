# -*- coding: utf-8 -*-
"""
messier_tour.py — 메시에 딥스카이 3종 투어 (2026-07-13, 확정 레시피)
★ 확정된 접근법 (프로브로 도달):
  · DB: MessierType 는 FadeTo 미지원 / DeepSkyObjectType 이름조회 실패 →
    **NebulaType + "M##" 가 정답** (M45 산개성단·M42 성운·M31 은하 전부 카탈로그됨).
  · 진입: **ConnectTo** (LookAt 미지원). = 대상 LOS 프레임으로 전환, R=초대형(트랙반지름 단위).
  · 센터링: 성운 LOS 프레임 = **Target 90 이 돔 중앙**.
  · 접근/확대: **setPositionR(읽은값×0.6, track=-1) 적응형 지오메트릭 줌** — 9스텝이면 돔 가득(사용자 확정).
    (setScale 아님. R 이 프레이밍/접근 담당. 아포피스 소행성과 동일 메커니즘.)
  · 첫 스텝 끊김 원인 = ConnectTo 내부 자세슬루(~4초) → **암전 속에서 진입·슬루·센터 끝내고 페이드인**.
  · R≈0(딥스카이 중앙)로 나오면 setScale 폴백.

무대: 초겨울 저녁(겨울 별자리 남중). 개체마다 암전 전환으로 슬루 숨김.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# 접근 이즈-인 램프(앞 완만). 개체별 depth 로 잘라 씀(최대 16).
EASE = [0.86, 0.74, 0.66, 0.62] + [0.60] * 12
CENTER_TH = 90.0 # 성운 LOS 프레임 돔 중앙

# ── 무대: 초겨울 저녁 밤하늘 ─────────────────────────────────
print("무대: 초겨울 저녁 밤하늘")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setIntensity(1.0, Anim(0.0))
Planet(Planet.PlanetName.Earth).setAtmosphereIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.45, Anim(0.0))
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 12, 1, 12, 0, 0, tz, Anim(0.5))
sleep(1.0)
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.9, 0.92, 1.0))

# 3종 대상: (DB 이름, Messier enum, 제목, 신화/설명, params)
#   params: depth=이즈램프 스텝수(개체별 줌 깊이) · roll=은하 등 기울기 세우기(deg, 0=안함)
#   ⚠️ 산개성단(M45)은 '날아드는' 접근에 부적합(밀집 천체 없음·배경 성운 잡음) → M27 로 교체.
#   세 타입: 행성상성운(M27) / 발광성운(M42) / 은하(M31, roll 로 세움).
TARGETS = [
    ("M27", Messier.MessierName.M27,
     "아령 성운 (M27)",
     "죽어가는 별의 마지막 숨결 — 우주로 흩어지는 가스 껍질",
     dict(depth=11, roll=0)),   # 작은 행성상성운 → 깊게 (4.85pc→~1.7pc)
    ("M42", Messier.MessierName.M42,
     "오리온 대성운 (M42)",
     "사냥꾼의 검 — 붉은 수소 구름 속 별의 탄생지",
     dict(depth=10, roll=0)),   # 32pc→~7pc (돔 가득)
    ("M31", Messier.MessierName.M31,
     "안드로메다 은하 (M31)",
     "250만 광년 — 맨눈으로 보는 가장 먼 것, 우리 은하의 이웃",
     dict(depth=7, roll=35)),   # 66kpc→~44kpc (크게, 통과 방지)
]

# DB 핸들 선확보 (NebulaType + "M##")
handles = {}
for key, _enum, _title, _desc, _p in TARGETS:
    try:
        handles[key] = DataManager.database().data(Data.Type.NebulaType, key)
        print("   DB '%s' = %s" % (key, handles[key] is not None))
    except Exception as e:
        handles[key] = None
        print("   DB '%s' 실패: %s" % (key, e))

# 인트로
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("밤하늘의 보석들 — 메시에 딥스카이 3선"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def approach(key, enum, title, desc, params):
    h = handles.get(key)
    ramp = EASE[:params.get("depth", 7)]
    roll = params.get("roll", 0)
    print("=" * 55); print("%s 접근 (depth=%d, roll=%d)" % (key, len(ramp), roll))
    if h is None:
        print("   DB 없음 → 건너뜀"); return

    # ① 암전 (ConnectTo 슬루 숨김)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)

    # ② ConnectTo (LOS 프레임 진입) — 내부 자세슬루 ~4초 대기
    ct = h.action(Action.Type.ConnectTo)
    nav = "ConnectTo"
    if ct is None:                                  # 폴백: FadeTo
        ct = h.action(Action.Type.FadeTo); nav = "FadeTo"
    if ct is not None:
        ct.trigger(); print("   진입=%s" % nav); sleep(6.5)
    else:
        print("   진입 액션 없음 → 건너뜀"); return

    # ②-b 배경/딴 개체 정리 (LOS 프레임에선 은하수·딴 딥스카이가 배경 잡음 → 끔)
    try:
        Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(1.5))
    except Exception:
        pass
    for _k, e2, _t, _d, _p in TARGETS:           # 딴 메시에 개체 끄기(오리온 성운 등 잡티 제거)
        if e2 != enum:
            try:
                Messier(e2).setIntensity(0.0, Anim(1.2))
            except Exception:
                pass
    try:
        Messier(enum).setIntensity(1.0, Anim(1.5))   # 타깃만 강조
    except Exception:
        pass

    # ③ Target 센터 + (은하 등) roll 로 세우기 — 암전 중에 다 끝냄
    cam.setTargetHeight(CENTER_TH, Anim.cubic(2.5)); sleep(2.7)
    if roll:
        try:
            b = cam.orientationHPR
            cam.setOrientationHPR(Vec(b.x, b.y, b.z + roll), Anim.cubic(3.0)); sleep(3.2)
            print("   roll %+d 적용(세우기)" % roll)
        except Exception as e:
            print("   roll 실패: %s" % e)
    try:
        R = cam.positionLBR.z
    except Exception:
        R = 0.0
    print("   진입 후 R=%.3e" % R)

    # ④ 페이드인 (개체 등장)
    t1.setText(title); t1.setIntensity(1.0, Anim(1.2))
    uni.setGlobalIntensity(1.0, Anim.cubic(2.6)); sleep(2.8)

    # ⑤ 접근 — ★ 목표 R 을 '절대값'으로 미리 계산 → 겹쳐 재생(정지 없이 연속=매끄러움)
    #   ⚠️ 'p.z×비율'(현재값 읽어 곱)은 겹치면 덜 줄고/작아지고 엉킴 → 절대 타겟은 겹쳐도 깊이 정확.
    t1.setText(desc)
    if R > 1.0:
        try:
            r = cam.positionLBR.z
            targets = []
            for ratio in ramp:
                r *= ratio
                targets.append(r)                  # [R0·r1, R0·r1r2, …] 마지막=정확한 최종 깊이
            for i, tgt in enumerate(targets):
                dur = 2.2 if i == 0 else 1.6        # 첫 스텝만 길게 = 가벼운 출발
                cam.setPositionR(tgt, Anim(dur), -1)
                sleep(dur * 0.60)                  # <Anim → 겹침(정지 없음). 절대타겟이라 깊이 손실 없음
            sleep(1.5)                             # 마지막 애니 완료 대기
            print("   접근 완료 R=%.3e (목표=%.3e)" % (cam.positionLBR.z, targets[-1]))
        except Exception as e:
            print("   접근 실패: %s" % e)
    else:
        # R≈0 (딥스카이 정중앙 도킹) → setScale (Messier 는 .scale 읽기 없음 → 절대값)
        print("   R≈0 딥스카이 → setScale 폴백")
        try:
            Messier(enum).setScale(80.0, Anim.cubic(7.0)); sleep(7.5)
        except Exception as e:
            print("   setScale 실패: %s" % e)
    sleep(3.5)
    t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


for key, enum, title, desc, params in TARGETS:
    approach(key, enum, title, desc, params)

# ── 피날레 ────────────────────────────────────────────────────
uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
SceneGraph().reset(1); sleep(1.5)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("메시에 목록 — 밤하늘에 흩어진 110개의 보석"); t1.setIntensity(1.0, Anim(1.2))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①3종 각각 ConnectTo 진입 R 값 ②암전 전환으로 첫 끊김 사라졌나 "
      "③9스텝으로 각각 돔 가득 왔나 ④M31/M45 도 M42 처럼 잘 되나(R≈0 폴백 탄 게 있나)")

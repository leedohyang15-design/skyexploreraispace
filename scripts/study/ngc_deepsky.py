# -*- coding: utf-8 -*-
"""
ngc_deepsky.py — NGC 클래스 예제 v2: 장미 성운 (2026-07-20, DB ConnectTo 방식으로 교체)
★ v1 실패(사용자): enum/포트는 잡혔으나(NGC enum=NGC2237, 포트=LineOfSightLocal) 자막만 보이고 별까지 다 사라짐.
  = 수동 `portId(NGC.NGCPort.LineOfSightLocal)` 카메라 이동이 프레임을 깨뜨림(NGC LOS 는 Nebula LOS 와 다르게 동작).
★ v2 = 검증된 딥스카이 접근(messier_tour.py, M42/M27/M31 렌더 확인): DB 핸들 → **ConnectTo**(내부 자세슬루, 암전 속)
  → setTargetHeight(90) 센터 → 페이드인 → **setPositionR 절대타겟 지오메트릭 줌**. 수동 포트 이동 안 함.
  · 별/은하수를 배경으로 유지 → 최소한 검은 화면은 안 남(개체 렌더 여부만 판정).
★ 만약 이 경로로도 안 뜨면 = NGC 빌보드 아트가 이 빌드에 없음 → NGC 클래스는 접고 Clock/Chart2D 로.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

CENTER_TH = 90.0                       # 딥스카이 LOS 프레임 돔 중앙
RAMP = [0.6] * 8                       # 적응형 지오메트릭 줌(9스텝 근사) — 돔 가득

# DB 핸들 후보 (타입, 이름) — ★ v3: NebulaType 우선(액션 살아있음). NgcType 은 핸들만 나오고 .action()=None(v2 로그로 확정).
DB_CANDIDATES = [
    ("NebulaType", "NGC 2237"), ("NebulaType", "NGC2237"),
    ("NebulaType", "Rosette"), ("NebulaType", "Rosette Nebula"),
    ("NebulaType", "Caldwell 49"), ("NebulaType", "C49"),
    ("NgcType", "NGC 2237"), ("NgcType", "NGC2237"), ("NgcType", "Rosette"),
    ("AsterismType", "NGC 2237"), ("DeepSkyObjectType", "NGC 2237"),
]
# ★ 핸들이 아니라 '쓸 수 있는 액션이 있는 핸들'을 고른다(v2 버그: NgcType 핸들 잡고 액션 죽어 종료).
NAV_ACTIONS = ("ConnectTo", "FadeTo", "GoTo")


def get_handle():
    """핸들 존재만이 아니라 '살아있는 nav 액션'이 있는 후보를 고른다. 각 후보의 액션 지원을 로그로 덤프."""
    db = DataManager.database()
    for tname, name in DB_CANDIDATES:
        if not hasattr(Data.Type, tname):
            continue
        try:
            h = db.data(getattr(Data.Type, tname), name)
        except Exception as e:
            print("   data(%s,%s) 예외: %s" % (tname, name, e)); continue
        if h is None:
            print("   – %s/'%s' 핸들 없음" % (tname, name)); continue
        avail = []
        for an in NAV_ACTIONS:
            try:
                if h.action(getattr(Action.Type, an)) is not None:
                    avail.append(an)
            except Exception:
                pass
        print("   · %s/'%s' 핸들 O, 액션=%s" % (tname, name, avail or "없음(死)"))
        if avail:
            print("   ✓✓ 채택 = %s / '%s' (액션 %s)" % (tname, name, avail))
            return h, tname, name, avail[0]
    return None, None, None, None


# ── 무대: 지상 밤 (별/은하수 배경 = 항상 보임) ──────────────
print("무대: NGC 장미 성운 v3 (DB, 액션 살아있는 핸들만 채택)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
cam.setTargetHeight(30.0, Anim(0.0)); cam.setOrientationH(0.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 42, 0)); txt.setSize(0.045); txt.setColor(Vec(1.0, 0.7, 0.8))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0)); sleep(3.2)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("NGC 2237 — 장미 성운 (Rosette Nebula)", 4.0)
narr("외뿔소자리, 5200광년 밖 — 지름 130광년의 붉은 꽃", 4.5)

# ── DB 핸들(액션 살아있는 것) → 진입 ────────────────────────
h, tname, name, nav = get_handle()
if h is None:
    narr("⚠️ 장미 성운 = 액션 살아있는 DB 핸들 없음 — 로그 확인", 5.0)
    print("   ★ 모든 후보에서 nav 액션 死 → NGC 는 이 빌드 DB 로 접근 불가 확정 → Clock 으로 넘어감")
else:
    # ① 암전(진입 내부 자세슬루 숨김)
    uni.setGlobalIntensity(0.0, Anim.cubic(1.5)); sleep(1.7)
    # ② 진입 (get_handle 이 고른 살아있는 액션)
    ct = h.action(getattr(Action.Type, nav))
    if ct is None:
        uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
        narr("⚠️ 진입 액션 재조회 None — 로그 확인", 5.0)
    else:
        ct.trigger(); print("   진입 = %s" % nav); sleep(6.5)
        # ②-b 배경 은하수만 낮춰 잡음 제거(별은 유지)
        try: Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.15, Anim(1.5))
        except Exception: pass
        # 타깃 강조(NGC 클래스로 intensity/label)
        try:
            ngc = NGC(NGC.NGCName.NGC2237)
            ngc.setIntensity(1.0, Anim(1.0)); ngc.setLabelIntensity(1.0, Anim(1.0))
        except Exception as e:
            print("   NGC intensity/label 실패: %s" % e)
        # ③ Target 센터
        cam.setTargetHeight(CENTER_TH, Anim.cubic(2.5)); sleep(2.7)
        try: R = cam.positionLBR.z
        except Exception: R = 0.0
        print("   진입 후 R = %.3e" % R)
        # ④ 페이드인(개체 등장)
        uni.setGlobalIntensity(1.0, Anim.cubic(2.6)); sleep(2.8)
        narr("그 붉은 꽃 한가운데로 들어간다", 3.5)
        # ⑤ 접근 — 절대타겟 지오메트릭 줌(겹쳐 재생=매끄러움)
        if R > 1.0:
            try:
                r = cam.positionLBR.z; targets = []
                for ratio in RAMP:
                    r *= ratio; targets.append(r)
                for i, tgt in enumerate(targets):
                    dur = 2.2 if i == 0 else 1.6
                    cam.setPositionR(tgt, Anim(dur), -1); sleep(dur * 0.6)
                sleep(1.5)
                print("   접근 완료 R=%.3e (목표=%.3e)" % (cam.positionLBR.z, targets[-1]))
            except Exception as e:
                print("   접근 실패: %s" % e)
        else:
            print("   R≈0 도킹 → setScale 폴백")
            try: NGC(NGC.NGCName.NGC2237).setScale(80.0, Anim.cubic(7.0)); sleep(7.5)
            except Exception as e: print("   setScale 실패: %s" % e)
        narr("중심의 젊은 별들이 뿜는 바람이 가스를 밀어 구멍을 냈다", 4.5)
        narr("NGC 2237 — 장미 성운", 4.0)

# ── 정리 ────────────────────────────────────────────────────
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료(v3 액션테스트). 리포트: ①★이번엔 장미 성운이 화면 중앙에 뜨나 (v2 버그=NgcType 액션死 핸들 잘못 채택, 이번엔 살아있는 액션만 채택) "
      "②로그 '·(후보)/액션=' 줄들 + '✓✓ 채택' + '진입=' + '진입 후 R' 값 붙여줘 "
      "③여전히 개체가 안 뜨면 = NGC 빌보드 아트가 이 빌드에 없음 → NGC 접고 Clock 클래스로 넘어감(확실한 HUD 렌더)")

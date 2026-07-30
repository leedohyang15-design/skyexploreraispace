# -*- coding: utf-8 -*-
# NGC 여행(접근) 재도전 — 장미성운 NGC2237
# 옛 실패의 두 원인 가설:
#   ① nav 액션을 3개(ConnectTo/FadeTo/GoTo)만 테스트했음 → Action.Type '전체' 스캔한다.
#   ② LOS 포트 카메라 이동 시 R 이 너무 작아 '대상을 통과' → 검은 화면+자막만 남았음
#      (메시에 LOS 는 R 이 1e15 급! 우리가 작은 값 줬던 게 문제)
#      → R 을 초대형에서 시작해 지오메트릭으로 줄이며 매 단계 R 을 로그로 찍는다.
from skyExplorer import *
from studio import *
from Initialization import *

TARGET_ENUM = "NGC2237"            # 장미성운
NAMES = ["NGC 2237", "NGC2237", "Rosette", "Rosette Nebula", "Caldwell 49"]
TYPES = ["NgcType", "NebulaType", "DeepSkyObjectType", "MessierType", "AsterismType", "GalaxyType"]

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 겨울 지상 밤 (장미성운은 겨울 외뿔소자리) ─────────────────────
try: SceneGraph().reset(1); sleep(1.5)
except Exception: pass
uni.setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))

ngc = NGC(getattr(NGC.NGCName, TARGET_ENUM))
ngc.setIntensity(1.0, Anim(0.0))
try: ngc.setLabelIntensity(1.0, Anim(0.0))
except Exception: pass
sleep(2.0)
print("장미성운 제자리 ON (지상서 확인) — id=%s" % getattr(ngc, "id", "?"))


def R():
    try: return cam.positionLBR.z
    except Exception: return None


# ═══ A) Action.Type '전체' 스캔 — 살아있는 액션 찾기 (옛날엔 3개만 봤음) ═══
print("\n===== A) 살아있는 DB 액션 전수 스캔 =====")
all_actions = [a for a in dir(Action.Type) if not a.startswith("_") and a[0].isupper()]
print("Action.Type 멤버 %d개 스캔" % len(all_actions))
alive = []          # (타입, 이름, 액션명, 액션객체)
db = DataManager.database()
for tn in TYPES:
    dt = getattr(Data.Type, tn, None)
    if dt is None: continue
    for nm in NAMES:
        try: h = db.data(dt, nm)
        except Exception: continue
        if h is None: continue
        got = []
        for an in all_actions:
            try:
                if h.action(getattr(Action.Type, an)) is not None:
                    got.append(an)
            except Exception:
                pass
        if got:
            print("  ★ %s / '%s' → 살아있는 액션 %d개: %s" % (tn, nm, len(got), got))
            for an in got:
                alive.append((tn, nm, an, h))
        else:
            print("  – %s / '%s' 핸들O, 살아있는 액션 없음" % (tn, nm))

# 이동에 쓸 만한 액션 우선순위
NAV_PREF = ["GoTo", "StraightGoTo", "ConnectTo", "FadeTo", "GoToPlace", "FadeToPlace", "LookAt", "ScaleUp"]
picked = None
for pref in NAV_PREF:
    for (tn, nm, an, h) in alive:
        if an == pref:
            picked = (tn, nm, an, h); break
    if picked: break

if picked:
    tn, nm, an, h = picked
    print("\n>>> 채택: %s / '%s' → %s 실행" % (tn, nm, an))
    print("    실행 전 R = %s" % R())
    h.action(getattr(Action.Type, an)).trigger()
    for i in range(8):                       # 최대 24초 관찰(비행형이면 R 이 계속 변함)
        sleep(3.0); print("    +%2ds  R = %s" % ((i+1)*3, R()))
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    print("    도착 R = %s  → 화면에 장미성운이 크게 보이나?" % R())
else:
    print("\n>>> 살아있는 nav 액션 없음 → B 경로(LOS 포트 수동 접근)로")

# ═══ B) LOS 포트 수동 접근 — ★R 을 '초대형'에서 시작 (옛 실패: R 이 작아 통과) ═══
print("\n===== B) LOS 포트 접근 (R 초대형→지오메트릭 축소) =====")
port = None
for pn in ["LineOfSightLocal", "Ecliptic"]:
    try:
        port = ngc.portId(getattr(NGC.NGCPort, pn))
        print("포트 확보: NGCPort.%s → id=%s" % (pn, port)); break
    except Exception as e:
        print("포트 %s 실패: %s" % (pn, e))

if port is not None:
    # ★ 메시에 LOS 는 R 이 1e15 급 → 초대형에서 출발해 단계적으로 줄인다.
    for r in [1e15, 1e14, 1e13, 1e12, 1e11, 1e10]:
        cam.setPositionLBR(Vec(0.0, 0.0, r), Anim(2.0), port)
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(2.0), port)   # 시선 정렬(필수)
        sleep(2.5)
        print("  R 지정 %.0e → 실제 R = %s   (별/성운 보이나?)" % (r, R()))
    cam.setTargetHeight(90.0, Anim(1.5)); sleep(2.0)   # 성운 LOS 프레임은 90=돔 중앙
    print("  TargetHeight 90 (성운 프레임 중앙) 적용")
    print("\n  >>> 여기서 장미성운이 화면에 크게 보이면 = B 경로 성공!")
    print("      어느 R 에서 보이기 시작했는지 알려주세요(그 값이 정답 스케일).")

print("\n===== 결과 보고 요청 =====")
print("① A 스캔에서 '★ 살아있는 액션' 이 나왔나 (나왔으면 그 목록)")
print("② A 실행 시 화면이 장미성운으로 접근했나")
print("③ B 에서 어느 R 값부터 성운/별이 보였나 (또는 계속 검은 화면인가)")

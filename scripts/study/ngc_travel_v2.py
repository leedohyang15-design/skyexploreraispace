# -*- coding: utf-8 -*-
# NGC 여행 v2 — ★전수 스캔으로 밝혀진 정답 경로: LookAt(조준) + ScaleUp(확대)
#
# v1 로그로 확정된 사실:
#   · NGC 살아있는 액션 13개 = LabelOn/Off, LookAt, On/Off, Properties, ScaleUp/Down/UpDown, Tag/Untag
#     → GoTo·FadeTo·ConnectTo·StraightGoTo·GoToPlace·FadeToPlace **전부 없음(확정 死)**
#   · LOS 포트 카메라 이동도 死 (R 37,156,789 에서 1e15~1e10 다 무시하고 안 변함)
#   · 그래서 '접근'은 카메라 이동이 아니라 **개체를 키우는 것(ScaleUp)** 으로 구현한다.
#
# ScaleUp 은 DB 액션이라 '한 번 = 한 단계' → 여러 번 trigger 해서 점점 크게.
from skyExplorer import *
from studio import *
from Initialization import *

STEPS = 8          # ScaleUp 반복 횟수(단계). 너무 크면 화면 넘칠 수 있음 → 로그 보며 조절
HOLD  = 1.2        # 단계 간 대기(초)

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# ── 무대: 겨울 지상 밤 (장미성운 = 겨울 외뿔소자리) ──────────────────────
try: SceneGraph().reset(1); sleep(1.6)
except Exception: pass
uni.setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0)); earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))

# 성운 켜기 + 라벨
ngc = NGC(NGC.NGCName.NGC2237)
ngc.setIntensity(1.0, Anim(1.0))
try: ngc.setLabelIntensity(1.0, Anim(1.0))
except Exception: pass
sleep(2.0)

# DB 핸들 (NgcType / 'NGC 2237' 이 유일하게 유효 — v1 로그 확정)
h = DataManager.database().data(Data.Type.NgcType, "NGC 2237")
if h is None:
    print("⚠️ 핸들 없음 — 중단"); raise SystemExit

def fire(name):
    """액션 하나 트리거. 살아있으면 True"""
    a = getattr(Action.Type, name, None)
    if a is None: return False
    try: act = h.action(a)
    except Exception: return False
    if act is None:
        print("   ✗ %s = None" % name); return False
    act.trigger(); return True

# ── ① LookAt = 조준 (성운을 화면 중앙으로) ─────────────────────────────
print("\n① LookAt — 성운 조준")
if fire("LookAt"):
    sleep(5.0)                              # 내부 조준 슬루 대기
    cam.setTargetHeight(30.0, Anim(1.5))    # 관람 정위치
    sleep(2.0)
    print("   조준 완료 — 장미성운이 화면 중앙(Target 30)에 왔나?")
else:
    print("   LookAt 실패")

# ── ② ScaleUp 반복 = '접근' (카메라 이동이 아니라 개체를 키움) ──────────
print("\n② ScaleUp %d단계 — 성운을 점점 크게 (이게 NGC 의 '줌인')" % STEPS)
for i in range(STEPS):
    ok = fire("ScaleUp")
    sleep(HOLD)
    print("   ScaleUp %d/%d %s" % (i + 1, STEPS, "OK" if ok else "실패"))
print("   >>> 단계가 올라갈수록 성운이 커졌나? 어느 단계쯤이 보기 좋았나?")
sleep(3.0)

# ── ③ 되돌리기 = ScaleDown 같은 횟수 (다음 쇼 대비) ────────────────────
print("\n③ ScaleDown %d단계 — 원래대로" % STEPS)
for i in range(STEPS):
    fire("ScaleDown"); sleep(0.6)
print("   복귀 완료")

print("\n===== 보고 =====")
print("① LookAt 으로 성운이 중앙에 왔나")
print("② ScaleUp 을 반복하니 성운이 실제로 커졌나 (커졌다면 몇 단계가 적당?)")
print("③ ScaleDown 으로 원복됐나")

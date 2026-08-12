# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 규칙 검사는 통과했으나 돔에서 본 기록이 없다. 기하(프레임·L/B·R 단위)는 정적 검사로 안 잡히니 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ═══ [정답 예제 3] 장미성운 (NGC 패널 = 여행 불가, LookAt + ScaleUp) ═══
# 대응 프롬프트: "겨울 외뿔소자리의 장미성운을 보여줘"
#
# '딥스카이 접근 3단' 중 ③번 경로:
#   NGC 패널 개체(NgcType)는 **이동 액션이 아예 없다**(GoTo/FadeTo/ConnectTo 전부 None,
#   Action.Type 68개 전수 스캔 확정). 살아있는 액션 13개 중 쓸 것은:
#     · LookAt   = 조준(성운을 화면 중앙으로)
#     · ScaleUp  = 확대 (1회 = 1단계 → 반복 트리거). NGC 는 setScale/scale 속성이 없음
#   → 카메라로 다가가는 게 아니라 '개체를 키워서' 접근 느낌을 낸다.
from skyExplorer import *
from studio import *
from Initialization import *
def _dark(sec=0.0):
    """암전 '유지' — reset/FadeTo/무거운 세팅은 밝기를 1.0 으로 되돌린다.
       ⚠️ setGlobalIntensity(0) 을 **한 번만** 걸면 소용없다(2026-08-12 실측: 그래서
          세팅 구간이 그대로 보였다). 이 함수를 세팅 단계마다 끼워 넣어 계속 눌러준다."""
    u = Universe(Universe.UniverseName.MainUniverse)
    for _ in range(max(int(sec / 0.2), 1)):
        u.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)

SCALE_STEPS = 6          # ScaleUp 반복 횟수(크기 조절용)

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 겨울 지상 밤하늘 (장미성운 = 외뿔소자리, 겨울) ────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
SceneGraph().reset(1); _dark(1.5)
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
_dark()
cam.setOrientationH(30.0, Anim(0.0))         # 남동쪽(외뿔소자리)
_dark()
cam.setTargetHeight(30.0, Anim(0.0))
_dark()
sleep(1.5)

# ★ 세팅이 전부 끝난 뒤에야 페이드인 — 관측지·시각·조준을 불 켠 채로 하면
#   그 조정 과정이 관객에게 그대로 보인다(돔 실측: "쇼마다 카메라를 자꾸 조정하는 게 보인다").
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.2)
# 옆 별자리(오리온)로 위치 감 잡아주기
Constellation(Constellation.ConstellationName.Ori).setLinesIntensity(0.6, Anim(1.5))
sleep(2.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("오리온 옆, 외뿔소자리의 장미성운"); t1.setIntensity(1.0, Anim(1.0))
sleep(3.0)

# ── ① 성운 제자리 ON (NGC 는 이렇게만 켜진다) ────────────────
ngc = NGC(NGC.NGCName.NGC2237)
ngc.setIntensity(1.0, Anim(2.0))
ngc.setLabelIntensity(1.0, Anim(2.0))        # ⚠️ NGC 엔 포인터/scale 속성 없음
sleep(3.0)

# ── ② LookAt = 조준 (카메라가 성운을 화면 중앙으로) ──────────
h = DataManager.database().data(Data.Type.NgcType, "NGC 2237")   # ⚠️ 이름은 공백 포함
h.action(Action.Type.LookAt).trigger()
sleep(5.0)                                   # 내부 조준 슬루 대기
cam.setTargetHeight(30.0, Anim(1.5))         # 관람 정위치
sleep(2.0)

t1.setText("1천 광년 밖, 장미 모양의 성운"); sleep(3.0)

# ── ③ ScaleUp 반복 = '접근' (카메라 이동이 아니라 개체를 키움) ─
for i in range(SCALE_STEPS):
    h.action(Action.Type.ScaleUp).trigger()
    sleep(1.2)
sleep(3.0)

t1.setText("성운 한가운데엔 갓 태어난 별들이 있다"); sleep(5.0)

# ── ④ 원복 (다음 쇼 대비) ────────────────────────────────────
for i in range(SCALE_STEPS):
    h.action(Action.Type.ScaleDown).trigger()
    sleep(0.6)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

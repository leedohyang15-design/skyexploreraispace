# -*- coding: utf-8 -*-
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

SCALE_STEPS = 6          # ScaleUp 반복 횟수(크기 조절용)

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 겨울 지상 밤하늘 (장미성운 = 외뿔소자리, 겨울) ────────────
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(30.0, Anim(0.0))         # 남동쪽(외뿔소자리)
cam.setTargetHeight(30.0, Anim(0.0))
sleep(1.5)

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

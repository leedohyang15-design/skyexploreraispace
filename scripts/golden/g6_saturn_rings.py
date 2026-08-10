# -*- coding: utf-8 -*-
# ═══ [정답 예제 6] 토성 고리 크게 보여주기 ═══
# 대응 프롬프트: "토성 고리를 크고 잘 보이게 보여줘"
#
# 오늘 '死→승격'시킨 항목: 고리는 세터가 아니라 **구도**가 8할이었다.
#   옛 결론('setRingModel 차이 미미 → 고리 연출 부적합')은 구도가 나빴던 것.
#   ✅ 확정 레시피 = ① 그림자 OFF 3세터  ② **고리면 크게 개방(B=75)**
#                    ③ **R 은 FadeTo 도킹값(≈5) 그대로 — 줌 금지**
#                    ④ 배경 검정(Stars 0) → 대비 확보
#   ⚠️⚠️ [2026-08-03 정정] 옛 ③은 '근접(R≥3.2)'이었는데 **틀렸다**.
#      A고리 바깥지름 = 2.27 토성반지름(옛 노트의 '4.6'이 오기였음) →
#      R=5 → 고리 시직경 54°(적당) / R=3.9 → 72°(이미 잘림, 실측 스샷) / R=1.7 → 180°(삼켜짐).
#      **고리는 다가가면 오히려 안 보인다. 구도(B 개방)가 8할.**
#   ⚠️ setRingModel(모델 교체) 자체는 여전히 차이 미미 → '고리 룩 바꾸기' 연출은 하지 말 것.
#   ⚠️ 가스행성은 도킹이 이미 옆(B≈20)이라 B 를 '열어주는' 조정은 필요(암석행성과 다름).
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 배경 검정(고리 대비 확보) ────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
dm.stop(); sleep(0.3)

# ── 토성 도킹 ────────────────────────────────────────────────
DataManager.database().data(Data.Type.PlanetType, "Saturn") \
    .action(Action.Type.FadeTo).trigger()
sleep(5.0)

sat = Planet(Planet.PlanetName.Saturn)

# ── ① 그림자 OFF 3세터 (터미네이터로 반쪽 어두워지는 것 방지) ─
sat.setShadowStrength(0.0, Anim(1.0))
sat.setShadowContrast(0.0, Anim(1.0))
sat.setPlanetShineStrength(1.0, Anim(1.0))
sleep(1.5)

# ── ②③ 고리면 개방(B=75) + 근접(R≥3.2) ★이게 핵심 ───────────
p = cam.positionLBR
# ⚠️ [2026-08-03 정정] 예전엔 R×0.7(=3.5)로 당겼다. 그건 고리를 잘라먹는다 → R 은 도킹값 그대로.
cam.setPositionLBR(Vec(p.x, 75.0, p.z), Anim.cubic(5.0), -1)
sleep(5.5)
cam.setTargetHeight(30.0, Anim.cubic(1.5))    # 관람 표준
sleep(2.0)

# ── 자막 ─────────────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0))
t1.setDistance(20.0, Anim(0.0))               # ⚠️ 행성 프레임 자막 = distance 20, setSize 금지
t1.setColor(Vec(1.0, 1.0, 0.55))
t1.setText("토성의 고리 — 얼음과 바위의 띠"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)

# ── 천천히 한 바퀴 (L 스윕 = 가스행성은 옆 도킹이라 자연스러움) ─
t1.setText("고리는 수천 개의 가느다란 띠로 이루어져 있다")
base_l = cam.positionLBR.x
for d in (60.0, 120.0, 180.0):
    q = cam.positionLBR
    cam.setPositionLBR(Vec(base_l + d, q.y, q.z), Anim(4.0), -1)
    sleep(3.6)                                 # sleep < anim = 겹쳐서 매끄럽게
sleep(2.0)

t1.setText("가장 큰 얼음덩이도 집 한 채 크기"); sleep(5.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

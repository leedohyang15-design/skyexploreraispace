# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인 (2026-08-10) — L 스윕이 재조준 없이 토성을 계속 중앙에 유지함을 확인, 고리 시직경 R=5/3.9/1.7 은 스샷 실측. 도킹 폴링 교체분은 미확인
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

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
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
dm.stop(); sleep(0.3)

# ── 토성 도킹 ────────────────────────────────────────────────
DataManager.database().data(Data.Type.PlanetType, "Saturn") \
    .action(Action.Type.FadeTo).trigger()


def wait_dock(max_s=16.0):
    """⚠️ 고정 sleep 으로 도킹을 기다리지 마라 — 도킹 애니가 R 을 계속 끌어당긴다.
       천왕성 실측: 6초 뒤에도 R 이 653,188 → 163,773 km 로 계속 수렴 중이었다.
       그 상태에서 `cam.positionLBR` 을 읽으면 **수렴 중인 먼 값이 그대로 고정**돼
       행성이 의도보다 작게 잡힌다. → R 이 멈춘 뒤에 읽는다."""
    prev, stable, t = None, 0, 0.0
    while t < max_s:
        cur = None
        try:
            cur = cam.positionLBR.z
        except Exception:
            pass
        if cur is not None and prev is not None and abs(cur - prev) < 1e-4 * max(1.0, abs(cur)):
            stable += 1
            if stable >= 4:
                break
        else:
            stable = 0
        prev = cur
        sleep(0.25); t += 0.25
    print("도킹 안정화, R =", prev)


wait_dock()

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
# ✅ [2026-08-10 사용자 돔 확인] 이 스윕은 **재조준 없이도 토성이 계속 중앙**에 있었다.
#    → track=-1 공전은 재조준 불필요(포트 프레임 공전과 다름). 달·성운은 반드시 재조준.
t1.setText("고리는 수천 개의 가느다란 띠로 이루어져 있다")
base_l = cam.positionLBR.x
for d in (60.0, 120.0, 180.0):
    q = cam.positionLBR
    cam.setPositionLBR(Vec(base_l + d, q.y, q.z), Anim(4.0), -1)
    sleep(3.6)                                 # sleep < anim = 겹쳐서 매끄럽게
sleep(2.0)

t1.setText("가장 큰 얼음덩이도 집 한 채 크기"); sleep(5.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

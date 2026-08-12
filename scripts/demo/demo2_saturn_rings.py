# -*- coding: utf-8 -*-
# ═══ [시연 폴백 2] 토성의 고리 — 한 바퀴 돌며 보기 (약 62초) ═══
#
# ⚠️⚠️ **이 파일은 v1(AI 생성 원본)을 사람이 고친 것이다.** 원본은 `_demo2_v1_as_generated.py` 에 보존.
#   2026-08-12 돔 실측에서 v1 이 두 군데 깨졌다("회전이 뚝뚝 끊기고, 처음에 토성이 보였다 사라진다"):
#     ① **공전 끊김** — `sleep(0.95) > Anim(0.9)` 로 스텝마다 멈추고, 재조준 뒤 `sleep(0.3)` 로 또 멈췄다.
#        → 규칙은 **`sleep < anim`(겹쳐야 매끄럽다)**. 게다가 토성 공전은 **`track=-1` 이면 재조준 자체가 불필요**
#          (g6_saturn_rings 에서 사용자 확인: "재조준 없이도 계속 중앙"). 재조준을 빼니 멈출 이유가 사라진다.
#     ② **시작하자마자 토성이 보였다 사라짐** — `reset(1)` 뒤 1초간 화면이 **켜진 상태**라 이전 장면이 노출됐다.
#        → **암전을 reset 보다 먼저** 걸고 그 구간 내내 클램프한다.
#
#   ⚠️ 교훈: v1 은 정적 규칙 검사를 7/7 통과했고 오늘 추가한 검사도 통과했다.
#      **검사 통과 ≠ 돔에서 돌아감.** 시연 폴백 카드는 반드시 돔에서 한 번 돌려보고 등록할 것.
#
# 시연 배치: 라이브 생성이 늦거나 실패했을 때 바로 재생하는 카드.
from skyExplorer import *
from studio import *
from Initialization import *

uni = Universe(Universe.UniverseName.MainUniverse)
cam = Camera(Camera.CameraName.MainCamera)
saturn = Planet(Planet.PlanetName.Saturn)


def clamp_dark(seconds):
    """암전을 '유지'한다 — reset/FadeTo 는 밝기를 1.0 으로 되돌리므로 계속 눌러야 한다."""
    for _ in range(max(int(seconds / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)


# ── 씬1 [암전 먼저, 그 다음 리셋] ────────────────────────────
#   ⚠️ v1 은 reset 을 먼저 하고 1초 잔 뒤에 껐다 → 그 1초 동안 이전 장면(토성)이 그대로 보였다.
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1)
except Exception:
    pass
clamp_dark(1.6)                                # reset 이 밝기를 되돌리므로 눌러둔 채로 대기

saturn.setIntensity(1.0, Anim(0.0))
clamp_dark(0.6)

# ── 씬2 [토성 도킹 + 고리면 개방] ────────────────────────────
try:
    DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
    clamp_dark(6.0)                            # 내부 방향정렬 슬루가 끝날 때까지

    saturn.setShadowStrength(0.0, Anim(0.0))
    saturn.setShadowContrast(0.0, Anim(0.0))
    saturn.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    # ★ 고리는 '구도'가 8할 — B 만 75 로 열고 R(도킹값 ≈5)은 그대로.
    #   줌을 넣으면 고리 바깥지름(A고리 2.27 토성반지름)이 화면 밖으로 잘린다.
    #   ⚠️ 여기서부터 끝까지 **track=-1 한 프레임만** 쓴다(포트와 섞지 않는다).
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 75.0, p.z), Anim.cubic(3.0), -1)
    cam.setTargetHeight(30.0, Anim(3.0))       # 관람 표준
    sleep(3.4)

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))   # 정렬이 끝난 뒤에야 페이드인
    sleep(2.6)
except Exception as e:
    print("씬2 오류:", e)

# ── 씬3 [자막] ───────────────────────────────────────────────
t = None
try:
    t = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 12, 0))
    t.setColor(Vec(1.0, 0.95, 0.6))
    t.setDistance(20.0, Anim(0.0))             # 행성 프레임 자막 표준
    t.setText("토성의 고리")
    t.setIntensity(1.0, Anim(1.5))
    sleep(3.5)
    t.setText("얼음과 바위 조각이 만든 띠")
    sleep(4.0)
except Exception as e:
    print("씬3 오류:", e)

# ── 씬4 [한 바퀴 공전] ───────────────────────────────────────
#   ⚠️ 매끄러움의 조건 두 개:
#     ① **sleep < anim** — 다음 스텝이 이전 애니가 끝나기 전에 들어가야 이어진다(v1 은 반대였다).
#     ② **재조준을 넣지 않는다** — `track=-1` 공전은 대상이 알아서 중앙을 지킨다(사용자 돔 확인).
#        포트 프레임 공전(달·성운)에서만 재조준이 필요하고, 거기서도 sleep 을 추가로 넣으면 안 된다.
try:
    base_l = cam.positionLBR.x
    for i in range(1, 25):                     # 24 × 15° = 360°
        q = cam.positionLBR
        cam.setPositionLBR(Vec(base_l + 15.0 * i, q.y, q.z), Anim(1.1), -1)
        sleep(0.85)                            # ★ sleep < anim = 겹쳐서 매끄럽게
        if i == 8:
            t and t.setText("수천 개의 가느다란 띠로 이루어져 있다")
        elif i == 16:
            t and t.setText("가장 큰 얼음덩이도 집 한 채 크기")
except Exception as e:
    print("씬4 오류:", e)

# ── 씬5 [마무리] ─────────────────────────────────────────────
try:
    sleep(1.5)
    if t:
        t.setText("토성 — 태양계에서 가장 큰 고리")
        sleep(4.0)
        t.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("씬5 오류:", e)

print("쇼 종료 — 토성의 고리 (시연 폴백 2)")

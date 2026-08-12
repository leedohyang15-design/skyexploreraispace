# -*- coding: utf-8 -*-
# ═══ [보존본] demo2 v1 — AI 가 생성한 원본 그대로 (실행용 아님) ═══
#
# ⚠️ 2026-08-12 돔 실측에서 **두 가지가 깨졌다** — 그래서 실행 카드는 demo2_saturn_rings.py 로 교체됐다.
#   ① 공전이 뚝뚝 끊김: `sleep(0.95) > Anim(0.9)` (규칙은 sleep < anim) + 재조준마다 `sleep(0.3)` 추가 정지.
#   ② 시작하자마자 토성이 보였다 사라짐: `reset(1)` 뒤 1초간 화면이 켜진 상태로 이전 장면이 노출.
#
# 이 파일은 '규칙 검사만 통과한 코드가 돔에서는 깨질 수 있다'는 증거로 남긴다.
# 정적 검사 7/7 통과 + 새 검사도 통과했지만, 실제로는 못 쓸 물건이었다.
# ═══ [원본 헤더] 토성의 고리 — 한 바퀴 돌며 보기 (약 65초) ═══
#
# ⚠️ 이 파일도 **Sky Explorer AI 가 생성한 결과물 그대로**다(사람이 손댄 곳 없음).
#    프롬프트: "토성의 고리를 제대로 보여주는 쇼를 만들어줘.
#               고리가 잘 보이는 각도로 자세를 잡고, 토성 주위를 한 바퀴 돌면서 보여줘."
#    2026-08-10 규칙 검사 7/7 통과 (줌 금지·B75 개방·암전·재조준·Target 30·그림자 OFF·배경 정리).
#
# 시연 배치: 라이브 생성이 늦거나 실패했을 때 바로 재생하는 카드.
#   ⏱ 약 65초 — 3분 대본의 '돔 재생' 슬롯에 맞춰 설계됨.
from skyExplorer import *
from studio import *
from Initialization import *

# ── 씬1 [초기 세팅] 암전 ─────────────────────────────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
try:
    SceneGraph().reset(1)
except Exception:
    pass
sleep(1.0)

uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))

cam = Camera(Camera.CameraName.MainCamera)
saturn = Planet(Planet.PlanetName.Saturn)
saturn.setIntensity(1.0, Anim(0.0))
sleep(2.0)

# ── 씬2 [토성 도킹 + 고리면 개방] ────────────────────────────
try:
    DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
    # ★ 암전 클램프 — FadeTo 가 밝기를 1.0 으로 되돌리므로 계속 눌러줘야 한다
    for _ in range(30):                       # 약 6초, 내부 방향정렬 슬루가 끝날 때까지
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # 표면 디테일 확보 + 배경 정리
    saturn.setShadowStrength(0.0, Anim(0.0))
    saturn.setShadowContrast(0.0, Anim(0.0))
    saturn.setPlanetShineStrength(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))

    sp = saturn.portId(Planet.PlanetPort.EquatorialSynchronous)
    p = cam.positionLBR

    # ★ 고리는 '구도'가 8할 — B 만 75 로 열고 R(도킹값 ≈5)은 그대로.
    #   줌을 넣으면 고리 바깥지름이 화면 밖으로 잘린다(A고리 = 2.27 토성반지름).
    cam.setPositionLBR(Vec(p.x, 75.0, p.z), Anim.cubic(3.0), sp)
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(3.0), sp)
    cam.setTargetHeight(30.0, Anim(3.0))      # 관람 표준
    sleep(3.2)

    uni.setGlobalIntensity(1.0, Anim.cubic(2.5))   # 정렬이 끝난 뒤에야 페이드인
    sleep(2.8)
except Exception as e:
    print("씬2 오류:", e)

# ── 씬3 [자막] ───────────────────────────────────────────────
t = None
try:
    t = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 12, 0))
    t.setColor(Vec(1.0, 0.95, 0.6))
    t.setDistance(20.0, Anim(0.0))            # 행성 프레임 자막 표준
    t.setText("토성의 고리\n얼음과 바위 조각이 만든 띠")
    t.setIntensity(1.0, Anim(2.0))
    sleep(9.0)
except Exception as e:
    print("씬3 오류:", e)

# ── 씬4 [한 바퀴 공전] ───────────────────────────────────────
try:
    sp = saturn.portId(Planet.PlanetPort.EquatorialSynchronous)
    p = cam.positionLBR
    for i in range(1, 25):                    # 24 × 15° = 360°
        cam.setPositionLBR(Vec(p.x + 15.0 * i, p.y, p.z), Anim(0.9), sp)
        sleep(0.95)
        if i % 3 == 0:                        # 포트 프레임 공전이므로 재조준 필요
            cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(0.3), sp)
            sleep(0.3)
except Exception as e:
    print("씬4 오류:", e)

# ── 씬5 [마무리] ─────────────────────────────────────────────
try:
    cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(2.0), sp)
    sleep(3.0)
    if t:
        t.setIntensity(0.0, Anim(2.0))
    sleep(2.5)
except Exception as e:
    print("씬5 오류:", e)

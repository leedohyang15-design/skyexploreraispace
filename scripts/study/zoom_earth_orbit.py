"""
zoom_earth_orbit.py — ✅ 확정 예제: 행성 화면 고정 + 돔 중앙 정렬 + 매개변수 줌
====================================================================
Studio 실측으로 검증된 것만 남긴 최종본 (2026-07-02, v1~v10 실험의 결론):

  ① goto_planet(name)   — FadeTo 로 행성에 화면 고정 (구체로 뜸)
  ② center_dome(cam)    — setTargetHeight(30, Anim(0)) → 🎯관람 정위치(운영 표준 30)
  ③ zoom(cam, scale, t) — '읽은 R × 배율' 상대 줌, track=-1 (절대값 금지!)

⚠️ 실험으로 확인된 한계 (하지 말 것 — 상세는 CLAUDE.md):
  · 이동 중 조준 유지 불가: setTargetHeight 는 일회성(같은 값 재호출 = no-op).
  · track=행성 portId → 포트마다 좌표축 달라 카메라 점프.
  · 카메라 L/B 이동 + 시간가속 조합의 '자전 연출'은 v7~v10 모두 실패 — 미해결 과제.
    (프로덕션 planet_earth.SPC 도 시간 가속 없이 정지 구도 + 미세 드리프트만 씀.)
"""
from skyExplorer import *
from studio import *
from Initialization import *


# ═════════════════════════════════════════════════════════════════
# 검증된 3종 부품 (매개변수화)
# ═════════════════════════════════════════════════════════════════
def goto_planet(name, wait=4.0):
    """① FadeTo — 행성에 화면 고정. name: 'Earth', 'Saturn', 'Jupiter' …"""
    DataManager.database().data(Data.Type.PlanetType, name) \
               .action(Action.Type.FadeTo).trigger()
    sleep(wait)                                  # 도착 대기 (R≈5 행성반지름에 프레이밍)


def center_dome(cam, height=30.0):
    """② 돔 정렬 — 🎯운영 표준 30(관람 정위치, FadeTo 기본과 동일). 90=천정(관람 부적합)."""
    cam.setTargetHeight(height, Anim(0.0))       # Anim(0) → 스윙 없이 즉시


def zoom(cam, scale, duration):
    """③ 상대 줌 — 현재 R × scale 로 접근/후퇴. scale<1 줌인, >1 줌아웃.
       R 단위는 '행성 반지름'이라 절대값 대신 반드시 배율로!
       ※ 2026-07-06 확정: 줌 자체는 화면 고정(달 실측 — R/스텝R/FOV 셋 다 OK).
         '화면 이동'의 정체는 FadeTo(하단 30°)→TH90 재정렬 슬루가 보이는 것
         → 정렬은 암전(GlobalIntensity 0)에서 끝내고 페이드인할 것."""
    p = cam.positionLBR
    cam.setPositionR(p.z * scale, Anim.cubic(duration), -1)
    sleep(duration + 0.5)
    return cam.positionLBR.z


# ═════════════════════════════════════════════════════════════════
# 데모: 지구를 돔 중앙에 띄우고 두 단계 줌인 (매개변수만 바꿔 재활용)
# ═════════════════════════════════════════════════════════════════
PLANET = "Earth"          # ← 'Saturn' 등으로 바꾸면 그대로 동작 (토성 실측 완료)

try:
    SceneGraph().reset(1)                        # 관측자 바인딩 해제(FadeTo 잠김 방지)
except Exception as e:
    print("reset skip:", repr(e)[:60])
sleep(1.0)

Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))

earth = Planet(Planet.PlanetName(2))
earth.setIntensity(1.0, Anim(1.0))
earth.setCloudsIntensity(0.6, Anim(1.0))
earth.setAtmosphereIntensity(1.0, Anim(1.0))

cam = Camera(Camera.CameraName.MainCamera)

goto_planet(PLANET)                              # ① 행성 고정
center_dome(cam)                                 # ② 돔 정중앙
sleep(1.0)

r1 = zoom(cam, scale=0.5, duration=6.0)          # ③ 줌인 2배
print(">>> 1차 줌 후 R=%.3f" % r1)
r2 = zoom(cam, scale=0.5, duration=6.0)          #    한 번 더 (누적 4배)
print(">>> 2차 줌 후 R=%.3f — 완료 ✅" % r2)

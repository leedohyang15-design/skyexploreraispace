"""
zoom_saturn.py — ✅ 검증 완료 (2026-07-02 실측): 행성 줌인 정석 레시피
====================================================================
Studio 실행 확인: FadeTo 로 토성 고정(고리·위성까지 뜸) → R 5.000 → 2.500 → 1.250
콘솔 실측 로그로 확정. 우리가 못 하던 '스크립트 행성 줌'의 첫 검증 예제.

★ 레시피 (어느 행성이든 동일):
  ① FadeTo               — 행성에 화면 고정 (Sky-View setTarget 잠김 우회)
  ② cam.positionLBR 읽기  — R 단위 = '트랙 대상 반지름' (km 아님! FadeTo 직후 R≈5)
  ③ setPositionLBR(Vec(p.x, p.y, p.z*배율), Anim.cubic(t), -1)
     · 절대값 금지 — 읽은 값 × 배율 (단위 몰라도 됨)
     · track=-1 = 현재 프레임 유지 (FadeTo 프레임 그대로) — 실측으로 동작 확인
     · track 인자는 필수 (생략하면 ArgumentError)

실패의 역사(교훈):
  v1 track만 걸고 안 감 → v2 절대값 130000 넣어 122AU 사고 → v3 track 생략 ArgumentError
  → v4 후보탐색에서 track=-1 이 첫 시도 성공 → 이 확정본.
"""
from skyExplorer import *
from studio import *
from Initialization import *


# ── 0) 관측자 바인딩 초기화 (FadeTo 잠김 방지) ──────────────
try:
    SceneGraph().reset(1)
except Exception as e:
    print("reset skip:", repr(e)[:60])
sleep(1.0)

# ── 1) 밝기 + 토성 켜기 ─────────────────────────────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
saturn = Planet(Planet.PlanetName(5))          # 5 = Saturn
saturn.setIntensity(1.0, Anim(1.0))

# ── 2) ① FadeTo — 토성에 화면 고정 ─────────────────────────
obj = DataManager.database().data(Data.Type.PlanetType, "Saturn")
obj.action(Action.Type.FadeTo).trigger()
sleep(4.0)                                      # 도착 대기 (R≈5 토성반지름에 프레이밍됨)

cam = Camera(Camera.CameraName.MainCamera)

# ── 3) ②③ 상대 줌: R×0.5 두 번 (5.0 → 2.5 → 1.25 = 4배 확대) ──
p = cam.positionLBR
print(">>> 시작 R=%.3f (토성반지름 단위)" % p.z)

cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.5), Anim.cubic(4.0), -1)   # track=-1: 현재 프레임 유지
sleep(4.5)

p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, p.y, p.z * 0.5), Anim.cubic(4.0), -1)
sleep(4.5)

print(">>> 최종 R=%.3f — 토성 줌인 완료 ✅" % cam.positionLBR.z)

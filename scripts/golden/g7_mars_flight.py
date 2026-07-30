# -*- coding: utf-8 -*-
# ═══ [정답 예제 7] 화성으로 '비행'해서 가기 (StraightGoTo + 도착 폴링) ═══
# 대응 프롬프트: "화성까지 날아가서 표면을 보여줘"
#
# ★ cam_30 로깅으로 확정된 StraightGoTo 의 실제 동작 (즉시 아님!):
#     +1s     프레임 전환 (R = 105,609 화성반지름 = 실제 2.4AU)
#     +1~9s   자세만 회전 (조준 슬루)
#     +10s    B=90 북극상공 자세로 재배치
#     +11~24s R 감소 = 실제 접근 비행 (105,608 → 12,448 → 9.48 → 5.00)
#     +25s~   R = 5.00 고정 = 도킹 완료
#
# ⚠️⚠️ **비행이 끝나기 전에 줌을 걸면 비행을 가로채 카메라가 태양계 한복판으로 날아간다.**
#      (sleep(4) 후 p0=105,609 를 읽어 나누면 2.6억km 지점으로 이동 → 태양만 보임)
# ✅ 정답 = **도착 폴링**: R 이 안정되고(변화 < 0.01) 도킹권(R < 100)에 들어올 때까지 기다린다.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def wait_arrival(max_sec=60, settle=3, dock_r=100.0):
    """비행(GoTo/StraightGoTo)이 끝날 때까지 대기.
       R 이 settle 초 연속 안 변하고 dock_r 미만이면 도착으로 판정."""
    prev, stable = None, 0
    for s in range(max_sec):
        sleep(1.0)
        try:
            r = cam.positionLBR.z
        except Exception:
            continue
        if prev is not None and abs(r - prev) < 0.01:
            stable += 1
        else:
            stable = 0
        prev = r
        if stable >= settle and r < dock_r:
            print("   도착 (%d초, R=%.2f)" % (s + 1, r))
            return r
    print("   ⚠️ %d초 내 도착 못 함 (R=%s) — 줌 생략" % (max_sec, prev))
    return None


# ── 지상 밤하늘에서 출발 ──────────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.0))
sleep(2.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("화성까지 2억 3천만 km, 지금 출발합니다")
t1.setIntensity(1.0, Anim(1.0))
sleep(3.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── 비행 시작 ────────────────────────────────────────────────
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.0))       # 도착했을 때 표면이 밝게 보이도록 미리
mars.setShadowContrast(0.0, Anim(0.0))
mars.setPlanetShineStrength(1.0, Anim(0.0))

DataManager.database().data(Data.Type.PlanetType, "Mars") \
    .action(Action.Type.StraightGoTo).trigger()
print("비행 시작 — 도착까지 대기(약 24초)")

# ── ★ 도착 폴링 (이게 핵심. sleep 고정값 쓰면 비행을 가로챈다) ─
p0 = wait_arrival()

# ── 도착 후: 관람 정위치 + 줌 ────────────────────────────────
cam.setTargetHeight(30.0, Anim.cubic(1.5))
sleep(2.0)
t1.setText("화성 궤도 진입"); t1.setIntensity(1.0, Anim(1.0))
sleep(2.5)

if p0:
    p0 = cam.positionLBR.z                    # Target 조정 후 다시 한 번(안전)
    for zoom in (1.35, 1.8, 2.3, 2.8, 3.2, 3.6):
        cam.setPositionR(p0 / zoom, Anim(1.4), -1)
        sleep(1.05)
    print("줌 완료 R = %.2f" % cam.positionLBR.z)
sleep(1.5)

mars.setTerrainModel(Planet.TerrainModel.Viking)
sleep(2.0)
t1.setText("바이킹이 본 붉은 사막")
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 이 배치 자체가 검증용이다. 각 절을 보고 판정한 뒤
#        원본 g*.py 의 '#  검증:' 줄을 갱신할 것 (python3 tools/ledger.py)
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  [배치 검증] 짧은 예제 7개 연속 재생  (총 약 4분 30초)
#
#  ⚠️ 이 파일은 **자동 생성물**이다 — 직접 고치지 마라.
#     원본 g*.py 를 고친 뒤 `python3 tools/make_batch.py` 로 재생성할 것.
#
#  ⚠️ 각 절은 자기 `SceneGraph().reset()` 으로 시작하므로 앞 절 상태를 물려받지 않는다.
#     절마다 try/except 로 감싸 하나가 죽어도 나머지가 돌고, 절 사이 2초 암전으로 구분한다.
#
#  재생 순서 (판정 포인트)
#    1) g1_mars_closeup.py           화성 클로즈업 — 줌이 폭발하지 않고 표면이 보이나
#    2) g7_mars_flight.py            화성으로 비행 — 도착 폴링이 먹어 카메라가 안 날아가나
#    3) g2_catseye_travel.py         고양이눈 성운 — NEBULA 패널은 GoTo 여행이 되나
#    4) g3_rosette_show.py           장미성운 — NGC 패널은 제자리 ON + ScaleUp 만 되나 (g2 와 짝)
#    5) g4_constellation_slider.py   별자리 슬라이더 — 선/그림/라벨이 한 번에 페이드되나
#    6) g5_spaceship_approach.py     우주선 접근 — Insert2D 애니가 영상처럼 움직이나
#    7) g8_world_sky_tour.py         세계 도시 투어 — 관측지가 이름으로 옮겨지고 하늘이 바뀌나
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *


def _gap(label):
    """절 사이 구분 — 암전 2초 + 로그. 어디서 끊겼는지 눈과 로그 양쪽으로 알 수 있다."""
    try:
        u = Universe(Universe.UniverseName.MainUniverse)
        for _ in range(10):
            u.setGlobalIntensity(0.0, Anim(0.0))
            sleep(0.2)
    except Exception as e:
        print("   구분 암전 실패:", e)
    print("\n" + "=" * 62)
    print(">>> " + label)
    print("=" * 62)


# ── 1) g1_mars_closeup.py ──────────────────────────────
_gap("1/7  화성 클로즈업 — 줌이 폭발하지 않고 표면이 보이나")
try:

    # ═══ [정답 예제 1] 화성 클로즈업 (v2 — 줌 폭발 수정) ═══
    # 대응 프롬프트: "화성으로 가서 표면을 크게 보여줘"
    #
    # ⚠️⚠️ v1 실패 원인 (사용자 실측): **StraightGoTo 프레임에서는 줌을 하면 안 된다.**
    #   그 프레임의 `positionLBR.z` 는 105,609 로 읽히는데(HUD 실제는 16,981km),
    #   그 값을 setPositionR 로 되쓰면 엔진이 다른 단위로 해석 → **R 이 수천~1만 Gm 으로 폭발**
    #   (카메라가 태양계 밖으로 날아가 태양만 점으로 보임).
    #   → **줌을 할 거면 반드시 `FadeTo`** — FadeTo 프레임은 R 이 '반지름 단위'(≈5.0)로 읽혀
    #      읽기/쓰기가 일치한다(토성 5.000→2.500→1.250 실측 검증).
    #   → StraightGoTo 는 '그냥 빨리 도착만' 할 때(뒤에 카메라 조작 없음) 쓸 것.
    #
    # 이 예제가 지키는 규칙:
    #   ① FadeTo 로 도킹 (줌하려면 이것)         ② 도킹이 남긴 B 를 건드리지 않는다
    #   ③ 프레이밍은 Target(고도) 30 으로만       ④ 그림자 OFF 3세터 = 표면 전체 밝게
    #   ⑤ 줌 2대 원칙: 절대타겟(p0 한 번만) + 선형 Anim + 겹치기(sleep < anim)
    #   ⑥ 안전장치: p0 가 비정상 범위면 줌을 건너뛴다(폭발 방지)

    cam = Camera(Camera.CameraName.MainCamera)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone

    # ── 지상 밤하늘에서 출발 ──────────────────────────────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
    SceneGraph().reset(1); sleep(1.5)
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))      # 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))         # 지면 OFF
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)         # 밤 21시 = 12 UTC
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(2.0)

    # 자막
    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
    t1.setText("붉은 행성, 화성으로"); t1.setIntensity(1.0, Anim(1.0))
    sleep(2.5)
    t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

    # ── ① FadeTo 로 도킹 (★줌을 하려면 StraightGoTo 말고 이것) ───
    DataManager.database().data(Data.Type.PlanetType, "Mars") \
        .action(Action.Type.FadeTo).trigger()
    sleep(5.0)

    # ── ③ Target 30 (② B 는 건드리지 않는다 — 도킹 기본값이 관람 정위치) ──
    cam.setTargetHeight(30.0, Anim.cubic(1.5))
    sleep(2.0)

    # ── ④ 그림자 OFF 3세터 = 표면 전체 밝게 ──────────────────────
    mars = Planet(Planet.PlanetName.Mars)
    mars.setShadowStrength(0.0, Anim(1.0))
    mars.setShadowContrast(0.0, Anim(1.0))
    mars.setPlanetShineStrength(1.0, Anim(1.0))
    sleep(1.5)

    # ── ⑤⑥ 줌: 절대타겟 + 선형 + 겹치기 (+ 폭발 방지 가드) ───────
    p0 = cam.positionLBR.z
    print("도킹 R = %.3f  (FadeTo 정상이면 5 안팎의 '반지름 단위' 값이어야 함)" % p0)
    if p0 > 100.0 or p0 <= 0.0:
        # 프레임이 이상해 읽기/쓰기 단위가 안 맞는 상태 → 줌하면 카메라가 날아간다
        print("⚠️ R 값이 비정상 범위 → 줌 생략(폭발 방지). FadeTo 로 다시 진입할 것")
    else:
        for zoom in (1.35, 1.8, 2.3, 2.8, 3.2, 3.6):   # 목표는 전부 p0 기준 절대값
            cam.setPositionR(p0 / zoom, Anim(1.4), -1) # 선형 Anim
            sleep(1.05)                                 # anim 보다 짧게 = 겹침
        print("줌 완료 R = %.3f" % cam.positionLBR.z)
    sleep(1.5)

    # ── 표면 지도 교체(탐사선 지도) + 마무리 자막 ────────────────
    mars.setTerrainModel(Planet.TerrainModel.Viking)
    sleep(2.0)
    t1.setText("바이킹 탐사선이 본 화성 표면"); t1.setIntensity(1.0, Anim(1.0))
    sleep(5.0)
    t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

except Exception as _e:
    print("!! g1_mars_closeup.py 실패:", _e)

# ── 2) g7_mars_flight.py ──────────────────────────────
_gap("2/7  화성으로 비행 — 도착 폴링이 먹어 카메라가 안 날아가나")
try:

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
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
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

except Exception as _e:
    print("!! g7_mars_flight.py 실패:", _e)

# ── 3) g2_catseye_travel.py ──────────────────────────────
_gap("3/7  고양이눈 성운 — NEBULA 패널은 GoTo 여행이 되나")
try:

    # ═══ [정답 예제 2] 고양이눈 성운 여행 (NEBULA 패널 = GoTo 가능) ═══
    # 대응 프롬프트: "고양이눈 성운으로 여행해줘"
    #
    # 오늘 확정한 '딥스카이 접근 3단 우선순위' 중 ①번 경로:
    #   ① NEBULA 패널 27개(NebulaType) → GoTo/FadeTo 여행 가능   ← 이 예제
    #   ② 그 외 메시에·은하·성단          → GoTo 없음, ConnectTo + 줌
    #   ③ NGC 패널(NgcType)              → 이동 액션 없음, LookAt + ScaleUp
    # ⚠️ NGC6543 은 'NGC 번호'지만 NEBULA 패널 소속이라 NebulaType 으로 찾아야 함
    #    (NgcType 으로 찾으면 안 나옴 — 같은 번호라도 패널 소속이 능력을 가름)

    cam = Camera(Camera.CameraName.MainCamera)
    uni = Universe(Universe.UniverseName.MainUniverse)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone

    # ── 지상 밤하늘 인트로 ────────────────────────────────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
    SceneGraph().reset(1); sleep(1.5)
    uni.setGlobalIntensity(1.0, Anim(0.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))
    earth.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 7, 15, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)   # 여름밤 22시
    cam.setOrientationH(180.0, Anim(0.0))       # 북쪽(용자리 방향)
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(2.0)

    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
    t1.setText("용자리의 고양이눈 성운 (NGC 6543)"); t1.setIntensity(1.0, Anim(1.0))
    sleep(3.5)

    # ── 핸들 선확보 (⚠️ NebulaType! NgcType 아님) ────────────────
    h = DataManager.database().data(Data.Type.NebulaType, "NGC 6543")

    # ── 암전 속에서 여행 (전환 슬루 숨기기) ──────────────────────
    t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)
    uni.setGlobalIntensity(0.0, Anim(1.2)); sleep(1.5)

    h.action(Action.Type.GoTo).trigger()
    sleep(20.0)                                  # GoTo = 연속 비행(시간 걸림)

    cam.setTargetHeight(30.0, Anim(1.0))         # ★ GoTo 도착 후 Target 30 필수
    sleep(1.5)
    uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(3.0)

    # ── 도착 후 줌 (절대타겟 + 선형 + 겹치기) ────────────────────
    p0 = cam.positionLBR.z
    for zoom in (1.5, 2.2, 3.0, 3.8, 4.5):
        cam.setPositionR(p0 / zoom, Anim(1.5), -1)
        sleep(1.15)
    sleep(2.0)

    t1.setText("죽어가는 별이 내뿜은 가스 껍질"); t1.setIntensity(1.0, Anim(1.0))
    sleep(5.0)
    t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

except Exception as _e:
    print("!! g2_catseye_travel.py 실패:", _e)

# ── 4) g3_rosette_show.py ──────────────────────────────
_gap("4/7  장미성운 — NGC 패널은 제자리 ON + ScaleUp 만 되나 (g2 와 짝)")
try:

    # ═══ [정답 예제 3] 장미성운 (NGC 패널 = 여행 불가, LookAt + ScaleUp) ═══
    # 대응 프롬프트: "겨울 외뿔소자리의 장미성운을 보여줘"
    #
    # '딥스카이 접근 3단' 중 ③번 경로:
    #   NGC 패널 개체(NgcType)는 **이동 액션이 아예 없다**(GoTo/FadeTo/ConnectTo 전부 None,
    #   Action.Type 68개 전수 스캔 확정). 살아있는 액션 13개 중 쓸 것은:
    #     · LookAt   = 조준(성운을 화면 중앙으로)
    #     · ScaleUp  = 확대 (1회 = 1단계 → 반복 트리거). NGC 는 setScale/scale 속성이 없음
    #   → 카메라로 다가가는 게 아니라 '개체를 키워서' 접근 느낌을 낸다.

    SCALE_STEPS = 6          # ScaleUp 반복 횟수(크기 조절용)

    cam = Camera(Camera.CameraName.MainCamera)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone

    # ── 겨울 지상 밤하늘 (장미성운 = 외뿔소자리, 겨울) ────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
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

except Exception as _e:
    print("!! g3_rosette_show.py 실패:", _e)

# ── 5) g4_constellation_slider.py ──────────────────────────────
_gap("5/7  별자리 슬라이더 — 선/그림/라벨이 한 번에 페이드되나")
try:

    # ═══ [정답 예제 4] 전 별자리 선/그림/라벨 슬라이더 페이드 ═══
    # 대응 프롬프트: "밤하늘의 모든 별자리 선을 부드럽게 켜줘"
    #
    # 오늘 부활시킨 ParameterizationLut '프리셋 슬롯' 활용:
    #   ⚠️ 수동 타겟(addTargetAttribute)은 여전히 死. **미리 배선된 프리셋 슬롯만 동작**.
    #   · 051_AllConstellationLines / 052_Pictures / 053_Labels / 054_Boundaries
    #   · 055~058_Slider* / 059_AutoExposure / 060_AutoContrast
    #   🛑 061_WeatherEffectRain / 062_Snow = 별도 날씨 렌더러 소관이라 死(쓰지 말 것)
    #   ★ 핵심: setEnabled(True) 후 **sleep(1.5) 프레임 대기** 없으면 enabled 가 False 로 남음
    #   → 88개 별자리를 개별 호출할 필요 없이 한 번에 부드럽게 페이드

    cam = Camera(Camera.CameraName.MainCamera)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone

    # ── 지상 밤하늘 ──────────────────────────────────────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
    SceneGraph().reset(1); sleep(1.5)
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))
    earth.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(2.0)

    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
    t1.setText("별들을 이어 보면"); t1.setIntensity(1.0, Anim(1.0))
    sleep(3.0)

    # ── ① 별자리 '선' 전체를 슬라이더로 페이드인 ─────────────────
    lines = ParameterizationLut(
        ParameterizationLut.ParameterizationLutName.ParameterizationLut051_AllConstellationLines)
    lines.setEnabled(True)
    sleep(1.5)                                   # ★ 프레임 대기 필수
    lines.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
    lines.setInternalValue(1.0, Anim(4.0))       # 0→1 = 부드럽게 전부 켜짐
    sleep(5.0)

    t1.setText("88개 별자리, 하나의 슬라이더로"); sleep(3.0)

    # ── ② 별자리 '이름표'도 페이드인 ─────────────────────────────
    labels = ParameterizationLut(
        ParameterizationLut.ParameterizationLutName.ParameterizationLut053_AllConstellationLabels)
    labels.setEnabled(True)
    sleep(1.5)
    labels.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
    labels.setInternalValue(1.0, Anim(3.0))
    sleep(4.0)

    t1.setText("신화의 그림까지"); sleep(2.0)

    # ── ③ 신화 그림(art) 페이드인 ────────────────────────────────
    art = ParameterizationLut(
        ParameterizationLut.ParameterizationLutName.ParameterizationLut052_AllConstellationPictures)
    art.setEnabled(True)
    sleep(1.5)
    art.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
    art.setInternalValue(1.0, Anim(5.0))
    sleep(6.0)

    t1.setText("하늘 가득한 이야기"); sleep(4.0)

    # ── ④ 정리: 그림만 끄고 선은 남기기 ──────────────────────────
    art.setInternalValue(0.0, Anim(3.0)); sleep(3.5)
    t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)
    lines.restore(); labels.restore(); art.restore()

except Exception as _e:
    print("!! g4_constellation_slider.py 실패:", _e)

# ── 6) g5_spaceship_approach.py ──────────────────────────────
_gap("6/7  우주선 접근 — Insert2D 애니가 영상처럼 움직이나")
try:

    # ═══ [정답 예제 5] 우주선이 다가온다 (Insert2D 애니메이션 = 영상 대체) ═══
    # 대응 프롬프트: "우주선이 다가오는 장면을 만들어줘"
    #
    # 오늘 확보한 '영상의 유일한 대체 수단':
    #   🛑 VideoPlayer/Audio = 별도 호스트 소관이라 스크립트로 재생 불가(확정, 재시도 금지)
    #   ✅ 대신 Insert2D 는 **setPosition/setSize 가 Anim 을 받는다** → 이미지 한 장을
    #      돔에서 부드럽게 움직이고 키워서 '다가옴/지나감'을 만든다.
    #   · 접근    = setSize 작게→크게 + setPosition 낮게→높게
    #   · 플라이바이 = setPosition 좌→우
    #   · 프레임 flip = setTexture 를 sleep 간격으로 교체(저프레임 영상)
    #
    # ⚠️ 준비: localUserFolder(D:/SkyExplorer-Data/user)에 우주선 PNG(투명배경) 1장.
    #    파일명 몰라도 되게 폴더를 자동 탐색한다.
    import os

    cam = Camera(Camera.CameraName.MainCamera)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone

    # ── 이미지 자동 탐색 ─────────────────────────────────────────
    base = Configuration.configuration().localUserFolder
    imgs = []
    try:
        for f in sorted(os.listdir(base)):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                imgs.append(base.rstrip("/\\") + "/" + f)
    except Exception as ex:
        print("폴더 목록 실패:", ex)
    print("사용할 이미지:", imgs[0] if imgs else "(없음 — PNG 1장 넣어주세요)")

    # ── 별밭 배경 ────────────────────────────────────────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
    SceneGraph().reset(1); sleep(1.5)
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))
    earth.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)
    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))
    sleep(2.0)

    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 20, 0)); t1.setSize(0.052)
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
    t1.setText("저 멀리 무언가 다가온다"); t1.setIntensity(1.0, Anim(1.0))
    sleep(3.0)

    # ── Insert2D 붙이기 ──────────────────────────────────────────
    ship = Insert2D(Insert2D.Insert2DName.Insert2D001)
    cam.addChild(ship.id, Camera.CameraPort.FixedForeground)
    if imgs:
        ship.setTexture(imgs[0])
    ship.setIntensity(1.0, Anim(0.0))

    # ── ① 접근: 작은 점(낮은 곳) → 크게(위로) ───────────────────
    ship.setSize(0.04, Anim(0.0))
    ship.setPosition(Vec(0.0, 8.0, 0.0), Anim(0.0))
    sleep(0.5)
    ship.setSize(0.55, Anim.cubic(6.0))              # 커짐 = 다가옴
    ship.setPosition(Vec(0.0, 42.0, 0.0), Anim.cubic(6.0))
    sleep(6.5)

    t1.setText("가까이서 보니 탐사선이었다"); sleep(3.5)

    # ── ② 플라이바이: 좌 → 우로 지나감 ──────────────────────────
    ship.setPosition(Vec(-55.0, 42.0, 0.0), Anim(0.0)); sleep(0.4)
    ship.setPosition(Vec(55.0, 42.0, 0.0), Anim.cubic(5.0))
    sleep(5.5)

    # ── ③ 멀어짐: 작아지며 아래로 ───────────────────────────────
    t1.setText("그리고 다시 어둠 속으로")
    ship.setSize(0.04, Anim.cubic(4.0))
    ship.setPosition(Vec(55.0, 10.0, 0.0), Anim.cubic(4.0))
    sleep(4.5)
    ship.setIntensity(0.0, Anim(1.5))
    sleep(2.0)
    t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

except Exception as _e:
    print("!! g5_spaceship_approach.py 실패:", _e)

# ── 7) g8_world_sky_tour.py ──────────────────────────────
_gap("7/7  세계 도시 투어 — 관측지가 이름으로 옮겨지고 하늘이 바뀌나")
try:

    # ═══ [정답 예제 8] 세계 도시 밤하늘 투어 (관측지 이름으로 이동) ═══
    # 대응 프롬프트: "서울, 파리, 시드니에서 본 같은 시각의 밤하늘을 비교해줘"
    #
    # ★ 2026-07-30 새로 확인: **관측지를 '이름'으로 옮길 수 있다** (좌표 하드코딩 불필요)
    #     DataManager.database().data(Data.Type.CityType, "Paris").action(Action.Type.GoTo).trigger()
    #   · 실측: 청주(36.64,127.49,200m) → 서울(37.599,126.978,100m) 정확히 이동, 1~2초
    #   · 지상 시점 유지(camR=0), 고도까지 자동
    #   · 살아있는 타입: CityType(도시) / MountainType(산) / VolcanoType(화산) — 각각 GoTo·FadeTo
    #   🛑 GoToPlace·FadeToPlace 는 死 → 그냥 GoTo 를 쓴다
    #
    # 연출 포인트: 관측지가 바뀌면 **같은 시각인데 하늘이 달라진다**(위도에 따라 별자리 높이·
    #   보이는 별자리가 바뀜). 남반구(시드니)로 가면 오리온이 뒤집혀 보이는 게 하이라이트.

    # (도시이름, 자막) — 이름은 DB 표기 그대로. 실측 확인: Seoul/Paris/New York/London/Tokyo
    CITIES = [
        ("Seoul",    "서울 — 북위 37도"),
        ("Paris",    "파리 — 북위 49도, 별이 더 낮게 뜬다"),
        ("New York", "뉴욕 — 같은 시각, 다른 하늘"),
    ]

    cam = Camera(Camera.CameraName.MainCamera)
    uni = Universe(Universe.UniverseName.MainUniverse)
    dm  = DateManager()
    tz  = DateManager.TimeZone.DefaultTimeZone
    db  = DataManager.database()

    # ── 지상 밤하늘 기본 세팅 ────────────────────────────────────
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
    # ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
    #    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
    SceneGraph().reset(1); sleep(1.5)
    uni.setGlobalIntensity(1.0, Anim(0.0))
    earth = Planet(Planet.PlanetName.Earth)
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))     # 대기 OFF
    earth.setTerrainIntensity(0.0, Anim(0.0))        # 지면 OFF
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0))   # 같은 시각 고정(UTC)
    sleep(0.5)
    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))

    # 오리온을 기준점으로 (도시마다 높이·기울기가 달라지는 게 보임)
    ori = Constellation(Constellation.ConstellationName.Ori)
    ori.setLinesIntensity(0.8, Anim(1.0))
    ori.setLabelIntensity(0.7, Anim(1.0))
    sleep(2.0)

    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
    t1.setText("같은 시각, 지구 어디에서 보느냐에 따라"); t1.setIntensity(1.0, Anim(1.0))
    sleep(3.5)


    def goto_city(name, caption):
        """도시 이름으로 관측지 이동 (좌표 하드코딩 불필요)"""
        h = db.data(Data.Type.CityType, name)
        if h is None:
            print("⚠️ 도시 '%s' 조회 실패 — 이름 표기 확인 필요" % name)
            return
        # 전환을 부드럽게: 살짝 암전 → 이동 → 페이드인
        uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(1.2)
        h.action(Action.Type.GoTo).trigger()
        sleep(3.0)                                    # 관측지 전환은 1~2초면 끝남
        cam.setTargetHeight(30.0, Anim(0.0))          # 관람 정위치 재확인
        t1.setText(caption)
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(2.0)
        try:
            p = Place2D(Place2D.Place2DName(0)).position
            print("이동 완료: %s → 위도 %.3f / 경도 %.3f / 고도 %.0fm" % (name, p.x, p.y, p.z))
        except Exception:
            pass
        sleep(6.0)                                    # 하늘 감상


    for city, cap in CITIES:
        goto_city(city, cap)

    # ── 마무리: 산 위에서 보는 하늘 (MountainType 도 같은 방식) ──
    h = db.data(Data.Type.MountainType, "Mont blanc")
    if h is not None:
        uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(1.2)
        h.action(Action.Type.GoTo).trigger()
        sleep(3.0)
        cam.setTargetHeight(30.0, Anim(0.0))
        t1.setText("몽블랑 정상 — 4,800m 위의 하늘")
        uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(2.0)
        try:                                        # (v2) 산 구간도 좌표 로그 남기기
            q = Place2D(Place2D.Place2DName(0)).position
            print("이동 완료: Mont blanc → 위도 %.3f / 경도 %.3f / 고도 %.0fm" % (q.x, q.y, q.z))
        except Exception:
            pass
        sleep(6.0)

    t1.setText("같은 별, 다른 자리"); sleep(4.0)
    t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

except Exception as _e:
    print("!! g8_world_sky_tour.py 실패:", _e)

print("\n배치 종료 — 짧은 예제 7개")

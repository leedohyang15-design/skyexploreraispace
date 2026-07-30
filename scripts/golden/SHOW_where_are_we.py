# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 — "우리는 어디에 있는가"  (약 9~10분)
#  구조: 질문 하나에서 출발해 그 답이 다음 질문을 낳는 중첩 구조
#
#    막1  Q1. "지금 우리는 어디서 하늘을 보고 있나?"      → 관측지 이동(도시·산)
#    막2  Q2. "그럼 저 별들은 다 뭔가?"                    → 별자리 슬라이더
#    막3  Q3. "별과 별 사이엔 무엇이 있나?"                → 딥스카이 (제자리 ON / 여행)
#    막4  Q4. "그럼 우리 가까이엔?"                        → 행성 비행 + 고리
#    막5  A.  다시 지구로                                  → 처음 그 하늘로 귀환
#
#  ※ 오늘(2026-07-30) 확정한 규칙을 전부 태운 검증용 쇼:
#     · 관측지를 '이름'으로 이동 (CityType/MountainType + GoTo)
#     · ParameterizationLut 프리셋 (setEnabled 후 프레임 대기 1.5s)
#     · 딥스카이 3단: NGC 패널(LookAt+ScaleUp) / NEBULA 패널(GoTo 여행)
#     · 비행 후 '도착 폴링' 뒤에 줌 (비행 중 줌 = 태양계로 날아감)
#     · 줌 2대 원칙: 절대타겟(p0 한 번만) + 선형 Anim + 겹치기
#     · B 는 도킹 기본값 유지, 프레이밍은 Target(고도) 30 으로만
#     · 토성 고리는 '구도'가 8할 (B=75 개방 + R≥3.2)
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()

# ── 공용 헬퍼 ────────────────────────────────────────────────
t1 = None      # 자막(아래에서 생성)


def say(text, hold=0.0):
    """자막 교체(+선택적 홀드)"""
    if t1 is not None:
        t1.setText(text)
        t1.setIntensity(1.0, Anim(0.8))
    if hold:
        sleep(hold)


def dark(sec=1.2):
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(sec)


def light(sec=2.0):
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(sec)


def clamp_dark(sec):
    """★ 암전 '유지' 클램프 — reset()/FadeTo 는 GlobalIntensity 를 1.0 으로 되돌린다.
       한 번 setGlobalIntensity(0) 해두는 걸론 부족해서, 그 구간 내내 0 을 다시 찍어 눌러야
       재세팅 과정(별·은하수·날짜점프)이 화면에 안 보인다. (프로젝트 노트의 '클램프 루프')"""
    n = int(sec / 0.2)
    for _ in range(max(n, 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)


def ground_night_slow(lat=36.64, lon=127.49, alt=200.0,
                      y=2026, mo=1, d=15, h=12, mi=0, gap=0.35):
    """지상 세팅을 '나눠서' 건다 — 한 프레임에 몰아치면 엔진이 버벅여 화면이 뚝뚝 끊긴다.
       ⚠️ 반드시 clamp_dark 로 암전을 유지한 채 호출할 것."""
    e = Planet(Planet.PlanetName.Earth)
    e.setIntensity(1.0, Anim(0.0));                       uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(gap)
    e.setAtmosphereIntensity(0.0, Anim(0.0))
    e.setTerrainIntensity(0.0, Anim(0.0));                uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(gap)
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(lat, lon, alt))
    uni.setGlobalIntensity(0.0, Anim(0.0));               sleep(gap)
    dm.stop();                                            sleep(0.3)
    dm.setDateTime(y, mo, d, h, mi, 0, tz, Anim(0.0))     # 날짜 점프(무거움) — 단독으로
    uni.setGlobalIntensity(0.0, Anim(0.0));               sleep(gap + 0.3)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));               sleep(gap)
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));               sleep(gap)
    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));               sleep(gap)


def ground_night(lat=36.64, lon=127.49, alt=200.0,
                 y=2026, mo=1, d=15, h=12, mi=0):
    """지상 밤하늘 표준 세팅 (대기 OFF + 지면 OFF)"""
    e = Planet(Planet.PlanetName.Earth)
    e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0))
    e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(lat, lon, alt))
    dm.stop(); sleep(0.3)
    dm.setDateTime(y, mo, d, h, mi, 0, tz, Anim(0.0)); sleep(0.4)
    cam.setOrientationH(0.0, Anim(0.0))
    cam.setTargetHeight(30.0, Anim(0.0))


def wait_arrival(max_sec=60, settle=3, dock_r=None):
    """★ 비행(GoTo)이 끝날 때까지 대기. 안 하면 비행을 가로채 카메라가 날아간다.
       ⚠️ dock_r 는 '행성'에만 쓴다(R≈4~5). **딥스카이는 도착해도 R 이 거대**(1e13 등)라
          dock_r 를 걸면 영영 도착 판정이 안 난다 → None(=상대변화율로만 판정)."""
    prev, stable = None, 0
    for s in range(max_sec):
        sleep(1.0)
        try:
            r = cam.positionLBR.z
        except Exception:
            continue
        if prev is not None:
            scale = max(abs(prev), 1.0)                 # 상대 변화율(스케일 무관)
            if abs(r - prev) / scale < 1e-6:
                stable += 1
            else:
                stable = 0
        prev = r
        ok = (stable >= settle) and (dock_r is None or r < dock_r)
        if ok:
            print("   도착 %d초, R=%.4g" % (s + 1, r))
            return r
    print("   ⚠️ 도착 감지 실패(R=%s)" % prev)
    return None


def zoom_in(steps=(1.35, 1.8, 2.3, 2.8, 3.2)):
    """★ 줌 2대 원칙: 절대타겟(p0 한 번만) + 선형 Anim + 겹치기(sleep < anim)
       ⚠️ R 의 절대 크기로 정상/비정상을 판단하지 말 것 — 딥스카이는 원래 R 이 거대하다."""
    p0 = cam.positionLBR.z
    if p0 is None or p0 <= 0.0:
        print("   ⚠️ R=%s → 줌 생략" % p0); return
    print("   줌 시작 (p0=%.4g)" % p0)
    for z in steps:
        cam.setPositionR(p0 / z, Anim(1.4), -1)
        sleep(1.05)
    sleep(0.8)


def wait_place_settle(max_sec=30, settle=2):
    """★ 관측지 이동도 '애니메이션'이다 — 좌표가 멈출 때까지 기다린다.
       (안 기다리면 중간 좌표가 찍힘: 파리를 40.49/88.07 로 읽는 사고)"""
    prev, stable = None, 0
    for s in range(max_sec):
        sleep(1.0)
        try:
            q = Place2D(Place2D.Place2DName(0)).position
            cur = (round(q.x, 3), round(q.y, 3), round(q.z, 1))
        except Exception:
            continue
        if prev is not None and cur == prev:
            stable += 1
        else:
            stable = 0
        prev = cur
        if stable >= settle:
            return cur
    return prev


def goto_place(dtype, name, caption):
    """관측지를 '이름'으로 이동. ⚠️ 암전 없이 — 이동 자체가 부드러우니 끊지 않는다."""
    h = db.data(getattr(Data.Type, dtype), name)
    if h is None:
        print("   ⚠️ %s '%s' 조회 실패" % (dtype, name)); return False
    say(caption)                                  # 자막 먼저 → 이동 → 그대로 이어짐
    h.action(Action.Type.GoTo).trigger()
    pos = wait_place_settle()                     # ★ 좌표가 멈출 때까지
    cam.setTargetHeight(30.0, Anim(1.0))
    if pos:
        print("   → %s: 위도 %.3f / 경도 %.3f / 고도 %.0fm" % ((name,) + pos))
    return True


# ══════════════════════════════════════════════════════════════
#  막 0 — 시작
# ══════════════════════════════════════════════════════════════
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night()

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setIntensity(0.0, Anim(0.0))

light(2.5)
say("청주, 1월의 밤", 4.0)

# ══════════════════════════════════════════════════════════════
#  막 1 — Q1. "지금 우리는 어디서 하늘을 보고 있나?"
#         → 관측지를 이름으로 옮기며 '같은 시각 다른 하늘'
# ══════════════════════════════════════════════════════════════
print("\n[막1] Q1 — 우리는 어디에 서 있나 (관측지 이동)")
say("질문 하나. 지금 우리는 '어디에서' 이 하늘을 보고 있나?", 5.0)

ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.85, Anim(1.5))
ori.setLabelIntensity(0.7, Anim(1.5))
say("기준을 하나 두자 — 오리온자리", 4.5)

goto_place("CityType", "Paris", "파리. 같은 시각인데 오리온이 더 낮다")
sleep(6.0)
goto_place("CityType", "New York", "뉴욕. 또 다른 높이")
sleep(6.0)
goto_place("MountainType", "Mont blanc", "몽블랑 정상 — 4,800m 위의 하늘")
sleep(6.0)

say("서 있는 곳이 바뀌면 하늘도 바뀐다", 5.0)

# ── 다시 청주로 (같은 지상 프레임이라 암전 불필요 — 조용히 되돌린다) ──
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
cam.setTargetHeight(30.0, Anim(1.0))
say("다시, 청주")
sleep(4.0)

# ══════════════════════════════════════════════════════════════
#  막 2 — Q2(중첩). "그럼 저 별들은 다 뭔가?"
#         → 전 별자리를 슬라이더 하나로 (ParameterizationLut 프리셋)
# ══════════════════════════════════════════════════════════════
print("\n[막2] Q2 — 저 별들은 뭔가 (별자리 슬라이더)")
say("두 번째 질문. 그럼 저 별들은 대체 뭔가?", 5.0)

lines = ParameterizationLut(
    ParameterizationLut.ParameterizationLutName.ParameterizationLut051_AllConstellationLines)
lines.setEnabled(True)
sleep(1.5)                                   # ★ 프레임 대기 필수
lines.setInternalValue(0.0, Anim(0.0)); sleep(0.4)
say("사람들은 별을 이어 이름을 붙였다")
lines.setInternalValue(1.0, Anim(5.0))       # 88개가 한꺼번에 부드럽게
sleep(6.5)

art = ParameterizationLut(
    ParameterizationLut.ParameterizationLutName.ParameterizationLut052_AllConstellationPictures)
art.setEnabled(True)
sleep(1.5)
art.setInternalValue(0.0, Anim(0.0)); sleep(0.4)
say("그리고 이야기를 얹었다")
art.setInternalValue(0.85, Anim(5.0))
sleep(7.0)

say("하지만 그건 우리가 그은 선일 뿐", 4.5)
art.setInternalValue(0.0, Anim(3.0)); sleep(3.5)

# ══════════════════════════════════════════════════════════════
#  막 3 — Q3(중첩). "별과 별 사이엔 무엇이 있나?"
#         → 딥스카이 3단 중 ③(NGC 제자리 ON) + ①(NEBULA 여행)
# ══════════════════════════════════════════════════════════════
print("\n[막3] Q3 — 별 사이엔 뭐가 있나 (딥스카이)")
say("세 번째 질문. 그 별과 별 '사이'엔 무엇이 있나?", 5.0)

lines.setInternalValue(0.35, Anim(2.0)); sleep(2.5)

# ③ NGC 패널 = 이동 액션 없음 → 제자리 ON + LookAt + ScaleUp
rosette = NGC(NGC.NGCName.NGC2237)
rosette.setIntensity(1.0, Anim(2.5))
rosette.setLabelIntensity(1.0, Anim(2.5))
say("오리온 옆, 눈에 안 보이던 구름 하나")
sleep(4.0)

hr = db.data(Data.Type.NgcType, "NGC 2237")
if hr is not None:
    hr.action(Action.Type.LookAt).trigger()      # 조준
    sleep(5.0)
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    say("장미성운 — 1천 광년 밖의 가스 구름")
    for i in range(6):                           # 확대(1회=1단계)
        hr.action(Action.Type.ScaleUp).trigger()
        sleep(1.2)
    sleep(3.0)
    say("이 안에서 지금도 별이 태어나고 있다", 5.0)
    for i in range(6):
        hr.action(Action.Type.ScaleDown).trigger()
        sleep(0.5)

# ① NEBULA 패널 = GoTo 여행 가능
say("그리고 별이 죽는 자리도 있다", 4.0)
hc = db.data(Data.Type.NebulaType, "NGC 6543")
if hc is not None:
    say("고양이눈 성운으로")                      # 암전 없이 — 비행 자체가 볼거리
    hc.action(Action.Type.GoTo).trigger()
    print("   고양이눈 성운으로 비행")
    wait_arrival(max_sec=70, dock_r=None)        # ★ 딥스카이는 R 이 거대 → dock_r 걸지 않는다
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    say("고양이눈 성운")
    zoom_in()                                    # 도착 후에만 줌
    sleep(3.0)
    say("죽어가는 별이 벗어던진 껍질", 6.0)

# ══════════════════════════════════════════════════════════════
#  막 4 — Q4(중첩). "그럼 우리 '가까이'엔?"
#         → 행성 비행(GoTo + 폴링 + 줌) → 토성 고리(구도)
# ══════════════════════════════════════════════════════════════
print("\n[막4] Q4 — 우리 가까이엔 (행성)")
# 딥스카이 프레임 → 지상 프레임은 reset 이 필요 → 암전 클램프로 재세팅을 숨긴다
dark(1.2)
clamp_dark(0.6)                     # reset 직전까지 0 유지
SceneGraph().reset(1)
clamp_dark(1.4)                     # ★ reset 이 gi 를 1.0 으로 되돌리므로 계속 눌러준다
ground_night_slow()                 # 나눠서 세팅(버벅임 방지) + 내부에서도 계속 클램프
clamp_dark(0.4)
light(2.0)
say("네 번째 질문. 그렇게 먼 곳 말고, 우리 '가까이'엔?", 5.0)

# 화성 — GoTo 비행 (이륙 구간이 있어 '지구를 떠나는' 느낌)
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.0))       # 도착 시 표면 전체가 밝게
mars.setShadowContrast(0.0, Anim(0.0))
mars.setPlanetShineStrength(1.0, Anim(0.0))

say("2억 3천만 km. 지금 출발한다")
db.data(Data.Type.PlanetType, "Mars").action(Action.Type.GoTo).trigger()
print("   화성으로 비행")
wait_arrival(dock_r=100.0)                    # ★ 행성은 R≈4~5 로 수렴하니 dock_r 사용
cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)   # B 는 손대지 않는다
say("화성 궤도")
sleep(2.0)
zoom_in()
mars.setTerrainModel(Planet.TerrainModel.Viking)
sleep(2.0)
say("붉은 사막. 물이 흐른 흔적이 남아 있다", 6.0)

# 토성 — 고리는 '구도'가 8할. FadeTo 는 자체 페이드가 있으니 암전 불필요
say("더 멀리, 고리를 가진 행성")
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(1.5))    # 배경 검정 = 대비
db.data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
sleep(5.5)
sat = Planet(Planet.PlanetName.Saturn)
sat.setShadowStrength(0.0, Anim(0.5))
sat.setShadowContrast(0.0, Anim(0.5))
sat.setPlanetShineStrength(1.0, Anim(0.5))
p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, 75.0, max(3.2, p.z * 0.7)), Anim.cubic(5.0), -1)  # 고리면 개방+근접
sleep(5.5)
cam.setTargetHeight(30.0, Anim(1.5)); sleep(1.5)
t1.setDistance(20.0, Anim(0.0))              # 행성 프레임 자막 규칙
say("토성", 4.0)
say("고리는 얼음과 바위 — 가장 큰 조각도 집 한 채 크기", 6.0)

# 천천히 한 바퀴
base_l = cam.positionLBR.x
for d in (70.0, 140.0):
    q = cam.positionLBR
    cam.setPositionLBR(Vec(base_l + d, q.y, q.z), Anim(5.0), -1)
    sleep(4.2)
sleep(2.0)

# ══════════════════════════════════════════════════════════════
#  막 5 — A. 다시 지구로
# ══════════════════════════════════════════════════════════════
print("\n[막5] 귀환")
# ⚠️⚠️ 여기가 '화면 뚝뚝뚝'의 본진이었다. 원인 2가지:
#   ① `SceneGraph().reset(1)` 이 **GlobalIntensity 를 1.0 으로 되돌린다** →
#      암전을 미리 걸어놔도 reset 순간 화면이 밝아져 재세팅 과정이 그대로 노출됨
#   ② 재세팅(별·은하수·날짜점프·별자리·자막)을 **한 프레임에 몰아쳐** 엔진이 버벅임
# → 해결: **클램프 루프로 암전을 계속 눌러 유지** + **세팅을 잘게 나눠서** 실행
t1.setIntensity(0.0, Anim(1.0)); sleep(1.2)
dark(1.6)
clamp_dark(0.8)                              # reset 직전까지 0 을 계속 찍어 누름
SceneGraph().reset(1)
clamp_dark(2.0)                              # ★ reset 이 gi 를 되돌리므로 그 위를 계속 덮는다
ground_night_slow()                          # 나눠서 세팅 (내부에서도 클램프 유지)

ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.5, Anim(0.0))
uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(0.4)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setIntensity(0.0, Anim(0.0))
uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(0.4)

clamp_dark(1.0)                              # 모든 세팅이 앉을 때까지 암전 유지
light(3.5)                                   # 천천히 밝아짐 = 부드러운 복귀

say("그리고 다시, 청주의 1월 밤", 5.0)
say("같은 하늘인데 — 이제 조금 다르게 보인다", 6.0)
say("우리는 여기에 있다", 6.0)
t1.setIntensity(0.0, Anim(2.0))
sleep(2.5)
print("\n=== 쇼 종료 ===")

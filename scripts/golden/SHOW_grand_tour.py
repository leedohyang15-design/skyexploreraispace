# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 규칙 검사는 통과했으나 돔에서 본 기록이 없다. 기하(프레임·L/B·R 단위)는 정적 검사로 안 잡히니 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 ③ — "태양계 대여행"  (약 9분)
#  Q1. 우리 옆집엔 누가 사나?     → 화성(암석 행성, 탐사선 지도)
#  Q2. 더 나가면?                 → 목성(가스 행성 + 갈릴레이 위성계)
#  Q3. 가장 아름다운 건?          → 토성(고리는 '구도'가 8할)
#  Q4. 그 너머 끝엔?              → 명왕성(왜소행성, 뉴호라이즌스 하트)
#
#  태우는 규칙: GoTo 비행 + 도착 폴링(비행 중 줌 금지) · 줌 2대원칙 ·
#              B 는 도킹 기본값 유지 · 그림자 OFF 3세터 · 고리 구도 · 끊김 없는 복귀
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()
t1  = None

# ═══ 검증된 공통 헬퍼 (2026-07-30 실측 규칙) ═══════════════════
def say(text, hold=0.0):
    if t1 is not None:
        t1.setText(text); t1.setIntensity(1.0, Anim(0.8))
    if hold: sleep(hold)

def dark(sec=1.2):
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(sec)

def light(sec=2.0):
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(sec)

def clamp_dark(sec):
    """★ reset()/FadeTo 는 GlobalIntensity 를 1.0 으로 되돌린다 → 0 을 계속 찍어 눌러야 함"""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(0.2)

CAPTION_H = 12          # ★ 자막 기본 높이 (사용자 확정) — 25 는 천체와 겹쳤다. 더 아래로.


def make_caption(dist=1.0, height=None):
    """자막 생성/재배치.
       ⚠️ 이전 자막을 반드시 끈다 — 안 끄면 옛 자막이 그 자리에 남아 '안 내려간 것처럼' 보인다.
       ⚠️ 행성 프레임은 distance 20 + setSize 금지 / 지상은 distance 1.0 + setSize 0.052."""
    global t1
    if height is None:
        height = CAPTION_H
    if t1 is not None:
        try: t1.setIntensity(0.0, Anim(0.0))      # ★ 옛 자막 끄기
        except Exception: pass
    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, height, 0))
    if dist == 1.0:
        t1.setSize(0.052)                          # 행성 프레임에선 setSize 금지
    t1.setColor(Vec(1.0, 1.0, 0.55))
    t1.setDistance(dist, Anim(0.0))
    t1.setIntensity(0.0, Anim(0.0))

def ground_night_slow(lat=36.64, lon=127.49, alt=200.0,
                      y=2026, mo=1, d=15, h=12, mi=0, mw=0.55, gap=0.35):
    """★ 지상 세팅을 나눠서 — 한 프레임에 몰아치면 화면이 뚝뚝 끊긴다.
       반드시 clamp_dark 로 암전을 유지한 채 호출."""
    e = Planet(Planet.PlanetName.Earth)
    e.setIntensity(1.0, Anim(0.0));            uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(gap)
    e.setAtmosphereIntensity(0.0, Anim(0.0))
    e.setTerrainIntensity(0.0, Anim(0.0));     uni.setGlobalIntensity(0.0, Anim(0.0)); sleep(gap)
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(lat, lon, alt))
    uni.setGlobalIntensity(0.0, Anim(0.0));    sleep(gap)
    dm.stop(); sleep(0.3)
    dm.setDateTime(y, mo, d, h, mi, 0, tz, Anim(0.0))     # 날짜 점프(무거움) 단독
    uni.setGlobalIntensity(0.0, Anim(0.0));    sleep(gap + 0.3)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));    sleep(gap)
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(mw, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));    sleep(gap)
    cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
    uni.setGlobalIntensity(0.0, Anim(0.0));    sleep(gap)

def hard_reset_to_ground(**kw):
    """★ 행성/딥스카이 → 지상 복귀 (끊김 없이). 암전 클램프로 재세팅을 완전히 숨긴다."""
    if t1 is not None: t1.setIntensity(0.0, Anim(1.0))
    sleep(1.0); dark(1.4); clamp_dark(0.8)
    SceneGraph().reset(1)
    clamp_dark(2.0)                                        # reset 이 gi 를 되돌리므로 계속 덮기
    ground_night_slow(**kw)
    make_caption(1.0)
    clamp_dark(0.8)

def wait_arrival(max_sec=60, settle=3, dock_r=None):
    """★ 비행이 끝나기 전에 줌하면 비행을 가로채 카메라가 날아간다.
       dock_r 은 '행성'에만(R≈4~5). 딥스카이는 도착해도 R 이 거대(1e13) → None."""
    prev, stable = None, 0
    for s in range(max_sec):
        sleep(1.0)
        try: r = cam.positionLBR.z
        except Exception: continue
        if prev is not None:
            if abs(r - prev) / max(abs(prev), 1.0) < 1e-6: stable += 1
            else: stable = 0
        prev = r
        if stable >= settle and (dock_r is None or r < dock_r):
            print("   도착 %ds, R=%.4g" % (s + 1, r)); return r
    print("   ⚠️ 도착 감지 실패(R=%s)" % prev); return None

def zoom_in(steps=(1.35, 1.8, 2.3, 2.8, 3.2)):
    """★ 절대타겟(p0 한 번만) + 선형 Anim + 겹치기(sleep < anim)"""
    p0 = cam.positionLBR.z
    if p0 is None or p0 <= 0.0: return
    for z in steps:
        cam.setPositionR(p0 / z, Anim(1.4), -1); sleep(1.05)
    sleep(0.8)

def shadows_off(obj):
    """운영 표준: 표면을 보여줄 땐 그림자 3세터 OFF"""
    obj.setShadowStrength(0.0, Anim(1.0))
    obj.setShadowContrast(0.0, Anim(1.0))
    obj.setPlanetShineStrength(1.0, Anim(1.0))

def to_inertial(planet_obj):
    """★ 관성 프레임(EquatorialJ2000) 전환 — 위성 공전을 보려면 필수.
       도킹 프레임(EquatorialSynchronous)은 카메라가 행성 자전을 따라 돌아서
       시간을 흘려도 '위성이 도는 게 아니라 하늘이 도는 것'처럼 보인다.
       ⚠️ 전환 자체가 시점 점프로 보이므로 **도착 직후(장면이 아직 안 시작됐을 때)** 해야 한다.
          위성을 켠 뒤에 하면 화면이 갑자기 바뀌어 흐름이 끊긴다(실측 지적)."""
    try:
        ip = planet_obj.portId(Planet.PlanetPort.EquatorialJ2000)
        q = cam.positionLBR
        cam.setPositionLBR(Vec(q.x, q.y, q.z), Anim(2.5), ip)      # 위치 유지, 프레임만
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(2.5), ip)   # 시선 정렬 필수
        sleep(3.0)
        print("   관성 프레임(EquatorialJ2000) 전환 완료")
        return True
    except Exception as ex:
        print("   관성 프레임 전환 실패:", ex); return False


def fly_to_planet(name, caption, zoom=True, pullback=None, inertial_obj=None):
    """행성 GoTo 비행 → 도착 폴링 → [관성 프레임 전환] → Target 30 → (풀백) → 줌.
       B 는 손대지 않는다. inertial_obj 를 주면 도착 직후 관성 프레임으로 전환(위성 공전용)."""
    say(caption)
    db.data(Data.Type.PlanetType, name).action(Action.Type.GoTo).trigger()
    print("   %s 로 비행" % name)
    wait_arrival(dock_r=100.0)
    if inertial_obj is not None:
        to_inertial(inertial_obj)               # ★ 도착 직후 = 아직 장면이 시작 전이라 티가 덜 남
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    make_caption(20.0)                          # 행성 프레임 자막(낮은 위치)로 교체
    if pullback:
        p = cam.positionLBR
        cam.setPositionR(p.z * pullback, Anim.cubic(4.0), -1); sleep(4.5)
    if zoom: zoom_in()

# ── 막0 : 지상에서 출발 ──────────────────────────────────────
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night_slow(y=2026, mo=1, d=15, h=12)
make_caption(1.0)
light(2.5)
say("맨눈으로 보이는 행성은 다섯 개뿐이다", 5.0)
say("하나씩 찾아가 보자", 4.0)

# ── 막1 : 화성 (암석 행성) ───────────────────────────────────
print("\n[막1] 화성")
mars = Planet(Planet.PlanetName.Mars)
shadows_off(mars)
fly_to_planet("Mars", "첫 번째 — 화성. 2억 3천만 km")
say("붉은 사막의 행성", 4.0)
mars.setTerrainModel(Planet.TerrainModel.Viking)
sleep(2.5)
say("바이킹 탐사선이 찍은 지도", 5.0)
say("한때 물이 흘렀고, 지금은 얼어붙었다", 6.0)

# ── 막2 : 목성 + 갈릴레이 위성 ───────────────────────────────
print("\n[막2] 목성과 위성들")
hard_reset_to_ground()
light(1.8)
jup = Planet(Planet.PlanetName.Jupiter)
shadows_off(jup)
# ⚠️ 실측 지적: 도킹 R≈5 에선 위성 궤도가 화면 밖/너무 작아 안 보임
#    → **풀백(R×3.5)** 으로 궤도를 담고, 위성 **setScale 을 크게(14)** 준다
fly_to_planet("Jupiter", "두 번째 — 목성. 지구 1,300개가 들어간다",
              zoom=False, pullback=3.5, inertial_obj=jup)   # ★ 도착 직후 관성 전환
say("가스로만 이루어진 거대 행성", 5.0)

# 갈릴레이 위성 4개 (1610년 갈릴레오가 본 그것)
for nm in ("Io", "Europa", "Ganymede", "Callisto"):
    try:
        s = Satellite(getattr(Satellite.SatelliteName, nm))
        s.setIntensity(1.0, Anim(1.0))
        s.setOrbitIntensity(0.9, Anim(1.0))
        s.setLabelIntensity(1.0, Anim(1.0))
        s.setScale(14.0, Anim(1.5))              # ★ 크게 (7 은 안 보였음)
    except Exception as ex:
        print("   위성 %s: %s" % (nm, ex))
sleep(4.0)
say("갈릴레오가 1610년에 본 네 개의 점", 5.0)
say("이 점들이 목성을 돈다는 사실이 — 지동설의 증거가 됐다", 7.0)

# (관성 프레임 전환은 도착 직후 fly_to_planet 안에서 이미 끝났다 — 여기선 시간만 흘린다)

# ★ 시간가속 범위: 위성 주기는 이오 1.77 / 유로파 3.55 / 가니메데 7.15 / 칼리스토 16.7일
#   → +2일은 너무 짧아 바깥 위성이 거의 안 움직인다. **+8일을 50초에** = 이오 4.5바퀴,
#     유로파 2.3, 가니메데 1.1, 칼리스토 0.5 → '안쪽이 빠르다'가 눈에 보이는 범위.
say("시간을 감아 보자 — 8일치를 1분 만에")
dm.setDateTime(2026, 1, 23, 12, 0, 0, tz, Anim(50.0))
sleep(51.0)
say("안쪽일수록 빠르게 — 케플러의 법칙", 6.0)

# ── 막3 : 토성 (고리는 구도가 8할) ───────────────────────────
print("\n[막3] 토성")
hard_reset_to_ground()
light(1.8)
say("세 번째 — 고리를 가진 행성")
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(1.5))   # 배경 검정 = 대비
db.data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
sleep(5.5)
sat = Planet(Planet.PlanetName.Saturn)
shadows_off(sat)
p = cam.positionLBR
cam.setPositionLBR(Vec(p.x, 75.0, p.z), Anim.cubic(5.0), -1)   # 고리면만 개방(B=75), R 은 도킹값 유지
# ⚠️ [2026-08-03 정정] 예전엔 여기서 R×0.7 로 당겼는데 그건 고리를 잘라먹는다.
#   A고리 바깥지름 = 2.27 토성반지름(옛 '4.6'은 오기). R=5 → 고리 시직경 54°(적당),
#   R=3.9 → 72°(이미 잘림, 실측 스샷). **고리 쇼에서 줌은 금지 — 구도(B)로만 승부한다.**
sleep(5.5)
cam.setTargetHeight(30.0, Anim(1.5)); sleep(1.5)
make_caption(20.0)                              # 행성 프레임 자막 규칙
say("토성", 4.0)
say("고리는 얼음과 바위 조각 — 가장 큰 것도 집 한 채 크기", 6.0)

base_l = cam.positionLBR.x
for d in (70.0, 140.0):
    q = cam.positionLBR
    cam.setPositionLBR(Vec(base_l + d, q.y, q.z), Anim(5.0), -1)
    sleep(4.2)
say("두께는 겨우 10미터 남짓", 5.0)

# ── 막4 : 명왕성 (끝) ────────────────────────────────────────
print("\n[막4] 명왕성")
hard_reset_to_ground()
light(1.8)
say("마지막 — 태양계의 변두리로", 4.0)
hp = db.data(Data.Type.DwarfPlanetType, "Pluto")
if hp is not None:
    hp.action(Action.Type.FadeTo).trigger()
    sleep(5.0)
    pl = DwarfPlanet(DwarfPlanet.DwarfPlanetName.Pluto)
    shadows_off(pl)
    try:
        pl.setTerrainModel(DwarfPlanet.TerrainModel.NewHorizons)   # 진짜 '하트' 표면
    except Exception as ex:
        print("   terrainModel:", ex)
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    make_caption(20.0)
    say("명왕성")
    zoom_in()
    sleep(3.0)
    say("2015년, 뉴호라이즌스가 처음 얼굴을 보여줬다", 6.0)
    say("표면의 하트 — 질소 얼음 평원", 6.0)

# ── 막5 : 귀환 ───────────────────────────────────────────────
print("\n[막5] 귀환")
hard_reset_to_ground()
light(3.0)
say("빛으로 5시간 반. 그게 태양계의 끝이다", 6.0)
say("그리고 우리는 그 안쪽 세 번째 행성에 산다", 6.0)
t1.setIntensity(0.0, Anim(2.0)); sleep(2.5)
print("\n=== 쇼 종료 ===")

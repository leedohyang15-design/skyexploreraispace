# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 ⑤ — "달"  (약 7분)
#
#    막1  Q1. 달은 왜 모양이 변하나?      → 위상 수동 제어 타임랩스(신월→보름→그믐)
#    막2  Q2. 저 얼룩은 뭔가?             → 달 표면으로 가서 탐사선 지도 교체
#    막3  Q3. 왜 늘 같은 면만 보이나?     → 표면을 돌며 동주기 자전 이야기
#    A.   다시 지상에서 올려다보기
#
#  ※ 검증된 규칙만 사용:
#     · 지상 클로즈업은 카메라 줌이 아니라 `setScale`(원본×배율, 원본 먼저 읽기)
#     · 위상 = `setManualMoonPhase(True)` + `setMoonAge(0→29.5, Anim)` (한 번에 한 사이클)
#       ⚠️ 쇼 끝에 setManualMoonPhase(False) 로 되돌리지 말 것 — 그림자가 깜빡인다
#     · 달 접근 = `data(SatelliteType,"Moon").action(FadeTo)` → 그림자 OFF 3세터 → 줌
#     · 표면 지도 = `Satellite.setTerrainModel(...)` (Clementine/LROC 등 탐사선별)
#     · 자막 기본 높이 CAPTION_H=12 / 이전 자막은 반드시 끄기
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




# ══════════════════════════════════════════════════════════════
#  막 0 — 지상에서 달 올려다보기
# ══════════════════════════════════════════════════════════════
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night_slow(y=2026, mo=3, d=5, h=12, mi=0)     # 보름 근처 밤(21시=12 UTC)
make_caption(1.0)

moon = Satellite(Satellite.SatelliteName.Moon)
moon.setIntensity(1.0, Anim(0.0))
try:
    orig_scale = moon.scale            # ★ 지상 확대용 — 원본을 '먼저' 읽어둔다
except Exception:
    orig_scale = 1.0
print("달 원본 scale =", orig_scale)

cam.setOrientationH(90.0, Anim(0.0))   # 동쪽 하늘 근처
cam.setTargetHeight(30.0, Anim(0.0))
light(2.5)
say("3월의 밤, 동쪽 하늘", 4.5)
say("맨눈으로 볼 수 있는 유일한 '다른 세계'", 5.5)

# 지상 클로즈업은 카메라 줌이 무효 → setScale 로 개체를 키운다
say("조금 당겨서 보자")
moon.setScale(orig_scale * 12.0, Anim.cubic(4.0))
sleep(5.0)

# ══════════════════════════════════════════════════════════════
#  막 1 — Q1. 달은 왜 모양이 변하나? (위상 타임랩스)
# ══════════════════════════════════════════════════════════════
print("\n[막1] Q1 — 위상")
say("질문 하나. 달은 왜 매일 모양이 달라지나?", 6.0)
say("달이 변하는 게 아니라 — 햇빛을 받는 각도가 변하는 것", 6.5)

try:
    moon.setManualMoonPhase(True)      # 위상 수동 제어 ON
    moon.setPlanetShineStrength(0.15, Anim(1.5))   # 그늘면을 어둡게 = 초승달 선명
    sleep(1.5)
    moon.setMoonAge(0.0, Anim(0.0))    # 신월에서 시작
    sleep(1.0)
    say("신월 — 보이지 않는 달")
    sleep(3.0)
    say("한 달을 30초에 감아 보면")
    moon.setMoonAge(29.5, Anim(30.0))  # ★ 한 번의 호출로 한 사이클
    sleep(31.0)
    say("초승 → 상현 → 보름 → 하현 → 그믐", 6.0)
    # 보기 좋은 위상에서 멈춤 (⚠️ setManualMoonPhase(False) 로 되돌리지 않는다)
    moon.setMoonAge(11.0, Anim(4.0))
    sleep(4.5)
except Exception as ex:
    print("   위상 제어 예외:", ex)

# ══════════════════════════════════════════════════════════════
#  막 2 — Q2. 저 얼룩은 뭔가? (달 표면으로)
# ══════════════════════════════════════════════════════════════
print("\n[막2] Q2 — 표면")
say("두 번째 질문. 달 표면의 저 얼룩은 뭘까?", 6.0)
say("가까이 가 보자")
sleep(2.0)

moon.setScale(orig_scale, Anim(2.0))   # 지상 확대 원복(원본값으로! 1.0 하드코딩 금지)
sleep(2.5)

h = db.data(Data.Type.SatelliteType, "Moon")
if h is not None:
    h.action(Action.Type.FadeTo).trigger()
    sleep(5.5)
    # 표면을 보여주는 장면 = 그림자 OFF 3세터 (운영 표준)
    moon.setShadowStrength(0.0, Anim(1.5))
    moon.setShadowContrast(0.0, Anim(1.5))
    moon.setPlanetShineStrength(1.0, Anim(1.5))
    cam.setTargetHeight(30.0, Anim(1.5))
    sleep(2.0)
    make_caption(20.0)                 # 행성 프레임 자막
    say("달 표면")
    zoom_in()                          # 절대타겟 + 선형 + 겹치기
    sleep(2.0)

    say("어두운 부분은 '바다' — 물이 아니라 굳은 용암", 7.0)
    say("밝은 부분은 고지대. 크레이터가 빽빽하다", 6.5)

    # 탐사선별 지도 교체 (검증된 TerrainModel)
    for mdl, cap in (("Clementine", "클레멘타인 탐사선의 지도"),
                     ("LROC", "LRO 정찰위성의 고해상도 지도")):
        try:
            moon.setTerrainModel(getattr(Satellite.TerrainModel, mdl))
            say(cap)
            sleep(6.0)
        except Exception as ex:
            print("   지도 %s: %s" % (mdl, ex))

    # 크레이터 기복 강조
    try:
        moon.setElevationScale(6.0, Anim(3.0))
        say("높이를 과장해 보면 — 충돌의 흔적", 6.0)
    except Exception as ex:
        print("   elevationScale:", ex)

# ══════════════════════════════════════════════════════════════
#  막 3 — Q3. 왜 늘 같은 면만 보이나? (동주기 자전)
# ══════════════════════════════════════════════════════════════
print("\n[막3] Q3 — 동주기 자전")
say("세 번째 질문. 우리는 왜 늘 달의 '같은 면'만 볼까?", 7.0)

# 표면을 옆으로 돌아 본다 (FadeTo 프레임에서 L 스윕 — 토성 고리 스윕과 같은 방식)
base_l = cam.positionLBR.x
for d in (60.0, 120.0, 180.0):
    q = cam.positionLBR
    cam.setPositionLBR(Vec(base_l + d, q.y, q.z), Anim(5.0), -1)
    sleep(4.2)                          # sleep < anim = 겹쳐서 매끄럽게
sleep(1.5)

say("달은 자전을 한다 — 다만 공전과 주기가 똑같다", 7.0)
say("한 바퀴 도는 데 27.3일, 지구를 도는 데도 27.3일", 7.0)
say("그래서 지구에서는 늘 같은 얼굴만 보인다", 7.0)
say("뒷면을 처음 본 건 1959년, 소련의 루나 3호였다", 7.0)

# ══════════════════════════════════════════════════════════════
#  막 4 — 다시 지상으로
# ══════════════════════════════════════════════════════════════
print("\n[막4] 귀환")
hard_reset_to_ground(y=2026, mo=3, d=5, h=12)
moon = Satellite(Satellite.SatelliteName.Moon)
moon.setIntensity(1.0, Anim(0.0))
cam.setOrientationH(90.0, Anim(0.0))
light(3.0)

say("다시, 3월의 밤하늘", 5.0)
say("38만 km 떨어진 돌덩이 하나가", 6.0)
say("밀물과 썰물을 만들고, 지구의 자전축을 붙잡아 준다", 7.5)
say("우리가 아는 계절도, 그 덕분이다", 6.5)
t1.setIntensity(0.0, Anim(2.0)); sleep(2.5)
print("\n=== 쇼 종료 ===")

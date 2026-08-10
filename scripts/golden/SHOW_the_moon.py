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
  try:
      h.action(Action.Type.FadeTo).trigger()
      sleep(5.5)
      # 표면을 보여주는 장면 = 그림자 OFF 3세터 (운영 표준)
      moon.setShadowStrength(0.0, Anim(1.5))
      moon.setShadowContrast(0.0, Anim(1.5))
      moon.setPlanetShineStrength(1.0, Anim(1.5))
      cam.setTargetHeight(30.0, Anim(1.5))
      sleep(2.0)
      make_caption(20.0)                 # 도킹 직후(R≈4)에는 distance 20 이 맞다
      say("달 표면")

      # ⚠️⚠️ 줌은 '얕게'. 깊게 당기면(R<2) distance 20 자막이 달 뒤로 넘어가 사라진다.
      zoom_in((1.4, 1.9, 2.4))           # R ≈ 4/2.4 ≈ 1.7
      sleep(1.5)

      # ★★ 줌 뒤에는 자막을 카메라 쪽으로 되돌린다(dist 1.0 + size 0.052).
      #    실측 사고: 줌 후에도 distance 20 을 유지했더니 자막이 달 반대편에 놓여
      #    막2 후반부터 막3 전체가 '자막 없는 화면'이 됐다.
      make_caption(1.0)
      say("어두운 부분은 '바다' — 물이 아니라 굳은 용암", 6.0)
      say("밝은 부분은 고지대. 크레이터가 빽빽하다", 5.5)

      # 탐사선 지도 — ⚠️ 타일 로딩이 느리다. 2장 돌리면 '무변화 15초'가 된다 → 1장만.
      try:
          say("LRO 정찰위성이 찍은 고해상도 지도로 바꿔 본다")
          moon.setTerrainModel(Satellite.TerrainModel.LROC)
          sleep(5.0)
      except Exception as ex:
          print("   지도 LROC:", ex)

      # ★ 지루함의 해법 = 대비(OFF→ON). 그림자를 잠깐 켜면 크레이터 그림자가 확 진다.
      try:
          say("햇빛을 비스듬히 들여보면")
          moon.setShadowStrength(1.0, Anim(2.5))
          moon.setShadowContrast(1.0, Anim(2.5))
          moon.setPlanetShineStrength(0.1, Anim(2.5))
          sleep(3.5)
          say("크레이터 하나하나가 그림자를 드리운다", 5.0)
          say("전부 충돌의 흔적 — 대기가 없어 지워지지 않는다", 6.0)
          moon.setShadowStrength(0.0, Anim(2.0))      # 다시 전면 밝게(운영 표준)
          moon.setShadowContrast(0.0, Anim(2.0))
          moon.setPlanetShineStrength(1.0, Anim(2.0))
          sleep(2.5)
      except Exception as ex:
          print("   그림자 A/B:", ex)
  except Exception as ex:
    print("   막2 예외(무시하고 진행):", ex)

# ══════════════════════════════════════════════════════════════
#  막 3 — Q3. 왜 늘 같은 면만 보이나? (동주기 자전)
# ══════════════════════════════════════════════════════════════
print("\n[막3] Q3 — 동주기 자전")
say("세 번째 질문. 우리는 왜 늘 달의 '같은 면'만 볼까?", 7.0)

# ⚠️⚠️ 여기서 두 번 실패했다. 기록:
#   v1: L 스윕 단독 → 달은 **북극 상공 도킹(B≈90)** 이라 L 공전이 '극축 제자리 스핀' = 노트상 불가 케이스.
#   v2: B 굴림 단독(`setPositionB`) → 죽진 않지만 **고도만 위아래로 오르내려** 공전으로 안 보인다(사용자 지적).
#   ✅ v3 정답 = **두 단계**. ① 먼저 B 를 90→20 으로 내려 '가스행성 옆도킹'과 같은 자세를 만든 뒤
#      ② 그 자세에서 L 스윕 = 옆에서 한 바퀴 도는 진짜 공전. (토성/목성에서 L 스윕이 되는 조건이 바로 B≈20.)
try:
    # ★ 프레임 = 달의 EquatorialSynchronous (HUD 가 "Moon, Equatorial Sync" 로 확인해 준 그 프레임).
    #   위치·재조준을 같은 포트로 통일해야 프레임 점프가 없다.
    mp = moon.portId(Satellite.SatellitePort.EquatorialSynchronous)

    def reaim(a=1.0):
        """★★ 말머리 레시피의 '② 재조준'. 빠지면 카메라만 돌고 시선이 안 따라가
           대상이 화면에서 흘러나가 **돔 한가운데로 밀리고 이상하게 구른다**(실측 사고 2회).
           ⚠️⚠️ 여기에 `setTargetHeight` 를 같이 넣지 말 것 — **TargetHeight 가 곧 돔 틸트**라
           공전 중에 반복하면 3스텝마다 돔이 까딱거린다(실측 지적). 틸트는 '한 번만'."""
        cam.setOrientationSmoothXYZR(Vec4(0, 0, 0, 0), Anim(a), mp)

    def tilt30():
        """🎯 관람 정위치 30 — 자세를 바꾼 직후 '한 번만'. 같은 값 재호출은 no-op 이라 지글로 우회."""
        cam.setTargetHeight(29.9, Anim(0.5)); cam.setTargetHeight(30.0, Anim(0.5))

    p = cam.positionLBR
    print("   현재 L=%.1f B=%.1f R=%.3f" % (p.x, p.y, p.z))

    # ✅ [2026-08-10 사용자 돔 확인] 아래 자세 변경 구간의 암전 처리 = 깔끔하게 동작("암전 잘됐고").
    say("달의 옆으로 돌아가 보자")
    sleep(2.2)

    # ⚠️⚠️ 자세 변경(B 90→20)·재조준·풀백은 '슬루'라 그대로 보여주면 너저분하다(실측 지적).
    #   → 우리 표준: **자세를 바꾸는 구간은 암전 속에서 끝내고, 정렬이 끝난 뒤 페이드인.**
    #   (기존 'Target 재정렬은 암전에서' 규칙의 확장 — B 이동·프레임 전환도 같다.)
    dark(1.8)

    cam.setPositionLBR(Vec(p.x, 20.0, p.z), Anim.cubic(5.0), mp)   # ① 극 위 → 적도 옆
    sleep(5.2)
    reaim(1.2); tilt30(); sleep(1.6)                                # 자세 바꾼 직후 재조준 + 틸트 1회

    # ★ 공전 전 살짝 풀백 — 너무 붙어 있으면 도는 동안 달이 화면을 다 먹는다(실측 지적).
    r0 = cam.positionLBR.z
    cam.setPositionR(r0 * 1.8, Anim.cubic(2.5), mp); sleep(2.8)
    reaim(0.8); sleep(1.0)
    q = cam.positionLBR
    print("   공전 준비 완료 L=%.1f B=%.1f R=%.3f (암전 중 정렬)" % (q.x, q.y, q.z))

    light(2.4)                                                      # 정렬 끝난 뒤 페이드인

    # ② 스텝 오빗 — 15° 스텝 + 3스텝마다 '시선만' 재조준. 틸트는 건드리지 않는다.
    say("이제 달을 한 바퀴 돌아 뒷면으로")
    for i in range(1, 25):                                          # 24 × 15° = 360°
        cam.setPositionLBR(Vec(q.x + 15.0 * i, 20.0, q.z), Anim(0.7), mp)
        sleep(0.55)                                                 # sleep < anim = 겹쳐서 매끄럽게
        if i % 3 == 0:
            reaim(0.6)
            r = cam.positionLBR
            print("   공전 %3.0f°  L=%.1f B=%.1f R=%.3f" % (15.0 * i, r.x, r.y, r.z))
    reaim(1.5); sleep(1.5)
except Exception as ex:
    print("   공전 예외(무시하고 진행):", ex)

say("지구에서는 절대 볼 수 없는 면 — 달의 뒷면이다", 6.5)
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

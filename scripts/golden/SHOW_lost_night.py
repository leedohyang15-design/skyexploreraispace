# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════
#  장편 시뮬레이션 ④ — "사라진 밤하늘"  (약 7분)
#  Q1. 도시에서 별이 몇 개나 보이나?  → 광공해 단계별 감광
#  Q2. 그럼 원래는 어떻게 보였나?     → 어두운 곳으로 이동(관측지 이름 이동)
#  Q3. 우리가 잃은 건 뭔가?           → 은하수 + 별색 + 유성
#
#  태우는 규칙: 관측지 이름 이동(CityType/MountainType) + 좌표 안정 폴링 ·
#              광공해는 Stars/Galaxy 를 직접 감광(setLightPollutionIntensity 만으론 안 됨) ·
#              별 채도 · 유성우 · 끊김 없는 복귀
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

def make_caption(dist=1.0):
    """자막 생성 (지상=distance 1.0 / 행성 프레임=20)"""
    global t1
    t1 = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
    t1.setPosition(Vec(0, 25, 0))
    if dist == 1.0: t1.setSize(0.052)          # 행성 프레임에선 setSize 금지
    t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(dist, Anim(0.0))
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

def fly_to_planet(name, caption, zoom=True):
    """행성 GoTo 비행 → 도착 폴링 → Target 30 → 줌. B 는 손대지 않는다."""
    say(caption)
    db.data(Data.Type.PlanetType, name).action(Action.Type.GoTo).trigger()
    print("   %s 로 비행" % name)
    wait_arrival(dock_r=100.0)
    cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
    if zoom: zoom_in()

def wait_place_settle(max_sec=30, settle=2):
    """★ 관측지 이동도 애니메이션 — 좌표가 멈출 때까지 기다린다"""
    prev, stable = None, 0
    for s in range(max_sec):
        sleep(1.0)
        try:
            q = Place2D(Place2D.Place2DName(0)).position
            cur = (round(q.x, 3), round(q.y, 3), round(q.z, 1))
        except Exception:
            continue
        if prev is not None and cur == prev: stable += 1
        else: stable = 0
        prev = cur
        if stable >= settle: return cur
    return prev


def goto_place(dtype, name, caption):
    h = db.data(getattr(Data.Type, dtype), name)
    if h is None:
        print("   ⚠️ %s '%s' 조회 실패" % (dtype, name)); return False
    say(caption)
    h.action(Action.Type.GoTo).trigger()
    pos = wait_place_settle()
    cam.setTargetHeight(30.0, Anim(1.0))
    if pos: print("   → %s: %.3f / %.3f / %.0fm" % ((name,) + pos))
    return True


# ── 막0 : 도시의 밤 ──────────────────────────────────────────
SceneGraph().reset(1); sleep(1.6)
uni.setGlobalIntensity(0.0, Anim(0.0))
ground_night_slow(y=2026, mo=8, d=1, h=13, mw=0.0)     # 여름밤, 은하수 꺼진 채 시작
make_caption(1.0)
stars  = Stars(Stars.StarsName.StarrySky)
galaxy = Galaxy(Galaxy.GalaxyName.MilkyWay)
earth  = Planet(Planet.PlanetName.Earth)

stars.setIntensity(0.40, Anim(0.0))                    # 대도시 = 밝은 별만
try: earth.setLightPollutionIntensity(1.0, Anim(0.0))
except Exception as ex: print("   lightPollution:", ex)
light(2.5)

say("서울, 여름밤 10시", 5.0)
say("별이 몇 개나 보이나?", 5.0)

# ── 막1 : Q1 — 광공해 단계별로 되감기 ────────────────────────
print("\n[막1] 광공해 되감기")
say("도시를 하나씩 지워 보자", 4.0)

say("도시 외곽")
try: earth.setLightPollutionIntensity(0.6, Anim(3.0))
except Exception: pass
stars.setIntensity(0.60, Anim(3.0))
galaxy.setIntensity(0.10, Anim(3.0))
sleep(5.0)

say("시골 마을")
try: earth.setLightPollutionIntensity(0.3, Anim(3.0))
except Exception: pass
stars.setIntensity(0.80, Anim(3.0))
galaxy.setIntensity(0.35, Anim(3.0))
sleep(5.0)

say("그리고 — 불빛이 하나도 없는 곳")
try: earth.setLightPollutionIntensity(0.0, Anim(4.0))
except Exception: pass
stars.setIntensity(1.0, Anim(4.0))
galaxy.setIntensity(0.9, Anim(4.0))
galaxy.setExposure(1.8, Anim(4.0))                     # 은하수 노출 ↑
sleep(6.0)
say("이게 원래 밤하늘이다", 6.0)

# ── 막2 : Q2 — 진짜 어두운 곳으로 (관측지 이동) ──────────────
print("\n[막2] 어두운 곳으로")
say("두 번째 질문. 지금도 이런 하늘이 남아 있나?", 5.0)

goto_place("MountainType", "Everest", "에베레스트 — 해발 8,800m")
sleep(7.0)
say("공기가 얇을수록 별은 또렷해진다", 6.0)

stars.setPointSaturation(4.5, Anim(4.0))               # 별 색이 드러남
sleep(4.5)
say("그리고 별에는 — 색이 있다", 6.0)

# ── 막3 : Q3 — 잃어버린 것들 ─────────────────────────────────
print("\n[막3] 은하수와 유성")
say("우리 은하를 옆에서 본 단면 — 은하수", 6.0)
galaxy.setExposure(2.2, Anim(3.0))
sleep(4.0)

# 유성 하나
try:
    ss = ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)
    ss.setRepresentationType(ShootingStar.Model.Gradient)
    ss.setBrightness(1.0, Anim(0.0))
    ss.setTrailLength(1.2, Anim(0.0))
    ss.setStartPosition(Vec2(40.0, 70.0))
    ss.setArrivalPosition(Vec2(-30.0, 25.0))
    say("그리고 가끔, 이런 것도")
    ss.setAdvancing(0.0, Anim(0.0)); sleep(0.4)
    ss.setAdvancing(1.0, Anim(2.5)); sleep(3.5)
except Exception as ex:
    print("   유성:", ex)
sleep(2.0)

# ── 막4 : 다시 도시로 (대비) ─────────────────────────────────
print("\n[막4] 다시 도시로")
say("이제 다시, 도시로 돌아가 보자", 5.0)
goto_place("CityType", "Tokyo", "도쿄")
try: earth.setLightPollutionIntensity(1.0, Anim(4.0))
except Exception: pass
stars.setIntensity(0.40, Anim(4.0))
galaxy.setIntensity(0.0, Anim(4.0))
sleep(6.0)

say("같은 하늘, 같은 시각인데", 5.0)
say("은하수는 사라졌다", 6.0)
say("세계 인구의 3분의 1은 평생 은하수를 못 본다", 7.0)
say("잃어버린 건 별이 아니라 — 어둠이다", 7.0)
t1.setIntensity(0.0, Anim(2.0)); sleep(2.5)
print("\n=== 쇼 종료 ===")

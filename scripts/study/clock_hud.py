# -*- coding: utf-8 -*-
"""
clock_hud.py — Clock 클래스 첫 예제: 돔 시계 HUD + 시간가속 (2026-07-20, 완본 미개척 클래스)
★ NGC 는 이 빌드서 접근 불가 확정(ngc_deepsky v1~v3) → 완본 목록의 다음 미개척 = Clock.
★ Clock = 아날로그 시계 위젯(문자판+시침/분침/초침). InsertText 처럼 카메라에 붙이는 HUD → 확실히 렌더.
  · 렌더 열쇠 = `setModelset(Clock.Modelset.SystemClock001)` (Bolide 의 setModel 처럼, 모델 없으면 안 그려질 수 있음).
  · 붙이기 = `cam.addChild(clock.id, FixedForeground)` (InsertText 패턴) + setPosition/setSize/setIntensity.
  · 바늘색 = setHoursHandColor/setMinutesHandColor/setSecondsHandColor(Vec3) · setDisplaySecondsHand(bool).
★ 데모: 밤하늘 위에 시계 HUD 표시 → **DateManager 시간가속** → 바늘이 도는지(시뮬 시간 반영 여부) 확인 = 볼거리 + 판정.
  Clock API(완본): setModelset/setParent/addChild·setPosition·setSize·setDistance·setIntensity·
   setBackgroundColor/Texture·setForegroundColor/Texture·setHours/Minutes/SecondsHandColor/Texture·setTimezoneName.
★ ⚠️ 값 감각(size/distance/position)은 첫 실측이라 미지수 → 안 보이면 로그+스샷으로 튜닝.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대: 지상 밤하늘 (시계 HUD 배경) ───────────────────────
print("무대: Clock HUD + 시간가속")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF)")
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(지면 OFF)")
feat(earth, "setElevationScale", 0.0)
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))

# 청주 밤, 남쪽 하늘
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.5)   # 청주 밤 22시
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

# ── ★ Clock 생성 + 렌더 세팅 ───────────────────────────────
clk = None
for nm in ("Clock001", "Clock01", "Clock1"):
    if hasattr(Clock.ClockName, nm):
        try: clk = Clock(getattr(Clock.ClockName, nm)); print("   Clock enum = %s" % nm); break
        except Exception as e: print("   %s 생성 실패: %s" % (nm, e))
if clk is None:
    try: clk = Clock(Clock.ClockName(1)); print("   Clock(1) 생성")
    except Exception as e: print("   Clock 생성 실패: %s" % e)

if clk is not None:
    # ★ 렌더 열쇠: 모델셋(문자판+바늘 모델). 없으면 안 그려질 수 있음.
    if hasattr(Clock, "Modelset") and hasattr(Clock.Modelset, "SystemClock001"):
        feat(clk, "setModelset", Clock.Modelset.SystemClock001, label="(★ 시계 모델셋)")
    # 카메라 HUD 로 붙이기 (InsertText 패턴)
    try:
        cam.addChild(clk.id, Camera.CameraPort.FixedForeground); print("   ✓ addChild(FixedForeground)")
    except Exception as e:
        print("   ✗ addChild 실패: %s → setParent 시도" % e)
        feat(clk, "setParent", cam.id, label="(setParent 폴백)")
    # 위치/크기/거리 (미지수 → 중앙 하단쯤, 큼직하게)
    feat(clk, "setPosition", Vec(0, 40, 0), Anim(0.0), label="(방위0/높이40)")
    feat(clk, "setDistance", 1.0, Anim(0.0))
    feat(clk, "setSize", 0.5, Anim(0.0), label="(크기 0.5 — 안 보이면 튜닝)")
    # 색/바늘
    feat(clk, "setBackgroundColor", Vec(0.05, 0.08, 0.15), Anim(0.0), label="(문자판 남색)")
    feat(clk, "setForegroundColor", Vec(1.0, 1.0, 0.9), Anim(0.0), label="(눈금 흰)")
    feat(clk, "setHoursHandColor", Vec(1.0, 1.0, 1.0), Anim(0.0))
    feat(clk, "setMinutesHandColor", Vec(1.0, 1.0, 1.0), Anim(0.0))
    feat(clk, "setSecondsHandColor", Vec(1.0, 0.4, 0.3), Anim(0.0), label="(초침 빨강)")
    feat(clk, "setDisplaySecondsHand", True, label="(초침 표시)")
    feat(clk, "setTimezoneName", "Asia/Seoul", label="(시간대)")
    feat(clk, "setIntensity", 0.0, Anim(0.0))       # 페이드인 위해 0 시작

# 자막
txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))

uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── 시계 페이드인 ───────────────────────────────────────────
narr("돔 위의 시계 — 지금은 청주의 밤", 3.5)
if clk is not None:
    feat(clk, "setIntensity", 1.0, Anim(2.0)); sleep(2.3)
narr("이 시계는 시뮬레이션 시각을 가리킨다", 4.0)

# ── ★ 시간가속 → 바늘이 도나? ──────────────────────────────
narr("시간을 빠르게 흘려보자 — 바늘이 돌아간다", 3.5)
dm.setDateTime(2026, 8, 2, 13, 0, 0, tz, Anim(24.0)); sleep(25.0)   # +24시간을 24초에 = 바늘 하루치 회전
narr("하루가 지나는 동안 하늘도 함께 돌았다", 4.5)

# ── 정리 ────────────────────────────────────────────────────
dm.stop()
narr("Clock — 돔 위의 시계 위젯", 4.0)
if clk is not None:
    feat(clk, "setIntensity", 0.0, Anim(1.5))
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★시계(문자판+바늘)가 화면에 뜨나 — 로그 'Clock enum/모델셋/addChild' 확인 "
      "②시간가속(+24h/24초) 때 바늘이 실제로 도나(시뮬 시각 반영) 아니면 멈춰있나(실시각) "
      "③크기/위치 적당한가(size 0.5, 높이40) — 너무 크/작/치우쳤으면 목표값 알려줘 "
      "④안 보이면 = 모델셋/addChild 중 뭐가 실패했는지 로그로(그거 보고 setParent 등으로 교체)")

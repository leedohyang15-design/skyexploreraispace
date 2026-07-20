# -*- coding: utf-8 -*-
"""
complex_demo_fixed.py — [v22] 원상 복구 3종 + 대기 OFF 별 우선 (사용자 지시)
  ① 태양계 조망: 시작 시각 변경 제거(12월 세팅이 배치를 바꿔 망침) + 원래 구도 Vec(0,45,30) 복원.
  ② 토성/은하수 자막: 행성 프레임(distance 20)에선 setSize(0.035)가 너무 작아 실종(v21) →
     size 기본값 유지 (지상 자막만 0.035 + distance 1.0).
  ③ 지구 도착 즉시 대기효과 OFF(atmosphere+scattering 0) — 낮이어도 별이 바로 보임(사용자 아이디어).
     밤(12/21 22UT) 세팅은 착륙 딥(암전) 속에서 — 시간 점프 회전은 딥이 가림(v17 검증).
  ④ 별자리 = 자막의 3개만 (오리온·황소·쌍둥이). enum 627개 전체 ON 금지.
  유지: GoTo 도킹(R=4)→Land 재현(273+289) — 사용자 확인 성공!
  v3 실측: 토성 이탈 풀백 성공(4.21Gm)! 단 Place2D 좌표만으론 지상 복귀 불가 —
  카메라가 토성 프레임에 남음 → 복귀 = 암전 속 reset(1) 후 지상 전체 재세팅.
  정정: FadeTo 의 실체 = 'Fade out→순간이동→Fade in' (내부 로그 증거) — 페이드 전환임.
  연속 비행은 '같은 프레임 안 R/L 애니메이션'으로만 가능(실측) → 접근/이탈 비행을 직접 연출.
  몽블랑: MountainType FadeTo = 상공 191km Terrain View(실측) → 지상 밤하늘은 Place2D 좌표로.
====================================================================
원본 오류 (우리 CLAUDE.md 실측 기준):
  ❶ `from Initialization import *` 누락 → DateManager 에서 NameError (즉사)
  ❷ `Insert2D(...).reserved = False` → 속성 직접 대입 금지 + reserved 는 시스템 예약 (즉사)
  ❸ `Planet.PlanetName.Earth` 멤버 미확정 → 인덱스 생성 Planet(PlanetName(2)) 로 (안전)
  ❹ DefaultTimeZone = UTC 인데 21시 지정 → 실제론 아침! UT 변환 필요
  ❺ FadeTo 후 sleep(1.0) → 도착에 4초 필요 + FadeTo 가 밝기를 도로 올림(클램프 필요)
  ❻ AdvancedCamera FreeFly/takeOffOn → 스크립트에서 전부 무효(실측) — 제거
  + 몽블랑 지상 씬에 '지상 체크리스트'(지구 본체+대기+태양) 누락 → 하늘 검게 나옴
  + setTarget(Vec2) 의미 미해독 → FadeTo 기본 Target 30(관람 정위치) 그대로 사용
  + <BR/> 태그 미확정 → 한 줄 텍스트로
"""
from skyExplorer import *
from studio import *
from Initialization import *          # ❶ DateManager 등 매니저는 여기서

def wait_arrival(cam, timeout=60.0):
    """도착 감지 v2 — ① 움직임을 먼저 확인 ② 정지(변화<0.1%) 3연속이어야 도착.
       GoTo 는 출발이 느려서 초반 정지를 도착으로 오판하면 안 됨 (v7 실측)."""
    last = None
    moved = False
    still = 0
    t = 0.0
    while t < timeout:
        sleep(1.0); t += 1.0
        try:
            r = cam.positionLBR.z
        except Exception:
            continue
        if last is not None:
            rate = abs(r - last) / max(abs(last), 1e-9)
            if rate > 0.01:
                moved = True; still = 0
            elif moved and rate < 0.001:
                still += 1
                if still >= 3:
                    break
        last = r
    print("   도착 감지 (%.0f초, moved=%s)" % (t, moved))

def blackout_clamp(uni, sec):         # FadeTo/리셋의 밝기 되살아남 억제 (실측 확정 패턴)
    for _ in range(int(sec / 0.2)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

# ── 1) 초기화 ───────────────────────────────────────────────
print("초기화...")
try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:60])
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(30.0, Anim(0.0))   # ★ 시작부터 Target 30 고정 (사용자 지시)
sleep(0.5)
# v22: 시각 변경은 여기서 안 함! (v20 의 12월 세팅이 태양계 배치를 바꿔 조망을 망침)
#   밤 세팅은 착륙 딥(암전) 속에서 — 낮이어도 별은 '대기효과 OFF'로 즉시 보임(사용자 아이디어).
dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")   # = UTC (실측)

# ── 1.5) ★데이터 핸들 선확보 — 비행 중엔 DataManager 조회가 None (v7 실측) ──
DATA = {}
for key, dtype, dname in (("saturn", Data.Type.PlanetType, "Saturn"),
                          ("earth",  Data.Type.PlanetType, "Earth"),
                          ("mont",   Data.Type.MountainType, "Mont blanc"),
                          ("mw",     Data.Type.GalaxyType, "Milky Way")):
    try:
        o = DataManager.database().data(dtype, dname)
        DATA[key] = o if (o is not None and o.id != -1) else None
        print("★핸들 %s: %s" % (key, "OK" if DATA[key] else "실패"))
    except Exception as e:
        DATA[key] = None
        print("★핸들 %s 예외: %s" % (key, repr(e)[:40]))

# ── 2) 태양계 조망 (태양 황도 포트 기준 — 우주 뷰) ────────────
print("태양계 뷰...")
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun.setIntensity(1.0, Anim(0.5))
for i in range(8):
    p = Planet(Planet.PlanetName(i))
    p.setIntensity(1.0, Anim(0.5))
    p.setOrbitIntensity(1.0, Anim(0.5))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))

sun_port = sun.portId(IndividualStar.IndividualStarPort.Ecliptic)
cam.setPositionLBR(Vec(0.0, 45.0, 30.0), Anim(3.0), sun_port)   # 원래 구도 복원 (R=30 AU, B=45°)
sleep(3.5)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
print(">>> 태양계 조망 (8초)")
sleep(8.0)

# ── 3) 토성 — GoTo 진짜 비행 + 검증 줌 ───────────────────────
print("🚀 토성으로 비행! (GoTo — 연속 비행, 도착 감지 폴링)")
DATA["saturn"].action(Action.Type.GoTo).trigger()
wait_arrival(cam)                      # GoTo 도착 = R≈5 토성반지름 도킹 (실측)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setText("토성 Saturn — 지구에서 약 14억 km")
t1.setPosition(Vec(0, 55, 0))          # 높이 55 = 자막 표준 (0=지평선, 90=천정)
# ⚠️ 행성 프레임(distance 20)에선 setSize(0.035)가 너무 작아 안 보임(v21 리포트) → size 기본값 유지
t1.setColor(Vec(1, 0.9, 0.6)); t1.setIntensity(1.0, Anim(1.0))
t1.setDistance(20.0, Anim(0.0))        # ✅ 확정: 행성 프레임 자막 = setDistance(20)

p = cam.positionLBR                    # 검증된 화면 고정 줌 (읽은값×배율, track=-1)
if p.z > 0.01:
    cam.setPositionR(p.z * 0.5, Anim.cubic(6.0), -1)   # R 5→2.5 토성반지름: 고리 클로즈업 (원래대로)
    sleep(6.5)
print(">>> 토성 감상 (5초)")
sleep(5.0)
t1.setIntensity(0.0, Anim(0.5)); sleep(0.5)

# ★ 토성 이탈 비행 — 우주선 후진 연출 (검증된 R 애니메이션, 진짜 연속 이동!)
print("🚀 토성 이탈 — 후진 비행 (8초)")
p = cam.positionLBR
cam.setPositionR(p.z * 12.0, Anim.cubic(8.0), -1)
sleep(8.5)

# ── 4) 지구 귀환 = GoTo 착륙 (사용자 지시: 그냥 GoTo 로 가서 land!) ──
# GoTo 지구(현 관측지 행성) = 지표 R=0 까지 자동 착륙 (v9 실측) → 비행기 그대로 탑승.
print("몽블랑으로...")
for i in range(8):                     # 궤도선 끄기
    Planet(Planet.PlanetName(i)).setOrbitIntensity(0.0, Anim(0.5))

# ⚠️ Recording4 해독으로 순서 재설계:
#   ① 출발 전 setDateTime(7월→12월) = 토성 하늘이 통째로 회전('한바퀴'의 범인!) → 시각 변경은 착륙 후로.
#   ② GoTo 지구는 내부에서 Place2D 를 덮어씀(위도20/경도-90 에 착륙!) → 몽블랑 좌표도 착륙 후로.
#   비행 전엔 '회전을 유발하지 않는' 조명 계열만 미리.
earth = Planet(Planet.PlanetName(2))
earth.setIntensity(1.0, Anim(0.0))     # ★ 지상 하늘 마스터 스위치 (GoTo 내부 Turn ON bodies 와 중복 무해)
# ★v22 사용자 지시: 지구 들어오자마자 대기효과 OFF — 낮이어도 별이 바로 보이게!
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setScatteringIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
sun.setIntensity(1.0, Anim(0.0))

# ★★ Recording4 재해독 (v19 핵심 정정): GoTo 지구는 R=0 자동 착륙이 아님!
#   내부 목표 = posLBR={0, 89.999, 4} — 북극 상공 R=4 지구반지름에서 '호버'로 끝남.
#   그 뒤 R=0 은 사용자가 누른 Land 버튼이었음. Land 의 실체(녹화 41초 지점, 주석 없는 3연발):
#     cmd273: setPositionLBR(L,B 유지, R→0, 10초)   ← 하강
#     cmd289: setOrientationHPR(H 유지, pitch -90→0, 10초) ← 내려다보기→지평선으로 몸 일으키기
#     cmd305: setTarget 보정 (우린 TH30 으로 대체)
print("🚀 지구로 GoTo — 도킹(R=4 호버)까지 비행!")
DATA["earth"].action(Action.Type.GoTo).trigger()
wait_arrival(cam, timeout=60.0)        # 호버 도킹 감지 (움직임→정지 3연속)
try:
    hp = cam.positionLBR
    print("   도킹: L=%.2f B=%.2f R=%.2f (R≈4 지구반지름이면 정상)" % (hp.x, hp.y, hp.z))
except Exception:
    hp = None

# ★ Land 재현 (Recording4 의 사용자 Land 버튼 그대로)
landed = False
if hp is not None and hp.z > 0.5:
    print("🛬 Land! (하강 10초 + 몸 일으키기 10초 동시 — Recording4 해독)")
    try:
        h = cam.orientationHPR.x       # 현재 헤딩 유지 (읽기 실패 시 녹화값 180)
    except Exception:
        h = 180.0
    cam.setPositionLBR(Vec(hp.x, hp.y, 0.0), Anim.cubic(10.0), -1)   # R→0 하강
    try:
        cam.setOrientationHPR(Vec(h, 0.0, 0.0), Anim.cubic(10.0))    # pitch -90→0
    except Exception as e:
        print("   HPR 실패:", repr(e)[:50])
    # 착지 텔레메트리 (개입 없음, 관찰만)
    t = 0.0
    while t < 14.0:
        sleep(2.0); t += 2.0
        try:
            print("   [%3.0fs] R=%.3f" % (t, cam.positionLBR.z))
        except Exception:
            pass
    landed = True
    print("   착지 완료!")
    sleep(2.5)                         # 착지 직후 풍경 그대로 감상
elif hp is not None and hp.z <= 0.5:
    landed = True                      # 이미 지표 (엔진이 알아서 내린 경우)
    print("   이미 지표 도착 (R=%.2f)" % hp.z)
    sleep(2.5)

if landed:
    # 착륙 순간 낮이어도 대기 OFF 라 별이 바로 보임(사용자 아이디어).
    # 딥(암전) 속에서 몽블랑 재배치 + 겨울밤 시각 (시간 점프의 하늘 회전은 딥이 가림 — v17 검증)
    print("   착륙 보정: 몽블랑 + 겨울밤 (2초 딥 속에서)")
    uni.setGlobalIntensity(0.0, Anim(0.8)); sleep(1.0)
    place = Place2D(Place2D.Place2DName(0))
    place.setPosition(Vec(45.83, 6.86, 4808.0))
    dm.stop(); sleep(0.3)              # stop 먼저 (실측 함정)
    dm.setDateTime(2026, 12, 21, 22, 0, 0, tz, Anim(0.5))   # 몽블랑 현지 23시 = 22 UT
    earth.setAtmosphereIntensity(0.0, Anim(0.0))            # 대기 OFF 유지 (별 우선)
    earth.setScatteringIntensity(0.0, Anim(0.0))
    sleep(0.7)
else:                                  # 백업: 착륙 감지 실패 시에만 정석 복귀(암전+reset)
    print("   착륙 감지 실패 → 백업: 암전+reset 정석 복귀")
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(1.5)
    try:
        SceneGraph().reset(1); sleep(1.5)
    except Exception:
        pass
    uni.setGlobalIntensity(0.0, Anim(0.0))
    place = Place2D(Place2D.Place2DName(0))
    place.setPosition(Vec(45.83, 6.86, 4808.0))   # reset 이 초기화 → 재지정
    earth.setIntensity(1.0, Anim(0.0))
    earth.setAtmosphereIntensity(0.0, Anim(0.0))  # 대기 OFF (별 우선 — 사용자 지시)
    earth.setScatteringIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
    sun.setIntensity(1.0, Anim(0.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 12, 21, 22, 0, 0, tz, Anim(0.5))
    sleep(1.5)

cam.setTargetHeight(30.0, Anim(1.5))   # 착륙 후 관람 표준 재고정
sleep(1.7)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))   # 몽블랑 겨울 밤하늘 페이드인
sleep(2.7)

# ⚠️ 텍스트 실종 원인(v19 리포트) = setDistance(20)은 '행성 프레임' 전용 처방!
#   지상 Sky View 에선 기본 거리 1.0 이 정답 — 20이면 20배 멀어져 안 보임. → 지상 자막은 1.0.
t2 = InsertText(InsertText.InsertTextName(2))
cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
t2.setText("몽블랑 Mont Blanc — 해발 4,808 m")
t2.setPosition(Vec(0, 55, 0)); t2.setSize(0.035)
t2.setDistance(1.0, Anim(0.0))         # ★ 지상 = 기본 거리 (행성 프레임의 20 금지!)
t2.setColor(Vec(0.8, 0.9, 1.0)); t2.setIntensity(1.0, Anim(1.0))
print(">>> 몽블랑 겨울 밤하늘 (6초)")
sleep(6.0)
t2.setIntensity(0.0, Anim(0.5))

# ── 5) 별자리 + 메시에 ──────────────────────────────────────
# 사용자 확정: 자막에 나오는 3개만 (오리온·황소·쌍둥이). enum 전체 627개 ON 금지!
print("별자리... (자막의 3개: 오리온·황소·쌍둥이)")
cons = []
for cn in ("Ori", "Tau", "Gem"):
    try:
        c = Constellation(getattr(Constellation.ConstellationName, cn))
        c.setLinesIntensity(0.8, Anim(1.5))
        c.setLabelIntensity(0.6, Anim(1.5))
        cons.append(c)
    except Exception:
        pass
print("   별자리 선 %d개 ON" % len(cons))
for mn in ("M42", "M31", "M45"):
    try:
        Messier(getattr(Messier.MessierName, mn)).setIntensity(1.0, Anim(1.0))
    except Exception:
        pass
# ❷ Insert2D.reserved 대입 줄 삭제 (속성 대입 금지 + 시스템 예약)

t3 = InsertText(InsertText.InsertTextName(3))
cam.addChild(t3.id, Camera.CameraPort.FixedForeground)
t3.setText("겨울 밤하늘 — 오리온 · 황소 · 쌍둥이")
t3.setPosition(Vec(0, 55, 0)); t3.setSize(0.035)
t3.setDistance(1.0, Anim(0.0))         # ★ 지상 = 기본 거리
t3.setColor(Vec(0.9, 0.9, 1.0)); t3.setIntensity(1.0, Anim(1.0))
print(">>> 별자리 감상 (8초)")
sleep(8.0)
t3.setIntensity(0.0, Anim(0.5))
for c in cons:
    c.setLinesIntensity(0.0, Anim(1.0))
    c.setLabelIntensity(0.0, Anim(1.0))

# ── 6) 은하수 여행 ──────────────────────────────────────────
print("은하수로...")
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(1.0, Anim(0.0))
mw = DATA.get("mw")
if mw is not None:
    print("🚀 은하수로 대비행! (GoTo — 지구 탈출부터 은하 밖까지)")
    mw.action(Action.Type.GoTo).trigger()
    wait_arrival(cam, timeout=60.0)
    try:                                # 도착 후 표류 비행 (연속 이동 — 은하가 서서히 멀어짐)
        gp = cam.positionLBR
        cam.setPositionR(gp.z * 1.5, Anim.cubic(10.0), -1)
        print("🚀 은하 표류 (10초)")
    except Exception as e:
        print("표류 실패:", repr(e)[:50])
else:
    print("★ 은하수 DB 못 찾음 — 이름 알려줘 (지상에서 은하수 감상으로 대체)")

t4 = InsertText(InsertText.InsertTextName(4))
cam.addChild(t4.id, Camera.CameraPort.FixedForeground)
t4.setText("우리 은하 Milky Way — 지름 약 10만 광년")
t4.setPosition(Vec(0, 55, 0))          # 은하 프레임(distance 20) = size 기본값 (t1 과 동일 규칙)
t4.setDistance(20.0, Anim(0.0))
t4.setColor(Vec(0.7, 0.8, 1.0)); t4.setIntensity(1.0, Anim(1.0))
print(">>> 은하수 감상 (8초)")
sleep(8.0)

# ── 7) 마무리 ───────────────────────────────────────────────
t4.setIntensity(0.0, Anim(1.0)); sleep(1.0)
uni.setGlobalIntensity(0.0, Anim(2.0)); sleep(2.0)
print("데모 완료!")

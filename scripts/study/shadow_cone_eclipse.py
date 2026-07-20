# -*- coding: utf-8 -*-
"""
shadow_cone_eclipse.py — 그림자 원뿔: 일식·월식의 기하학 (2026-07-14, 미연습 코드)
★ 전부 처음 쓰는 Planet/Satellite 그림자 원뿔 기능:
  setShadowConeIntensity(원뿔 표시) · setShadowConeRepresentationType(표현) ·
  setShadowConeAreaIntensity/Color(본影 umbra / 반影 penumbra / antumbra 별) ·
  setShadowConeSectionIntensity/Distance(단면).
★ 지구가 만드는 그림자 원뿔(태양 반대쪽)에 달이 들어가면 = 월식. 달 그림자가 지구에 닿으면 = 일식.
  enum(ShadowConeArea/ShadowConeRepresentation/ShadowConeLineDrawingMode)은 dir() 로 프로브해 학습.
방어적: 모든 그림자 호출에 feat() 성공/실패 로그. 접근/스케일은 로그 보고 조정.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
PN = Planet.PlanetName
earth = Planet(PN.Earth)
moon = Satellite(Satellite.SatelliteName.Moon)


def probe_enum(name, cls):
    try:
        print("[enum] %s: %s" % (name, ", ".join([m for m in dir(cls) if not m.startswith("_") and not m.islower()])))
    except Exception as e:
        print("[enum] %s 실패: %s" % (name, e))


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g" % (tag, p.x, p.y, p.z))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args)
        print("   ✓ %s.%s%s %s" % (type(obj).__name__, fn, tuple(str(a)[:24] for a in args), label))
        return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e))
        return False


def wait_arrival(maxs=50, docked_R=200.0):
    prev = None; r = 0.0
    for k in range(maxs):
        sleep(1.0)
        try:
            r = cam.positionLBR.z
        except Exception:
            continue
        if k % 3 == 0:
            print("   ...비행중 R=%.4g" % r)
        if 0 < r < docked_R and prev is not None and 0 < prev < docked_R:
            if abs(r - prev) / prev < 0.01:
                print("   도킹 R=%.4f" % r); return r
        prev = r
    print("   타임아웃 R=%.4g" % r); return r


# ── enum 프로브 ─────────────────────────────────────────────
for nm, attr in (("ShadowConeArea", "ShadowConeArea"),
                 ("ShadowConeRepresentation", "ShadowConeRepresentation"),
                 ("ShadowConeLineDrawingMode", "ShadowConeLineDrawingMode")):
    try:
        probe_enum(nm, getattr(Planet, attr))
    except Exception as e:
        print("[enum] Planet.%s 없음: %s" % (attr, e))

# ── 무대(지상) & 인트로 ─────────────────────────────────────
print("무대: 지상")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
try:
    moon.setIntensity(1.0, Anim(0.0))
except Exception:
    pass
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 12, 0, 0, tz, Anim(0.5)); sleep(1.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setSize(0.035); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.8, 0.85, 1.0))
uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
t1.setText("그림자 원뿔 — 일식과 월식은 왜 생길까"); t1.setIntensity(1.0, Anim(1.5))
sleep(4.5); t1.setIntensity(0.0, Anim(1.0)); sleep(1.0)


def narr(text, dur=3.5):
    t1.setText(text); sleep(dur)


# ── ★★ 지구 접근 = FadeTo/take off 말고 '완전 수동' (docs/05_face_earth.md 확정 방법) ──
#   smoothReset(False) → cam.setPositionLBR(Vec(L, 90, R), Anim, earth 포트) 로 직접 배치.
#   ✅ R 단위 = 지구반지름, 작을수록 지구가 큼 (R=1.5≈돔 40%, R=3≈20%). FadeTo 바인딩 없음 → R 자유.
#   ✅ 포트 = Ecliptic(황도) → B=90 이 황도 북극 = 공전면에 수직(위에서 내려다봄).
#   ★ 구성: beat A) 지구를 '크게'(R≈2.2) 보여주고 그림자 → beat B) 풀백(R 2.2→170)해서
#      지구가 점이 되며 달 궤도가 드러남 = '달이 지구 60배 거리'라는 스케일이 눈으로 보임.
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
narr("지구를 우주에서 — 크게 마주본다", 1.0)
uni.setGlobalIntensity(0.0, Anim.cubic(1.2)); sleep(1.4)
try:
    smoothReset(False); sleep(1.5); print("   smoothReset(False)")
except Exception as e:
    print("   smoothReset 실패(%s) → SceneGraph reset" % e); SceneGraph().reset(1); sleep(1.5)
# 천체 재점등(reset 이 다 끔)
for i in range(8):
    try:
        Planet(PN(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.5, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.2, Anim(0.0))
try:
    moon.setIntensity(1.0, Anim(0.0))
except Exception:
    pass

# 황도 포트 확보(수직 축)
ECL = -1
for pn in ("Ecliptic", "EquatorialJ2000", "Equatorial"):
    try:
        ECL = earth.portId(getattr(Planet.PlanetPort, pn))
        print("   ★ 포트=%s" % pn); break
    except Exception as e:
        print("   %s 실패: %s" % (pn, e))

BIG_R = 2.2        # 지구반지름. 작을수록 큼 → 지구가 돔에 크게.
NEAR_R = 170.0     # 달 궤도(60)·그림자가 보이는 풀백 거리.

# ── beat A: 지구를 크게 (완전 수동 배치) ─────────────────────
try:
    cam.setPositionLBR(Vec(0.0, 90.0, BIG_R), Anim.cubic(3.0), ECL); sleep(3.3)
    rlog("지구 크게(수동 배치) 후")
except Exception as e:
    print("   수동 배치 실패: %s" % e)
cam.setTargetHeight(110.0, Anim.cubic(1.5)); sleep(1.6)         # 돔 중앙(수동 B90 정렬 ≈110, docs/05)
feat(earth, "setLabelIntensity", 1.0, Anim(1.5), label="(지구 라벨)")
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)
# ★ 큰 지구를 충분히 보여줌(사용자: '커진 게 맞는지 모르겠다' → 오래 홀드)
narr("이게 지구다 — 위에서 수직으로 본 모습 (공전면에 직각)", 4.5)
narr("이 크기를 기억해 두자 — 이제 뒤로 물러난다", 3.0)
# ⚠️ 그림자·달은 풀백 '후'에 켠다 = 거대한 원뿔이 전환 중에 줄며 지저분해지는 걸 방지.

# ── beat B: 풀백 → 지구가 점이 되고 달 궤도가 드러남(스케일 체감) ──
try:
    cam.setPositionLBR(Vec(0.0, 90.0, NEAR_R), Anim.cubic(13.0), ECL); sleep(13.3)
    rlog("풀백 후")
except Exception as e:
    print("   풀백 실패: %s" % e)
narr("지구가 점이 됐다 — 달은 지구보다 60배 멀리 있다", 2.5)
cam.setTargetHeight(90.0, Anim.cubic(1.2)); sleep(1.3)
# 달 궤도선 + 달/태양 라벨·확대
feat(moon, "setOrbitIntensity", 1.0, Anim(2.0), label="(달 궤도선 — 지구 도는 원)")
feat(moon, "setScale", 8.0, Anim(2.0), label="(달 ×8 = 궤도 위 점으로)")
feat(moon, "setLabelIntensity", 1.0, Anim(1.5), label="(달 라벨)")
feat(sun, "setScale", 14.0, Anim(2.0), label="(태양 ×14 = 가장자리 원반)")
feat(sun, "setLabelIntensity", 1.0, Anim(1.5), label="(태양 라벨)")
t2 = InsertText(InsertText.InsertTextName(2))
cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
t2.setPosition(Vec(0, 12, 0)); t2.setSize(0.03); t2.setDistance(1.0, Anim(0.0))
t2.setColor(Vec(1.0, 0.85, 0.4))
t2.setText("☀ 태양(가장자리) → 지구(가운데 점) → 달(노란 궤도). 그림자는 태양 반대쪽.")
t2.setIntensity(0.9, Anim(1.5)); sleep(1.0)


def area_color(name):
    """area 이름으로 표준 색 배정 — 설명 가능하게 명시적으로 칠함.
    본影(Umbra)=빨강 / 반影(Penumbra)=파랑 / Antumbra=초록."""
    n = name.lower()
    if "pen" in n:
        return Vec(0.3, 0.5, 1.0), "반影 Penumbra(파랑) — 태양 일부만 가림=부분식"
    if "ant" in n:
        return Vec(0.3, 1.0, 0.45), "Antumbra(초록) — 본影 꼭짓점 너머=금환식"
    if "umbra" in n:
        return Vec(1.0, 0.25, 0.25), "본影 Umbra(빨강) — 태양 완전히 가림=개기식"
    return Vec(1.0, 1.0, 1.0), "기타(흰색)"


# ── ★ 지구의 그림자 원뿔 — 깔끔하게 '본影(빨강)'만 주인공 ──────
#  ⚠️ 이전 클러터 원인 3가지 정리:
#   ① Antumbra(초록) = 본影 꼭짓점 '너머'라 무한대로 뻗음 → 화면 밖 먼 곳에 밝은 점처럼 보였음(달 아님!). 제거.
#   ② 달의 자체 그림자 원뿔 = 일식용(다른 얘기) → 월식 장면엔 안 씀. 제거.
#   ③ setShadowConeSection = 여분의 원 → 제거.
#  → 남기는 것: 지구 본影(UmbraAfter, 빨강) 뚜렷 + 반影(PenumbraAfter, 파랑) 옅게. 달이 이 빨강을 지나면 월식.
narr("위에서 내려다본 지구-달 계 — 노란 원이 달의 궤도", 3.0)
narr("지구는 태양 반대쪽으로 그림자(본影)를 드리운다", 1.0)
feat(earth, "setShadowConeIntensity", 1.0, Anim(3.0), label="(그림자 원뿔 ON)")
# COLOR_3D = 입체 원뿔
try:
    if hasattr(Planet.ShadowConeRepresentation, "COLOR_3D"):
        feat(earth, "setShadowConeRepresentationType", Planet.ShadowConeRepresentation.COLOR_3D, Anim(1.0), label="(rep=COLOR_3D)")
except Exception as e:
    print("   rep 실패: %s" % e)
sleep(2.0)

narr("빨간 쐐기 = 지구 본影(개기 월식이 일어나는 곳)", 1.0)
# ★ UmbraAfter(빨강) 만 강하게, PenumbraAfter(파랑) 옅게. Antumbra·Before 는 전부 끔.
allareas = []
try:
    allareas = [m for m in dir(Planet.ShadowConeArea) if not m.startswith("_") and not m.islower() and "Invalid" not in m]
    print("   ShadowConeArea 멤버(전체): %s" % allareas)
except Exception as e:
    print("   area 실패: %s" % e)
# 먼저 전부 끔(안티움브라 포함) → 원하는 것만 켬
for a in allareas:
    try:
        feat(earth, "setShadowConeAreaIntensity", getattr(Planet.ShadowConeArea, a), 0.0, Anim(0.5), label="(off %s)" % a)
    except Exception:
        pass
# ★ UmbraAfter(빨강)만 주인공. PenumbraAfter(파랑 발산 빔)는 화면을 덮는 '아사리'의 주범(사용자 지적) → 완전 OFF.
plan = [("UmbraAfter", 1.0, Vec(1.0, 0.2, 0.2), "본影(빨강) — 태양 완전히 가림=개기 월식")]
for nm, inten, col, desc in plan:
    if nm in allareas:
        av = getattr(Planet.ShadowConeArea, nm)
        feat(earth, "setShadowConeAreaIntensity", av, inten, Anim(1.5), label="(%s %.2f)" % (nm, inten))
        feat(earth, "setShadowConeAreaColor", av, col, Anim(1.5), label="")
        print("   ★ %s → %s" % (nm, desc))
sleep(3.0)

# 달을 보이게 확대(궤도 위 점) — 자체 그림자 원뿔은 안 켬(월식 장면 깔끔하게)
feat(moon, "setScale", 6.0, Anim(2.0), label="(달 ×6 = 궤도 위 점으로)"); sleep(2.0)
sleep(3.5)

# ── 시간가속 — 달이 궤도를 돌아 지구 그림자(쐐기)를 가로지름 = 월식 ──
#  ★ 위에서 보면(황도 북극) 달의 궤도 원이 그림자 쐐기(태양 반대)를 반드시 가로지른다 —
#     그 순간이 보름(태양-지구-달 일직선) = 월식. 한 달(달 궤도 1바퀴)에 한 번.
#  느리게(한 달을 55초에) = 달이 천천히 돌며 쐐기를 지나는 게 또렷이 보임.
narr("시간을 흘린다 — 달이 궤도를 한 바퀴 돈다", 3.0)
narr("달이 그림자 쐐기를 가로지르는 순간 = 월식", 2.0)
dm.stop(); sleep(0.3)
try:
    j0 = dm.julianDate
except Exception:
    j0 = 0.0
dm.setDateTime(2026, 8, 30, 12, 0, 0, tz, Anim(55.0)); sleep(56.0)   # +29일(달 궤도 한 바퀴) 천천히
try:
    print("   시간가속 JD Δ=%.4f일 (달 궤도 약 %.2f바퀴)" % (dm.julianDate - j0, (dm.julianDate - j0) / 27.32))
except Exception:
    pass
dm.stop()

# ── 정리 ────────────────────────────────────────────────────
narr("본影에 들어가면 개기, 반影이면 부분 — 그림자의 기하학", 3.5)
feat(earth, "setShadowConeIntensity", 0.0, Anim(2.0))
feat(moon, "setShadowConeIntensity", 0.0, Anim(2.0))
try:
    t2.setIntensity(0.0, Anim(1.0))
except Exception:
    pass
t1.setText("일식과 월식 — 빛과 그림자의 정렬"); t1.setIntensity(1.0, Anim(1.2))
sleep(4.5); t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①황도 북극(위에서) 관점 = 달 궤도가 정면 '원'으로 보이나 "
      "②달 궤도선/지구 라벨 보이나 ③그림자 쐐기(빨강 본影)가 궤도 평면에 누워 보이나 "
      "④POLE_R=160 프레이밍 적당한가(달 궤도 원이 화면에 잘 차나 — 더 넓게/좁게?) "
      "⑤시간가속(55초) 속도 적당한가 ⑥달이 궤도 돌며 그림자 쐐기를 '가로지르나'(핵심!)")

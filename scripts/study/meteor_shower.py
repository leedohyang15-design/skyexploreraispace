# -*- coding: utf-8 -*-
"""
meteor_shower.py — 페르세우스 유성우 (2026-07-16, 지상 밤하늘)
★ 8월 12~13일 절정: 스위프트-터틀 혜성이 남긴 부스러기에 지구가 돌진 → 페르세우스자리에서 방사하는 유성우.
★ 미사용 조합: ShootingStar '유성우(rain)' + `setReferential(RaDec)`(복사점을 진짜 별자리에 하늘 고정) + ZHR.
  ⚠️ ZHR 내부 저장 = ZHR/60 (분당개수) → 볼만한 쇼는 ZHR 800~1500 (실제 100은 돔에서 거의 안 보임 — CLAUDE.md).
  ⚠️ `setRainSeed(1)`=재생 / 0=정지.
★ 시각: 청주 8/13 새벽 2시(절정, 페르세우스 높이 뜸) = 17:00 UTC(8/12) (UTC=KST-9). 북동 하늘 조준.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
LON, LAT, ALT = 127.49, 36.64, 800.0
earth = Planet(Planet.PlanetName.Earth)

# 페르세우스 복사점(적경/적위, 도)
RADIANT_RA, RADIANT_DEC = 47.0, 58.0


def _find_enum(cls, *cands, **kw):
    for n in cands:
        if hasattr(cls, n):
            return getattr(cls, n)
    sub = (kw.get("contains") or "").lower()
    for n in [m for m in dir(cls) if not m.startswith("__")]:
        if sub and sub in n.lower():
            print("   [auto] %s <- '%s'" % (cls.__name__, n)); return getattr(cls, n)
    return None


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대(지상 여름 새벽, 북동) ─────────────────────────────
print("무대: 청주 8/13 새벽, 페르세우스 유성우")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 어두운 하늘)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(1.0, Anim(0.0))
feat(Galaxy(Galaxy.GalaxyName.MilkyWay), "setExposure", 1.6, Anim(0.0), label="(은하수)")

Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 12, 17, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 8/13 02:00 KST
cam.setOrientationH(135.0, Anim(0.0))     # 북동
cam.setTargetHeight(22.0, Anim(0.0))      # 하늘 높이 올려다봄

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("8월의 밤하늘 — 별똥별이 쏟아진다", 3.5)

# ── 페르세우스자리 (복사점) 표시 ──────────────────────────
if hasattr(Constellation.ConstellationName, "Per"):
    feat(Constellation(Constellation.ConstellationName.Per), "setLinesIntensity", 0.7, Anim(1.5), label="(페르세우스 선)")
narr("유성은 모두 페르세우스자리 한 점에서 뻗어 나온다 — '복사점'", 4.0)

# ── ★ 유성우(rain) 세팅 ───────────────────────────────────
ss = ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)
# 모델(그라디언트)
_mdl = _find_enum(ShootingStar.Model, "Gradient", contains="grad") if hasattr(ShootingStar, "Model") else None
if _mdl is not None:
    feat(ss, "setRepresentationType", _mdl, label="(그라디언트 모델)")
# 복사점을 하늘(적도좌표)에 고정 → 진짜 페르세우스에서 방사
_ref = _find_enum(ShootingStar.Referential, "RaDec", "Equatorial", contains="radec") if hasattr(ShootingStar, "Referential") else None
if _ref is not None:
    feat(ss, "setReferential", _ref, label="(복사점 하늘 고정 RaDec)")
feat(ss, "setRainGradientPoint", Vec2(RADIANT_RA, RADIANT_DEC), label="(복사점=페르세우스 RA47/Dec58)")
feat(ss, "setRainChaosGradientPoint", 12.0, label="(방사 산포 12°)")
feat(ss, "setRainSpeed", 1.0, label="(유성 속도)")
feat(ss, "setBrightness", 1.0, label="(밝기/굵기)")
feat(ss, "setTrailLength", 0.7, label="(꼬리 길이)")

# ── ★ 재생: ZHR 단계적으로 올려 '쏟아짐' ──────────────────
narr("교외의 어두운 하늘이라면, 시간당 백 개도 넘게", 3.0)
feat(ss, "setZenithalHourlyRate", 1200.0, label="(ZHR 1200 = 볼만한 쇼)")
feat(ss, "setRainSeed", 1, label="(★ 유성우 재생 시작)")
sleep(10.0)

narr("스위프트-터틀 혜성이 남긴 먼지가 대기와 부딪혀 타오른다", 4.5)
sleep(4.0)

# ── 폭풍 급으로 잠깐 올림 ──────────────────────────────────
narr("유성 폭풍 — 하늘이 불꽃으로 가득", 2.0)
feat(ss, "setZenithalHourlyRate", 3000.0, label="(ZHR 3000 = 폭풍)")
sleep(9.0)

# ── 정리 ────────────────────────────────────────────────────
narr("소원을 빌어도 좋다 — 페르세우스 유성우", 4.0)
feat(ss, "setZenithalHourlyRate", 1000.0, label="(진정)")
sleep(3.0)
t1.setText("페르세우스 유성우 — 매년 8월의 선물"); t1.setIntensity(1.0, Anim(1.2)); sleep(4.0)
feat(ss, "setRainSeed", 0, label="(유성우 정지)")
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①청주 북동 밤하늘에 유성이 '쏟아지나'(ZHR 1200→3000) — 안 보이면 ZHR 더/구도 조정 "
      "②유성이 '페르세우스 한 점(복사점)'에서 방사되나(setReferential RaDec 먹었나 — 로그 [auto] 확인) "
      "③페르세우스자리 선 뜨나 ④꼬리/밝기 OK ⑤구도(H135/TH22) 조정?")

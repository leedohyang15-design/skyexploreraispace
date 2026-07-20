# -*- coding: utf-8 -*-
"""
ephemeris_tonight.py — Ephemeris 클래스: 오늘 청주의 일출·일몰·남중 (2026-07-20, 완본 미개척)
★ Ephemeris = '데이터 클래스' (렌더 아님) — 천체의 rise/set/transit 율리우스일을 계산해 속성으로 반환.
  읽기 속성: riseDate / setDate / transitDate / date / isValid. → 값을 읽어 InsertText 로 시각 표출.
★ 세터: setTargetBody(int 천체id) · setEventType(EventType) · setOffset/setOffsetType · setStartDate(JD) ·
  setUseSimulationTime(bool) · setTimeOffset(day) · setDayLimit(int). 프리셋 슬롯: Ephemeris007_Tonight/009_Sunrise 등.
★ ⚠️ 완본상 EventType/OffsetType enum 이 'Invalid' 만 보임(잘렸을 수도) → 런타임 dir() 로 실제 멤버 확인 +
  프리셋도 시도 + rise/set/transit 3속성 다 읽어 isValid 인 것만 표시. targetBody = 태양 id 로 일출/일몰.
★ JD(UTC) → KST(+9h) 변환해서 표출. (일몰/일출 시각이 주제라 밤하늘 위 자막이면 충분.)
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


def jd_to_kst(jd):
    """율리우스일(UTC) → (Y,M,D,hh,mm) KST(+9h). 유효 안하면 None."""
    try:
        if jd is None or jd <= 0 or jd != jd:  # None/0/NaN
            return None
    except Exception:
        return None
    j = jd + 9.0 / 24.0 + 0.5           # +KST, +0.5 (JD→그레고리안 알고리즘)
    Z = int(j); F = j - Z
    if Z < 2299161: A = Z
    else:
        al = int((Z - 1867216.25) / 36524.25); A = Z + 1 + al - int(al / 4)
    B = A + 1524; C = int((B - 122.1) / 365.25); D = int(365.25 * C); E = int((B - D) / 30.6001)
    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    d = int(day); fr = day - d
    hh = int(fr * 24); mm = int((fr * 24 - hh) * 60)
    return (year, month, d, hh, mm)


def fmt(t):
    return "--:--" if t is None else "%02d:%02d" % (t[3], t[4])


# ── 무대: 청주 밤하늘 ───────────────────────────────────────
print("무대: Ephemeris — 오늘 청주 일출·일몰·남중")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
feat(earth, "setElevationScale", 0.0)
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))

Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 20, 13, 0, 0, tz, Anim(0.0)); sleep(0.5)   # 청주 밤 22시
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))
try: JD_NOW = dm.julianDate; print("   현재 JD=%.5f" % JD_NOW)
except Exception as e: JD_NOW = 0.0; print("   julianDate 실패: %s" % e)

# ── EventType / OffsetType 실제 멤버 덤프 ──────────────────
ev = [m for m in dir(Ephemeris.EventType) if not m.startswith("__") and m[0].isupper() and "Invalid" not in m]
of = [m for m in dir(Ephemeris.OffsetType) if not m.startswith("__") and m[0].isupper() and "Invalid" not in m]
print("   [EventType 멤버] %s" % (ev or "없음(Invalid만)"))
print("   [OffsetType 멤버] %s" % (of or "없음(Invalid만)"))

# 태양 id (targetBody)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)
sun_id = getattr(sun, "id", None)
print("   태양 id=%s" % sun_id)


def compute(slot_name, target_id, want_event=None):
    """Ephemeris 슬롯 하나로 rise/set/transit 계산해 읽기."""
    try:
        eph = Ephemeris(getattr(Ephemeris.EphemerisName, slot_name))
    except Exception as e:
        print("   [%s] 생성 실패: %s" % (slot_name, e)); return {}
    feat(eph, "setUseSimulationTime", True, label="(%s)" % slot_name)
    if JD_NOW > 0: feat(eph, "setStartDate", float(JD_NOW))
    if target_id is not None: feat(eph, "setTargetBody", int(target_id))
    if want_event and hasattr(Ephemeris.EventType, want_event):
        feat(eph, "setEventType", getattr(Ephemeris.EventType, want_event), label="(event=%s)" % want_event)
    feat(eph, "setDayLimit", 2)
    sleep(0.4)   # 계산 프레임 대기
    out = {}
    for prop in ("riseDate", "setDate", "transitDate", "date"):
        try: out[prop] = getattr(eph, prop)
        except Exception: out[prop] = None
    try: out["isValid"] = eph.isValid
    except Exception: out["isValid"] = "?"
    print("   [%s] isValid=%s rise=%s set=%s transit=%s"
          % (slot_name, out.get("isValid"), out.get("riseDate"), out.get("setDate"), out.get("transitDate")))
    return out


# 태양 출몰 계산 (일반 슬롯 + 프리셋)
res = compute("Ephemeris001", sun_id, want_event=(ev[0] if ev else None))
if not (res.get("riseDate") or res.get("setDate")):
    for preset in ("Ephemeris007_Tonight", "Ephemeris009_Sunrise"):
        if hasattr(Ephemeris.EphemerisName, preset):
            r2 = compute(preset, sun_id)
            if r2.get("riseDate") or r2.get("setDate"): res = r2; break

rise = jd_to_kst(res.get("riseDate"))
sett = jd_to_kst(res.get("setDate"))
trans = jd_to_kst(res.get("transitDate"))

# ── 자막 표출 ───────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 40, 0)); t1.setSize(0.05); t1.setColor(Vec(1.0, 1.0, 0.6)); t1.setDistance(1.0, Anim(0.0))
t2 = InsertText(InsertText.InsertTextName(2))
cam.addChild(t2.id, Camera.CameraPort.FixedForeground)
t2.setPosition(Vec(0, 22, 0)); t2.setSize(0.06); t2.setColor(Vec(1.0, 0.85, 0.4)); t2.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def show(a, b, dur=4.5):
    t1.setText(a); t1.setIntensity(1.0, Anim(1.0))
    t2.setText(b); t2.setIntensity(1.0, Anim(1.0)); sleep(dur)


show("오늘 청주의 태양", "일출  %s      일몰  %s" % (fmt(rise), fmt(sett)), 5.0)
show("태양이 가장 높이 뜨는 시각 (남중)", "남중  %s" % fmt(trans), 5.0)
if rise is None and sett is None and trans is None:
    show("Ephemeris 계산값이 비어있음", "로그의 EventType/isValid/rise/set 확인 필요", 5.0)

# ── 정리 ────────────────────────────────────────────────────
show("Ephemeris — 천체의 출몰을 계산한다", " ", 4.0)
t1.setIntensity(0.0, Anim(1.5)); t2.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.5)); sleep(4.0)
print("종료. ★리포트: ①★자막에 일출/일몰/남중 시각(HH:MM)이 실제로 떴나(--:-- 면 계산 실패) "
      "②로그 '[EventType 멤버]'/'[OffsetType 멤버]' 가 뭐가 있나(Rise/Set/Transit 등) "
      "③로그 '[슬롯] isValid=.. rise=.. set=..' 값 붙여줘 — 어느 슬롯/방법이 값을 냈는지 "
      "④전부 비면 = Ephemeris 는 스크립트 계산 미지원(프리셋 UI 전용)으로 판정하고 마무리")

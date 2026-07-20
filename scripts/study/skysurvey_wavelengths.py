# -*- coding: utf-8 -*-
"""
skysurvey_wavelengths.py — SkySurvey HTTP(평문) 재시도 (v7, 2026-07-20)
★ v6 판정 = 검은 화면(서베이 렌더 X). 그런데 브라우저 테스트로 확인:
  · https://alasky.u-strasbg.fr/MellingerRGB/properties → ✅ 정상 로드 (인터넷 O, 서버 O, URL O)
  · properties 파일이 광고하는 서비스 주소 = 전부 'http://'(평문): hips_service_url/moc_access_url.
  → 강한 의심: '오래된 엔진의 타일 로더가 TLS(https)를 못 함' → 브라우저는 https OK, 엔진은 못 받음.
★ v7 유일한 변경 = URL 을 'http://'(평문)로. 그 외 구조는 v6 판정본 그대로(엔진 은하수 기준 → 서베이 겹침 → 엔진 OFF).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam    = Camera(Camera.CameraName.MainCamera)
uni    = Universe(Universe.UniverseName.MainUniverse)
dm     = DateManager()
tz     = DateManager.TimeZone.DefaultTimeZone
earth  = Planet(Planet.PlanetName.Earth)
stars  = Stars(Stars.StarsName.StarrySky)
galaxy = Galaxy(Galaxy.GalaxyName.MilkyWay)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:48] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def make_survey():
    SN = SkySurvey.SkySurveyName
    for nm in ("SkySurvey001", "SkySurvey01", "SkySurvey1"):
        if hasattr(SN, nm):
            try: return SkySurvey(getattr(SN, nm))
            except Exception as e: print("   %s 생성 실패: %s" % (nm, e))
    try: return SkySurvey(SkySurvey.SkySurveyName(0))
    except Exception as e:
        print("   SkySurvey 생성 실패: %s" % e); return None


# ★ 핵심 변경: 평문 http:// (properties 가 광고하는 그 서비스 주소 형식)
URL = "http://alasky.u-strasbg.fr/MellingerRGB"

# ── 무대: 지상 밤 + 엔진 은하수 ON(기준 화면) ──────────────
print("무대: SkySurvey HTTP 재시도 (v7) — URL=%s" % URL)
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF)")
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(지면 OFF)")
feat(earth, "setElevationScale", 0.0)
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(0.0, Anim(0.0))
stars.setIntensity(0.6, Anim(0.0))
galaxy.setIntensity(1.0, Anim(0.0))
feat(galaxy, "setExposure", 1.6, Anim(0.0), label="(은하수 밝게)")

Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 8, 1, 15, 0, 0, tz, Anim(0.0)); sleep(0.5)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(50.0, Anim(0.0))

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("STEP1) 엔진 은하수 — 기준 화면", 4.0)

ss = make_survey()
if ss is None:
    narr("SkySurvey 생성 실패 — 로그 확인", 4.0)
else:
    print("   SkySurvey id=%s" % getattr(ss, "id", "?"))
    ss.setIntensity(0.0, Anim(0.0))
    feat(ss, "setUrl", URL, label="(★ 평문 http)")
    print("   setUrl 직후 readback url=%s" % getattr(ss, "url", "?"))
    sleep(5.0)                                           # 평문 http 타일 로드 대기(넉넉히)
    narr("STEP2) http:// 서베이를 그 위에 겹친다", 3.0)
    ss.setIntensity(1.0, Anim(3.0)); sleep(4.0)
    print("   [겹친 뒤] survey intensity=%s url=%s" % (ss.intensity, getattr(ss, "url", "?")))
    narr("서베이 intensity=1 — 화면 질감이 바뀌었나?", 5.0)

    narr("STEP3) ★ 엔진 은하수를 끈다 — http 서베이가 로드됐다면 은하수가 '남는다'", 4.0)
    galaxy.setIntensity(0.0, Anim(3.0))
    stars.setIntensity(0.0, Anim(3.0)); sleep(4.0)
    ss.setIntensity(1.0, Anim(0.6))
    narr("★★ 지금 화면: 은하수가 남았나(http 성공!) / 검은 화면인가(엔진 HiPS 미지원 확정)?", 8.0)
    print("   [엔진 OFF 후] survey intensity=%s url=%s" % (ss.intensity, getattr(ss, "url", "?")))

# ── 정리 ────────────────────────────────────────────────────
narr("판정 끝", 2.5)
stars.setIntensity(1.0, Anim(1.5))
galaxy.setIntensity(1.0, Anim(1.5))
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. ★핵심(딱 하나): STEP3에서 엔진 은하수 끈 뒤 → "
      "(A)은하수/성운이 '남음' = 평문 http 로 서베이 렌더 성공! → 이제 진짜 파장쇼 만든다 "
      "(B)여전히 '검은 화면' = 이 엔진은 온라인 HiPS 자체를 안 그림(https/http 무관) → SkySurvey 접고 새 천체로. "
      "브라우저에선 properties 가 떴으니(인터넷 O) 이 결과가 최종 판정.")

# -*- coding: utf-8 -*-
"""
aurora.py — 오로라(북극광): 태양풍이 그리는 하늘의 커튼 (2026-07-16, 안 쓴 API=setAuroraIntensity)
★ 안 쓴 코드: `Planet(Earth).setAuroraIntensity` — 지구 프로브(constellation_boundaries v3 덤프)에서 발굴한 미사용 렌더러블.
  태양풍의 하전입자가 지구 자기장을 따라 극지방 상공으로 쏟아져 대기 원자(산소=초록/빨강, 질소=보라)를 들뜨게 해
  빛나는 커튼 = 오로라. 이 빌드에 렌더가 내장돼 있으니 켜서 확인 + 세기를 출렁여 '춤추게'.
★ 관측지: 노르웨이 트롬쇠(위도 69.6°N, 오로라 벨트 아래). 1월 = 극야(종일 어둠)라 언제든 밤하늘.
  ⚠️ 청주(위도 36)는 오로라 벨트 밖 → 이 쇼만은 관측지를 고위도로 옮김(setPosition 으로 위도 69).
★ 안 쓴 보조 렌더도 곁들임(확인용): setMagnetosphereIntensity(자기권) — '왜 극지방에 뜨나' 설명용(효과는 로그로 판단).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)
stars = Stars(Stars.StarsName.StarrySky)

# 트롬쇠(노르웨이) — 오로라 명소
LAT, LON, ALT = 69.65, 18.96, 100.0


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 오로라 관련 메서드 프로브 (색/고도/속도 세터 있나) ──────
aur = [m for m in dir(earth) if "auror" in m.lower()]
mag = [m for m in dir(earth) if "magneto" in m.lower()]
print("   [오로라 메서드] %s" % aur)
print("   [자기권 메서드] %s" % mag)

# ── 무대: 트롬쇠 극야 밤, 북쪽 하늘 (대기 OFF = 검은 하늘) ───
print("무대: 노르웨이 트롬쇠, 극야의 밤 — 오로라")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0), label="(대기 OFF = 어두운 하늘)")
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0), label="(지면 OFF)")
feat(earth, "setElevationScale", 0.0, label="(평탄)")
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
stars.setIntensity(1.0, Anim(0.0))
feat(stars, "setPointSaturation", 2.0, Anim(0.0), label="(별 색)")

Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))   # ★ 고위도로 이동
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 1, 15, 22, 0, 0, tz, Anim(0.0)); sleep(0.6)  # 극야 = 종일 어둠
cam.setOrientationH(180.0, Anim(0.0))     # 북쪽(오로라 벨트 방향)
cam.setTargetHeight(40.0, Anim(0.0))      # 하늘 높이 올려다봄(오로라 커튼이 머리 위까지)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052); t1.setColor(Vec(0.7, 1.0, 0.7)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("노르웨이, 북위 69도 — 극야의 어두운 밤", 4.0)
narr("태양에서 날아온 입자들이 지구 자기장에 이끌려 극지방으로", 4.5)

# ── ★ 오로라 켜기 ───────────────────────────────────────────
narr("그리고 하늘에 커튼이 드리운다 — 오로라", 3.0)
feat(earth, "setAuroraIntensity", 1.0, Anim(3.0), label="(★★ 오로라 ON)")
sleep(3.5)
narr("산소는 초록으로, 높은 곳에선 붉게 — 질소는 보랏빛으로", 4.5)

# ── ★ 춤추게: 세기를 출렁 (커튼이 밝아졌다 옅어졌다) ────────
narr("오로라는 살아 움직인다 — 밝아졌다, 옅어졌다", 3.0)
for lv, du in [(0.4, 2.5), (1.0, 2.0), (0.6, 2.2), (1.0, 1.8), (0.5, 2.4), (1.0, 2.0)]:
    feat(earth, "setAuroraIntensity", lv, Anim(du))
    sleep(du + 0.2)

# ── 시간가속: 하늘(별)이 천천히 돌며 오로라가 흐른다 ────────
narr("밤이 흐르는 동안, 별과 함께 오로라도 춤춘다", 3.0)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 16, 1, 0, 0, tz, Anim(20.0)); sleep(21.0)   # +3h 극야 밤
dm.stop()

# ── 자기권 곁들임 (왜 극지방인가) — 효과는 로그/화면으로 판단 ─
narr("이 빛은 지구 자기장이 우주 방사선으로부터 우릴 지키는 흔적", 4.5)
feat(earth, "setMagnetosphereIntensity", 0.6, Anim(2.0), label="(자기권 — 보조)")
sleep(2.5)
feat(earth, "setMagnetosphereIntensity", 0.0, Anim(1.5))

narr("오로라 — 태양과 지구가 함께 그리는 빛의 춤", 4.5)

# ── 정리 ────────────────────────────────────────────────────
narr("북극광, 아우로라 — 하늘 끝의 커튼", 4.0)
feat(earth, "setAuroraIntensity", 0.0, Anim(3.0), label="(오로라 OFF)")
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트: ①★★북쪽 하늘에 '오로라(초록 커튼)'가 뜨나(setAuroraIntensity) — 핵심, 로그 [오로라 메서드] 확인 "
      "②세기 출렁일 때 커튼이 밝아졌다 옅어졌다 '춤추나' ③시간가속 때 별과 함께 흐르나 "
      "④색(초록/빨강/보라) 나오나 ⑤자기권(setMagnetosphereIntensity) 뭔가 보이나(보조) ⑥구도(북쪽 H180/TH40)·밝기 조정?")

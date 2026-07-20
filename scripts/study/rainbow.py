# -*- coding: utf-8 -*-
"""
rainbow.py — 무지개: 비 온 뒤 태양 반대편에 뜨는 빛의 아치 (2026-07-16, 안 쓴 API=setRainbowIntensity)
★ 안 쓴 코드: `Planet(Earth).setRainbowIntensity` (지구 프로브에서 발굴). 대낮 대기광학 현상 —
  햇빛이 공중의 빗방울 안에서 굴절·반사돼 색이 갈라짐(빨강 42°/보라 40°). 항상 '태양의 정반대쪽(대일점)'에 아치.
★ 지금까지와 다른 세팅 = '대낮': 대기 ON(밝은 파란 하늘) + 지면 ON(풍경). 태양을 낮게(저녁) 두고 반대편(동쪽)을 본다.
  ⚠️ 무지개는 태양 반대편에만 뜸 → 카메라를 '태양 반대 방위'로 조준해야 아치가 화면에 들어옴.
★ 관측지 청주, 여름 저녁(태양 낮게 서쪽) 18:30 KST = 09:30 UTC. 태양 서쪽 → 무지개 동쪽, 동쪽 조준.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
LON, LAT, ALT = 127.49, 36.64, 300.0
earth = Planet(Planet.PlanetName.Earth)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:14] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 대기광학 관련 메서드 프로브 ─────────────────────────────
opt = [m for m in dir(earth) if any(k in m.lower() for k in ("rainbow", "halo", "rain", "cloud"))]
print("   [대기광학/구름 메서드] %s" % opt)

# ── 무대: 청주 여름 저녁, 대낮(대기 ON) ─────────────────────
print("무대: 청주 여름 저녁 — 비 갠 하늘의 무지개")
smoothReset(False)
uni.setGlobalIntensity(0.0, Anim(0.0))
earth.setIntensity(1.0, Anim(0.0))                                 # 지상 낮 하늘 마스터
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0), label="(★ 대기 ON = 밝은 파란 하늘)")
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0), label="(지면 ON = 풍경)")
sun.setIntensity(1.0, Anim(0.0))

Place2D(Place2D.Place2DName(0)).setPosition(Vec(LAT, LON, ALT))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 6, 15, 10, 0, 0, tz, Anim(0.0)); sleep(0.6)   # 19:00 KST, 태양 더 낮게(일몰 47분 전) = 아치 높게
cam.setOrientationH(65.0, Anim(0.0))      # 동남동(태양 반대=대일점) 조준
cam.setTargetHeight(33.0, Anim(0.0))      # 높아진 아치 담기게

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 22, 0)); t1.setSize(0.05); t1.setColor(Vec(1.0, 1.0, 1.0)); t1.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(2.6)


def narr(text, dur=3.5):
    t1.setText(text); t1.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("비가 그친 여름 저녁, 해는 서쪽으로 낮게 기울고", 4.0)
narr("동쪽 하늘을 보면 — 공기 중엔 아직 빗방울이 남아 있다", 4.0)

# ── ★ 무지개 켜기 (태양 반대편 아치) ───────────────────────
narr("그리고 빛의 아치가 걸린다 — 무지개", 3.0)
feat(earth, "setRainbowIntensity", 1.0, Anim(3.0), label="(★★ 무지개 ON)")
sleep(3.5)
narr("햇빛이 빗방울 안에서 굴절·반사되며 일곱 빛깔로 갈라진다", 4.5)
narr("바깥은 빨강, 안쪽은 보라 — 언제나 태양의 정반대편에", 4.5)

# ── 진하게↔옅게 (구름/비 지나가듯) ─────────────────────────
narr("빗방울이 많을수록 진하게, 마르면 옅게", 3.0)
for lv, du in [(0.5, 2.2), (1.0, 2.0), (0.7, 2.2), (1.0, 2.0)]:
    feat(earth, "setRainbowIntensity", lv, Anim(du)); sleep(du + 0.2)

# ── 시간가속: 해가 더 기울며 무지개가 높이 올라간다 ─────────
narr("해가 낮아질수록 무지개는 더 높이 솟는다", 3.5)
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 6, 15, 10, 40, 0, tz, Anim(22.0)); sleep(23.0)   # 일몰 직전 → 아치 최대(반원 근접)
dm.stop()

narr("해가 지평선에 닿으면, 무지개는 반원(半圓)이 된다", 5.0)   # 최대 아치에서 홀드

# ── 정리 ────────────────────────────────────────────────────
narr("무지개 — 비와 햇빛이 함께 있을 때만 나타나는 약속", 4.5)
narr("태양을 등지고 서야만 볼 수 있는, 하늘의 아치", 4.0)
feat(earth, "setRainbowIntensity", 0.0, Anim(3.0), label="(무지개 OFF)")
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0)); sleep(4.5)
print("종료. 리포트(v2 해 더 낮게=아치 크게): ①무지개 아치가 v1 보다 '높고 크게' 뜨나(해 낮춤: 10:00→10:40 UTC) "
      "②색(빨강~보라)이 파란 하늘 배경에 더 선명해졌나(지평선 노을에 안 묻히고) "
      "③시간가속 끝(일몰 직전)에 반원에 가깝게 솟나 ④세기 출렁 OK ⑤그래도 옅으면: 무지개 색은 SDK 렌더 한계일 수 있음(intensity 이미 최대)")

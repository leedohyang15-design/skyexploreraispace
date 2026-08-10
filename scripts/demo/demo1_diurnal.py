# -*- coding: utf-8 -*-
# ═══ [시연 폴백 1] 지구 자전 — 별의 일주운동 (약 45초) ═══
#
# ⚠️ 이 파일은 '사람이 쓴 예제'가 아니라 **Sky Explorer AI 가 생성한 결과물 그대로**다.
#    프롬프트: "청주에서 지구 자전으로 별이 도는 걸 보여줘"
#    2026-08-10 규칙 검사 무위반 통과 + 일주운동 레시피 전 항목 반영 확인.
#
# 시연에서의 쓰임: 라이브 생성이 실패하거나 API 하루 한도에 걸렸을 때
#   "미리 만들어 둔 것이 이겁니다" 하고 바로 재생 → 시연이 죽지 않는다.
#   (관객에게 숨길 것 없음 — '만들어 두면 관에 쌓인다'가 오히려 세일즈 포인트다.)
from skyExplorer import *
from studio import *
from Initialization import *

try:
    SceneGraph().reset(1)
except Exception:
    pass
sleep(1.5)

uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))          # 세팅 중 암전

cam = Camera(Camera.CameraName.MainCamera)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone

# 관측지 = 청주
place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.49, 100.0))

# 지상 하늘 쇼 체크리스트: 대기 OFF + 지면 OFF
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))

Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))

# 청주 밤 22:00 KST = 13:00 UTC
dm.stop()
sleep(0.2)
dm.setDateTime(2026, 7, 22, 13, 0, 0, tz, Anim(0.0))
sleep(0.4)

# 북쪽 조준(H=180) + 전천 격자 구도(Target 0)
cam.setOrientationH(180.0, Anim(0.0))
cam.setTargetHeight(0.0, Anim(0.0))

# ★ 이 쇼의 핵심 — '고정된 땅의 격자' 와 '도는 하늘의 격자' 를 같이 켠다
place.setAzimuthGridIntensity(0.45, Anim(1.5))      # 방위·고도 (지평 프레임 = 고정)
place.setMeridianIntensity(0.4, Anim(1.5))          # 자오선
place.setCardinalPointsIntensity(0.9, Anim(1.5))    # 동서남북
earth.setEquatorialGridIntensity(0.6, Anim(1.5))    # 천구 적도 (별과 함께 회전)

# 회전의 중심을 눈에 보이게
polaris = IndividualStar(IndividualStar.IndividualStarName.Polaris)
polaris.setPointerIntensity(1.0, Anim(1.5))

uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.5)

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0))
txt.setSize(0.052)
txt.setColor(Vec(1.0, 1.0, 0.55))
txt.setDistance(1.0, Anim(0.0))
txt.setText("지구 자전에 의한 별의 일주운동\n(중심: 북극성)")
txt.setIntensity(1.0, Anim(1.0))
sleep(2.0)

# 6시간을 30초에 = 0.2h/초 (이보다 빠르면 어지럽다)
dm.setDateTime(2026, 7, 22, 19, 0, 0, tz, Anim(30.0))
sleep(30.5)

txt.setText("지구가 자전함에 따라 천구가 북극성을 중심으로 회전합니다")
sleep(3.0)

cam.setTargetHeight(30.0, Anim(3.0))                # 관람 표준으로 복귀
sleep(3.2)

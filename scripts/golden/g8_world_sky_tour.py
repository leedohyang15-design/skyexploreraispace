# -*- coding: utf-8 -*-
# ═══ [정답 예제 8] 세계 도시 밤하늘 투어 (관측지 이름으로 이동) ═══
# 대응 프롬프트: "서울, 파리, 시드니에서 본 같은 시각의 밤하늘을 비교해줘"
#
# ★ 2026-07-30 새로 확인: **관측지를 '이름'으로 옮길 수 있다** (좌표 하드코딩 불필요)
#     DataManager.database().data(Data.Type.CityType, "Paris").action(Action.Type.GoTo).trigger()
#   · 실측: 청주(36.64,127.49,200m) → 서울(37.599,126.978,100m) 정확히 이동, 1~2초
#   · 지상 시점 유지(camR=0), 고도까지 자동
#   · 살아있는 타입: CityType(도시) / MountainType(산) / VolcanoType(화산) — 각각 GoTo·FadeTo
#   🛑 GoToPlace·FadeToPlace 는 死 → 그냥 GoTo 를 쓴다
#
# 연출 포인트: 관측지가 바뀌면 **같은 시각인데 하늘이 달라진다**(위도에 따라 별자리 높이·
#   보이는 별자리가 바뀜). 남반구(시드니)로 가면 오리온이 뒤집혀 보이는 게 하이라이트.
from skyExplorer import *
from studio import *
from Initialization import *

# (도시이름, 자막) — 이름은 DB 표기 그대로. 실측 확인: Seoul/Paris/New York/London/Tokyo
CITIES = [
    ("Seoul",    "서울 — 북위 37도"),
    ("Paris",    "파리 — 북위 49도, 별이 더 낮게 뜬다"),
    ("New York", "뉴욕 — 같은 시각, 다른 하늘"),
]

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()

# ── 지상 밤하늘 기본 세팅 ────────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
uni.setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))     # 대기 OFF
earth.setTerrainIntensity(0.0, Anim(0.0))        # 지면 OFF
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0))   # 같은 시각 고정(UTC)
sleep(0.5)
cam.setOrientationH(0.0, Anim(0.0))
cam.setTargetHeight(30.0, Anim(0.0))

# 오리온을 기준점으로 (도시마다 높이·기울기가 달라지는 게 보임)
ori = Constellation(Constellation.ConstellationName.Ori)
ori.setLinesIntensity(0.8, Anim(1.0))
ori.setLabelIntensity(0.7, Anim(1.0))
sleep(2.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("같은 시각, 지구 어디에서 보느냐에 따라"); t1.setIntensity(1.0, Anim(1.0))
sleep(3.5)


def goto_city(name, caption):
    """도시 이름으로 관측지 이동 (좌표 하드코딩 불필요)"""
    h = db.data(Data.Type.CityType, name)
    if h is None:
        print("⚠️ 도시 '%s' 조회 실패 — 이름 표기 확인 필요" % name)
        return
    # 전환을 부드럽게: 살짝 암전 → 이동 → 페이드인
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(1.2)
    h.action(Action.Type.GoTo).trigger()
    sleep(3.0)                                    # 관측지 전환은 1~2초면 끝남
    cam.setTargetHeight(30.0, Anim(0.0))          # 관람 정위치 재확인
    t1.setText(caption)
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(2.0)
    try:
        p = Place2D(Place2D.Place2DName(0)).position
        print("이동 완료: %s → 위도 %.3f / 경도 %.3f / 고도 %.0fm" % (name, p.x, p.y, p.z))
    except Exception:
        pass
    sleep(6.0)                                    # 하늘 감상


for city, cap in CITIES:
    goto_city(city, cap)

# ── 마무리: 산 위에서 보는 하늘 (MountainType 도 같은 방식) ──
h = db.data(Data.Type.MountainType, "Mont blanc")
if h is not None:
    uni.setGlobalIntensity(0.0, Anim(1.0)); sleep(1.2)
    h.action(Action.Type.GoTo).trigger()
    sleep(3.0)
    cam.setTargetHeight(30.0, Anim(0.0))
    t1.setText("몽블랑 정상 — 4,800m 위의 하늘")
    uni.setGlobalIntensity(1.0, Anim.cubic(1.5)); sleep(2.0)
    try:                                        # (v2) 산 구간도 좌표 로그 남기기
        q = Place2D(Place2D.Place2DName(0)).position
        print("이동 완료: Mont blanc → 위도 %.3f / 경도 %.3f / 고도 %.0fm" % (q.x, q.y, q.z))
    except Exception:
        pass
    sleep(6.0)

t1.setText("같은 별, 다른 자리"); sleep(4.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

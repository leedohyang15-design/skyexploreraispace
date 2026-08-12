# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 규칙 검사는 통과했으나 돔에서 본 기록이 없다. 기하(프레임·L/B·R 단위)는 정적 검사로 안 잡히니 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ═══ [정답 예제 4] 전 별자리 선/그림/라벨 슬라이더 페이드 ═══
# 대응 프롬프트: "밤하늘의 모든 별자리 선을 부드럽게 켜줘"
#
# 오늘 부활시킨 ParameterizationLut '프리셋 슬롯' 활용:
#   ⚠️ 수동 타겟(addTargetAttribute)은 여전히 死. **미리 배선된 프리셋 슬롯만 동작**.
#   · 051_AllConstellationLines / 052_Pictures / 053_Labels / 054_Boundaries
#   · 055~058_Slider* / 059_AutoExposure / 060_AutoContrast
#   🛑 061_WeatherEffectRain / 062_Snow = 별도 날씨 렌더러 소관이라 死(쓰지 말 것)
#   ★ 핵심: setEnabled(True) 후 **sleep(1.5) 프레임 대기** 없으면 enabled 가 False 로 남음
#   → 88개 별자리를 개별 호출할 필요 없이 한 번에 부드럽게 페이드
from skyExplorer import *
from studio import *
from Initialization import *
def _dark(sec=0.0):
    """암전 '유지' — reset/FadeTo/무거운 세팅은 밝기를 1.0 으로 되돌린다.
       ⚠️ setGlobalIntensity(0) 을 **한 번만** 걸면 소용없다(2026-08-12 실측: 그래서
          세팅 구간이 그대로 보였다). 이 함수를 세팅 단계마다 끼워 넣어 계속 눌러준다."""
    u = Universe(Universe.UniverseName.MainUniverse)
    for _ in range(max(int(sec / 0.2), 1)):
        u.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 지상 밤하늘 ──────────────────────────────────────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
SceneGraph().reset(1); _dark(1.5)
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
_dark()
cam.setOrientationH(0.0, Anim(0.0))
_dark()
cam.setTargetHeight(30.0, Anim(0.0))
_dark()
sleep(2.0)

# ★ 세팅이 전부 끝난 뒤에야 페이드인 — 관측지·시각·조준을 불 켠 채로 하면
#   그 조정 과정이 관객에게 그대로 보인다(돔 실측: "쇼마다 카메라를 자꾸 조정하는 게 보인다").
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.2)
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 25, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("별들을 이어 보면"); t1.setIntensity(1.0, Anim(1.0))
sleep(3.0)

# ── ① 별자리 '선' 전체를 슬라이더로 페이드인 ─────────────────
lines = ParameterizationLut(
    ParameterizationLut.ParameterizationLutName.ParameterizationLut051_AllConstellationLines)
lines.setEnabled(True)
sleep(1.5)                                   # ★ 프레임 대기 필수
lines.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
lines.setInternalValue(1.0, Anim(4.0))       # 0→1 = 부드럽게 전부 켜짐
sleep(5.0)

t1.setText("88개 별자리, 하나의 슬라이더로"); sleep(3.0)

# ── ② 별자리 '이름표'도 페이드인 ─────────────────────────────
labels = ParameterizationLut(
    ParameterizationLut.ParameterizationLutName.ParameterizationLut053_AllConstellationLabels)
labels.setEnabled(True)
sleep(1.5)
labels.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
labels.setInternalValue(1.0, Anim(3.0))
sleep(4.0)

t1.setText("신화의 그림까지"); sleep(2.0)

# ── ③ 신화 그림(art) 페이드인 ────────────────────────────────
art = ParameterizationLut(
    ParameterizationLut.ParameterizationLutName.ParameterizationLut052_AllConstellationPictures)
art.setEnabled(True)
sleep(1.5)
art.setInternalValue(0.0, Anim(0.0)); sleep(0.5)
art.setInternalValue(1.0, Anim(5.0))
sleep(6.0)

t1.setText("하늘 가득한 이야기"); sleep(4.0)

# ── ④ 정리: 그림만 끄고 선은 남기기 ──────────────────────────
art.setInternalValue(0.0, Anim(3.0)); sleep(3.5)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)
lines.restore(); labels.restore(); art.restore()

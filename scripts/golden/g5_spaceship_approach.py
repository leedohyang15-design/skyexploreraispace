# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 규칙 검사는 통과했으나 돔에서 본 기록이 없다. 기하(프레임·L/B·R 단위)는 정적 검사로 안 잡히니 재생 전 신뢰하지 말 것
#  ⚠️ 이 줄은 '돔에서 실제로 봤는가'만 적는다. 코드가 규칙을 지켰는지와는 별개다.
#     확인했으면 날짜와 확인 범위를 남길 것 — 안 남기면 다음에 처음부터 다시 의심해야 한다.
# ─────────────────────────────────────────────────────────────

# ═══ [정답 예제 5] 우주선이 다가온다 (Insert2D 애니메이션 = 영상 대체) ═══
# 대응 프롬프트: "우주선이 다가오는 장면을 만들어줘"
#
# 오늘 확보한 '영상의 유일한 대체 수단':
#   🛑 VideoPlayer/Audio = 별도 호스트 소관이라 스크립트로 재생 불가(확정, 재시도 금지)
#   ✅ 대신 Insert2D 는 **setPosition/setSize 가 Anim 을 받는다** → 이미지 한 장을
#      돔에서 부드럽게 움직이고 키워서 '다가옴/지나감'을 만든다.
#   · 접근    = setSize 작게→크게 + setPosition 낮게→높게
#   · 플라이바이 = setPosition 좌→우
#   · 프레임 flip = setTexture 를 sleep 간격으로 교체(저프레임 영상)
#
# ⚠️ 준비: localUserFolder(D:/SkyExplorer-Data/user)에 우주선 PNG(투명배경) 1장.
#    파일명 몰라도 되게 폴더를 자동 탐색한다.
from skyExplorer import *
from studio import *
from Initialization import *
import os

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 이미지 자동 탐색 ─────────────────────────────────────────
base = Configuration.configuration().localUserFolder
imgs = []
try:
    for f in sorted(os.listdir(base)):
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            imgs.append(base.rstrip("/\\") + "/" + f)
except Exception as ex:
    print("폴더 목록 실패:", ex)
print("사용할 이미지:", imgs[0] if imgs else "(없음 — PNG 1장 넣어주세요)")

# ── 별밭 배경 ────────────────────────────────────────────────
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(0.0, Anim(0.0))
# ⚠️ [2026-08-12] 암전은 **reset 보다 먼저**. reset 뒤에 걸면 그 사이 직전 장면이 그대로 보인다
#    (돔 실측: 토성이 잠깐 보였다 사라짐). reset 은 밝기를 1.0 으로 되돌리니 뒤에서 다시 눌러야 한다.
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth)
earth.setIntensity(1.0, Anim(0.0))
earth.setAtmosphereIntensity(0.0, Anim(0.0))
earth.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.7, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 8, 1, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0))
cam.setTargetHeight(30.0, Anim(0.0))
sleep(2.0)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 20, 0)); t1.setSize(0.052)
t1.setColor(Vec(1.0, 1.0, 0.55)); t1.setDistance(1.0, Anim(0.0))
t1.setText("저 멀리 무언가 다가온다"); t1.setIntensity(1.0, Anim(1.0))
sleep(3.0)

# ── Insert2D 붙이기 ──────────────────────────────────────────
ship = Insert2D(Insert2D.Insert2DName.Insert2D001)
cam.addChild(ship.id, Camera.CameraPort.FixedForeground)
if imgs:
    ship.setTexture(imgs[0])
ship.setIntensity(1.0, Anim(0.0))

# ── ① 접근: 작은 점(낮은 곳) → 크게(위로) ───────────────────
ship.setSize(0.04, Anim(0.0))
ship.setPosition(Vec(0.0, 8.0, 0.0), Anim(0.0))
sleep(0.5)
ship.setSize(0.55, Anim.cubic(6.0))              # 커짐 = 다가옴
ship.setPosition(Vec(0.0, 42.0, 0.0), Anim.cubic(6.0))
sleep(6.5)

t1.setText("가까이서 보니 탐사선이었다"); sleep(3.5)

# ── ② 플라이바이: 좌 → 우로 지나감 ──────────────────────────
ship.setPosition(Vec(-55.0, 42.0, 0.0), Anim(0.0)); sleep(0.4)
ship.setPosition(Vec(55.0, 42.0, 0.0), Anim.cubic(5.0))
sleep(5.5)

# ── ③ 멀어짐: 작아지며 아래로 ───────────────────────────────
t1.setText("그리고 다시 어둠 속으로")
ship.setSize(0.04, Anim.cubic(4.0))
ship.setPosition(Vec(55.0, 10.0, 0.0), Anim.cubic(4.0))
sleep(4.5)
ship.setIntensity(0.0, Anim(1.5))
sleep(2.0)
t1.setIntensity(0.0, Anim(1.5)); sleep(2.0)

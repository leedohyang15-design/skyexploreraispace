# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 부분확인(v5) — 돔 재생 4회 + 프레임 프로브 1회.
#    프로브(scripts/study/probe_geo_frame.py, 2026-08-12 사용자 확인)로 **확정된 것**:
#      ✅ A 관성 프레임 + **재조준 두 줄** → 지구가 돈다(하늘이 아니라)
#      ✅ B **동기 프레임 경도 128.2** 에 놓은 위성이 한반도 위에 붙어 지구와 함께 돈다
#      ✅ D 동기 프레임에서 위성으로 **진짜 줌인**이 된다(중앙 유지)
#      🛑 C **`OrbitalPlace` 궤도선은 못 쓴다 — 2026-08-13 판별 완료.**
#         판별 프로브의 A 단계가 **검증된 예제 코드 그대로**였는데 그것도 나선이었다
#         → 클래스 자체가 이 빌드에서 닫힌 원을 못 그린다(내 쇼의 버그가 아니다).
#      ✅✅ **대체 확정 (2026-08-13 사용자 스샷 4장)**: 궤도선 = **직접 구운 고리 모델**
#         (make_orbit_ring.py). **`RING_HPR = Vec(0,0,0)` 이 적도면에 눕는다**
#         (0,90,0 은 옆으로 섬 / 90,0,0 도 누움 — 같은 평면). **닫힌 원**으로 렌더되고,
#         **천리안이 그 고리 위에 정확히 얹힌다**(축척도 검증). 옆에서 보면 '선'이 된다.
#      ✅✅ **로켓 자세 확정**: `setOrientationHPR(Vec(경도 + 180, 90, 0))`.
#         바퀴살 프로브로 축을 잡고(경도 8곳), 돔 재생에서 **코가 지구를 향한 걸 보고 180 을 더했다**.
#      🛑 **우주에서 로켓을 옆에 달고 올라가는 구성은 버렸다 (v10).** 세 번 고쳐도 안 잡혔다:
#         크기(146°→76°) → 지면에 안 붙음 → 시선축 86° 로 밀림. 매번 다른 데가 틀렸다.
#         → **지상에서 올려다보는 발사**로 바꿨다. 거리가 수백 km 라 과장이 거의 필요 없고
#           로켓이 올라가며 작아지는 게 그대로 발사 장면이 된다.
#    ⚠️ **v10 에서 아직 돔에서 못 본 것**: Intro 딥스페이스(R 140→22→3.4) ·
#       **지상 발사 장면 전체**(⚠️ 지상 Sky View 에서 Insert3D 가 렌더되는지 미검증) ·
#       이름표 · 연도 타임랩스 · 은색 2A·2B 판 · Scene 4 반지름(8.6/16).
#    ✅ **[2026-08-13 원인 확정] '위성 분신술'·'옛 나선 궤도선'은 앞 실행 잔여였다** —
#       `reset(1)` 이 Insert3D·OrbitalPlace 슬롯을 안 비운다. `clear_leftovers()` 로 해결.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  "지구를 바라보는 하나의 눈 — 천리안 1호의 11년"   (약 5분)
#
#  ★ 어린이·가족 관람객.  ★ 스크립트는 **무음** — 나레이션·음악은 오퍼레이터가 입힌다.
#    대본과 큐시트: docs/27_chollian_narration.md
#
#
#  ⚠️⚠️⚠️ 규칙 1 — 자막 슬롯을 절대 섞지 마라
#     지상 = `setSize(0.052)` + `setDistance(1.0)` / 우주 = **크기를 만지지 말고** `setDistance(20)`
#     ⚠️ 크기를 되돌리는 API 가 **없다.** 그래서 핵심은 '`setSize` 를 안 부르는 것'이 아니라
#        **'슬롯을 갈아타는 것'** 이다. 지상 슬롯을 우주에서 재사용하면 크기가 남아 자막이 사라진다.
#        (이걸로 두 번 죽었다.) → **지상 슬롯 1, 우주 슬롯 5. 끝.**
#
#  ⚠️⚠️⚠️ 규칙 2 — 프레임 세 개를 구분해서 쓴다 (프로브로 확정)
#     · **관성(EquatorialJ2000)** = 카메라의 집. 여기 있어야 **지구가 도는 게 보인다.**
#       FadeTo 도킹 프레임(EquatorialSynchronous)에 그냥 두면 카메라가 자전을 따라 돌아
#       **지구는 멈추고 하늘이 돈다**("지구는 가만히 두고 왜 우주를 돌리냐" — v3·v4 가 이랬다).
#     · ⚠️ 프레임 전환은 **반드시 두 줄**: `setPositionLBR(..., 포트)` **+
#       `setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, 포트)`**.
#       v2 는 두 번째 줄을 빠뜨려 지구·위성이 통째로 화면 밖으로 나갔다.
#     · **동기(EquatorialSynchronous)** = 위성의 집. 이 프레임의 경도 = 지구 경도라서
#       **128.2 를 넣으면 한반도 위에 자동으로 붙는다.** 손으로 밀 필요가 없다.
#       (v4 는 관성 프레임 경도 0 에 박아 두고 손으로 밀면서 시간가속까지 걸어 **삼중 구동 →
#        급발진**했다. 이제 `RATE`·`tick()` 기계장치가 통째로 없다.)
#
#
#  ⚠️⚠️⚠️ 규칙 3 — 위성의 눈(동기 프레임)과 밖에서 보기(관성 프레임)를 **의도적으로** 나눈다
#     · **동기(sp)** 에 서면 지구가 안 도는 게 정상이다 — 정지궤도 위성이 보는 그림.
#     · **관성(ip)** 에 서야 지구가 도는 게 보인다 — 낮밤·정지궤도 설명은 여기서만 성립한다.
#
#  ══ v9 — 사용자 대본으로 전면 재구성 (2026-08-13) ══
#
#  대본 "지구를 바라보는 하나의 눈, 천리안 1호의 11년" 5장 구성을 그대로 옮겼다.
#
#  ⚠️⚠️ **사실 정정 — 16년이 아니라 11년이다.**
#     전 판은 "16년 / 2025년 12월 임무 종료"로 썼는데 **틀렸다.**
#     천리안 1호는 **2010-06-27 발사 → 2021년 4월 폐기궤도 이동**, 약 **11년** 운용이다.
#     (기상 임무는 2018년 2A, 해양은 2020년 2B 로 이관.) 대본이 맞고 내가 틀렸다.
#     → 스크립트·대본·패키지 문서의 연수와 날짜를 전부 11년/2021년 4월로 고쳤다.
#
#  ══ v10 — 돔 재생 지적 9건 반영 (2026-08-13) ══
#  ① **Intro 를 딥스페이스에서 시작** — R 140 → 22 → 3.4 로 두 단계로 파고든다
#  ② **발사를 지상에서 본다** — 쿠루에 서서 올려다본다. 우주 랑데부 구성은 버렸다
#  ③ **로켓 배율 1,000배 축소** (5.5e4 → 3.6e3) — "무슨 지구 반지름만 한데"
#  ④ **이름표를 넣었다** — 로켓 · 천리안 1호 · 2A · 2B (자막과 별개 슬롯)
#  ⑤ **Scene 2 의 '하늘이 도는' 현상 제거** — 동기 프레임 + 시간가속이면 배경 별이 돈다 → 별을 껐다
#  ⑥ **시간 타임랩스를 텍스트로** — 돔 시계 대신 연도(2011→2021)가 올라간다
#  ⑦ **2A·2B 를 은색 판으로** — 1호(금색)와 한눈에 갈린다
#  ⑧ **폐기궤도 8.6 + 카메라 16** — 이탈이 화면 밖으로 밀리던 걸 양쪽에서 고쳤다
#  ⑨ **마지막 세 위성 타블로 삭제** — 내가 만든 비트였다
#
#  ══ v11 — 돔 재생 지적 6건 반영 (2026-08-13) ══
#  ① **로켓 이름 = 아리랑 5호** (`ROCKET_NAME`) — 사용자 지시.
#     ※ 사실은 아리안 5(Ariane 5)이고 '아리랑'은 KOMPSAT 위성 이름이다. 한 줄만 고치면 되돌린다.
#  ② **Intro → 발사 전환에서 암전을 없앴다** — 발사장 상공에서 그대로 떨어진다(Land 레시피).
#  ③ **'로켓이 투명하다'의 진짜 원인 = 거리** — 333 km 때문에 대기 산란이 덮었다.
#     → 6.6 km 앞으로 당기고 배율을 3.6e3 → 50 으로 낮췄다.
#  ④ **발사를 짧게** — 상승 4단계 → 2단계, 끝나면 로켓을 페이드아웃.
#  ⑤ **Scene 2 의 '배경이 도는' 진짜 원인 = 시간가속** — 별을 끈 것과는 무관했다.
#     동기 프레임에서 5일을 흘리니 **터미네이터가 5바퀴 쓸고 지나갔다** → 시간을 안 흘린다.
#  ⑥ **위성이 지구 뒤로 숨는 것 = 각도 문제** — 투영 최소반지름 = 궤도R × cos(B).
#     6.611 × cos(62°) = 3.10 > 1 이므로 **B 62 에서는 절대 안 가려진다.** 막 3·4 에 적용.
#     + 막 4 는 탑뷰 → 오블리크 구도, 이탈 16초 → 8초.
#
#  ══ v12 — 돔 재생 지적 5건 반영 (2026-08-13) ══
#  ① **로켓 이름을 "아리안 5호"로 되돌렸다** (v11 의 '아리랑'을 사용자 지시로 원복).
#  ② **"지구로 들어간 다음 아리안이 안 보인다"** → 낙하를 **2단**으로 쪼개고(대기권 → 로켓 옆),
#     **로켓을 착지 직후 바로 켠다**(돌아서면 발사대가 이미 서 있다). 배율 50 → **150**,
#     거리 6.6 → **11 km** = 겉보기 앙각 0→37°. v11 은 산란을 피하려다 **너무 작게** 만들었다.
#  ③ **"궤도마다 자막을 달아 줘"** → `ring_tag()` 신설. 금색 = "정지궤도 · 3만 6천 km",
#     회색 = "폐기궤도 — 여기로 비켜난다". ⚠️ 자막(1·5)·이름표(2·6)와 **또 다른 슬롯(7·8)**.
#  ④ **"마지막 화면을 위에서 말고 옆에서 위성 기준으로"** → Scene 4 를 **동기 프레임**으로 옮기고
#     B 62 → **24**(옆), 경도를 위성에서 20° 벌려 위성이 앞에 잡히게. 고리는 옆으로 눕는다.
#  ⑤ **"마지막에 지구 야간 화면은 뭥미"** → **그 비트를 뺐다.** 밤면 정면 + R 3.4 라 거의 캄캄한
#     원반만 남았다(도시광 몇 점). 이제 이탈에서 **바로 청주 밤하늘로 착지**한다.
#
#  ══ v13 — 돔 재생 지적 2건 (2026-08-13) ══
#  ① **"각각의 부품 명칭을 자막으로"** → Scene 2 에서 위성이 도는 동안 부품 이름을 차례로 띄운다
#     (태양전지판 → 솔라세일 → Ka 주안테나 → 기상 관측기 → 해양 관측기). 슬롯 **9**.
#  ② ⚠️⚠️⚠️ **"줌 땡기면 천리안이 안 보인다"(L 0 · B 62 · R 57,403km 스샷) — Scene 3 의 진짜 버그를 찾았다.**
#     그 장면만 **관성 프레임에 카메라를 세우고 경도를 0** 으로 줬는데, 위성은 **동기 프레임 경도 128.2**
#     에 있다. **두 프레임의 경도는 서로 아무 관계가 없다** → 카메라가 위성 없는 쪽을 보고 있었다.
#     내가 두 번(v11·v12) '가림 각도' 로 진단한 게 **둘 다 틀렸다** — 각도가 아니라 **프레임**이었다.
#     → Scene 3 도 **동기 프레임**으로 옮기고 카메라 경도를 위성과 같게(128.2). B 62 → **16**,
#       R 9.0 → **8.6** = 위성 겉보기 **11.4° → 31.9°**.
#
#  ══ v14 — "로켓 아직 안 보인다" (2026-08-13) ══
#  ⚠️⚠️⚠️ 사용자 지적이 정확했다: **"로켓을 미리 만들어 놓고 그곳으로 land·이동하면 되는 걸
#     왜 이렇게 복잡하게 생각하냐"** — 세 판(v11·v12·v13) 동안 배율·거리만 만졌는데,
#     진짜 문제는 **조준이었다.** 착지 후 카메라 heading 이 얼마인지 모르는 채
#     `setOrientationH(90)`('동쪽을 봐라')을 밀어넣었고, 그게 낙하가 남긴 자세와 싸웠다.
#  ✅ **뒤집었다 — 조준을 아예 안 한다.**
#     착지 후 **카메라가 실제로 보고 있는 heading 을 읽어서**(`cam.orientationHPR.x`),
#     방위 = 180 − H 로 환산해 **그 방향 11 km 앞에 로켓을 세운다.**
#     조준 명령이 없으니 싸울 것도 없고, 값이 뭐가 나오든 **로켓은 반드시 화면 안**이다.
#     (heading 을 못 읽으면 기존 '동쪽 기본값'으로 떨어진다 — 로그에 찍힌다.)
#  ✅ 관측자 고도 10 m → **300 m**. 10 m 면 지평선이 11 km 라 로켓 밑동이 걸린다(62 km 로 늘어난다).
#  ✅ **부품 설명을 화살표로** — `DomePointer`(검증된 돔 화살표)를 부품마다 찍고 이름을 그 옆에.
#     회전은 **설명 전에 끝낸다**(도는 물체에 화살표를 대면 가리키는 게 어긋난다).
#     ⚠️ **미검증**: DomePointer 는 지상에서만 확인됐다. 우주 프레임에서 안 뜨면 `SHOW_POINTERS = False`
#        → 이름만 뜨는 v13 방식으로 돌아간다. 화살표가 부품에서 어긋나면 `PART_AZ0`/`PART_H0` 두 값만 옮긴다.
#  ✅ **막4 를 '지구 옆'으로** — "지구를 태양처럼 가운데 두고 궤도가 옆으로 이동하는" 그림.
#     `B_LEAVE` 24 → **8**(거의 궤도면 안). 위성 겉보기 19.2° → 27.2°, 지구 중심에서 19.7° → 38.7° 로
#     **옆으로 19° 를 가로지른다.** 고리는 옆에서 보니 가는 선이 되지만 '밀려 나가는' 건 이 각도가 제일 또렷.
#
#  ══ v15 — "위성이 안 보인다"의 진짜 원인 = **조명** (2026-08-13 스샷으로 확정) ══
#  스샷 HUD: `L 128°12'E · B 16°N · R 54,852 km` = Scene 3, **카메라는 제자리였다.**
#  그런데 **지구가 초승달**이었다 = 밤면을 보고 있었고, 위성도 그늘에 들어가 **검은 배경에 검은 물체**.
#  ⚠️ 원인: 이 장면이 **27시간**을 흘렸다. 동기 프레임에서 우리는 경도 128.2 에 고정인데
#     태양 직하점은 시간당 15° 서쪽으로 간다 → 15:00 UTC 면 직하점이 45°W = **우리는 한밤**.
#  ✅ **계산으로 못 박는다: 직하점 경도 = 180 − 15×UTC. 우리와 80° 안쪽이어야 낮.**
#     → 시간 흐름을 **+5시간(03:30 → 08:30)** 으로 줄였다(76° = 늦은 오후, 아직 낮).
#  ✅ **위성 모델을 자체발광으로** — `emissionColor` 0.12 → **0.55**(궤도 고리가 늘 보이는 이유가 이것).
#     ⚠️ **`make_chollian_model.py` 를 다시 돌려야 반영된다.**
#  ✅ **부품 설명 = 화살표(DomePointer) → 지시선(DrawableInsert)** — "돔포인터는 가독성이 없다".
#     부품에서 바깥 이름표까지 선을 긋고 부품 쪽 끝에 짧은 눈금을 찍는다.
#
#  구성 (대본의 시간표를 따른다)
#    Intro    광활한 우주와 하나의 결심          0:00–0:40
#    Scene 1  쿠루 우주센터와 카운트다운          0:40–1:20
#    Scene 2  3만 6천 km 상공의 파수꾼           1:20–2:20
#    Scene 3  임무 연장과 헌신                   2:20–3:20
#    Scene 4  마지막 여정, 폐기궤도로의 이동      3:20–4:20
#    Outro    유산과 기억                        4:20–5:00
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *
import math

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

MODEL = "chollian.osg"

SLOT_GROUND = 1               # 지상 전용. setSize 를 거는 유일한 슬롯
SLOT_SPACE = 5                # 우주 전용. **영원히 setSize 를 부르지 않는다**

# ★ 자막을 통째로 끄는 스위치. 화면만 보고 싶을 때 False.
#   길이·타이밍은 그대로 유지된다(자막이 없어도 같은 박자로 흘러간다).
SHOW_TEXT = False

# ★★ **이름표**는 자막과 별개다 (2026-08-13 지시).
#   "로켓에 이름 박기" · "천리안 1호랑 나머지 위성이랑 분간이 안 가"
#   → 물체 이름만 짧게 띄운다. 자막(SHOW_TEXT)을 꺼도 이건 나온다.
#   ⚠️ 자막 슬롯 규칙은 그대로 — **지상용/우주용 슬롯을 절대 섞지 않는다.**
SHOW_LABELS = True
SLOT_LABEL_GROUND = 2         # 지상 전용(setSize 를 거는 슬롯)
SLOT_LABEL_SPACE = 6          # 우주 전용(setSize 를 영원히 안 부르는 슬롯)

# ★ 궤도선 스위치. 보기 싫으면 이 한 줄만 False (길이·타이밍은 안 바뀐다).
SHOW_RINGS = True

# ⚠️⚠️⚠️ [2026-08-13 확정] **`OrbitalPlace` 는 이 빌드에서 닫힌 원을 못 그린다 — 버렸다.**
#   판별 프로브(probe_orbit_spiral.py)의 A 단계가 **검증된 예제(orbital_satellites.py) 코드 그대로**
#   였는데 **그것도 나선**이었다. 즉 내 쇼의 버그가 아니라 클래스 자체가 안 되는 것이다
#   (SkySurvey·VideoPlayer 와 같은 '호스트/엔진 소관' 부류).
#   ⚠️ 예전에 "궤도 렌더됨"으로 적어 둔 기록은 궤도 5개가 겹쳐 있어 나선인 걸 못 알아본 것이다.
#   → **궤도선을 직접 구운 3D 모델로 바꿨다**(scripts/study/make_orbit_ring.py).
#     계산으로 그린 원이라 **전파기가 없다 = 나선이 될 수가 없다.** ✅ 돔에서 확인됨.
#   ⚠️ 쇼를 돌리기 전에 **생성기 세 개를 한 번씩** 돌려 유저 폴더에 파일을 만들어 둘 것:
#      make_chollian_model.py(위성) · make_orbit_ring.py(궤도선) · make_ariane5.py(로켓)
RING_GOLD, RING_GRAY = "ring_gold.osg", "ring_gray.osg"
RING_HPR = Vec(0.0, 0.0, 0.0)   # ✅ **확정** (2026-08-13 probe_ring_model.py, 사용자 스샷)
#   (0,0,0) = 적도면에 눕는다 ✅ / (0,90,0) = 옆으로 선다 ✗ / (90,0,0) = 누움(같은 평면) ✅
#   같은 프로브에서 **천리안이 고리 위에 정확히 얹히는 것**까지 확인 = 축척도 맞다.
RING_SLOT_GOLD, RING_SLOT_GRAY = 41, 42
SLOT_SAT, SLOT_2A, SLOT_2B = 5, 6, 7    # Insert3D 슬롯 — 위성 세 대

# ★ 돔 시계 — Scene 3 의 '수명 7년 타임랩스'. 시간가속을 걸면 바늘이 실제로 돈다(검증됨).
#   ⚠️⚠️ **기본 끔** — 돔에서 두 번 다 이상하게 나왔다("시계 또 지랄이네").
#   지상 장면에서만 검증된 HUD 라 우주 프레임에서는 자리·크기가 안 맞는 것으로 보인다.
#   살려 보고 싶으면 True 로 하고 `clock_hud()` 의 setDistance 를 1.0 ↔ 20 으로 A/B 할 것.
SHOW_CLOCK = False

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M          # 6.611 지구반지름 = 정지궤도
# 무덤궤도 — ⚠️ 실제는 정지궤도 300km 위(0.7% 차이 = 화면에서 안 보인다).
# "이탈할 때 너무 안 보인다"는 지적을 받아 **크게 과장**했다. 나레이션에서 고지한다.
GRAVE_R = 8.6                           # 10.5 → 8.6 (≈55,000km). GEO 6.611 대비 30% 바깥
#   ⚠️ 10.5 는 카메라(13)에 너무 가까워 이탈이 화면 밖으로 밀렸다("안 보여"). 30% 면 충분히 읽힌다
KOREA_LON = 128.2                       # 천리안 1호의 정지궤도 경도
LON_2A, LON_2B = 133.0, 123.5           # ⚠️ 실제 2A·2B 도 128.2 부근이지만 겹쳐 보여서 벌렸다

B_TOP = 88.0                  # 북극 위(현재 미사용 — 막4 를 오블리크 B_LEAVE 로 바꿨다)

# ★ Intro — 딥 스페이스에서 한반도 상공으로 (동기 프레임 하나로 처리)
# ⚠️ [2026-08-13 지시] "우리 은하 밖에서 줌인하면서 지구로 도달"
#   ⚠️ **은하 밖으로 실제로 나가는 레버는 없다**(검증된 방법이 없다). 대신 아주 멀리서 출발한다 —
#      R=140 이면 지구가 각지름 0.8° 짜리 점이고 은하수가 돔을 채운다. 화면상 '딥 스페이스'다.
R_DEEP = 140.0                # 지구는 점, 은하수가 돔을 채운다
R_MID = 22.0                  # 중간 — 지구가 원반으로 보이기 시작
R_INTRO_END = 3.4             # 발사장 상공(각지름 약 35°)

# ⚠️⚠️ [2026-08-13 지시] "장면1에서 장면2(로켓발사)로 갈 때 **암막 효과 빼고 그대로 낙하해서**"
#   → Intro 와 발사 장면 사이의 암전·reset 을 **없앴다.** 카메라가 발사장 상공에서
#     **그대로 지면까지 떨어진다**(R 3.4 → 0). 검증된 'Land' 레시피 그대로:
#       ① `setPositionLBR(Vec(L, B, 0), Anim.cubic(N), -1)`  (R → 0 하강)
#       ② `setOrientationHPR(Vec(현재 H, 0, 0), Anim.cubic(N))`  (수직하방 → 수평)
#     **둘을 동시에** 쏘아야 자연스럽다. 착지하면 state 가 SkyView 로 바뀐다(reset 불필요).
#   ⚠️ 그래서 **지상 세팅(관측지·시각·대기)을 하강 전에 미리** 걸어 둔다 — 착지 후엔 손댈 게 없다.
# ⚠️ [v12 지시] "지구 대기 어느 정도 들어간 다음에 아리안 위치로 이동해서 보여야 한다"
#   → 낙하를 **두 단계**로 나눈다. ① 대기권 상단까지 곧장 내려가고(R 3.4 → 1.05 ≈ 320 km)
#     ② 거기서 **로켓이 서 있는 자리 옆으로** 이동하며 지면에 닿는다(R 1.05 → 0).
#   ⚠️ 로켓은 **①이 끝나는 시점에 이미 켜 둔다** — 내려가면서 발사대가 보이는 게 목적이다.
R_ATMO = 1.05                 # 약 320 km — 대기권 상단
LAND_A, LAND_B = 8.0, 7.0     # ① 대기권까지 / ② 지면까지
# ⚠️ 지면(terrain)은 **켠 채로** 내려간다. 운영 규칙의 '지면 OFF'는 별을 보는 하늘 쇼 얘기고,
#    여기는 땅에 내려서는 장면이라 지면이 있어야 한다. 지저분하면 이 값을 0.0 으로.
GROUND_TERRAIN = 1.0

# ★ Scene 1 — 쿠루에서 정지궤도까지
# ★★ 아리안 5 로켓 — 직접 구웠다(scripts/study/make_ariane5.py).
#    ⚠️ 쇼를 돌리기 전에 그 생성기를 한 번 돌려 `ariane5.osg` 를 만들어 둘 것.
#    실물 치수: 높이 53m · 부스터 포함 폭 11.9m · 주황 EPC + 흰 부스터 2기 + 페어링.
ROCKET_MODEL = "ariane5.osg"
ROCKET_SLOT = 9
SAT2_MODEL = "chollian2.osg"  # ★ 2A·2B 는 **은색 판** — 1호(금색)와 구분되게 따로 구웠다
# ⚠️⚠️ [2026-08-13 지시] **발사를 지상에서 본다.** "로켓 발사하는 걸 그냥 지구 안에서 보여주는 게 낫겠다"
#   + "로켓이 너무 크다 — 무슨 지구 반지름만 한데".
#   → 우주에서 로켓을 옆에 달고 올라가던 구성을 **통째로 버렸다**(세 번 고쳐도 구도가 안 잡혔다).
#     이제 **쿠루 지상에 서서 올려다본다.** 로켓은 하늘로 올라가며 작아진다 — 진짜 발사 장면이다.
#   ⚠️ 배율이 1,000배 이상 작아진다: 지상에서는 수백 km 거리라 과장이 거의 필요 없다.
KOURU_LAT, KOURU_LON = 5.2, -52.8       # 프랑스령 기아나 쿠루 발사장

# 로켓 이름. ⚠️ v11 에서 "아리랑"으로 바꿨다가 v12 에서 **"아리안 5호"로 되돌렸다**(사용자 지시).
#   실제 발사체가 아리안 5(Ariane 5)라 이게 맞다. 바꾸려면 이 한 줄만 고치면 된다.
ROCKET_NAME = "아리안 5호"

# ⚠️ 지상 Sky View 에서 Insert3D 가 렌더되는지는 v10 에서 처음 쓴다.
#    안 보이면 이 한 줄만 False — 로켓 없이 발사장 하늘만 나온다(길이·타이밍 동일).
LAUNCH_FROM_GROUND = True

# ⚠️⚠️ [2026-08-13 돔 실측] **"아리랑이 무슨 투명하다"** — 모델이 반투명하게 보인 원인은
#   재질이 아니라 **거리다.** 경도 3° 옆 = **333 km** 떨어져 있었고, 그 거리의 대기 산란
#   (aerial perspective)이 물체를 통째로 하늘색으로 덮어 씌운다. 그래서 하늘이 비쳐 보였다.
#   → **가까이·작게.** 6.7 km 앞에 세우면 산란이 거의 없어 색과 윤곽이 살아난다.
#   ⚠️ 경도 오프셋은 **각도**라 지상에서는 아주 작은 값이어야 한다:
#      거리 ≈ 지구반지름 × Δ경도(rad) × cos(위도) → 0.06° ≈ 6.6 km.
# ⚠️⚠️ [2026-08-13 v12] "지구로 들어간 다음 아리안이 안 보인다" — v11 에서 72배를 줄였더니
#   이번엔 **너무 작아졌다.** 산란(멀면 반투명)과 크기(가까우면 안 보임) 사이를 다시 잡는다:
#   11 km 앞 · 높이 8.4 km → **겉보기 앙각 0 → 37°, 폭 약 9°** = 돔에서 크고 또렷하다.
#   (v10 의 333 km 보다 30배 가까워 산란은 문제없다.)
ROCKET_SCALE = 150.0          # 모델 높이 56.2m × 150 ≈ 8.4 km
ROCKET_DIST_KM = 11.0         # ★ v14 — 카메라가 보는 방향으로 이만큼 앞에 세운다
ROCKET_LON_OFF = 0.10         # (heading 을 못 읽었을 때 쓰는 기본값 = 동쪽 ≈11 km)
# ⚠️ 관측자 고도 10 m 면 지평선까지 겨우 11 km — 로켓 밑동이 지평선에 걸린다.
#    300 m 로 올리면 지평선이 62 km 라 밑동까지 다 보인다. (발사대 언덕이라고 치면 된다.)
GROUND_ALT_M = 300.0
# ⚠️ [지시] "발사 어느 정도 되면 발사 끝내고" → 상승을 **두 단계로 줄였다**(전 4단계).
#    고도 0 → 12.8 km → 64 km. 돔을 가로질러 위로 오르며 23° → 11° → 2.5° 로 작아진다.
ROCKET_R = [1.0000, 1.0035, 1.0150]

# ✅ 자세 = `HPR(경도 + 180, 90, 0)` — 확정(바퀴살 프로브 + 돔 재생).
#   모델 +Z 는 북극을 향하므로 pitch 90 으로 눕히고 heading 을 그 물체의 경도로 준다.
#   ⚠️ 그것만으론 코가 지구를 향한다(바퀴살은 축만 갈랐지 부호는 못 갈랐다) → **+180**.
ROCKET_HEAD_OFF = 180.0       # ⚠️ 코가 지구를 향하면 이 값을 0 으로

# ★ Scene 2 — 파수꾼 (위성 옆에서 지구를 함께 본다)
R_WATCH_A, R_WATCH_B = 10.0, 8.3
#  ⚠️ 7.6 은 위성까지 6,300km 라 태양전지판 하나가 돔을 다 덮었다(돔 실측).
#     8.3 이면 10,800km — 위성이 화면 절반, 뒤로 지구도 들어온다

# ★ Scene 3 — 세월이 흐른다
# ⚠️⚠️⚠️ [2026-08-13 v13 돔 실측] **"줌 땡기면 천리안이 안 보인다"** — 스샷: L 0 · B 62 · R 57,403 km.
#   내가 두 번이나 '가림(occlusion) 각도' 문제로 진단했는데 **둘 다 틀렸다.** 진짜 원인은 이것이다:
#     이 장면만 **관성 프레임(ip)** 에 카메라를 세워 놓고 **경도를 0** 으로 줬다.
#     그런데 위성은 **동기 프레임의 경도 128.2** 에 있다. **두 프레임의 경도는 서로 아무 관계가 없다.**
#     → 카메라가 위성이 없는 쪽을 보고 있었다. 각도를 아무리 만져도 안 보이는 게 당연했다.
#   ✅ **해법 = 이 장면도 동기 프레임(sp)에 선다.** 그러면 위성 경도가 128.2 로 고정이라
#     카메라를 **같은 경도**에 두면 반드시 화면에 든다(가림 계산도 필요 없다 — 늘 앞에 있다).
#   ⚠️ **대가**: 동기 프레임이라 지구가 자전으로 도는 그림은 사라진다. 대신 시간이 흐르면
#     **낮/밤 경계가 표면을 쓸고 지나간다** — '세월이 흐른다'는 이 장면의 주제엔 이게 오히려 맞다.
#     (Scene 2 에서 같은 현상이 거슬렸던 건 거기가 '위성을 보는' 정지 장면이었기 때문이다.)
#   ⚠️ B 는 낮게. 계산: L=128.2·R=8.6 에서 **B 16 → 위성 겉보기 31.9°**(B 62 는 11.4° 였다).
B_TOGETHER, R_TOGETHER = 16.0, 8.6

# ★ Scene 4 — 이탈
# ⚠️⚠️ [2026-08-13 지시] "정지궤도서 폐기궤도로 가는 거 **다른 구도로 좀 빠르게** 볼 수 없나?
#    너무 느리고 너무 잘 안 보여."
#   → ① 구도를 **북극 탑뷰(B 88) → 비스듬한 오블리크(B 62)** 로 바꿨다. 고리가 원이 아니라
#        타원으로 눕고, 위성이 그 위를 **바깥으로 밀려 올라가는 게** 눈에 읽힌다(탑뷰는 평면적이었다).
#        B 62 = Scene 3 과 같은 이유로 **가림이 없는 각도**다.
#     ② 카메라를 **16 → 13** 으로 당겨 두 고리가 화면을 채우게 하고,
#     ③ 이탈 시간을 **16초 → 8초** 로 줄였다.
# ⚠️⚠️ [v12 지시] "마지막 화면을 위에서 보지 말고 **옆에서 위성을 기준으로** 보는 화면으로"
#   → 관성 프레임 위에서 내려다보던 구도를 버리고 **동기 프레임에 옆으로 선다.**
#     동기 프레임이라 위성(경도 128.2)이 화면에 붙박이고, 카메라를 경도 20° 옆에 두면
#     **위성이 앞에, 지구가 아래에, 두 고리가 옆으로 눕는** 그림이 된다.
#   ⚠️ B 24 = 여전히 가림 없음(6.611 × cos24° = 6.04 ≫ 1). 옆에서 보면서도 안 숨는다.
# ⚠️ [v14 지시] "그냥 아예 **지구 옆에서** 보는 게 구도가 더 나아 보여 — 정지궤도서 폐기로 가는 게"
#   → B 24 → **8**. 거의 궤도면 안에서 옆으로 본다.
#     계산: 위성 겉보기 19.2° → 27.2°(다가오며 커진다), 지구 중심에서 19.7° → 38.7° 로 **19° 를 가로지른다.**
#     고리 두 개는 옆에서 보니 **가느다란 선**이 되지만, '바깥으로 밀려 나가는' 움직임은 이 각도가 제일 또렷하다.
B_LEAVE = 8.0                 # 88(탑뷰) → 62 → 24 → **8(완전 옆)**
LON_LEAVE = KOREA_LON - 12.0  # 위성 경도에서 12° 옆
#   계산 확인(v13): 위성 겉보기 16.0° → 18.4°, 지구 중심에서 30° → 49° 로 **19° 를 가로질러** 밀려난다.
#   (오프셋 20° 는 끝에서 51° 까지 벌어져 화면 가장자리로 밀렸다.)
R_BACK = 11.0
R_OUT = 15.0
LEAVE_SECONDS = 8.0           # 16 → 8 ("너무 느리다")

# ★ Outro — 도시 불빛 → 지상
# ⚠️ [2026-08-13 지시] "마지막 위성 3개 있는 건 뭐냐" → **그 타블로를 통째로 뺐다.**
#    (2A·2B 는 대본 Outro 에도 있지만, 배율 ×2.2 로 부풀려 새 비트를 만든 건 내가 한 짓이다.
#     이제 2A·2B 는 Scene 3 에서 이름표와 함께 한 번만 나온다.)
B_CITY, R_CITY = 28.0, 3.4    # 한반도 밤 쪽을 내려다보는 자리(지구 각지름 ~35°, 불빛이 보인다)
R_LAND = 2.0                  # 지상 전환 직전까지 내려온다

SCALE_SAT = 1.0e6             # 반지름 5,270km — 처음에 고른 값(v4 의 5e5 는 "너무 작다")

H_SOUTH, TILT_SOUTH = 0.0, 40.0   # 청주에서 128.2°E 정지위성 = 고도 47.5°, 거의 정남

txt = None
ip = None                     # 관성 — 카메라의 집
sp = None                     # 동기 — 위성의 집
sat = None
rocket = None                 # ⚠️ Intro 에서 만든다(암전 안에서 로딩) — 막이 죽어도 NameError 안 나게


def _dark(sec=0.0):
    """암전 클램프. reset/FadeTo 는 밝기를 1.0 으로 되돌리므로 한 번 눌러선 안 된다."""
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def say(s, hold=None):
    """자막 교체. hold 를 안 주면 글자 수로 자동 계산(2초 + 글자당 0.1초)."""
    if txt:
        txt.setText(s)
    if hold is None:
        hold = 2.0 + len(s) * 0.1
    if hold:
        sleep(hold)


def feat(obj, fn, *args):
    try:
        getattr(obj, fn)(*args)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


class _NoText(object):
    """SHOW_TEXT=False 일 때 자막 자리에 들어가는 빈 껍데기 — 모든 호출을 삼킨다."""
    def __getattr__(self, n):
        def _f(*a, **k):
            return None
        return _f


def sub_ground():
    """지상 자막 — 슬롯 1. **여기서만** setSize 를 부른다."""
    if not SHOW_TEXT:
        return _NoText()
    t = InsertText(InsertText.InsertTextName(SLOT_GROUND))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setSize(0.052)
    t.setColor(Vec(1.0, 1.0, 0.55))
    t.setDistance(1.0, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


def sub_space():
    """우주 자막 — 슬롯 5. ⚠️ **setSize 를 절대 부르지 않는다**(부르면 화면에서 사라진다)."""
    if not SHOW_TEXT:
        return _NoText()
    t = InsertText(InsertText.InsertTextName(SLOT_SPACE))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setColor(Vec(1.0, 1.0, 0.55))
    t.setDistance(20.0, Anim(0.0))
    t.setIntensity(1.0, Anim(0.0))
    return t


_lab_g = [None]
_lab_s = [None]


def label(text, ground=False):
    """물체 이름표. ⚠️ 자막과 **다른 슬롯**을 쓴다(규칙 1). 빈 문자열이면 지운다."""
    if not SHOW_LABELS:
        return
    box = _lab_g if ground else _lab_s
    if box[0] is None:
        t = InsertText(InsertText.InsertTextName(
            SLOT_LABEL_GROUND if ground else SLOT_LABEL_SPACE))
        cam.addChild(t.id, Camera.CameraPort.FixedForeground)
        t.setPosition(Vec(0, 36, 0))
        t.setColor(Vec(0.75, 0.92, 1.0))
        if ground:
            t.setSize(0.046)                    # 지상만 크기를 건다
            t.setDistance(1.0, Anim(0.0))
        else:
            t.setDistance(20.0, Anim(0.0))      # 우주는 크기를 만지지 않는다
        box[0] = t
    box[0].setText(text)
    box[0].setIntensity(0.0 if not text else 0.95, Anim(0.6))


SLOT_TAG_GEO, SLOT_TAG_GRAVE = 7, 8      # ⚠️ 우주 전용 — setSize 를 영원히 안 부른다
SLOT_PART = 9                            # ★ [v13] 위성 '부품 이름' 전용 슬롯

# ★★ [2026-08-13 v14 지시] "자막을 화살표 같은 걸로 가리키면서" → "**돔포인터는 가독성이 없다.
#    그냥 지시선으로 바꿔**" → **`DrawableInsert` 로 돔에 지시선을 긋는다**(검증된 클래스).
#   부품 자리에서 바깥쪽 이름표까지 **선 하나**를 그어 뭘 가리키는지 분명히 한다.
#   ⚠️ **돔 좌표 규약(실측)**: az = 180 − 나침반방위 · **h = 돔 Target 좌표**(하늘 고도 아님).
#      Scene 2 는 카메라가 위성을 정면으로 보고 Target 30 이라 **위성 중심 ≈ (az 0, h 30)**.
#      → 화면에서 어긋나면 **아래 두 값만** 옮기면 다섯 개가 통째로 따라간다.
SHOW_LEADERS = True
PART_AZ0, PART_H0 = 0.0, 30.0
#   (이름, 부품 az, 부품 h, 이름표 az, 이름표 h) — 전부 위성 중심에서의 오프셋.
#   ⚠️ 이름표는 **부품보다 바깥**에 둔다. 선이 위성 위를 가로지르면 더 안 보인다.
PARTS = (
    ("태양전지판",         -13.0,   6.0,  -32.0,  17.0),
    ("솔라세일 — 균형추",   13.0,   6.0,   32.0,  17.0),
    ("Ka 대역 주안테나",     0.0,   1.5,    0.0,  24.0),
    ("기상 관측기 (MI)",    -5.5,  -8.0,  -28.0, -19.0),
    ("해양 관측기 (GOCI)",   5.5,  -8.0,   28.0, -19.0),
)
_tags = {}


def side_tag(slot, text, height, color, az=0.0):
    """★ 화면에 짧게 붙이는 보조 태그 — **궤도 이름**(v12)과 **위성 부품 이름**(v13)에 쓴다.
    ⚠️ 자막(1·5)·물체 이름표(2·6)와 **또 다른 슬롯**이다(규칙 1). 빈 문자열이면 지운다."""
    if not SHOW_LABELS:
        return
    t = _tags.get(slot)
    if t is None:
        t = InsertText(InsertText.InsertTextName(slot))
        cam.addChild(t.id, Camera.CameraPort.FixedForeground)
        t.setColor(color)
        t.setDistance(20.0, Anim(0.0))    # 우주 전용 — 크기는 건드리지 않는다
        _tags[slot] = t
    t.setPosition(Vec(az, height, 0))     # 화살표를 따라다닐 수 있게 매번 갱신
    t.setText(text)
    t.setIntensity(0.0 if not text else 0.95, Anim(0.8))


_drw = [None]


def point_at(name, daz, dh, laz, lh):
    """★ [v14] 부품에 **지시선**을 긋고 그 끝에 이름을 붙인다.
    ⚠️ 돔포인터(화살표)는 가독성이 없어서 버렸다(사용자 지적) — `DrawableInsert` 로 선을 긋는다.
    name="" 이면 선과 이름을 함께 지운다."""
    if not SHOW_LABELS:
        return
    az_t, h_t = PART_AZ0 + daz, PART_H0 + dh          # 선이 가리키는 곳 = 부품
    az_l, h_l = PART_AZ0 + laz, PART_H0 + lh          # 선이 끝나는 곳 = 이름표 자리
    if SHOW_LEADERS:
        try:
            d = _drw[0]
            if d is None:
                d = DrawableInsert(DrawableInsert.DrawableInsertName.DrawableInsert2D001)
                cam.addChild(d.id, Camera.CameraPort.FixedForeground)
                d.setBrushType(DrawableInsert.BrushType.Pen)
                d.setBrushSize(2.2)
                d.setIntensity(1.0, Anim(0.0))
                _drw[0] = d
            d.clearAll(Anim(0.15))
            if name:
                d.beginDraw()
                # 부품 → 이름표. 촘촘히 찍어야 끊기지 않는다(각 점이 한 획).
                for i in range(41):
                    t = i / 40.0
                    d.setBrushPosition(Vec(az_t + (az_l - az_t) * t,
                                           h_t + (h_l - h_t) * t, 0.0))
                # 부품 쪽 끝에 짧은 가로 눈금 — 어느 점을 가리키는지 못 박는다
                for i in range(9):
                    d.setBrushPosition(Vec(az_t - 2.0 + i * 0.5, h_t, 0.0))
                d.endDraw()
        except Exception as e:
            print("   x 지시선: %s" % e)
    side_tag(SLOT_PART, name, h_l + 2.5, Vec(0.72, 0.93, 1.0), az_l)


def fly(pos, seconds, port):
    """⚠️ 프레임을 옮기거나 그 안에서 움직일 때는 **반드시 두 줄**.
    조준을 같이 안 옮기면 카메라가 대상이 없는 쪽을 본다(v2 가 그렇게 화면을 날렸다)."""
    cam.setPositionLBR(pos, Anim(seconds), port)
    feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(seconds), port)


def stand(pos, port, target=30.0):
    """암전 중에 카메라를 어느 프레임의 어느 자리에 **즉시** 세운다.
    ⚠️ reset/FadeTo 뒤에는 밝기가 1.0 으로 되돌아오므로 단계마다 암전을 다시 누른다."""
    _dark()
    fly(pos, 0.0, port)
    _dark()
    cam.setTargetHeight(target, Anim(0.0))
    _dark()


def load_model(slot, model=None):
    """⚠️ 고정 sleep 으로 기다리면 Loading 인 채 지나간다(실측) — Loaded 뜰 때까지 폴링."""
    ins = Insert3D(Insert3D.Insert3DName(slot))
    model = model or MODEL
    path = model
    try:
        import os
        u = Configuration.configuration().localUserFolder
        if u:
            path = os.path.join(u, model)
    except Exception:
        pass
    ins.setModelFilename(path)
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        try:
            if "Loaded" in str(ins.loadingStatus):
                return ins
        except Exception:
            pass
    print("   ⚠️ 모델 로드 실패 — %s (유저 폴더에 있는지 확인)" % path)
    return ins


def hide(ins, times=3):
    """⚠️ **끈 게 안 꺼지는 일이 있다** — 모델이 로드를 마치며 밝기를 되돌리는 것으로 보인다.
    (돔 실측: 켜지면 안 되는 장면에서 궤도선·위성이 보였다.)
    → 한 번 끄고 끝내지 말고 **프레임을 사이에 두고 몇 번 다시 누른다.**"""
    for _ in range(times):
        feat(ins, "setIntensity", 0.0, Anim(0.0))
        sleep(0.15)


def clear_leftovers():
    """⚠️⚠️⚠️ **앞 실행이 남긴 개체를 전부 끈다. 돔에서 두 가지가 이걸로 깨졌다.**

      ① **'분신술'** — 위성이 둘로 보였다. 앞 쇼가 켜 둔 2A·2B(Insert3D 슬롯)가 살아 있었다.
      ② **'궤도선이 옛날 것'** — 나선 호가 다시 나왔다. v9 코드에는 `OrbitalPlace` 가
         **한 줄도 없다** — 새로 만들어질 수가 없다. 즉 화면의 그 호는 전부
         **앞 판(v8)이 켜 두고 간 `OrbitalPlace`** 였다.

    ⚠️ 원인은 하나다: **`SceneGraph().reset(1)` 은 Insert3D·OrbitalPlace 슬롯을 안 비운다.**
       씬을 초기화해도 이 개체들은 제 슬롯에 그대로 남아 다음 실행 화면에 끼어든다.
    → 쇼 첫머리에서 **우리가 쓰는 슬롯 범위를 싹 꺼 놓고** 시작한다. 이건 매번 해야 한다."""
    n = m = 0
    for i in list(range(0, 12)) + list(range(38, 50)):
        try:
            Insert3D(Insert3D.Insert3DName(i)).setIntensity(0.0, Anim(0.0))
            n += 1
        except Exception:
            pass
    for i in range(0, 10):
        try:
            o = OrbitalPlace(OrbitalPlace.OrbitalPlaceName(i))
            o.setOrbitIntensity(0.0, Anim(0.0))     # ★ 옛 나선 궤도선을 끈다
            try:
                o.setIntensity(0.0, Anim(0.0))
            except Exception:
                pass
            m += 1
        except Exception:
            pass
    print("   앞 실행 잔여 정리 — Insert3D %d개 · OrbitalPlace %d개" % (n, m))


def place_sat(slot, lon, scale=SCALE_SAT, model=None):
    """★ 정지궤도 위성 하나 — **동기 프레임의 경도**에 놓는다.
    이 프레임의 경도 = 지구 경도라서 그 자리에 붙고, 지구가 돌면 같이 돈다.
    손으로 밀 필요가 없다(v4 의 '급발진'은 손으로 밀면서 시간가속까지 걸어서 났다)."""
    ins = load_model(slot, model)
    hide(ins)
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setScale", scale, Anim(0.0))
    feat(ins, "setOrientationHPR", Vec(140.0, 20.0, 0.0), Anim(0.0))
    feat(ins, "setParent", sp if sp is not None else ip)
    feat(ins, "setPositionLBR", Vec(lon, 0.0, GEO_R), Anim(0.0))
    return ins


def ring(slot, model, radius_m):
    """궤도선 하나 — **직접 구운 고리 모델**을 지구 중심에 놓고 반지름만큼 키운다.

    ⚠️ `OrbitalPlace` 를 안 쓴다(위 주석 참조 — 이 빌드에서 닫힌 원을 못 그린다).
       고리는 반지름 1.0(미터) 짜리로 구워져 있으므로 `setScale(반지름[m])` 이 곧 궤도 반지름이다.
       정지궤도 42,164 km → setScale(4.2164e7).
    ⚠️ 부모는 **관성 프레임(ip)** — 궤도는 별에 대해 고정된 것이지 지면에 붙은 게 아니다."""
    if not SHOW_RINGS:
        return _NoText()
    ins = load_model(slot, model)
    hide(ins)
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))   # 그림자로 반쪽이 어두워지지 않게
    feat(ins, "setScale", radius_m, Anim(0.0))
    feat(ins, "setOrientationHPR", RING_HPR, Anim(0.0))
    feat(ins, "setParent", ip)
    feat(ins, "setPositionLBR", Vec(0.0, 0.0, 0.0), Anim(0.0))   # 지구 중심
    return ins


def clock_hud():
    """돔 시계 HUD — 수명을 세는 시계. ⚠️ `setModelset` 을 안 걸면 아무것도 안 그려진다."""
    if not SHOW_CLOCK:
        return None
    try:
        c = Clock(Clock.ClockName.Clock001)
        feat(c, "setModelset", Clock.Modelset.SystemClock001)
        cam.addChild(c.id, Camera.CameraPort.FixedForeground)
        feat(c, "setPosition", Vec(0.0, 62.0, 0.0))
        feat(c, "setSize", 0.34)
        feat(c, "setDistance", 1.0)
        feat(c, "setDisplaySecondsHand", True)
        feat(c, "setSecondsHandColor", Vec(0.95, 0.35, 0.25))
        feat(c, "setIntensity", 0.9, Anim(1.5))
        return c
    except Exception as e:
        print("   시계 실패: %s" % e)
        return None


def ground_night():
    """우주 → 지상 복귀. ⚠️ 검증된 경로는 **암전 속 reset(1) 후 지상 전체 재세팅**이다
    (좌표만 바꾸면 카메라가 우주 프레임에 남는다)."""
    _dark()
    SceneGraph().reset(1)
    _dark(1.5)
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))    # 지상 하늘 쇼 = 대기 OFF
    feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))       #               + 지면 OFF
    feat(earth, "setElevationScale", 0.0)
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.55, Anim(0.0))
    _dark()
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2026, 8, 12, 13, 0, 0, tz, Anim(0.0))     # 청주 22:00 KST
    _dark()
    sleep(0.4)
    cam.setOrientationH(H_SOUTH, Anim(0.0))
    _dark()
    cam.setTargetHeight(TILT_SOUTH, Anim(0.0))
    _dark()


def shadows(on):
    """지구 그림자 — 끄면 원반 전체가 밝고(운영 표준), 켜면 낮과 밤이 갈린다.
    ⚠️ 막4 는 **낮밤 자체가 주제**라 운영 표준(그림자 OFF)의 예외로 켠다(위상·일식과 같은 부류)."""
    if on:
        feat(earth, "setShadowStrength", 1.0, Anim(2.0))
        feat(earth, "setShadowContrast", 1.0, Anim(2.0))
        feat(earth, "setPlanetShineStrength", 0.05, Anim(2.0))
        feat(earth, "setNightLightsIntensity", 1.0, Anim(3.0))   # 밤면 도시광(호박색)
    else:
        feat(earth, "setShadowStrength", 0.0, Anim(1.0))
        feat(earth, "setShadowContrast", 0.0, Anim(1.0))
        feat(earth, "setPlanetShineStrength", 1.0, Anim(1.0))
        feat(earth, "setNightLightsIntensity", 0.0, Anim(1.0))


def enter_space():
    """FadeTo 지구 → 지구 렌더 복구 → 프레임 확보. 전 과정 암전.
    ⚠️ **카메라는 여기서 놓지 않는다** — 어디에 설지는 막마다 다르므로 각 막이 직접 fly 한다."""
    global ip, sp
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)

    # ⚠️ 막0 이 지상 하늘 쇼를 위해 꺼 둔 것을 되살린다.
    #    안 하면 지구가 회색 공이 되고, 가까이 가면 그릴 표면이 없어 **아예 사라진다**(실측).
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainModel", Planet.TerrainModel.BMNG_Ocean)
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))       # 구름은 막4 의 비트
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))
    _dark()

    ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
    for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
        try:
            sp = earth.portId(getattr(Planet.PlanetPort, nm))
            break
        except Exception:
            continue
    if sp is None:
        print("   ⚠️ 동기 프레임 포트를 못 찾았다 — 1인칭이 성립하지 않는다")
    _dark()


# ══ Intro : 광활한 우주와 하나의 결심 (0:00–0:40) ══════════════
# 대본: "깊은 밤하늘과 은하수 → 시점이 서서히 지구로 내려온다."
# ⚠️ [2026-08-13 지시] "우리 은하 밖에서 줌인하면서 지구로 도달" —
#    은하 밖으로 실제로 나가는 레버는 없어서, **아주 멀리(R=140)에서 두 단계로 파고든다.**
#    R=140 이면 지구는 각지름 0.8° 짜리 점이고 은하수가 돔을 채운다. 화면상 딥 스페이스다.
try:
    _dark()
    SceneGraph().reset(1)
    _dark(1.5)
    clear_leftovers()        # ★ 앞 실행 잔여 정리 — 분신술·옛 나선 궤도선의 원인
    _dark()
    enter_space()

    dm.stop()
    sleep(0.2)
    # ★ 시각을 **실제 발사 시각**으로 처음부터 맞춘다 — 낙하가 끊기지 않으려면
    #   지상 세팅(시각·관측지·대기)을 **내려가기 전에** 다 걸어 둬야 한다.
    dm.setDateTime(2010, 6, 26, 21, 41, 0, tz, Anim(0.0))   # 쿠루 현지 18:41, 저녁
    _dark()
    sleep(0.4)
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(KOURU_LAT, KOURU_LON, 10.0))
    feat(earth, "setTerrainIntensity", GROUND_TERRAIN, Anim(0.0))
    feat(earth, "setElevationScale", 0.0)
    _dark()

    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.75, Anim(0.0))   # 은하수를 진하게
    feat(earth, "setCloudsIntensity", 0.0, Anim(0.0))
    _dark()

    # ★ 로켓도 **지금** 실어 둔다(꺼 둔 채로). 모델 로딩은 최대 12초 폴링이라
    #   낙하 도중에 부르면 화면이 멈춘다 — 암전 안에서 미리 끝낸다.
    rocket = None
    if LAUNCH_FROM_GROUND and ROCKET_MODEL:
        rocket = load_model(ROCKET_SLOT, ROCKET_MODEL)
        hide(rocket)
        feat(rocket, "setShadowStrength", 0.0, Anim(0.0))
        feat(rocket, "setScale", ROCKET_SCALE, Anim(0.0))
        _rlon = KOURU_LON + ROCKET_LON_OFF
        feat(rocket, "setOrientationHPR",
             Vec(_rlon + ROCKET_HEAD_OFF, 90.0, 0.0), Anim(0.0))
        feat(rocket, "setParent", sp if sp is not None else ip)
        feat(rocket, "setPositionLBR",
             Vec(_rlon, KOURU_LAT, ROCKET_R[0]), Anim(0.0))   # 발사대 = 지표(R 1.0)
    _dark()

    sat = place_sat(SLOT_SAT, KOREA_LON)     # 미리 올려두되 꺼 둔다
    hide(sat)
    r_geo = ring(RING_SLOT_GOLD, RING_GOLD, GEO_R * EARTH_R_M)
    r_grave = ring(RING_SLOT_GRAY, RING_GRAY, GRAVE_R * EARTH_R_M)
    hide(r_geo)
    hide(r_grave)
    _dark()

    if sp is not None:
        stand(Vec(KOURU_LON, KOURU_LAT, R_DEEP), sp)   # ★ 아주 멀리 — 은하수만 보인다
    txt = sub_space()
    txt.setText("천리안 1호")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(3.5))
    sleep(4.0)
    say("기상과 바다를 스스로 볼 수 없던 시절", 5.0)

    # ★ 2단 하강 — 먼저 크게 파고들고(140→22), 이어서 **발사장 상공**까지(22→3.4)
    if sp is not None:
        fly(Vec(KOURU_LON, KOURU_LAT, R_MID), 14.0, sp)
    say("우리는 우주에 우리만의 눈을 가지려 했다", 7.0)
    say("저 작은 점이 우리가 사는 곳이다", 7.0)
    if sp is not None:
        fly(Vec(KOURU_LON, KOURU_LAT, R_INTRO_END), 14.0, sp)
    feat(earth, "setCloudsIntensity", 0.85, Anim(8.0))
    say("2010년 6월", 4.5)
    say("남아메리카 북동쪽 끝, 쿠루 우주센터로 내려간다", 7.0)
except Exception as e:
    print("Intro 오류:", e)

# ══ Scene 1 : 쿠루 우주센터 — ★지상에서 올려다본다 (0:40–1:20) ══
# ⚠️⚠️ [2026-08-13 지시] "로켓 발사하는 걸 그냥 지구 안에서 보여주는 게 낫겠다"
#    + "로켓이 너무 크다 — 무슨 지구 반지름만 한데"
#    → 우주에서 로켓을 옆에 달고 올라가던 구성을 **버렸다**(세 번 고쳐도 구도가 안 잡혔다).
#      이제 **쿠루 발사장에 서서 올려다본다.** 로켓이 하늘로 오르며 작아진다 = 진짜 발사 장면.
#    ⚠️ 배율이 1,000배 이상 작아진다(3.6e3). 지상에서는 거리가 수백 km 라 과장이 거의 필요 없다.
#    ⚠️ **미검증**: 지상 Sky View 에서 Insert3D 가 렌더되는지 확인된 적이 없다.
#       안 보이면 `LAUNCH_FROM_GROUND` 를 False 로 — 로켓 없이 지상 발사 하늘만 나온다.
try:
    # ★★★ 암전 없음. 앞 장면에서 **그대로 이어서 떨어진다.**
    #   검증된 'Land' 레시피 = R→0 하강과 pitch→0 을 **동시에** 발사.
    _cur_h = 0.0
    try:
        _cur_h = cam.orientationHPR.x
    except Exception:
        pass

    # ① 대기권까지 (R 3.4 → 1.05 ≈ 320 km). 아직 위에서 내려다보는 그림이다.
    cam.setPositionLBR(Vec(KOURU_LON, KOURU_LAT, R_ATMO), Anim.cubic(LAND_A), -1)
    say("지구의 대기 안으로 들어간다", LAND_A)

    # ② ★ 여기서 **로켓이 서 있는 자리로** 옮겨 앉으며 지면에 닿는다.
    #    ⚠️ [v12 지시] "아리안 위치로 이동해서 보여야 한다" — 착지점을 로켓 바로 옆으로 못 박는다.
    #    자세도 같이 일으킨다(수직하방 → 수평).
    cam.setPositionLBR(Vec(KOURU_LON, KOURU_LAT, 0.0), Anim.cubic(LAND_B), -1)
    cam.setOrientationHPR(Vec(_cur_h, 0.0, 0.0), Anim.cubic(LAND_B))
    say("발사장이 눈앞으로 다가온다", LAND_B)

    # 착지 — 관측지를 못 박는다(하강이 어디에 내려놓든 여기가 쿠루다).
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(KOURU_LAT, KOURU_LON, GROUND_ALT_M))
    txt.setIntensity(0.0, Anim(0.8))          # 우주 자막을 내리고
    txt = sub_ground()                        # ⚠️ 지상 슬롯으로 **갈아탄다**(규칙 1)
    txt.setText("2010년 6월 27일")
    cam.setTargetHeight(30.0, Anim(0.0))      # 🎯 관람 표준 틸트(30)
    sleep(0.6)                                # 자세가 반영될 한 박자

    # ★★★ [2026-08-13 v14 지시] "로켓을 미리 만들어 놓고 **그곳으로 land·이동**하면 되는 걸
    #   왜 이렇게 복잡하게 생각하냐" — 맞는 말이다. **조준을 아예 안 한다.**
    #   ⚠️ 여태 실패한 이유: 착지 후 카메라 heading 이 얼마인지 모르는데 `setOrientationH(90)` 로
    #      '동쪽을 봐라'고 밀어넣었다. 낙하가 남긴 자세와 싸우니 어디를 보는지 알 수 없었다.
    #   ✅ **뒤집는다 — 카메라가 실제로 보고 있는 방향을 읽어서, 그 자리에 로켓을 세운다.**
    #      조준 명령이 없으니 싸울 것도 없고, 어떤 값이 나오든 로켓은 반드시 화면 안에 있다.
    _lat, _lon = KOURU_LAT, KOURU_LON + ROCKET_LON_OFF     # 못 읽으면 쓰는 기본값(동쪽)
    try:
        _h = cam.orientationHPR.x                # 돔 heading
        _az = math.radians(180.0 - _h)           # 검증된 환산: 방위 = 180 − H
        _dd = ROCKET_DIST_KM / 6378.0            # 지구반지름 단위 각거리
        _lat = KOURU_LAT + math.degrees(_dd * math.cos(_az))
        _lon = KOURU_LON + math.degrees(_dd * math.sin(_az) /
                                        max(0.2, math.cos(math.radians(KOURU_LAT))))
        print("   로켓 배치 — 카메라 H %.1f (방위 %.1f) → 위도 %.4f 경도 %.4f"
              % (_h, 180.0 - _h, _lat, _lon))
    except Exception as e:
        print("   ⚠️ heading 을 못 읽었다 — 기본 동쪽에 세운다: %s" % e)

    if rocket:
        feat(rocket, "setOrientationHPR", Vec(_lon + ROCKET_HEAD_OFF, 90.0, 0.0), Anim(0.0))
        feat(rocket, "setPositionLBR", Vec(_lon, _lat, ROCKET_R[0]), Anim(0.0))
        feat(rocket, "setIntensity", 1.0, Anim(2.0))
    label(ROCKET_NAME, ground=True)              # ★ 로켓 이름표
    say("2010년 6월 27일, 쿠루 우주센터", 6.0)
    say("%s가 화염을 뿜으며 하늘을 가른다" % ROCKET_NAME, 6.5)

    # ★ 발사 — 두 단계로 짧게. 돔을 가로질러 오르며 작아진다(고도 0 → 12.8 → 64 km).
    #   ⚠️ [지시] "발사 어느 정도 되면 발사 끝내고" — 길게 끌지 않는다.
    for k, rr in enumerate(ROCKET_R[1:]):
        if rocket:
            feat(rocket, "setPositionLBR", Vec(_lon, _lat, rr), Anim(6.5))
        say(["그 정상에 천리안 1호가 실려 있다", "점이 될 때까지, 계속"][k], 6.5)
    if rocket:
        feat(rocket, "setIntensity", 0.0, Anim(2.5))   # 발사 끝 — 조용히 사라진다
    label("")
    say("지구 상공 3만 6천 킬로미터, 정지궤도를 향한 도약이다", 6.5)
except Exception as e:
    print("Scene 1 오류:", e)

# ══ Scene 2 : 3만 6천 km 상공의 파수꾼 (1:20–2:20) ══════════════
# ⚠️ [2026-08-13 지시] "천리안 위성 가만히 있고 하늘이 도는 씬은 뭔지 모르겠음"
#    → 원인: **동기 프레임에서 시간을 흘리면 배경 별이 돈다**(지구·위성은 고정이라 하늘만 돈다).
#      이 장면은 위성과 지구를 보는 자리지 하늘을 보는 자리가 아니다. → **별을 끈다.**
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    label("")
    SceneGraph().reset(1)
    _dark(1.5)
    clear_leftovers()
    _dark()
    enter_space()
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # ★ 하늘이 도는 걸 없앤다
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2011, 4, 1, 3, 30, 0, tz, Anim(0.0))
    _dark()

    sat = place_sat(SLOT_SAT, KOREA_LON)
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    r_geo = ring(RING_SLOT_GOLD, RING_GOLD, GEO_R * EARTH_R_M)
    r_grave = ring(RING_SLOT_GRAY, RING_GRAY, GRAVE_R * EARTH_R_M)
    hide(r_geo)
    hide(r_grave)
    if sp is not None:
        stand(Vec(KOREA_LON, 0.0, R_WATCH_A), sp)
    txt = sub_space()
    txt.setText("동경 128.2도")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)
    label("천리안 1호")                        # ★ 이름표
    # ★ 회전은 **부품 설명 전에 끝낸다** — 도는 물체에 화살표를 대면 가리키는 게 어긋난다.
    feat(sat, "setOrientationHPR", Vec(500.0, 20.0, 0.0), Anim(15.0))
    if sp is not None:
        fly(Vec(KOREA_LON, 0.0, R_WATCH_B), 15.0, sp)
    say("동경 128.2도", 4.0)
    say("지구가 도는 속도에 딱 맞춰 함께 돈다", 5.5)
    say("그래서 24시간 한반도를 내려다본다", 5.5)

    # ★★ [v14 지시] "자막을 그 **화살표 같은 걸로 가리키면서** 해야지"
    #   → 회전이 멈춘 위성에 화살표를 하나씩 대고, 이름을 그 옆에 띄운다.
    label("")                                  # 위성 이름표는 내리고 부품으로 넘어간다
    point_at(*PARTS[0])
    say("한쪽에만 날개가 달렸다 — 태양전지판이다", 5.5)
    point_at(*PARTS[1])
    say("반대편 막대 끝의 반사판이 그 힘을 받아 균형을 잡는다", 6.0)
    point_at(*PARTS[2])
    say("가운데 접시는 안테나, 아래 두 개가 관측기다", 5.5)

    # ⚠️⚠️ [2026-08-13 지시] "천리안 눈앞에서 돌려놓고 **갑자기 왜 배경은 왜 돌리는 거야**"
    #   → 별을 껐는데도 배경이 돌아 보인 진짜 이유: **여기서 시간을 5일치 흘렸다.**
    #     동기 프레임에서는 지구가 고정이라 **태양 각도(터미네이터)만 5바퀴 쓸고 지나간다** =
    #     지구 표면의 밝은 쪽이 빙빙 도는 것처럼 보인다. 별을 끈 것과는 무관한 별개 원인이었다.
    #   → **이 장면에서는 시간을 아예 안 흘린다.** 구름은 세기 페이드인만으로 충분히 보인다
    #     (검증된 사실: '구름이 밀려온다'는 setCloudCoverage 가 아니라 setCloudsIntensity 0→1).
    feat(earth, "setCloudsIntensity", 1.0, Anim(8.0))
    point_at(*PARTS[3])
    say("기상 관측기가 구름을 읽고", 5.0)
    point_at(*PARTS[4])
    say("해양 관측기가 바다를 읽는다", 5.0)
    point_at("", 0.0, 0.0, 0.0, 0.0)           # 지시선·이름 내린다
    say("태풍의 길목을 미리 알리고, 적조와 기름 유출을 감시했다", 6.5)
    say("가장 높은 곳에서 우리를 지켜보는 눈이었다", 5.5)
except Exception as e:
    print("Scene 2 오류:", e)

# ══ Scene 3 : 임무 연장과 헌신 (2:20–3:20) ══════════════════════
# ⚠️ [2026-08-13 지시] "시간 타임랩스 효과는 텍스트로 해도 괜찮을 듯. 돌면서 텍스트의 시간이 흐르는."
#    → 돔 시계를 버리고 **연도 텍스트가 올라가는** 방식으로 바꿨다. 지구가 도는 동안 2011→2021.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    label("")
    # ★ [v13] 관성(ip) → **동기(sp)**. 위성 경도 128.2 와 같은 경도에 서야 화면에 든다.
    stand(Vec(KOREA_LON, B_TOGETHER, R_TOGETHER), sp if sp is not None else ip)
    hide(r_geo, 1)
    hide(r_grave, 1)
    shadows(True)
    Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))    # 동기 프레임이라 별은 끈다
    _dark()
    txt = sub_space()
    txt.setText("설계 수명 7년")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)
    say("당초 설계된 수명은 7년", 4.5)
    say("2017년이면 끝났어야 할 기계다", 5.0)

    # ★ 연도 타임랩스 — 지구가 도는 동안 이름표 자리에 연도가 올라간다
    # ⚠️⚠️ [지시] "천리안 도는 궤도 좀 줄여야겠다" → **1.1일치(≈1바퀴)로 줄였다.**
    #   전 판은 4/6 → 4/3 = **3일치를 거꾸로** 흘려 위성이 3바퀴를 역주행했다. 그래서
    #   뒤로 갈 때마다 지구에 가려 사라졌다. 지금은 **앞으로 1바퀴**만, 그것도 B62 라 안 가려진다.
    # ⚠️⚠️⚠️ [2026-08-13 돔 실측 — 위성이 사라진 진짜 이유] 전 판은 **27시간**을 흘렸다.
    #   동기 프레임에서는 우리가 경도 128.2 에 고정이라, 시간을 흘리면 **태양 직하점이 지나가 버린다** —
    #   15:00 UTC 즈음엔 직하점이 45°W 라 **우리는 완전한 밤면**이고, 지구는 초승달, 위성은 칠흑이었다
    #   (사용자 스샷이 정확히 그 순간이다). 각도도 거리도 배율도 문제가 아니었다. **조명이었다.**
    #   ✅ 계산으로 못 박는다: 직하점 경도 = 180 − 15×UTC시각. 우리(128.2)와 **80° 안쪽이어야 낮.**
    #      03:30 → 0.7° (정오) · 08:30 → 76° (늦은 오후, 아직 낮) · 15:00 → 173° (한밤).
    #   → **+5시간(03:30 → 08:30)만 흘린다.** 터미네이터가 눈에 띄게 밀려오되 밤으로는 안 넘어간다.
    dm.setDateTime(2011, 4, 1, 8, 30, 0, tz, Anim(48.0))
    say("하지만 천리안 1호는 멈추지 않았다", 4.0)
    for _yr, _hold in (("2011", 3.2), ("2013", 3.2), ("2015", 3.2),
                       ("2017  설계 수명", 4.0), ("2019", 3.2), ("2021", 3.6)):
        label(_yr)
        sleep(_hold)
    label("")
    say("설계 수명을 넘긴 뒤로도 4년을 더, 모두 합쳐 11년", 6.0)

    s2a = place_sat(SLOT_2A, LON_2A, SCALE_SAT * 0.8, SAT2_MODEL)   # ★ 은색 판
    feat(s2a, "setIntensity", 1.0, Anim(2.5))
    label("천리안 2A")
    say("2018년, 천리안 2A 가 기상을 이어받고", 5.0)
    s2b = place_sat(SLOT_2B, LON_2B, SCALE_SAT * 0.8, SAT2_MODEL)
    feat(s2b, "setIntensity", 1.0, Anim(2.5))
    label("천리안 2B")
    say("2020년, 2B 가 해양과 환경을 이어받았다", 5.0)
    label("")
    say("후배들에게 바통을 넘길 때까지, 제자리를 지켰다", 5.5)
except Exception as e:
    print("Scene 3 오류:", e)

# ══ Scene 4 : 마지막 여정, 폐기궤도로의 이동 (3:20–4:20) ════════
# ⚠️ [2026-08-13 지시] "폐기궤도 갈 때 안 보이고 지구 남쪽으로 가니까 또 안 보여" →
#    ① 폐기궤도 반지름을 10.5 → 8.6 으로 낮추고 ② 카메라를 13 → 16 으로 더 물렸다.
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    label("")
    shadows(False)
    feat(earth, "setCloudsIntensity", 0.4, Anim(0.0))
    hide(s2a, 1)                                     # 이탈 장면은 1호만 본다
    hide(s2b, 1)
    dm.stop()
    sleep(0.2)
    # ★★ [v12 지시] "위에서 보지 말고 **옆에서 위성을 기준으로**"
    #   → 동기 프레임(sp)에 선다. 이 프레임의 경도 = 지구 경도라 **위성(128.2)이 화면에 붙박이**고,
    #     카메라를 20° 옆·B 24 에 두면 위성이 앞에, 지구가 아래에, 두 고리가 옆으로 눕는다.
    stand(Vec(LON_LEAVE, B_LEAVE, R_BACK), sp if sp is not None else ip)
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GEO_R), Anim(0.0))
    feat(sat, "setIntensity", 1.0, Anim(0.0))
    txt = sub_space()
    txt.setText("2021년 4월")
    _dark()

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.0)
    feat(r_geo, "setIntensity", 1.0, Anim(3.0))
    # ★ [v12 지시] "궤도마다 자막을 좀 달아 줘 — 뭐가 뭔지 모를 수도 있겠네"
    side_tag(SLOT_TAG_GEO, "정지궤도 · 3만 6천 km", 46.0, Vec(1.0, 0.85, 0.35))
    label("천리안 1호")
    say("2021년 4월, 임무가 끝났다", 4.5)
    say("저 금색 원이 11년을 돈 자리다", 5.0)
    feat(r_grave, "setIntensity", 0.9, Anim(3.0))
    side_tag(SLOT_TAG_GRAVE, "폐기궤도 — 여기로 비켜난다", 54.0, Vec(0.80, 0.84, 0.88))
    say("다른 위성과 부딪히지 않도록, 스스로 몸을 일으킨다", 5.5)

    # ★★ 이 한 줄이 이 장면의 핵심 — 금색 원에서 회색 원으로 건너간다
    # ⚠️ [지시] "너무 느리다" → 16초 → 8초. 오블리크 구도라 '바깥으로 밀려 올라가는' 게 읽힌다.
    feat(sat, "setPositionLBR", Vec(KOREA_LON, 0.0, GRAVE_R), Anim(LEAVE_SECONDS))
    say("남은 연료를 모두 태우며, 정지궤도보다 높은 폐기궤도로", 6.5)
    say("(실제로는 300km 남짓 위다. 보이라고 크게 그렸다)", 5.5)

    feat(sat, "setIntensity", 0.30, Anim(7.0))
    label("")
    fly(Vec(LON_LEAVE, B_LEAVE, R_OUT), 12.0, sp if sp is not None else ip)
    say("모든 통신을 차단하고", 5.0)
    say("11년의 임무를 마친 채", 5.0)
    say("영원한 우주의 휴식에 들어간다", 5.5)
except Exception as e:
    print("Scene 4 오류:", e)

# ══ Outro : 유산과 기억 ════════════════════════════════════════
# ⚠️⚠️ [2026-08-13 v12 지시] "마지막에 지구 야간 화면은 뭥미"
#   → **그 비트를 통째로 뺐다.** 원래 의도는 '천리안이 11년간 지켜본 그 땅의 불빛'이었는데,
#     화면에는 **거의 캄캄한 원반**만 남았다. 그림자를 최대로 켜고(밤면 칠흑) R 3.4 까지 붙은
#     구도라 도시광 몇 점 말고는 읽을 게 없었다 — 마무리로 쓰기엔 화면이 비어 있었다.
#   → 이제 Scene 4 의 이탈에서 **바로 청주 밤하늘로 착지**한다. 비트가 하나 줄고 흐름이 붙는다.
#     (도시 불빛 장면을 되살리고 싶으면 이 자리에 shadows(True) + stand(Vec(KOREA_LON, 28, 3.4), sp)
#      를 넣고 낮/밤 경계 근처 시각으로 맞출 것 — 정면 밤면은 캄캄해서 안 된다.)
try:
    _dark()
    txt.setIntensity(0.0, Anim(0.5))
    sleep(0.6)
    label("")
    side_tag(SLOT_TAG_GEO, "", 46.0, Vec(1.0, 0.85, 0.35))
    side_tag(SLOT_TAG_GRAVE, "", 54.0, Vec(0.80, 0.84, 0.88))
    hide(sat, 1)
    hide(r_geo, 1)
    hide(r_grave, 1)
    _dark()
    ground_night()                                   # 청주 밤하늘 — 관객의 자리로
    txt = sub_ground()
    txt.setText("천리안 1호")
    _dark()
    uni.setGlobalIntensity(1.0, Anim.cubic(3.0))
    sleep(2.5)
    say("천리안 1호가 열어 준 길을 따라", 5.5)
    say("더 나은 위성들이 그 자리를 이어받고 있다", 6.0)
    say("우리 우주 역사의 첫 장을 연 이름 — 천리안 1호", 6.0)
    say("그 별은 지금도 저 높은 곳에서", 5.0)
    say("우리의 다음 도전을 내려다보고 있다", 5.5)

    txt.setIntensity(0.0, Anim(3.0))
    uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
    sleep(3.0)
except Exception as e:
    print("Outro 오류:", e)

print("쇼 종료 — 지구를 바라보는 하나의 눈, 천리안 1호의 11년")

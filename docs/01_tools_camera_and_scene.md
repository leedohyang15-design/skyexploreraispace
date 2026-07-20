# Sky Explorer 학습 노트 ① — 카메라 / 밝기 / 장면 연출 Tool

> 천체 투영 시뮬레이션 시스템 **Sky Explorer**를 LLM이 제어하기 위한 tool-use 스키마 모음.
> 원본 스크립트: [`scripts/tools_camera_and_scene.py`](../scripts/tools_camera_and_scene.py)

## 개요

이 도구들은 LLM이 자연어 지시를 받아 천체 투영(planetarium) 화면을 연출할 수 있도록
노출된 **함수 호출(tool-use) 인터페이스**다. 크게 세 갈래로 나뉜다.

1. 카메라 제어 (시점/위치/모드)
2. 밝기(Intensity) 제어 — 페이드 인/아웃
3. 장면 전환 & 화면 연출(오버레이)

---

## 1. 카메라 제어

| 도구 | 역할 | 핵심 파라미터 | 필수 |
|------|------|--------------|------|
| `set_camera_target` | 카메라가 **바라보는 방향(타겟)** | x, y, z, duration | x, y, z |
| `set_camera_position_lbr` | 카메라 **위치**를 경도(L)/위도(B)/거리(R) 구면좌표로 설정 | l, b, r, duration, reference_body | l, b, r |
| `set_camera_freefly_mode` | 자유 비행(조이스틱/사용자 입력) 모드 전환 | 없음 | - |
| `stop_camera` | 자동 이동/애니메이션 정지 | 없음 | - |

**핵심 포인트**
- **방향(target)** 과 **위치(position)** 가 분리된 개념. 시점을 돌리는 것과 카메라를 옮기는 것은 별도 도구.
- 위치는 절대 xyz가 아니라 **천체 중심 구면좌표(LBR)** 로 지정 가능. `reference_body`(예: `Sun`)를 주면 그 천체 기준, 없으면 절대 좌표계.
- `set_camera_freefly_mode` / `stop_camera`는 인자 없는 **상태 전환 도구**.

---

## 2. 밝기(Intensity) 제어 — 레이어 계층

밝기는 정규화된 `0.0~1.0` 값으로 통일되어 있고, 대부분 `duration`으로 부드러운 전환을 지원.

```
Universe (set_global_intensity)         ← 최상위, 0이면 완전 암전
├─ StarrySky (set_stars_intensity / get_stars_intensity)
├─ Galaxy    (set_galaxy_intensity, galaxy_name 기본 MilkyWay)
├─ Planet    (set_planet_intensity)
│  └─ Orbit  (set_planet_orbit_intensity)   ← 행성 궤도선 별도
└─ IndividualStar (set_individual_star_intensity, 예: Sun)
```

| 도구 | 대상 | default duration |
|------|------|-----------------|
| `set_global_intensity` | 전체 화면(Universe) | 1.0 |
| `set_stars_intensity` | 별 전체(StarrySky) | 1.0 |
| `get_stars_intensity` | 현재 별 밝기 **조회** (토글 전 확인용) | - |
| `set_galaxy_intensity` | 은하(이름 지정) | 1.0 |
| `set_planet_intensity` | 개별 행성 | 0.5 |
| `set_planet_orbit_intensity` | 행성 궤도선 | 0.5 |
| `set_individual_star_intensity` | 개별 별(예: Sun) | 0.5 |

**핵심 포인트**
- 행성/궤도/개별별 계열은 default duration이 **0.5**로 더 짧다(빠른 토글 의도).
- `get_stars_intensity`처럼 **조회 → 토글** 패턴이 의도되어 있음(현재 켜짐/꺼짐 확인 후 반전).
- 별인 태양(Sun)이 `StarrySky`가 아니라 `IndividualStar`로 분류된다는 점이 특징.

---

## 3. 장면 전환 & 연출

| 도구 | 역할 | 주요 파라미터 |
|------|------|--------------|
| `goto_database_object` | DB 등록 천체/장소로 화면 전환 트리거 | data_type, object_name, action_type |
| `smooth_reset` | 새 시퀀스 시작 전 초기 상태로 부드럽게 리셋 | with_logo |
| `show_text_insert` | 화면에 텍스트 오버레이 | text, azimuth, height, size, intensity |
| `show_image_insert` | 화면에 이미지 오버레이 | image_path, azimuth, height, size |
| `toggle_light_pollution` | 광공해 오버레이 on/off | enabled |

**`goto_database_object` 상세**
- `data_type`: `PlanetType`, `GalaxyType`, `MountainType`, `SpcType` 등
- `object_name`: 예 `Saturn`, `Milky Way`, `Mont blanc`
- `action_type`: `FadeTo`(기본), `ConnectTo`, `Play`
- 저수준 카메라/밝기 도구를 직접 조합하지 않고도 **고수준 연출을 한 번에 트리거**하는 추상화 계층으로 보임.

---

## 짚어둔 설계 패턴

- **좌표계 이원화**: 카메라는 `xyz` / `LBR`, 오버레이(text·image)는 `azimuth`/`height`(지평좌표계).
- **intensity 정규화**: 모든 밝기 도구가 `0.0~1.0`.
- **조회→토글 패턴**: `get_stars_intensity`로 상태 확인 후 set으로 반전.
- **추상화 계층**: `goto_database_object`(고수준) ↔ 개별 camera/intensity 도구(저수준).
- **duration 일관성**: 거의 모든 전환 도구가 `duration`으로 애니메이션 시간을 받아 cut이 아닌 부드러운 전환을 기본으로 함.

---

## 예상 연출 시퀀스 (이해 확인용)

> "토성으로 이동해서 보여줘" 같은 지시를 받았을 때의 전형적 흐름:

1. `smooth_reset()` — 장면 초기화
2. `set_global_intensity(1.0, duration=2)` — 페이드 인
3. `goto_database_object(data_type="PlanetType", object_name="Saturn", action_type="FadeTo")`
4. `set_planet_orbit_intensity("Saturn", 1.0)` — 궤도선 표시
5. `show_text_insert("토성", azimuth=..., height=...)` — 라벨 표시

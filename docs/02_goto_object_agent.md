# Sky Explorer 학습 노트 ② — "천체로 이동" 스킬 에이전트 (API 검증판)

> 원본 스크립트: [`scripts/goto_object_agent.py`](../scripts/goto_object_agent.py)
> 앞 노트: [`01_tools_camera_and_scene.md`](./01_tools_camera_and_scene.md)

`class_rst` HTML API 레퍼런스로 시그니처를 검증한 **실행 가능한 에이전트** 버전.
v1(스키마만 있던 버전)에서 도구 정의가 일부 수정·축소되었고, 실제 SDK 래퍼 / mock 모드 /
Claude 에이전트 루프 / 테스트·평가 루프가 추가됐다.

## v1 대비 변경점 (★ = 공식 문서로 검증된 수정)

| 항목 | v1 | v2 (검증판) | 비고 |
|------|----|-----------|------|
| ★ `set_camera_target` 좌표 | `Vec3(x, y, z)` | `Vec2(azimuth, height)` | **Vec3는 DEPRECATED.** 수평/고도 2값만 사용 |
| ★ `set_camera_position_lbr` 기준 | `reference_body: str` (예: "Sun") | `track: int` (DB portId, 기본 -1) | -1 = 현재 좌표계 |
| 도구 개수 | 16개 | 13개 | 아래 3개 제외 |
| 제외된 도구 | `show_text_insert`, `show_image_insert`, `toggle_light_pollution` | (없음) | 이 "이동" 스킬 범위 밖이라 빠진 것으로 보임 |
| 구현 형태 | 스키마(JSON)만 | SDK 래퍼 + 에이전트 루프 + 평가 | 실제 실행 가능 |

## 검증된 SDK 매핑 (래퍼 → 실제 호출)

| 래퍼 함수 | 실제 SDK 호출 |
|-----------|--------------|
| `set_camera_target` | `Camera(MainCamera).setTarget(Vec2(az, h), Anim(d))` |
| `set_camera_position_lbr` | `Camera(MainCamera).setPositionLBR(Vec(l,b,r), Anim(d), track)` |
| `set_camera_freefly_mode` | `AdvancedCamera().setModeFreeFly()` |
| `stop_camera` | `AdvancedCamera().stop()` |
| `set_global_intensity` | `Universe(MainUniverse).setGlobalIntensity(i, Anim(d))` |
| `set_stars_intensity` | `Stars(StarrySky).setIntensity(i, Anim(d))` |
| `get_stars_intensity` | `Stars(StarrySky).intensity` (속성 조회) |
| `set_galaxy_intensity` | `Galaxy(<name>).setIntensity(i, Anim(d))` |
| `set_planet_intensity` | `Planet(<name>).setIntensity(i, Anim(d))` |
| `set_planet_orbit_intensity` | `Planet(<name>).setOrbitIntensity(i, Anim(d))` |
| `set_individual_star_intensity` | `IndividualStar(<name>).setIntensity(i, Anim(d))` |
| `goto_database_object` | `DataManager.database().data(Data.Type.X, name).action(Action.Type.Y).trigger()` |
| `smooth_reset` | `smoothReset(with_logo)` (Initialization.py 재사용) |

**관찰 포인트**
- 카메라는 두 객체로 갈린다: 절대/타겟 제어는 `Camera(MainCamera)`, 모드/정지는 `AdvancedCamera()`.
- 밝기 계열은 전부 `setIntensity(value, Anim(duration))` 패턴으로 통일. `Anim(duration)`이 전환 애니메이션 래퍼.
- `getattr(EnumClass, name_str)`로 문자열 이름 → SDK enum 변환 (예: `Planet.PlanetName.Saturn`).
- `goto_database_object`는 `data → action → trigger` 체이닝(고수준 연출 트리거).
- SDK 미존재 시 `from skyExplorer import *` 실패 → **mock 모드** 자동 전환(print만).

## 에이전트 동작 구조

- `TOOL_FUNCTIONS`: 도구 이름 → 실제 파이썬 함수 디스패치 테이블.
- `TOOLS`: Claude에 넘기는 tool-use 스키마(검증된 시그니처 반영).
- `SYSTEM_PROMPT` 운영 규칙:
  1. 천체 이름은 영문 표기
  2. 큰 전환 전 `stop_camera`로 기존 애니메이션 정지
  3. 이동은 `goto_database_object` 우선, 세부 조정은 camera 도구 추가
  4. 타겟은 azimuth/height만 (Vec3 금지)
  5. 모호한 명령은 되묻기
- `run_agent`: `stop_reason == "tool_use"`인 동안 도구를 실행하고 `tool_result`를 되돌려주는 표준 tool-use 루프 (model: `claude-sonnet-4-6`).
- `evaluate`: 6개 테스트 케이스에서 `expected_tools ⊆ 실제 호출`이면 PASS.

## 테스트 케이스 ↔ 예제 파일 매핑

| 명령 | 출처 예제 | 기대 도구 |
|------|----------|----------|
| 토성 이동+고리 | FreeFlySaturn.py | stop_camera, goto_database_object, set_camera_freefly_mode |
| 태양계 전체+궤도 | FreeFlySun.py / Step.py | set_camera_target, set_planet_intensity, set_planet_orbit_intensity |
| 은하수로 비행 | FreeFlyMilkyway.py | goto_database_object, set_camera_freefly_mode |
| 화면 초기화 | Initialization.py | smooth_reset |
| 멈추고 몽블랑 | TrackballMontBlanc.py | stop_camera, goto_database_object |
| 태양/별/은하수 켜기 | Step.py (SolarSystemState) | set_individual_star_intensity, set_stars_intensity, set_galaxy_intensity |

---

## 학습 중 발견한 사항 (공식 문서로 확인 완료)

1. **`Vec` vs `Vec3` — ✅ 해소 (버그 아님)**
   공식 레퍼런스(`reference/api/Vec.md`) 확인 결과 **`skyExplorer.Vec`는 `alias of Vec3`** 다.
   즉 `setPositionLBR(Vec(l,b,r), ...)`는 `Vec3(l,b,r)`와 완전히 동일 → 코드 정상, 수정 불필요.
   (애초에 코드 독스트링이 `Vec3(l,b,r)`라고 적은 것도 맞는 표기.)
   - 공식 시그니처: `setPositionLBR((Camera), (Vec3)value, (Anim)anim, (int)track)` — `reference/api/Camera.md`

2. **`setTarget` — ✅ Vec2 확정** `setTarget((Camera), (Vec2)target [, (Anim)])`가 정식.
   `Vec3` 오버로드는 *"DEPRECATED: please prefer Vec2 parameter over Vec3"* 로 문서에 명시됨.
   노트 v2의 Vec2 수정이 공식 문서와 일치.

3. **`track` = referential id — ✅ 확인** 공식 설명: *"Database id of the referencial
   (For example, celestial body port). Set -1 to use current coordinate system, defaults to -1"*.
   독스트링("DB id")과 스키마("portId")는 같은 값을 가리킴. 용어만 통일하면 됨(기능 동일).

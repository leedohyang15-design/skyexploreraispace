# Sky Explorer 학습 인덱스

> 하나 배울 때마다 자동 갱신되는 학습 노트/스크립트 목록.
> 참고자료(API·도움말) 지도는 [`00_reference_index.md`](./00_reference_index.md).

## 학습 노트

| # | 노트 | 주제 | 관련 스크립트 |
|---|------|------|--------------|
| 00 | [reference_index](./00_reference_index.md) | 자료 지도 (API 70클래스 + 도움말 157토픽) | — |
| 01 | [tools_camera_and_scene](./01_tools_camera_and_scene.md) | LLM tool 정의: 카메라/밝기/장면 연출 | `scripts/tools_camera_and_scene.py` |
| 02 | [goto_object_agent](./02_goto_object_agent.md) | API 검증판 "천체로 이동" 에이전트 | `scripts/goto_object_agent.py` |
| 03 | [compare_freefly_solar](./03_compare_freefly_solar.md) | 내 구현 vs 정답: 태양계 행성 궤도 | `scripts/my_freefly_solar_orbits.py` |
| 04 | [compare_freefly_saturn](./04_compare_freefly_saturn.md) | 내 구현 vs 정답: 토성 (저수준 vs 고수준) | `scripts/my_freefly_saturn.py` |
| 05 | [face_earth](./05_face_earth.md) | 직접 설계: 지구 정면/정중앙 (실측 튜닝) | `scripts/my_face_earth.py` |
| 06 | [skill_center_on](./06_skill_center_on.md) | 스킬: 임의 천체를 돔 정중앙에 | `scripts/skill_center_on.py` |
| 07 | [more_tools_verified](./07_more_tools_verified.md) | 추가 명령어(별자리/성운/시간/텍스트/리셋) 검증 | `scripts/goto_object_agent.py` |
| 08 | [demo_scenarios](./08_demo_scenarios.md) | 자연어 시나리오 4종 → 연출 코드 | `scripts/demo_scenarios.py` |
| 09 | [api_code_digest](./09_api_code_digest.md) | **전체 70클래스/932메서드 코드 다이제스트 + 함정 총정리** | `reference/api/` 전체 |
| 10 | [help_scripting_digest](./10_help_scripting_digest.md) | 도움말 157토픽 중 코드/스크립트 운용 정리 | `reference/help/` 전체 |
| 11 | [summary](./11_summary.md) | **학습 결과 총정리 (캡스톤)** | — |
| 12 | [spc_horsehead](./12_spc_horsehead.md) | 말머리 성운 줌인+좌우회전 (SPC↔Python, 탐구) | `scripts/zoom_horsehead.py` |
| 13 | [sim_log_horsehead](./13_sim_log_horsehead.md) | **말머리 ST 실측 로그 (A~F) + 이전 결론 교정** | `scripts/zoom_horsehead.py` |
| 14 | [moon_analemma](./14_moon_analemma.md) | 달의 아날렘마 (MotionAnalemma 시간모드) | `scripts/moon_analemma.py` |
| 15 | [spc_format_and_converter](./15_spc_format_and_converter.md) | **SPC 포맷 역설계 + Python↔SPC 양방향 변환기** | `scripts/spc_convert/` |

## 핵심 정리 (지금까지 확정된 것)

- **카메라 제어 2계층**: 저수준(`Camera.setPositionLBR`/`setTarget` + `AdvancedCamera`) ↔ 고수준(`DataManager…action(FadeTo).trigger()`). 정확 구도=저수준, 단순 이동=고수준.
- **좌표 타입**: `setTarget`=`Vec2{azimuth,height}` (Vec3은 deprecated), `setPositionLBR`=`Vec3{L,B,R}`+`Anim`+`track(int)`. `skyExplorer.Vec`는 `Vec3`의 별칭.
- **기준 좌표계(track)**: `<body>.portId(<Port>)`로 id 획득. `Planet.PlanetPort` = Ecliptic/Equatorial/EquatorialSynchronous/Galactic/OrbitalMeanEquinox/EquatorialJ2000/NoonEcliptic/NoonEquatorial. `IndividualStar`는 `Ecliptic` 포트.
- **밝기**: 모든 객체 `setIntensity(value, Anim)` 공통. 행성 궤도선은 `setOrbitIntensity`. 전체는 `Universe.setGlobalIntensity`. 토성 고리는 본체 intensity에 포함.
- ⭐ **LBR의 R 단위는 좌표계마다 다름**: 행성 port 기준 = **행성 반지름**(가까이 보기엔 4~12), 태양/별 Ecliptic 기준 = **AU**. HUD는 크기에 따라 AU/km를 자동 전환 표시(성운 LOS서 `91919 AU` ↔ `88848 km` 목격)라 입력 스케일이 헷갈림. (HUD 표시값을 입력에 그대로 넣으면 안 됨 — 실측 함정.)
- ⚠️ **특정 천체 프레임 수동 조준은 프레임마다 규약이 달라 깨지기 쉬움**: `setOrientationXYZR(0,0,0,0)`=천체 안 봄(접선), 행성용 정중앙 스킬(`B=90`+`target125`)=성운 LOS선 위치가 극점으로 튐. ✅ **"천체를 화면 중앙에 크게"는 프레임 독립적인 `setZoomPosition`(대상 트랙)+`setZoomFov`로** (별=오리온·성운=말머리 둘 다 성공).
- ⭐ **(ST 실측 검증) 천체 중앙 '고정+공전'**: `setZoomPosition` 줌 락은 방향을 잠그는 게 아니라 **엔진이 자동 재조준**해 카메라가 움직여도 대상을 중앙 유지 → 그 위에서 **베이스 위치 `setPositionL` 스윙**으로 "대상을 축으로" 공전(롤 아님). 수동 pitch/heading 공전은 드리프트·짐벌로 실패. 근접 360°는 뒷면(검은 실루엣) 통과 → **정면 스윙 ±75°**. 줌 타깃 오프셋은 롤 유발(0 유지). 상세: **노트 ⑬(실측 로그)**, 탐구과정: 노트 ⑫.
- **표준 시퀀스**: `smoothReset(False)` → 암전 → 카메라/대상 설정 → 페이드인(`setGlobalIntensity(1, Anim.cubic(1))`) → `AdvancedCamera().setModeFreeFly()`.
- ⭐ **정중앙 공식(스킬)**: 천체를 돔 정중앙에 크게 = `B=90, target azimuth=0, target height=125, R=1.5`(반지름) + 대상 좌표계 port(행성=EquatorialSynchronous). "X로 향해줘" → `skill_center_on.goto_center(type, name)`. 상세: 노트 ⑥.
- ⭐ **아날렘마(Analemma 포트)**: 적도동기와 같지만 '자전 안 따르는' 프레임. 관측자를 `Planet.portId(PlanetPort.Analemma)`에 두고 시간 진행 → 자전 무시하고 아날렘마를 그림. 회전주기 기본=공전주기, `setAnalemmaRotationPeriod`로 위성 동기화(달=27.321661일). 지형 `setElevationScale(0)` 필수. `setDateTime`에 Anim=날짜 타임랩스. 상세: 노트 ⑭.
- **추가 명령어군**: 별자리(`setLines/Label/ArtIntensity`, setIntensity 없음), 성운/메시에(`setIntensity`), 시간(`DateManager.setDateTime/setCurrentDate/stop`, ⚠️TimeZone은 `UTC`/`Local` 없이 `DefaultTimeZone`·`UTC_P_00_00_MON` 등 436개), 텍스트(`InsertText` + `Camera.addChild(id, CameraPort.FixedForeground)`), 전체 리셋(`SceneGraph.reset(id)`). 상세: 노트 ⑦.

## 참고자료 추출 보관

`reference/` 에 핵심 API/도움말을 텍스트로 보관. 추가 추출은
`scripts/extract_reference.py` 사용(원본 아카이브 존재 시).

# Sky Explorer 자료 인덱스 — "어디에 뭐가 있는지" 지도

> 사용자가 제공한 공식 자료 2종의 내용 지도. 원본은 세션마다 초기화되는 업로드 폴더에 있으므로,
> 이 인덱스가 "무엇을 어디서 찾는지" 기준 역할을 한다.

## 자료 2종 개요

| 자료 | 형식 | 규모 | 성격 |
|------|------|------|------|
| **class.rst.zip** | Sphinx 스타일 HTML (클래스별 1파일) | 70개 파일 / 3.3MB | **Python API 레퍼런스** (SDK 시그니처의 1차 출처) |
| **HelpCenter_4.8.1_ko_KR.glp** | XLIFF 번역패키지(`.txlf`) | 157개 토픽 / 9.2MB | **사용자 도움말** (영어 원문 + 한국어 번역 양쪽 포함) |

- `.glp` 내부: `ko-KR/txlf/<토픽>.htm.txlf` — 각 파일은 `<source>`(en-US) + `<target>`(ko-KR) 세그먼트 쌍. 영/한 양방향 추출 가능.
- `.rst` HTML: `skyExplorer.<Class>.html` (59개) + `studio.<Class>.html` (11개).

---

## A. Python API 레퍼런스 (class.rst) — 클래스 지도

두 네임스페이스로 나뉜다. **이전에 학습한 도구들의 실제 출처가 여기 다 있음.**

### 네임스페이스 `studio.*` (11) — 시스템/제어 계층
| 클래스 | 역할 | 학습한 도구와 연결 |
|--------|------|-------------------|
| `AdvancedCamera` | 카메라 모드/정지 (FreeFly 등) | `set_camera_freefly_mode`, `stop_camera` |
| `Action` | 액션 타입(FadeTo/ConnectTo/Play) | `goto_database_object`의 action |
| `Data` | DB 데이터 타입(PlanetType 등) | `goto_database_object`의 data_type |
| `DataManager` | DB 접근(`database().data(...)`) | `goto_database_object` |
| `Configuration` | 환경 설정 | - |
| `ShowMonitor` | 쇼 모니터링 | - |
| `AudienceResponseSystem` / `VotingDevice` | 관객 응답/투표 | (도움말 AudienceResponseSystem) |
| `QObject` | Qt 베이스 클래스 | - |
| `Vec2` | 2D 벡터 (studio쪽) | - |

### 네임스페이스 `skyExplorer.*` (59) — 도메인 계층

**카메라/장면 (3)**: `Camera`, `SceneGraph`, `Universe`
→ `Camera`: `setTarget`, `setPositionLBR`, `setPositionXYZ` 등 / `Universe`: `setGlobalIntensity`

**천체 (20)**: `Planet`, `DwarfPlanet`, `Asteroid`, `Comet`, `Satellite`, `IndividualStar`, `Stars`, `Galaxy`, `Nebula`, `Messier`, `NGC`, `GlobularCluster`, `Constellation`, `OrbitalPlace`, `Body`, `Bolide`, `ShootingStar`, `SkySurvey`, `Patch`, `Light`
→ 대부분 `setIntensity(value, Anim)` 공통 패턴. `Planet`엔 `setOrbitIntensity`도.

**시간 (3)**: `Clock`, `DateManager`, `Ephemeris`

**오버레이/그래픽 (10)**: `Insert2D`, `Insert3D`, `InsertText`, `DrawableInsert`, `Place2D`, `Place3D`, `Mark`, `Line`, `Chart2D`, `Comment`
→ v1의 `show_text_insert`/`show_image_insert`가 여기 `InsertText`/`Insert2D/3D` 계열

**애니메이션 (2)**: `Anim`, `Animator`
→ `Anim(duration)` = 모든 전환 도구의 시간 래퍼

**오디오/미디어 (5)**: `Audio`, `AudioLayer`, `AudioLite`, `AudioPlayer`, `VideoPlayer`

**색/LUT (2)**: `Lut`, `ParameterizationLut`

**수학 (6)**: `Vec`, `Vec2`, `Vec3`, `Vec4`, `Mat`, `Mat4x4`
→ ⭐ **`Vec`/`Vec2`/`Vec3`/`Vec4`가 전부 별도 클래스로 존재.** 즉 `set_camera_position_lbr`의 `Vec(l,b,r)`는 오타가 아니라 실존 클래스 호출 (노트 ②의 의문 해소 — 단, LBR에 `Vec` vs `Vec3` 중 무엇이 맞는지는 Camera.html 본문 확인 필요).

**시스템/관리 (8)**: `SoftwareManager`, `ShowEngineManager`, `SlideShowHandler`, `RemoteShow`, `FreeDomeManager`, `DomePointer`, `DMX512`, `html`

> 도구↔클래스 상세 매핑은 `docs/02_goto_object_agent.md`의 SDK 매핑 표 참고.

---

## B. 사용자 도움말 (HelpCenter.glp) — 토픽 지도 (157개)

영/한 양쪽 텍스트 포함. 주제별 분류:

### 시작/기본 개념
`Start_SkyExplorer`, `Common`, `Studio`, `StudioData`, `Editor`, `ControlCenter`, `Environment`, `Architecture_&_Visualisation`, `SoftwareManagement`, `Deployment`, `UserManagement`, `Community`, `UserPages`

### 스크립팅/자동화
`Python`, `JavaScript`, `MacroCommands`, `Tags`, `Bookmark`, `Quick_Save`, `Backup`

### 천체 (도움말)
`AstronomicalObjects`, `PlanetsAndSatellites`, `Stars`, `StarrySky`, `MilkyWay`, `Asteroids`, `Comets`, `Bolides`, `BlackHole`, `Nebulae`, `Messier`, `NGC`, `GlobularClusters`, `OtherDeepSkyObjects`, `Molecules`, `ShootingStars`, `Constellations`, `OrbitalPlace`

### 천문 현상/계산
`Eclipses`, `MoonPhases`, `Tides`, `Analemma`, `Precession`, `Zodiacal light`, `ShadowCone`, `RevolutionRotation`, `OrbitsTrajectories`, `Zoom`

### 시간/좌표/기준계
`Clock`, `Time_and_date`, `FramesOfReference`, `Position`, `Orientation`, `Target`, `TraceMode`, `SpaceTimeGrid`, `Flattening`, `SeaLevel`, `Interpolation`

### 데이터셋/Live Atlas
`Live_Atlas`, `Introduction_to_Live_Atlas_Dataset`, `List_of_all_available_datasets`, `List_of_Solar_System_datasets`, `List_of_Galactic_datasets`, `List_of_Galactic_and_extra-galactic_*`, `List_of_extra-galactic_datasets`, `List_of_artificial_Earth_satellites(_*)`, `SkySurvey`, `JPL_Horizons`, `Data2Dome`, `Science_On_a_Sphere`, `Modelset`, `KML`, `AVMMetadata`

### 3D 모델 / 패치 / 환경
`3DModels`(최대 708세그먼트), `3DPlace`, `2DPlace`, `3Dmodel_ExportOSG_3DSmax`, `3Dmodel_ExportOSG_Blender`, `ListOfProlandModels`, `Patch`, `Advanced-patch-integration`, `Advanced_WMS_Patch_Integration`, `Clouds`, `Trees`, `Atmosphere`, `Nightlights`

### 미디어/오디오/비디오
`AudioHome`, `AudioMediaPlayer`, `AudioSkyEx`, `AudioVX`, `Audacity`, `FulldomeVideo`, `VideoEncoding`, `VideoStreaming`, `Slicing`, `Recording`, `DomeCasting`, `MultimediaWidget`, `InsertImageVideo`, `InsertText`, `Insert3D`, `SlideShow`, `Recommendations_for_multimedia_content`

### 오버레이/마크/UI 요소
`AstronomicalMarks`, `Placemark`, `Pointer`, `LabelManager`, `LinkingLine`, `Blackboard`, `Chart2D`, `Sky_Widget`, `MultimediaWidget`

### 하드웨어/돔/제어
`GamePad`, `iPad`, `Eclipse_Controller`, `AudienceResponseSystem`, `Room Lights`, `Introduction_to_FreeDome`, `Freedome_settings`, `SuperVision`, `Stereoscopy`, `InteractiveDomeView`, `RenderingModeCapture`, `DomeCasting`

### STEAM 교육
`STEAM__Arts`, `STEAM__Biology`, `STEAM__Chemistry`, `STEAM__Engineering`, `STEAM__Mathematics`, `STEAM__Physics`, `Experiences`

### 지원 파일 형식
`Supported3DmodelFileFormats`, `SupportedAudioFileFormats`, `SupportedFontFileFormats`, `SupportedImageFileFormat`, `SupportedPatchFileFormats`, `SupportedVideoFileFormats`

### 릴리스 노트
`ReleaseNotes-SkyExplorer2021~2025` (v4.4.0 ~ v4.8.1, 다수), `What_is_new_in_SkyExplorer_2025`

---

## 빠른 찾기 가이드 (작업별)

| 알고 싶은 것 | 보는 곳 |
|--------------|---------|
| SDK 함수 정확한 시그니처/파라미터 | `class.rst` → 해당 `skyExplorer.<Class>.html` 또는 `studio.<Class>.html` |
| 카메라 타겟/위치 (Vec2 vs Vec3) | `skyExplorer.Camera.html` |
| 밝기 setIntensity 범위/단위 | 각 천체 클래스 html (Planet/Stars/Galaxy/IndividualStar) |
| 기능 개념·사용법 (한국어 설명) | `HelpCenter.glp` → 해당 토픽 `.txlf`의 `<target>` |
| 신기능/버전 변경 | 도움말 `ReleaseNotes-*`, `What_is_new_*` |
| Python 스크립팅 전반 | 도움말 `Python`, `JavaScript`, `MacroCommands` |

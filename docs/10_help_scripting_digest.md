# 학습 노트 ⑩ — 도움말(HelpCenter) 코드/운용 다이제스트

> 157개 도움말 토픽(`reference/help/`, 영/한) 중 **코드·스크립트 운용**에 직접 관련된 것 정리.
> 전체 토픽 분류는 노트 ⓪(`00_reference_index.md`).

## 1. Python 스크립팅 운용 (토픽: Python)

- SkyExplorer는 **Python 스크립트로 시뮬레이션을 제어**함(우리가 짠 스크립트들이 이 방식).
- 작성: 일반 텍스트 에디터/IDE. 사용 가능한 API 목록은 Studio의 **Python 위젯**(도움말 아이콘 옆)에서 문서로 제공 → 이게 바로 우리가 추출한 `class.rst` HTML.
- **실행 방법 (Studio)**: `추가` 버튼 또는 드래그앤드롭으로 스크립트 임포트 → DB의
  `스크립트 > Python 스크립트` 섹션에 표시 → **더블클릭하면 재생**.
- **재생 패널**(측면 툴바)에서 실행 중 스크립트 관리 + **Python 디버거**로 사용, 오류 알림 표시.
- **Editor(SPC) 통합**: SPC 스크립트 안에 Python을 넣을 수 있음 → 주변장치 명령의
  `Studio Python / JS Script Play` 로 py 파일 로드.

## 2. JavaScript (토픽: JavaScript)

- Python과 유사하게 JS로도 제어 가능(`JsScriptType`). 실행 경로도 유사(Studio/Editor).

## 3. 매크로/쇼 명령어 (토픽: MacroCommands) — 연출 타임라인 제어

| 명령 | 역할 |
|------|------|
| `SHOW Macro` | **다른 스크립트를 호출**(같은 폴더면 이름만, 예 `MyScript.SPC`). 현재 스크립트와 **병렬 실행** |
| `SHOW Beginning` / `SHOW End` | 실행 창 시작/끝 표시. `SHOW End`를 늦은 타이밍에 두면 **실행 창을 계속 열어둠**(일시정지/중지 가능) |
| `SHOW Pause` | 스크립트 일시정지 |
| `SHOW Popup Text` | 팝업 텍스트 |

- 기본: 스크립트의 첫 명령은 **타이밍 0초**에 실행. 타이밍으로 시퀀스 구성.
- 시사점: 우리 데모의 `sleep()` 대신, Editor에선 명령별 **타이밍**으로 병렬/순차 연출 가능.

## 4. 태그 / 데이터 정리 (토픽: Tags, StudioData)

- **태그** = Studio 데이터를 폴더/하위폴더로 정리(2022부터 '가상 드라이브' 대체).
- 우리가 `DataManager.database().data(Data.Type.X, "name")` 로 접근하는 그 DB의 조직 체계.

## 5. 좌표계 / 시점 (토픽: FramesOfReference, Position, Orientation, Target, TraceMode, Zoom)

- 코드의 `portId(<Port>)`·`setPositionLBR`·`setTarget`·`setZoomFov`의 개념적 배경.
- **TraceMode** = 장노출(별궤적) 효과(추적 아님) — 노트 ⑧에서 확인.
- 좌표: L(경도)/B(위도)/R(거리), azimuth/height(지평), HPR(heading/pitch/roll).

## 6. 코드로 다룰 수 있는 콘텐츠 토픽 (대응 클래스)

| 도움말 토픽군 | 대응 API |
|--------------|----------|
| PlanetsAndSatellites, Asteroids, Comets, Stars, StarrySky, MilkyWay, Nebulae, Messier, NGC, GlobularClusters, Constellations | 노트 ⑨ §2 천체 클래스들 |
| Clock, Time_and_date, Eclipses, MoonPhases, Precession | `DateManager`/`Clock`/`Ephemeris` |
| InsertText, InsertImageVideo, Insert3D, SlideShow | `InsertText`/`Insert2D`/`Insert3D` |
| AudioSkyEx, AudioVX, FulldomeVideo | `Audio*`/`VideoPlayer` |
| Patch, SkySurvey, Live_Atlas, 3DModels | `Patch`/`SkySurvey`/`Model3D*` |
| GamePad, iPad, Eclipse_Controller, AudienceResponseSystem | 하드웨어/투표 클래스 |

## 7. 순수 운영/설치 토픽 (코드 무관, 참고용)

Deployment, SoftwareManagement, UserManagement, Backup, Quick_Save, VideoEncoding,
VideoStreaming, Slicing, Recommendations_*, Supported*FileFormats, ReleaseNotes-*,
STEAM__* (교육) — 코드보다 운영/콘텐츠 제작 가이드. `reference/help/`에 전문 보관.

---

## 요약: 학습 자료 → 코드 3계층 매핑

```
도움말(txlf)  →  "무엇을/왜"  (기능 개념, 실행 방법, 운용)
API(class.rst) →  "어떻게"    (클래스/메서드 시그니처 = 코드)   ← 노트 ⑨
예제(py)       →  "패턴"      (실전 조합: reset→설정→페이드→모드) ← 노트 ①~④,⑧
```
전량은 `reference/`(api 70 + help 157)에 보관, 요점·함정은 노트 ⑨/⑩ + ①~⑧.

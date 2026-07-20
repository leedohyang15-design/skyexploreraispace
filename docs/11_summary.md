# 학습 결과 총정리 (캡스톤)

Sky Explorer 천체투영 시스템을 코드로 제어하는 법을 자료 학습 + 실기(실제 실행/튜닝)로 익힌 기록.

## 1. 자료 3계층
```
도움말(txlf 157)  → "무엇을/왜"  (기능 개념·실행 방법)   → reference/help/
API(class.rst 70) → "어떻게"     (클래스·메서드 = 코드)  → reference/api/  (932 메서드)
예제(py)          → "패턴"       (실전 조합)             → scripts/
```

## 2. 핵심 코드 지식
- **생성**: `Class(Class.<Class>Name.X)`, 문자열은 `getattr(enum, "X")`.
- **밝기**: 어디서나 `setIntensity(value, Anim(t))`. 전체는 `Universe.setGlobalIntensity`. 궤도선 `Planet.setOrbitIntensity`. 단, **Constellation은 setIntensity 없음** → lines/label/art 개별.
- **좌표계 track**: `<body>.portId(<Class>Port.X)`. 행성=`EquatorialSynchronous`, 태양=`Ecliptic`, 은하=`Galactic`, 소행성/혜성=`Synchronous`.
- **카메라 2계열**: `setTarget(Vec2{az,height})`(궤도/트랙볼) vs `setOrientationHPR`(고개돌리기). 위치 `setPositionLBR(Vec3{L,B,R}, Anim, track)`.
- **고수준 이동**: `DataManager.database().data(Data.Type.X,"name").action(Action.Type.FadeTo).trigger()`.
- **모드**: `AdvancedCamera().setModeFreeFly()`.
- **오버레이**: `InsertText` → `Camera.addChild(id, CameraPort.FixedForeground)`로 화면 고정.
- **시간**: `DateManager().setDateTime(...)/setCurrentDate(...)/stop()`.
- **표준 시퀀스**: `smoothReset(False)` → 암전 → 설정 → 페이드인 → `setModeFreeFly()`.

## 3. 정중앙 스킬 (행성류 — 검증됨)
```
B=90, target azimuth=0, target height=125, R=1.5(반지름) + 대상 좌표계 port
```
→ `scripts/skill_center_on.py` (goto_center). 크기는 R로 독립 조절.

## 4. ⭐ 실기로 얻은 함정 12가지 (문서엔 없고, 돌려봐야 아는 것)
1. **LBR R 단위**: 행성=반지름, 태양/별=AU. HUD의 km/AU를 입력에 그대로 넣으면 안 됨.
2. **Vec = Vec3 별칭**.
3. **setTarget은 Vec2**(Vec3 deprecated).
4. **target height 비선형·포화**: 값↑→위로, 90 부근 포화, 정중앙 ≈ 125.
5. **FadeTo → Place2D 바인딩**: 이후 카메라 부분세터 무시.
6. **지상 Sky View 카메라 잠금**: setTarget/HPR/takeOffOn 모두 코드 무시 → 하늘 조정은 `Place2D.setLatitude/Longitude`+시간(천정=중앙)으로만.
7. **stop()이 애니메이션 setDateTime 취소** → 즉시 `Anim()` 적용 후 stop.
8. **TimeZone enum**: UTC/Local 없음(436개 도시별) → `UTC_P_00_00_MON`/`DefaultTimeZone`.
9. **PlanetName/InsertTextName 정수 캐스팅** 오프셋 주의.
10. **Anim/Animator** 둘 다 통용.
11. **TraceMode = 장노출**(추적 아님).
12. **천체가 화면 하단**은 정상(establishing shot 프레이밍).

## 5. 만든 결과물
| 종류 | 파일 |
|------|------|
| 검증 에이전트 | `goto_object_agent.py` (카메라·밝기·별자리·성운·시간·텍스트·리셋 tool, TimeZone 버그 수정) |
| 정중앙 스킬 | `skill_center_on.py` |
| 예제 재현·비교 | `my_freefly_solar_orbits.py`, `my_freefly_saturn.py`, `my_face_earth.py` |
| 자연어 연출 데모 | `demo_scenarios.py`, `run_orion.py` |
| 추출기 | `extract_reference.py` |
| 노트 | `docs/00`~`11` (인덱스·검증·비교·스킬·함정·다이제스트) |

## 6. 성공 vs 한계
- ✅ **우주 시점 천체 정중앙/크기 제어**: 스킬로 신뢰성 있게 됨(지구 실측 완성).
- ✅ **연출 요소**(별자리 선/그림, 성운, 자막, 시간, 페이드): 검증·동작.
- ⚠️ **지상 별자리 화면 정중앙**: 이 빌드에선 카메라가 코드로 잠겨 미해결. 물리적으로 위치+시간(천정)으로만 가능하나 정밀 튜닝이 어려움 → FadeTo 기본 프레이밍 수용 권장.

## 7. 한 줄 요약
> "밝기를 켜는 것과 카메라를 그쪽으로 조준하는 것은 별개이고, 조준 방법·단위·바인딩은
> 뷰 모드마다 다르다" — Sky Explorer 코드 제어의 핵심.

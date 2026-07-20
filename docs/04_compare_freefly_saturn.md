# 학습 노트 ④ — 내 구현 vs 정답(FreeFlySaturn.py) 비교

> 과제: 첨부 사진(토성 적도 동기 기준, L78°45'22.8"/B20°/R701950km)처럼 **토성만 보이는**
> 스크립트를 정답 안 보고 직접 작성 → 정답과 비교.
>
> - 내 구현: [`scripts/my_freefly_saturn.py`](../scripts/my_freefly_saturn.py)
> - 정답: `FreeFlySaturn.py` (사용자 제공)

## 핵심: 접근 방식(패러다임)이 다르다

이번 정답은 노트 ①에서 분류했던 **두 카메라 제어 계층** 중 *고수준* 을 택했다.

| | 내 구현 | 정답(FreeFlySaturn.py) |
|--|---------|----------------------|
| 패러다임 | **저수준** — 카메라를 직접 배치 | **고수준** — DB 액션에 위임 |
| 핵심 줄 | `setPositionLBR(Vec3(78.7563,20,701950), Anim(), eqSync)` 등 | `DataManager.database().data(PlanetType,"Saturn").action(FadeTo).trigger()` |
| 코드량 | ~6 단계(좌표/좌표계 명시) | 1줄 트리거 + sleep |
| 좌표 지정 | 사진의 L/B/R을 정확히 재현 | FadeTo가 **자동으로 토성 기본 구도**로 이동 (사진의 그 좌표가 그 기본값) |

```python
# 정답 — 고수준
saturn = DataManager.database().data(Data.Type.PlanetType, "Saturn")
saturn.action(Action.Type.FadeTo).trigger()
sleep(1.0)
AdvancedCamera().setModeFreeFly()

# 내 구현 — 저수준 (핵심부)
eq_sync = saturn.portId(Planet.PlanetPort.EquatorialSynchronous)
observer.setTarget(Vec2(0, 30))
observer.setPositionLBR(Vec3(78.7563, 20.0, 701950), Anim(), eq_sync)
observer.setOrientationSmoothXYZR(Vec4(0,0,0,1), Anim(), eq_sync)
```

## 같은 점
- `smoothReset(False)`로 시작 → `AdvancedCamera().setModeFreeFly()`로 끝, `sleep(1.0)` 후 모드 전환.
- 결과 화면(토성+고리+위성)이 사실상 동일.
- "토성만" 표시는 **별도로 다른 천체를 끄지 않는다** — `smoothReset` 직후의 깨끗한 상태 + 토성으로 줌인된 카메라가 알아서 해결(다른 행성은 천문학적으로 멀어 화면 밖).

## 차이점 분석

| 항목 | 내 구현 | 정답 | 평가 |
|------|---------|------|------|
| 토성 등장 | `Planet(Saturn).setIntensity(1.0)` + 카메라 수동 이동 | `FadeTo` 액션이 등장+이동을 한 번에 | 정답이 훨씬 간결 |
| 좌표계 | `EquatorialSynchronous` 포트 명시 | 액션 내부가 알아서 선택 | - |
| 재현 정확도 | 사진의 정확한 L/B/R 보장 | FadeTo 기본값에 의존(보통 그 값) | 정확 구도가 필요하면 내 쪽 |
| 유지보수 | 좌표/좌표계 직접 관리 필요 | DB가 관리 | 대상만 바꾸면 되는 정답이 유리 |
| 페이드 | `setGlobalIntensity` 수동 | `FadeTo`에 페이드 포함 | 정답이 의미상 깔끔 |

## 결론 / 배운 점

- **정답이 더 좋은 케이스다.** "등록된 천체로 이동"은 `goto_database_object`(=DataManager→data→action(FadeTo)→trigger) **고수준 한 줄**이 정석. 페이드+카메라 이동+적절한 구도 선택을 액션이 캡슐화한다.
- 노트 ①에서 *"`goto_database_object`는 저수준 카메라/밝기 도구의 상위 추상화"* 라 적어둔 것이 이 정답으로 입증됨.
- **내 저수준 방식의 쓸모**: 사진처럼 *정확한 L/B/R/좌표계*를 강제해야 하거나, FadeTo 기본 구도를 커스터마이즈해야 할 때. 실무에선 **FadeTo로 이동 후 필요시 `setPositionLBR`로 미세조정**하는 조합이 베스트(노트 ② SYSTEM_PROMPT 규칙 3과 일치).
- 새로 확인한 API: `Planet.PlanetPort` = {Ecliptic, Equatorial, **EquatorialSynchronous**, Galactic, OrbitalMeanEquinox, EquatorialJ2000, NoonEcliptic, NoonEquatorial}; 토성 고리는 `setRingIntensity`가 따로 없고 **본체 intensity에 포함**(고리 모델은 `setRingModel`로 교체).

> 정리: 이번엔 "정답 = 고수준이 정석", 지난 Sun 과제는 "수동 구도가 필요해 저수준". **상황에 따라 계층을 고르는 감각**이 이번 학습의 핵심.

# 학습 노트 ⑥ — 스킬: 천체를 돔 정중앙에 (goto_center)

> 스크립트: [`scripts/skill_center_on.py`](../scripts/skill_center_on.py)
> Earth 튜닝(노트 ⑤)으로 확정한 "정중앙 공식"을 임의 천체에 재사용하는 스킬.

## 정중앙 공식 (Earth 실측 확정)

| 파라미터 | 값 | 역할 |
|----------|-----|------|
| `B` (카메라 위도) | **90** | 극축 정렬 → 좌우 자동 중앙 |
| `target azimuth` | **0** | 좌우 중앙 |
| `target height` | **125** | 상하 중앙 (⚠️ 90은 포화라 아래로 치우침, 125가 진짜 중앙) |
| `R` (거리) | **1.5** | 반지름 단위 → 화면에 크게 (작을수록 큼) |
| `L` (경도) | 10 | 어느 면을 볼지 (임의) |

- **height/R 은 프레임 기하 기반** → 고체 천체(행성/위성/소행성 등)에 그대로 일반화.
- **R 은 반지름 단위** → 천체 크기에 자동 비례(어떤 행성이든 1.5면 비슷한 화면 크기).
- 배경: `Stars(StarrySky)` + `Galaxy(MilkyWay)` intensity 1.0.
- 마무리: 페이드인 → `AdvancedCamera().setModeFreeFly()`.

## 타입별 좌표계 포트 (공식 문서 확인)

| data_type | 좌표계 port | R 기본 | 비고 |
|-----------|-------------|--------|------|
| Planet / DwarfPlanet / Satellite | `EquatorialSynchronous` | 1.5 | ✅ 검증된 정중앙 |
| Asteroid / Comet | `Synchronous` | 1.5 | 고체 → 동일 공식 |
| IndividualStar (태양) | `Ecliptic` | 0.05 | ⚠️ 거리=AU라 R 튜닝 필요 |
| Galaxy | `Galactic` | 3.0 | ⚠️ 스케일 달라 R 튜닝 필요 |

## 사용법

```python
from skill_center_on import goto_center, goto

goto_center("Planet", "Saturn")        # 토성 정중앙
goto_center("Planet", "Mars", r=2.0)   # 크기 조절(멀리)
goto_center("Planet", "Jupiter", height=130)  # 상하 미세조정
goto("Neptune")                        # 이름만으로(아는 천체 자동 타입)
```

- `r` : 작을수록 큼(고체=반지름 단위). 기본은 타입별 값.
- `height` : 상하 정렬. 위로 더=↑, 아래로=↓ (기본 125).
- `longitude` : 보는 경도(대륙/면 선택).
- `background=False` : 별/은하수 배경 끄기.

## "X로 향해줘" 요청 처리 레시피 (앞으로 이렇게)

1. 대상 이름 → 타입 판별(행성/위성/은하 등).
2. `goto_center(<type>, "<Name>")` 호출하는 짧은 스크립트 생성.
3. 고체 천체면 그대로 정중앙. 태양/은하는 R을 상황에 맞게 튜닝 제시.
4. 결과 보고 크기(`r`)·상하(`height`)만 미세조정.

## 한계 / 메모

- 정중앙(B/az/height)은 **고체 천체에서 검증**. 태양·은하·성운 등은 프레임 단위가
  달라 **R(크기)만 재튜닝** 필요(정렬 로직은 대체로 동일).
- 이름→타입 자동 해석은 자주 쓰는 천체만 등록(`_KNOWN`). 나머지는 타입 명시.
- `Satellite`/`DwarfPlanet` 등의 정확한 이름 enum 값은 해당 클래스 문서 참고
  (`reference/api/`에 추가 추출 가능).

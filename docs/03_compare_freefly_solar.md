# 학습 노트 ③ — 내 구현 vs 정답(FreeFlySun.py) 비교

> 과제: 첨부 사진(태양 황도 기준, L0/B45/R30, Free Fly)의 구도로 태양계 행성 궤도를
> 보여주는 스크립트를 **정답을 보지 않은 셈 치고** 직접 작성 → 정답과 비교.
>
> - 내 구현: [`scripts/my_freefly_solar_orbits.py`](../scripts/my_freefly_solar_orbits.py)
> - 정답: `FreeFlySun.py` (사용자 제공)

## 전체 흐름 — 동일

두 코드 모두 같은 7단계 골격을 따른다. **구도·로직의 큰 그림은 일치**한다.

1. `smoothReset(False)` → 장면 초기화
2. `Universe(MainUniverse).setGlobalIntensity(0.0)` → 암전(페이드 인 준비)
3. 카메라 target / LBR position / orientation 을 태양 황도 좌표계 기준으로 설정
4. 행성 궤도선 + 본체 intensity = 1.0
5. `setGlobalIntensity(1.0, <1초 anim>)` + `sleep(1.0)` → 페이드 인
6. `AdvancedCamera().setModeFreeFly()` → 자유 비행 모드
7. 조작 안내 출력

→ 핵심 파라미터(L=0, B=45, R=30, target 30°, Ecliptic port, 8행성 궤도)까지 정확히 일치했다.

## 줄 단위 차이

| 항목 | 내 구현 | 정답(FreeFlySun.py) | 평가 |
|------|---------|--------------------|------|
| **target 타입** | `setTarget(Vec2(0, 30))` | `setTarget(Vec(0, 30, 0))` | 둘 다 동작. `Vec`=`alias of Vec3`이고 `setTarget(Vec3)`는 **공식 문서상 DEPRECATED**("prefer Vec2"). → **내 쪽이 권장 API** |
| **LBR value 타입** | `setPositionLBR(Vec3(0,45,30), …)` | `setPositionLBR(Vec(0,45,30), …)` | 동일(`Vec`=`Vec3`). 표기만 다름 |
| **anim 객체** | `Anim()` / `Anim.cubic(1.0)` | `Animator()` / `Animator(1)` | 둘 다 실존 클래스. 공식 시그니처의 파라미터 타입은 `Anim`. `Animator`도 호환되어 정답도 정상 동작 |
| **기준 좌표계** | `sun.portId(IndividualStarPort.Ecliptic)` | 동일 | 일치 |
| **orientation** | `setOrientationSmoothXYZR(Vec4(0,0,0,1), Anim(), ecliptic)` | `…(Vec4(0,0,0,1), Animator(), ecliptic)` | 일치(anim 표기만) |
| **행성 순회** | 이름 명시 리스트 `Mercury…Neptune` (8개) | `while i<8: Planet(PlanetName(i))` (i=0..7) | ⭐ 아래 별도 분석 |
| **Universe 핸들** | 변수에 저장해 재사용 | 8번/25번 줄에서 매번 새로 생성 | 내 쪽이 약간 더 깔끔(기능 차이 없음) |

## ⭐ 핵심 차이: 행성 순회 방식

**정답**은 enum을 정수로 캐스팅해 순회한다:
```python
planetIndex = 0
while planetIndex < 8:
    p = Planet(Planet.PlanetName(planetIndex))   # 0,1,...,7
    ...
```
**내 구현**은 이름을 명시한다:
```python
PLANETS = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]
for name in PLANETS:
    p = Planet(name)
```

- 공식 `PlanetName` enum 나열 순서는 `InvalidPlanet, Mercury, Venus, …, Neptune, HD142_b, …`.
- 정답이 8개 행성을 모두 켜려면 **`Mercury`의 정수값이 0**이어야 한다(즉 `InvalidPlanet = -1` 센티넬).
  SkyExplorer 개발팀 예제가 `i<8`로 8회 도는 걸 보면 이 가정이 맞을 가능성이 높다 → 정답도 정상.
- 다만 만약 `InvalidPlanet = 0`이라면 정답은 `InvalidPlanet + Mercury…Uranus`가 되어 **Neptune 누락**.
  → **내 이름 기반 방식은 이 enum 정수값 가정에 의존하지 않아 더 안전·명시적**이다.

## 결론

- **구도·시퀀스·기준계는 정답과 일치** → 추출 보관한 레퍼런스만으로 정답에 준하는 구현 도달.
- 내 구현이 더 나은 점: ① `Vec2` 권장 API 사용(정답은 deprecated `Vec3` 폼) ② 행성 순회를 enum 정수값에 의존하지 않게 명시.
- 정답에서 배운 점: ① `Animator()` 도 anim 인자로 통용 ② `setOrientationSmoothXYZR(Vec4(0,0,0,1), …, track)`로 카메라를 기준 좌표계에 부드럽게 정렬하는 관용 패턴 ③ 짧은 예제에선 enum 정수 순회가 간결.

> 검증 한계: `Anim()`/`Anim.cubic()` 및 enum 정수값(Mercury==0 여부)은 실제 SDK 런타임에서 최종 확인 필요.
> 본 비교는 추출 레퍼런스 + 사진 구도 기준의 정적 분석.

# 학습 노트 ⑧ — 자연어 시나리오 데모

> 스크립트: [`scripts/demo_scenarios.py`](../scripts/demo_scenarios.py)
> 학습한 명령어(별자리/성운·메시에/시간/텍스트/리셋 + 정중앙 스킬)를 실제 연출로 엮은 예제.
> SDK 없으면 mock 으로 호출 순서 출력(오프라인 실행 확인 완료).

## 시나리오 ↔ 사용 명령어

| # | 자연어 요청 | 핵심 명령어 |
|---|-------------|-------------|
| 1 | "오리온자리 선·그림 켜고 M42 강조 후 자막" | `Constellation.setLines/Art/LabelIntensity`, `Messier(M42).setIntensity`, `InsertText` |
| 2 | "2024 크리스마스 밤 9시로 시간 맞추고 별·은하수 켜고 시간 정지" | `DateManager.setDateTime`(tz 수정), `Stars/Galaxy.setIntensity`, `DateManager.stop` |
| 3 | "초기화 후 토성 정중앙에 크게 + 'Saturn' 자막" | 정중앙 공식(B=90/az=0/height=125/R=1.5), `InsertText` |
| 4 | "암전에서 오리온 선·라벨 서서히 + 자막 3초 후 숨김" | `setGlobalIntensity` 페이드, `Constellation`, `show_text`→`hide_text` |

## 설계 포인트

- **자연어 → 시퀀스**: 각 요청을 "초기화 → 밝기/배경 → 대상 연출 → 오버레이 → 모드" 순서로 매핑.
- **검증된 시그니처만 사용**: 노트 ⑦의 수정(예: TimeZone `UTC`→`UTC_P_00_00_MON`)을 그대로 반영.
- **정중앙 스킬 재사용**: 시나리오 3의 `center_on_planet` 이 노트 ⑥ 공식을 그대로 사용.
- **페이드 연출 관용구**: 암전(`setGlobalIntensity(0)`) → 대상 세팅 → `setGlobalIntensity(1, Anim(t))`.
- **자막 슬롯**: `InsertText` 슬롯 번호로 여러 자막 동시/개별 제어(`hide_text(slot)`).

## 시나리오 1 실행에서 얻은 교훈 (오리온 정중앙)

- **지상 Sky View(Place2D 바인딩)에선 `MainCamera.setTarget`/`FadeTo`로 화면 위치를 못 바꿈**
  (a,h 바꿔도 무반응) — Earth 시리즈의 Place2D 바인딩 함정과 동일.
- **밝기만 켜는 것 ≠ 화면에 보이게**: 천체를 보려면 그쪽으로 조준해야 함(자막은 카메라
  전경에 고정이라 시선과 무관하게 남음).
- **정중앙 트릭**: 지상 fisheye 는 *천정(머리 위) 천체가 자동으로 돔 중앙*.
  → 카메라를 돌리지 말고 **관측 위도=천체 적위**, **시각=남중(천정 통과)** 로 맞추면 정중앙.
  위치/시간은 `Place2D.setLatitude/setLongitude`·`DateManager.setDateTime`(바인딩 무관)로 제어.
- **지상 관측의 물리 한계**: 위도 36°N(한국)에선 오리온(적위 ~0°) 최고 고도 ~54° → 천정 불가.
  관측지를 적도 부근(위도 ≈ 적위)으로 옮겨야 천정 통과.
- 실행판: `scripts/run_orion.py` (setTarget/FadeTo 대신 위치+시각 방식).

### ⚠️ 오리온 정중앙 — 미해결 한계 (정직 기록)
여러 방식 모두 지상 Sky View의 벽에 막힘:
- `setTarget`, `setOrientationHPR`, `AdvancedCamera.takeOffOn()` → **코드로 전부 무시**(카메라 잠금).
- 유일하게 작동한 레버 = `Place2D.setLatitude`(남북) + `DateManager.setDateTime`(동서, 천정=중앙).
  단 오리온을 정확히 천정에 올리려면 관측 위도=적위 + 정확한 남중 시각이 필요한데,
  런타임 없이 시각을 정밀히 못 맞춰 반복 실패.
- 결론: **이 빌드의 지상 별자리 뷰는 스크립트로 화면 정중앙을 강제하기 어렵다**(수동 UI 전용).
  실용적으로는 FadeTo 기본 프레이밍(하단-중앙, 오리온 명확히 보임)을 수용하는 게 안정적.
  천체를 '정중앙+크게'는 **우주 시점(행성 등, 정중앙 스킬 ⑥)** 에서만 신뢰성 있게 됨.

## 확장 아이디어

- 별자리 이름을 파라미터화해 "임의 별자리 스토리텔링" 함수로.
- `set_planet_orbit_intensity` + 시간 진행으로 "행성 궤도 운동" 연출.
- 시나리오들을 타임라인(sleep 간격)으로 이어 붙이면 미니 돔쇼가 됨.

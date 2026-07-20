# 학습 노트 ⑦ — 추가 명령어 블록 (별자리/성운/시간/텍스트/리셋) 검증

> 대상: `goto_object_agent.py` 2차 추가 블록. 공식 API 레퍼런스로 하나씩 대조.

## 검증 요약

| 도구 | SDK 호출 | 검증 |
|------|----------|------|
| `set_constellation_lines` | `Constellation.setLinesIntensity(f, Anim)` | ✅ |
| `set_constellation_label` | `Constellation.setLabelIntensity(f, Anim)` | ✅ |
| `set_constellation_art` | `Constellation.setArtIntensity(f, Anim)` | ✅ |
| `set_nebula_intensity` | `Nebula.setIntensity(f, Anim)` | ✅ |
| `set_messier_intensity` | `Messier.setIntensity(f, Anim)` | ✅ |
| `set_simulation_datetime` | `DateManager.setDateTime(y,m,d,h,mi,s,tz,Anim)` | ✅ (tz만 수정) |
| `set_simulation_time_today` | `DateManager.setCurrentDate(h,mi,s,tz,Anim)` | ✅ (tz만 수정) |
| `stop_time` | `DateManager.stop()` | ✅ |
| `show_text` | `InsertText.setText/setPosition/setSize/setColor/setIntensity` + `Camera.addChild(id, CameraPort)` | ✅ (주의 1건) |
| `hide_text` | `InsertText.setIntensity(0, Anim)` | ✅ |
| `scene_reset` | `SceneGraph.reset(int reinitId)` | ✅ |

## ⚠️ 실제 버그 발견: TimeZone enum

원본 스크립트는 `DateManager.TimeZone.UTC` / `DateManager.TimeZone.Local` 을 사용 →
**공식 enum엔 그런 값이 없다**(총 **436개** 구체 시간대). 그대로면 **AttributeError 크래시**.

- 실제 값: `DefaultTimeZone`, 그리고 `UTC_M_12_00_IDL`, `UTC_P_00_00_MON` … 처럼
  부호(M/P)+오프셋+도시코드 형식.
- **수정 매핑(반영 완료)**:
  - `"UTC"`  → `DateManager.TimeZone.UTC_P_00_00_MON` (UTC+0, 연중 DST 없음)
  - `"Local"`→ `DateManager.TimeZone.DefaultTimeZone` (시스템 로컬)
- 코드엔 `_resolve_tz()` 헬퍼로 통일.

## 주의 / 가정

1. **`InsertText.InsertTextName(slot)` 정수 캐스팅**: enum 값은 `InsertText001`..`InsertText046`.
   `InsertTextName(1)` 이 `InsertText001` 이 되는지는 enum 정수 base(0/1) 가정에 의존
   (노트 ③의 `PlanetName(index)` 와 동일한 오프셋 주의). 최대 46 슬롯.
2. **텍스트는 카메라 자식으로 부착**: `Camera.addChild(text.id, Camera.CameraPort.FixedForeground)`.
   `CameraPort` = {FixedBackground, Background, **FixedForeground**, Foreground} ✓.
   즉 텍스트/이미지는 카메라의 전경 레이어에 붙여 화면 고정.
3. **Constellation 은 `setIntensity` 없음**: 반드시 요소별(lines/label/art)로 제어.
   추가 요소: `setLimitsIntensity`(경계), `setArtHybridRatio` 등도 존재.

## 새로 익힌 개념

- **좌표계별 R 단위**에 이어 **시간대 enum이 도시 단위**로 세분(436개) — HUD/문자열 값을
  그대로 넣지 말고 enum 실제 이름 확인 필요(반복되는 함정 패턴).
- **오버레이 레이어 모델**: `Camera.CameraPort` 4종(전/배경 × 고정/비고정)에 자식을 붙여
  텍스트·이미지를 화면에 고정 표시.
- **리셋 2단계**: 부드러운 재시작 `smoothReset()` vs 전체 `SceneGraph().reset(id)`.

# 17. Recording6 해독 — 밤하늘 가이드 투어 SPC판 vs Python (2026-07-07)

> 사용자가 `night_guide_tour_final.py` 를 SPC 로 옮긴 Recording6.SPC 를 원본과 1:1 대조.
> 결과: **쇼 구조 완전 일치** (86줄 = 우리 쇼의 전 장면). 신규 cmd 15종 확정 → `spc_converter.py` 등록.

## 1. 장면별 대응표 (전부 일치)

| 시각 | SPC cmd | 우리 Python | 값 일치 |
|---|---|---|---|
| 00:00 | 4885 gi=0 → 1026/1065/770/514/2050 | 암전 + 지상 체크리스트(지구·대기·태양·별·은하수) | ✅ |
| 00:00 | 5633 (127.49, 36.64, 60) | `place.setPosition(Vec(36.64, 127.49, 60))` | ✅ ⚠️순서 반전(아래) |
| 00:00 | 257 mode2 JD → 257 mode1 (2026 1 15 14 0 0) | `dm.stop()` → `setDateTime(...14 UT)` | ✅ |
| 00:01 | 307 TH=30 → 290 H=0 | 관람 표준 30 + 남쪽 조준 | ✅ |
| 00:02 | 4881 부착, 3845/3843/3846/3842, 3844 자막, 4885 cubic 페이드인 | addChild + 자막 4종 세팅 + 오프닝 | ✅ |
| 00:09 | **513×1 + 517=1.2** … **513 + 517=0.4** | 반짝임 3.0 → 원본(1.0) 복귀 | ⚠️ 값 튜닝됨 |
| 00:19~20 | 4885 dip → 307 TH=0 → 4885 in | 암전 속 Target 0 전환 | ✅ |
| 00:22 | **5637 v0.9 layer2** + **5637 v0.9 layer10** | 방위그리드 + 방위표지 | ✅ |
| 00:32 | **1097 v0.9** | 지구 적도 그리드 | ✅ |
| 00:39 | **5644 v0.9** | 시간각 그리드 | ✅ |
| 00:47~49 | dip → 307 TH=30 → in | Target 30 복귀 | ✅ |
| 00:51 | **8196 type=2, 8195 색, 8197 크기5, 8194 (0,30)** | 포인터 등장 (az0, h30) | ✅ |
| 00:53 | 8194 (0,85) cubic 3s | h85 상승 | ✅ |
| 00:56~64 | 8194 az 0→360 step30 ×13 (0.55s) | 서클링 12스텝 | ✅ |
| 01:05 | **1537=0.8, 1553=0.6** | 오리온 선/라벨 | ✅ |
| 01:08 | **1545=0.9** → 0 | 아트 페이드인/아웃 | ✅ |
| 01:19 | **530=1** → **526=50000 (20s)** → 526=0 (6s) → 530=0 | 고유운동 +5만 년/20초 → 복귀 | ✅ |
| 01:48 | 1537/1553=0, 자막 '끝', 4885=0 cubic 4s | 피날레 | ✅ |

## 2. 차이점 (전부 의미 있는 발견)

1. **반짝임 값이 튜닝됨**: 스크립트 3.0→1.0 이 SPC 에선 **증폭 1.2 / 복귀 0.4**.
   → 운영 감각: 3.0 은 과했고 1.2 정도가 적정, 기본 하늘도 0.4 로 차분하게. 이후 쇼에 반영 권장.
2. **SceneGraph.reset 없음**: SPC 는 리셋 없이 바로 시작 — SPC 재생 환경은 초기 상태 전제.
3. **Place2D.setPosition 의 SPC 컬럼 순서 = (경도, 위도, 고도)** — Python Vec(위도,경도,고도)와
   x/y 스왑. 컨버터 spec 을 ["G","R","B"] 로 수정 완료 (양방향 정합).
4. **DefaultTimeZone 의 SPC 코드 = 0** (기존 probe 의 32 는 특정 지역존이었음).
5. **✨ value_anim 페이로드 첫 상수의 정체 = 보간 코드**: 1=Linear, 2=Cubic.
   (gi 페이드인 Anim.cubic → 2, 포인터 cubic 상승 → 2 실측. 기존 '상수 1' 가정 정정!)
6. **미확정 1건**: Stars cmd **513** (head[1,3], pay[1,0]) — Studio 가 반짝임 편집 때마다 동반 발행.
   기능 미상 (isTwinkling 토글? 후속 프로브 후보).

## 3. 신규 확정 cmd (converter 등록 완료)

| cmd | 클래스.메서드 | 비고 |
|---|---|---|
| 3846 | InsertText.setDistance | 표준 value_anim |
| 517 / 526 / 530 | Stars.setTwinklingAmplitude / setProperMotionOffsetInYears / setProperMotion | 517 만 꼬리 0, 530 은 bool |
| 1545 / 1553 | Constellation.setArtIntensity / setLabelIntensity | 1537(lines)과 한 세트 |
| 5637 L2 / 5637 L10 / 5644 | Place2D 방위그리드 / 방위표지 / 시간각그리드 | 레이어 인덱스 방식(일식 1128 패턴) |
| 1097 | Planet.setEquatorialGridIntensity | head[3,7] |
| 8193~8197 | DomePointer intensity/position/color/type/apparentSize | **family 0x11 확정**. position=(az,h)+상수1 |
| — | 4881 = 범용 부착(addChild/setParent 겸용), 257 mode2 = DateManager.stop | 중복 cmdId 라 주석 등록 |

## 4. 포인터로 '개체'를 직접 지정하기 (사용자 질문 답)

DomePointer 는 **화면(돔) 좌표 전용** — 개체 추적 기능이 없다. 개체 직결 포인터는 별도 2경로:

1. **천체 내장 포인터**: `IndividualStar/Planet/Satellite/Nebula/Galaxy/Comet/Asteroid/GlobularCluster`
   전부 `setPointerIntensity(i, Anim)` + `setPointerType(Body.PointerType.…)` 보유 —
   켜면 엔진이 그 천체 위치에 포인터를 그려주고 **천체가 움직여도 따라감**.
   ```python
   star = IndividualStar(IndividualStar.IndividualStarName.Betelgeuse)  # 멤버명은 dir() 확인
   star.setPointerType(Body.PointerType.Model1Bold)
   star.setPointerIntensity(1.0, Anim(1.0))
   ```
2. **DB 액션 경로** (enum 에 없는 천체도 가능): `Action.Type.PointerOn / PointerOff`
   ```python
   d = DataManager.database().data(Data.Type.StarType, "Betelgeuse")
   a = d.action(Action.Type.PointerOn)
   if a is not None: a.trigger()
   ```
⚠️ **Constellation 은 내장 포인터가 없음** — 별자리는 대표 별(베텔게우스 등)을 포인팅하거나
DomePointer 로 서클링. Messier 도 포인터 API 없음(M42 PointerOn 미지원 실측) → 성운은 Nebula 경유.

**v1/v2 실측 확정 (2026-07-07)**: 베텔게우스 ①/② 모두 성공, 목성은 **setPointerType 지정 전 PointerOn
무표시(A) → Model1Bold 지정 후 표시(B)** — 행성 기본 pointerType 은 무효라 타입 지정 필수.
별은 기본 타입이 있어 타입 없이도 표시(리겔 C). IndividualStarName enum = 3,189개(오리온 7별 포함).
검증: `scripts/study/pointer_object_test.py` + `_v2.py`

# 18. Recording7 해독 — 쌍둥이자리 유성우 SPC판 (2026-07-07)

> `geminid_night.py` 를 SPC 로 옮긴 Recording7.SPC 대조. **쇼는 정상 작동, 명령 전부 스크립트대로 발행.**
> "애매하게" 느낀 이유 = **값 세팅이 시각적으로 약했던 것** (아래 2대 발견).

## 1. ★★ 핵심 발견 2가지

### ① ZHR 내부 저장 = '분당' (ZHR ÷ 60) — 유성우가 성긴 이유
`setZenithalHourlyRate` 의 SPC 기록값 = **ZHR/60** (실측 4건 전부 ÷60 일치):

| Python ZHR | SPC 값 | 뜻 |
|---|---|---|
| 120 | 2 | 분당 2개 |
| 300 | 5 | 분당 5개 |
| 3000 | 50 | 분당 50개 |
| 60 | 1 | 분당 1개 |

→ **ZHR 120 = 분당 2개 = 30초에 1개.** 12초 장면에선 0~1개밖에 안 보임 → "애매함"의 정체.
실제 유성우가 원래 성기지만, **돔 쇼로 볼만하려면 ZHR 를 훨씬 크게** 써야 함:
- 은은한 배경: ZHR 600~1200 (분당 10~20개)
- 활발한 유성우: ZHR 1800~3000 (분당 30~50개, 폭풍 느낌)
- 우리 스토리의 '폭풍(3000)' 만 시각적으로 확실했던 이유가 이것.

### ② Bolide 화구가 '거의 안 움직인' 이유 = 148초 크로싱
`bo.set(az,h,alt_m…, speed=1.0)` → `play(1.0)` 시 내부 `setEvolution` 애니 **dur=148.3초**(실측)!
- `set()` 은 복합 명령: 우리 (방위,고도,고도m) 를 **지리좌표(경도,위도,고도)로 자동 변환** —
  시작 (128.71°E, 36.66°N, 99,880m) / 끝 (127.49°E, 36.65°N, 62m) 로 기록됨(청주 상공 실제 궤적!).
- `play(speed)` 의 크로싱 시간 = 경로길이/speed. speed=1.0 이면 148초 → 6초 슬립 동안 4%만 이동.
- ⚠️ **빠른 화구 = speed 를 크게(≈40~60)**. 실제 화구는 수 초 내 소멸.

## 2. 장면별 대응 (전부 일치)

| 시각 | SPC cmd | Python | 비고 |
|---|---|---|---|
| 00:00 | 307 TH=30, 290 H=105 | 복사점 조준(방위 75) | ✅ |
| 00:01 | 3845/3843/3846/3842/3844/3841 | 자막 세팅+오프닝 | ✅ |
| 00:06 | 1537/1553 (body 0x0A Gem), 807 type + 805 int (body 0x0B Castor) | 쌍둥이 선/라벨 + 카스토르 포인터 | ✅ |
| 00:12 | 2561 rep, 2565 bright, 2567 trail → 2562/2563/2564 ×3 | 단발 유성 3발 | ✅ |
| 00:21 | 2569 (0,60), 2570=15, 2571=1, 2573=**2**, 2566 seed=1 | 유성우 3a (ZHR 120=분당2) | ✅ |
| 00:33 | 2574 ref, 2569 (113,32), 2573=**5** | RaDec 복사점 (ZHR 300) | ✅ |
| 00:47 | 14081 int, 14084/14085/14087(set 복합), 14082 dur=148 | 화구 | ✅ |
| 00:53 | 2573=**50** (ZHR 3000) → =1 (ZHR 60) → 2566 seed=0 | 폭풍→고요→정지 | ✅ |
| 01:10 | 1537/1553/805=0, 자막 끝, 4885=0 | 피날레 | ✅ |
| (t=0) | 257 mode1 (2026 12 14 14 UT) | setDateTime | ✅ |

## 3. 신규 확정 cmd (converter 등록 완료)

| cmd | 클래스.메서드 | 비고 |
|---|---|---|
| 805 / 807 | IndividualStar.setPointerIntensity / setPointerType | 별 포인터 (770 intensity 근처) |
| 2561 | ShootingStar.setRepresentationType | enum(Model) |
| 2562 / 2563 | setStartPosition / setArrivalPosition | Vec2(az,h) — DomePointer 화면좌표 규약 |
| 2564 | setAdvancing | 0→1 = 단발 유성 비행 |
| 2565 / 2567 | setBrightness / setTrailLength | |
| 2566 | setRainSeed | int, 0=정지·그외=생성 |
| 2569 | setRainGradientPoint | Vec2 (기본=화면az,h / RaDec 모드=적경,적위) |
| 2570 / 2571 | setRainChaosGradientPoint / setRainSpeed | 복사점 반경° / 속도 |
| **2573** | setZenithalHourlyRate | **★ 저장값 = ZHR/60 (분당)** |
| 2574 | setReferential | enum, RaDec=1 |
| 14081 | Bolide.setIntensity | |
| 14082/14084/14085/14087 | Bolide setEvolution/setStartPosition/setEndPosition/(경로길이) | set()/play() 복합, family 0x2E |

## 4. 개선 권고 (geminid_night v2 용)
- 유성우 ZHR: 3a 120→**800**, 3b 300→**1500**, 폭풍 3000 유지.
- 단발 유성(setAdvancing)은 12초 안에 3발 = 잘 보였을 것(성긴 유성우와 대비되는 '연출된' 유성).

## 5. 화구를 '별똥별' 아닌 '불덩이'로 (2026-07-09 실측, bolide_fireball_test)
사용자 리포트: "화구가 유성우랑 똑같이 날아갔다" → 원인 규명 + 시그니처 3버그 확정.
- **enum 실측**: `ModelID` = Chelyabinsk / ColoredFireball / User ·
  `Element` = Sodium(주황) / Magnesium(청록) / Iron(노랑) / Calcium(보라) / NitrogenOxygen(적색) / Custom.
- **화구다움 = 모델+색**: ⚠️ **모델 없으면 아예 안 그려짐(실측)** — 확정 정답 =
  `setModel(ModelID.ColoredFireball, "")` + `setElement(Element.Sodium, Vec3(0,0,0), Anim())`.
  실측 결과: A(모델 없음)=✗ 안 보임 / **B(ColoredFireball+Sodium)=✓ "진짜 운석 떨어지듯이"** /
  C(Chelyabinsk)=✗ 안 보임(에셋 파일 필요 추정, 이 빌드선 렌더 실패 — 쓰지 말 것).
- **시그니처 3버그(실측 에러)**:
  ① `setModel(model, filename)` — filename 필수(내장도 `""`). 없으면 ArgumentError → 모델 미적용.
  ② `setElement(element, customColor, anim)` — 3인자 전부 필수(문서 optional 무시). 1인자 호출=실패.
  ③ **`set()` 의 speed 를 1.0 외 값(20)으로 주면 화구가 아예 안 보임** — set speed 1.0 고정,
     재생 속도는 play() 로만. (v2 가 set 1.0/play 50 이라 보였고, 테스트가 set 20 이라 사라진 것.)
- **속도감**: 크로싱 = 148/play_speed 초. 극적 불덩이 play(12~18)≈8~12초 / 빠른 유성풍 play(40~60).

# 학습 노트 ⑮ — SPC 라인 포맷 역설계 & Python→SPC 변환기

> 녹화 샘플: `test_A_satellite.py`→`a.SPC`, `test_C_mark.py`→`c.SPC` 로 역설계.
> 변환기: [`scripts/spc_convert/spc_converter.py`](../scripts/spc_convert/spc_converter.py)
> 회귀검증: [`scripts/spc_convert/verify.py`](../scripts/spc_convert/verify.py) (샘플 재현 ✅)

## ⚠️ SPC 는 '스크립트(악보)'일 뿐 — 쇼는 폴더 패키지

`.SPC` = 텍스트 명령 타임라인 **하나**. 실제 '쇼/미니씬'은 **여러 파일이 든 폴더**이고 .SPC 는 그 일부.
.SPC 는 에셋을 품지 않고 **경로로 참조만** 함:
- `129`(Macro) → 외부 서브스크립트(`common_off.SPC` 등)
- `6146`/Insert3D → 외부 3D 모델(`modelHH111-animated.osg`)
- `Insert2D.setTexture(경로)` → 외부 이미지/텍스처

```
쇼 폴더/  ├─ scene.SPC(스크립트) ├─ *.SPC(매크로) ├─ *.osg(모델) ├─ textures/(이미지) …
```
→ **결론: SPC↔Python 변환은 '스크립트'만 옮김. 참조된 에셋(모델·이미지·매크로)은 별도 파일이라
  우리가 없으면 재현 불가.** 프로덕션 쇼 100% 클론이 안 되는 이유가 이것(카메라·명령 흐름은 재현됨).

## SPC 라인 포맷 (TAB 구분, 67컬럼 고정)

```
[0]  E                     이벤트 표시(첫 줄엔 BOM ﻿ 선행)
[1]  HH-MM-SS-FF           타임코드(녹화 시점 — 런타임 값)
[2]  101                   상수(SkyEx 명령 카테고리로 추정)
[3]  cmdId                 SPC 명령 ID  ← (클래스,메서드)로 결정
[4..]                      헤더 필드(인자 타입에 따라 2~3개)
     bodyId                대상 천체 id = (family<<24)|(index+1)
     값들                  인자 페이로드
     0 …                   고정폭까지 0 패딩
[66] "……(공백 30칸)"       꼬리
```

## 확정된 매핑 (녹화 14건)

| cmdId | 클래스.메서드 | 헤더 | bodyId | 페이로드 | Python |
|-------|---------------|------|--------|---------|--------|
| 1394 | Satellite.setTerrainModel | `1 2` | ○ | `[모델idx]` | `setTerrainModel(TerrainModel(7))` → `7` |
| 1282 | Satellite.setIntensity | `3 6 <dur>` | ○ | `[1, v, 1]` | `setIntensity(0.3, Anim(2.5))` → head `3 6 2.5` / pay `1 0.3 1` |
| 4356 | Mark.setIntensity | `3 6 <dur>` | ○ | `[1, v, 1]` | 위와 동일 레이아웃 |
| 4357 | Mark.setColor | `3 9 0` | ○ | `[r,g,b, 1,1]` | `setColor(Vec(1,1,1))` → `1 1 1 1 1` |
| 5634 | Place2D.setLongitude | `3 6 <dur>` | ○ | `[1, 1, v]` | `setLongitude(12.5)` → pay `1 1 12.5` (값이 **끝**) |
| 5635 | Place2D.setLatitude | `3 6 <dur>` | ○ | `[1, 1, v]` | `setLatitude(48.25)` |
| 5636 | Place2D.setAltitude | `3 6 <dur>` | ○ | `[1, 1, v]` | `setAltitude(789)` |
| 257 | DateManager.setDateTime | `3 12 <dur>` | **✗(전역)** | `[1,1,1, y,mo,d,h,mi,s, 0,0,tz]` | `setDateTime(2021,3,14,15,9,26, tz, Anim(4))` → `…4 1 1 1 2021 3 14 15 9 26 0 0 32` |
| 1026 | Planet.setIntensity | `3 6 <dur>` | ○ | `[1, v, 1]` | `setIntensity(0.11, Anim(1.5))` (Earth=PlanetName(2)→bodyId 0x12000003) |
| 1064 | Planet.setCloudsIntensity | `3 6 <dur>` | ○ | `[1, v, 1]` | `setCloudsIntensity(0.22, Anim(2.5))` |
| 1065 | Planet.setAtmosphereIntensity | `3 6 <dur>` | ○ | `[1, v, 0]` | `setAtmosphereIntensity(0.33, …)` (끝 상수 **0**) |
| 1030 | Planet.setOrbitIntensity | `3 6 <dur>` | ○ | `[1, v, 1]` | `setOrbitIntensity(0.44, …)` |
| 1059 | Planet.setElevationScale | `3 6 <dur>` | ○ | `[1, v, 1]` | `setElevationScale(0.55, …)` |
| 1186 | Planet.setRingModel | `1 2` | ○ | `[idx]` | `setRingModel(RingModel(3))` — enum, **animDur 없음** |

> 🔑 **probe_01 (p1.SPC)**: `setIntensity(0.3, Anim(2.5))` = `[3, 6, 2.5, bodyId, 1, 0.3, 1]` →
> **animDuration 은 헤더 3번째 슬롯**, **값은 페이로드**. 구 v0.1 가정 `[v, animDur, 1]` 은
> 샘플이 전부 1.0 이라 겹쳐 안 보였던 착각.
>
> 🔑 **probe_02 (p2.SPC) — 날짜 257**: **전역 명령(bodyId 없음)** 확정. y·m·d·h·mi·s 6필드가
> 순서대로, `animDur` 은 또 헤더 3번째, tz 는 정수 `32`(멤버 매핑 미확정, 관측 상수). fieldCount=12=페이로드 길이.
>
> 🔑 **probe_03 (p3.SPC) — Place2D**: **family = 0x1A 확정**(`436207618=0x1A000002`). lon/lat/alt 는
> **별도 cmd 5634/5635/5636**(결합 아님) → 프로덕션 `5633` 은 **다른 명령**(위치 결합 추정, 미확정).
> 페이로드가 `[1, 1, v]`(값이 **끝**)라 intensity `[1, v, 1]`(값 가운데)와 달라 → **레이아웃은 명령별**.
>
> 🔑 **probe_05 (p5.SPC) — Planet**: **family = 0x12 확정**(`301989891=0x12000003`, Earth=PlanetName(2)).
> intensity류 4종=`[1,v,1]`, **atmosphere(1065)만 끝 상수 `0`**, **RingModel(1186)=enum(`1 2`, animDur 미인코딩)**.
> ⚠️ **구 디스어셈블 추정 오류 정정**: `1062≠clouds`(clouds=**1064**), `1065≠ring`(=atmosphere), ring=**1186**.
> → 교훈: 디스어셈블 추정보다 **단일메서드·값차이 직접 프로브가 진실**.

- **cmdId는 (클래스, 메서드) 쌍으로 결정** (같은 setIntensity라도 Satellite=1282, Mark=4356, Planet=1026).
- **argType(col4)=3 이면 헤더 3번째 = animDur** (없으면 0). **enum 세터(TerrainModel/RingModel)는 animDur 미인코딩**. **전역 명령은 bodyId 생략**.
- **bodyId**: `(family<<24)|(index+1)`. family: **Satellite=0x15, Mark=0x03, Place2D=0x1A, Planet=0x12**.
  (예: `SatelliteName(1)` → `0x15000002`, `Place2DName(1)` → `0x1A000002` = 436207618.)
- ⚠️ 사용자 추정치와 실제가 달랐음: setTerrainModel 1281→**1394**, setIntensity 1311→**1282**.

## 양방향 변환기

- **Python → SPC**: [`spc_converter.py`](../scripts/spc_convert/spc_converter.py)
- **SPC → Python**: [`spc_to_python.py`](../scripts/spc_convert/spc_to_python.py)
  (동일 매핑 `CMD`/`FAMILY` 재사용 → 단일 소스). `cmdId→(클래스,메서드)`,
  `bodyId→(family,index)`, 값 슬롯→Python 인자 복원.
- **왕복 검증**: `verify.py` — `Py→SPC` 와 `SPC→Py→SPC` 모두 녹화본과 일치(ALL PASS ✅).
  (복원 Python 은 변수명만 `satellite1`/`mark1` 로 생성, 호출은 원본과 동일.)

## 변환기 구조 (`spc_converter.py`)

1. **Python AST 파싱**: `var = Class(ClassName(idx))` → 변수↔(클래스,index),
   `var.method(args)` / `Class(...).method(args)` → 이벤트.
2. 인자 파싱: 숫자 / `Anim(d)` / `Vec(r,g,b)` / `Enum(idx)` 구분.
3. `(클래스,메서드)` → `CMD` 테이블에서 cmdId·헤더·인코더 조회 → 값 슬롯 생성.
4. `[E,타임코드,101,cmdId]+헤더+[bodyId]+값 + 0패딩(66) + 꼬리` 로 라인 조립.

## TimeZone 코드표 (probe_04 로 역설계)

- 문제: `setDateTime` 의 tz 는 SPC 에 **정수코드**로만 남음(예 `32`). `dir()` 알파벳 순서 ≠
  enum 정수값(엔진 내부는 **UTC 오프셋 순** −12→+). → 매핑 없이는 복원 불가.
- 방법: tz 멤버마다 `second` 슬롯에 태그(0,1,2…)를 넣어 녹화 → `.SPC(second↔tz코드)` +
  콘솔 로그(`TAG↔이름`)를 조인. 생성기: [`gen_tz_table.py`](../scripts/spc_convert/gen_tz_table.py)
  → [`tz_table.py`](../scripts/spc_convert/tz_table.py)(`TZ_CODE2NAME`/`TZ_NAME2CODE`).
- **실제 시간대 값 102개 전부 확정**(코드 −1~100, probe_04 60개 + probe_04b 42개 누적).
  `dir(TimeZone)` 총 116개 중 나머지 14개는 시간대 값이 아니라 **메서드**(소문자, 알파벳순 뒤쪽 →
  probe_04b tag42 에서 `method_descriptor` ArgumentError). 예: `DefaultTimeZone=0, InvalidTimeZone=-1,
  UTC_M_12_00_IDL=1 …(서→동)… UTC_P_13_00_SAM=100`.
- 변환기 연동: 정방향은 `DateManager.TimeZone.<이름>` → 코드, 역방향은 코드 → `.<이름>`
  (미매핑 코드는 `DateManager.TimeZone(<int>)` 로 폴백). `verify.py` p4(날짜×60) 왕복 PASS.

## 아직 불확실 (추가 녹화로 검증 필요)

- ~~**값 인코딩**~~ ✅ **확정**(probe_01): animDur=헤더 3번째, 값=페이로드(레이아웃은 명령별).
  아직 추정: 페이로드 앞뒤 상수 `1`(뒤=보간코드로 추정), 색 trailing `1 1`, 날짜 페이로드 `sec` 뒤 `0 0`.
- ~~**TimeZone 매핑**~~ ✅ **완료**(probe_04+04b): 실제 시간대 값 **102개 전부**(코드 −1~100). 나머지 dir 항목은 메서드.
- **프로덕션 5633**: `5634=setLongitude` 로 확정됐으니 `5633`(≠5634)은 별개 명령(위치 결합? 다른 포트?) — 미확정.
- **family 코드**: Satellite/Mark/**Place2D(0x1A)** 확정. Planet·Camera·Constellation·`0x0B`/`0x0C` 미확정.
- **index→instance**: `index+1` 이 규칙인지 미확정(`Name(0)` vs `Name(1)` 녹화로 구분).
- **헤더 필드 의미**(argType/fieldCount): 명령별 상수로 템플릿화만 함(의미 해석 보류).

## 범용 디코더 (`spc_decode.py`) — 매핑 없이도 구조 해독

실제 프로덕션 SPC(`samples/scenario/`)는 명령이 ~20종이라 v0.1 변환기론 부족.
→ **디스어셈블러**로 모든 라인을 구조화: `타입 타임코드 cat cmd | obj=family#idx | val=[…] | str="…"`.
실행: `python spc_decode.py file.SPC` (결과: `samples/scenario/DISASSEMBLY.txt`).

### 커버리지 측정 (scenario_v2 5종 = 실제 쇼 파일)

실행 매핑으로 `samples/scenario_v2/` 재변환 결과: **SkyEx 명령 27줄 중 23줄(85%) 변환 가능**
(probe_09 대기/광공해 + probe_11 family 발견 추가). 남은 4줄 = 771(IndividualStar?)·1062(Planet#0)·
1283(Satellite?)·1025(init). (디스어셈블: `scenario_v2/DISASSEMBLY.txt`)

**"Light ON" 정체(probe_11)**: **태양(IndividualStar=family 0x0B, setIntensity=770)** + **별(Stars=0x0C, 514)**.
그 외 family 확정: Galaxy 0x06, Constellation 0x0A, Nebula/Messier 0x02, Insert2D 0x01, SkySurvey 0x2D.
**검은하늘 명령(probe_09)**: `1057=Planet.setLightPollutionIntensity`(0=밤/20=낮). scattering=1061, halo=1206,
cloudLightPollution=1182, refraction=1204. 전부 표준 intensity 레이아웃 `[3,6,dur]+[1,v,1]`.

**관측자 바인딩(probe_10)**: `Place2D.setParent(4881)` = body(child Place2D) + payload[parent, parent].
Python `place.setParent(earth.portId(port))` 의 `earth.portId(...)` 는 부모 객체 bodyId 로 해석(양방향).
같은 규칙으로 카메라 track 의 `place.portId(...)` 도 bodyId 로 왕복 → scene 완전 왕복.

**Camera(시점) 구조**(probe_06): 전역(카메라 bodyId 없음). track(대상 천체)을 payload 에 `TRK` 로
2회 임베드. `track=-1`(현재유지)은 녹화 시 실제 부착 객체 bodyId 로 치환 → 역변환은 그 int 로 복원.
setPositionLBR=273, setPositionR=276, setOrientationHPR=289, setZoomFov=316.

### 실제 파일에서 밝혀진 것 (scenario 5종 디스어셈블 결과)

| cmdId | 대상 | 값 패턴 | 해석(신뢰도) |
|-------|------|---------|--------------|
| 128 | — | str | 주석/라벨 (확정) |
| 129 | — | str(경로) | Macro include (확정) |
| **257** | — | y,m,d,h,mi[,s] | **DateManager.setDateTime** (강) — 예 `2010,6,16,23,40` |
| **5633** | Place2D | 1,1,lat,lon,alt | **setPosition(Vec3)** — 프로덕션 확정. 단일 5634/5635/5636 의 결합형(`31,31,1000`=나일) |
| **273** | Camera | 1,TRK,TRK,18,1,L,B,R | **setPositionLBR** (probe_06) — TRK=track 천체 bodyId ×2 |
| **274/275/276** | Camera | 1,TRK,TRK,18,1,V | **setPositionL / setPositionB / setPositionR** (probe_06/07; 274=프로덕션) |
| **289** | Camera | 1,0,0,33,1,H,P,R | **setOrientationHPR** (probe_06, track 없음) |
| **290/291** | Camera | 1,0,0,33,1,V | **setOrientationH / setOrientationP** (probe_07) |
| **306/307** | Camera | 1,1,V | **setTargetAzimuth / setTargetHeight** (probe_07) |
| **305** | Camera | 1,1,az,h,roll | **setTarget** (probe_08 확정, Vec3 우회) — Vec2 는 studio 와 타입충돌, `Vec`(=Vec3) 로 |
| **316** | Camera | 1,fov,1 | **setZoomFov** (probe_06) |
| **4881** | Place2D+Planet×2 | body=child, [parent,parent] | **Place2D.setParent** (probe_10 확정) — 관측지→지구 부착. arg=parent.portId |
| **1184** | Planet | 9 | **setTerrainModel** — "Earth Terrain" 라벨+enum([1,2]) 확정 |
| 1062 | Planet | 0.1/0.8 | ⚠️ 구'setCloudsIntensity' 추정 **오류** — probe_05 상 clouds=**1064**. 1062 정체 재확인 필요 |
| **1064** | Planet | — | **setCloudsIntensity** (probe_05 확정) |
| 1057 | Planet | 20 | ?(재확인) (약) |
| **1065** | Planet | — | **setAtmosphereIntensity** (probe_05 확정; 구 ring 추정 오류) |
| **1026** | Planet | — | **setIntensity** (probe_05 확정) / 1030=Orbit,1059=Elev,1186=Ring |
| **1282** | Satellite | 1 | **setIntensity** (확정) |
| 1283 | Satellite | 4 | Satellite.? (약) |
| 770/771 | fam0x0B | | ? (미확정 클래스) |
| 514 | fam0x0C | | ? (미확정 클래스) |

### 추가 확정 사실
- **family**: `0x12=Planet`, `0x15=Satellite`, `0x03=Mark`. 미확정: `0x1A`(관측자/Place로 추정),
  `0x0B`, `0x0C`.
- ⚠️ **헤더는 고정 아님**: cmd 뒤 `[argType, fieldCount, animDuration]` 구조 —
  3번째 값이 **애니메이션 duration**(예 `60/30/15/1`). v0.1 이 `[3,6,1]`로 하드코딩한 건
  샘플이 마침 그 값이라 맞았을 뿐 → 일반화하려면 헤더를 `[argType, fieldCount, dur]`로
  동적 생성해야 함(다음 버전 과제).
- `cat`(col2): `101`=SkyEx 명령, `0`=주석, `600`=Macro. `type`(col0): `E`/`C`.

## 다음 단계 제안

- 값을 바꾼 재녹화(예: `setIntensity(0.3, Anim(2.5))`) → 값 인코딩 규칙 확정.
- 클래스별 1건씩 녹화 → `FAMILY`·`CMD` 테이블 확장.
- 확장은 `spc_converter.py` 의 `FAMILY`/`CMD` 딕셔너리에 줄 추가로 끝(데이터 주도 설계).

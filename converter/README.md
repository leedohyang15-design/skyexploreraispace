# Python ↔ SPC 변환기

Sky Explorer 의 Python 스크립트와 Editor SPC 시퀀스를 상호 변환. 매핑은 실행·녹화로
역설계(자세한 포맷/매핑: [`docs/15_spc_format_and_converter.md`](../../docs/15_spc_format_and_converter.md)).

## 도구 3종

| 파일 | 방향 | 실행 |
|------|------|------|
| `spc_converter.py` | Python → SPC | `python spc_converter.py in.py [out.SPC]` |
| `spc_to_python.py` | SPC → Python | `python spc_to_python.py in.SPC [out.py]` |
| `spc_to_js.py` | SPC → JavaScript (v0.1 POC) | `python spc_to_js.py in.SPC [out.js]` |
| `spc_decode.py` | SPC → 구조 해독(디스어셈블) | `python spc_decode.py in.SPC [more.SPC ...]` |
| `verify.py` | 회귀 검증 | `python verify.py` |

> **JS 변환(v0.1 POC)**: `parse_spc()`(언어중립 이벤트)를 재사용해 JS 문법으로 렌더. 구조는 완성.
> ⚠️ 이 빌드 JS 실물 예제가 없어 `new` 사용 여부·슬롯 enum 표기만 Studio JS 런타임서 1회 확인하면 확정.

- `spc_converter.py` / `spc_to_python.py` 는 매핑(`CMD`/`FAMILY`)이 있는 명령만 정확 변환.
- `spc_decode.py` 는 **매핑이 없어도** 모든 SPC 라인을 `타입/타임코드/cmd/객체/값/문자열` 로 해독
  → 새 명령 매핑을 채우는 재료(프로덕션 SPC 이해용).

## 매핑 확장 방법

새 명령을 녹화해 cmdId 를 알아내면 `spc_converter.py` 의 두 딕셔너리에 줄 추가:
```python
FAMILY = { "Satellite": 0x15, "Mark": 0x03, "Planet": 0x12, ... }
CMD = { ("Planet","setCloudsIntensity"): dict(cmd=1062, head=[3,4,0], enc=..., nval=...), ... }
```
`spc_to_python.py` 는 같은 매핑을 import 하므로 역방향도 자동 반영.

## 샘플
- `samples/` : 단일 명령 픽스처(test_A→a.SPC, test_C→c.SPC) + 회귀 기준.
- `samples/scenario/` : 실제 프로덕션 쇼 SPC 5종 + `DISASSEMBLY.txt`(디코더 출력).

## v0.3 (2026-07-22) 최신화
- **두 사본 통합**: `converter/` 와 `scripts/spc_convert/` 의 `spc_converter.py` 동일화(옛 분기 해소).
- **매핑 209개 / family 27개** (157→209, 20→27). 신규 family: Clock(0x2B)/Chart2D(0x24)/DrawableInsert(0x26)/
  Ephemeris(0x2A)/OrbitalPlace(0x25)/Lut(0x18)/Line(0x20).
- **Oumuamua SPC 완전 변환**(미매핑 0): Asteroid 궤도표시(6414) + 결합 궤도요소(6405, 케플러8)→개별 setter 전개 + Insert3D 3D모델.
- **JS 에미터(spc_to_js.py)** 추가. 회귀(verify.py) ALL PASS 유지.
- ⚠️ 신규 매핑 중 value_anim/color/enum 은 지배적 레이아웃 패턴 기반(개별 녹화 회귀검증은 TODO — 값 오독 시 head 슬롯 조정).

## 현재 상태 / 한계 (v0.2)
- 확정 매핑(녹화 8건): `Satellite.setIntensity`(1282)/`setTerrainModel`(1394),
  `Mark.setIntensity`(4356)/`setColor`(4357), `Place2D.setLongitude/Latitude/Altitude`(5634/5635/5636),
  `DateManager.setDateTime`(257, 전역). family: Satellite=0x15, Mark=0x03, **Place2D=0x1A**.
- ✅ 값/Anim 인코딩 확정(probe_01): animDur=헤더 3번째 슬롯("DUR"), 값=페이로드(레이아웃은 명령별).
- ✅ 전역 명령(probe_02): bodyId 없는 명령 지원(DateManager). 위치인자 `A0..An` 지원.
- ✅ TimeZone 코드표(probe_04+04b): **실제 시간대 102개 전부 확정**(코드 −1~100) → `tz_table.py`.
  날짜 명령이 임의 시간대로 완전 변환. (dir 나머지 14개는 시간대 아닌 메서드.)
- ✅ Planet(0x12) 명령군(probe_05): setIntensity(1026)/CloudsIntensity(1064)/AtmosphereIntensity(1065)/
  OrbitIntensity(1030)/ElevationScale(1059)/RingModel(1186)/TerrainModel(1184). ⚠️ 구 디스어셈블 추정 오류 정정.
- ✅ Place2D.setPosition(5633, Vec3 결합) — 프로덕션에서 확정(옛 5633 미스터리 해소).
- ✅ Camera(시점, 전역) 명령군(probe_06/07): setPositionLBR(273)/L(274)/B(275)/R(276),
  setOrientationHPR(289)/H(290)/P(291), setTargetAzimuth(306)/Height(307), setTarget(305), setZoomFov(316).
  track 대상 천체를 payload 에 `TRK` 로 임베드(첫 슬롯 채택).
- ✅ 관측자 바인딩(probe_10): `Place2D.setParent(4881)` — 관측지→지구 부착. `earth.portId(port)` 를
  부모 bodyId 로 양방향 해석. 같은 규칙으로 카메라 track 의 `place.portId(...)` 도 왕복 → **scene 완전 왕복**.
- ✅ Light ON 정체(probe_11): **태양(IndividualStar=0x0B/770)·별(Stars=0x0C/514)**. + Galaxy/Constellation/
  Nebula/Messier/Insert2D/SkySurvey family 확정. 검은하늘(probe_09): `Planet.setLightPollutionIntensity=1057`.
- **프로덕션 쇼 커버리지 85%**(scenario_v2 5종, 27줄 중 23줄).
- 남은 과제(4줄): 771(IndividualStar?), 1062(Planet#0), 1283(Satellite?), 1025(init). 상세: 노트 ⑮.

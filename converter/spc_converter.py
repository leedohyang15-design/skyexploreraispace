"""
Sky Explorer - Python → SPC 변환기 (v0.1)
====================================================================
녹화 샘플(test_A→a.SPC, test_C→c.SPC)에서 역설계한 SPC 라인 포맷 기반.

SPC 라인 = TAB 구분 67컬럼 고정:
  [0]=E  [1]=타임코드(HH-MM-SS-FF)  [2]=101  [3]=cmdId
  [4..]=헤더필드  →  bodyId  →  값들  →  0 패딩  →  [66]=꼬리공백(30칸)

역설계된 매핑(녹화 확정):
  (Satellite, setTerrainModel) → cmd 1394, 헤더[1,2],     페이로드[모델idx]
  (Satellite, setIntensity)    → cmd 1282, 헤더[3,6,DUR], 페이로드[1, v, 1]
  (Mark,      setIntensity)    → cmd 4356, 헤더[3,6,DUR], 페이로드[1, v, 1]
  (Mark,      setColor)        → cmd 4357, 헤더[3,9,0],   페이로드[r,g,b, 1,1]
  bodyId = (family<<24)|(index+1)   family: Satellite=0x15, Mark=0x03

🔑 probe_01(p1.SPC, setIntensity(0.3, Anim(2.5))) 로 값/Anim 인코딩 확정:
  1282 라인 = [3, 6, 2.5, bodyId, 1, 0.3, 1]
    → animDuration(2.5)은 '헤더 3번째 슬롯'(head 의 "DUR" 자리), intensity(0.3)는
      페이로드 '가운데'(pay 의 "V"), 앞뒤 1 은 상수(추정: 뒤=보간코드).
  1394 라인 = [1, 2, bodyId, 7]  → 모델 인덱스 7 그대로.
  (구 v0.1 가정 '값[v, animDur, 1]' 은 샘플이 전부 1.0 이라 착각한 것으로 판명.)

⚠️ 아직 추정: color trailing(1,1), 페이로드 앞 상수 1, argType/fieldCount 의 의미.
  각 클래스 1건씩 값 바꿔 녹화하면 확정.

spec 주도 설계:
  head: cmdId 뒤 헤더. "DUR" 는 Anim duration 자리표시자(없으면 상수만).
  pay : bodyId 뒤 페이로드 레이아웃. "V"=스칼라값, "IDX"=enum/인덱스,
        "R"/"G"/"B"=Vec 성분, 그 외 정수=상수. (양방향 변환기가 이 spec 공유)
"""
import ast
import os
import sys

# TimeZone 정수코드↔멤버 매핑(probe_04 자동생성). 없으면 빈 표로 폴백.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from tz_table import TZ_NAME2CODE, TZ_CODE2NAME
except Exception:
    TZ_NAME2CODE, TZ_CODE2NAME = {}, {}

NUM_COLS  = 67                 # 총 컬럼 수 (마지막 = 꼬리공백)
TRAILING  = " " * 30           # col 66
PAD_UPTO  = NUM_COLS - 1       # 0 으로 채울 마지막 인덱스(66은 꼬리)

# --- 클래스 → body family (bodyId 상위 바이트). 녹화로 확정된 것만. 추가 시 확장 ---
FAMILY = {
    "Satellite":      0x15,
    "Mark":           0x03,
    "Place2D":        0x1A,   # probe_03 확정 (436207618 = 0x1A000002)
    "Planet":         0x12,   # probe_05 확정 (301989891 = 0x12000003, Earth=PlanetName(2))
    # probe_11 로 확정된 family 바이트:
    "IndividualStar": 0x0B,   # 프로덕션 770/771 = 태양 켜기
    "Stars":          0x0C,   # 프로덕션 514 = 별 켜기
    "Galaxy":         0x06,
    "Constellation":  0x0A,
    "Nebula":         0x02,
    "Messier":        0x02,   # Nebula 와 같은 family(0x02) — cmdId 로 구분
    "Insert2D":       0x01,
    "SkySurvey":      0x2D,
    "Insert3D":       0x1D,   # 3D 모델(블랙홀/혜성/ISS/로버 등) — 라이브러리의 1/3 이 사용
    "InsertText":     0x1B,   # 사용자 녹화(일식 쇼) 확정: 452984834 = 0x1B000002
    "DomePointer":    0x11,   # Recording6 확정: 285212673 = 0x11000001 (DomePointer001)
    "ShootingStar":   0x07,   # Recording7 확정: 117440513 = 0x07000001 (ShootingStar001)
    "Bolide":         0x2E,   # Recording7 확정: 771751937 = 0x2E000001 (Bolide001)
    "Asteroid":       0x14,   # Recording9 확정: 335544326 = 0x14000006 (DB Apophis 인스턴스)
    "DwarfPlanet":    0x08,   # Recording10 확정: 134217730 = 0x08000002 (Pluto)
    "GlobularCluster":0x22,   # Recording12 확정: 570425370 = 0x2200001A (NGC5139_omegaCen=idx25)
}

# --- 전역(매니저/싱글톤) 클래스: bodyId 없는 명령. ---
#   DateManager(probe_02): 257 에 대상 천체 없음. Camera(probe_06): MainCamera 싱글톤 →
#   카메라 자체 bodyId 없이 payload 안에 track(대상 천체) 객체를 임베드.
GLOBAL = {"DateManager", "Camera", "Universe"}   # Universe: 녹화 확정(4885, bodyId 없음)

def body_id(cls, index):
    if cls not in FAMILY:
        raise KeyError("family 미확정 클래스: %s (녹화로 bodyId 상위바이트 확인 필요)" % cls)
    return (FAMILY[cls] << 24) | (index + 1)   # 관측: index 1 → +2

# --- (클래스, 메서드) → SPC 명령 스펙 ---
#   head: cmdId 뒤 헤더 필드("DUR"=Anim duration 자리). pay: (전역이면 헤더, 아니면 bodyId) 뒤
#         페이로드 레이아웃. 심볼: "V"=단일값, "IDX"=enum/인덱스, "A0".."An"=n번째 위치인자,
#         "R"/"G"/"B"=Vec 성분, 정수=상수. form: 역변환(SPC→Python) 렌더 방식.
CMD = {
    ("Satellite", "setTerrainModel"): dict(cmd=1394, head=[1, 2],        pay=["IDX"],                 form="enum"),
    ("Satellite", "setIntensity"):    dict(cmd=1282, head=[3, 6, "DUR"], pay=[1, "V", 1],             form="value_anim"),
    ("Mark",      "setIntensity"):    dict(cmd=4356, head=[3, 6, "DUR"], pay=[1, "V", 1],             form="value_anim"),
    ("Mark",      "setColor"):        dict(cmd=4357, head=[3, 9, 0],     pay=["R", "G", "B", 1, 1],   form="color"),
    # probe_03: Place2D 위치 3종 (값이 페이로드 '끝', animDur=0)
    ("Place2D",   "setLongitude"):    dict(cmd=5634, head=[3, 6, "DUR"], pay=[1, 1, "V"],             form="value_anim"),
    ("Place2D",   "setLatitude"):     dict(cmd=5635, head=[3, 6, "DUR"], pay=[1, 1, "V"],             form="value_anim"),
    ("Place2D",   "setAltitude"):     dict(cmd=5636, head=[3, 6, "DUR"], pay=[1, 1, "V"],             form="value_anim"),
    # 프로덕션에서 확정: 결합 위치. 단일 5634~6 과 별개(=옛 5633 미스터리 해소)
    # ⚠️ Recording6 확정: SPC 컬럼 순서 = (경도, 위도, 고도) — Python Vec(위도,경도,고도)와 x/y 스왑!
    ("Place2D",   "setPosition"):     dict(cmd=5633, head=[3, 6, "DUR"], pay=[1, 1, "G", "R", "B"],   form="vec"),
    # probe_02: DateManager.setDateTime — 전역(bodyId 없음). tz=32 는 관측 상수(멤버 매핑 미확정)
    ("DateManager", "setDateTime"):   dict(cmd=257,  head=[3, 12, "DUR"],
                                          pay=[1, 1, 1, "A0", "A1", "A2", "A3", "A4", "A5", 0, 0, "TZ"],
                                          form="datetime"),
    # probe_05: Planet(0x12) 명령군. intensity류=[1,v,1](atmo만 끝 0), RingModel=enum(animDur 없음)
    ("Planet", "setIntensity"):           dict(cmd=1026, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setCloudsIntensity"):     dict(cmd=1064, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setAtmosphereIntensity"): dict(cmd=1065, head=[3, 6, "DUR"], pay=[1, "V", 0], form="value_anim"),
    ("Planet", "setOrbitIntensity"):      dict(cmd=1030, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setElevationScale"):      dict(cmd=1059, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # ★ Recording19(지구 자전 시뮬) 확정: 지구형 행성 '객체 자전' 레시피 명령들.
    ("Planet", "setTerrainIntensity"):    dict(cmd=1063, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setNightLightsIntensity"):dict(cmd=1057, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),  # 밤면 도시광(호박색). ※1057=lightPollution 과 동일 cmd(레코딩 확인)
    # setRotationSpeedScale = 자전 속도 배율(Anim 없음, 단일 float). reset = 원복(인자 없음).
    ("Planet", "setRotationSpeedScale"):  dict(cmd=1029, head=[1, 2], pay=["V"],  form="value"),
    ("Planet", "resetRotationSpeedScale"):dict(cmd=1045, head=[1, 1], pay=[],     form="noarg"),
    # 자전축 시각화 = 1097 레이어형(레이어2=적도그리드/7=자전축/8=축포인터). Recording19 line81/82.
    ("Planet", "setEquatorialPoleAxisIntensity"):    dict(cmd=1097, head=[3, 7, "DUR"], pay=[1, "V", 7, 1], form="value_anim"),
    ("Planet", "setEquatorialPolePointerIntensity"): dict(cmd=1097, head=[3, 7, "DUR"], pay=[1, "V", 8, 1], form="value_anim"),
    # ── 토성 고리/렌더 = Recording22(saturn_rings) 확정 ──
    #   setRingModel enum 값: DefaultRing=0, BasicRing=2, Asteroids=13, Asteroids_3_0=28.
    #   ⚠️ 실측: 4모델 전환은 되지만 화면 차이가 '미미'(사용자 3회 확인) — DefaultRing/BasicRing 도 구별 어려움.
    ("Planet", "setRingModel"):            dict(cmd=1186, head=[1, 2],        pay=["IDX"],     form="enum"),
    ("Planet", "setScatteringIntensity"):  dict(cmd=1061, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setPointSaturation"):      dict(cmd=1034, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setCloudDirection"):       dict(cmd=1168, head=[1, 2],        pay=["V"],       form="value"),
    ("Planet", "setRingModel"):           dict(cmd=1186, head=[1, 2],        pay=["IDX"],     form="enum"),
    # 프로덕션 확정: "Earth Terrain" 라벨 + [1,2] enum 레이아웃 (Satellite.setTerrainModel 과 동형)
    ("Planet", "setTerrainModel"):        dict(cmd=1184, head=[1, 2],        pay=["IDX"],     form="enum"),
    # probe_10: 관측지→지구 '부착'. body=child(Place2D), payload=parent bodyId ×2. (arg=parent.portId)
    ("Place2D", "setParent"):             dict(cmd=4881, head=[1, 3],        pay=["PAR", "PAR"], form="parent"),
    # probe_09: Planet 대기/광공해 (레이아웃 = 표준 intensity)
    ("Planet", "setScatteringIntensity"):        dict(cmd=1061, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setLightPollutionIntensity"):    dict(cmd=1057, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setCloudLightPollution"):        dict(cmd=1182, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setAtmosphericRefractionFactor"):dict(cmd=1204, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setAtmosphereHaloIntensity"):    dict(cmd=1206, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # probe_11: family 발견 클래스들 (전부 표준 intensity 레이아웃)
    ("IndividualStar", "setIntensity"):          dict(cmd=770,   head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # ★ Recording20(태양 클로즈업) 확정: IndividualStar 태양 표면 기능 (family 184549377=Sun).
    ("IndividualStar", "setModel"):                  dict(cmd=830, head=[1, 2],        pay=["IDX"],       form="enum"),        # SDO=57
    ("IndividualStar", "setFilter"):                 dict(cmd=831, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),  # value=필터 index(304 홍염 등)
    ("IndividualStar", "setCycle"):                  dict(cmd=832, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),  # value=활동주기 index(2232 등)
    ("IndividualStar", "setPhotosphereIntensity"):   dict(cmd=833, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("IndividualStar", "setMagnetogramIntensity"):   dict(cmd=834, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),  # 흑점=자기 활동영역
    ("IndividualStar", "setMagneticLinesIntensity"): dict(cmd=835, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),  # 코로나 루프
    ("IndividualStar", "setCoronaIntensity"):        dict(cmd=794, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("IndividualStar", "setSaturationFactor"):       dict(cmd=793, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    # 황도광 = Recording26(zodiacal_light) 확정 (family Sun). EclipticGrid 은 Planet(Earth) 레이어2.
    ("IndividualStar", "setZodiacalLightIntensity"):           dict(cmd=821, head=[3, 6, "DUR"], pay=[1, "V", 1],    form="value_anim"),
    ("IndividualStar", "setZodiacalLightScatteringIntensity"): dict(cmd=822, head=[3, 6, "DUR"], pay=[1, "V", 1],    form="value_anim"),
    ("Planet",         "setEclipticGridIntensity"):            dict(cmd=1109, head=[3, 7, "DUR"], pay=[1, "V", 2, 1], form="value_anim"),
    ("Stars",          "setIntensity"):          dict(cmd=514,   head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Galaxy",         "setIntensity"):          dict(cmd=2050,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Galaxy",         "setExposure"):           dict(cmd=2073,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),  # Recording28(milky_way) 확정
    ("Constellation",  "setLinesIntensity"):     dict(cmd=1537,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # setArtIntensity(1545)·setLabelIntensity(1553) 은 아래(196~197)에 이미 정의됨 — Recording12/14 로 재확인.
    ("Nebula",         "setIntensity"):          dict(cmd=9985,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Messier",        "setIntensity"):          dict(cmd=5889,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Insert2D",       "setIntensity"):          dict(cmd=1802,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("SkySurvey",      "setIntensity"):          dict(cmd=13825, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # probe_11: Satellite 추가 메서드
    ("Satellite", "setLabelIntensity"):          dict(cmd=1302,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setElevationScale"):          dict(cmd=1309,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setCloudsIntensity"):         dict(cmd=1313,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # probe_06: Camera(시점, 전역). "TRK"=track 대상 천체 bodyId(2회 반복), 18/1/33 은 상수(모드?).
    #   track=-1(현재유지) 은 녹화 시 실제 부착 객체로 치환됨 → 역변환은 그 bodyId(int)로 복원.
    ("Camera", "setPositionLBR"):   dict(cmd=273, head=[3, 10, "DUR"], pay=[1, "TRK", "TRK", 18, 1, "R", "G", "B"], form="cam_vec3_track"),
    ("Camera", "setPositionR"):     dict(cmd=276, head=[3,  8, "DUR"], pay=[1, "TRK", "TRK", 18, 1, "V"],           form="cam_val_track"),
    ("Camera", "setOrientationHPR"):dict(cmd=289, head=[3, 10, "DUR"], pay=[1, 0, 0, 33, 1, "R", "G", "B"],         form="cam_vec3"),
    ("Camera", "setZoomFov"):       dict(cmd=316, head=[3,  5, "DUR"], pay=[1, "V", 1],                             form="value_anim"),
    # probe_07: 단축 시점 명령. L/B=track형(274 는 프로덕션과 동일 cmdId), Target/Orientation=track 없음.
    ("Camera", "setPositionL"):     dict(cmd=274, head=[3,  8, "DUR"], pay=[1, "TRK", "TRK", 18, 1, "V"],           form="cam_val_track"),
    ("Camera", "setPositionB"):     dict(cmd=275, head=[3,  8, "DUR"], pay=[1, "TRK", "TRK", 18, 1, "V"],           form="cam_val_track"),
    ("Camera", "setTargetAzimuth"): dict(cmd=306, head=[3,  5, "DUR"], pay=[1, 1, "V"],                             form="value_anim"),
    ("Camera", "setTargetHeight"):  dict(cmd=307, head=[3,  5, "DUR"], pay=[1, 1, "V"],                             form="value_anim"),
    ("Camera", "setOrientationH"):  dict(cmd=290, head=[3,  8, "DUR"], pay=[1, 0, 0, 33, 1, "V"],                   form="value_anim"),
    ("Camera", "setOrientationP"):  dict(cmd=291, head=[3,  8, "DUR"], pay=[1, 0, 0, 33, 1, "V"],                   form="value_anim"),
    # probe_08: setTarget(Vec(az,h,roll)) — 프로덕션 305 확정. Place2D.setPosition 과 동일 vec 레이아웃.
    ("Camera", "setTarget"):        dict(cmd=305, head=[3,  6, "DUR"], pay=[1, 1, "R", "G", "B"],                   form="vec"),
    # Insert3D (3D 모델, family 0x1D) — ff 라이브러리 최다 미매핑(1056줄/81파일). Orion 라벨로 확정.
    ("Insert3D", "setModelFilename"):  dict(cmd=6146, head=[2, 1],        pay=[],                       form="modelfile"),
    ("Insert3D", "setIntensity"):      dict(cmd=6145, head=[3, 6, "DUR"], pay=[1, "V", 1],              form="value_anim"),
    ("Insert3D", "setPositionLBR"):    dict(cmd=6147, head=[3, 9, "DUR"], pay=[1, 2, 1, "R", "G", "B"], form="vec"),
    ("Insert3D", "setOrientationHPR"): dict(cmd=6148, head=[3, 9, "DUR"], pay=[1, 2, 1, "R", "G", "B"], form="vec"),
    ("Insert3D", "setScale"):          dict(cmd=6149, head=[3, 6, "DUR"], pay=[1, "V", 1],              form="value_anim"),
    # ═══ Recording12 확정: GlobularCluster(0x22) — 오메가 센타우리 완성쇼 ═══
    ("GlobularCluster", "setIntensity"):        dict(cmd=9729, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("GlobularCluster", "setScale"):            dict(cmd=9730, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("GlobularCluster", "setPointerIntensity"): dict(cmd=9737, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("GlobularCluster", "setPointerType"):      dict(cmd=9740, head=[1, 2],        pay=["IDX"],     form="enum"),
    # ═══ 2026-07-06 사용자 녹화(일식·달 쇼 재녹화) 역해석으로 확정 ═══
    ("Universe",  "setGlobalIntensity"):       dict(cmd=4885, head=[3, 5, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setMoonAge"):               dict(cmd=1389, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setPlanetShineStrength"):   dict(cmd=1328, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # 달 그림자 세터 = Recording27(moon_terrain) 확정
    ("Satellite", "setShadowStrength"):        dict(cmd=1292, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setShadowContrast"):        dict(cmd=1291, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setScale"):                 dict(cmd=1283, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setEclipseShapeIntensity"): dict(cmd=1366, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Satellite", "setManualMoonPhase"):       dict(cmd=1391, head=[1, 2],        pay=["V"],       form="bool"),
    ("IndividualStar", "setScale"):            dict(cmd=771,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # 아날렘마(Recording30 실측): setTrajectoryIntensity=궤적선(8자). setMotionType=DateManager 전역
    #  (family 없음). MotionAnalemma 는 내부적으로 Earth 에 setRotationSpeedScale(≈1/366) 를 걸어 일일자전 상쇄.
    ("IndividualStar", "setTrajectoryIntensity"): dict(cmd=772, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("DateManager", "setMotionType"):          dict(cmd=4891, head=[1, 1],        pay=["V"],       form="value"),
    ("Planet",    "setEclipseShapeIntensity"): dict(cmd=1138, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Camera", "setOrientationSmoothXYZR"):    dict(cmd=295,  head=[3, 11, "DUR"],
                                                    pay=[1, "TRK", "TRK", 33, 1, "R", "G", "B", "W"], form="cam_vec4_track"),
    ("InsertText", "setIntensity"):            dict(cmd=3841, head=[3, 6, "DUR"], pay=[1, "V", 1],           form="value_anim"),
    ("InsertText", "setColor"):                dict(cmd=3842, head=[3, 9, "DUR"], pay=[1, "R", "G", "B", 1], form="color"),
    ("InsertText", "setSize"):                 dict(cmd=3843, head=[3, 6, "DUR"], pay=[1, "V", 1],           form="value_anim"),
    ("InsertText", "setText"):                 dict(cmd=3844, head=[2, 2],        pay=[],                    form="text"),
    ("InsertText", "setPosition"):             dict(cmd=3845, head=[3, 8, "DUR"], pay=[1, "R", "G", "B", 1], form="vec"),
    # 그림자(일식) 계열 — Recording1 실측: 레이어 상수(2=PenumbraBefore, 3=PenumbraAfter, 4=Antumbra)
    ("Planet", "setPenumbraBeforeLineIntensity"):  dict(cmd=1128, head=[3, 7, "DUR"], pay=[1, "V", 2, 1], form="value_anim"),
    ("Planet", "setPenumbraAfterLineIntensity"):   dict(cmd=1128, head=[3, 7, "DUR"], pay=[1, "V", 3, 1], form="value_anim"),
    ("Planet", "setAntumbraLineIntensity"):        dict(cmd=1128, head=[3, 7, "DUR"], pay=[1, "V", 4, 1], form="value_anim"),
    # ── 그림자 원뿔 마스터/본影 = Recording21(shadow_cone_eclipse) 확정 ──
    #   1073 = setShadowConeIntensity(마스터 ON/OFF). area 레이어(1132/1133): UmbraBefore=0, UmbraAfter=1,
    #   PenumbraBefore=2, PenumbraAfter=3, Antumbra=4. 1133 = setShadowConeAreaColor(레이어+RGB).
    ("Planet", "setShadowConeIntensity"):          dict(cmd=1073, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Planet", "setUmbraBeforeAreaIntensity"):     dict(cmd=1132, head=[3, 7, "DUR"], pay=[1, "V", 0, 1], form="value_anim"),
    ("Planet", "setUmbraAfterAreaIntensity"):      dict(cmd=1132, head=[3, 7, "DUR"], pay=[1, "V", 1, 1], form="value_anim"),
    ("Planet", "setPenumbraBeforeAreaIntensity"):  dict(cmd=1132, head=[3, 7, "DUR"], pay=[1, "V", 2, 1], form="value_anim"),
    ("Planet", "setPenumbraAfterAreaIntensity"):   dict(cmd=1132, head=[3, 7, "DUR"], pay=[1, "V", 3, 1], form="value_anim"),
    ("Planet", "setAntumbraAreaIntensity"):        dict(cmd=1132, head=[3, 7, "DUR"], pay=[1, "V", 4, 1], form="value_anim"),
    ("Satellite", "setPenumbraBeforeLineIntensity"): dict(cmd=1356, head=[3, 7, "DUR"], pay=[1, "V", 2, 1], form="value_anim"),
    ("Satellite", "setPenumbraAfterLineIntensity"):  dict(cmd=1356, head=[3, 7, "DUR"], pay=[1, "V", 3, 1], form="value_anim"),
    ("Satellite", "setAntumbraLineIntensity"):       dict(cmd=1356, head=[3, 7, "DUR"], pay=[1, "V", 4, 1], form="value_anim"),
    ("Satellite", "setPenumbraBeforeAreaIntensity"): dict(cmd=1360, head=[3, 7, "DUR"], pay=[1, "V", 2, 1], form="value_anim"),
    ("Satellite", "setPenumbraAfterAreaIntensity"):  dict(cmd=1360, head=[3, 7, "DUR"], pay=[1, "V", 3, 1], form="value_anim"),
    ("Satellite", "setAntumbraAreaIntensity"):       dict(cmd=1360, head=[3, 7, "DUR"], pay=[1, "V", 4, 1], form="value_anim"),
    # ── 별하늘 렌더링 = Recording23(stars_rendering) 확정 ──
    #   기본값 실측: exposure 5.68, contrast 1.6, pointSaturation 1.0. Modelset enum = GaiaDR2/Hipparcos.
    ("Stars", "setExposure"):            dict(cmd=535, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Stars", "setContrast"):            dict(cmd=536, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Stars", "setPointSaturation"):     dict(cmd=515, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Stars", "setModelset"):            dict(cmd=531, head=[1, 2],        pay=["IDX"],     form="enum"),
    # ═══ 2026-07-07 Recording6(밤하늘 가이드 투어 SPC판) 역해석으로 확정 ═══
    # 공통 발견: value_anim 계열 pay 첫 상수 1 의 정체 = 보간 코드(1=Linear, 2=Cubic)!
    #   (4885 gi 페이드인 Anim.cubic → "2", 8194 포인터 cubic 상승 → "2" 실측)
    ("InsertText", "setDistance"):               dict(cmd=3846, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Stars", "setTwinklingAmplitude"):          dict(cmd=517,  head=[3, 6, "DUR"], pay=[1, "V", 0], form="value_anim"),
    ("Stars", "setProperMotionOffsetInYears"):   dict(cmd=526,  head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Stars", "setProperMotion"):                dict(cmd=530,  head=[1, 2],        pay=["V"],       form="bool"),
    ("Constellation", "setArtIntensity"):        dict(cmd=1545, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("Constellation", "setLabelIntensity"):      dict(cmd=1553, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    # Place2D 그리드 = 5637 통합명령 + 레이어 인덱스 (1=자오선, 2=방위그리드, 10=방위표지) — 일식 1128 패턴과 동형
    ("Place2D", "setMeridianIntensity"):         dict(cmd=5637, head=[3, 7, "DUR"], pay=[1, "V", 1, 1],  form="value_anim"),  # Recording15 확정
    ("Place2D", "setAzimuthGridIntensity"):      dict(cmd=5637, head=[3, 7, "DUR"], pay=[1, "V", 2, 1],  form="value_anim"),
    ("Place2D", "setCardinalPointsIntensity"):   dict(cmd=5637, head=[3, 7, "DUR"], pay=[1, "V", 10, 1], form="value_anim"),
    ("Place2D", "setHourAngleGridIntensity"):    dict(cmd=5644, head=[3, 7, "DUR"], pay=[1, "V", 2, 1],  form="value_anim"),
    ("Planet",  "setEquatorialGridIntensity"):   dict(cmd=1097, head=[3, 7, "DUR"], pay=[1, "V", 2, 1],  form="value_anim"),
    # DomePointer (family 0x11): position 은 (az, h) 2성분 + 상수 1 (roll 미기록)
    ("DomePointer", "setPointerIntensity"):      dict(cmd=8193, head=[3, 6, "DUR"], pay=[1, "V", 1],           form="value_anim"),
    ("DomePointer", "setPosition"):              dict(cmd=8194, head=[3, 7, "DUR"], pay=[1, "R", "G", 1],      form="vec"),
    ("DomePointer", "setColor"):                 dict(cmd=8195, head=[3, 9, "DUR"], pay=[1, "R", "G", "B", 1], form="color"),
    ("DomePointer", "setPointerType"):           dict(cmd=8196, head=[1, 2],        pay=["IDX"],               form="enum"),
    ("DomePointer", "setApparentSize"):          dict(cmd=8197, head=[3, 6, "DUR"], pay=[1, "V", 1],           form="value_anim"),
    # 미등록 관찰(중복 cmdId 라 표엔 안 넣음 — 역변환기는 body family 로 분기해야 함):
    #  · 4881 = 범용 '부착'(setParent/addChild): Recording6 에선 cam.addChild(text, FixedForeground)
    #    → body=텍스트id, pay=[469762049(카메라), 469762052(포트 FixedForeground=+3)]
    #  · 257 mode 2 = DateManager.stop() (현재 JD 로 동결: pay=[1,1,2,JD]) / mode 1 = setDateTime
    #    Recording6 에서 TZ(DefaultTimeZone) = 0 관측 (probe 의 32 는 다른 존이었던 것)
    #  · 513(Stars) = 미확정 동반 명령(head[1,3], pay[1,0]) — Studio 가 반짝임 편집 때 2회 발행
    # ═══ 2026-07-09 Recording9(소행성 아포피스 ConnectTo 줌) 역해석 확정 ═══
    # Asteroid (family 0x14). DB Apophis 를 ConnectTo 하면 지형모델+궤도요소 인스턴스로 생성됨.
    # 궤도요소는 값으로 매핑 확정(203.9=Ω / 3.34=i / 0.191=e / 126.67=ω / 0.922=a / 90.28=M / epoch).
    ("Asteroid", "setTerrainUserModelFilename"): dict(cmd=6402, head=[2, 1],        pay=[],           form="modelfile"),
    ("Asteroid", "setIntensity"):                dict(cmd=6403, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setLongitudeOfAscendingNode"): dict(cmd=6406, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setInclination"):              dict(cmd=6407, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setEccentricity"):             dict(cmd=6408, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setArgumentOfPeriapsis"):      dict(cmd=6409, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setSemiMajorAxis"):            dict(cmd=6410, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setMeanAnomaly"):              dict(cmd=6412, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setEpoch"):                    dict(cmd=6413, head=[3, 6, "DUR"], pay=[1, "V", 1],  form="value_anim"),
    ("Asteroid", "setLabelNameOverride"):        dict(cmd=6425, head=[2, 1],        pay=[],           form="modelfile"),
    # ═══ 2026-07-09 Recording10(명왕성 뉴호라이즌스) 역해석 확정 — DwarfPlanet family 0x08 ═══
    ("DwarfPlanet", "setIntensity"):       dict(cmd=6913, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("DwarfPlanet", "setShadowStrength"):  dict(cmd=6926, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("DwarfPlanet", "setElevationScale"):  dict(cmd=6967, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("DwarfPlanet", "setTerrainModel"):    dict(cmd=7008, head=[1, 2],        pay=["IDX"],      form="enum"),
    #  · FadeTo Pluto = 지구형 안무(Set place2D→posLBR={0,89.999,4} 북극 R=4 도킹, target 30) + 위성들(1282) ON.
    #    줌은 276(setPositionR) 4→2.88→2.07→1.7. TerrainModel enum: NewHorizons=38(실측).
    #  · Asteroid 6414/6426/6432 = 표시 intensity 3종(orbit/label/pointer 추정, 시작 시 0 리셋) — 정확 매핑 TBD.
    #  · ConnectTo(SPC): 128 로그 = Time stop→Camera stop→Turn ON→Switch→'Look at'(295 자세슬루 3.97초)→307 TH30.
    #    줌은 우리 setPositionR = cmd 276(Asteroid 트랙) 연속. cubic 스텝 경계=끊김 → 선형 잘게가 매끄러움.
    # ═══ 2026-07-09 Recording(카메라 팬) 역해석 ═══
    #  · 지상 Sky View '수동 카메라 팬'(Turn left/right 드래그) = 273(setPositionLBR)+295
    #    (setOrientationSmoothXYZR) 쌍을 Place2D 관측자 트랙(0x1A000001)으로 0.6초 스텝 연속 발행,
    #    방위 L 을 부드럽게 스윕(-180→-284° 20초 실측). 종료 = 273/295 mode 2 릴리스 + 305 setTarget.
    #    → 스크립트 재현 시 setOrientationH 연속 호출이 이에 해당(수동 드래그와 동일 결과).
    # ═══ 2026-07-07 Recording7(쌍둥이자리 유성우) 역해석으로 확정 ═══
    # IndividualStar 포인터 (family 0x0B, 770 intensity 근처):
    ("IndividualStar", "setPointerIntensity"):   dict(cmd=805, head=[3, 6, "DUR"], pay=[1, "V", 1], form="value_anim"),
    ("IndividualStar", "setPointerType"):        dict(cmd=807, head=[1, 2],        pay=["IDX"],      form="enum"),
    # ShootingStar (family 0x07). ★★ setZenithalHourlyRate 값 = ZHR/60 (엔진 내부는 '분당' 저장!)
    #    실측: 120→2, 300→5, 3000→50, 60→1 (전부 ÷60 일치). 화면좌표=(az,h) DomePointer 규약과 동형.
    ("ShootingStar", "setRepresentationType"):     dict(cmd=2561, head=[1, 2],        pay=["IDX"],           form="enum"),
    ("ShootingStar", "setStartPosition"):          dict(cmd=2562, head=[3, 7, "DUR"], pay=[1, "R", "G", 1],  form="vec"),
    ("ShootingStar", "setArrivalPosition"):        dict(cmd=2563, head=[3, 7, "DUR"], pay=[1, "R", "G", 1],  form="vec"),
    ("ShootingStar", "setAdvancing"):              dict(cmd=2564, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setBrightness"):             dict(cmd=2565, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setRainSeed"):               dict(cmd=2566, head=[1, 2],        pay=["IDX"],           form="enum"),
    ("ShootingStar", "setTrailLength"):            dict(cmd=2567, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setRainGradientPoint"):      dict(cmd=2569, head=[3, 7, "DUR"], pay=[1, "R", "G", 1],  form="vec"),
    ("ShootingStar", "setRainChaosGradientPoint"): dict(cmd=2570, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setRainSpeed"):              dict(cmd=2571, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setZenithalHourlyRate"):     dict(cmd=2573, head=[3, 6, "DUR"], pay=[1, "V", 1],       form="value_anim"),
    ("ShootingStar", "setReferential"):            dict(cmd=2574, head=[1, 2],        pay=["IDX"],           form="enum"),
    # Bolide (family 0x2E). setIntensity 만 단순. set()/play() 은 복합 — 아래 주석 참조.
    ("Bolide", "setIntensity"):                    dict(cmd=14081, head=[3, 6, "DUR"], pay=[1, "V", 1],      form="value_anim"),
    #  · Bolide.set(az,h,alt_m ×2, speed) = 복합: 내부에서 (경도,위도,고도)로 변환 후
    #    14084 setStartPosition(Vec3 지리좌표) + 14085 setEndPosition + 14087(경로길이 스칼라) 발행.
    #    play(speed) → 14082 setEvolution 을 dur=경로길이/speed 로 애니(실측: speed 1.0 → 148초!).
    #    ⚠️ 화구가 '거의 안 움직임'의 원인 = 이 148초 크로싱. 빠른 화구는 speed 를 크게(≈50).
}

# cmdId → (클래스, 메서드) 역참조 (SPC→Python 변환기가 재사용)
CMD_BY_ID = {spec["cmd"]: (cls, method) for (cls, method), spec in CMD.items()}
FAMILY_BY_CODE = {code: cls for cls, code in FAMILY.items()}


def _is_pos(p):
    """위치인자 심볼 "A0".."An" 판정."""
    return isinstance(p, str) and len(p) >= 2 and p[0] == "A" and p[1:].isdigit()

def _arg_ctx(args):
    """파싱된 인자 리스트 → {scalars, val, dur, vec, tz, track}."""
    ctx = {"scalars": [], "dur": 0, "vec": [0, 0, 0], "tz": 0}
    for a in args:
        if a["kind"] == "anim":
            ctx["dur"] = a["val"]
        elif a["kind"] == "vec":
            ctx["vec"] = a["vec"]
        elif a["kind"] == "attr":         # TimeZone 등 enum 멤버 → 코드로 해석(스칼라 아님)
            ctx["tz"] = TZ_NAME2CODE.get(a["name"], 0)
        elif a["kind"] in ("num", "enum"):
            ctx["scalars"].append(a["val"])
        else:
            ctx["scalars"].append(0)      # 미해석 인자 → 자리 유지
    ctx["val"] = ctx["scalars"][0] if ctx["scalars"] else 0
    ctx["track"] = ctx["scalars"][-1] if ctx["scalars"] else -1   # Camera: track 은 마지막 int
    ctx["parent"] = 0
    ctx["str"] = ""
    for a in args:
        if a["kind"] == "parentbody":
            ctx["parent"] = a["val"]
        elif a["kind"] == "str":
            ctx["str"] = a["val"]
    return ctx

def build_head(spec, ctx):
    """head 템플릿의 "DUR" 를 실제 Anim duration 으로 치환."""
    return [ctx["dur"] if h == "DUR" else h for h in spec["head"]]

def build_payload(spec, ctx):
    """pay 레이아웃의 심볼("V"/"IDX"/"A0..An"/"R"/"G"/"B")을 실제 값으로 치환."""
    out = []
    for p in spec["pay"]:
        if p in ("V", "IDX"):
            out.append(ctx["val"])
        elif _is_pos(p):
            i = int(p[1:])
            out.append(ctx["scalars"][i] if i < len(ctx["scalars"]) else 0)
        elif p == "TZ":
            out.append(ctx["tz"])
        elif p == "TRK":
            out.append(ctx["track"])
        elif p == "PAR":
            out.append(ctx["parent"])
        elif p in ("R", "G", "B"):
            out.append(ctx["vec"]["RGB".index(p)])
        else:
            out.append(p)                 # 상수
    return out


# ======================= Python 파싱 =======================
def _num(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_num(node.operand)
    return None

def _parse_arg(node):
    """인자 노드 → {kind, val/vec}."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {"kind": "str", "val": node.value}     # 문자열(모델 경로 등)
    n = _num(node)
    if n is not None:
        return {"kind": "num", "val": n}
    if isinstance(node, ast.Call):
        fname = _callname(node.func)
        if fname in ("Anim", "Animator"):
            d = _num(node.args[0]) if node.args else 0
            return {"kind": "anim", "val": d}
        if fname in ("Vec", "Vec3", "Vec4"):
            return {"kind": "vec", "vec": [_num(a) for a in node.args]}
        # enum-스타일 래퍼: XxxName(1), TerrainModel(12), RingModel(1) 등 → 내부 인덱스
        if node.args:
            iv = _num(node.args[0])
            if iv is not None:
                return {"kind": "enum", "val": iv}
    # 속성 접근 enum 멤버: DateManager.TimeZone.UTC_... → 멤버 이름 보존(스칼라 아님)
    if isinstance(node, ast.Attribute):
        return {"kind": "attr", "name": node.attr}
    return {"kind": "other", "val": 0}

def _callname(func):
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None

def _ctor_index(call):
    """ClassName(ClassName.XxxName(idx)) → idx. 없으면 0."""
    if call.args:
        return _parse_arg(call.args[0]).get("val", 0)
    return 0

def _resolve_parent_body(node, vars_):
    """setParent 인자 → 부모 객체 bodyId. `<var>.portId(...)` 는 var 의 (클래스,index)로 해석."""
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "portId"):
        recv = node.func.value
        if isinstance(recv, ast.Name) and recv.id in vars_:
            c, i = vars_[recv.id]
            try:
                return body_id(c, i)
            except KeyError:
                return 0
    n = _num(node)                      # 정수 리터럴 부모 id 도 허용
    return n if n is not None else 0


def parse_events(py_source):
    """Python 소스 → 이벤트 리스트 [(cls, method, [argdict...]) ...]."""
    tree = ast.parse(py_source)
    vars_ = {}     # 변수명 → (클래스, index)
    events = []

    def handle_call(call):
        # 체이닝: Camera(...).setX(...) 또는 var.setX(...)
        if not isinstance(call.func, ast.Attribute):
            return
        method = call.func.attr
        recv = call.func.value
        cls = index = None
        if isinstance(recv, ast.Name) and recv.id in vars_:
            cls, index = vars_[recv.id]
        elif isinstance(recv, ast.Call):
            cname = _callname(recv.func)
            if cname in FAMILY:
                cls, index = cname, _ctor_index(recv)
            elif cname in GLOBAL:
                cls, index = cname, None          # 전역 클래스: 인덱스 없음
        if cls is None:
            return
        if method == "setParent" and call.args:
            # place.setParent(earth.portId(port)) → 부모 객체 bodyId 로 해석
            args = [{"kind": "parentbody", "val": _resolve_parent_body(call.args[0], vars_)}]
        else:
            args = [_parse_arg(a) for a in call.args]
            # 카메라 track 등: 마지막 인자가 `<var>.portId(...)` 면 그 객체 bodyId 로 해석
            if call.args and args and args[-1]["kind"] == "other":
                rb = _resolve_parent_body(call.args[-1], vars_)
                if rb:
                    args[-1] = {"kind": "num", "val": rb}
        events.append((cls, method, index, args))

    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
            call = stmt.value
            cname = _callname(call.func)
            if cname in FAMILY and isinstance(stmt.targets[0], ast.Name):
                vars_[stmt.targets[0].id] = (cname, _ctor_index(call))
                continue
            if cname in GLOBAL and isinstance(stmt.targets[0], ast.Name):
                vars_[stmt.targets[0].id] = (cname, None)   # dm = DateManager()
                continue
        # 식(메서드 호출)
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                handle_call(node)
                break
    return events


# ======================= SPC 생성 =======================
def event_to_row(cls, method, index, args, timecode="00-00-00-00", bom=False):
    key = (cls, method)
    if key not in CMD:
        raise KeyError("매핑 미확정: %s.%s (녹화로 cmdId/헤더 확인 필요)" % (cls, method))
    spec = CMD[key]
    ctx = _arg_ctx(args)
    row = [("E" if not bom else "﻿E"), timecode, "101", spec["cmd"]]
    row += build_head(spec, ctx)
    if spec.get("form") == "modelfile":    # 특수: head + 문자열(경로) + bodyId
        row += [ctx["str"], body_id(cls, index)]
    else:
        if cls not in GLOBAL:              # 전역 명령(DateManager 등)은 bodyId 없음
            row += [body_id(cls, index)]
        row += build_payload(spec, ctx)
    fields = [str(_fmt(x)) for x in row]
    while len(fields) < PAD_UPTO:
        fields.append("0")
    fields.append(TRAILING)
    return "\t".join(fields)

def _fmt(x):
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x

def convert(py_source, timecode="00-00-00-00"):
    events = parse_events(py_source)
    rows = []
    for i, (cls, method, index, args) in enumerate(events):
        try:
            rows.append(event_to_row(cls, method, index, args, timecode,
                                     bom=(i == 0)))
        except KeyError as e:
            rows.append("# SKIP: %s" % e)
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python spc_converter.py <input.py> [output.SPC]")
        sys.exit(1)
    src = open(sys.argv[1], encoding="utf-8").read()
    out = convert(src)
    if len(sys.argv) >= 3:
        open(sys.argv[2], "w", encoding="utf-8").write(out)
        print("wrote", sys.argv[2])
    else:
        print(out)

"""
study_blackhole.py — SPC→Python 학습노트: 블랙홀 강착원반 씬
====================================================================
원본: model3d_blackHoleAccretion.SPC (우리 변환기 + 미매핑 수동해독).
이 씬으로 배우는 것: '3D 모델(.osg) 로드 → 부모에 부착 → 카메라 조준/줌' 패턴.

읽는 법: 각 블록 위 주석 = SPC 원본 cmdId 와 의미. [매핑]=우리 변환기가 자동, [해독]=수동.
"""
from skyExplorer import *
from studio import *
from Initialization import *

# ═════════════════════════════════════════════════════════════════
# 1) 블랙홀의 '위치'를 은하 중심에 잡는다 — Place2D 를 좌표 홀더로 사용
# ═════════════════════════════════════════════════════════════════
# [매핑] 5633 Place2D.setPosition(Vec(위도, 경도, 거리))
#   거리 2.468542e20 m = 약 2.6만 광년 (우리은하 중심까지). 블랙홀을 거기 놓음.
bh_place = Place2D(Place2D.Place2DName(0))
bh_place.setPosition(Vec(0.0, 0.0, 2.468542e20))

# [매핑] 4881 Place2D.setParent — 이 위치를 '은하(MilkyWay)' 좌표계에 부착
#   → 은하가 움직이면 블랙홀도 같이 따라감(상대좌표).
milkyway = Galaxy(Galaxy.GalaxyName.MilkyWay)
bh_place.setParent(milkyway.portId(Galaxy.GalaxyPort.EquatorialSynchronous))

# ═════════════════════════════════════════════════════════════════
# 2) 3D 블랙홀 모델(.osg)을 불러와 그 위치에 부착 — Insert3D
# ═════════════════════════════════════════════════════════════════
bh = Insert3D(Insert3D.Insert3DName(0))                 # 486539265 = 0x1D000001 → Insert3D#0
# [해독] 6145 Insert3D.setIntensity(1.0) — 모델 밝기 ON
bh.setIntensity(1.0, Anim(0.0))
# [해독] 6146 Insert3D.setModelFilename(path) — 강착원반 3D 모델 로드
#   ⚠️ 이 .osg 파일은 네 Studio 안에 있어야 로드됨(경로 참조만).
bh.setModelFilename("..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg")
# [매핑] 4881 Insert3D.setParent — 모델을 위 Place2D(블랙홀 위치)에 부착
bh.setParent(bh_place.portId(Place2D.Place2DPort.EquatorialSynchronous))
# [해독] 6148 Insert3D.setOrientationHPR(Vec(H,P,R)) — 원반을 90/0/90 로 기울임(옆에서 보이게)
bh.setOrientationHPR(Vec(90.0, 0.0, 90.0), Anim(0.0))
# [해독] 6149 Insert3D.setSize(1.0) — 크기 배율
bh.setSize(1.0, Anim(0.0))

# ═════════════════════════════════════════════════════════════════
# 3) 카메라: 블랙홀을 바라보며(track) 멀리서 → 4초간 접근(줌)
#    ★ 우리가 배운 '스크립트 줌' 패턴: setPositionLBR track=대상 + R/위치 애니메이션
# ═════════════════════════════════════════════════════════════════
cam = Camera(Camera.CameraName.MainCamera)
# [매핑] 273 setPositionLBR — L=-100(방향), R=5e-14(아주 가까운 스케일) / track=436207617(Place2D#0=블랙홀)
cam.setPositionLBR(Vec(-100.0, 0.0, 5e-14), Anim(0.0), bh_place.portId(Place2D.Place2DPort.EquatorialSynchronous))
# [해독] 295 = Camera ObsOri(대상 조준) — "블랙홀을 정면으로 바라보게" (보조 orientation)
#   295 는 아직 미매핑이지만, 실질 조준은 위 setPositionLBR 의 track 이 담당.
# [매핑] 273 setPositionLBR (Anim 4초) — L=5,B=5 로 이동 = 블랙홀로 다가가는 카메라 워크
cam.setPositionLBR(Vec(5.0, 5.0, 0.0), Anim(4.0), bh_place.portId(Place2D.Place2DPort.EquatorialSynchronous))

# ═════════════════════════════════════════════════════════════════
# 4) 시간 (원본은 특이한 257 형태 — 초=10 만 세팅, 시간연출용으로 추정)
# ═════════════════════════════════════════════════════════════════
# [매핑] 257 DateManager.setDateTime(...) — 원본 값이 비정상(year=0)이라 여기선 생략/주석.
#   (일반적 사용은: setDateTime(2010,6,17,12,0,0, tz, Anim))

print(">>> 블랙홀 씬 학습본 끝. 핵심: Insert3D 모델 로드+부착 / 카메라 track+애니메이션 줌")

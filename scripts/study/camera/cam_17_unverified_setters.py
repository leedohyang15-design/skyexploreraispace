# -*- coding: utf-8 -*-
# [카메라 17] 아직 안 써본 카메라 세터 13종 점검 (Camera 총 36개 중 미확인분)
#   시그니처는 API 문서에서 확인해 정확히 맞춤. 각 세터가 '뭘 하는지' 실측한다.
#
# 대상: setOrientationP / setOrientationR / setOrientationD / setOrientationHPRD /
#       setOrientationXYZ / setPositionL / setPositionX·Y·Z / setPositionXYZ /
#       setTargetAzimuth / setActiveTarget / setFocusDegree / setTraceMode
# (제외: setEyeDistance·setStereoPosition·setStereoRatio·setActiveTrackStereo·
#        setDomeMeanPixelRatio·setResolutionRatioStrength = 돔 스테레오/투영 하드웨어 설정)
#
# 총 예상 ~2분. 각 항목 4초 홀드 + 상태 읽기.
from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone


def st(tag):
    try:
        p = cam.positionLBR; o = cam.orientationHPR
        print("      [%s] pos(L=%.2f B=%.2f z=%.2f) HPR(%.1f, %.1f, %.1f)"
              % (tag, p.x, p.y, p.z, o.x, o.y, o.z))
    except Exception as e:
        print("      [%s] 읽기 예외: %s" % (tag, e))


def ground():
    try: SceneGraph().reset(1); sleep(1.5)
    except Exception: pass
    Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
    e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6, Anim(0.0))
    for c in ("Ori", "UMa", "Cas"):
        try: Constellation(getattr(Constellation.ConstellationName, c)).setLinesIntensity(0.7, Anim(0.0))
        except Exception: pass
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.2); dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.3)
    cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0)); sleep(0.6)


def trial(label, fn, hold=4.0, note=""):
    print("\n--- %s ---" % label)
    st("전")
    try:
        fn()
    except Exception as e:
        print("      ✗ 호출 실패(시그니처?): %s" % e); return
    sleep(hold); st("후")
    if note: print("      ★볼 것: %s" % note)


# ══════ A) 지상 프레임에서 — 방향(orientation) 계열 ══════
print("########## A) 지상 프레임: 방향 세터 ##########")
ground()

trial("setOrientationP(30) — 단독 Pitch(위아래 젖힘?)",
      lambda: cam.setOrientationP(30.0, Anim.cubic(2.0)),
      note="화면이 위/아래로 젖혀졌나 (Target 과 뭐가 다른가)")
ground()
trial("setOrientationR(45) — 단독 Roll(시선축 기울기?)",
      lambda: cam.setOrientationR(45.0, Anim.cubic(2.0)),
      note="하늘이 시계/반시계로 기울었나")
ground()
trial("setOrientationD(45) — D 가 뭔가? (Dome? Distance? 미지)",
      lambda: cam.setOrientationD(45.0, Anim.cubic(2.0)),
      note="뭐가 바뀌었나 (아무 변화 없으면 무반응)")
ground()
trial("setOrientationXYZ(Vec(0,0,1)) — 방향벡터(Roll 없는 버전)",
      lambda: cam.setOrientationXYZ(Vec(0.0, 0.0, 1.0), Anim.cubic(2.0)),
      note="위(+Z)를 바라보나")
ground()
trial("setOrientationHPRD(Vec4(90,0,0,0)) — HPR + D",
      lambda: cam.setOrientationHPRD(Vec4(90.0, 0.0, 0.0, 0.0), Anim.cubic(2.0), -1),
      note="H90 으로 돌았나 (D=0 은 무의미?)")
ground()
trial("setTargetAzimuth(90) — 타겟 방위 (옛 노트: 무반응)",
      lambda: cam.setTargetAzimuth(90.0, Anim.cubic(2.0)),
      note="방위가 동쪽으로 돌았나 (setOrientationH 와 차이)")
ground()
trial("setActiveTarget(True) — 타겟 활성화?",
      lambda: cam.setActiveTarget(True, Anim(1.0)), hold=3.0,
      note="화면 변화 있나 (없으면 내부 플래그)")
trial("setFocusDegree(0.5) — 초점?",
      lambda: cam.setFocusDegree(0.5, Anim(1.5)), hold=3.0,
      note="흐림/선명도 변화 있나")
trial("setTraceMode(True) — 트레이스 모드?",
      lambda: cam.setTraceMode(True), hold=3.0,
      note="궤적이 남나/뭔가 켜지나")
try: cam.setTraceMode(False)
except Exception: pass

# ══════ B) 행성 프레임에서 — 위치(position) 계열 ══════
print("\n\n########## B) 행성(화성) 프레임: 위치 세터 ##########")
ground()
h = DataManager.database().data(Data.Type.PlanetType, "Mars")
h.action(Action.Type.StraightGoTo).trigger(); sleep(4.0)
cam.setTargetHeight(30.0, Anim(1.0)); sleep(1.5)
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.5)); mars.setShadowContrast(0.0, Anim(0.5))
mars.setPlanetShineStrength(1.0, Anim(0.5)); sleep(1.0)
print("화성 도착 (B=90 도킹 유지)")
st("기준")

trial("setPositionL(+60) — 단독 L(경도) = 대상 주위 옆으로?",
      lambda: cam.setPositionL(cam.positionLBR.x + 60.0, Anim.cubic(3.0), -1), hold=4.0,
      note="화성 주위를 옆으로 돌았나 (오빗 연출 가능성)")

trial("setPositionXYZ(직교좌표) — LBR 대신 XYZ 로 이동?",
      lambda: cam.setPositionXYZ(Vec(0.0, 0.0, 3.0), Anim.cubic(3.0), -1), hold=4.0,
      note="⚠️ 화성이 사라졌으면 XYZ 단위가 달라 위험 → 쓰지 말 것")

print("\n\n===== 보고 요청 =====")
print("각 항목의 '전/후' 상태값 + 화면에서 무슨 일이 났는지 알려주세요.")
print("특히: ① setOrientationP/R 가 Target·HPR 과 어떻게 다른가")
print("      ② setOrientationD 의 D 가 뭔가 (무반응이면 그대로 기록)")
print("      ③ setPositionL 로 행성 주위 오빗이 되나 (되면 연출 도구 추가!)")
print("      ④ setFocusDegree/setTraceMode 가 화면에 뭘 하나")

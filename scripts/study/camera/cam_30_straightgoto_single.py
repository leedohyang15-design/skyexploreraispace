# -*- coding: utf-8 -*-
# [카메라 30] StraightGoTo 단독 정밀 관찰 — 화성 하나만, 끝까지, 아무것도 안 건드림
#
# ⚠️ cam_29 의 내 실수 2가지 (사용자 "화면 조정하다가 갑자기 넘어간다"의 원인):
#   ① R(positionLBR.z) 만 로깅 → **자세(orientation)가 도는 동안엔 R 이 안 변해** '정지'로 오판
#   ② "6초 R 불변이면 조기 종료" → 화면이 아직 조정 중인데 다음 대상으로 넘어가며 reset() = '갑자기 넘어감'
#
# 이 버전:
#   · **대상 1개(화성)만**. 다음 대상 없음 → 중간에 안 넘어감
#   · **조기 종료 없음**. 40초 끝까지 관찰
#   · **위치(L,B,R) + 자세(H,P,R) 둘 다** 1초 간격 로깅 → 뭐가 움직이는지 정확히 보임
#   · 관찰 끝나고도 **reset 안 함** → 최종 화면을 눈으로 확인 가능
from skyExplorer import *
from studio import *
from Initialization import *

WATCH = 40          # 관찰 시간(초) — 끝까지 본다

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone

# ── 지상 밤에서 출발 (여기까지만 세팅, 이후 카메라 안 건드림) ──
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.0)); sleep(1.5)

# 화성을 미리 밝게(도착 여부 눈으로 판별하기 쉽게)
mars = Planet(Planet.PlanetName.Mars)
mars.setShadowStrength(0.0, Anim(0.0)); mars.setShadowContrast(0.0, Anim(0.0))
mars.setPlanetShineStrength(1.0, Anim(0.0))


def snap():
    """위치와 자세를 동시에 읽는다 (둘 중 뭐가 움직이는지 봐야 하니까)"""
    try:
        p = cam.positionLBR; o = cam.orientationHPR
        return (p.x, p.y, p.z, o.x, o.y, o.z)
    except Exception:
        return None


print("=" * 66)
print("StraightGoTo → 화성 : 40초 정밀 관찰 (카메라 일절 안 건드림)")
print("=" * 66)
s0 = snap()
print("실행 전  pos(L=%.2f B=%.2f R=%.2f)  HPR(%.1f %.1f %.1f)" % s0)

DataManager.database().data(Data.Type.PlanetType, "Mars") \
    .action(Action.Type.StraightGoTo).trigger()

prev = s0
for t in range(1, WATCH + 1):
    sleep(1.0)
    s = snap()
    if s is None:
        print(" +%2ds  (읽기 실패)" % t); continue
    # 뭐가 변했는지 표시 — 위치인가 자세인가
    dpos = max(abs(s[0]-prev[0]), abs(s[1]-prev[1]), abs(s[2]-prev[2])) if prev else 0
    dori = max(abs(s[3]-prev[3]), abs(s[4]-prev[4]), abs(s[5]-prev[5])) if prev else 0
    tag = ""
    if dpos > 1e-6 and dori > 1e-6: tag = "  ← 위치+자세 둘 다 변화"
    elif dpos > 1e-6:               tag = "  ← 위치만 변화(이동중)"
    elif dori > 1e-6:               tag = "  ← 자세만 변화(회전중)"
    else:                            tag = "  (정지)"
    print(" +%2ds  pos(L=%8.2f B=%6.2f R=%12.2f)  HPR(%7.1f %6.1f %6.1f)%s"
          % ((t,) + s + (tag,)))
    prev = s

print("\n관찰 종료 — 화면은 그대로 둡니다(reset 안 함). 눈으로 확인하세요:")
print("  ① 지금 화면에 화성이 크게 보이나?  ② 태양/빈 우주인가?")
print("  ③ 위 로그에서 '위치만/자세만/둘다' 중 어떤 패턴이었나?")
print("  ④ 중간에 멈췄다면 몇 초쯤에 멈췄나?")
print("  (HUD 의 R 값도 같이 알려주시면 단위 대조에 도움됩니다)")

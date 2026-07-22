# -*- coding: utf-8 -*-
"""
videoplayer_show.py — VideoPlayer 로컬 영상 재생 (v3, 2026-07-22, 포맷 판별)
★ 이전 실패(v1/v2): H.264 MP4 로 load 해도 state=LegacyInvalidState / videoFile="" (빈값) = 엔진이 파일을 아예 안 받음.
★ 완본 핵심 발견: load 문서 = "filename (str) – Video file path to load. **Must be relative to user folder.**"
  → 절대경로는 거부될 수 있음 → 이번엔 **상대 파일명만** 사용(파일은 D:/SkyExplorer-Data/user 에).
★ 포맷 판별: 같은 영상을 4개 컨테이너로 만들어 하나씩 load → videoFile 이 채워지는(=엔진이 받는) 포맷을 찾는다.
  후보: video_test.wmv(WMV8) / .mpg(MPEG-1) / .avi(MS-MPEG4) / .mp4(H.264 대조군).
  → 4개 파일 전부 D:/SkyExplorer-Data/user 폴더에 넣고 실행. 로그의 'videoFile=' 이 비지 않는 포맷이 정답.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

# ★ 상대 파일명만 (완본: 반드시 유저폴더 상대경로). 우선순위 = Windows 호환 높은 순.
CANDIDATES = ["video_test.wmv", "video_test.mpg", "video_test.avi", "video_test.mp4"]

try:
    folder = str(Configuration.configuration().localUserFolder)
    print("★ 파일 넣을 폴더 localUserFolder = %r" % folder)
except Exception as e:
    print("Configuration 실패: %s" % e)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % e


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: VideoPlayer v3 — 포맷 판별(wmv/mpg/avi/mp4)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.4, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 12, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.6)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── VideoPlayer 생성 ────────────────────────────────────────
narr("로컬 영상 재생 — VideoPlayer (포맷 판별)", 3.0)
vp = None
for mk in (lambda: VideoPlayer(), lambda: VideoPlayer(0)):
    try:
        vp = mk(); print("   VideoPlayer 생성"); break
    except Exception as e:
        print("   생성 시도 실패: %s" % e)

eye = getattr(VideoPlayer.Eye, "Both", None)
print("   Eye=%s" % eye)


def try_format(fname):
    """한 포맷 load → videoFile/state/duration 즉시+폴링 확인. (videoFile 채워지면 엔진이 받은 것)"""
    print("   ════ load(%r) ════" % fname)
    feat(vp, "reset", Anim(0.0), label="(직전 상태 초기화)"); sleep(0.4)
    feat(vp, "setVolume", 0.5, Anim(0.0))
    feat(vp, "setOpacity", 1.0, Anim(0.0), label="(영상 보이게)")
    # load 는 (filename, anim, eye)
    if eye is not None:
        feat(vp, "load", fname, Anim(0.3), eye, label="(상대경로)")
    else:
        feat(vp, "load", fname, Anim(0.3), label="(상대경로)")
    sleep(0.3)
    print("   [즉시] videoFile=%r state=%s" % (rd(vp, "videoFile"), rd(vp, "state")))
    feat(vp, "play", Anim(0.3))
    accepted = False
    t = 0.0
    while t < 3.5:
        vf = rd(vp, "videoFile"); st = rd(vp, "state"); dur = rd(vp, "duration"); pos = rd(vp, "position")
        print("   [+%.1fs] videoFile=%r state=%s duration=%s position=%s" % (t, vf, st, dur, pos))
        if (isinstance(vf, str) and vf.strip()) or (isinstance(dur, (int, float)) and dur > 0) or ("Play" in str(st)):
            accepted = True
        sleep(0.5); t += 0.5
    return accepted


winner = None
for fname in CANDIDATES:
    narr("포맷 시도: %s" % fname, 1.5)
    if try_format(fname):
        winner = fname
        print("   ★★★ 엔진이 받은 포맷 = %s" % fname)
        break
    feat(vp, "stop", Anim(0.0)); feat(vp, "unLoad", Anim(0.0)); sleep(0.3)

if winner:
    narr("재생 중 — %s (6초)" % winner, 2.0)
    feat(vp, "setOpacity", 1.0, Anim(1.0)); sleep(6.0)
    print("   최종 state=%s position=%s" % (rd(vp, "state"), rd(vp, "position")))
    feat(vp, "setOpacity", 0.0, Anim(2.0)); sleep(2.2)
    narr("하늘로 복귀 — %s 재생 성공" % winner, 3.0)
    feat(vp, "stop", Anim(0.5)); feat(vp, "unLoad", Anim(0.5))
else:
    narr("4개 포맷 모두 로드 실패 — 엔진이 파일을 안 받음", 4.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v3 포맷판별). ★리포트: "
      "①★★4개 파일(video_test.wmv/.mpg/.avi/.mp4)을 전부 D:\\SkyExplorer-Data\\user 폴더에 넣었나(먼저 확인) "
      "②로그에서 'videoFile=' 이 '빈값 아닌' 포맷이 있나 — 있으면 그 포맷이 정답 "
      "③화면에 회전 초침 영상이 떴나(어느 포맷에서) "
      "④4개 다 videoFile='' 이면 = 이 빌드 VideoPlayer 가 파일 자체를 안 받음(경로/서브폴더 문제거나 미지원)")

# -*- coding: utf-8 -*-
"""
videoplayer_show.py — VideoPlayer 로 로컬 영상 재생 (2026-07-20, 완본 미개척 — 클로드 생성 파일)
★ VideoPlayer = 전체화면 비디오 오버레이. load(파일, Anim, Eye) → play(Anim) → setOpacity(1=영상/0=하늘).
  Name enum 없음 → `VideoPlayer()` 싱글톤. Eye = Both/Left/Right (Both=모노). 경로 = 유저폴더 상대 or 절대.
★ 파일: 클로드가 만든 video_test.mp4 (회전 초침 + 펄스 링 + 프레임 카운터, 6초) 를 D:/SkyExplorer-Data/user 에 넣음.
★ 흐름: 밤하늘 → 영상 load+play → opacity 0→1 (전체화면 영상, 6초 재생) → opacity 1→0 (하늘 복귀) → stop.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

VID_NAME = "video_test.mp4"
paths = []
try:
    folder = str(Configuration.configuration().localUserFolder)
    print("★ localUserFolder = %r" % folder)
    base = folder.rstrip("/\\")
    paths.append(("절대(/)", base + "/" + VID_NAME))
except Exception as e:
    print("Configuration 실패: %s" % e)
paths.append(("상대", VID_NAME))
print("★ 경로 후보: %s" % [p for _, p in paths])


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


def rd(obj, prop):
    try: return getattr(obj, prop)
    except Exception as e: return "err:%s" % e


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: VideoPlayer — 로컬 영상(video_test.mp4)")
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
narr("로컬 영상을 재생한다 — VideoPlayer", 3.0)
vp = None
for mk in (lambda: VideoPlayer(), lambda: VideoPlayer(0)):
    try: vp = mk(); print("   VideoPlayer 생성"); break
    except Exception as e: print("   생성 시도 실패: %s" % e)

if vp is not None:
    eye = getattr(VideoPlayer.Eye, "Both", None)
    print("   Eye=%s" % eye)
    feat(vp, "setOpacity", 0.0, Anim(0.0))
    feat(vp, "setVolume", 0.5, Anim(0.0))
    # 경로 후보로 로드 시도 (state 로 성공 판별)
    loaded = False
    for name, path in paths:
        print("   [%s] load %s" % (name, path))
        feat(vp, "load", path, Anim(0.5), eye, label="(%s)" % name)
        sleep(1.5)
        st = rd(vp, "state"); dur = rd(vp, "duration"); vf = rd(vp, "videoFile")
        print("      state=%s duration=%s videoFile=%s" % (st, dur, vf))
        loaded = True  # 어느 게 성공인지는 화면/state 로 판별
    # 재생 + 전체화면
    narr("재생 — 영상이 화면을 채운다 (6초)", 2.5)
    feat(vp, "play", Anim(0.5))
    feat(vp, "setOpacity", 1.0, Anim(1.5), label="(전체화면 영상)")
    sleep(6.5)   # 6초 영상 재생 관람
    print("   재생 중 state=%s position=%s" % (rd(vp, "state"), rd(vp, "position")))
    # 하늘 복귀
    feat(vp, "setOpacity", 0.0, Anim(2.0)); sleep(2.2)
    narr("하늘로 복귀", 2.0)
    feat(vp, "stop", Anim(0.5))
    feat(vp, "unLoad", Anim(0.5))
else:
    narr("VideoPlayer 생성 실패 — 로그 확인", 4.0)

narr("VideoPlayer — 돔에 재생하는 로컬 영상", 4.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. ★리포트: ①★★video_test.mp4 를 'D:\\SkyExplorer-Data\\user\\' 에 넣었나(먼저 확인) "
      "②재생 때 전체화면에 회전 초침+펄스 링+카운터 영상이 나왔나(움직이나) "
      "③로그 'state=' / 'duration=' 값 — StopState/PlayState & duration=6 이면 로드 성공 "
      "④안 나오면 = 파일 없음/코덱 문제 → state/duration 값 알려줘")

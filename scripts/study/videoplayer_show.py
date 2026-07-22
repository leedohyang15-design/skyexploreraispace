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

def poll(tag, secs=6.0, step=0.5):
    """load/play 가 비동기일 수 있어 state/duration 을 여러 번 폴링."""
    t = 0.0; ok = False
    while t < secs:
        st = rd(vp, "state"); dur = rd(vp, "duration"); vf = rd(vp, "videoFile"); pos = rd(vp, "position")
        print("   [%s +%.1fs] state=%s duration=%s position=%s videoFile=%s" % (tag, t, st, dur, pos, vf))
        try:
            if (isinstance(dur, (int, float)) and dur > 0) or ("Play" in str(st)):
                ok = True
        except Exception: pass
        sleep(step); t += step
    return ok


if vp is not None:
    eye = getattr(VideoPlayer.Eye, "Both", None)
    print("   Eye=%s" % eye)
    feat(vp, "setVolume", 0.5, Anim(0.0))
    feat(vp, "setOpacity", 1.0, Anim(0.0), label="(전체화면=영상 보이게 미리)")
    got = False
    for name, path in paths:
        print("   ── load(%s) = %s ──" % (name, path))
        feat(vp, "load", path, Anim(0.5), eye)
        sleep(0.5)
        feat(vp, "play", Anim(0.5))           # ★ play 가 실제 디코드를 트리거할 수 있어 load 직후 play
        if poll("%s load+play" % name, secs=4.0):
            got = True; print("   ★ 로드 성공(%s)" % name); break
        feat(vp, "stop", Anim(0.0)); feat(vp, "unLoad", Anim(0.0)); sleep(0.3)
    if got:
        narr("영상 재생 중 — 6초", 2.0)
        sleep(6.0)
    else:
        narr("영상 로드 실패 (duration=0) — 코덱/파일 확인", 4.0)
    print("   최종 state=%s position=%s" % (rd(vp, "state"), rd(vp, "position")))
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
print("종료(v2 호환코덱+폴링). ★리포트: ①★★새 video_test.mp4(baseline 코덱)로 교체했나 — 기존 파일 덮어쓰기 "
      "②이번엔 로그 'duration=' 이 6 근처로 뜨나(0 이면 아직 로드 실패) "
      "③화면에 회전 초침 영상 나왔나 ④duration 계속 0 이면 = 이 엔진이 mp4/h264 자체를 안 받는 것 → wmv/mpeg 로 바꿔봄")

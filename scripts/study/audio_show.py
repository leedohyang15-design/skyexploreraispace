# -*- coding: utf-8 -*-
"""
audio_show.py — 오디오 재생 (2026-07-22, 완본 미개척 Audio 계열)
★ 미개척 클래스 4형제: AudioLite(가장 단순) / AudioLayer(50레이어+상태읽기) / Audio(모노/스테레오 채널) / AudioPlayer(마스터볼륨).
★ VideoPlayer 는 ViPlayer 별도 호스트라 죽었지만, 오디오는 별도 렌더소스가 필요 없어 될 가능성 높음.
  게다가 AudioLayer 는 audioState/audioDuration/audioPosition 읽기가 있어 '파일이 실제로 로드됐는지' 검증 가능(video 처럼).
★ 경로: 완본 = "audio 폴더 상대경로 or 절대경로" → 절대경로(localUserFolder+파일명) 사용(그 폴더는 Insert2D 로 검증됨).
  파일: 클로드가 만든 audio_test.wav(+mp3/ogg) — 8초 도미솔 아르페지오+화음. D:/SkyExplorer-Data/user 에 넣음.
★ 흐름: 밤하늘 자막 → AudioLayer 로 load+play (상태 폴링) → 안되면 AudioLite → 안되면 Audio. 소리 나는지 귀로 확인.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

FILES = ["audio_test.wav", "audio_test.mp3", "audio_test.ogg"]
base = None
try:
    base = str(Configuration.configuration().localUserFolder).rstrip("/\\")
    print("★ 파일 넣을 폴더 = %r" % base)
except Exception as e:
    print("Configuration 실패: %s" % e)


def abspath(fn):
    return (base + "/" + fn) if base else fn


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:80])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:30]


# ── 무대: 밤하늘 ────────────────────────────────────────────
print("무대: Audio — 오디오 재생")
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
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.5, Anim(0.0))
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 20, 0)); txt.setSize(0.052); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


narr("밤하늘에 소리를 입힌다 — Audio", 3.0)

played = None   # (클래스명, 파일명)


# ── 1) AudioLayer (상태 읽기로 검증 가능) ───────────────────
def try_audiolayer():
    try:
        al = AudioLayer(AudioLayer.AudioLayerName.Layer001); print("   AudioLayer Layer001 생성")
    except Exception as e:
        print("   AudioLayer 생성 실패: %s" % str(e)[:80]); return None
    feat(al, "setOutputVolume", 0.9, Anim(0.0))
    for fn in FILES:
        p = abspath(fn)
        print("   ── AudioLayer.load(-1, %r) ──" % p)
        feat(al, "load", -1, p, label="(채널 -1=자동)")
        sleep(0.4)
        feat(al, "play", False, label="(loop=False)")
        t = 0.0
        while t < 3.0:
            st = rd(al, "audioState"); dur = rd(al, "audioDuration"); pos = rd(al, "audioPosition")
            print("   [+%.1fs] state=%s duration(ms)=%s position(ms)=%s" % (t, st, dur, pos))
            try:
                if (isinstance(dur, (int, float)) and dur > 0) or ("Play" in str(st)):
                    return (al, fn)
            except Exception:
                pass
            sleep(0.5); t += 0.5
        feat(al, "stop"); feat(al, "unload")
    return None


narr("① AudioLayer (상태 읽기로 검증)", 2.0)
r = try_audiolayer()
if r:
    played = ("AudioLayer", r[1]); al_obj = r[0]
    print("   ★★★ AudioLayer 재생 등록됨 = %s" % r[1])


# ── 2) AudioLite (가장 단순) ────────────────────────────────
if not played:
    narr("② AudioLite (단순 재생)", 2.0)
    try:
        lite = AudioLite(); print("   AudioLite 생성")
        for fn in FILES:
            p = abspath(fn)
            print("   ── AudioLite.load(%r) ──" % p)
            feat(lite, "load", p)
            sleep(0.4)
            feat(lite, "setVolume", 0.9)
            feat(lite, "play", Anim(0.0))
            sleep(3.0)   # AudioLite 는 상태 읽기 없음 → 귀로 확인
            print("   AudioLite %s 재생 시도(귀로 확인)" % fn)
            played = ("AudioLite", fn)
            break        # 소리 확인용으로 첫 파일만
    except Exception as e:
        print("   AudioLite 실패: %s" % str(e)[:80])


# ── 3) Audio (모노 채널) ────────────────────────────────────
if not played:
    narr("③ Audio (모노 채널 0)", 2.0)
    try:
        aud = Audio(); print("   Audio 생성")
        for fn in FILES:
            p = abspath(fn)
            print("   ── Audio.load(0, %r) ──" % p)
            feat(aud, "load", 0, p)
            sleep(0.4)
            feat(aud, "setVolume", 0.9, Anim(0.0))
            feat(aud, "play", Anim(0.0))
            sleep(3.0)
            played = ("Audio", fn)
            break
    except Exception as e:
        print("   Audio 실패: %s" % str(e)[:80])


# ── 결과 ────────────────────────────────────────────────────
if played:
    narr("재생 중 — %s / %s (소리 들리나?)" % played, 6.0)
    # 마무리: 페이드아웃 후 정지
    try:
        if played[0] == "AudioLayer":
            al_obj.setOutputVolume(0.0, Anim(2.0)); sleep(2.2); al_obj.stop(); al_obj.unload()
    except Exception as e:
        print("   정지 실패: %s" % str(e)[:60])
    narr("소리를 입힌 밤하늘 — Audio", 3.0)
else:
    narr("오디오 3형제 모두 로드 실패 — 로그 확인", 4.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(오디오 판별). ★리포트: "
      "①★★3개 파일(audio_test.wav/.mp3/.ogg)을 D:\\SkyExplorer-Data\\user 에 넣었나(먼저) "
      "②★스피커/헤드폰에서 '도미솔 아르페지오+화음(8초)' 소리가 났나 — 어느 단계(AudioLayer/AudioLite/Audio)에서 "
      "③로그 'AudioLayer [+Ns] state=.. duration(ms)=..' 에서 duration 이 0 이 아닌 값(8000 근처)이 떴나 "
      "④전부 무음+duration 0 이면 = 오디오도 별도 호스트 필요(스크립트 창 미지원)로 판정")

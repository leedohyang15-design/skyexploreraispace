# -*- coding: utf-8 -*-
"""
audio_show.py — 오디오 재생 v2 (2026-07-22, 판별 강화)
★ v1 결과: AudioLayer = InvalidAudioState + duration 0 (video 처럼 별도 호스트 필요 = 죽음).
  AudioLite 는 상태 읽기가 없어 '귀로만' 확인인데 v1 은 3초만 재생+명확한 큐 없어 사용자가 "잘 모르겠다".
★ v2 개선: ①**마스터 볼륨** AudioPlayer(MainAudioPlayer).setOutputVolume(1.0) 먼저 (0이면 무조건 무음).
  ②AudioLite wav 를 **풀 8초** 재생 + 화면 카운트다운("🔊 지금 소리! 8..7..") 으로 언제 들을지 명확.
  ③2번 반복 재생(확실히 들을 기회). wav 만(가장 호환).
★ 파일: audio_test.wav (D:/SkyExplorer-Data/user).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)

base = None
try:
    base = str(Configuration.configuration().localUserFolder).rstrip("/\\")
    print("★ 폴더 = %r" % base)
except Exception as e:
    print("Configuration 실패: %s" % e)
WAV = (base + "/audio_test.wav") if base else "audio_test.wav"


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:80])); return False


# ── 무대 ────────────────────────────────────────────────────
print("무대: Audio v2 — AudioLite 풀재생 + 마스터볼륨")
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
txt.setPosition(Vec(0, 22, 0)); txt.setSize(0.06); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def show(text):
    txt.setText(text); txt.setIntensity(1.0, Anim(0.5))


# ── ① 마스터 볼륨 최대 (핵심 — 0이면 무조건 무음) ──────────
show("① 마스터 볼륨 최대")
sleep(1.5)
try:
    ap = AudioPlayer(AudioPlayer.AudioPlayerName.MainAudioPlayer)
    print("   AudioPlayer(MainAudioPlayer) 생성")
    feat(ap, "setOutputVolume", 1.0, Anim(0.0), label="(마스터 100%)")
except Exception as e:
    print("   AudioPlayer 실패: %s" % str(e)[:80])

# ── ② AudioLite 로 풀 8초 재생 x2 ───────────────────────────
try:
    lite = AudioLite(); print("   AudioLite 생성")
except Exception as e:
    lite = None; print("   AudioLite 생성 실패: %s" % str(e)[:80])

if lite is not None:
    for round_i in (1, 2):
        show("② 오디오 로드 (%d회차)" % round_i); sleep(1.0)
        print("   ── AudioLite.load(%r) [%d회] ──" % (WAV, round_i))
        feat(lite, "load", WAV)
        sleep(0.5)
        feat(lite, "setVolume", 1.0, label="(파일 볼륨 100%)")
        feat(lite, "play", Anim(0.0), label="(재생 시작)")
        # 풀 8초 카운트다운 — 언제 들을지 명확
        for n in range(8, 0, -1):
            show("🔊 지금 소리 나야 함  —  %d" % n)
            sleep(1.0)
        feat(lite, "stop")
        show("(정지)"); sleep(1.5)
    show("소리가 났나요? — AudioLite")
    sleep(3.0)
else:
    show("AudioLite 생성 실패 — 로그 확인"); sleep(3.0)

txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(v2). ★리포트(딱 하나만 답해주면 됨): "
      "화면 '🔊 지금 소리 나야 함 8..7..' 카운트다운 도는 동안 스피커/헤드폰에서 "
      "'도미솔 아르페지오+화음' 소리가 ①또렷이 났다 / ②아주 작게라도 뭔가 났다 / ③완전 무음 "
      "— 이 셋 중 뭐였는지만 알려줘. (③이면 오디오도 별도 호스트라 스크립트 창 미지원으로 확정하고 접음)")

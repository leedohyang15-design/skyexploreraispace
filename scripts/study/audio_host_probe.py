# -*- coding: utf-8 -*-
# ═══ 오디오 호스트 프로브 — 'SoftwareManager 로 오디오 소스를 켤 수 있나?' ═══
#
# 배경 (2026-07-22 확정):
#   AudioLite / AudioLayer / Audio / AudioPlayer 4형제 전부 실패.
#   근거는 추측이 아니라 상태 읽기 — wav·mp3·ogg 모두 audioState=InvalidAudioState, duration=0.
#   = 파일이 아예 로드되지 않음. 마스터 볼륨 1.0 + 8초 재생해도 완전 무음(사용자 확인).
#   원인 추정: 미디어(ViPlayer)·오디오는 '별도 소프트웨어 소스/호스트' 소관이고
#             스크립트 창(Studio window)에선 그 소스가 비활성.
#
# ★ 이번에 확인할 것 (여태 한 번도 안 해본 것):
#   `SoftwareManager` 는 우리 노트에 '하드웨어/시스템(비검증)'으로만 남아 있다.
#   → 여기에 **소스를 켜는 메서드가 있는지**, 있다면 켠 뒤 오디오가 살아나는지.
#
# ⚠️ 안전 원칙: 1~3단계는 '읽기 전용 덤프'만 한다.
#   외부 프로그램을 실제로 띄우는 호출(softStart/softExe)은 4단계에 격리해 두고
#   기본은 꺼져 있다. 시스템에 영향을 줄 수 있으니 확인 후 직접 켤 것.
from skyExplorer import *
from studio import *
from Initialization import *

RUN_STEP4_LAUNCH = False      # ← 4단계(외부 실행 시도)를 하려면 True 로. 기본 False.

print("=" * 70)
print("오디오 호스트 프로브 시작")
print("=" * 70)

# ── 1. SoftwareManager 가 파이썬에 노출돼 있나 ───────────────
sm = None
try:
    sm = SoftwareManager()
    print("\n[1] SoftwareManager() 생성 OK →", sm)
except Exception as e:
    print("\n[1] SoftwareManager() 생성 실패:", e)
    try:
        sm = SoftwareManager
        print("    (클래스 자체는 접근 가능 — 싱글톤/정적일 수 있음)")
    except Exception as e2:
        print("    클래스 접근도 실패:", e2)

if sm is not None:
    try:
        members = [m for m in dir(sm) if not m.startswith("_")]
        print("\n[2] SoftwareManager 멤버 %d 개:" % len(members))
        for m in members:
            print("     ·", m)
    except Exception as e:
        print("\n[2] dir 실패:", e)

    # ── 3. Source enum — 오디오/ViPlayer 관련 멤버 확인 ──────
    try:
        srcs = [s for s in dir(SoftwareManager.Source) if not s.startswith("_")]
        print("\n[3] SoftwareManager.Source 멤버 %d 개:" % len(srcs))
        for s in srcs:
            mark = "  ★" if ("audio" in s.lower() or "player" in s.lower()
                             or "sound" in s.lower() or "vi" in s.lower()) else ""
            print("     ·", s, mark)
    except Exception as e:
        print("\n[3] Source enum 접근 실패:", e)

    # ── 3-b. '소스를 켜는' 것처럼 보이는 메서드가 있나 ───────
    try:
        cand = [m for m in dir(sm)
                if any(k in m.lower() for k in
                       ("start", "enable", "activate", "launch", "open", "source", "soft"))]
        print("\n[3-b] 소스 활성화 후보 메서드:", cand if cand else "(없음)")
    except Exception as e:
        print("\n[3-b] 후보 스캔 실패:", e)

# ── 4. (선택) 실제로 켜 보기 ─────────────────────────────────
if RUN_STEP4_LAUNCH and sm is not None:
    print("\n[4] 소스 활성화 시도 — 실패해도 스크립트는 계속된다")
    for name in ("Source_ViPlayer", "Source_Audio", "Source_Sound"):
        try:
            src = getattr(SoftwareManager.Source, name)
            print("     시도:", name, "→", src)
            try:
                sm.softStart(src)
                print("       softStart 호출 성공")
            except Exception as e:
                print("       softStart 실패:", e)
        except AttributeError:
            print("     (enum 에", name, "없음)")
    sleep(2.0)
else:
    print("\n[4] 건너뜀 (RUN_STEP4_LAUNCH=False). 1~3 결과 보고 판단할 것.")

# ── 5. 오디오 상태 재측정 — 호스트가 켜졌으면 값이 달라져야 한다 ─
print("\n[5] AudioLayer 상태 재측정 (기준값: InvalidAudioState / duration 0)")
try:
    lay = AudioLayer(AudioLayer.AudioLayerName.Layer001)
    print("     생성 OK. 로드 전 상태 =", getattr(lay, "audioState", "?"),
          "/ duration =", getattr(lay, "audioDuration", "?"))
    # ⚠️ 실제 파일 경로는 환경에 맞게 바꿔서 테스트할 것
    base = Configuration.configuration().localUserFolder
    print("     localUserFolder =", base)
    print("     → 이 폴더에 test.wav 를 두고 아래 줄의 주석을 풀어 재시도할 수 있다")
    # lay.load(0, base + "/test.wav"); sleep(1.0)
    # print("     로드 후 상태 =", lay.audioState, "/ duration =", lay.audioDuration)
except Exception as e:
    print("     AudioLayer 실패:", e)

print("\n" + "=" * 70)
print("판정 기준")
print("  · [3] Source enum 에 오디오 계열이 있고 [3-b] 에 start/enable 류가 있으면 → 4단계 시도 가치 있음")
print("  · 그런 메서드가 아예 없으면 → 파이썬에서 호스트를 켤 방법이 없다는 뜻 =")
print("    '오디오는 Studio UI/오퍼레이터 소관' 이 최종 확정. 더 파지 말 것.")
print("=" * 70)

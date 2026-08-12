#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""짧은 예제(g*.py) 를 한 파일로 묶어 돔에서 한 번에 훑을 수 있게 만든다.

왜 필요한가:
  Studio 는 스크립트를 하나씩 불러 실행한다. 검증할 게 7개면 7번 반복해야 하고,
  그러다 보면 '나중에 한꺼번에' 미루게 된다. 그게 미확인 12개가 쌓인 이유다.
  → 4분 30초짜리 한 파일로 만들어 한 번에 끝낸다.

⚠️ 원본을 고쳤으면 이 도구를 다시 돌려 배치를 재생성할 것 (배치를 직접 고치지 마라).
    python3 tools/make_batch.py
"""
import os
import re

OUT = "scripts/demo/BATCH_g_series.py"
SRC = "scripts/golden/"

# 순서에 의도가 있다: 화성 2개(클로즈업↔비행)를 붙이고, 딥스카이 2개(NEBULA↔NGC)를 붙여
# '되는 것'과 '안 되는 것'을 나란히 보게 한다.
ORDER = [
    ("g1_mars_closeup.py",         "화성 클로즈업 — 줌이 폭발하지 않고 표면이 보이나"),
    ("g7_mars_flight.py",          "화성으로 비행 — 도착 폴링이 먹어 카메라가 안 날아가나"),
    ("g2_catseye_travel.py",       "고양이눈 성운 — NEBULA 패널은 GoTo 여행이 되나"),
    ("g3_rosette_show.py",         "장미성운 — NGC 패널은 제자리 ON + ScaleUp 만 되나 (g2 와 짝)"),
    ("g4_constellation_slider.py", "별자리 슬라이더 — 선/그림/라벨이 한 번에 페이드되나"),
    ("g5_spaceship_approach.py",   "우주선 접근 — Insert2D 애니가 영상처럼 움직이나"),
    ("g8_world_sky_tour.py",       "세계 도시 투어 — 관측지가 이름으로 옮겨지고 하늘이 바뀌나"),
]

GAP = '''
def _gap(label):
    """절 사이 구분 — 암전 2초 + 로그. 어디서 끊겼는지 눈과 로그 양쪽으로 알 수 있다."""
    try:
        u = Universe(Universe.UniverseName.MainUniverse)
        for _ in range(10):
            u.setGlobalIntensity(0.0, Anim(0.0))
            sleep(0.2)
    except Exception as e:
        print("   구분 암전 실패:", e)
    print("\\n" + "=" * 62)
    print(">>> " + label)
    print("=" * 62)

'''


def build():
    head = ["# -*- coding: utf-8 -*-",
            "# ─────────────────────────────────────────────────────────────",
            "#  검증: 미확인 — 이 배치 자체가 검증용이다. 각 절을 보고 판정한 뒤",
            "#        원본 g*.py 의 '#  검증:' 줄을 갱신할 것 (python3 tools/ledger.py)",
            "# ─────────────────────────────────────────────────────────────",
            "",
            "# " + "═" * 74,
            "#  [배치 검증] 짧은 예제 %d개 연속 재생  (총 약 4분 30초)" % len(ORDER),
            "#",
            "#  ⚠️ 이 파일은 **자동 생성물**이다 — 직접 고치지 마라.",
            "#     원본 g*.py 를 고친 뒤 `python3 tools/make_batch.py` 로 재생성할 것.",
            "#",
            "#  ⚠️ 각 절은 자기 `SceneGraph().reset()` 으로 시작하므로 앞 절 상태를 물려받지 않는다.",
            "#     절마다 try/except 로 감싸 하나가 죽어도 나머지가 돌고, 절 사이 2초 암전으로 구분한다.",
            "#",
            "#  재생 순서 (판정 포인트)"]
    for i, (f, why) in enumerate(ORDER, 1):
        head.append("#    %d) %-28s %s" % (i, f, why))
    head += ["# " + "═" * 74,
             "from skyExplorer import *",
             "from studio import *",
             "from Initialization import *",
             ""]
    body = "\n".join(head) + "\n" + GAP

    for i, (fname, why) in enumerate(ORDER, 1):
        src = open(SRC + fname, encoding="utf-8").read()
        src = re.sub(r"^# -\*- coding[^\n]*\n", "", src)
        src = re.sub(r"^#\s*─+\n(?:#[^\n]*\n)+?#\s*─+\n", "", src, count=1)   # 검증 헤더 제거
        src = re.sub(r"^from (skyExplorer|studio|Initialization) import \*\n", "", src, flags=re.M)
        ind = "\n".join(("    " + ln) if ln.strip() else ln for ln in src.split("\n"))
        body += "\n# ── %d) %s ──────────────────────────────\n" % (i, fname)
        body += '_gap("%d/%d  %s")\ntry:\n%s\nexcept Exception as _e:\n    print("!! %s 실패:", _e)\n' % (
            i, len(ORDER), why.replace('"', "'"), ind, fname)

    body += '\nprint("\\n배치 종료 — 짧은 예제 %d개")\n' % len(ORDER)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(body)
    print("생성: %s (%d 줄, 절 %d개)" % (OUT, body.count("\n"), len(ORDER)))


if __name__ == "__main__":
    build()

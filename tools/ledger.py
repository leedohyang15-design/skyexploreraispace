#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""검증 원장 — 골든 스크립트가 '돔에서 실제로 확인됐는지'를 모아 보여준다.

왜 필요한가 (2026-08-10):
  천왕성 쇼에서 기하 오류가 **연달아 네 개** 나왔다(L축·R단위·도킹대기·intensity).
  전부 **코드는 멀쩡하고 규칙 검사도 통과**했는데 돔에서 돌려보고서야 드러났다.
  → 정적 검사로 잡히는 결함과, 돔에서만 드러나는 결함은 종류가 다르다.
    그래서 "규칙 통과"와 "돔 확인"을 **따로** 기록해야 하고, 그게 이 원장이다.

쓰는 법:
    python3 tools/ledger.py            # 표 출력
    python3 tools/ledger.py --md       # docs/24_verification_ledger.md 갱신

확인했으면 해당 스크립트 머리의 `#  검증:` 줄을 직접 고친다(이 도구는 읽기만 한다).
  예) #  검증: 확인 (2026-08-12) — 전막 재생, 이상 없음
"""
import glob
import os
import re
import sys

HEADER_RE = re.compile(r"^#\s+검증:\s*(.+)$", re.M)
GOLDEN = "scripts/golden/*.py"


def grade(note):
    if note.startswith("미확인"):
        return "❌ 미확인"
    if note.startswith("부분확인"):
        return "🟡 부분확인"
    return "✅ 확인"


def rows():
    out = []
    for f in sorted(glob.glob(GOLDEN)):
        s = open(f, encoding="utf-8").read()
        m = HEADER_RE.search(s)
        note = m.group(1).strip() if m else "(검증 줄 없음 — 헤더를 추가할 것)"
        out.append((os.path.basename(f), len(s.splitlines()), grade(note), note))
    return out


def main():
    r = rows()
    if "--md" in sys.argv:
        md = ["# 검증 원장 — 골든 스크립트",
              "",
              "> `python3 tools/ledger.py --md` 로 생성. 원본은 각 스크립트 머리의 `#  검증:` 줄이다.",
              "",
              "**규칙 통과 ≠ 돔 확인.** 프레임·L/B·R 단위 같은 기하 오류는 정적 검사로 안 잡히고",
              "돔에서 돌려야만 드러난다(2026-08-10 천왕성에서 네 개가 한꺼번에 터진 이유).",
              "",
              "| 스크립트 | 줄 | 상태 | 내용 |",
              "|---|---:|---|---|"]
        for name, n, g, note in r:
            md.append("| `%s` | %d | %s | %s |" % (name, n, g, note))
        done = sum(1 for x in r if x[2].startswith("✅"))
        part = sum(1 for x in r if x[2].startswith("🟡"))
        md += ["",
               "**요약: 확인 %d · 부분확인 %d · 미확인 %d (총 %d)**"
               % (done, part, len(r) - done - part, len(r)),
               "",
               "## 돔 세션에서 볼 것 (미확인 우선)",
               ""]
        for name, n, g, note in r:
            if g.startswith("❌"):
                md.append("- [ ] `%s`" % name)
        os.makedirs("docs", exist_ok=True)
        open("docs/24_verification_ledger.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
        print("docs/24_verification_ledger.md 갱신 (%d개)" % len(r))
        return

    print("%-32s %5s  %-12s %s" % ("스크립트", "줄", "상태", "내용"))
    print("-" * 100)
    for name, n, g, note in r:
        print("%-32s %5d  %-12s %s" % (name, n, g, note[:52]))
    done = sum(1 for x in r if x[2].startswith("✅"))
    part = sum(1 for x in r if x[2].startswith("🟡"))
    print("-" * 100)
    print("확인 %d · 부분확인 %d · 미확인 %d (총 %d)" % (done, part, len(r) - done - part, len(r)))


if __name__ == "__main__":
    main()

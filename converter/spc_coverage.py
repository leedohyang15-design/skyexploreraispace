"""
spc_coverage.py — SPC 코퍼스 커버리지 리포트 (2026-07-22)
====================================================================
SPC 파일들이 쓰는 cmdId 를 전수 집계 → '매핑됨/미매핑'을 빈도순으로 출력.
→ 프로덕션 쇼가 실제로 자주 쓰는데 아직 매핑 안 된 cmd = 다음에 채울 최우선 후보.

사용법:  python spc_coverage.py <dir 또는 file.SPC ...>
예:      python spc_coverage.py samples/  converter/samples/
"""
import os, sys, glob
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spc_converter import CMD_BY_ID

NOISE = {128, 4865, 4885, 12037, 12038, 5650, 4881}   # 주석/세션/부착 등 스크립트 무관


def iter_spc(paths):
    for p in paths:
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, "**", "*.SPC"), recursive=True):
                yield f
        elif p.endswith(".SPC"):
            yield p


def cmds_in(path):
    out = []
    for ln in open(path, encoding="utf-8", errors="ignore"):
        cols = ln.split("\t")
        if len(cols) < 4 or cols[0].strip() not in ("E", "C"):
            continue
        if cols[2].strip() != "101":     # 101 = 실제 명령 (0=주석 등)
            continue
        try:
            out.append(int(cols[3]))
        except ValueError:
            pass
    return out


def main(paths):
    files = sorted(set(iter_spc(paths)))
    if not files:
        print("SPC 파일 없음:", paths); return
    total = Counter()
    per_file_unmapped = Counter()
    for f in files:
        cs = cmds_in(f)
        total.update(cs)
    mapped = {c: n for c, n in total.items() if c in CMD_BY_ID and c not in NOISE}
    unmapped = {c: n for c, n in total.items() if c not in CMD_BY_ID and c not in NOISE}
    distinct = len([c for c in total if c not in NOISE])
    cov = 100.0 * len(mapped) / distinct if distinct else 0
    occ_all = sum(n for c, n in total.items() if c not in NOISE)
    occ_map = sum(n for c, n in total.items() if c in CMD_BY_ID and c not in NOISE)
    cov_w = 100.0 * occ_map / occ_all if occ_all else 0

    print("=" * 60)
    print("SPC 코퍼스 커버리지 —  파일 %d개 / 고유 cmd %d개(노이즈 제외)" % (len(files), distinct))
    print("  고유 cmd 기준:  매핑 %d / 미매핑 %d  = %.1f%%" % (len(mapped), len(unmapped), cov))
    print("  ★실사용(빈도가중) 기준:  %d/%d 라인  = %.1f%%  ← 실제 변환 가능 비율" % (occ_map, occ_all, cov_w))
    print("=" * 60)
    print("\n[미매핑 cmd — 빈도순 (다음 매핑 최우선 후보)]")
    for c, n in sorted(unmapped.items(), key=lambda x: -x[1])[:40]:
        print("  cmd %-6d  ×%-4d  (family추정 0x%02X)" % (c, n, (0)))  # family는 bodyId 로 별도 확인
    print("\n[매핑된 상위 cmd (참고)]")
    for c, n in sorted(mapped.items(), key=lambda x: -x[1])[:15]:
        cls, m = CMD_BY_ID[c]
        print("  cmd %-6d  ×%-4d  %s.%s" % (c, n, cls, m))


if __name__ == "__main__":
    args = sys.argv[1:] or [os.path.join(HERE, "samples")]
    main(args)

"""
spc_converter 회귀 테스트 — 녹화 샘플(samples/)을 재현하는지 검증.
실행: python verify.py   (타임코드는 런타임값이라 비교에서 제외)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spc_converter as C
import spc_to_python as R

#   (py, spc): py=None 이면 소스가 없는 SPC → 왕복(SPC→Py→SPC)만 검증.
CASES = [("test_A_satellite.py", "a.SPC"), ("test_C_mark.py", "c.SPC"),
         ("p1_probe.py", "p1.SPC"),   # 값≠1.0 녹화: animDur=헤더, 값=페이로드 확정
         ("p2_probe.py", "p2.SPC"),   # DateManager.setDateTime(257): 전역/위치인자 6개
         ("p3_probe.py", "p3.SPC"),   # Place2D lon/lat/alt(5634-6): family 0x1A
         (None,          "p4.SPC"),   # 날짜×60 시간대 — tz 코드표 왕복 검증
         (None,          "p4b.SPC"),  # 날짜×42 시간대(동쪽 구간) — tz 누적분 왕복
         ("p5_probe.py", "p5.SPC"),   # Planet 6종(1026/1064/1065/1030/1059/1186): family 0x12
         (None,          "p6.SPC"),   # Camera 시점 4종(273/276/289/316): 전역+track obj-ref
         (None,          "p7.SPC"),   # Camera 단축 6종(274/275/306/307/290/291)
         (None,          "p8.SPC"),   # Camera.setTarget(305) — 시점 시스템 완성
         ("p10_probe.py","p10.SPC"),  # Place2D.setParent(4881) — 관측지→지구 부착
         (None,          "p9.SPC")]   # Planet 대기/광공해(1061/1206/1057/1182/1204)

def cols(line):
    return [x.lstrip("﻿").strip() for x in line.rstrip("\n").split("\t")]

def _cmp_spc(a_lines, b_lines):
    """타임코드(col1) 제외 전 컬럼 비교."""
    if len(a_lines) != len(b_lines):
        return False
    for g, r in zip(a_lines, b_lines):
        gc, rc = cols(g), cols(r)
        if gc[:1] + gc[2:] != rc[:1] + rc[2:]:
            return False
    return True

def _spc_lines(text):
    return [l for l in text.splitlines() if l.strip() and not l.lstrip("﻿").startswith("#")]

def main():
    allok = True
    for py, spc in CASES:
        ref = _spc_lines(open(os.path.join(HERE, "samples", spc),
                              encoding="utf-8", errors="ignore").read())
        # 정방향: Python → SPC == 녹화본 (소스 있을 때만)
        if py is not None:
            src = open(os.path.join(HERE, "samples", py), encoding="utf-8").read()
            fwd = _cmp_spc(_spc_lines(C.convert(src)), ref)
            fwd_s = "✅" if fwd else "❌"
        else:
            fwd, fwd_s = True, "—"      # 소스 없음: 정방향 스킵
        # 역방향 왕복: SPC → Python → SPC == 녹화본
        rt = _cmp_spc(_spc_lines(C.convert(R.to_python("\n".join(ref)))), ref)
        print("%-24s : Py→SPC %s | SPC→Py→SPC %s"
              % (py or spc, fwd_s, "✅" if rt else "❌"))
        allok = allok and fwd and rt
    print("\nRESULT:", "ALL PASS ✅" if allok else "FAIL ❌")
    sys.exit(0 if allok else 1)

if __name__ == "__main__":
    main()

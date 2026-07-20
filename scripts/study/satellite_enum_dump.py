# -*- coding: utf-8 -*-
"""
satellite_enum_dump.py — SatelliteName enum '전체' 덤프 (2026-07-16)
★ 목적: "해왕성은 트리톤만" 이 진짜인지 검증. 지금까지 '내가 추측한 이름으로 hasattr' 만 했음(게으름).
  → 실제 enum 에 등록된 위성 이름을 전부 출력해서, 해왕성(및 다른 행성) 위성이 어떤 철자/이름으로
    존재하는지 눈으로 확인한다. (Nereid/Proteus/Larissa 가 다른 표기로 있을 수도.)
★ 참고로 각 이름의 인덱스(int 값)도 같이 출력 — SPC family/index 매핑에 유용.
"""

from skyExplorer import *
from studio import *
from Initialization import *

SN = Satellite.SatelliteName
names = [m for m in dir(SN) if not m.startswith("__")
         and m not in ("name", "names", "values", "as_integer_ratio", "bit_count",
                       "bit_length", "conjugate", "denominator", "from_bytes",
                       "imag", "is_integer", "numerator", "real", "to_bytes")]

print("=== SatelliteName 전체 %d개 ===" % len(names))
# 이름 + 정수값 출력 (값으로 정렬해 계열이 뭉치게)
rows = []
for nm in names:
    try:
        v = int(getattr(SN, nm))
    except Exception:
        v = -999
    rows.append((v, nm))
rows.sort()
for v, nm in rows:
    print("  %5d  %s" % (v, nm))

# 해왕성·천왕성 후보 키워드로 필터(있으면 잡힘)
print("\n=== 해왕성/천왕성 위성 후보 키워드 매칭 ===")
KW = ["Triton", "Nereid", "Proteus", "Larissa", "Galatea", "Despina", "Thalassa",
      "Naiad", "Halimede", "Psamathe", "Sao", "Laomedeia", "Neso", "Hippocamp",
      "Miranda", "Ariel", "Umbriel", "Titania", "Oberon", "Puck", "Portia",
      "Juliet", "Cressida", "Rosalind", "Belinda", "Cordelia", "Ophelia"]
low = {n.lower(): n for n in names}
for kw in KW:
    hit = [orig for l, orig in low.items() if kw.lower() in l]
    print("  %-12s -> %s" % (kw, hit if hit else "(없음)"))

print("\n종료. 리포트: 위 '전체 목록'에서 해왕성 위성(트리톤 말고 Nereid/Proteus 등)이 "
      "다른 철자로라도 있는지 확인 요망. 키워드 매칭 결과도 같이 봐줘.")

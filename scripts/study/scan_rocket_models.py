# -*- coding: utf-8 -*-
"""
scan_rocket_models.py — 유저 폴더에서 **로켓·발사체 모델을 찾아낸다** (2026-08-13)

★ 왜: 대본 Scene 1 은 아리안 5호 발사 장면인데 우리에겐 로켓 모델이 없다.
  그런데 유저 폴더에는 **모델 파일이 1,282개**(우주선 .osg/.ive 만 151개) 있다
  — 허블·아폴로·새턴V·셔틀·카시니·ISS 등이 이미 들어 있는 걸 전에 확인했다.
  로켓을 새로 굽기 전에 **이미 있는 걸 먼저 찾는다.**

★ 하는 일
  ① 유저 폴더를 훑어 3D 모델 파일을 전부 모으고
  ② 이름이 로켓·발사체스러운 것을 추려 목록으로 찍고
  ③ 상위 후보를 **실제로 로드해 보고 modelRadius 까지 찍는다**(이름만으로는 모른다)

★ 결과 사용법: 쓸 만한 게 나오면 그 **경로를 알려 주세요.**
  쇼의 `ROCKET_MODEL` 한 줄에 넣으면 Scene 1 에 로켓이 붙는다(배선은 이미 해 뒀다).
  쓸 만한 게 없으면 고리처럼 **직접 구우면 된다**(아리안 5 는 원통 + 부스터 2개 + 페어링이라 쉽다).
"""

from skyExplorer import *
from studio import *
from Initialization import *

import os

EXT = (".osg", ".ive", ".obj", ".3ds", ".stl", ".osgb", ".osgt", ".flt")

# 로켓·발사체·발사대 후보 키워드 (소문자 비교)
KEYS = ("ariane", "arian", "rocket", "launch", "saturn", "soyuz", "falcon", "atlas",
        "delta", "titan", "proton", "vega", "h2a", "h-2", "gslv", "pslv", "long march",
        "shuttle", "sts", "booster", "pad", "gantry", "nuri", "kslv", "naro",
        "apollo", "vehicle", "lv", "stage")

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception as e:
    print("유저 폴더 조회 실패: %s" % e)

print("=" * 66)
print("유저 폴더: %s" % USER)
print("=" * 66)

allm, hits = [], []
if USER and os.path.isdir(USER):
    for root, dirs, files in os.walk(USER):
        for f in files:
            if f.lower().endswith(EXT):
                full = os.path.join(root, f)
                rel = full[len(USER):].lstrip("\\/")
                allm.append(rel)
                low = rel.lower()
                if any(k in low for k in KEYS):
                    hits.append(rel)
else:
    print("⚠️ 유저 폴더를 못 찾았다 — 경로를 확인해 주세요")

print("모델 파일 총 %d개 · 키워드 일치 %d개" % (len(allm), len(hits)))
print("-" * 66)

hits.sort(key=lambda x: (len(x), x))
for h in hits[:60]:
    try:
        sz = os.path.getsize(os.path.join(USER, h))
    except Exception:
        sz = -1
    print("   %-58s %8d B" % (h[:58], sz))
if len(hits) > 60:
    print("   … 그 외 %d개" % (len(hits) - 60))

# ── 상위 후보를 실제로 로드해 본다 (이름만으로는 모른다) ──────────
print("-" * 66)
print("로드 판정 — 상위 후보 (⚠️ 폴링. 고정 sleep 은 Loading 인 채 지나간다)")


def probe(rel, slot):
    try:
        ins = Insert3D(Insert3D.Insert3DName(slot))
        ins.setModelFilename(os.path.join(USER, rel))
        t = 0.0
        while t < 12.0:
            sleep(0.4)
            t += 0.4
            st = str(ins.loadingStatus)
            if "Loaded" in st:
                print("   ✓ %-46s radius=%s" % (rel[:46], ins.modelRadius))
                return True
            if "Error" in st:
                print("   ✗ %-46s %s" % (rel[:46], st))
                return False
        print("   … %-46s 시간초과" % rel[:46])
    except Exception as e:
        print("   ✗ %-46s %s" % (rel[:46], e))
    return False


for i, h in enumerate(hits[:8]):
    probe(h, 20 + i)
    try:
        Insert3D(Insert3D.Insert3DName(20 + i)).setIntensity(0.0, Anim(0.0))
    except Exception:
        pass

# ── 로켓이 없으면 우주선이라도 (참고용) ────────────────────────────
print("-" * 66)
print("참고 — 우주선/탐사선 계열 모델 (로켓이 없을 때 대안)")
ships = [m for m in allm if any(k in m.lower() for k in
                                ("cassini", "hubble", "iss", "voyager", "galileo",
                                 "juno", "newhorizons", "viking", "spacecraft", "sat"))]
for m in ships[:25]:
    print("   %s" % m[:62])
if len(ships) > 25:
    print("   … 그 외 %d개" % (len(ships) - 25))

print("=" * 66)
print("쓸 만한 경로를 알려 주시면 쇼의 ROCKET_MODEL 한 줄에 넣습니다.")
print("없으면 아리안 5 를 직접 굽겠습니다(원통 + 부스터 2개 + 페어링 — 고리보다 쉽습니다).")
print("=" * 66)

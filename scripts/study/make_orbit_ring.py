# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 만들기만 했다. probe_ring_model.py 로 방향·크기를 확인해야 한다.
# ─────────────────────────────────────────────────────────────
"""
make_orbit_ring.py — 궤도선을 **직접 만든 3D 모델**로 그린다 (2026-08-13)

★ 왜 만드나
  `OrbitalPlace` 궤도선이 **이 빌드에서는 닫힌 원을 못 그린다.** 나선으로 벌어진다.
  판별 프로브(probe_orbit_spiral.py)의 A 단계 = **검증된 예제 코드 그대로**였는데 그것도 나선이었다.
  → 내 쇼의 버그가 아니라 **클래스 자체가 안 되는 것**이다(SkySurvey·VideoPlayer 와 같은 부류).
    예전에 "궤도 렌더됨"으로 적어 둔 기록은 궤도 5개가 겹쳐 있어 나선인 걸 못 알아본 것이다.

★ 그래서 기계를 바꾼다
  **원을 계산으로 그려서 파일로 굽는다.** 전파기(propagator)가 없으니 **나선이 될 수가 없다.**
  모델 파이프라인은 이미 검증돼 있다 — 천리안 모델이 로드·착색·축척 전부 맞게 돌아간다.

★ 규격
  · 반지름 **1.0 (모델 단위 = 미터)** 인 얇은 띠. 쇼에서 `setScale` 로 실제 궤도 반지름을 준다.
    정지궤도 42,164 km → `setScale(4.2164e7)` / 무덤궤도 66,930 km → `setScale(6.693e7)`
  · **XY 평면**(z=0)에 눕혀 있다. 부모 프레임의 적도면과 맞는지는 프로브로 확인한다.
  · **앞뒤 양면**을 다 굽는다(뒷면 컬링으로 사라지는 일이 없게).
  · **`emissionColor` 를 색 그대로** 준다 = 스스로 빛난다. 태양 각도와 무관하게 늘 보인다.
    (천리안 모델에서 확인된 `Material{diffuseColor}` 구조를 그대로 쓰되 발광만 올렸다.)

⚠️ 파일 내용은 **ASCII 로만** — Studio 파이썬의 open(w) 은 cp949 라 한 글자만 벗어나도 통째로 실패한다.
"""

from skyExplorer import *
from studio import *
from Initialization import *

import os
import math

SEG = 128            # 둘레 분할 수. 128 이면 육안으로 완전한 원이다
BAND = 0.012         # 띠 폭(반지름 대비). 0.012 = 정지궤도에서 약 500km 폭 = 가느다란 선
#   ⚠️ 화면에서 너무 얇아 안 보이면 0.02~0.03 으로 올릴 것. 너무 굵으면 도넛처럼 보인다

RINGS = [
    ("ring_gold.osg", (1.00, 0.80, 0.30)),   # 정지궤도 — 일하던 자리
    ("ring_gray.osg", (0.62, 0.62, 0.70)),   # 무덤궤도 — 갈 곳
    ("ring_cyan.osg", (0.35, 0.90, 1.00)),   # 프로브 전용(방향 판별)
]

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception as e:
    print("   유저 폴더 조회 실패: %s" % e)
print("유저 폴더: %s" % USER)


def ring_tris(r_in, r_out):
    """XY 평면에 눕힌 고리 하나 → 삼각형 목록. 앞뒤 양면을 다 만든다."""
    tris = []
    for i in range(SEG):
        a0 = 2.0 * math.pi * i / SEG
        a1 = 2.0 * math.pi * (i + 1) / SEG
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)
        p00 = (r_in * c0, r_in * s0, 0.0)
        p01 = (r_out * c0, r_out * s0, 0.0)
        p11 = (r_out * c1, r_out * s1, 0.0)
        p10 = (r_in * c1, r_in * s1, 0.0)
        # 윗면(+Z)
        tris.append(((p00, p01, p11), (0.0, 0.0, 1.0)))
        tris.append(((p00, p11, p10), (0.0, 0.0, 1.0)))
        # 아랫면(-Z) — 감는 방향을 뒤집는다. 어느 쪽에서 봐도 보이게
        tris.append(((p00, p11, p01), (0.0, 0.0, -1.0)))
        tris.append(((p00, p10, p11), (0.0, 0.0, -1.0)))
    return tris


def geom(col, tris):
    """천리안 모델에서 **확인된** Material 구조. emissionColor 만 색 그대로 = 스스로 빛난다."""
    verts, norms = [], []
    for tri, n in tris:
        for v in tri:
            verts.append("        %.6f %.6f %.6f" % v)
            norms.append("        %.4f %.4f %.4f" % n)
    st = ['      StateSet {', '        DataVariance STATIC',
          '        rendering_hint DEFAULT_BIN', '        renderBinMode INHERIT',
          '        GL_LIGHTING ON',
          '        Material {', '          DataVariance STATIC',
          '          ColorMode OFF',
          '          ambientColor %.3f %.3f %.3f 1' % tuple(c * 0.5 for c in col),
          '          diffuseColor %.3f %.3f %.3f 1' % col,
          '          specularColor 0.05 0.05 0.05 1',
          '          emissionColor %.3f %.3f %.3f 1' % col,   # ← 스스로 빛난다
          '          shininess 4', '        }', '      }']
    return (['    Geometry {', '      DataVariance DYNAMIC',
             '      useDisplayList TRUE', '      useVertexBufferObjects FALSE'] + st +
            ['      PrimitiveSets 1', '      {',
             '        DrawArrays TRIANGLES 0 %d' % len(verts), '      }',
             '      VertexArray Vec3Array %d' % len(verts), '      {'] + verts +
            ['      }', '      NormalBinding PER_VERTEX',
             '      NormalArray Vec3Array %d' % len(norms), '      {'] + norms +
            ['      }', '      ColorBinding OVERALL', '      ColorArray Vec4Array 1',
             '      {', '        %.3f %.3f %.3f 1' % col, '      }', '    }'])


def w(name, text):
    """⚠️ Studio 파이썬 open(w) 은 cp949 — 내용에 ASCII 밖 글자가 있으면 통째로 실패한다."""
    if not USER:
        return None
    bad = [c for c in text if ord(c) > 127]
    if bad:
        print("   ✗ %s: ASCII 밖 문자 %d개 — 내용은 ASCII 로만" % (name, len(bad)))
        return None
    p = os.path.join(USER, name)
    try:
        f = open(p, "w")
        f.write(text)
        f.close()
        print("   ✓ %-16s %8d 바이트" % (name, len(text)))
        return p
    except Exception as e:
        print("   ✗ %s: %s" % (name, e))
        return None


print("=" * 60)
print("궤도선 모델 만들기 — 반지름 1.0 의 얇은 고리")
print("=" * 60)
tris = ring_tris(1.0 - BAND * 0.5, 1.0 + BAND * 0.5)
print("   분할 %d · 삼각형 %d개 · 띠 폭 %.3f(반지름 대비)" % (SEG, len(tris), BAND))

for fname, col in RINGS:
    body = geom(col, tris)
    osg = (['Geode {', '  DataVariance DYNAMIC', '  name "orbitring"',
            '  nodeMask 0xffffffff', '  cullingActive TRUE',
            '  num_drawables 1'] + body + ['}'])
    w(fname, "\n".join(osg) + "\n")

# ── 로드 판정 (폴링 — 고정 sleep 은 Loading 인 채 지나간다) ──
print("-" * 60)
print("로드 판정")
for i, (fname, col) in enumerate(RINGS):
    try:
        ins = Insert3D(Insert3D.Insert3DName(40 + i))
        ins.setModelFilename(os.path.join(USER, fname) if USER else fname)
        t = 0.0
        ok = False
        while t < 12.0:
            sleep(0.4)
            t += 0.4
            if "Loaded" in str(ins.loadingStatus):
                ok = True
                break
        print("   %-16s %s  modelRadius=%s" %
              (fname, "Loaded" if ok else "실패", ins.modelRadius))
        # ⚠️ 반지름 1.0 짜리 고리이므로 modelRadius 는 약 1.0 이어야 한다.
        #   (바운딩박스 대각선의 절반 = 평평한 원판이라 sqrt(2)/... 대략 1.41 근처일 수도 있다)
    except Exception as e:
        print("   %-16s 오류: %s" % (fname, e))

print("=" * 60)
print("다음: probe_ring_model.py 로 **어느 방향(HPR)이 적도면에 눕는지** 확인")
print("=" * 60)

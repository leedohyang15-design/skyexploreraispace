# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 만들고 방향까지 한 번에 확인하는 판이다.
#        ③ 단계에서 **어느 HPR 이 지구 밖으로 곧게 서는지**를 화면으로 가른다.
# ─────────────────────────────────────────────────────────────
"""
make_ariane5.py — 아리안 5 로켓을 굽는다 (2026-08-13)

★ 왜: 대본 Scene 1 이 발사 장면인데 로켓이 없었다. 유저 폴더를 뒤지는 대신 그냥 만든다.
  궤도선 고리에서 확인된 그대로 — **엔진이 못 주는 기하는 직접 구워서 올리면 된다.**

★ 실물 치수(아리안 5 ECA, 미터)
  · 전체 높이 약 53 m
  · EPC 중앙단  지름 5.4 · 길이 30.5   — **주황 단열폼**(아리안 5 의 얼굴)
  · EAP 고체부스터 지름 3.05 · 길이 31.6 — 흰색, 양옆에 하나씩
  · 페어링      지름 5.4 · 길이 17     — 흰색, 끝이 원뿔
  · 발칸 엔진 노즐 + 부스터 노즐 2기

★ 모델은 **+Z 를 향해 선다**(z=0 이 엔진면, z=53 이 페어링 끝).
  ⚠️ 문제는 이 +Z 가 부모 프레임에서 어느 쪽이냐다. 고리 실측에서 **모델 XY 평면 = 적도면**,
  즉 **모델 +Z = 북극 방향**이었다. 로켓은 적도에서 **바깥(하늘)** 을 향해야 하므로 눕혀야 한다.
  → ③ 단계에서 HPR 세 개를 나란히 세워 **어느 것이 곧게 서는지** 눈으로 고른다.

★ 발사대는 안 만든다 — 이유는 파일 끝 메모 참조.
"""

from skyExplorer import *
from studio import *
from Initialization import *

import os
import math

RUN_WRITE = True
RUN_CHECK = True          # ③ 방향 판별을 같이 돌린다

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M
KOURU_LON = -52.8
ROCKET_SCALE = 1.8e5      # 모델 반지름 ~28m × 1.8e5 = 약 5,000km (천리안 5,270km 와 비슷하게)

ORANGE = (0.82, 0.42, 0.18)   # EPC 단열폼 — 아리안 5 하면 떠오르는 그 색
WHITE = (0.93, 0.93, 0.95)
GREY = (0.55, 0.55, 0.60)
DARK = (0.16, 0.16, 0.19)
BLUE = (0.10, 0.20, 0.50)

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception as e:
    print("   유저 폴더 조회 실패: %s" % e)
print("유저 폴더: %s" % USER)


# ══ 기하 ═══════════════════════════════════════════════════════
def cyl(cx, cy, z0, z1, radius, seg=16, cap=True):
    """+Z 축 원통 (z0 → z1)."""
    tris = []
    for i in range(seg):
        a0 = 2.0 * math.pi * i / seg
        a1 = 2.0 * math.pi * (i + 1) / seg
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)
        p00 = (cx + radius * c0, cy + radius * s0, z0)
        p01 = (cx + radius * c0, cy + radius * s0, z1)
        p11 = (cx + radius * c1, cy + radius * s1, z1)
        p10 = (cx + radius * c1, cy + radius * s1, z0)
        n = ((c0 + c1) / 2.0, (s0 + s1) / 2.0, 0.0)
        tris.append(((p00, p01, p11), n))
        tris.append(((p00, p11, p10), n))
        if cap:
            tris.append((((cx, cy, z1), p01, p11), (0.0, 0.0, 1.0)))
            tris.append((((cx, cy, z0), p10, p00), (0.0, 0.0, -1.0)))
    return tris


def cone(cx, cy, z0, z1, r0, r1, seg=16):
    """원뿔대 — 페어링 끝(r1=0)이나 노즐(아래로 벌어짐)에 쓴다."""
    tris = []
    for i in range(seg):
        a0 = 2.0 * math.pi * i / seg
        a1 = 2.0 * math.pi * (i + 1) / seg
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)
        p00 = (cx + r0 * c0, cy + r0 * s0, z0)
        p01 = (cx + r1 * c0, cy + r1 * s0, z1)
        p11 = (cx + r1 * c1, cy + r1 * s1, z1)
        p10 = (cx + r0 * c1, cy + r0 * s1, z0)
        n = ((c0 + c1) / 2.0, (s0 + s1) / 2.0, 0.35)
        tris.append(((p00, p01, p11), n))
        tris.append(((p00, p11, p10), n))
        tris.append(((p00, p11, p01), (-n[0], -n[1], -n[2])))   # 안쪽면(노즐용)
        tris.append(((p00, p10, p11), (-n[0], -n[1], -n[2])))
    return tris


#  ── 아리안 5 조립 (z=0 엔진면 → z=53 페어링 끝) ─────────────────
PARTS = []
# 중앙단 EPC — 주황 단열폼
PARTS.append(("epc", ORANGE, cyl(0.0, 0.0, 0.0, 30.5, 2.70)))
PARTS.append(("epc_band", GREY, cyl(0.0, 0.0, 15.0, 15.8, 2.76, cap=False)))
PARTS.append(("vulcain", DARK, cone(0.0, 0.0, 0.0, -3.2, 0.9, 1.7)))     # 발칸 엔진 노즐

# 상단단 + 페어링 — 흰색
PARTS.append(("upper", WHITE, cyl(0.0, 0.0, 30.5, 36.0, 2.70)))
PARTS.append(("fairing", WHITE, cyl(0.0, 0.0, 36.0, 47.5, 2.70)))
PARTS.append(("fair_band", BLUE, cyl(0.0, 0.0, 41.0, 42.2, 2.74, cap=False)))
PARTS.append(("nose", WHITE, cone(0.0, 0.0, 47.5, 53.0, 2.70, 0.12)))

# 고체 부스터 EAP 2기 — 흰색, 양옆
for _nm, _x in (("eap_l", -4.45), ("eap_r", 4.45)):
    PARTS.append((_nm, WHITE, cyl(_x, 0.0, 1.2, 32.6, 1.52)))
    PARTS.append((_nm + "_nose", WHITE, cone(_x, 0.0, 32.6, 36.4, 1.52, 0.10)))
    PARTS.append((_nm + "_noz", DARK, cone(_x, 0.0, 1.2, -1.6, 0.75, 1.15)))
    PARTS.append((_nm + "_strut", GREY, cyl(_x * 0.5, 0.0, 24.0, 24.9, 0.30, seg=8)))
    PARTS.append((_nm + "_strut2", GREY, cyl(_x * 0.5, 0.0, 6.0, 6.9, 0.30, seg=8)))


# ══ 쓰기 ═══════════════════════════════════════════════════════
def geom(col, tris):
    """천리안 모델에서 확인된 Material 구조 그대로."""
    verts, norms = [], []
    for tri, n in tris:
        for v in tri:
            verts.append("        %.4f %.4f %.4f" % v)
            norms.append("        %.4f %.4f %.4f" % n)
    st = ['      StateSet {', '        DataVariance STATIC',
          '        rendering_hint DEFAULT_BIN', '        renderBinMode INHERIT',
          '        GL_LIGHTING ON',
          '        Material {', '          DataVariance STATIC',
          '          ColorMode OFF',
          '          ambientColor %.3f %.3f %.3f 1' % tuple(c * 0.40 for c in col),
          '          diffuseColor %.3f %.3f %.3f 1' % col,
          '          specularColor 0.10 0.10 0.10 1',
          '          emissionColor %.3f %.3f %.3f 1' % tuple(c * 0.18 for c in col),
          '          shininess 12', '        }', '      }']
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
        print("   ✗ %s: ASCII 밖 문자 %d개" % (name, len(bad)))
        return None
    p = os.path.join(USER, name)
    try:
        f = open(p, "w")
        f.write(text)
        f.close()
        print("   ✓ %-18s %8d 바이트" % (name, len(text)))
        return p
    except Exception as e:
        print("   ✗ %s: %s" % (name, e))
        return None


print("=" * 66)
print("아리안 5 만들기")
print("=" * 66)
if RUN_WRITE:
    nt = sum(len(t) for _, _, t in PARTS)
    zs = [v[2] for _, _, ts in PARTS for tri, _ in ts for v in tri]
    xs = [v[0] for _, _, ts in PARTS for tri, _ in ts for v in tri]
    print("   조각 %d개 · 삼각형 %d개 · 높이 %.1f m · 폭 %.1f m"
          % (len(PARTS), nt, max(zs) - min(zs), max(xs) - min(xs)))
    body = []
    for nm, col, tris in PARTS:
        body += geom(col, tris)
    osg = (['Geode {', '  DataVariance DYNAMIC', '  name "ariane5"',
            '  nodeMask 0xffffffff', '  cullingActive TRUE',
            '  num_drawables %d' % len(PARTS)] + body + ['}'])
    w("ariane5.osg", "\n".join(osg) + "\n")


# ══ ③ 방향 판별 — 어느 HPR 이 하늘을 향해 곧게 서나 ═════════════
# ⚠️ 모델은 +Z 로 서 있는데, 고리 실측에서 **모델 +Z = 북극 방향**이었다.
#    로켓은 적도에서 **바깥(하늘)** 을 향해야 하므로 눕혀야 한다. 후보 셋을 나란히 본다.
if RUN_CHECK:
    cam = Camera(Camera.CameraName.MainCamera)
    uni = Universe(Universe.UniverseName.MainUniverse)
    dm = DateManager()
    tz = DateManager.TimeZone.DefaultTimeZone
    earth = Planet(Planet.PlanetName.Earth)

    def feat(o, fn, *a):
        try:
            getattr(o, fn)(*a)
            return True
        except Exception as e:
            print("   ✗ %s: %s" % (fn, e))
            return False

    def dark(total, step=0.2):
        t = 0.0
        while t < total:
            uni.setGlobalIntensity(0.0, Anim(0.0))
            sleep(step)
            t += step

    print("-" * 66)
    print("③ 방향 판별 — 세 자세를 차례로 세운다")
    uni.setGlobalIntensity(0.0, Anim(0.0))
    SceneGraph().reset(1)
    sleep(1.8)
    dark(0.6)
    for i in range(8):
        try:
            Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
        except Exception:
            pass
    IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(0.4, Anim(0.0))
    dm.stop()
    sleep(0.2)
    dm.setDateTime(2010, 6, 26, 18, 0, 0, tz, Anim(0.0))   # 쿠루가 낮
    sleep(0.4)

    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    a = h.action(Action.Type.FadeTo) if h is not None else None
    if a is not None:
        a.trigger()
        dark(4.5)
    feat(earth, "setIntensity", 1.0, Anim(0.0))
    feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
    feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        feat(earth, fn, v, Anim(0.0))

    sp = None
    for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
        try:
            sp = earth.portId(getattr(Planet.PlanetPort, nm))
            break
        except Exception:
            continue

    ins = Insert3D(Insert3D.Insert3DName(9))
    ins.setModelFilename(os.path.join(USER, "ariane5.osg") if USER else "ariane5.osg")
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        if "Loaded" in str(ins.loadingStatus):
            break
    print("   로드=%s  modelRadius=%s" % (ins.loadingStatus, ins.modelRadius))
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setScale", ROCKET_SCALE, Anim(0.0))
    feat(ins, "setParent", sp)
    feat(ins, "setPositionLBR", Vec(KOURU_LON, 0.0, 1.9), Anim(0.0))

    # 카메라 — 로켓 옆에서 본다
    dark(0.4)
    cam.setPositionLBR(Vec(KOURU_LON + 11.0, 0.0, 2.6), Anim(0.0), sp)
    feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), sp)
    dark(0.4)
    cam.setTargetHeight(30.0, Anim(0.0))
    dark(0.4)

    txt = InsertText(InsertText.InsertTextName(5))
    cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
    txt.setPosition(Vec(0, 55, 0))
    txt.setColor(Vec(1.0, 1.0, 0.6))
    txt.setDistance(20.0, Anim(0.0))
    txt.setIntensity(1.0, Anim(0.0))

    uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
    sleep(2.5)
    feat(ins, "setIntensity", 1.0, Anim(1.0))

    CASES = [
        (Vec(0.0, 0.0, 0.0), "A  HPR(0,0,0)"),
        (Vec(0.0, 90.0, 0.0), "B  HPR(0,90,0)"),
        (Vec(KOURU_LON, 90.0, 0.0), "C  HPR(경도,90,0)"),
        (Vec(-KOURU_LON, 90.0, 0.0), "D  HPR(-경도,90,0)"),
        (Vec(90.0, 90.0, 0.0), "E  HPR(90,90,0)"),
    ]
    for hpr, label in CASES:
        feat(ins, "setOrientationHPR", hpr, Anim(0.0))
        txt.setText(label + "  -  하늘을 향해 곧게 섰나?")
        print("   %s" % label)
        sleep(9.0)

    txt.setText("어느 글자일 때 로켓이 지구 밖으로 곧게 섰는지 알려 주세요")
    sleep(6.0)
    uni.setGlobalIntensity(0.0, Anim.cubic(2.0))
    sleep(2.5)

print("=" * 66)
print("정답 HPR 을 알려 주시면 쇼의 ROCKET_HPR 에 넣습니다.")
print("")
print("⚠️ 발사대(런치 패드)는 안 만들었습니다 — 이유:")
print("   쇼의 Scene 1 은 고도 3,800km 에서 시작합니다. 지상 구조물은 그 높이에서 점도 안 됩니다.")
print("   지면에 붙여 보여주려면 카메라를 지표(R≈1.0)까지 내려야 하는데,")
print("   그 구도는 이 엔진에서 검증된 적이 없습니다(Terrain View 는 오퍼레이터 수동).")
print("   원하시면 '발사대 클로즈업'을 별도 장면으로 시도해 보겠습니다 — 다만 실패 가능성이 있습니다.")
print("=" * 66)

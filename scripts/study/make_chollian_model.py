# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 확인 (2026-08-12) — 돔 실행. `chollian.osg` `Loaded`, radius 5.27 m,
#        모양 확인(사용자 "모델링은 잘했네"), 궤도 배율은 **×1e6** 채택.
#  ✅ 색 확정 (2026-08-12) — **`Material { diffuseColor }` 방식이 통한다**(사용자 화면 확인).
#     `ColorArray` 만으로는 안 먹는다(조명이 켜져 있어 재질 기본 흰색이 이긴다).
#     → `chollian.osg` 를 Material 판으로 굳혔다. 쇼는 파일명 그대로 쓴다.
#        ⚠️ `.obj` 는 인코딩 사고로 안 만들어졌었다 → 이 판에서 ASCII 가드로 수정(재확인 필요).
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  [2단계] 천리안 1호 3D 모델 만들기
#
#  프로브 v2 로 확정된 것 (2026-08-12 사용자 실행)
#    · 유저 폴더 모델 1,282개 중 **천리안은 0개** → 우리가 만든다
#    · 자작 모델 obj/stl/osg 전부 로드됨. **모델 단위 = 미터, setScale = 순수 배율**
#      (근거: 반지름 1.732 상자를 ×1e7 하니 화면에서 17,321 km = 지구 2.7배로 보였다)
#    · **물체형은 바깥에서 보인다** — 지구 EquatorialJ2000 포트에 붙여 궤도에 놓은 상자가 또렷했다.
#      (블랙홀이 안 보였던 건 그 모델이 몰입형 셸이어서지 Insert3D 한계가 아니다)
#    · ⚠️ 큰 모델은 `sleep` 고정으로 기다리면 `Loading` 인 채로 지나간다 → **폴링해야 한다**
#
#  이 스크립트가 하는 일
#    ① 천리안 1호를 **세 포맷으로** 유저 폴더에 쓴다
#       (스키마 위험 분산: 색+법선 osg / 색만 osg / obj+mtl)
#    ② 셋 다 로드해 보고 어느 게 살아있는지 판정
#    ③ 살아있는 걸로 **가까이서 모양 확인** → 모양이 마음에 드는지 보는 게 목적
#    ④ 이어서 정지궤도에 놓고 배율 3단(×1e5 / 3e5 / 1e6) → 쇼에 쓸 배율 결정
#
#  천리안 1호(COMS-1) 실루엣 — 어린이·가족 관람객용이라 정밀 재현보다 **알아보기 쉽게**
#    · 본체 상자 + **한쪽에만 있는 태양전지판**(천리안 1호의 특징: 비대칭 단일 날개)
#    · 지구를 향한 큰 통신 안테나 접시
#    · 반대쪽 짧은 마스트
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *
import os
import math

RUN_WRITE = True     # ① 파일 쓰기
RUN_LOAD = True      # ② 로드 판정
RUN_LOOK = True      # ③ 가까이서 모양 확인
RUN_ORBIT = True     # ④ 정지궤도 배율 결정

EARTH_R_M = 6378137.0
GEO_R = 42164000.0 / EARTH_R_M      # 6.611 지구반지름

# ⚠️⚠️ [2026-08-12 사용자 실측] **궤도 위 물체는 구도를 맞춰야 보인다.**
#   프로브 v2 D 는 검증된 궤도 조망 구도(B=35, R=12)로 잡았는데 **위성이 안 보였다.**
#   사용자가 직접 카메라를 돌리자 보였고, 그때 HUD 가 **L 0 / B 90 / R 131,247 km**(=20.6 지구반지름).
#   → 크기가 아니라 **프레이밍** 문제였다. 정지궤도(6.6 지구반지름)는 R=12 옆구리 구도에서는
#     화면 밖으로 밀린다. **북극 위(B≈88)에서 R≈20 이면 GEO 링 전체가 한 화면에 들어온다.**
#   이 쇼의 궤도 장면은 이 구도를 기본으로 쓴다.
B_TOP = 88.0
R_TOP = 20.0

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
earth = Planet(Planet.PlanetName.Earth)

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception as e:
    print("localUserFolder 실패:", e)


def line(t):
    print("\n" + "=" * 70)
    print(t)
    print("=" * 70)


def dark(sec=0.0):
    for _ in range(max(int(sec / 0.2), 1)):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def wait_loaded(ins, timeout=12.0):
    """⚠️ 프로브 v2 교훈 — 큰 모델은 고정 sleep 으로 기다리면 Loading 인 채 지나간다."""
    t = 0.0
    while t < timeout:
        sleep(0.4)
        t += 0.4
        try:
            st = str(ins.loadingStatus)
        except Exception:
            continue
        if "Loaded" in st:
            try:
                return (st, ins.modelRadius)
            except Exception:
                return (st, None)
        if "Error" in st:
            return (st, None)
    try:
        return ("시간초과(%s)" % ins.loadingStatus, None)
    except Exception:
        return ("시간초과", None)


# ══════════════════════════════════════════════════════════════════════════
#  기하 — 삼각형 목록으로 만든다. 각 조각은 (이름, 색, [(정점3, 법선)])
# ══════════════════════════════════════════════════════════════════════════
def box(cx, cy, cz, sx, sy, sz):
    """중심 (cx,cy,cz), 크기 (sx,sy,sz) 상자 → 삼각형 12개."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    x0, x1 = cx - hx, cx + hx
    y0, y1 = cy - hy, cy + hy
    z0, z1 = cz - hz, cz + hz
    faces = [
        ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1)),
        ([(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)], (0, 0, -1)),
        ([(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)], (1, 0, 0)),
        ([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1, 0, 0)),
        ([(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)], (0, 1, 0)),
        ([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], (0, -1, 0)),
    ]
    tris = []
    for q, n in faces:
        tris.append(((q[0], q[1], q[2]), n))
        tris.append(((q[0], q[2], q[3]), n))
    return tris


def dish(cx, cy, cz, radius, depth, seg=18):
    """+Z 를 향해 열린 얕은 접시(원뿔). 안테나용."""
    tris = []
    apex = (cx, cy, cz - depth)
    for i in range(seg):
        a0 = 2.0 * math.pi * i / seg
        a1 = 2.0 * math.pi * (i + 1) / seg
        p0 = (cx + radius * math.cos(a0), cy + radius * math.sin(a0), cz)
        p1 = (cx + radius * math.cos(a1), cy + radius * math.sin(a1), cz)
        # 바깥(뒤)면과 안(오목)면을 둘 다 넣어 어느 쪽에서 봐도 보이게 한다
        nx = math.cos((a0 + a1) / 2.0) * 0.5
        ny = math.sin((a0 + a1) / 2.0) * 0.5
        tris.append(((apex, p0, p1), (nx, ny, 0.8)))
        tris.append(((apex, p1, p0), (-nx, -ny, -0.8)))
    return tris


#  ── 천리안 1호 조립 (단위 = 미터, 실제 치수에 가깝게) ──────────────
#     +Z = 지구를 향하는 면(안테나 쪽) / +X = 태양전지판이 뻗는 쪽
#  ⚠️ 색 배합 = 실제 정지궤도 위성의 전형: **금색 단열재(MLI) 본체 + 짙은 남색 태양전지판 +
#     흰 안테나 접시**. 어린이가 한눈에 '위성'으로 알아보는 조합이다.
GOLD   = (0.86, 0.68, 0.24)     # 다층 단열재 — 실제 위성의 금박
NAVY   = (0.10, 0.14, 0.36)     # 태양전지 셀 — 실제로 짙은 남색이다
SILVER = (0.62, 0.62, 0.68)
WHITE  = (0.92, 0.92, 0.95)
DARK   = (0.22, 0.22, 0.26)

PARTS = []
PARTS.append(("body", GOLD, box(0.0, 0.0, 0.0, 2.4, 2.2, 3.0)))          # 본체 — 금색 단열재
PARTS.append(("body_belt", DARK, box(0.0, 0.0, 0.0, 2.5, 2.3, 0.35)))    # 허리 띠(디테일)
PARTS.append(("boom", SILVER, box(1.9, 0.0, 0.0, 1.4, 0.25, 0.25)))      # 태양전지판 붐
PARTS.append(("panel", NAVY, box(5.1, 0.0, 0.0, 5.0, 2.3, 0.10)))        # 전지판(한쪽만!)
PARTS.append(("panel_frame", SILVER, box(5.1, 0.0, 0.0, 5.1, 2.42, 0.05)))   # 테두리
PARTS.append(("panel_hinge", SILVER, box(5.1, 0.0, 0.0, 0.12, 2.44, 0.16)))  # 가운데 이음매
PARTS.append(("dish", WHITE, dish(0.0, 0.35, 2.30, 1.05, 0.50)))         # 통신 안테나
PARTS.append(("dish_arm", SILVER, box(0.0, 0.35, 1.75, 0.14, 0.14, 0.8)))
PARTS.append(("dish2", WHITE, dish(0.85, -0.55, 1.95, 0.42, 0.22)))      # 작은 보조 안테나
PARTS.append(("horn", DARK, box(0.0, -0.75, 1.85, 0.7, 0.7, 0.8)))       # 관측 센서(GOCI 쪽)
PARTS.append(("horn_lens", WHITE, box(0.0, -0.75, 2.28, 0.42, 0.42, 0.08)))  # 렌즈면
PARTS.append(("mast", SILVER, box(0.0, 0.0, -2.2, 0.16, 0.16, 1.4)))
PARTS.append(("nozzle", DARK, dish(0.0, 0.0, -2.95, 0.30, 0.45)))        # 추력기 노즐

written = []


def w(name, text):
    """⚠️⚠️ [2026-08-12 실측 사고] Studio 파이썬의 `open(p,"w")` 는 **cp949**(한국어 윈도우 기본
    코덱)로 쓴다. 파일 내용에 ASCII 밖 글자가 하나라도 있으면 통째로 실패한다 —
    `.obj` 가 헤더의 em-dash(—) 하나 때문에 안 만들어졌고, 그 뒤 '로드 시간초과'는
    파일이 없어서였지 obj 로더 문제가 아니었다.
    → **모델 파일 내용은 ASCII 로만 쓴다.** 한글 설명은 이 스크립트 주석에만 둔다."""
    if not USER:
        return None
    bad = [c for c in text if ord(c) > 127]
    if bad:
        print("   ✗ %s: ASCII 밖 문자 %d개(%s...) — 파일 내용은 ASCII 로만 써야 한다"
              % (name, len(bad), repr("".join(bad[:5]))))
        return None
    p = os.path.join(USER, name)
    try:
        f = open(p, "w")
        f.write(text)
        f.close()
        written.append(p)
        print("   ✓ %-26s %6d 바이트" % (name, len(text)))
        return p
    except Exception as e:
        print("   ✗ %s: %s" % (name, e))
        return None


if RUN_WRITE:
    line("① 천리안 1호 모델 쓰기 — 세 포맷")

    nt = sum(len(t) for _, _, t in PARTS)
    span = max(abs(v[0]) for _, _, ts in PARTS for tri, _ in ts for v in tri)
    print("   삼각형 %d개, X 최대 %.2f m (태양전지판 끝)" % (nt, span))

    # ⚠️⚠️ [2026-08-12 돔 실측] `ColorArray` 만으로는 **색이 안 나온다 — 전부 흰색**이다.
    #   조명이 켜져 있어 재질(Material)의 기본 흰색이 정점색을 이긴다.
    #   그래서 색을 먹이는 방식 **세 가지를 다 만들어** 어느 게 통하는지 화면으로 가른다:
    #     (a) mat   — StateSet 안에 Material{diffuseColor}   ← 가장 표준
    #     (b) cm    — Material{ColorMode DIFFUSE} + ColorArray (색배열이 diffuse 로)
    #     (c) unlit — GL_LIGHTING OFF + ColorArray            (조명을 꺼서 정점색을 그대로)
    def geom(col, tris, mode):
        verts, norms = [], []
        for tri, n in tris:
            for v in tri:
                verts.append("        %.4f %.4f %.4f" % v)
                norms.append("        %.4f %.4f %.4f" % n)
        if mode == "unlit":
            st = ['      StateSet {', '        DataVariance STATIC',
                  '        GL_LIGHTING OFF', '      }']
        else:
            st = ['      StateSet {', '        DataVariance STATIC',
                  '        rendering_hint DEFAULT_BIN', '        renderBinMode INHERIT',
                  '        GL_LIGHTING ON',
                  '        Material {', '          DataVariance STATIC',
                  '          ColorMode %s' % ("DIFFUSE" if mode == "cm" else "OFF"),
                  '          ambientColor %.3f %.3f %.3f 1' % tuple(c * 0.35 for c in col),
                  '          diffuseColor %.3f %.3f %.3f 1' % col,
                  '          specularColor 0.10 0.10 0.10 1',
                  '          emissionColor %.3f %.3f %.3f 1' % tuple(c * 0.12 for c in col),
                  '          shininess 16', '        }', '      }']
        return (['    Geometry {', '      DataVariance DYNAMIC',
                 '      useDisplayList TRUE', '      useVertexBufferObjects FALSE'] + st +
                ['      PrimitiveSets 1', '      {',
                 '        DrawArrays TRIANGLES 0 %d' % len(verts), '      }',
                 '      VertexArray Vec3Array %d' % len(verts), '      {'] + verts +
                ['      }', '      NormalBinding PER_VERTEX',
                 '      NormalArray Vec3Array %d' % len(norms), '      {'] + norms +
                ['      }', '      ColorBinding OVERALL', '      ColorArray Vec4Array 1',
                 '      {', '        %.3f %.3f %.3f 1' % col, '      }', '    }'])

    for mode, fname in (("mat", "chollian_mat.osg"), ("cm", "chollian_cm.osg"),
                        ("unlit", "chollian_unlit.osg")):
        body = []
        for nm, col, tris in PARTS:
            body += geom(col, tris, mode)
        osg = (['Geode {', '  DataVariance DYNAMIC', '  name "chollian1"',
                '  nodeMask 0xffffffff', '  cullingActive TRUE',
                '  num_drawables %d' % len(PARTS)] + body + ['}'])
        w(fname, "\n".join(osg) + "\n")

    # ★ [2026-08-12 확정] **Material 방식이 통한다** — 사용자가 화면에서 색을 확인했다.
    #   그래서 쇼가 쓰는 `chollian.osg` 를 **Material 판 그대로** 쓴다(대조군은 없앴다).
    body = []
    for nm, col, tris in PARTS:
        body += geom(col, tris, "mat")
    osg = (['Geode {', '  DataVariance DYNAMIC', '  name "chollian1"',
            '  nodeMask 0xffffffff', '  cullingActive TRUE',
            '  num_drawables %d' % len(PARTS)] + body + ['}'])
    w("chollian.osg", "\n".join(osg) + "\n")

# ══ ② 어느 포맷이 살아있나 ════════════════════════════════════
GOOD = None
if RUN_LOAD and USER:
    line("② 로드 판정 — 폴링으로 (고정 sleep 은 Loading 인 채 지나간다)")
    for nm in ("chollian_mat.osg", "chollian_cm.osg", "chollian_unlit.osg", "chollian.osg"):
        p = os.path.join(USER, nm)
        try:
            ins = Insert3D(Insert3D.Insert3DName(3))
            ins.setModelFilename(p)
            st, rad = wait_loaded(ins, 12.0)
            ok = "Loaded" in st
            print("%s %-22s status=%-16s radius=%s" % ("✅" if ok else "❌", nm, st, rad))
            if ok and GOOD is None:
                GOOD = (p, rad)
        except Exception as e:
            print("❌ %-22s 예외: %s" % (nm, e))
    print("\n판정: %s" % ("쓸 모델 = %s (반지름 %.2f m)" % (os.path.basename(GOOD[0]), GOOD[1])
                        if GOOD else "셋 다 실패 — 스키마를 다시 짜야 한다"))


# ══ ③ 가까이서 모양 확인 ═══════════════════════════════════════
#   쇼에 넣기 전에 **모양이 천리안처럼 보이는지** 사람이 봐야 한다.
#   ⚠️ 카메라를 옮겨 다가가는 대신 **모델을 키운다** — 구도를 한 번만 잡고 건드리지 않는다.
#      (프레이밍이 어긋나면 아무것도 안 보인다는 걸 D 에서 배웠다. 지상 쇼 setScale 규칙과 같은 논리.)
#      모델은 지구 중심에 두고 지구는 꺼서, 위성만 화면에 남긴다.
def frame_earth():
    """FadeTo 지구 → 북극 위 조망. 사용자가 찾은 구도(B≈90, R≈20)를 고정으로 쓴다."""
    dark()
    SceneGraph().reset(1)
    dark(1.6)
    h = DataManager.database().data(Data.Type.PlanetType, "Earth")
    if h is not None:
        a = h.action(Action.Type.FadeTo)
        if a is not None:
            a.trigger()
    for _ in range(22):                       # FadeTo 진행 내내 암전 유지
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(0.2)
    for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                  ("setPlanetShineStrength", 1.0)):
        try:
            getattr(earth, fn)(v, Anim(0.0))
        except Exception:
            pass
    dark()
    cam.setPositionLBR(Vec(0.0, B_TOP, R_TOP), Anim(0.0), -1)
    dark()
    cam.setTargetHeight(30.0, Anim(0.0))
    dark()


def sub():
    """⚠️⚠️ [2026-08-12 돔 실측] 행성 프레임 자막은 **setSize 를 부르면 화면에서 사라진다.**
    (천리안 쇼 v1 이 이걸로 우주 장면 4분간 자막을 못 띄웠다.)
    지상 = size 0.052 + distance 1.0 / 우주 = 크기를 만지지 말고 distance 20."""
    t = InsertText(InsertText.InsertTextName(1))
    cam.addChild(t.id, Camera.CameraPort.FixedForeground)
    t.setPosition(Vec(0, 14, 0))
    t.setColor(Vec(1.0, 1.0, 0.6))
    t.setDistance(20.0, Anim(0.0))            # 행성 프레임 자막 = distance 20, setSize 없음
    t.setIntensity(1.0, Anim(0.0))
    return t


if RUN_LOOK and GOOD:
    line("③ 모양 확인 — 위성만 크게 띄워 세 방향")
    try:
        frame_earth()
        earth.setIntensity(0.0, Anim(0.0))    # 지구를 꺼서 위성만 남긴다
        Stars(Stars.StarsName.StarrySky).setIntensity(0.2, Anim(0.0))
        Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))
        dark()

        ins = Insert3D(Insert3D.Insert3DName(3))
        ins.setModelFilename(GOOD[0])
        wait_loaded(ins, 12.0)
        ins.setIntensity(1.0, Anim(0.0))
        try:
            ins.setShadowStrength(0.0, Anim(0.0))     # 반쪽이 어두우면 모양이 안 보인다
        except Exception:
            pass
        try:
            ins.setParent(earth.portId(Planet.PlanetPort.EquatorialJ2000))
            ins.setPositionLBR(Vec(0.0, 0.0, 0.0), Anim(0.0))   # 지구 중심 = 화면 한가운데
        except Exception as e:
            print("   배치 실패:", e)
        try:
            print("   parentRadius =", ins.parentRadius)   # 이 프레임의 길이 단위(m)를 직접 읽는다
        except Exception:
            pass
        dark()

        # 화면을 반쯤 채우도록 배율을 **역산**한다 (하드코딩하지 않는다)
        SCALE = 0.45 * R_TOP * EARTH_R_M / GOOD[1]
        try:
            ins.setScale(SCALE, Anim(0.0))
        except Exception:
            ins.setScale(SCALE)
        print("   scale ×%.2e → 반지름 %.0f km (카메라 R=%.0f km)"
              % (SCALE, GOOD[1] * SCALE / 1000.0, R_TOP * EARTH_R_M / 1000.0))

        txt = sub()
        dark()

        # ⚠️ 전 판은 **한 모델만** 세 각도로 보여줬다("모델 3개 보낸 거 맞아?" 지적).
        #    이제 각 각도마다 이름표를 붙여 무엇을 보고 있는지 분명히 한다.
        for label, hpr in (("정면 — 안테나 쪽", (0.0, 0.0, 0.0)),
                           ("옆 — 태양전지판", (90.0, 0.0, 0.0)),
                           ("비스듬히", (140.0, 25.0, 0.0))):
            try:
                dark()
                try:
                    ins.setOrientationHPR(Vec(*hpr), Anim(0.0))
                except Exception:
                    ins.setOrientationHPR(Vec(*hpr))
                dark()
                sleep(0.5)
                txt.setText("천리안 1호 — %s" % label)
                uni.setGlobalIntensity(1.0, Anim.cubic(1.0))
                print("   >>> %s  HPR=%s" % (label, hpr))
                sleep(7.0)
            except Exception as e:
                print("   %s 실패: %s" % (label, e))
        dark()
        earth.setIntensity(1.0, Anim(0.0))
    except Exception as e:
        print("③ 오류:", e)


# ══ ④ 정지궤도 배율 결정 ═══════════════════════════════════════
if RUN_ORBIT and GOOD:
    line("④ 정지궤도 배치 — 쇼에 쓸 배율 고르기 (북극 위 구도)")
    try:
        frame_earth()
        try:
            op = OrbitalPlace(OrbitalPlace.OrbitalPlaceName.OrbitalPlace001)
            op.setParent(earth.portId(Planet.PlanetPort.EquatorialJ2000))
            op.setMeanMotion(1.0027, Anim(0.0))
            op.setEccentricity(0.0002, Anim(0.0))
            op.setInclination(0.1, Anim(0.0))
            op.setAscendingNodeLongitude(0.0, Anim(0.0))
            op.setArgumentOfPeriapsis(0.0, Anim(0.0))
            op.setMeanAnomaly(0.0, Anim(0.0))
            sleep(0.4)
            op.setOrbitColor(Vec(1.0, 0.75, 0.25))
            op.setOrbitThickness(1.5)
            op.setOrbitIntensity(0.9, Anim(0.0))
        except Exception as e:
            print("   궤도선 실패:", e)
        dark()

        ins = Insert3D(Insert3D.Insert3DName(4))
        ins.setModelFilename(GOOD[0])
        wait_loaded(ins, 12.0)
        ins.setIntensity(1.0, Anim(0.0))
        try:
            ins.setShadowStrength(0.0, Anim(0.0))
        except Exception:
            pass
        try:
            ins.setParent(earth.portId(Planet.PlanetPort.EquatorialJ2000))
            ins.setPositionLBR(Vec(0.0, 0.0, GEO_R), Anim(0.0))
        except Exception as e:
            print("   배치 실패:", e)
        dark()

        txt = sub()
        dark()

        # ⚠️ 화면이 R=20 지구반지름(127,563 km)이니 위성이 '점'이 되지 않으려면 수천 km 는 돼야 한다.
        #    실제 8m 위성을 그만큼 키우는 건 물리적으로 거짓말이지만, 안 키우면 아예 안 보인다.
        #    (교육 돔의 관례 — 위성 아이콘을 과장해 그린다. 나레이션에서 실제 크기를 말해 준다.)
        for mul in (3.0e5, 1.0e6, 3.0e6):
            try:
                dark()
                km = GOOD[1] * mul / 1000.0
                try:
                    ins.setScale(mul, Anim(0.0))
                except Exception:
                    ins.setScale(mul)
                sleep(0.5)
                txt.setText("×%.0e — 반지름 %.0f km (지구의 %.2f배)" % (mul, km, km / 6378.0))
                uni.setGlobalIntensity(1.0, Anim.cubic(1.0))
                print("   >>> ×%.0e → %.0f km (지구의 %.2f배)" % (mul, km, km / 6378.0))
                sleep(8.0)
            except Exception as e:
                print("   ×%.0e 실패: %s" % (mul, e))

        txt.setText("어느 배율이 보기 좋았나요")
        sleep(5.0)
        txt.setIntensity(0.0, Anim(1.5))
        sleep(1.5)
    except Exception as e:
        print("④ 오류:", e)


line("모델 제작 종료 — 알려주세요")
print("색은 확정됐다 — Material 방식. chollian.osg 가 그 판으로 덮어써졌으니")
print("이제 쇼(SHOW_chollian.py)를 그대로 돌리면 색이 들어간 천리안이 나온다.")
print("")
print("1) 모양이 나아졌나 — 허리띠·보조안테나·렌즈면·추력기 노즐을 더 넣었다")
print("2) 배색이 괜찮나 — 본체 금색(단열재) / 전지판 짙은 남색 / 접시 흰색")
print("3) ④ 궤도 위 크기가 적당한 배율 (×3e5 / 1e6 / 3e6)")
print("만든 파일 %d개:" % len(written))
for p in written:
    print("   ", p)

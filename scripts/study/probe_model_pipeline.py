# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 이 파일 자체가 검증 도구다. 돌리고 나온 로그가 곧 결과다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  [프로브] 3D 모델 파이프라인 뚫기 — "우리가 만든 모델을 넣을 수 있는가"
#
#  목적: 천리안 1호 쇼(5분)를 만들려면 위성 3D 모델이 필요한데,
#        지금 저장소에 **로드 성공이 기록된 .osg 는 블랙홀 하나뿐**이고
#        위성/우주선 모델의 존재 여부는 근거가 전혀 없다.
#        그런데 프로덕션 SPC 코퍼스에는 **쇼와 함께 동봉된 모델**이 나온다:
#          · studio/9bf98da1b97641f7b7fe1d2abf94a75f/0/Load_Oumuamua_v1_Rock.osg
#          · modelHH111-animated.osg
#        게다가 API 문서는 setModelFilename 을 이렇게 규정한다:
#          "3D model file path. **Must be a relative file path to user.**"
#        → 유저 폴더에 우리가 만든 모델을 넣는 길이 열려 있을 가능성이 크다. 그걸 확인한다.
#
#  이 프로브가 답하는 것 (순서대로)
#    ① 경로 기준점 — `..\data\...` 는 무엇에 상대인가
#    ② 이미 있는 모델 — 위성/우주선 모델이 혹시 있나 (있으면 만들 필요가 없다)
#    ③ ★가장 중요 — **우리가 만든 모델이 로드되는가.** obj / stl / osg 세 포맷을 시험한다
#    ④ 물체형 모델이 **바깥에서 보이는가** (블랙홀은 R≈0 에서만 보였다.
#       그게 모델 고유 성질인지 Insert3D 일반 성질인지 아직 모른다 — 여기서 갈린다)
#
#  ⚠️ 이 프로브는 파일을 **쓴다**(유저 폴더에 테스트 모델 3개). 그래야 사용자가
#     파일을 손으로 복사하는 단계가 없어진다. 지우고 싶으면 아래 파일명으로 지우면 된다.
#
#  단계별로 끌 수 있다 — 문제가 생기면 해당 RUN_* 를 False 로.
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *
import os

RUN_WALK = True         # ② 기존 모델 전수 조사 (느리면 False)
RUN_WRITE = True        # ③-a 테스트 모델 파일 쓰기
RUN_LOAD = True         # ③-b 로드 시도
RUN_VIEW = True         # ④ 바깥 조망 확인

WALK_MAX_FILES = 400    # 안전장치 — 디스크 전체를 훑지 않는다
WALK_MAX_DEPTH = 6

MODEL_EXT = (".osg", ".osgt", ".osgb", ".ive", ".obj", ".stl", ".dae", ".3ds", ".ply")
WANT = ("satell", "spacecraft", "probe", "orbiter", "craft", "station", "rocket",
        "coms", "chollian", "sonde", "iss", "hubble", "voyager", "cassini")

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)


def line(t):
    print("\n" + "=" * 68)
    print(t)
    print("=" * 68)


# ══ ① 경로 기준점 ═════════════════════════════════════════════
line("① 경로 기준점")
USER = ""
try:
    USER = Configuration.configuration().localUserFolder
    print("localUserFolder =", USER)
except Exception as e:
    print("localUserFolder 실패:", e)
try:
    print("os.getcwd()     =", os.getcwd())
except Exception as e:
    print("getcwd 실패:", e)

# 블랙홀이 쓰는 상대경로가 실제로 어디를 가리키는지 되짚어 본다
KNOWN = "..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg"
for base in (".", "..", USER):
    if not base:
        continue
    p = os.path.normpath(os.path.join(base, KNOWN.replace("\\", "/")))
    try:
        print("   %-6s 기준 → %s  존재=%s" % (base, p, os.path.exists(p)))
    except Exception as e:
        print("   %s 확인 실패: %s" % (base, e))


# ══ ② 이미 있는 모델 전수 조사 ════════════════════════════════
found = []
if RUN_WALK:
    line("② 기존 3D 모델 전수 조사")
    roots = [r for r in (".", "..", "../data", "../data/scene", USER) if r]
    seen = set()
    for root in roots:
        try:
            root_abs = os.path.abspath(root)
        except Exception:
            continue
        if root_abs in seen:
            continue
        seen.add(root_abs)
        base_depth = root_abs.rstrip("/\\").count(os.sep)
        try:
            for dirpath, dirnames, filenames in os.walk(root_abs):
                if dirpath.count(os.sep) - base_depth > WALK_MAX_DEPTH:
                    dirnames[:] = []
                    continue
                for fn in filenames:
                    if fn.lower().endswith(MODEL_EXT):
                        found.append(os.path.join(dirpath, fn))
                        if len(found) >= WALK_MAX_FILES:
                            break
                if len(found) >= WALK_MAX_FILES:
                    break
        except Exception as e:
            print("   walk 실패 %s: %s" % (root_abs, e))
        if len(found) >= WALK_MAX_FILES:
            print("   ⚠️ %d개에서 중단(안전장치)" % WALK_MAX_FILES)
            break

    print("발견한 모델 파일: %d개" % len(found))
    hits = [p for p in found if any(w in os.path.basename(p).lower() for w in WANT)]
    print("\n★ 위성/우주선 키워드 일치: %d개" % len(hits))
    for p in hits[:20]:
        print("   ", p)
    print("\n(참고) 전체 목록 앞 40개:")
    for p in found[:40]:
        print("   ", p)


# ══ ③-a 테스트 모델 만들기 ════════════════════════════════════
#   정점 8개짜리 상자를 세 포맷으로 쓴다. 어느 포맷이 읽히는지가
#   곧 '우리가 모델을 만들어 넣을 수 있는 경로'다.
V = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
     (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
QUADS = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
TRIS = []
for a, b, c, d in QUADS:
    TRIS.append((a, b, c))
    TRIS.append((a, c, d))

written = []
if RUN_WRITE and USER:
    line("③-a 테스트 모델 쓰기")

    def w(name, text):
        p = os.path.join(USER, name)
        try:
            f = open(p, "w")
            f.write(text)
            f.close()
            written.append(p)
            print("   ✓ %s (%d 바이트)" % (p, len(text)))
            return p
        except Exception as e:
            print("   ✗ %s: %s" % (name, e))
            return None

    # OBJ — 평문이라 가장 확실하게 작성 가능
    obj = ["# probe test box"]
    for x, y, z in V:
        obj.append("v %g %g %g" % (x, y, z))
    for q in QUADS:
        obj.append("f %d %d %d %d" % (q[0] + 1, q[1] + 1, q[2] + 1, q[3] + 1))
    w("probe_box.obj", "\n".join(obj) + "\n")

    # STL(ASCII) — 삼각형만. 역시 손으로 쓰기 쉬운 포맷
    stl = ["solid probebox"]
    for a, b, c in TRIS:
        stl.append("facet normal 0 0 0")
        stl.append("  outer loop")
        for i in (a, b, c):
            stl.append("    vertex %g %g %g" % V[i])
        stl.append("  endloop")
        stl.append("endfacet")
    stl.append("endsolid probebox")
    w("probe_box.stl", "\n".join(stl) + "\n")

    # OSG(ASCII 네이티브) — 스키마가 까다로워 실패 가능성이 셋 중 가장 높다
    verts = []
    for a, b, c in TRIS:
        for i in (a, b, c):
            verts.append("      %g %g %g" % V[i])
    osg = [
        'Geode {',
        '  DataVariance DYNAMIC',
        '  name "probebox"',
        '  nodeMask 0xffffffff',
        '  cullingActive TRUE',
        '  num_drawables 1',
        '  Geometry {',
        '    DataVariance DYNAMIC',
        '    useDisplayList TRUE',
        '    useVertexBufferObjects FALSE',
        '    PrimitiveSets 1',
        '    {',
        '      DrawArrays TRIANGLES 0 %d' % len(verts),
        '    }',
        '    VertexArray Vec3Array %d' % len(verts),
        '    {',
    ] + verts + [
        '    }',
        '    ColorBinding OVERALL',
        '    ColorArray Vec4Array 1',
        '    {',
        '      1 1 1 1',
        '    }',
        '  }',
        '}',
    ]
    w("probe_box.osg", "\n".join(osg) + "\n")
elif RUN_WRITE:
    print("\n⚠️ localUserFolder 를 못 읽어 테스트 모델을 쓸 수 없다 — ③ 건너뜀")


# ══ ③-b 로드 시도 ═════════════════════════════════════════════
ok_model = None
ok_radius = None
if RUN_LOAD:
    line("③-b 로드 시도 — 어느 포맷이 읽히나")
    ins = None
    try:
        ins = Insert3D(Insert3D.Insert3DName(0))
    except Exception as e:
        print("Insert3D 생성 실패:", e)

    # 유저폴더 상대(파일명만) / 절대경로 두 형식을 다 시험한다.
    # API 문서는 "relative to user" 라고 하지만 블랙홀은 ..\data\ 로 동작한다 — 규약이 불분명.
    cands = []
    for nm in ("probe_box.obj", "probe_box.stl", "probe_box.osg"):
        cands.append((nm + "  [유저폴더 상대]", nm))
        if USER:
            cands.append((nm + "  [절대경로]", os.path.join(USER, nm)))
    cands.append(("블랙홀(대조군 — 이건 되는 게 확인됨)", KNOWN))

    if ins is not None:
        for label, path in cands:
            try:
                ins.setModelFilename(path)
                sleep(1.2)
                st = str(ins.loadingStatus)
                rad = None
                try:
                    rad = ins.modelRadius
                except Exception:
                    pass
                mark = "✅" if "Loaded" in st else "❌"
                print("%s %-38s status=%-28s radius=%s" % (mark, label, st, rad))
                if "Loaded" in st and "블랙홀" not in label and ok_model is None:
                    ok_model, ok_radius = path, rad
            except Exception as e:
                print("❌ %-38s 예외: %s" % (label, e))

    print("\n판정: %s" % ("우리가 만든 모델 로드 성공 → %s" % ok_model if ok_model
                        else "자작 모델은 셋 다 실패 (기존 모델로 대역하거나 방향 재검토)"))


# ══ ④ 바깥에서 보이는가 ═══════════════════════════════════════
#   블랙홀은 R≈0 에서만 보였다. 그게 그 모델 성질인지 Insert3D 일반 성질인지 모른다.
#   물체형이 바깥 조망이 되어야 '위성이 도는 걸 보여주는' 연출이 가능하다.
if RUN_VIEW and ok_model:
    line("④ 바깥 조망 — 모델이 밖에서 보이나")
    try:
        uni.setGlobalIntensity(0.0, Anim(0.0))
        SceneGraph().reset(1)
        for _ in range(8):
            uni.setGlobalIntensity(0.0, Anim(0.0))
            sleep(0.2)

        Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
        Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))

        ins = Insert3D(Insert3D.Insert3DName(0))
        ins.setModelFilename(ok_model)
        sleep(1.2)
        ins.setIntensity(1.0, Anim(0.0))
        print("   재로드 status =", ins.loadingStatus, " radius =", ins.modelRadius)

        # 홀더 프레임에 붙인다. 포트 이름은 클래스마다 달라 폴백으로 찾는다(블랙홀 교훈).
        holder = Place2D(Place2D.Place2DName(0))
        pport = None
        for pn in ("CenteredPort", "Centered", "LocalPort"):
            try:
                pport = holder.portId(getattr(Place2D.Place2DPort, pn))
                print("   포트 OK:", pn)
                break
            except Exception:
                continue
        if pport is None:
            print("   ⚠️ Place2D 포트를 못 찾음 — 부착 없이 진행")
        else:
            try:
                ins.setParent(pport)
            except Exception as e:
                print("   setParent 실패:", e)

        txt = InsertText(InsertText.InsertTextName(1))
        cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
        txt.setPosition(Vec(0, 14, 0))
        txt.setColor(Vec(1.0, 1.0, 0.6))
        txt.setDistance(1.0, Anim(0.0))
        txt.setIntensity(1.0, Anim(0.0))

        R0 = ok_radius if ok_radius else 1.0
        for mul in (5.0, 2.0, 0.5, 0.05):
            try:
                uni.setGlobalIntensity(0.0, Anim(0.0))
                if pport is not None:
                    cam.setPositionLBR(Vec(0.0, 0.0, R0 * mul), Anim(0.0), pport)
                cam.setTargetHeight(30.0, Anim(0.0))
                sleep(0.8)
                txt.setText("R = modelRadius × %g  — 상자가 보이나요?" % mul)
                uni.setGlobalIntensity(1.0, Anim.cubic(1.2))
                print("   >>> R = radius × %g  (= %s)" % (mul, R0 * mul))
                sleep(9.0)
            except Exception as e:
                print("   배율 %g 실패: %s" % (mul, e))

        txt.setText("어느 배율에서 보였는지 알려주세요")
        sleep(5.0)
        txt.setIntensity(0.0, Anim(1.5))
        sleep(1.5)
    except Exception as e:
        print("④ 구간 오류:", e)
elif RUN_VIEW:
    print("\n④ 건너뜀 — 로드 성공한 자작 모델이 없다")


line("프로브 종료 — 아래를 알려주세요")
print("1) ② 에서 위성/우주선 모델이 나왔는지 (나왔으면 경로)")
print("2) ③ 에서 ✅ 가 뜬 포맷이 무엇인지 (obj / stl / osg / 없음)")
print("3) ④ 에서 상자가 보인 배율 (× 5 / 2 / 0.5 / 0.05 / 전부 안 보임)")
print("")
print("만든 테스트 파일 %d개 — 필요 없으면 지우면 됩니다:" % len(written))
for p in written:
    print("   ", p)

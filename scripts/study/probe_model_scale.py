# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  검증: 미확인 — 이 파일 자체가 검증 도구다. 돌리고 나온 로그·화면이 곧 결과다.
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════
#  [프로브 v2] 3D 모델 — "단위를 맞추면 밖에서 보이는가"
#
#  v1 결과 (사용자 실행, 2026-08-12)
#    ① 경로 기준점 = localUserFolder (D:/SkyExplorer-Data/user). ..\data\ 는 그 부모로 올라간다. ✅
#    ② 유저 폴더에 우주선 모델이 이미 많다 (cassini.osg / ISS .osg / .ive / .3DS 다수) ✅
#    ③ 자작 모델 obj·stl·osg **세 포맷 전부 Loaded**, radius=1.7320508=√3 (2×2×2 상자 정답) ✅
#    ④ 바깥 조망 = 상자가 안 보였다 ❌
#
#  ★ ④ 는 엔진 한계가 아니라 **내 단위 실수**로 보인다.
#    HUD 실측: R = radius×5 = 8.66 일 때 **55,236 km**.
#      55236 / 8.66 = **6,378 km = 지구 반지름**.
#    → 이 프레임의 카메라 R 단위 = 지구반지름. 그런데 modelRadius(1.732)는 **미터**다.
#      즉 3.5m 짜리 상자를 5만 km 밖에서 본 것. 안 보이는 게 당연하다.
#
#  ⚠️ 그리고 같은 실수를 **옛 블랙홀 프로브도 했을 것이다.**
#     지식베이스의 "블랙홀은 몰입형이라 바깥 조망 불가(R≥0.05×modelRadius 에서 안 보임)" 는
#     0.05 × 4.85e7 = 242만을 **포트 단위(지구반지름)** 로 넣은 것 = 2.4e6 지구반지름 = 은하 밖.
#     안 보이는 게 당연하다. → **이 프로브의 C 단계가 그 확정 노트를 재판한다.**
#
#  가설:  R_port = modelRadius[m] / 6,378,137 × 배율
#
#  단계
#    A  천리안/COMS 모델이 폴더에 있나 (v1 은 400개 상한에 걸려 목록이 잘렸다) + Insert3D 메서드 덤프
#    B  실존 우주선 모델을 로드해 modelRadius 표 — '이 엔진이 쓰는 스케일'을 배운다
#    C  ★단위 가설 검증 — 블랙홀을 환산한 R 로 **바깥에서** 본다
#    D  ★실전 — 지구 궤도(정지궤도)에 위성 모델을 놓고 setScale 을 훑는다
#
#  ⚠️ 파일을 쓰지 않는다(v1 이 만든 probe_box.* 를 재사용). 읽기·로드·카메라만.
# ══════════════════════════════════════════════════════════════════════════
from skyExplorer import *
from studio import *
from Initialization import *
import os

RUN_FIND = True      # A 이름 탐색 + 메서드 덤프
RUN_RADIUS = True    # B 실존 모델 modelRadius 표
RUN_UNIT = True      # C 단위 가설 — 블랙홀 바깥 조망
RUN_ORBIT = True     # D 지구 궤도에 위성 배치 + setScale 스윕

EARTH_R_M = 6378137.0          # 이 프레임 R 1.0 = 지구반지름 (HUD 로 역산한 값)
GEO_R = 42164000.0 / EARTH_R_M  # 정지궤도 = 6.61 지구반지름

BLACKHOLE = "..\\data\\scene\\astronomy\\blackhole\\schwarzschild\\blackholeAccretionSharp.osg"

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
    """암전 클램프 — reset/FadeTo 는 밝기를 1.0 으로 되돌린다. 한 번만 눌러선 안 된다."""
    n = max(int(sec / 0.2), 1)
    for _ in range(n):
        uni.setGlobalIntensity(0.0, Anim(0.0))
        if sec:
            sleep(0.2)


def load(ins, path, wait=1.4):
    """모델 로드 후 (status, radius) 반환."""
    try:
        ins.setModelFilename(path)
    except Exception as e:
        return ("예외: %s" % e, None)
    sleep(wait)
    st = "?"
    rad = None
    try:
        st = str(ins.loadingStatus)
    except Exception:
        pass
    try:
        rad = ins.modelRadius
    except Exception:
        pass
    return (st, rad)


# ══ A. 천리안 탐색 + Insert3D 메서드 덤프 ══════════════════════
CHOLLIAN = None
SPACECRAFT = []
if RUN_FIND:
    line("A. 천리안/COMS 탐색  +  Insert3D 메서드 덤프")

    # v1 은 모든 모델파일을 모으다 400개에서 잘렸다. 이번엔 '이름만' 보고 지나간다 — 상한 없음.
    KEY = ("chollian", "cheollian", "coms", "cheonrian", "천리안",
           "gk2", "geo-kompsat", "geokompsat", "kompsat", "geostat")
    EXT = (".osg", ".osgt", ".osgb", ".ive", ".obj", ".stl", ".dae", ".3ds", ".ply")
    SHIP = ("satell", "spacecraft", "probe", "orbiter", "craft", "station",
            "rocket", "cassini", "iss", "hubble", "voyager", "shuttle", "apollo")

    total = 0
    hits = []
    if USER:
        try:
            for dirpath, dirnames, filenames in os.walk(USER):
                for fn in filenames:
                    low = fn.lower()
                    if not low.endswith(EXT):
                        continue
                    total += 1
                    full = os.path.join(dirpath, fn)
                    blob = (dirpath + "/" + fn).lower()
                    if any(k in blob for k in KEY):
                        hits.append(full)
                    # 프로덕션 포맷(.osg/.ive)의 우주선만 따로 모은다 — 스케일 학습용
                    if low.endswith((".osg", ".ive")) and any(s in blob for s in SHIP):
                        SPACECRAFT.append(full)
        except Exception as e:
            print("   walk 실패:", e)

    print("유저 폴더 전체 모델 파일: %d개 (상한 없이 전수)" % total)
    print("\n★ 천리안/COMS/천리안2 계열 일치: %d개" % len(hits))
    for p in hits[:20]:
        print("   ", p)
    if not hits:
        print("    → 없다. 천리안 모델은 **우리가 만들어야 한다**(v1 에서 자작 로드는 이미 성공).")

    print("\n.osg/.ive 우주선 후보: %d개" % len(SPACECRAFT))
    for p in SPACECRAFT[:12]:
        print("   ", p)

    # Insert3D 가 실제로 무엇을 할 수 있는지 — 지식베이스에 이 클래스 기록이 거의 없다
    try:
        _i = Insert3D(Insert3D.Insert3DName(0))
        ms = [m for m in dir(_i) if m.startswith("set")]
        print("\nInsert3D set* 메서드 %d개:" % len(ms))
        print("   " + ", ".join(ms))
        rd = [m for m in dir(_i) if not m.startswith("_") and not m.startswith("set")]
        print("\nInsert3D 읽기/기타:")
        print("   " + ", ".join(rd))
    except Exception as e:
        print("Insert3D 덤프 실패:", e)


# ══ B. 실존 모델의 modelRadius — 스케일 감각 배우기 ═════════════
REAL = None       # (경로, 반지름) — D 단계에서 쓸 실존 우주선 모델
if RUN_RADIUS:
    line("B. 실존 모델 modelRadius — 이 엔진이 쓰는 스케일")
    print("(우리가 천리안을 만들 때 몇 미터짜리로 만들어야 하는지가 여기서 나온다)")
    try:
        ins = Insert3D(Insert3D.Insert3DName(1))
        cands = list(SPACECRAFT[:6])
        if USER:
            cands.append(os.path.join(USER, "probe_box.obj"))   # 대조군 = √3 인 걸 아는 모델
        cands.append(BLACKHOLE)                                  # 대조군 = 4.85e7

        for p in cands:
            st, rad = load(ins, p, 1.3)
            ok = "Loaded" in st
            name = os.path.basename(p)
            print("%s %-42s radius=%-18s %s" % ("✅" if ok else "❌", name[:42], rad, st))
            if ok and rad and REAL is None and p in SPACECRAFT:
                REAL = (p, rad)
        if REAL:
            print("\n→ D 단계에서 쓸 모델: %s (radius=%s)" % (os.path.basename(REAL[0]), REAL[1]))
    except Exception as e:
        print("B 단계 오류:", e)


# ══ C. ★단위 가설 — 블랙홀을 '밖에서' 본다 ═════════════════════
#   지식베이스: "블랙홀은 R≈0 에서만 보인다 (0.05×modelRadius 에서도 안 보임)" — 확정으로 기록돼 있다.
#   그런데 그 0.05×4.85e7 = 242만은 포트 단위(지구반지름)로 넣은 값이다 = 은하 밖.
#   가설대로 환산하면 R_port = 4.85e7/6.378e6 = 7.6 지구반지름. 배율 5면 38.
#   여기서 링이 보이면 → 단위가 원인이었고, 그 확정 노트는 틀렸다.
if RUN_UNIT:
    line("C. 단위 가설 검증 — 블랙홀 바깥 조망")
    try:
        dark()
        SceneGraph().reset(1)
        dark(1.6)

        Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
        Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.0, Anim(0.0))
        dark()

        ins = Insert3D(Insert3D.Insert3DName(0))
        st, rad = load(ins, BLACKHOLE, 1.6)
        ins.setIntensity(1.0, Anim(0.0))
        print("   블랙홀 status=%s radius=%s" % (st, rad))
        dark()

        holder = Place2D(Place2D.Place2DName(0))
        pport = None
        for pn in ("CenteredPort", "Centered", "LocalPort"):
            try:
                pport = holder.portId(getattr(Place2D.Place2DPort, pn))
                break
            except Exception:
                continue
        if pport is not None:
            try:
                ins.setParent(pport)
            except Exception as e:
                print("   setParent 실패:", e)
        dark()

        txt = InsertText(InsertText.InsertTextName(1))
        cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
        txt.setPosition(Vec(0, 14, 0))
        txt.setSize(0.05)
        txt.setColor(Vec(1.0, 1.0, 0.6))
        txt.setDistance(1.0, Anim(0.0))
        txt.setIntensity(1.0, Anim(0.0))
        dark()

        base = (rad if rad else 4.85e7) / EARTH_R_M      # = 7.6 지구반지름
        print("   환산 기준 R(지구반지름 단위) = %.4f" % base)
        for mul in (30.0, 8.0, 2.5):
            try:
                dark()
                if pport is not None:
                    cam.setPositionLBR(Vec(0.0, -30.0, base * mul), Anim(0.0), pport)
                cam.setTargetHeight(30.0, Anim(0.0))
                dark()
                sleep(0.6)
                txt.setText("블랙홀  ×%g  (R=%.2f 지구반지름)" % (mul, base * mul))
                uni.setGlobalIntensity(1.0, Anim.cubic(1.2))
                print("   >>> ×%g → R=%.3f" % (mul, base * mul))
                sleep(7.0)
            except Exception as e:
                print("   ×%g 실패: %s" % (mul, e))
        dark()
        try:
            ins.setIntensity(0.0, Anim(0.0))
        except Exception:
            pass
    except Exception as e:
        print("C 단계 오류:", e)


# ══ D. ★실전 — 정지궤도에 위성 모델을 놓는다 ════════════════════
#   천리안 쇼가 실제로 쓸 구도: FadeTo 지구 → 풀백 R=12 → 위성이 궤도에 보인다.
#   문제는 크기다. 실제 위성(수 m)은 76,000 km 밖에서 점도 안 된다 → setScale 로 키워야 한다.
#   얼마나 키워야 하는지를 여기서 잰다.
if RUN_ORBIT:
    line("D. 정지궤도 배치 + setScale 스윕 — '쇼에 쓸 수 있는가'")
    try:
        dark()
        SceneGraph().reset(1)
        dark(1.6)

        h = DataManager.database().data(Data.Type.PlanetType, "Earth")
        if h is not None:
            a = h.action(Action.Type.FadeTo)
            if a is not None:
                a.trigger()
        for _ in range(22):                 # FadeTo 진행 내내 암전 유지
            uni.setGlobalIntensity(0.0, Anim(0.0))
            sleep(0.2)

        # 그림자 OFF — 지구 반쪽이 어두우면 그 쪽 위성이 안 보인다
        for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
                      ("setPlanetShineStrength", 1.0)):
            try:
                getattr(earth, fn)(v, Anim(0.0))
            except Exception:
                pass
        dark()

        cam.setPositionLBR(Vec(0.0, 35.0, 12.0), Anim(0.0), -1)   # 검증된 궤도 조망 구도
        dark()
        cam.setTargetHeight(30.0, Anim(0.0))
        dark()

        # 참조 궤도선 — 위성이 어디쯤 있어야 하는지 눈으로 확인하기 위해
        op = None
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
            print("   GEO 궤도선 ON (참조)")
        except Exception as e:
            print("   궤도선 실패:", e)
        dark()

        # 위성 모델 — 실존 모델이 있으면 그걸, 없으면 자작 상자
        path = REAL[0] if REAL else (os.path.join(USER, "probe_box.obj") if USER else None)
        ins = Insert3D(Insert3D.Insert3DName(2))
        rad = None
        if path:
            st, rad = load(ins, path, 1.6)
            print("   위성 모델: %s  status=%s radius=%s" % (os.path.basename(path), st, rad))
        ins.setIntensity(1.0, Anim(0.0))
        dark()

        # 지구 관성 프레임에 부착 → 정지궤도 반지름에 놓는다
        try:
            ep = earth.portId(Planet.PlanetPort.EquatorialJ2000)
            ins.setParent(ep)
            print("   setParent(Earth EquatorialJ2000) OK")
        except Exception as e:
            print("   setParent 실패:", e)
        placed = False
        for args in ((Vec(0.0, 0.0, GEO_R), Anim(0.0)), (Vec(0.0, 0.0, GEO_R),)):
            try:
                ins.setPositionLBR(*args)
                placed = True
                print("   setPositionLBR(GEO=%.3f 지구반지름) OK  인자 %d개" % (GEO_R, len(args)))
                break
            except Exception as e:
                print("   setPositionLBR 인자 %d개 실패: %s" % (len(args), e))
        if not placed:
            print("   ⚠️ 위치 지정 실패 — 원점(지구 중심)에 남는다")
        dark()

        # 원본 scale 을 먼저 읽는다 (기본이 1.0 이 아닐 수 있다 — 구상성단 교훈)
        orig = 1.0
        try:
            orig = ins.scale
            print("   원본 scale = %s" % orig)
        except Exception as e:
            print("   scale 읽기 실패(1.0 가정):", e)

        txt = InsertText(InsertText.InsertTextName(1))
        cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
        txt.setPosition(Vec(0, 14, 0))
        txt.setSize(0.05)
        txt.setColor(Vec(1.0, 1.0, 0.6))
        txt.setDistance(20.0, Anim(0.0))     # 행성 프레임 자막 = distance 20
        txt.setIntensity(1.0, Anim(0.0))
        dark()

        # 얼마나 키워야 보이나. 모델이 rad 미터라면 화면에서 대략 (rad×배율/76538km) 각.
        for mul in (1.0e4, 1.0e5, 1.0e6, 1.0e7):
            try:
                dark()
                km = (rad * mul / 1000.0) if rad else 0.0
                try:
                    ins.setScale(orig * mul, Anim(0.0))
                except Exception:
                    ins.setScale(orig * mul)
                sleep(0.5)
                txt.setText("setScale ×%.0e   (반지름 약 %.0f km)" % (mul, km))
                uni.setGlobalIntensity(1.0, Anim.cubic(1.0))
                print("   >>> setScale ×%.0e  → 모델 반지름 약 %.0f km" % (mul, km))
                sleep(7.0)
            except Exception as e:
                print("   ×%.0e 실패: %s" % (mul, e))

        txt.setText("어느 배율에서 위성이 보였나요")
        sleep(5.0)
        txt.setIntensity(0.0, Anim(1.5))
        sleep(1.5)
    except Exception as e:
        print("D 단계 오류:", e)


line("프로브 v2 종료 — 알려주세요")
print("A) 천리안/COMS 모델이 있었나 (로그에 목록)")
print("B) 실존 우주선 모델의 radius 값 (스케일 감각)")
print("C) ★블랙홀이 **밖에서** 보였나 — ×30 / ×8 / ×2.5 중 어디서")
print("    → 보였다면 '몰입형이라 바깥 불가'는 단위 실수였고, 우리 모델도 밖에서 보인다는 뜻")
print("D) ★위성이 궤도에 보였나 — setScale ×1e4 / 1e5 / 1e6 / 1e7 중 어디서")

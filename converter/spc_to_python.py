"""
Sky Explorer - SPC → Python 변환기 (v0.1)
====================================================================
spc_converter.py 의 매핑(CMD/FAMILY)을 그대로 재사용한 역변환.
SPC 라인 → 대상 천체/명령/값 복원 → Python 스크립트 생성.

라인 포맷(TAB 67컬럼): [0]E [1]타임코드 [2]101 [3]cmdId [4..]헤더 bodyId 값들 0패딩 [66]꼬리
  cmdId → (클래스,메서드),  bodyId → (family, index),  값 슬롯 → Python 인자.
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spc_converter import (CMD, CMD_BY_ID, FAMILY_BY_CODE, GLOBAL, _is_pos,
                           TZ_CODE2NAME)  # 단일 소스 매핑 재사용

# 부모 클래스별 기본 portId 멤버(각 클래스 XxxPort enum 이 다름 — 실측 이름).
# SPC 에 포트 인덱스가 없어 '부착에 적합한 대표 포트'를 클래스별로 지정. 미등록은 "Synchronous" 폴백.
DEFAULT_PARENT_PORT = {
    "Planet": "EquatorialSynchronous", "Satellite": "EquatorialSynchronous",
    "DwarfPlanet": "EquatorialSynchronous",
    "Asteroid": "Synchronous", "Comet": "Synchronous", "OrbitalPlace": "Synchronous",
    "IndividualStar": "Ecliptic", "Galaxy": "Galactic", "GlobularCluster": "Galactic",
    "Nebula": "LineOfSightLocal",
}


def _fnum(x):
    """intensity/anim/color 값 → float 표기(1 → '1.0'). 정수형이면 .0 부여."""
    f = float(x)
    return str(int(f)) + ".0" if f.is_integer() else repr(f)

def _inum(x):
    """enum/index 값 → int 표기."""
    return str(int(round(float(x))))


# --- spec.form 주도 복원: 추출값 → Python 인자 문자열 리스트 ---
def _render_args(spec, cls, method, slots):
    """slots = {dur, val, vec, pos{n:v}} → Python 인자 리스트."""
    form = spec.get("form")
    if form in ("color", "vec", "cam_vec3", "cam_vec3_track"):
        v = slots["vec"]
        arg = "Vec(%s, %s, %s)" % (_fnum(v[0]), _fnum(v[1]), _fnum(v[2]))
        if form == "vec":                           # setPosition: Vec + (옵션)Anim
            return [arg, "Anim(%s)" % _fnum(slots["dur"])] if slots["dur"] else [arg]
        if form == "cam_vec3":                       # setOrientationHPR: Vec + Anim (track 없음)
            return [arg, "Anim(%s)" % _fnum(slots["dur"])]
        if form == "cam_vec3_track":                 # setPositionLBR: Vec + Anim + track
            return [arg, "Anim(%s)" % _fnum(slots["dur"]), _inum(slots["track"])]
        return [arg]
    if form == "bool":                               # setManualMoonPhase 등
        return ["True" if slots["val"] else "False"]
    if form == "cam_vec4_track":                     # setOrientationSmoothXYZR: Vec4 + Anim + track
        v = slots["vec"]
        arg = "Vec4(%s, %s, %s, %s)" % (_fnum(v[0]), _fnum(v[1]), _fnum(v[2]), _fnum(slots.get("w", 0)))
        return [arg, "Anim(%s)" % _fnum(slots["dur"]), _inum(slots["track"])]
    if form == "cam_val_track":                      # setPositionR: 값 + Anim + track
        return [_fnum(slots["val"]), "Anim(%s)" % _fnum(slots["dur"]), _inum(slots["track"])]
    if form == "enum":
        wrapper = method[3:] if method.startswith("set") else method  # setTerrainModel→TerrainModel
        return ["%s.%s(%s)" % (cls, wrapper, _inum(slots["val"]))]
    if form == "datetime":
        p = slots["pos"]
        ints = [_inum(p.get(i, 0)) for i in range(6)]       # y,m,d,h,mi,s
        code = int(round(slots.get("tz", 0)))
        name = TZ_CODE2NAME.get(code)                        # 코드→멤버(probe_04 표)
        ints.append("DateManager.TimeZone.%s" % name if name
                    else "DateManager.TimeZone(%d)" % code)  # 미매핑 코드는 정수 생성자
        ints.append("Anim(%s)" % _fnum(slots["dur"]))
        return ints
    # value_anim: 값 + (dur>0 이면) Anim
    args = [_fnum(slots["val"])]
    if slots["dur"]:
        args.append("Anim(%s)" % _fnum(slots["dur"]))
    return args


def _label_text(cols):
    """숫자/객체id 가 아닌 텍스트 필드를 라벨로 추출(주석/매크로 경로용)."""
    for c in cols[4:]:
        s = c.strip()
        if s and not s.lstrip("-").replace(".", "", 1).isdigit():
            return s
    return ""

def parse_spc(spc_text):
    """SPC 텍스트 → 이벤트 리스트 [(cls, index, method, [pyArgStr...]) ...].
       cat!=101(주석 128/매크로 129 등)은 파이썬 주석으로, 미매핑 101 은 '# 미매핑'으로."""
    events = []
    for ln in spc_text.splitlines():
        raw = ln.lstrip("﻿")
        if not ln.strip():
            continue
        if raw.startswith("#"):                     # 섹션 마커 등 → 그대로 주석 통과
            events.append(("?", None, "?", [raw], None))
            continue
        cols = [c.strip() for c in ln.split("\t")]
        cols = [c.lstrip("﻿") for c in cols]
        if len(cols) < 5 or cols[0] not in ("E", "C"):
            continue
        tc  = cols[1] if len(cols) > 1 else None    # 타임코드 HH-MM-SS-FF (타이밍 재현용)
        cat = cols[2] if len(cols) > 2 else ""
        try:
            cmd_id = int(cols[3])
        except ValueError:
            continue
        if cat != "101":                             # 주석/매크로/기타 카테고리
            lbl = _label_text(cols)
            kind = {"0": "주석", "600": "매크로", "": "cat?"}.get(cat, "cat=%s" % cat)
            if not lbl and kind == "주석":            # 빈 섹션 주석(내용 없음) → 생략
                continue
            note = "# [%s] %s" % (kind, lbl) if lbl else "# [%s] (cmd %d)" % (kind, cmd_id)
            events.append(("?", None, "?", [note], tc))
            continue
        SHADOW_CMDS = {1128: ("Planet", "Line"), 1132: ("Planet", "Area"),
                       1356: ("Satellite", "Line"), 1360: ("Satellite", "Area")}
        KNOWN_NOISE = {4865, 12037, 12038, 5650}
        if cmd_id in KNOWN_NOISE:
            continue                     # Studio 세션/UI 내부 명령 — 아예 생략(주석도 안 남김)
        if cmd_id in SHADOW_CMDS:              # 레이어 값으로 메서드 이름 복원
            scls, kind = SHADOW_CMDS[cmd_id]
            try:
                body = int(cols[7]); v = float(cols[9]); layer = int(float(cols[10]))
                dur = float(cols[6])
                lname = {2: "PenumbraBefore", 3: "PenumbraAfter", 4: "Antumbra"}.get(layer, "PenumbraBefore")
                method = "set%s%sIntensity" % (lname, kind)
                args = [_fnum(v)] + (["Anim(%s)" % _fnum(dur)] if dur else [])
                events.append((scls, (body & 0xFFFFFF) - 1, method, args, tc))
                continue
            except Exception:
                pass
        if cmd_id == 6405:     # Asteroid/OrbitalBody 결합 궤도요소(케플러8) → 개별 setter 로 전개
            try:                # payload[8..] = [const1, node, incl, ecc, argperi, a, M, ?, epochJD]
                body = int(cols[7]); idx = (body & 0xFFFFFF) - 1
                p = [float(cols[8 + i]) for i in range(9)]
                order = [("setLongitudeOfAscendingNode", p[1]), ("setInclination", p[2]),
                         ("setEccentricity", p[3]), ("setArgumentOfPeriapsis", p[4]),
                         ("setSemiMajorAxis", p[5]), ("setMeanAnomaly", p[6]), ("setEpoch", p[8])]
                for m, v in order:
                    events.append(("Asteroid", idx, m, [_fnum(v)], tc))
                continue
            except Exception:
                pass
        if cmd_id not in CMD_BY_ID:
            # 미매핑이라도 bodyId 로 family(클래스)를 찾아 주석에 표기 → 학습/향후 매핑에 유용
            fam_cls = "?"
            for cc in cols[4:14]:
                try:
                    v = int(cc)
                    if v > 0x1000000:
                        fam_cls = FAMILY_BY_CODE.get(v >> 24, "0x%02X" % (v >> 24)); break
                except ValueError:
                    pass
            lbl = _label_text(cols)
            note = "# 미매핑 %s cmd %d%s" % (fam_cls, cmd_id, (" (%s)" % lbl if lbl else ""))
            events.append(("?", None, "?", [note], tc))
            continue
        cls, method = CMD_BY_ID[cmd_id]
        spec = CMD[(cls, method)]
        head = spec["head"]
        h = len(head)
        base = 4                          # cols[4] 부터 헤더 시작
        if spec.get("form") in ("modelfile", "text"):   # head + 문자열 + bodyId
            path = cols[base + h]
            body = int(cols[base + h + 1])
            index = (body & 0xFFFFFF) - 1
            events.append((cls, index, method, [repr(path)], tc))
            continue
        is_global = cls in GLOBAL
        # 전역 명령은 bodyId 없음 → 페이로드가 헤더 바로 뒤에서 시작
        body_off = 0 if is_global else 1
        body = 0 if is_global else int(cols[base + h])
        pstart = base + h + body_off
        pay = [float(cols[pstart + i]) for i in range(len(spec["pay"]))]
        # animDur = 헤더의 "DUR" 슬롯, 값/벡터/위치인자 = 페이로드 레이아웃에서 추출
        dur = float(cols[base + head.index("DUR")]) if "DUR" in head else 0
        slots = {"dur": dur, "val": 0, "vec": [0, 0, 0], "w": 0, "pos": {}, "tz": 0, "track": -1, "parent": None}
        for i, p in enumerate(spec["pay"]):
            if p in ("V", "IDX"):
                slots["val"] = pay[i]
            elif _is_pos(p):
                slots["pos"][int(p[1:])] = pay[i]
            elif p == "TZ":
                slots["tz"] = pay[i]
            elif p == "TRK":
                if slots["track"] == -1:          # 첫 TRK 채택(프로덕션 상대변형은 2번째가 0)
                    slots["track"] = pay[i]
            elif p == "PAR" and slots.get("parent") is None:
                slots["parent"] = int(round(pay[i]))   # 부모 객체 bodyId
            elif p in ("R", "G", "B"):
                slots["vec"]["RGB".index(p)] = pay[i]
            elif p == "W":
                slots["w"] = pay[i]
        if is_global:
            real_cls, index = cls, None
        else:
            index = (body & 0xFFFFFF) - 1     # bodyId → index (family<<24 | index+1)
            real_cls = cls                    # cmdId 의 클래스가 authoritative(같은 family 공유 대비)
        # DateManager 257 의 모드 판별: 페이로드 3번째 상수 2 = 율리우스일 직접 지정
        if cls == "DateManager" and method == "setDateTime" and len(pay) > 3 and int(pay[2]) == 2:
            args = [_fnum(pay[3]), "Anim(%s)" % _fnum(dur)]
            events.append((cls, None, "setJulianDate", args, tc))
            continue
        if spec.get("form") == "parent":       # setParent: 부모(cls,index) 를 마커로 전달
            pbody = slots.get("parent") or 0
            pcls = FAMILY_BY_CODE.get(pbody >> 24, "Planet")
            pidx = (pbody & 0xFFFFFF) - 1
            events.append((real_cls, index, method, [("__PARENT__", pcls, pidx)], tc))
            continue
        pyargs = _render_args(spec, real_cls, method, slots)
        # setDateTime 상대/특수 모드(항성시 등) 방어: 연도가 비정상(<100)이면 깨진 절대날짜 대신 주석.
        if real_cls == "DateManager" and method == "setDateTime":
            try:
                yr = int(float(str(pyargs[0])))
            except (ValueError, IndexError):
                yr = None
            if yr is not None and yr < 100:
                events.append(("?", None, "?",
                    ["# [시간 이동] setDateTime 상대/특수 모드(cmd 257, 항성시 기준) — 자동 해독 불가. "
                     "원본은 '시간을 빠르게 흘려보내는' 명령이니 필요 시 setDateTime(목표날짜, Anim(초))로 직접 지정."],
                    tc))
                continue
        events.append((real_cls, index, method, pyargs, tc))
    return events


def _varname(cls, index):
    base = cls[0].lower() + cls[1:]
    return base if index is None else "%s%d" % (base, index)  # Satellite,1→satellite1 / DateManager→dateManager


def _tc_seconds(tc, fps=30):
    """타임코드 'HH-MM-SS-FF' → 초(float). 파싱 실패 시 None."""
    try:
        hh, mm, ss, ff = (int(x) for x in tc.split("-"))
        return hh * 3600 + mm * 60 + ss + ff / float(fps)
    except Exception:
        return None


# ── 후처리: 오퍼레이터가 트랙볼/슬라이더로 한 '연속 동작'은 SPC 에 0.16초마다 한 프레임씩
#    기록됨 → 거의 같은 setter 가 수십~수백 줄이 됨. 그 '기어가는 키프레임 run' 을
#    (같은 개체·같은 메서드, 시간 간격 작음) 끝값 하나로 압축한다. 전체 시간만큼 Anim 재설정.
#    ⚠️ 시간 간격이 큰(≥GAP) 연속 호출은 절대 합치지 않음 → 자막 show/hide 등 '의도된 시퀀스' 보호.
_ANIM_NUM = re.compile(r"Anim\(([-\d.eE+]+)\)")


def _anim_dur_of(args):
    for a in args:
        if isinstance(a, str):
            m = _ANIM_NUM.search(a)
            if m:
                try:
                    return float(m.group(1))
                except ValueError:
                    pass
    return None


def _retime_anim(a, dur):
    """arg 문자열의 Anim(...) 지속시간을 dur 로 교체(카메라 팬처럼 전체 시간에 맞춤)."""
    if dur is None or not (isinstance(a, str) and a.startswith("Anim(")):
        return a
    return re.sub(r"Anim\([^)]*\)", "Anim(%s)" % _fnum(dur), a)


def _collapse_runs(events, fps=30, min_run=2, gap=0.5):
    """연속 키프레임 run 압축. run = '같은 개체 + 시간간격≤gap' 인 연속 이벤트.
       run 안에서 메서드별 '마지막' 값만 남기고, Anim 은 max(run 시간, 원래 Anim) 로."""
    out, buf = [], []

    def _t(ev):
        return _tc_seconds(ev[4], fps)

    def flush():
        if not buf:
            return
        if len(buf) <= min_run:                 # 2개 이하(단일 키프레임)는 그대로
            out.extend(buf); buf.clear(); return
        t0, t1 = _t(buf[0]), _t(buf[-1])
        span = (t1 - t0) if (t0 is not None and t1 is not None and t1 > t0) else None
        last, order = {}, []
        for ev in buf:                          # 메서드별 마지막 값만
            if ev[2] not in last:
                order.append(ev[2])
            last[ev[2]] = ev
        for m in order:
            ev = last[m]
            dur = _anim_dur_of(ev[3])
            # 팬(span 큼)이면 전체 시간으로 늘리고, 슬라이더 순간드래그(span≈0)면 원래 Anim 유지
            target = None if span is None else (span if dur is None else max(span, dur))
            a = [_retime_anim(x, target) for x in ev[3]]
            out.append((ev[0], ev[1], m, a, buf[0][4]))   # tc=run 시작(뒤 sleep 이 run 시간 흡수)
        buf.clear()

    def collapsible(ev):
        return ev[0] != "?"                     # 주석/미매핑은 압축 대상 아님

    def compat(prev, ev):                       # 같은 개체 + 시간간격 작음
        if prev[0] != ev[0] or prev[1] != ev[1]:
            return False
        tp, te = _t(prev), _t(ev)
        if tp is None or te is None:
            return True                         # 타임코드 없으면 붙임(안전)
        return (te - tp) <= gap

    for ev in events:
        if collapsible(ev) and (not buf or compat(buf[-1], ev)):
            buf.append(ev)
        else:
            flush()
            if collapsible(ev):
                buf.append(ev)                  # 호환 안 되는 새 개체 → 새 run 시작
            else:
                out.append(ev)
    flush()
    return out


def _dedup_consecutive(events):
    """바로 앞과 (클래스·인덱스·메서드·인자) 가 똑같은 이벤트 제거(같은 값 재설정 = no-op)."""
    out = []
    for ev in events:
        if ev[0] == "?":                        # 주석/미매핑은 건드리지 않음
            out.append(ev); continue
        if out and out[-1][0] == ev[0] and out[-1][1] == ev[1] \
                and out[-1][2] == ev[2] and out[-1][3] == ev[3]:
            continue
        out.append(ev)
    return out


def to_python(spc_text, timed=False, fps=30):
    """timed=True 면 타임코드 증가분마다 sleep() 삽입 → 시간축 애니메이션 재현."""
    events = parse_spc(spc_text)
    events = _collapse_runs(events, fps)          # 트랙볼 팬·슬라이더 드래그 압축
    events = _dedup_consecutive(events)           # 연속 중복 제거
    # ⚠️ 3종 import 를 '항상' 넣는다 — 우리의 검증된 예제 표준과 동일.
    #    sleep()·DateManager 등이 Initialization 에서 노출되므로, 조건부로 빼면
    #    (예: DateManager 없는 clock 스크립트) `NameError: name 'sleep' is not defined` 로 죽는다.
    lines = ["from skyExplorer import *",
             "from studio import *",
             "from Initialization import *"]   # sleep·DateManager 등 노출 (항상 필요)
    lines.append("")
    seen = {}     # (cls,index) → varname

    def ensure_var(c, i):
        """(cls,index) 의 변수를 반환하고, 처음이면 생성자 라인 추가."""
        k = (c, i)
        if k not in seen:
            v = _varname(c, i)
            seen[k] = v
            if c in GLOBAL:
                ctor = {"Camera": "Camera(Camera.CameraName.MainCamera)",
                        "Universe": "Universe(Universe.UniverseName.MainUniverse)"}.get(c, "%s()" % c)
                lines.append("%s = %s" % (v, ctor))
            else:
                lines.append("%s = %s(%s.%sName(%d))" % (v, c, c, c, i))
        return seen[k]

    prev_t = None
    for cls, index, method, pyargs, tc in events:
        if timed and cls != "?":
            t = _tc_seconds(tc, fps)
            if t is not None and prev_t is not None and t > prev_t + 1e-6:
                lines.append("sleep(%s)" % _fnum(t - prev_t))   # 타임코드 간격만큼 대기
            if t is not None:
                prev_t = t
        if cls == "?":
            lines.append(pyargs[0]); continue
        var = ensure_var(cls, index)
        # setParent: 부모 객체 변수 생성 후 <child>.setParent(<parent>.portId(...Port.X))
        # ⚠️ SPC 는 포트 인덱스를 안 담음 → 부모 클래스별 '유효한 기본 포트'로 렌더(클래스마다 enum 멤버가 다름).
        if pyargs and isinstance(pyargs[0], tuple) and pyargs[0][0] == "__PARENT__":
            _, pcls, pidx = pyargs[0]
            pvar = ensure_var(pcls, pidx)
            port_name = DEFAULT_PARENT_PORT.get(pcls, "Synchronous")
            port = "%s.%sPort.%s" % (pcls, pcls, port_name)
            lines.append("%s.setParent(%s.portId(%s))" % (var, pvar, port))
            continue
        lines.append("%s.%s(%s)" % (var, method, ", ".join(str(a) for a in pyargs)))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python spc_to_python.py <input.SPC> [output.py]")
        sys.exit(1)
    txt = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    out = to_python(txt, timed=("--timed" in sys.argv))   # --timed: 타임코드→sleep 재현
    if len(sys.argv) >= 3:
        open(sys.argv[2], "w", encoding="utf-8").write(out)
        print("wrote", sys.argv[2])
    else:
        print(out)

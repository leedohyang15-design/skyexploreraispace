"""
Sky Explorer - SPC → JavaScript 변환기 (v0.1 POC)
====================================================================
spc_to_python 의 parse_spc(언어중립 이벤트) 를 그대로 재사용해 JS 문법으로 렌더.
아키텍처: SPC → parse_spc() → [(cls,index,method,args,tc)] → (Python | JavaScript) 에미터.

⚠️⚠️ JS 문법 가정(이 빌드 JS 실물 예제 부재 → Studio JS 런타임서 1회 검증 필요):
  · 생성자에 `new` 사용:  var camera = new Camera(Camera.CameraName.MainCamera);
  · 문장 끝 `;`,  변수 `var`,  주석 `//`,  Vec/Vec4/Anim 도 `new`.
  · enum 접근(Camera.CameraName.X)·슬롯 생성(Asteroid.AsteroidName(0))은 Python 과 동일 표기 가정.
  이 4가지(특히 new 여부·슬롯 enum 표기)만 실행 로그로 확인하면 완전 확정.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spc_converter import GLOBAL
from spc_to_python import parse_spc, _varname, DEFAULT_PARENT_PORT


def _to_js_arg(a):
    """Python 인자 문자열 → JS 인자 문자열."""
    s = str(a)
    for ctor in ("Vec4(", "Vec(", "Anim("):
        if s.startswith(ctor):
            return "new " + s
    if s == "True":
        return "true"
    if s == "False":
        return "false"
    return s          # 숫자 · 'path' · Enum.접근 은 그대로


def to_js(spc_text, timed=False, fps=30):
    from spc_to_python import _tc_seconds, _fnum
    events = parse_spc(spc_text)
    lines = ["// SkyExplorer JS (SPC 변환, v0.1 POC — Studio JS 런타임서 new/enum 표기 1회 확인 요망)"]
    seen = {}

    def ensure_var(c, i):
        k = (c, i)
        if k not in seen:
            v = _varname(c, i)
            seen[k] = v
            if c in GLOBAL:
                ctor = {"Camera": "new Camera(Camera.CameraName.MainCamera)",
                        "Universe": "new Universe(Universe.UniverseName.MainUniverse)"}.get(c, "new %s()" % c)
                lines.append("var %s = %s;" % (v, ctor))
            else:
                lines.append("var %s = new %s(%s.%sName(%d));" % (v, c, c, c, i))
        return seen[k]

    prev_t = None
    for cls, index, method, pyargs, tc in events:
        if timed and cls != "?":
            t = _tc_seconds(tc, fps)
            if t is not None and prev_t is not None and t > prev_t + 1e-6:
                lines.append("sleep(%s);" % _fnum(t - prev_t))
            if t is not None:
                prev_t = t
        if cls == "?":
            note = pyargs[0]
            lines.append(("//" + note[1:]) if note.startswith("#") else ("// " + note))
            continue
        var = ensure_var(cls, index)
        if pyargs and isinstance(pyargs[0], tuple) and pyargs[0][0] == "__PARENT__":
            _, pcls, pidx = pyargs[0]
            pvar = ensure_var(pcls, pidx)
            port_name = DEFAULT_PARENT_PORT.get(pcls, "Synchronous")
            port = "%s.%sPort.%s" % (pcls, pcls, port_name)
            lines.append("%s.setParent(%s.portId(%s));" % (var, pvar, port))
            continue
        jsargs = [_to_js_arg(a) for a in pyargs]
        lines.append("%s.%s(%s);" % (var, method, ", ".join(jsargs)))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python spc_to_js.py <input.SPC> [output.js]")
        sys.exit(1)
    txt = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    out = to_js(txt, timed=("--timed" in sys.argv))
    if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
        open(sys.argv[2], "w", encoding="utf-8").write(out)
        print("wrote", sys.argv[2])
    else:
        print(out)

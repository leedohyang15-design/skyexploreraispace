# -*- coding: utf-8 -*-
"""
생성 코드 검증기 — LLM 출력을 '실측 지식'에 결정론적으로 대조한다.
====================================================================
시스템 프롬프트의 "추측 금지" 규칙은 모델이 지켜주기를 바랄 뿐 강제하지 못한다.
특히 TPM 폴백 시엔 축소 지식(SYSTEM_LITE)으로 돌기 때문에 환각 확률이 더 높다.
여기서는 프롬프트가 아니라 코드로 검증한다.

신뢰 소스(셋의 합집합):
  1. knowledge/reference.md  — 실측 레퍼런스
  2. knowledge/examples.md   — 검증된 예제
  3. converter/spc_converter.py 의 CMD 표 — 녹화로 cmdId 까지 확정된 매핑

검사 항목:
  ⛔ locked  — 레퍼런스가 '호출은 되지만 효과 없음'으로 실측 확정한 API
  ⚠️ unknown — 어느 신뢰 소스에도 없는 메서드 (환각 후보)
  ❌ syntax  — 파싱 자체가 안 되는 코드

한계(의도적): 메서드 '이름' 단위 검사다. 올바른 메서드를 엉뚱한 클래스에 호출하는 것까지는
잡지 않는다 — 클래스 단위로 좁히면 레퍼런스 문서 구조에 의존하게 돼 오탐이 늘기 때문.
오탐 하나가 진짜 경고 열 개의 신뢰를 깎으므로, 확신하는 것만 보고한다.
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

# reference.md '## AdvancedCamera' 절에서 실측 확정된 스크립트 잠금 API.
# "호출은 되지만 화면 안 움직임" → 코드가 문법적으로 멀쩡해도 무용지물이라 반드시 알려야 한다.
LOCKED = {
    "zoom":               "AdvancedCamera.zoom() 은 스크립트에서 효과 없음(연속이동 잠금). 접근/줌은 마우스(Move closer)로만.",
    "move":               "AdvancedCamera.move() 는 스크립트에서 효과 없음(연속이동 잠금).",
    "tilt":               "AdvancedCamera.tilt() 는 스크립트에서 효과 없음(연속이동 잠금).",
    "roll":               "AdvancedCamera.roll() 은 스크립트에서 효과 없음(실측 무반응).",
    "takeOffOn":          "비행뷰는 UI 'Take off' 버튼을 사람이 눌러야 함 — 스크립트 호출은 화면이 안 바뀝니다.",
    "setModeTerrainView": "좌표계만 L/B/R→X/Y/Z 로 바뀌고 화면은 안 바뀜(스크립트 카메라 잠금).",
}


def _read(rel: str) -> str:
    p = HERE / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _build_known():
    """레퍼런스·예제·CMD 표에서 (SDK 클래스, 알려진 메서드) 집합을 만든다."""
    text = _read("knowledge/reference.md") + "\n" + _read("knowledge/examples.md")

    # 문서에 `.method(` 로 등장하는 것 = 실측된 호출
    methods = set(re.findall(r"\.([a-zA-Z_]\w*)\s*\(", text))
    # '## Camera — ...' 같은 절 제목 = SDK 클래스 (한글 제목은 대문자 시작 조건으로 걸러진다)
    classes = set(re.findall(r"^##\s+([A-Z][A-Za-z0-9]*)", text, re.M))

    try:                                   # 녹화로 확정된 매핑 — 문서에 없더라도 검증된 것
        sys.path.append(str(HERE / "converter"))
        from spc_converter import CMD, FAMILY, GLOBAL
        methods |= {m for (_c, m) in CMD}
        classes |= set(FAMILY) | set(GLOBAL)
    except Exception:                      # noqa: BLE001 — 변환기가 없어도 검증기는 동작
        pass

    classes |= {"Anim", "Animator", "SceneGraph", "DataManager", "AdvancedCamera",
                "Universe", "InsertText", "Vec"}
    return classes, methods


SDK_CLASSES, KNOWN_METHODS = _build_known()

# 지식팩이 통째로 빠진 상태(app.py 의 '(경고: knowledge/... 가 업로드되지 않음)')에서
# 검증기를 돌리면 멀쩡한 코드가 전부 '미검증'으로 찍힌다 → 아예 끈다.
ENABLED = len(KNOWN_METHODS) >= 20


def _root(node):
    """어트리뷰트/호출 체인의 뿌리 이름.
    Planet(..).setX()            → 'Planet'
    DataManager.database().data()→ 'DataManager'
    cam.setPositionR()           → 'cam'
    """
    while True:
        if isinstance(node, ast.Attribute):
            node = node.value
        elif isinstance(node, ast.Call):
            node = node.func
        elif isinstance(node, ast.Name):
            return node.id
        else:
            return None


def lint(code: str) -> list:
    """코드 → 경고 리스트 [{level, line, api, msg}]. 문제 없으면 []."""
    if not ENABLED or not code or not code.strip():
        return []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{"level": "syntax", "line": e.lineno or 0, "api": "",
                 "msg": "문법 오류 (%s행): %s — 그대로 실행하면 Studio 에서 SyntaxError 가 납니다."
                        % (e.lineno, e.msg)}]

    # SDK 생성자에 묶인 변수 추적: earth = Planet(...) → earth 는 Planet
    sdk_vars = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            root = _root(node.value.func)
            if root in SDK_CLASSES:
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        sdk_vars[t.id] = root

    issues, seen = [], set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        m = node.func.attr
        if not m or not m[0].islower():
            continue          # CamelCase = enum/타입 생성자(PlanetName, NebulaPort…) — API 호출 아님
        root = _root(node.func.value)
        if root not in SDK_CLASSES and root not in sdk_vars:
            continue          # SDK 객체가 아님(time.sleep, list.append 등) → 검사 대상 밖
        cls = sdk_vars.get(root, root)

        if m in LOCKED:
            level, msg = "locked", LOCKED[m]
        elif m not in KNOWN_METHODS:
            level = "unknown"
            msg = ("%s.%s() 는 실측 레퍼런스·예제·녹화 매핑 어디에도 없습니다 — "
                   "모델이 지어낸 API 일 수 있습니다." % (cls, m))
        else:
            continue

        key = (level, m, node.lineno)
        if key in seen:
            continue
        seen.add(key)
        issues.append({"level": level, "line": node.lineno, "api": "%s.%s" % (cls, m), "msg": msg})

    issues.sort(key=lambda i: (i["level"] != "locked", i["line"]))
    return issues

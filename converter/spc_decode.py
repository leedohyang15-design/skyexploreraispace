"""
Sky Explorer - 범용 SPC 디코더 (disassembler)
====================================================================
매핑이 없어도 '모든' SPC 라인을 구조적으로 해독한다:
  라인타입(E/C) · 타임코드 · 카테고리 · cmdId · 대상객체(family#index) · 값 · 문자열.
목적: 프로덕션 SPC 를 읽을 수 있는 중간표현으로 만들어, cmdId→메서드 매핑을
      채워나가는 재료로 사용(변환기 확장용).

객체 id 규칙(역설계): id = (family<<24) | low24.  low24 = 인덱스/포트.
  확정 family: 0x12=Planet, 0x15=Satellite, 0x03=Mark. 그 외는 hex 로 표기.
알려진 cmdId(부분): 257=Date, 273/274=ObsPos?, 1062=Planet.setCloudsIntensity,
  1282=Satellite.setIntensity, 128=주석/라벨, 129=Macro, 5633=?(Place2D?).
"""
import os, sys

OBJ_MIN = 0x01000000   # 이 이상 정수 = 객체 id(상위바이트=family)로 간주
FAMILY_NAME = {0x12: "Planet", 0x15: "Satellite", 0x03: "Mark", 0x1A: "Place2D",
               0x0B: "IndividualStar", 0x0C: "Stars", 0x06: "Galaxy", 0x0A: "Constellation",
               0x02: "Nebula/Messier", 0x01: "Insert2D", 0x2D: "SkySurvey",
               0x1D: "Insert3D", 0x1B: "Chart2D?", 0x1E: "Model3Dnode?", 0x14: "OrbitalBody?"}

# 참고용 알려진 cmdId (있으면 주석으로 붙임). 계속 채워나가면 됨.
KNOWN_CMD = {
    128: "comment/label", 129: "Macro", 257: "DateManager.setDateTime",
    # Planet(0x12) — probe_05 로 직접 확정(구 디스어셈블 추정 수정: clouds=1064, atmo=1065, ring=1186)
    1026: "Planet.setIntensity", 1030: "Planet.setOrbitIntensity",
    1057: "Planet.?(재확인)", 1059: "Planet.setElevationScale",
    1062: "Planet.?(clouds계열 재확인)", 1064: "Planet.setCloudsIntensity",
    1065: "Planet.setAtmosphereIntensity", 1184: "Planet.setTerrainModel",
    1186: "Planet.setRingModel",
    1282: "Satellite.setIntensity",
    1283: "Satellite.?", 1394: "Satellite.setTerrainModel",
    4356: "Mark.setIntensity", 4357: "Mark.setColor",
    # probe_09/11 확정 (Light ON = 태양·별 켜기)
    514: "Stars.setIntensity", 770: "IndividualStar.setIntensity",
    771: "IndividualStar.?(값4)", 1057: "Planet.setLightPollutionIntensity",
    1061: "Planet.setScatteringIntensity", 1182: "Planet.setCloudLightPollution",
    1204: "Planet.setAtmosphericRefractionFactor", 1206: "Planet.setAtmosphereHaloIntensity",
    1302: "Satellite.setLabelIntensity", 1309: "Satellite.setElevationScale",
    1313: "Satellite.setCloudsIntensity", 1537: "Constellation.setLinesIntensity",
    2050: "Galaxy.setIntensity", 5889: "Messier.setIntensity",
    9985: "Nebula.setIntensity", 13825: "SkySurvey.setIntensity", 1802: "Insert2D.setIntensity",
    # Insert3D(0x1D) 3D모델 — 확정
    6145: "Insert3D.setIntensity", 6146: "Insert3D.setModelFilename",
    6147: "Insert3D.setPositionLBR", 6148: "Insert3D.setOrientationHPR",
    6149: "Insert3D.setScale",
    # 정체는 알지만 메서드명 미확정(디코드 라벨만)
    295:  "Camera.ObsOri(대상조준,look)", 6151: "Insert3D.videoControl(문자열)",
    6152: "Insert3D.?(intensity류)", 6154: "Insert3D.?(상태,문자열)",
    6166: "Insert3D.?(명명부품)", 6167: "Insert3D.?(명명부품)",
    3844: "Chart2D.title?(문자열)", 6402: "OrbitalBody.model(경로)",
    6405: "OrbitalBody.orbitalElements(케플러8)",
    4881: "Place2D.setParent(부착)", 5633: "Place2D.setPosition",
    5634: "Place2D.setLongitude", 5635: "Place2D.setLatitude",
    5636: "Place2D.setAltitude",
    # Camera(시점) 계열 — probe_06/07 확정. 305 는 setTarget(Vec2) 유력(미검증)
    273: "Camera.setPositionLBR", 274: "Camera.setPositionL",
    275: "Camera.setPositionB", 276: "Camera.setPositionR",
    289: "Camera.setOrientationHPR", 290: "Camera.setOrientationH",
    291: "Camera.setOrientationP", 305: "Camera.setTarget",
    306: "Camera.setTargetAzimuth", 307: "Camera.setTargetHeight",
    316: "Camera.setZoomFov",
}

def _isint(s):
    try: int(s); return True
    except: return False
def _isnum(s):
    try: float(s); return True
    except: return False

def decode_field(s):
    """필드 → ('obj', fam, low24) / ('num', value) / ('str', text)."""
    if _isint(s):
        v = int(s)
        if v >= OBJ_MIN:
            return ("obj", v >> 24, v & 0xFFFFFF)
        return ("num", v)
    if _isnum(s):
        return ("num", float(s))
    return ("str", s)

def fam_label(fam, low24):
    name = FAMILY_NAME.get(fam, "fam0x%02X" % fam)
    return "%s#%d" % (name, low24)      # low24 = 인덱스/포트 원값

def decode_line(line):
    cols = [c.lstrip("﻿") for c in line.rstrip("\n").split("\t")]
    cols = [c for c in cols if c.strip() != ""]     # 꼬리공백/빈칸 제거
    if not cols:
        return None
    ltype = cols[0]                       # E / C
    tc    = cols[1] if len(cols) > 1 else ""
    cat   = cols[2] if len(cols) > 2 else ""
    cmd   = cols[3] if len(cols) > 3 else ""
    rest  = cols[4:]
    # 뒤쪽 연속 0 패딩 제거
    while rest and rest[-1] == "0":
        rest.pop()
    objs, nums, strs = [], [], []
    for f in rest:
        k = decode_field(f)
        if k[0] == "obj": objs.append(fam_label(k[1], k[2]))
        elif k[0] == "num": nums.append(k[1])
        else: strs.append(k[1])
    note = KNOWN_CMD.get(int(cmd), "") if _isint(cmd) else ""
    return dict(ltype=ltype, tc=tc, cat=cat, cmd=cmd, objs=objs, nums=nums,
               strs=strs, note=note)

def disassemble(spc_text):
    out = []
    for ln in spc_text.splitlines():
        d = decode_line(ln)
        if d is None:
            continue
        seg = "%s %s cat=%s cmd=%-5s" % (d["ltype"], d["tc"], d["cat"], d["cmd"])
        if d["note"]: seg += " (%s)" % d["note"]
        if d["objs"]: seg += " | obj=%s" % ",".join(d["objs"])
        if d["nums"]: seg += " | val=%s" % d["nums"]
        if d["strs"]: seg += ' | str="%s"' % " ".join(d["strs"])
        out.append(seg)
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python spc_decode.py <input.SPC> [more.SPC ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        print("========== %s ==========" % os.path.basename(path))
        txt = open(path, encoding="utf-8", errors="ignore").read()
        print(disassemble(txt))

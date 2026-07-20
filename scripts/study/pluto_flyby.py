# -*- coding: utf-8 -*-
"""
pluto_flyby.py — 명왕성 근접 v1 (2026-07-09)
새 예제: 처음 연습하는 DwarfPlanet 클래스 (Pluto/Ceres/Eris/Haumea/Makemake).
소재: 뉴호라이즌스 2015-07-14 명왕성 최근접 — '하트'(톰보 지역) 표면.

★ 새 API (레퍼런스): setTerrainModel(3D 지형) / setElevationScale(고도 과장) /
   setShadowStrength·setShadowContrast / setIntensity / setOrbitIntensity / setLabelIntensity /
   setPointerType. DB = Data.Type.DwarfPlanetType.
확정 레시피 적용: FadeTo 로 프레임 확보 → setPositionR(읽은값×배율, -1) 줌인 (혜성/행성과 동일).

무대: 우주 조망. FadeTo 후 명왕성 프레임에서 줌.
"""

from skyExplorer import *
from studio import *
from Initialization import *


def probe(title, obj):
    try:
        ms = [m for m in dir(obj) if not m.startswith("_") and m not in ("name", "names", "values")]
        print("[PROBE] %s (%d): %s" % (title, len(ms), ", ".join(ms)))
        return ms
    except Exception as e:
        print("[PROBE] %s 실패: %s" % (title, e)); return []


cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone

# ── 프로브 ────────────────────────────────────────────────────
print("=" * 60); print("ACT 0: DwarfPlanet 프로브"); print("=" * 60)
probe("DwarfPlanet.DwarfPlanetName", DwarfPlanet.DwarfPlanetName)
if hasattr(DwarfPlanet, "TerrainModel"):
    probe("DwarfPlanet.TerrainModel", DwarfPlanet.TerrainModel)
if hasattr(DwarfPlanet, "DwarfPlanetPort"):
    probe("DwarfPlanet.DwarfPlanetPort", DwarfPlanet.DwarfPlanetPort)
pluto_db = None
try:
    for nm in ("Pluto", "134340 Pluto", "(134340) Pluto"):
        d = DataManager.database().data(Data.Type.DwarfPlanetType, nm)
        print("   DB DwarfPlanetType '%s' → %s" % (nm, "found" if d is not None else "None"))
        if d is not None and pluto_db is None:
            pluto_db = (nm, d)
except Exception as e:
    print("   DB 조회 실패: %s" % e)

# ── 무대 ──────────────────────────────────────────────────────
print("=" * 60); print("ACT 1: 무대"); print("=" * 60)
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
dm.stop(); sleep(0.3)
dm.setDateTime(2015, 7, 14, 11, 49, 0, tz, Anim(0.5))    # 뉴호라이즌스 최근접
sleep(1.0)

# 명왕성 본체 핸들 + 지형/표시 세팅
pluto = DwarfPlanet(DwarfPlanet.DwarfPlanetName.Pluto)
pluto.setIntensity(1.0, Anim(0.0))
try:
    # ★ TerrainModel 실측: Basic/DefaultTerrain(밋밋) / NewHorizons(명왕성 실측 표면=하트!) /
    #   DawnHamo·DawnLamo(Dawn 탐사선 세레스 표면). → 명왕성은 NewHorizons 로 진짜 하트를!
    pluto.setTerrainModel(DwarfPlanet.TerrainModel.NewHorizons)
    print("   setTerrainModel(NewHorizons) — 실측 표면")
except Exception as e:
    print("   NewHorizons 실패(%s) → DefaultTerrain 폴백" % e)
    try:
        pluto.setTerrainModel(DwarfPlanet.TerrainModel.DefaultTerrain)
    except Exception:
        pass

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 55, 0)); t1.setDistance(20.0, Anim(0.0)); t1.setColor(Vec(0.9, 0.85, 0.75))
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
t1.setText("명왕성 — 뉴호라이즌스, 2015년 7월"); t1.setIntensity(1.0, Anim(1.5))
sleep(5.0)
t1.setIntensity(0.0, Anim(0.8)); sleep(1.0)

# ── FadeTo 명왕성 → 줌인 ─────────────────────────────────────
print("=" * 60); print("ACT 2: FadeTo 명왕성 + 줌인"); print("=" * 60)
if pluto_db is not None:
    nm, d = pluto_db
    act = d.action(Action.Type.FadeTo)
    if act is not None:
        t1.setText("명왕성 곁으로"); t1.setIntensity(1.0, Anim(0.8))
        act.trigger()
        sleep(6.0)
        try:
            p = cam.positionLBR
            print("   FadeTo 후 R=%.3f → 줌인" % p.z)
            t1.setText("얼어붙은 세계 — 지름 2,377 km")
            # 매끄러운 줌 (선형+잘게, 소행성 v5 교훈). R=4 도킹서 표면 채우게 1.7까지.
            target = 1.7
            step = 0
            while cam.positionLBR.z > target * 1.15 and step < 30:
                r = max(cam.positionLBR.z * 0.72, target)
                cam.setPositionR(r, Anim(1.2), -1)
                sleep(1.25); step += 1
            print("   줌 완료 R=%.2f (%d단계)" % (cam.positionLBR.z, step))
        except Exception as e:
            print("   줌 실패: %s" % e)
        sleep(2.0)
        t1.setIntensity(0.0, Anim(0.8))
    else:
        print("   FadeTo 미지원")
else:
    print("   DB 핸들 없음")

# ── ACT 3: 지형 강조 (고도 과장 + 그림자) ────────────────────
print("=" * 60); print("ACT 3: 지형 강조"); print("=" * 60)
try:
    t1.setText("하트 모양 평원 — 톰보 지역"); t1.setIntensity(1.0, Anim(0.8))
    orig_elev = None
    try:
        orig_elev = pluto.elevationScale
    except Exception:
        pass
    pluto.setElevationScale(8.0, Anim(3.0))          # 고도 과장 (산맥 강조)
    sleep(4.0)
    try:
        pluto.setShadowStrength(0.3, Anim(2.0))      # 그림자 강하게(명암 대비)
    except Exception as e:
        print("   setShadowStrength 스킵: %s" % e)
    print("   ★ 표면 지형·그림자가 강조됐나?")
    sleep(4.0)
    if orig_elev is not None:
        pluto.setElevationScale(orig_elev, Anim(2.0))
    t1.setText("태양에서 59억 km — 빛조차 5시간 걸리는 변방")
    sleep(4.0)
    t1.setIntensity(0.0, Anim(0.8))
except Exception as e:
    print("   지형 강조 실패: %s" % e)

# ── 피날레 ────────────────────────────────────────────────────
t1.setText("명왕성 — 태양계의 끝, 카이퍼 벨트의 왕"); t1.setIntensity(1.0, Anim(1.0))
sleep(5.0)
t1.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(4.0))
sleep(4.5)
print("종료. 리포트: ①[PROBE] TerrainModel/이름 ②FadeTo 후 줌 R ③표면/하트 보이나 ④고도과장·그림자 효과")

# Insert3D (family 0x1D) cmd → 메서드 매핑 근거표

469개 프로덕션 SPC 코퍼스 교차대조로 추출한 Insert3D 명령 증거.
완본 메서드 26종: getIntrospection/modifyUniform/remove/rotateMatrix/scaleMatrix/setAnimationEvolution/
setAnimationName/setAnimationStartTime/setExposure/setIntensity/setIntensityIDV/setModelFilename/
setOrientationHPR/setParent/setPointExposure/setPointSize/setPointSizeFactor/setPositionLBR/setPositionXYZ/
setScale/setShadowStrength/setUniform/setVideoSpeed/setVideoState/translateMatrix/updateTexture.

## ✅ 확정 (매핑 완료)
| cmd | 메서드 | 근거 |
|----|--------|------|
| 6145 | setIntensity | 녹화 확정 |
| 6146 | setModelFilename | 헤더에 .osg 경로 |
| 6147 | setPositionLBR | 녹화 확정, [3,9,DUR] Vec |
| 6148 | setOrientationHPR | 녹화 확정, [3,9,DUR] Vec |
| 6149 | setScale | 녹화 확정, 스칼라 |

## 🟡 강한 추정 (문자열/구조 단서 — 녹화로 확정 요망)
| cmd | ×빈도 | 추정 메서드 | 근거 |
|----|------|-----------|------|
| 6151 | 956 | **setVideoState** | 헤더 키워드 = STOP/PLAY (VideoState enum 값) |
| 6154 | 528 | setAnimation* | 헤더 키워드 = EVOLUTION/START_TIME (애니 모드) |
| 6153 | 4 | **setAnimationStartTime** | 페이로드 = 날짜(2017-07-28) datetime |
| 6166 | 52 | **modifyUniform** | 헤더 = 유니폼명(blackholeGeode/u_AccrIntensity) + Vec4. (blackhole_final 에서 실사용 확인) |
| 6167 | 132 | setUniform/translateMatrix | 헤더 = 명명노드(Position_AuxiliaryTelescope_01 / MATRIX_*) + Vec3 |
| 6172 | 12 | **updateTexture** | 헤더 = 텍스처 경로(.dds cubemap) |
| 6175 | 50 | setParent | 페이로드에 부모 bodyId(Planet 등) 임베드 |
| 6183 | 6 | (노드 선택) | 헤더 = 노드명(blackholeGeode) |

## 🔵 스칼라 value_anim (레이아웃 [3,6,DUR]+[1,V,1] — 이름만 미상, 녹화 필요)
6150(×58,val5) · 6152(×618,val0) · 6155 · 6158 · 6162(val10) · 6164(val0.1) · 6165(val0.5) · 6174 · 6176(val0.995).
→ 후보(스칼라 메서드): setExposure/setShadowStrength/setPointExposure/setPointSize/setPointSizeFactor/setIntensityIDV/setVideoSpeed.
→ **값 하나 바꿔 녹화하면 즉시 확정** (예: setExposure(0.5) 만 있는 쇼 1개).

## 🔵 enum (레이아웃 [1,2]+[IDX] — 이름 미상)
6177(×476,val0) · 6157(val10) · 6178([1,3]) · 6179 · 6181.

## 결론
- **고빈도 미매핑 = Insert3D 고급 메서드**(비디오/셰이더/애니/명명노드) — 시그니처가 복잡·다양해 코퍼스만으론 이름 확정 불가.
- 순수 스칼라 9개 + enum 5개는 **각 1회 타깃 녹화**로 확정 가능(값 바꿔 찍기).
- 컨버터 미매핑 주석이 이제 `# 미매핑 Insert3D cmd 6166 (유니폼명)` 로 family+단서 표기 → 학습 데이터로도 읽힘.

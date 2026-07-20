# skyExplorer 모듈

## Classes

| Class | Description |
|---|---|
| `skyExplorer.Anim` |  |
| `skyExplorer.Animator` | [deprecated] Please prefer Anim over Animator. |
| `skyExplorer.Asteroid` |  |
| `skyExplorer.Audio` |  |
| `skyExplorer.AudioLayer` |  |
| `skyExplorer.AudioLite` |  |
| `skyExplorer.AudioPlayer` |  |
| `skyExplorer.Body` |  |
| `skyExplorer.Bolide` |  |
| `skyExplorer.Camera` |  |
| `skyExplorer.Chart2D` |  |
| `skyExplorer.Clock` |  |
| `skyExplorer.Comet` |  |
| `skyExplorer.Comment` |  |
| `skyExplorer.Constellation` |  |
| `skyExplorer.DMX512` |  |
| `skyExplorer.DateManager` |  |
| `skyExplorer.DomePointer` |  |
| `skyExplorer.DrawableInsert` |  |
| `skyExplorer.DwarfPlanet` |  |
| `skyExplorer.Ephemeris` |  |
| `skyExplorer.FreeDomeManager` |  |
| `skyExplorer.Galaxy` |  |
| `skyExplorer.GlobularCluster` |  |
| `skyExplorer.IndividualStar` |  |
| `skyExplorer.Insert2D` |  |
| `skyExplorer.Insert3D` |  |
| `skyExplorer.InsertText` |  |
| `skyExplorer.Light` |  |
| `skyExplorer.Line` |  |
| `skyExplorer.Lut` |  |
| `skyExplorer.Mark` |  |
| `skyExplorer.Mat` | alias of Mat4x4 |
| `skyExplorer.Mat4x4` | 4×4 matrix of doubles. |
| `skyExplorer.Messier` |  |
| `skyExplorer.NGC` |  |
| `skyExplorer.Nebula` |  |
| `skyExplorer.OrbitalPlace` |  |
| `skyExplorer.ParameterizationLut` |  |
| `skyExplorer.Patch` |  |
| `skyExplorer.Place2D` |  |
| `skyExplorer.Place3D` |  |
| `skyExplorer.Planet` |  |
| `skyExplorer.RemoteShow` |  |
| `skyExplorer.Satellite` |  |
| `skyExplorer.SceneGraph` |  |
| `skyExplorer.ShootingStar` |  |
| `skyExplorer.ShowEngineManager` |  |
| `skyExplorer.SkySurvey` |  |
| `skyExplorer.SlideShowHandler` |  |
| `skyExplorer.SoftwareManager` |  |
| `skyExplorer.Stars` |  |
| `skyExplorer.Universe` |  |
| `skyExplorer.Vec` | alias of Vec3 |
| `skyExplorer.Vec2` | 2D vector of doubles. |
| `skyExplorer.Vec3` | 3D vector of doubles. |
| `skyExplorer.Vec4` | 4D vector of doubles. |
| `skyExplorer.VideoPlayer` |  |

---

# skyExplorer.Anim

## class skyExplorer.Anim

### class Interpo

Linear

Cubic

Quintic

LinearEvo

Sin

SinEvo

CubicIn

CubicOut

ExpIn

ExpOut

Inertial

InertialEvo

Exp

ExpInOut

ExpEvoIn

ExpEvoOut

### class Type

Abs

Rel

RelMul

RelMulDef

RelDef

### `static cubic((float)duration) -> Anim`

[static] Creates a basic cubic Anim.

### `static cubicIn((float)duration) -> Anim`

[static] Creates a basic cubicIn Anim.

### `static cubicOut((float)duration) -> Anim`

[static] Creates a basic cubicOut Anim.

### `static exp((float)duration) -> Anim`

[static] Creates a basic exp Anim.

### `static expEvoIn((float)duration[, (float)accRatio=1.0]) -> Anim`

[static] Creates a basic expEvoIn Anim.

### `static expEvoOut((float)duration[, (float)accRatio=1.0]) -> Anim`

[static] Creates a basic expEvoOut Anim.

### `static expIn((float)duration) -> Anim`

[static] Creates a basic expIn Anim.

### `static expInOut((float)duration) -> Anim`

[static] Creates a basic expInOut Anim.

### `static expOut((float)duration) -> Anim`

[static] Creates a basic expOut Anim.

### `static inertial((float)duration[, (float)accRatio=0.33[, (float)decRatio=0.33]]) -> Anim`

[static] Creates a basic inertial Anim.

### `static inertialEvo((float)duration[, (float)accRatio=0.33]) -> Anim`

[static] Creates a basic inertialEvo Anim.

### `static linear((float)duration) -> Anim`

[static] Creates a basic linear Anim.

### `static linearEvo((float)duration) -> Anim`

[static] Creates a basic linearEvo Anim.

### `static quintic((float)duration) -> Anim`

[static] Creates a basic quintic Anim.

### `static rel() -> Anim`

[static] Creates a basic relative Anim.

### `static sin((float)duration) -> Anim`

[static] Creates a basic sin Anim.

### `static sinEvo((float)duration) -> Anim`

[static] Creates a basic sinEvo Anim.

### `static switchA() -> Anim`

[static] Creates a switch Anim (supposed to be used for camera pos/ori switches).

### `shift((Anim)arg1, (float)offset) -> Anim`

Returns a reference to the caller after adding an offset (modifies caller).

### `shifted((Anim)arg1, (float)offset) -> Anim`

Returns a new Anim with an added offset (caller remains unchanged).

### property: `property acc`

Acceleration (seconds).

### property: `property dec`

Deceleration (seconds).

### property: `property duration`

Duration (seconds).

### property: `property interpo`

Interpolation

### property: `property offset`

Timing offset (seconds).

### property: `property type`

Type (abolute, relative…)

---

# skyExplorer.Animator

## class skyExplorer.Animator

[deprecated] Please prefer Anim over Animator.

### class Interpolator

InvalidInterpolator

InterpolatorLinear

InterpolatorInertial

InterpolatorPsc

InterpolatorCount

### class Modulator

InvalidModulator

ModulatorLinear

ModulatorCubic

ModulatorSinusoidal

ModulatorQuintic

ModulatorCubicIn

ModulatorCubicOut

ModulatorExponentialIn

ModulatorExponentialOut

ModulatorExponentialInOut

ModulatorCount

### class PostBehavior

InvalidPostBehavior

PostBehaviorStop

PostBehaviorContinue

PostBehaviorCount

### class Relativity

InvalidRelativity

RelativityAbsolute

RelativityAdd

RelativityMultiply

RelativityMultiplyDefaultValue

RelativityAddDefaultValue

RelativityCount

### property: `property acceleration`

Duration of the acceleration in seconds at animation start. acceleration + deceleration must be lesser than duration value.

### property: `property deceleration`

Duration of the deceleration in seconds at animation end. acceleration + deceleration must be lesser than duration value.

### property: `property duration`

Duration of the animation in seconds.

### property: `property interpolator`

Interpolation model of the animation. See ‘Interpolator’ enumeration documentation for available values

### property: `property modulator`

Modulation model of the animation. See ‘Modulator’ enumeration documentation for available values

### property: `property postBehavior`

Behavior of the animation after reaching target value. See ‘PostBehavior’ enumeration documentation for available values

### property: `property relativity`

Relativity model of the animation. See ‘Relativity’ enumeration documentation for available values

### property: `property timingOffset`

Offset in seconds use to delay the animation. Use 0 to start the animation directly.

---

# skyExplorer.Asteroid

## class skyExplorer.Asteroid

### class AsteroidName

InvalidAsteroid

Asteroid001

Asteroid002

Asteroid003

Asteroid004

Asteroid005

Asteroid006

Asteroid007

Asteroid008

Asteroid009

Asteroid010

Asteroid011

Asteroid012

Asteroid013

Asteroid014

Asteroid015

Asteroid016

Asteroid017

Asteroid018

Asteroid019

Asteroid020

Asteroid021

Asteroid022

Asteroid023

Asteroid024

Asteroid025

Asteroid026

Asteroid027

Asteroid028

Asteroid029

Asteroid030

Asteroid031

Asteroid032

Asteroid033

Asteroid034

Asteroid035

Asteroid036

Asteroid037

Asteroid038

Asteroid039

Asteroid040

Asteroid041

Asteroid042

Asteroid043

Asteroid044

Asteroid045

Asteroid046

Asteroid047

Asteroid048

Asteroid049

Asteroid050

Asteroid051

Asteroid052

Asteroid053

Asteroid054

Asteroid055

Asteroid056

Asteroid057

Asteroid058

Asteroid059

Asteroid060

Asteroid061

Asteroid062

Asteroid063

Asteroid064

Asteroid065

Asteroid066

Asteroid067

Asteroid068

Asteroid069

Asteroid070

Asteroid071

Asteroid072

Asteroid073

Asteroid074

Asteroid075

Asteroid076

Asteroid077

Asteroid078

Asteroid079

Asteroid080

Asteroid081

Asteroid082

Asteroid083

Asteroid084

Asteroid085

Asteroid086

Asteroid087

Asteroid088

Asteroid089

Asteroid090

Asteroid091

Asteroid092

Asteroid093

Asteroid094

Asteroid095

Asteroid096

Asteroid097

Asteroid098

Asteroid099

Asteroid100

AsteroidCount

### class AsteroidPort

InvalidAsteroidPort

TerrestrialEquatorialJ2000

EclipticJ2000

OribitalMeanEquinox

Synchronous

Galactic

### `portId((Asteroid)arg1, (Asteroid.AsteroidPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (AsteroidPort) – Name of the port. See ‘AsteroidPort’ documentation for more information.

### `setArgumentOfPeriapsis((Asteroid)arg1, (float)argumentOfPeriapsis[, (Anim)animator]) -> None`

Setter for property argumentOfPeriapsis

**Parameters:**
- argumentOfPeriapsis (double) – Periapsis
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEccentricity((Asteroid)arg1, (float)eccentricity[, (Anim)animator]) -> None`

Setter for property eccentricity

**Parameters:**
- eccentricity (double) – Eccentricity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEpoch((Asteroid)arg1, (float)epoch[, (Anim)animator]) -> None`

Setter for property epoch

**Parameters:**
- epoch (double) – Epoch
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setInclination((Asteroid)arg1, (float)inclination[, (Anim)animator]) -> None`

Setter for property inclination

**Parameters:**
- inclination (double) – Inclination
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Asteroid)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Asteroid)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Label intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelNameOverride((Asteroid)arg1, (object)labelNameOverride) -> None`

Setter for property labelNameOverride

**Parameters:**
- labelNameOverride (str) – Label Text

### `setLongitudeOfAscendingNode((Asteroid)arg1, (float)longitudeOfAscendingNode[, (Anim)animator]) -> None`

Setter for property longitudeOfAscendingNode

**Parameters:**
- longitudeOfAscendingNode (double) – Ascending node
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeanAnomaly((Asteroid)arg1, (float)meanAnomaly[, (Anim)animator]) -> None`

Setter for property meanAnomaly

**Parameters:**
- meanAnomaly (double) – Mean anomaly
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitColor((Asteroid)arg1, (Vec3)orbitColor[, (Anim)animator]) -> None`

Setter for property orbitColor

**Parameters:**
- orbitColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((Asteroid)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double) – Orbit intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitThickness((Asteroid)arg1, (float)orbitThickness[, (Anim)animator]) -> None`

Setter for property orbitThickness

**Parameters:**
- orbitThickness (double) – Orbit thickness
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((Asteroid)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the Asteroid parent port in database.

### `setPointerIntensity((Asteroid)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Pointer intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Asteroid)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Pointer type

### `setSemiMajorAxis((Asteroid)arg1, (float)semiMajorAxis[, (Anim)animator]) -> None`

Setter for property semiMajorAxis

**Parameters:**
- semiMajorAxis (double) – Semi major axis
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainUserModelFilename((Asteroid)arg1, (object)terrainUserModelFilename) -> None`

Setter for property terrainUserModelFilename

**Parameters:**
- terrainUserModelFilename (str) – Model Path

### property: `property argumentOfPeriapsis`

Periapsis

### property: `property eccentricity`

Eccentricity

### property: `property epoch`

Epoch

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property inclination`

Inclination

### property: `property intensity`

Intensity

### property: `property labelIntensity`

Label intensity

### property: `property labelNameOverride`

Label Text

### property: `property longitudeOfAscendingNode`

Ascending node

### property: `property meanAnomaly`

Mean anomaly

### property: `property name`

Returns the name.

### property: `property orbitColor`

None( (skyExplorer.Asteroid)arg1) -> skyExplorer.Vec3

### property: `property orbitIntensity`

Orbit intensity

### property: `property orbitThickness`

Orbit thickness

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of the Asteroid parent port in database.

### property: `property pointerIntensity`

Pointer intensity

### property: `property pointerType`

Pointer type

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property semiMajorAxis`

Semi major axis

### property: `property terrainUserModelFilename`

Model Path

---

# skyExplorer.Audio

## class skyExplorer.Audio

### `clear((Audio)arg1) -> None`

Clear association between mono audio files and channels.

### `clearStereo((Audio)arg1) -> None`

Clear association between stereo audio files and channels.

### `load((Audio)arg1, (int)ouputId, (object)filename) -> None`

Load a mono audio file associated with a channel.

**Parameters:**
- ouputId (int) – Id of the channel used to read audio file.
- filename (str) – Path to the audio file to read. Can be a relative path to audio folder or an absolute path.

### `loadStereo((Audio)arg1, (int)channelId, (object)filename) -> None`

Load a stereo audio file associated with a channel.

**Parameters:**
- channelId (int) – Id of the channel used to read audio file.
- filename (str) – Path to the audio file to read. Can be a relative path to audio folder or an absolute path.

### `pause((Audio)arg1, (bool)value) -> None`

Toggle play and pause on current playing mono audio file.

param value: Use True to pause audio file, or False to play audio file. type value: bool

pause( (Audio)arg1, (int)association, (bool)value) -> None :Toggle play and pause on association. param association: Association to pause. type association: int param value: Use True to pause audio file, or False to play audio file. type value: bool

### `pauseStereo((Audio)arg1, (bool)value) -> None`

Toggle play and pause on current playing stereo audio file.

**Parameters:**
- value (bool) – Use True to pause audio file, or False to play audio file.

### `play((Audio)arg1, (Anim)anim) -> None`

Play current loaded mono sound. The load function must have been called before.

param anim: defaults to Anim() type anim: Anim, optional

play( (Audio)arg1, (int)association, (Anim)anim) -> None :Play specified association. The load function must have been called before. param association: Association to start. type association: int param anim: defaults to Anim() type anim: Anim, optional

### `playStereo((Audio)arg1, (Anim)anim) -> None`

Play current loaded mono sound. The loadStereo function must have been called before.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `seek((Audio)arg1, (int)time) -> None`

Change the current audio timing.

param time: Position to reach in the audio file (in seconds). type time: int

seek( (Audio)arg1, (int)association, (int)time) -> None :Change the current audio timing. param association: Association to start. type association: int param time: Position to reach in the audio file (in seconds). type time: int

### `seekStereo((Audio)arg1, (int)time) -> None`

Change the current audio timing.

**Parameters:**
- time (int) – Position to reach in the audio file (in seconds).

### `setVolume((Audio)arg1, (float)volume[, (Anim)animator]) -> None`

Setter for property volume param volume: Global current audio volume. type volume: double param animator: Anim used for property interpolation, defaults to Anim() type animator: Anim, optional

setVolume( (Audio)arg1, (int)channelId, (float)volume, (Anim)anim) -> None :Set the input volume of the given channel. param channelId: Id of the channel to modify volume. type channelId: int param volume: New audio volume of the channel. type volume: double param anim: Animation used to change the volume., defaults to Anim() type anim: Anim, optional

### `setVolumeDb((Audio)arg1, (float)volumeDb[, (Anim)animator]) -> None`

Setter for property volumeDb param volumeDb: Global current audio volume id decibel. type volumeDb: double param animator: Anim used for property interpolation, defaults to Anim() type animator: Anim, optional

setVolumeDb( (Audio)arg1, (int)channelId, (float)volumeDb, (Anim)anim) -> None :Set the input volume of the given channel. Same as setVolume but unit is decibel. param channelId: Id of the channel to modify volume. type channelId: int param volumeDb: New audio volume (in decibel) of the channel. type volumeDb: double param anim: Animation used to change the volume., defaults to Anim() type anim: Anim, optional

### `stop((Audio)arg1) -> None`

Stop current loaded mono audio files.

### `stopStereo((Audio)arg1) -> None`

Stop current loaded stereo audio files.

---

# skyExplorer.AudioLayer

## class skyExplorer.AudioLayer

### class AudioLayerName

InvalidAudioLayer

Layer001

Layer002

Layer003

Layer004

Layer005

Layer006

Layer007

Layer008

Layer009

Layer010

Layer011

Layer012

Layer013

Layer014

Layer015

Layer016

Layer017

Layer018

Layer019

Layer020

Layer021

Layer022

Layer023

Layer024

Layer025

Layer026

Layer027

Layer028

Layer029

Layer030

Layer031

Layer032

Layer033

Layer034

Layer035

Layer036

Layer037

Layer038

Layer039

Layer040

Layer041

Layer042

Layer043

Layer044

Layer045

Layer046

Layer047

Layer048

Layer049

Layer050

AudioLayerCount

### class AudioState

InvalidAudioState

AudioStateStop

AudioStatePlay

AudioStatePause

AudioStatePlayLoop

### `load((AudioLayer)arg1, (int)chanelId, (object)filename) -> None`

Load an audio file associated with a channel use -1 to let systeme output to chanel specfied on audio file (for multi chanel ac3 file for ex).

**Parameters:**
- chanelId (int) – Id of the channel used to read audio file.
- filename (str) – Path to the audio file to read. Can be a relative path to audio folder or an absolute path.

### `pause((AudioLayer)arg1) -> None`

Toggle play and pause on current playing audio file.

### `play((AudioLayer)arg1, (bool)loop) -> None`

Play current loaded sound. The load function must have been called before.

**Parameters:**
- loop (bool) – Play in loop or not.

### `seek((AudioLayer)arg1, (int)time, (Anim)anim) -> None`

Change the current audio timing.

**Parameters:**
- time (int) – Position to reach in the audio file (in seconds).
- anim (Anim, optional) – defaults to Anim()

### `setInputVolume((AudioLayer)arg1, (int)channelId, (float)volume) -> None`

Set the input volume of the given channel.

**Parameters:**
- channelId (int) – Id of the channel to modify volume.
- volume (double) – New audio volume of the channel in percent [0 1].

### `setInputVolumeDb((AudioLayer)arg1, (int)channelId, (float)volume) -> None`

Set the input volume of the given channel.

**Parameters:**
- channelId (int) – Id of the channel to modify volume.
- volume (double) – New audio volume of the channel in db [-72 0].

### `setOutputVolume((AudioLayer)arg1, (float)outputVolume[, (Anim)animator]) -> None`

Setter for property outputVolume

**Parameters:**
- outputVolume (double) – Global current audio layer volume in percent.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOutputVolumeDb((AudioLayer)arg1, (float)outputVolumeDb[, (Anim)animator]) -> None`

Setter for property outputVolumeDb

**Parameters:**
- outputVolumeDb (double) – Global current audio layer volume in db.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `stop((AudioLayer)arg1) -> None`

Stop current loaded mono audio files.

### `unload((AudioLayer)arg1) -> None`

Unload all loaded audio files and channels.

### property: `property audioDuration`

[Read-only]

Audio file duration in ms.

### property: `property audioPosition`

[Read-only]

Position in ms current file

### property: `property audioStartTime`

[Read-only]

Time when audio start in s (julian day)

### property: `property audioState`

[Read-only]

Audio status

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property outputVolume`

Global current audio layer volume in percent.

### property: `property outputVolumeDb`

Global current audio layer volume in db.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.AudioLite

## class skyExplorer.AudioLite

### `load((AudioLite)arg1, (object)filename) -> None`

Load an audio file.

**Parameters:**
- filename (str) – Path to the audio file to read. Can be a relative path to audio folder or an absolute path.

### `pause((AudioLite)arg1) -> None`

Pause the current playing audio file.

### `play((AudioLite)arg1, (Anim)anim) -> None`

Play the current playing audio file.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `seek((AudioLite)arg1, (float)time) -> None`

Change the current audio timing.

**Parameters:**
- time (double) – Position to reach in the audio file (in seconds).

### `setVolume((AudioLite)arg1, (float)volume) -> None`

Set the volume of the current loaded audio file.

**Parameters:**
- volume (double) – New volume for loaded audio file.

### `stop((AudioLite)arg1) -> None`

Stop the current playing audio file.

---

# skyExplorer.AudioPlayer

## class skyExplorer.AudioPlayer

### class AudioPlayerName

InvalidAudioPlayer

MainAudioPlayer

AudioPlayerCount

### `setOutputVolume((AudioPlayer)arg1, (float)outputVolume[, (Anim)animator]) -> None`

Setter for property outputVolume

**Parameters:**
- outputVolume (double) – Global audio volume in percent [0 1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOutputVolumeDb((AudioPlayer)arg1, (float)outputVolumeDb[, (Anim)animator]) -> None`

Setter for property outputVolumeDb

**Parameters:**
- outputVolumeDb (double) – Global audio volume in db [-72 0].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property instancedAudioLayer`

[Read-only]

List of current instancied audio layer

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property outputVolume`

Global audio volume in percent [0 1].

### property: `property outputVolumeDb`

Global audio volume in db [-72 0].

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.Body

## class skyExplorer.Body

### class PointerType

InvalidPointerType

Model3d

Legacy

Model1

Model1Bold

Model2

Model2Bold

Model3

Model3Bold

Model4

Model4Bold

Model5

Model5Bold

Model6

Model6Bold

Model7

Model7Bold

Model8

Model8Bold

Model9

Model9Bold

Model10

Model10Bold

---

# skyExplorer.Bolide

## class skyExplorer.Bolide

### class BolideName

InvalidBolide

Bolide001

BolideCount

### class DrawError

InvalidDrawError

NoError

PartiallyDrawnOnTerrain

DrawnOnTerrain

DrawnOutsideRange

### class Element

InvalidElement

NitrogenOxygen

Iron

Calcium

Magnesium

Sodium

Custom

### class ModelID

InvalidModelID

User

Chelyabinsk

ColoredFireball

### `play((Bolide)arg1, (float)speed) -> None`

Play the bolide animation with given speed.

**Parameters:**
- speed (double) – Bolide speed [km/s].

### `set((Bolide)arg1, (float)startAzimuth, (float)startHeight, (float)startAltitude, (float)endAzimuth, (float)endHeight, (float)endAltitude, (float)speed) -> int`

Sets the bolide start position from screen coordinates.

**Parameters:**
- startAzimuth (double) – Start azimuth [degrees] (dome space).
- startHeight (double) – Start height [degrees] (dome space).
- startAltitude (double) – Start point altitude [meters].
- endAzimuth (double) – End azimuth [degrees] (dome space).
- endHeight (double) – End height [degrees] (dome space).
- endAltitude (double) – End point altitude [meters].
- speed (double) – Bolide speed [km/s].

### `setElement((Bolide)arg1, (Bolide.Element)element, (Vec3)customColor, (Anim)anim) -> None`

Setup the element composing the bolide

**Parameters:**
- element (Element) – Chemical element
- customColor (Vec3, optional) – Custom color to use for the bolide., defaults to Vec3(0,0,0)
- anim (Anim, optional) – Color animation (only for custom color mode)., defaults to Anim()

### `setEndPosition((Bolide)arg1, (Vec3)endPosition) -> None`

Setter for property endPosition

**Parameters:**
- endPosition (Vec3) – End position of the bolide trajectory

### `setEvolution((Bolide)arg1, (float)evolution[, (Anim)animator]) -> None`

Setter for property evolution

**Parameters:**
- evolution (double) – Evolution of the bolide [0.0; +inf] (Only for User model) use an infinite animator to play the bolide.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Bolide)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the bolide. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModel((Bolide)arg1, (Bolide.ModelID)model, (object)filename) -> None`

Load a bolide model.

**Parameters:**
- model (ModelID) – Model index of the bolide
- filename (str, optional) – Path to the model file (optional, required for User model)., defaults to

### `setStartPosition((Bolide)arg1, (Vec3)startPosition) -> None`

Setter for property startPosition

**Parameters:**
- startPosition (Vec3) – Start position of the bolide trajectory

### property: `property element`

[Read-only]

Name of the element composing the bolide.

### property: `property elementColor`

[Read-only]

Color of the bolide (valid only for Custom element).

### property: `property endPosition`

End position of the bolide trajectory

### property: `property evolution`

Evolution of the bolide [0.0; +inf] (Only for User model) use an infinite animator to play the bolide.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the bolide. Usually in range [0;1].

### property: `property model`

[Read-only]

Name of the current displayed bolide model.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property startPosition`

Start position of the bolide trajectory

---

# skyExplorer.Camera

## class skyExplorer.Camera

### class CameraName

InvalidCamera

MainCamera

CameraCount

### class CameraPort

InvalidCameraPort

FixedBackground

Background

FixedForeground

Foreground

### class OrientationMode

InvalidOrientationMode

SmoothXYZR

XYZR

HPRD

### class PositionMode

InvalidPositionMode

XYZ

LBR

### class ZoomFormula

InvalidZoomFormula

GreatCircleHPR

GreatCircle

FisheyePlane

VerticalCircle

### `addChild((Camera)arg1, (int)child, (Camera.CameraPort)port) -> None`

Add a child object to the camera scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (CameraPort) – Coordinate system to use for adding child. See CameraPort documentation for more information.

### `defaultResolutionRatioStrength((Camera)arg1) -> float`

### `portId((Camera)arg1, (Camera.CameraPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (CameraPort) – Name of the port. See ‘CameraPort’ documentation for more information.

### `setActiveTarget((Camera)arg1, (bool)activeTarget[, (Anim)animator]) -> None`

Setter for property activeTarget

**Parameters:**
- activeTarget (bool) – Stereo active On Off
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setActiveTrackStereo((Camera)arg1, (bool)activeTrackStereo[, (Anim)animator]) -> None`

Setter for property activeTrackStereo

**Parameters:**
- activeTrackStereo (bool) – False by defaut
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDomeMeanPixelRatio((Camera)arg1, (float)domeMeanPixelRatio[, (Anim)animator]) -> None`

Setter for property domeMeanPixelRatio

**Parameters:**
- domeMeanPixelRatio (double) – Mean pixel ratio of the dome where the stars are displayed
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEyeDistance((Camera)arg1, (float)eyeDistance[, (Anim)animator]) -> None`

Setter for property eyeDistance

**Parameters:**
- eyeDistance (double) – Stereo eye separation value
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFocusDegree((Camera)arg1, (float)focusDegree[, (Anim)animator]) -> None`

Setter for property focusDegree

**Parameters:**
- focusDegree (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationD((Camera)arg1, (float)orientationD[, (Anim)animator]) -> None`

Setter for property orientationD

**Parameters:**
- orientationD (double) – Set the distance value of camera orientation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationH((Camera)arg1, (float)orientationH[, (Anim)animator]) -> None`

Setter for property orientationH

**Parameters:**
- orientationH (double) – Set the heading value of camera orientation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationHPR((Camera)arg1, (Vec3)orientationHPR[, (Anim)animator]) -> None`

Setter for property orientationHPR

**Parameters:**
- orientationHPR (Vec3) – HPR orientation of the camera relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationHPRD((Camera)arg1, (Vec4)value, (Anim)anim, (int)track) -> None`

Change the HPRD orientation of the camera, relative to given coordinate system.

**Parameters:**
- value (Vec4) – Target HPRD orientation value.
- anim (Anim, optional) – Animator used for HPRD orientation interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setOrientationP((Camera)arg1, (float)orientationP[, (Anim)animator]) -> None`

Setter for property orientationP

**Parameters:**
- orientationP (double) – Set the pitch value of camera orientation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationR((Camera)arg1, (float)orientationR[, (Anim)animator]) -> None`

Setter for property orientationR

**Parameters:**
- orientationR (double) – Set the roll value of camera orientation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationSmoothXYZR((Camera)arg1, (Vec4)value, (Anim)anim, (int)track) -> None`

Smoothly change the XYZR orientation of the camera, relative to given coordinate system.

**Parameters:**
- value (Vec4) – Target XYZR orientation value.
- anim (Anim, optional) – Animator used for XYZR orientation interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port)., defaults to -1

### `setOrientationXYZ((Camera)arg1, (Vec3)orientationXYZ[, (Anim)animator]) -> None`

Setter for property orientationXYZ

**Parameters:**
- orientationXYZ (Vec3) – XYZ orientation of the camera relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationXYZR((Camera)arg1, (Vec4)value, (Anim)anim, (int)track) -> None`

Change the XYZR orientation of the camera, relative to given coordinate system.

**Parameters:**
- value (Vec4) – Target XYZR orientation value.
- anim (Anim, optional) – Animator used for XYZR orientation interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionB((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera longitude position, relative to given coordinate system.

**Parameters:**
- value (double) – Target longitude position value.
- anim (Anim, optional) – Animator used for longitude position interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionL((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera latitude position, relative to given coordinate system.

**Parameters:**
- value (double) – Target latitude position value.
- anim (Anim, optional) – Animator used for latitude position interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionLBR((Camera)arg1, (Vec3)value, (Anim)anim, (int)track) -> None`

Change the LBR position of the camera, relative to given coordinate system.

**Parameters:**
- value (Vec3) – Target LBR position value.
- anim (Anim, optional) – Animator used for LBR position interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionR((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera distance to body, relative to given coordinate system.

**Parameters:**
- value (double) – Target distance value.
- anim (Anim, optional) – Animator used for distance value interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionX((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera X coordinate around body, relative to given coordinate system.

**Parameters:**
- value (double) – Target X value.
- anim (Anim, optional) – Animator used for latitude position interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionXYZ((Camera)arg1, (Vec3)value, (Anim)anim, (int)track) -> None`

Change the camera XYZ position, relative to given coordinate system.

**Parameters:**
- value (Vec3) – Target XYZ position.
- anim (Anim, optional) – Animator used for distance value interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionY((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera Y coordinate around body, relative to given coordinate system.

**Parameters:**
- value (double) – Target Y value.
- anim (Anim, optional) – Animator used for longitude position interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setPositionZ((Camera)arg1, (float)value, (Anim)anim, (int)track) -> None`

Change the camera Z coordinate around body, relative to given coordinate system.

**Parameters:**
- value (double) – Target Z value.
- anim (Anim, optional) – Animator used for distance value interpolation., defaults to Anim()
- track (int, optional) – Database id of the referencial (For example, celestial body port). Set -1 to use current coordinate system., defaults to -1

### `setResolutionRatioStrength((Camera)arg1, (float)resolutionRatioStrength[, (Anim)animator]) -> None`

Setter for property resolutionRatioStrength

**Parameters:**
- resolutionRatioStrength (double) – Strength of the effect of the ratio between the dome and skyEx mean pixel ratio
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setStereoPosition((Camera)arg1, (int)stereoPosition[, (Anim)animator]) -> None`

Setter for property stereoPosition

**Parameters:**
- stereoPosition (int)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setStereoRatio((Camera)arg1, (float)stereoRatio[, (Anim)animator]) -> None`

Setter for property stereoRatio

**Parameters:**
- stereoRatio (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTarget((Camera)arg1, (Vec2)target[, (Anim)animator]) -> None`

Setter for property target param target: Camera target {azimuth, height}. type target: Vec2 param animator: Anim used for property interpolation, defaults to Anim() type animator: Anim, optional

setTarget( (Camera)arg1, (Vec3)arg2) -> None :Set target from Vec3 {azimuth, height, ignored}. DEPRECATED: please prefer Vec2 parameter over Vec3 setTarget( (Camera)arg1, (Vec3)arg2, (Anim)arg3) -> None :Set target from Vec3 {azimuth, height, ignored}. DEPRECATED: please prefer Vec2 parameter over Vec3

### `setTargetAzimuth((Camera)arg1, (float)targetAzimuth[, (Anim)animator]) -> None`

Setter for property targetAzimuth

**Parameters:**
- targetAzimuth (double) – Camera target azimuth.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTargetHeight((Camera)arg1, (float)targetHeight[, (Anim)animator]) -> None`

Setter for property targetHeight

**Parameters:**
- targetHeight (double) – Camera target height.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTraceMode((Camera)arg1, (bool)traceMode) -> None`

Setter for property traceMode

**Parameters:**
- traceMode (bool) – Flag used to know if trace mode is enabled.

### `setZoomFormula((Camera)arg1, (Camera.ZoomFormula)zoomFormula) -> None`

Setter for property zoomFormula

**Parameters:**
- zoomFormula (ZoomFormula) – Zoom formula.

### `setZoomFov((Camera)arg1, (float)zoomFov[, (Anim)animator]) -> None`

Setter for property zoomFov

**Parameters:**
- zoomFov (double) – Fov angle in degrees after zooming.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setZoomPosition((Camera)arg1, (Vec3)position, (int)track, (Anim)anim, (Camera.PositionMode)mode) -> None`

Zoom on a body.

**Parameters:**
- position (Vec3) – Position to zoom in track referencial.
- track (int) – Database id of the referencial (For example, celestial body port).
- anim (Anim, optional) – Animator used for position value interpolation., defaults to Anim()
- mode (PositionMode, optional) – Mode used for zooming. See PositionMode documentation for more information, defaults to PositionMode::XYZ

### `takeScreenshot((Camera)arg1, (object)value) -> None`

Save the image from every channel in specified file.

**Parameters:**
- value (str) – Output file name.

### property: `property activeTarget`

Stereo active On Off

### property: `property activeTrackStereo`

False by defaut

### property: `property domeMeanPixelRatio`

Mean pixel ratio of the dome where the stars are displayed

### property: `property eyeDistance`

Stereo eye separation value

### property: `property focusDegree`

### property: `property icrfToTrack`

[Read-only]

Matrix transformation between ICRF coordinate system and current coordinate system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property orientationHPR`

HPR orientation of the camera relative to it’s parent coordinate system.

### property: `property orientationHPRD`

[Read-only]

HPRD orientation of the camera relative to it’s parent coordinate system.

### property: `property orientationMode`

[Read-only]

Get the orientation mode.

### property: `property orientationTrack`

[Read-only]

Parent port used to compute the orientation of the camera.

### property: `property orientationXYZR`

[Read-only]

XYZR orientation of the camera relative to it’s parent coordinate system.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

[Read-only]

Position parent database (id + port).

### property: `property parentFamily`

[Read-only]

Position parent family.

### property: `property parentIndex`

[Read-only]

Position parent index (in its family).

### property: `property parentOri`

[Read-only]

Orientation parent database (id + port).

### property: `property parentOriFamily`

[Read-only]

Orientation parent family.

### property: `property parentOriIndex`

[Read-only]

Orientation parent index (in its family).

### property: `property port`

[Read-only]

Position port.

### property: `property portOri`

[Read-only]

Orientation port.

### property: `property position`

[Read-only]

XYZ position of the camera in ICRF coordinate system.

### property: `property positionB`

[Read-only]

B position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property positionL`

[Read-only]

L position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property positionLBR`

[Read-only]

LBR position of the camera, relative to it’s parent coordinate system.

### property: `property positionMode`

[Read-only]

Get the position mode.

### property: `property positionR`

[Read-only]

R position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property positionTrack`

[Read-only]

Parent port used to compute the position of the camera.

### property: `property positionX`

[Read-only]

X position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property positionXYZ`

[Read-only]

XYZ position of the camera, relative to it’s parent coordinate system.

### property: `property positionY`

[Read-only]

Y position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property positionZ`

[Read-only]

Z position coordinate of the camera, relative to it’s parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property resolutionRatioStrength`

Strength of the effect of the ratio between the dome and skyEx mean pixel ratio

### property: `property stereoPosition`

### property: `property stereoRatio`

### property: `property target`

Camera target {azimuth, height}.

### property: `property targetAzimuth`

Camera target azimuth.

### property: `property targetHeight`

Camera target height.

### property: `property traceMode`

Flag used to know if trace mode is enabled.

### property: `property trackToDome`

[Read-only]

Matrix transformation between current coordinate system to dome one’s.

### property: `property zoomFormula`

Zoom formula.

### property: `property zoomFov`

Fov angle in degrees after zooming.

### property: `property zoomPosition`

[Read-only]

Return the position of the zoom.

### property: `property zoomPositionTrack`

[Read-only]

Return the zoom target body id.

---

# skyExplorer.Chart2D

## class skyExplorer.Chart2D

### class Chart2DName

InvalidChart2D

Chart2D001

Chart2D002

Chart2D003

Chart2D004

Chart2D005

Chart2D006

Chart2D007

Chart2D008

Chart2D009

Chart2D010

Chart2DCount

### class ChartType

InvalidChartType

Histogram

Pie

### `remove((Chart2D)arg1) -> None`

Remove chart2D from scene graph.

### `setCategory10Color((Chart2D)arg1, (Vec3)category10Color[, (Anim)animator]) -> None`

Setter for property category10Color

**Parameters:**
- category10Color (Vec3) – Change color of the tenth category. If category count is lesser than 10, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory10Text((Chart2D)arg1, (object)category10Text) -> None`

Setter for property category10Text

**Parameters:**
- category10Text (str) – Change text of the tenth category. If category count is lesser than 10, it has no effect.

### `setCategory10Value((Chart2D)arg1, (float)category10Value[, (Anim)animator]) -> None`

Setter for property category10Value

**Parameters:**
- category10Value (double) – Change value of the tenth category. If category count is lesser than 10, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory1Color((Chart2D)arg1, (Vec3)category1Color[, (Anim)animator]) -> None`

Setter for property category1Color

**Parameters:**
- category1Color (Vec3) – Change color of the first category. If category count is lesser than 1, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory1Text((Chart2D)arg1, (object)category1Text) -> None`

Setter for property category1Text

**Parameters:**
- category1Text (str) – Change text of the first category. If category count is lesser than 1, it has no effect.

### `setCategory1Value((Chart2D)arg1, (float)category1Value[, (Anim)animator]) -> None`

Setter for property category1Value

**Parameters:**
- category1Value (double) – Change value of the first category. If category count is lesser than 1, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory2Color((Chart2D)arg1, (Vec3)category2Color[, (Anim)animator]) -> None`

Setter for property category2Color

**Parameters:**
- category2Color (Vec3) – Change color of the second category. If category count is lesser than 2, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory2Text((Chart2D)arg1, (object)category2Text) -> None`

Setter for property category2Text

**Parameters:**
- category2Text (str) – Change text of the second category. If category count is lesser than 2, it has no effect.

### `setCategory2Value((Chart2D)arg1, (float)category2Value[, (Anim)animator]) -> None`

Setter for property category2Value

**Parameters:**
- category2Value (double) – Change value of the second category. If category count is lesser than 2, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory3Color((Chart2D)arg1, (Vec3)category3Color[, (Anim)animator]) -> None`

Setter for property category3Color

**Parameters:**
- category3Color (Vec3) – Change color of the third category. If category count is lesser than 3, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory3Text((Chart2D)arg1, (object)category3Text) -> None`

Setter for property category3Text

**Parameters:**
- category3Text (str) – Change text of the third category. If category count is lesser than 3, it has no effect.

### `setCategory3Value((Chart2D)arg1, (float)category3Value[, (Anim)animator]) -> None`

Setter for property category3Value

**Parameters:**
- category3Value (double) – Change value of the third category. If category count is lesser than 3, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory4Color((Chart2D)arg1, (Vec3)category4Color[, (Anim)animator]) -> None`

Setter for property category4Color

**Parameters:**
- category4Color (Vec3) – Change color of the fourth category. If category count is lesser than 4, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory4Text((Chart2D)arg1, (object)category4Text) -> None`

Setter for property category4Text

**Parameters:**
- category4Text (str) – Change text of the fourth category. If category count is lesser than 4, it has no effect.

### `setCategory4Value((Chart2D)arg1, (float)category4Value[, (Anim)animator]) -> None`

Setter for property category4Value

**Parameters:**
- category4Value (double) – Change value of the fourth category. If category count is lesser than 4, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory5Color((Chart2D)arg1, (Vec3)category5Color[, (Anim)animator]) -> None`

Setter for property category5Color

**Parameters:**
- category5Color (Vec3) – Change color of the fifth category. If category count is lesser than 5, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory5Text((Chart2D)arg1, (object)category5Text) -> None`

Setter for property category5Text

**Parameters:**
- category5Text (str) – Change text of the fifth category. If category count is lesser than 5, it has no effect.

### `setCategory5Value((Chart2D)arg1, (float)category5Value[, (Anim)animator]) -> None`

Setter for property category5Value

**Parameters:**
- category5Value (double) – Change value of the fifth category. If category count is lesser than 5, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory6Color((Chart2D)arg1, (Vec3)category6Color[, (Anim)animator]) -> None`

Setter for property category6Color

**Parameters:**
- category6Color (Vec3) – Change color of the sixth category. If category count is lesser than 6, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory6Text((Chart2D)arg1, (object)category6Text) -> None`

Setter for property category6Text

**Parameters:**
- category6Text (str) – Change text of the sixth category. If category count is lesser than 6, it has no effect.

### `setCategory6Value((Chart2D)arg1, (float)category6Value[, (Anim)animator]) -> None`

Setter for property category6Value

**Parameters:**
- category6Value (double) – Change value of the sixth category. If category count is lesser than 6, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory7Color((Chart2D)arg1, (Vec3)category7Color[, (Anim)animator]) -> None`

Setter for property category7Color

**Parameters:**
- category7Color (Vec3) – Change color of the seventh category. If category count is lesser than 7, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory7Text((Chart2D)arg1, (object)category7Text) -> None`

Setter for property category7Text

**Parameters:**
- category7Text (str) – Change text of the seventh category. If category count is lesser than 7, it has no effect.

### `setCategory7Value((Chart2D)arg1, (float)category7Value[, (Anim)animator]) -> None`

Setter for property category7Value

**Parameters:**
- category7Value (double) – Change value of the seventh category. If category count is lesser than 7, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory8Color((Chart2D)arg1, (Vec3)category8Color[, (Anim)animator]) -> None`

Setter for property category8Color

**Parameters:**
- category8Color (Vec3) – Change color of the heighth category. If category count is lesser than 8, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory8Text((Chart2D)arg1, (object)category8Text) -> None`

Setter for property category8Text

**Parameters:**
- category8Text (str) – Change text of the heighth category. If category count is lesser than 8, it has no effect.

### `setCategory8Value((Chart2D)arg1, (float)category8Value[, (Anim)animator]) -> None`

Setter for property category8Value

**Parameters:**
- category8Value (double) – Change value of the heighth category. If category count is lesser than 8, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory9Color((Chart2D)arg1, (Vec3)category9Color[, (Anim)animator]) -> None`

Setter for property category9Color

**Parameters:**
- category9Color (Vec3) – Change color of the ninth category. If category count is lesser than 9, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategory9Text((Chart2D)arg1, (object)category9Text) -> None`

Setter for property category9Text

**Parameters:**
- category9Text (str) – Change text of the ninth category. If category count is lesser than 9, it has no effect.

### `setCategory9Value((Chart2D)arg1, (float)category9Value[, (Anim)animator]) -> None`

Setter for property category9Value

**Parameters:**
- category9Value (double) – Change value of the ninth category. If category count is lesser than 9, it has no effect.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCategoryCount((Chart2D)arg1, (int)categoryCount) -> None`

Setter for property categoryCount

**Parameters:**
- categoryCount (int) – Number of section in the chart2D. Must be in range [0;10].

### `setChartType((Chart2D)arg1, (Chart2D.ChartType)chartType) -> None`

Setter for property chartType

**Parameters:**
- chartType (ChartType) – Type of chart2D. See ChartType documentation for available values.

### `setDistance((Chart2D)arg1, (float)distance[, (Anim)animator]) -> None`

Setter for property distance

**Parameters:**
- distance (double) – Distance from the chart2D to the center of it’s parent (unit is parent radius).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Chart2D)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the chart2D. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((Chart2D)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Current parent id. This id refer to the parent port where the chart is hooked.

### `setPosition((Chart2D)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – Position of the chart2D, according to parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSize((Chart2D)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Apparent size of the chart 2D on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property category10Color`

Change color of the tenth category. If category count is lesser than 10, it has no effect.

### property: `property category10Text`

Change text of the tenth category. If category count is lesser than 10, it has no effect.

### property: `property category10Value`

Change value of the tenth category. If category count is lesser than 10, it has no effect.

### property: `property category1Color`

Change color of the first category. If category count is lesser than 1, it has no effect.

### property: `property category1Text`

Change text of the first category. If category count is lesser than 1, it has no effect.

### property: `property category1Value`

Change value of the first category. If category count is lesser than 1, it has no effect.

### property: `property category2Color`

Change color of the second category. If category count is lesser than 2, it has no effect.

### property: `property category2Text`

Change text of the second category. If category count is lesser than 2, it has no effect.

### property: `property category2Value`

Change value of the second category. If category count is lesser than 2, it has no effect.

### property: `property category3Color`

Change color of the third category. If category count is lesser than 3, it has no effect.

### property: `property category3Text`

Change text of the third category. If category count is lesser than 3, it has no effect.

### property: `property category3Value`

Change value of the third category. If category count is lesser than 3, it has no effect.

### property: `property category4Color`

Change color of the fourth category. If category count is lesser than 4, it has no effect.

### property: `property category4Text`

Change text of the fourth category. If category count is lesser than 4, it has no effect.

### property: `property category4Value`

Change value of the fourth category. If category count is lesser than 4, it has no effect.

### property: `property category5Color`

Change color of the fifth category. If category count is lesser than 5, it has no effect.

### property: `property category5Text`

Change text of the fifth category. If category count is lesser than 5, it has no effect.

### property: `property category5Value`

Change value of the fifth category. If category count is lesser than 5, it has no effect.

### property: `property category6Color`

Change color of the sixth category. If category count is lesser than 6, it has no effect.

### property: `property category6Text`

Change text of the sixth category. If category count is lesser than 6, it has no effect.

### property: `property category6Value`

Change value of the sixth category. If category count is lesser than 6, it has no effect.

### property: `property category7Color`

Change color of the seventh category. If category count is lesser than 7, it has no effect.

### property: `property category7Text`

Change text of the seventh category. If category count is lesser than 7, it has no effect.

### property: `property category7Value`

Change value of the seventh category. If category count is lesser than 7, it has no effect.

### property: `property category8Color`

Change color of the heighth category. If category count is lesser than 8, it has no effect.

### property: `property category8Text`

Change text of the heighth category. If category count is lesser than 8, it has no effect.

### property: `property category8Value`

Change value of the heighth category. If category count is lesser than 8, it has no effect.

### property: `property category9Color`

Change color of the ninth category. If category count is lesser than 9, it has no effect.

### property: `property category9Text`

Change text of the ninth category. If category count is lesser than 9, it has no effect.

### property: `property category9Value`

Change value of the ninth category. If category count is lesser than 9, it has no effect.

### property: `property categoryCount`

Number of section in the chart2D. Must be in range [0;10].

### property: `property chartType`

Type of chart2D. See ChartType documentation for available values.

### property: `property distance`

Distance from the chart2D to the center of it’s parent (unit is parent radius).

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the chart2D. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Current parent id. This id refer to the parent port where the chart is hooked.

### property: `property position`

Position of the chart2D, according to parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property size`

Apparent size of the chart 2D on the dome.

---

# skyExplorer.Clock

## class skyExplorer.Clock

### class ClockName

InvalidClock

Clock001

Clock002

Clock003

Clock004

Clock005

Clock006

Clock007

Clock008

Clock009

Clock010

Clock011

ClockCount

### class Modelset

InvalidModelset

SystemClock001

### `setBackgroundColor((Clock)arg1, (Vec3)backgroundColor[, (Anim)animator]) -> None`

Setter for property backgroundColor

**Parameters:**
- backgroundColor (Vec3) – Color of the background of the clock. Color will be multiplied by the background texture color.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setBackgroundTexture((Clock)arg1, (object)backgroundTexture) -> None`

Setter for property backgroundTexture

**Parameters:**
- backgroundTexture (str) – Path to the background texture. Relative to user folder.

### `setDisplaySecondsHand((Clock)arg1, (bool)displaySecondsHand) -> None`

Setter for property displaySecondsHand

**Parameters:**
- displaySecondsHand (bool) – Displays, respectively hides the seconds hand.

### `setDistance((Clock)arg1, (float)distance[, (Anim)animator]) -> None`

Setter for property distance

**Parameters:**
- distance (double) – Distance of the clock from it’s parent center. Default is 1.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setForegroundColor((Clock)arg1, (Vec3)foregroundColor[, (Anim)animator]) -> None`

Setter for property foregroundColor

**Parameters:**
- foregroundColor (Vec3) – Color of the foreground of the clock. Color will be multiplied by the foreground texture color.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setForegroundTexture((Clock)arg1, (object)foregroundTexture) -> None`

Setter for property foregroundTexture

**Parameters:**
- foregroundTexture (str) – Path to the foreground texture. Relative to user folder.

### `setHoursHandColor((Clock)arg1, (Vec3)hoursHandColor[, (Anim)animator]) -> None`

Setter for property hoursHandColor

**Parameters:**
- hoursHandColor (Vec3) – Color of the hours hand of the clock. Color will be multiplied by the hours hand texture color.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHoursHandTexture((Clock)arg1, (object)hoursHandTexture) -> None`

Setter for property hoursHandTexture

**Parameters:**
- hoursHandTexture (str) – Path to the hours hand texture. Relative to user folder.

### `setIntensity((Clock)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the clock. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMinutesHandColor((Clock)arg1, (Vec3)minutesHandColor[, (Anim)animator]) -> None`

Setter for property minutesHandColor

**Parameters:**
- minutesHandColor (Vec3) – Color of the minutes hand of the clock. Color will be multiplied by the minutes hand texture color.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMinutesHandTexture((Clock)arg1, (object)minutesHandTexture) -> None`

Setter for property minutesHandTexture

**Parameters:**
- minutesHandTexture (str) – Path to the minutes hand texture. Relative to user folder.

### `setModelset((Clock)arg1, (Clock.Modelset)modelset) -> None`

Change the modelset of the clock.

**Parameters:**
- modelset (Modelset)

### `setParent((Clock)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the clock’s parent port in database.

### `setPosition((Clock)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – Position of the clock relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSecondsHandColor((Clock)arg1, (Vec3)secondsHandColor[, (Anim)animator]) -> None`

Setter for property secondsHandColor

**Parameters:**
- secondsHandColor (Vec3) – Color of the seconds hand of the clock. Color will be multiplied by the seconds hand texture color.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSecondsHandTexture((Clock)arg1, (object)secondsHandTexture) -> None`

Setter for property secondsHandTexture

**Parameters:**
- secondsHandTexture (str) – Path to the seconds hand texture. Relative to user folder.

### `setSize((Clock)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Size of the clock. Default is 1.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTimezoneName((Clock)arg1, (object)timezoneName) -> None`

Setter for property timezoneName

**Parameters:**
- timezoneName (str) – Timezone used to convert time displayed by the clock. Timezone strings are the same as Insert text.

### property: `property backgroundColor`

Color of the background of the clock. Color will be multiplied by the background texture color.

### property: `property backgroundTexture`

Path to the background texture. Relative to user folder.

### property: `property displaySecondsHand`

Displays, respectively hides the seconds hand.

### property: `property distance`

Distance of the clock from it’s parent center. Default is 1.

### property: `property foregroundColor`

Color of the foreground of the clock. Color will be multiplied by the foreground texture color.

### property: `property foregroundTexture`

Path to the foreground texture. Relative to user folder.

### property: `property hoursHandColor`

Color of the hours hand of the clock. Color will be multiplied by the hours hand texture color.

### property: `property hoursHandTexture`

Path to the hours hand texture. Relative to user folder.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the clock. Usually in range [0;1].

### property: `property minutesHandColor`

Color of the minutes hand of the clock. Color will be multiplied by the minutes hand texture color.

### property: `property minutesHandTexture`

Path to the minutes hand texture. Relative to user folder.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of the clock’s parent port in database.

### property: `property position`

Position of the clock relative to it’s parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property secondsHandColor`

Color of the seconds hand of the clock. Color will be multiplied by the seconds hand texture color.

### property: `property secondsHandTexture`

Path to the seconds hand texture. Relative to user folder.

### property: `property size`

Size of the clock. Default is 1.

### property: `property timezoneName`

Timezone used to convert time displayed by the clock. Timezone strings are the same as Insert text.

---

# skyExplorer.Comet

## class skyExplorer.Comet

### class CometModelSet

InvalidCometModelSet

Basic

Generic3D

Halley3D

UserModel

HaleBopp3D

Bradfield3D

Hyakutake3D

McNaught3D

### class CometName

InvalidComet

Comet001

Comet002

Comet003

Comet004

Comet005

Comet006

Comet007

Comet008

Comet009

Comet010

Comet011

Comet012

Comet013

Comet014

Comet015

Comet016

Comet017

Comet018

Comet019

Comet020

Comet021

Comet022

Comet023

Comet024

Comet025

Comet026

Comet027

Comet028

Comet029

Comet030

Comet031

Comet032

Comet033

Comet034

Comet035

Comet036

Comet037

Comet038

Comet039

Comet040

Comet041

Comet042

Comet043

Comet044

Comet045

Comet046

Comet047

Comet048

Comet049

Comet050

Comet051

Comet052

Comet053

Comet054

Comet055

Comet056

Comet057

Comet058

Comet059

Comet060

Comet061

Comet062

Comet063

Comet064

Comet065

Comet066

Comet067

Comet068

Comet069

Comet070

Comet071

Comet072

Comet073

Comet074

Comet075

Comet076

Comet077

Comet078

Comet079

Comet080

Comet081

Comet082

Comet083

Comet084

Comet085

Comet086

Comet087

Comet088

Comet089

Comet090

Comet091

Comet092

Comet093

Comet094

Comet095

Comet096

Comet097

Comet098

Comet099

Comet100

CometCount

### class CometPort

InvalidCometPort

TerrestrialEquatorialJ2000

EclipticJ2000

OribitalMeanEquinox

Synchronous

Galactic

### `portId((Comet)arg1, (Comet.CometPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (CometPort) – Name of the port. See ‘CometPort’ documentation for more information.

### `setArgumentOfPeriapsis((Comet)arg1, (float)argumentOfPeriapsis[, (Anim)animator]) -> None`

Setter for property argumentOfPeriapsis

**Parameters:**
- argumentOfPeriapsis (double) – Periapsis
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDistanceToPeriapsis((Comet)arg1, (float)distanceToPeriapsis[, (Anim)animator]) -> None`

Setter for property distanceToPeriapsis

**Parameters:**
- distanceToPeriapsis (double) – Distance to periapsis
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEccentricity((Comet)arg1, (float)eccentricity[, (Anim)animator]) -> None`

Setter for property eccentricity

**Parameters:**
- eccentricity (double) – Eccentricity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setInclination((Comet)arg1, (float)inclination[, (Anim)animator]) -> None`

Setter for property inclination

**Parameters:**
- inclination (double) – Inclination
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Comet)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Comet)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelNameOverride((Comet)arg1, (object)labelNameOverride) -> None`

Setter for property labelNameOverride

**Parameters:**
- labelNameOverride (str) – Label Text

### `setLongitudeOfAscendingNode((Comet)arg1, (float)longitudeOfAscendingNode[, (Anim)animator]) -> None`

Setter for property longitudeOfAscendingNode

**Parameters:**
- longitudeOfAscendingNode (double) – Ascending node
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModelScale((Comet)arg1, (float)modelScale[, (Anim)animator]) -> None`

Setter for property modelScale

**Parameters:**
- modelScale (double) – Model Scale
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((Comet)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double) – Orbit intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitThickness((Comet)arg1, (float)orbitThickness[, (Anim)animator]) -> None`

Setter for property orbitThickness

**Parameters:**
- orbitThickness (double) – Orbit thickness
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((Comet)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Pointer intensity
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Comet)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Pointer type

### `setStandardModelName((Comet)arg1, (Comet.CometModelSet)standardModelName) -> None`

Setter for property standardModelName

**Parameters:**
- standardModelName (CometModelSet) – Model Path

### `setTimeOfLastPeriapsis((Comet)arg1, (float)timeOfLastPeriapsis[, (Anim)animator]) -> None`

Setter for property timeOfLastPeriapsis

**Parameters:**
- timeOfLastPeriapsis (double) – Date and time of the last periapsis.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUserModelFilename((Comet)arg1, (object)userModelFilename) -> None`

Setter for property userModelFilename

**Parameters:**
- userModelFilename (str)

### property: `property argumentOfPeriapsis`

Periapsis

### property: `property distanceToPeriapsis`

Distance to periapsis

### property: `property eccentricity`

Eccentricity

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property inclination`

Inclination

### property: `property intensity`

Intensity

### property: `property labelIntensity`

Intensity

### property: `property labelNameOverride`

Label Text

### property: `property longitudeOfAscendingNode`

Ascending node

### property: `property modelScale`

Model Scale

### property: `property name`

Returns the name.

### property: `property orbitIntensity`

Orbit intensity

### property: `property orbitThickness`

Orbit thickness

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Pointer intensity

### property: `property pointerType`

Pointer type

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property standardModelName`

Model Path

### property: `property timeOfLastPeriapsis`

Date and time of the last periapsis.

### property: `property userModelFilename`

None( (skyExplorer.Comet)arg1) -> object

---

# skyExplorer.Comment

## class skyExplorer.Comment

### `line((Comment)arg1, (object)text) -> None`

Send a comment line (that can be captured by recording)

**Parameters:**
- text (str)

---

# skyExplorer.Constellation

## class skyExplorer.Constellation

### class ConstellationName

InvalidConstellation

And

Ant

Aps

Aqr

Aql

Ara

Ari

Aur

Boo

Cae

Cam

Cnc

Cvn

CMa

CMi

Cap

Car

Cas

Cen

Cep

Cet

Cha

Cir

Col

Com

CrA

CrB

Crv

Crt

Cru

Cyg

Del

Dor

Dra

Equ

Eri

For

Gem

Gru

Her

Hor

Hya

Hyi

Ind

Lac

Leo

Lmi

Lep

Lib

Lup

Lyn

Lyr

Men

Mic

Mon

Mus

Nor

Oct

Oph

Ori

Pav

Peg

Per

Phe

Pic

Psc

PsA

Pup

Pyx

Ret

Sge

Sgr

Sco

Scl

Sct

Ser

Sex

Tau

Tel

Tri

Tra

Tuc

UMa

UMi

Vel

Vir

Vol

Vul

ASTERISM_GDi

ASTERISM_SpT

ASTERISM_STr

ASTERISM_GSP

ASTERISM_WTr

ASTERISM_WHx

ASTERISM_NCr

ASTERISM_WAs

ASTERISM_KSt

ASTERISM_Bfl

ASTERISM_Kit

ASTERISM_Sal

ASTERISM_SSR

ASTERISM_CoH

ASTERISM_BDr

ASTERISM_LDr

ASTERISM_Ptr

ASTERISM_HDr

ASTERISM_HMG

ASTERISM_Goa

ASTERISM_Urn

ASTERISM_OrB

ASTERISM_OrS

ASTERISM_OSh

ASTERISM_OrC

ASTERISM_HWl

ASTERISM_HSr

ASTERISM_HHy

ASTERISM_Tea

ASTERISM_Ter

ASTERISM_ECr

ASTERISM_FCr

ASTERISM_Sic

ASTERISM_DCr

ASTERISM_Cir

ASTERISM_BA1

ASTERISM_BA2

CUSTOM_1001

CUSTOM_1002

CUSTOM_1003

CUSTOM_1004

CUSTOM_1005

CUSTOM_1006

CUSTOM_1007

CUSTOM_1008

CUSTOM_1009

CUSTOM_1010

CUSTOM_1011

CUSTOM_1012

CUSTOM_1013

CUSTOM_1014

CUSTOM_1015

CUSTOM_1016

CUSTOM_1017

CUSTOM_1018

CUSTOM_1019

CUSTOM_1020

CUSTOM_1021

CUSTOM_1022

CUSTOM_1023

CUSTOM_1024

CUSTOM_1025

CUSTOM_1026

CUSTOM_1027

CUSTOM_1028

CUSTOM_1029

CUSTOM_1030

CUSTOM_1031

CUSTOM_1032

CUSTOM_1033

CUSTOM_1034

CUSTOM_1035

CUSTOM_1036

CUSTOM_1037

CUSTOM_1038

CUSTOM_1039

CUSTOM_1040

CUSTOM_1041

CUSTOM_1042

CUSTOM_1043

CUSTOM_1044

CUSTOM_1045

CUSTOM_1046

CUSTOM_1047

CUSTOM_1048

CUSTOM_1049

CUSTOM_1050

CUSTOM_1051

CUSTOM_1052

CUSTOM_1053

CUSTOM_1054

CUSTOM_1055

CUSTOM_1056

CUSTOM_1057

CUSTOM_1058

CUSTOM_1059

CUSTOM_1060

CUSTOM_1061

CUSTOM_1062

CUSTOM_1063

CUSTOM_1064

CUSTOM_1065

CUSTOM_1066

CUSTOM_1067

CUSTOM_1068

CUSTOM_1069

CUSTOM_1070

CUSTOM_1071

CUSTOM_1072

CUSTOM_1073

CUSTOM_1074

CUSTOM_1075

CUSTOM_1076

CUSTOM_1077

CUSTOM_1078

CUSTOM_1079

CUSTOM_1080

CUSTOM_1081

CUSTOM_1082

CUSTOM_1083

CUSTOM_1084

CUSTOM_1085

CUSTOM_1086

CUSTOM_1087

CUSTOM_1088

CUSTOM_1089

CUSTOM_1090

CUSTOM_1091

CUSTOM_1092

CUSTOM_1093

CUSTOM_1094

CUSTOM_1095

CUSTOM_1096

CUSTOM_1097

CUSTOM_1098

CUSTOM_1099

CUSTOM_1100

CUSTOM_2001

CUSTOM_2002

CUSTOM_2003

CUSTOM_2004

CUSTOM_2005

CUSTOM_2006

CUSTOM_2007

CUSTOM_2008

CUSTOM_2009

CUSTOM_2010

CUSTOM_2011

CUSTOM_2012

CUSTOM_2013

CUSTOM_2014

CUSTOM_2015

CUSTOM_2016

CUSTOM_2017

CUSTOM_2018

CUSTOM_2019

CUSTOM_2020

CUSTOM_2021

CUSTOM_2022

CUSTOM_2023

CUSTOM_2024

CUSTOM_2025

CUSTOM_2026

CUSTOM_2027

CUSTOM_2028

CUSTOM_2029

CUSTOM_2030

CUSTOM_2031

CUSTOM_2032

CUSTOM_2033

CUSTOM_2034

CUSTOM_2035

CUSTOM_2036

CUSTOM_2037

CUSTOM_2038

CUSTOM_2039

CUSTOM_2040

CUSTOM_2041

CUSTOM_2042

CUSTOM_2043

CUSTOM_2044

CUSTOM_2045

CUSTOM_2046

CUSTOM_2047

CUSTOM_2048

CUSTOM_2049

CUSTOM_2050

CUSTOM_2051

CUSTOM_2052

CUSTOM_2053

CUSTOM_2054

CUSTOM_2055

CUSTOM_2056

CUSTOM_2057

CUSTOM_2058

CUSTOM_2059

CUSTOM_2060

CUSTOM_2061

CUSTOM_2062

CUSTOM_2063

CUSTOM_2064

CUSTOM_2065

CUSTOM_2066

CUSTOM_2067

CUSTOM_2068

CUSTOM_2069

CUSTOM_2070

CUSTOM_2071

CUSTOM_2072

CUSTOM_2073

CUSTOM_2074

CUSTOM_2075

CUSTOM_2076

CUSTOM_2077

CUSTOM_2078

CUSTOM_2079

CUSTOM_2080

CUSTOM_2081

CUSTOM_2082

CUSTOM_2083

CUSTOM_2084

CUSTOM_2085

CUSTOM_2086

CUSTOM_2087

CUSTOM_2088

CUSTOM_2089

CUSTOM_2090

CUSTOM_2091

CUSTOM_2092

CUSTOM_2093

CUSTOM_2094

CUSTOM_2095

CUSTOM_2096

CUSTOM_2097

CUSTOM_2098

CUSTOM_2099

CUSTOM_2100

CUSTOM_3001

CUSTOM_3002

CUSTOM_3003

CUSTOM_3004

CUSTOM_3005

CUSTOM_3006

CUSTOM_3007

CUSTOM_3008

CUSTOM_3009

CUSTOM_3010

CUSTOM_3011

CUSTOM_3012

CUSTOM_3013

CUSTOM_3014

CUSTOM_3015

CUSTOM_3016

CUSTOM_3017

CUSTOM_3018

CUSTOM_3019

CUSTOM_3020

CUSTOM_3021

CUSTOM_3022

CUSTOM_3023

CUSTOM_3024

CUSTOM_3025

CUSTOM_3026

CUSTOM_3027

CUSTOM_3028

CUSTOM_3029

CUSTOM_3030

CUSTOM_3031

CUSTOM_3032

CUSTOM_3033

CUSTOM_3034

CUSTOM_3035

CUSTOM_3036

CUSTOM_3037

CUSTOM_3038

CUSTOM_3039

CUSTOM_3040

CUSTOM_3041

CUSTOM_3042

CUSTOM_3043

CUSTOM_3044

CUSTOM_3045

CUSTOM_3046

CUSTOM_3047

CUSTOM_3048

CUSTOM_3049

CUSTOM_3050

CUSTOM_3051

CUSTOM_3052

CUSTOM_3053

CUSTOM_3054

CUSTOM_3055

CUSTOM_3056

CUSTOM_3057

CUSTOM_3058

CUSTOM_3059

CUSTOM_3060

CUSTOM_3061

CUSTOM_3062

CUSTOM_3063

CUSTOM_3064

CUSTOM_3065

CUSTOM_3066

CUSTOM_3067

CUSTOM_3068

CUSTOM_3069

CUSTOM_3070

CUSTOM_3071

CUSTOM_3072

CUSTOM_3073

CUSTOM_3074

CUSTOM_3075

CUSTOM_3076

CUSTOM_3077

CUSTOM_3078

CUSTOM_3079

CUSTOM_3080

CUSTOM_3081

CUSTOM_3082

CUSTOM_3083

CUSTOM_3084

CUSTOM_3085

CUSTOM_3086

CUSTOM_3087

CUSTOM_3088

CUSTOM_3089

CUSTOM_3090

CUSTOM_3091

CUSTOM_3092

CUSTOM_3093

CUSTOM_3094

CUSTOM_3095

CUSTOM_3096

CUSTOM_3097

CUSTOM_3098

CUSTOM_3099

CUSTOM_3100

CUSTOM_4001

CUSTOM_4002

CUSTOM_4003

CUSTOM_4004

CUSTOM_4005

CUSTOM_4006

CUSTOM_4007

CUSTOM_4008

CUSTOM_4009

CUSTOM_4010

CUSTOM_4011

CUSTOM_4012

CUSTOM_4013

CUSTOM_4014

CUSTOM_4015

CUSTOM_4016

CUSTOM_4017

CUSTOM_4018

CUSTOM_4019

CUSTOM_4020

CUSTOM_4021

CUSTOM_4022

CUSTOM_4023

CUSTOM_4024

CUSTOM_4025

CUSTOM_4026

CUSTOM_4027

CUSTOM_4028

CUSTOM_4029

CUSTOM_4030

CUSTOM_4031

CUSTOM_4032

CUSTOM_4033

CUSTOM_4034

CUSTOM_4035

CUSTOM_4036

CUSTOM_4037

CUSTOM_4038

CUSTOM_4039

CUSTOM_4040

CUSTOM_4041

CUSTOM_4042

CUSTOM_4043

CUSTOM_4044

CUSTOM_4045

CUSTOM_4046

CUSTOM_4047

CUSTOM_4048

CUSTOM_4049

CUSTOM_4050

CUSTOM_4051

CUSTOM_4052

CUSTOM_4053

CUSTOM_4054

CUSTOM_4055

CUSTOM_4056

CUSTOM_4057

CUSTOM_4058

CUSTOM_4059

CUSTOM_4060

CUSTOM_4061

CUSTOM_4062

CUSTOM_4063

CUSTOM_4064

CUSTOM_4065

CUSTOM_4066

CUSTOM_4067

CUSTOM_4068

CUSTOM_4069

CUSTOM_4070

CUSTOM_4071

CUSTOM_4072

CUSTOM_4073

CUSTOM_4074

CUSTOM_4075

CUSTOM_4076

CUSTOM_4077

CUSTOM_4078

CUSTOM_4079

CUSTOM_4080

CUSTOM_4081

CUSTOM_4082

CUSTOM_4083

CUSTOM_4084

CUSTOM_4085

CUSTOM_4086

CUSTOM_4087

CUSTOM_4088

CUSTOM_4089

CUSTOM_4090

CUSTOM_4091

CUSTOM_4092

CUSTOM_4093

CUSTOM_4094

CUSTOM_4095

CUSTOM_4096

CUSTOM_4097

CUSTOM_4098

CUSTOM_4099

CUSTOM_4100

CUSTOM_5001

CUSTOM_5002

CUSTOM_5003

CUSTOM_5004

CUSTOM_5005

CUSTOM_5006

CUSTOM_5007

CUSTOM_5008

CUSTOM_5009

CUSTOM_5010

CUSTOM_5011

CUSTOM_5012

CUSTOM_5013

CUSTOM_5014

CUSTOM_5015

CUSTOM_5016

CUSTOM_5017

CUSTOM_5018

CUSTOM_5019

CUSTOM_5020

CUSTOM_5021

CUSTOM_5022

CUSTOM_5023

CUSTOM_5024

CUSTOM_5025

CUSTOM_5026

CUSTOM_5027

CUSTOM_5028

CUSTOM_5029

CUSTOM_5030

CUSTOM_5031

CUSTOM_5032

CUSTOM_5033

CUSTOM_5034

CUSTOM_5035

CUSTOM_5036

CUSTOM_5037

CUSTOM_5038

CUSTOM_5039

CUSTOM_5040

CUSTOM_5041

CUSTOM_5042

CUSTOM_5043

CUSTOM_5044

CUSTOM_5045

CUSTOM_5046

CUSTOM_5047

CUSTOM_5048

CUSTOM_5049

CUSTOM_5050

CUSTOM_5051

CUSTOM_5052

CUSTOM_5053

CUSTOM_5054

CUSTOM_5055

CUSTOM_5056

CUSTOM_5057

CUSTOM_5058

CUSTOM_5059

CUSTOM_5060

CUSTOM_5061

CUSTOM_5062

CUSTOM_5063

CUSTOM_5064

CUSTOM_5065

CUSTOM_5066

CUSTOM_5067

CUSTOM_5068

CUSTOM_5069

CUSTOM_5070

CUSTOM_5071

CUSTOM_5072

CUSTOM_5073

CUSTOM_5074

CUSTOM_5075

CUSTOM_5076

CUSTOM_5077

CUSTOM_5078

CUSTOM_5079

CUSTOM_5080

CUSTOM_5081

CUSTOM_5082

CUSTOM_5083

CUSTOM_5084

CUSTOM_5085

CUSTOM_5086

CUSTOM_5087

CUSTOM_5088

CUSTOM_5089

CUSTOM_5090

CUSTOM_5091

CUSTOM_5092

CUSTOM_5093

CUSTOM_5094

CUSTOM_5095

CUSTOM_5096

CUSTOM_5097

CUSTOM_5098

CUSTOM_5099

CUSTOM_5100

ConstellationCount

### `setArtHybridRatio((Constellation)arg1, (float)artHybridRatio[, (Anim)animator]) -> None`

Setter for property artHybridRatio

**Parameters:**
- artHybridRatio (double) – Used to define which device will display the constellation image. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setArtIntensity((Constellation)arg1, (float)artIntensity[, (Anim)animator]) -> None`

Setter for property artIntensity

**Parameters:**
- artIntensity (double) – Current intensity of the picture of the constellation. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setArtUseHybridRatio((Constellation)arg1, (float)artUseHybridRatio[, (Anim)animator]) -> None`

Setter for property artUseHybridRatio

**Parameters:**
- artUseHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘art hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Constellation)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Current intensity of the label of the constellation. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLimitsIntensity((Constellation)arg1, (float)limitsIntensity[, (Anim)animator]) -> None`

Setter for property limitsIntensity

**Parameters:**
- limitsIntensity (double) – Current intensity of the constellation border lines. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLinesGap((Constellation)arg1, (float)linesGap[, (Anim)animator]) -> None`

Setter for property linesGap

**Parameters:**
- linesGap (double) – Modify the gap between constellation line and according star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLinesIntensity((Constellation)arg1, (float)linesIntensity[, (Anim)animator]) -> None`

Setter for property linesIntensity

**Parameters:**
- linesIntensity (double) – Current intensity of the constelation lines. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property artHybridRatio`

Used to define which device will display the constellation image. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property artIntensity`

Current intensity of the picture of the constellation. Usually in range [0;1].

### property: `property artUseHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘art hybrid ratio’ value). This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property labelIntensity`

Current intensity of the label of the constellation. Usually in range [0;1].

### property: `property limitsIntensity`

Current intensity of the constellation border lines. Usually in range [0;1].

### property: `property linesGap`

Modify the gap between constellation line and according star.

### property: `property linesIntensity`

Current intensity of the constelation lines. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.DMX512

## class skyExplorer.DMX512

### class DMX512Name

InvalidDMX512

DMX_001

DMX_002

DMX_003

DMX_004

DMX_005

DMX_006

DMX_007

DMX_008

DMX_009

DMX_010

DMX_011

DMX_012

DMX_013

DMX_014

DMX_015

DMX_016

DMX_017

DMX_018

DMX_019

DMX_020

DMX_021

DMX_022

DMX_023

DMX_024

DMX_025

DMX_026

DMX_027

DMX_028

DMX_029

DMX_030

DMX_031

DMX_032

DMX_033

DMX_034

DMX_035

DMX_036

DMX_037

DMX_038

DMX_039

DMX_040

DMX_041

DMX_042

DMX_043

DMX_044

DMX_045

DMX_046

DMX_047

DMX_048

DMX_049

DMX_050

DMX_051

DMX_052

DMX_053

DMX_054

DMX_055

DMX_056

DMX_057

DMX_058

DMX_059

DMX_060

DMX_061

DMX_062

DMX_063

DMX_064

DMX_065

DMX_066

DMX_067

DMX_068

DMX_069

DMX_070

DMX_071

DMX_072

DMX_073

DMX_074

DMX_075

DMX_076

DMX_077

DMX_078

DMX_079

DMX_080

DMX_081

DMX_082

DMX_083

DMX_084

DMX_085

DMX_086

DMX_087

DMX_088

DMX_089

DMX_090

DMX_091

DMX_092

DMX_093

DMX_094

DMX_095

DMX_096

DMX_097

DMX_098

DMX_099

DMX_100

DMX_101

DMX_102

DMX_103

DMX_104

DMX_105

DMX_106

DMX_107

DMX_108

DMX_109

DMX_110

DMX_111

DMX_112

DMX_113

DMX_114

DMX_115

DMX_116

DMX_117

DMX_118

DMX_119

DMX_120

DMX_121

DMX_122

DMX_123

DMX_124

DMX_125

DMX_126

DMX_127

DMX_128

DMX_129

DMX_130

DMX_131

DMX_132

DMX_133

DMX_134

DMX_135

DMX_136

DMX_137

DMX_138

DMX_139

DMX_140

DMX_141

DMX_142

DMX_143

DMX_144

DMX_145

DMX_146

DMX_147

DMX_148

DMX_149

DMX_150

DMX_151

DMX_152

DMX_153

DMX_154

DMX_155

DMX_156

DMX_157

DMX_158

DMX_159

DMX_160

DMX_161

DMX_162

DMX_163

DMX_164

DMX_165

DMX_166

DMX_167

DMX_168

DMX_169

DMX_170

DMX_171

DMX_172

DMX_173

DMX_174

DMX_175

DMX_176

DMX_177

DMX_178

DMX_179

DMX_180

DMX_181

DMX_182

DMX_183

DMX_184

DMX_185

DMX_186

DMX_187

DMX_188

DMX_189

DMX_190

DMX_191

DMX_192

DMX_193

DMX_194

DMX_195

DMX_196

DMX_197

DMX_198

DMX_199

DMX_200

DMX_201

DMX_202

DMX_203

DMX_204

DMX_205

DMX_206

DMX_207

DMX_208

DMX_209

DMX_210

DMX_211

DMX_212

DMX_213

DMX_214

DMX_215

DMX_216

DMX_217

DMX_218

DMX_219

DMX_220

DMX_221

DMX_222

DMX_223

DMX_224

DMX_225

DMX_226

DMX_227

DMX_228

DMX_229

DMX_230

DMX_231

DMX_232

DMX_233

DMX_234

DMX_235

DMX_236

DMX_237

DMX_238

DMX_239

DMX_240

DMX_241

DMX_242

DMX_243

DMX_244

DMX_245

DMX_246

DMX_247

DMX_248

DMX_249

DMX_250

DMX_251

DMX_252

DMX_253

DMX_254

DMX_255

DMX_256

DMX_257

DMX_258

DMX_259

DMX_260

DMX_261

DMX_262

DMX_263

DMX_264

DMX_265

DMX_266

DMX_267

DMX_268

DMX_269

DMX_270

DMX_271

DMX_272

DMX_273

DMX_274

DMX_275

DMX_276

DMX_277

DMX_278

DMX_279

DMX_280

DMX_281

DMX_282

DMX_283

DMX_284

DMX_285

DMX_286

DMX_287

DMX_288

DMX_289

DMX_290

DMX_291

DMX_292

DMX_293

DMX_294

DMX_295

DMX_296

DMX_297

DMX_298

DMX_299

DMX_300

DMX_301

DMX_302

DMX_303

DMX_304

DMX_305

DMX_306

DMX_307

DMX_308

DMX_309

DMX_310

DMX_311

DMX_312

DMX_313

DMX_314

DMX_315

DMX_316

DMX_317

DMX_318

DMX_319

DMX_320

DMX_321

DMX_322

DMX_323

DMX_324

DMX_325

DMX_326

DMX_327

DMX_328

DMX_329

DMX_330

DMX_331

DMX_332

DMX_333

DMX_334

DMX_335

DMX_336

DMX_337

DMX_338

DMX_339

DMX_340

DMX_341

DMX_342

DMX_343

DMX_344

DMX_345

DMX_346

DMX_347

DMX_348

DMX_349

DMX_350

DMX_351

DMX_352

DMX_353

DMX_354

DMX_355

DMX_356

DMX_357

DMX_358

DMX_359

DMX_360

DMX_361

DMX_362

DMX_363

DMX_364

DMX_365

DMX_366

DMX_367

DMX_368

DMX_369

DMX_370

DMX_371

DMX_372

DMX_373

DMX_374

DMX_375

DMX_376

DMX_377

DMX_378

DMX_379

DMX_380

DMX_381

DMX_382

DMX_383

DMX_384

DMX_385

DMX_386

DMX_387

DMX_388

DMX_389

DMX_390

DMX_391

DMX_392

DMX_393

DMX_394

DMX_395

DMX_396

DMX_397

DMX_398

DMX_399

DMX_400

DMX_401

DMX_402

DMX_403

DMX_404

DMX_405

DMX_406

DMX_407

DMX_408

DMX_409

DMX_410

DMX_411

DMX_412

DMX_413

DMX_414

DMX_415

DMX_416

DMX_417

DMX_418

DMX_419

DMX_420

DMX_421

DMX_422

DMX_423

DMX_424

DMX_425

DMX_426

DMX_427

DMX_428

DMX_429

DMX_430

DMX_431

DMX_432

DMX_433

DMX_434

DMX_435

DMX_436

DMX_437

DMX_438

DMX_439

DMX_440

DMX_441

DMX_442

DMX_443

DMX_444

DMX_445

DMX_446

DMX_447

DMX_448

DMX_449

DMX_450

DMX_451

DMX_452

DMX_453

DMX_454

DMX_455

DMX_456

DMX_457

DMX_458

DMX_459

DMX_460

DMX_461

DMX_462

DMX_463

DMX_464

DMX_465

DMX_466

DMX_467

DMX_468

DMX_469

DMX_470

DMX_471

DMX_472

DMX_473

DMX_474

DMX_475

DMX_476

DMX_477

DMX_478

DMX_479

DMX_480

DMX_481

DMX_482

DMX_483

DMX_484

DMX_485

DMX_486

DMX_487

DMX_488

DMX_489

DMX_490

DMX_491

DMX_492

DMX_493

DMX_494

DMX_495

DMX_496

DMX_497

DMX_498

DMX_499

DMX_500

DMX_501

DMX_502

DMX_503

DMX_504

DMX_505

DMX_506

DMX_507

DMX_508

DMX_509

DMX_510

DMX_511

DMX_512

DMX512Count

### `setValue((DMX512)arg1, (float)value, (Anim)anim) -> None`

Set this dmx value.

**Parameters:**
- value (double) – Value to send to dmx.
- anim (Anim, optional) – Animation used to change the dmx value., defaults to Anim()

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.DateManager

## class skyExplorer.DateManager

### class MotionType

InvalidMotionType

MotionDiurnal

MotionAnnual

MotionAnalemma

MotionPrecession

### class SiderealTimeDirection

InvalidSiderealTimeDirection

Forward

Back

Nearest

### class SiderealTimeType

InvalidSiderealTimeType

Duration

Speed

### class TimeZone

InvalidTimeZone

DefaultTimeZone

UTC_M_12_00_IDL

UTC_M_11_00_COO

UTC_M_10_00_HAW

UTC_M_09_00_ALA

UTC_M_08_00_BAJ

UTC_M_08_00_PAC

UTC_M_07_00_ARI

UTC_M_07_00_CHI

UTC_M_07_00_MOU

UTC_M_06_00_CENTRALA

UTC_M_06_00_CENTRALT

UTC_M_06_00_GUA

UTC_M_06_00_SAS

UTC_M_05_00_BOG

UTC_M_05_00_EAS

UTC_M_05_00_IND

UTC_M_04_30_CAR

UTC_M_04_00_ASU

UTC_M_04_00_ATL

UTC_M_04_00_CUI

UTC_M_04_00_GEO

UTC_M_04_00_SAN

UTC_M_03_30_NEW

UTC_M_03_00_BRA

UTC_M_03_00_BUE

UTC_M_03_00_CAY

UTC_M_03_00_GRE

UTC_M_03_00_MON

UTC_M_03_00_SAL

UTC_M_02_00_COO

UTC_M_02_00_MID

UTC_M_01_00_AZO

UTC_M_01_00_CAP

UTC_P_00_00_CAS

UTC_P_00_00_COO

UTC_P_00_00_DUB

UTC_P_00_00_MON

UTC_P_01_00_AMS

UTC_P_01_00_BEL

UTC_P_01_00_BRU

UTC_P_01_00_SAR

UTC_P_01_00_WES

UTC_P_01_00_WIN

UTC_P_02_00_ATH

UTC_P_02_00_BEI

UTC_P_02_00_CAI

UTC_P_02_00_DAM

UTC_P_02_00_EEU

UTC_P_02_00_HAR

UTC_P_02_00_HEL

UTC_P_02_00_IST

UTC_P_02_00_JER

UTC_P_03_00_AMM

UTC_P_03_00_BAG

UTC_P_03_00_KAL

UTC_P_03_00_KUW

UTC_P_03_00_NAI

UTC_P_03_30_TEH

UTC_P_04_00_ABU

UTC_P_04_00_BAK

UTC_P_04_00_MOS

UTC_P_04_00_POR

UTC_P_04_00_TSI

UTC_P_04_00_YER

UTC_P_04_30_KAB

UTC_P_05_00_ISL

UTC_P_05_00_TAS

UTC_P_05_30_CHE

UTC_P_05_30_SRI

UTC_P_05_45_KAT

UTC_P_06_00_AST

UTC_P_06_00_DHA

UTC_P_06_00_EKA

UTC_P_06_30_YAN

UTC_P_07_00_BAN

UTC_P_07_00_NOV

UTC_P_08_00_BEI

UTC_P_08_00_KRA

UTC_P_08_00_KUA

UTC_P_08_00_PER

UTC_P_08_00_TAI

UTC_P_08_00_ULA

UTC_P_09_00_IRK

UTC_P_09_00_OSA

UTC_P_09_00_SEO

UTC_P_09_30_ADE

UTC_P_09_30_DAR

UTC_P_10_00_BRI

UTC_P_10_00_CAN

UTC_P_10_00_GUA

UTC_P_10_00_HOB

UTC_P_10_00_YAK

UTC_P_11_00_SOL

UTC_P_11_00_VLA

UTC_P_12_00_AUC

UTC_P_12_00_COO

UTC_P_12_00_FIJ

UTC_P_12_00_MAG

UTC_P_13_00_NUK

UTC_P_13_00_SAM

### `localDate((DateManager)arg1, (object)timezone) -> float`

Get the current julian date of the simulation according to given time zone.

**Parameters:**
- timezone (str, optional) – Name of the time zone used to convert date., defaults to

### `reachSiderealTime((DateManager)arg1, (float)targetSidTime, (DateManager.SiderealTimeDirection)direction, (DateManager.SiderealTimeType)type, (float)speed, (Anim)anim) -> None`

**Parameters:**
- targetSidTime (double)
- direction (SiderealTimeDirection, optional) – defaults to Forward
- type (SiderealTimeType, optional) – defaults to Duration
- speed (double, optional) – defaults to 0
- anim (Anim, optional) – Animation used for the time motion., defaults to Anim()

### `setCurrentDate((DateManager)arg1, (int)hour, (int)minute, (int)second, (DateManager.TimeZone)tz, (Anim)anim) -> None`

Set simulation date to current date with a given time

**Parameters:**
- hour (int)
- minute (int)
- second (int)
- tz (TimeZone)
- anim (Anim, optional) – defaults to Anim()

### `setCurrentDateTime((DateManager)arg1, (Anim)anim) -> None`

Set simulation date and time to current date and time

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `setDateTime((DateManager)arg1, (int)year, (int)month, (int)day, (int)hour, (int)minute, (int)second, (DateManager.TimeZone)tz, (Anim)anim) -> None`

Set simulation date and time

**Parameters:**
- year (int)
- month (int)
- day (int)
- hour (int)
- minute (int)
- second (int)
- tz (TimeZone)
- anim (Anim, optional) – defaults to Anim()

### `setJulianDate((DateManager)arg1, (float)julianDate[, (Anim)animator]) -> None`

Setter for property julianDate

**Parameters:**
- julianDate (double) – Current julian date of the simulation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLocalDate((DateManager)arg1, (float)value, (object)timezone, (Anim)anim) -> None`

Change simulation date according to a timezone

**Parameters:**
- value (double) – Date to reach (julian date in timezone system).
- timezone (str, optional) – Time zone of the given date value., defaults to
- anim (Anim, optional) – Animation used for the time motion., defaults to Anim()

### `setMotionType((DateManager)arg1, (DateManager.MotionType)motionType) -> None`

Setter for property motionType

**Parameters:**
- motionType (MotionType) – Current type of time motion. See ‘MotionType’ enumeration documentation for available values.

### `setTimeDaemonEnabled((DateManager)arg1, (bool)timeDaemonEnabled) -> None`

Setter for property timeDaemonEnabled

**Parameters:**
- timeDaemonEnabled (bool)

### `siderealTimeDelta((DateManager)arg1, (float)targetSidTime, (DateManager.SiderealTimeDirection)direction) -> float`

**Parameters:**
- targetSidTime (double)
- direction (SiderealTimeDirection, optional) – defaults to Forward

### `stop((DateManager)arg1) -> None`

Stop the current time motion. If no time motion in progress, it has no effect.

### `systemDate((DateManager)arg1) -> float`

Get the system julian date according to the system time zone.

### property: `property julianDate`

Current julian date of the simulation.

### property: `property motionType`

Current type of time motion. See ‘MotionType’ enumeration documentation for available values.

### property: `property siderealTime`

[Read-only]

Current sidereal time of the simulation at the greenwitch meridian

### property: `property timeDaemonEnabled`

None( (skyExplorer.DateManager)arg1) -> bool

### property: `property timeSpeed`

[Read-only]

Current simulation time speed in day(s) per second.

---

# skyExplorer.DomePointer

## class skyExplorer.DomePointer

### class DomePointerName

InvalidDomePointer

DomePointer001

DomePointer002

DomePointer003

DomePointer004

DomePointer005

DomePointer006

DomePointer007

DomePointer008

DomePointer009

DomePointer010

DomePointerCount

### `setApparentSize((DomePointer)arg1, (float)apparentSize[, (Anim)animator]) -> None`

Setter for property apparentSize

**Parameters:**
- apparentSize (double) – Apparent size in degree of the pointer on the screen.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAzimuth((DomePointer)arg1, (float)azimuth[, (Anim)animator]) -> None`

Setter for property azimuth

**Parameters:**
- azimuth (double) – Dome pointer’s azimut position on screen. Unit : degrees usually in range [-180;180]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setColor((DomePointer)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3) – Color of the pointer. Values are (red, green, blue). Each value must be in range[0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHeight((DomePointer)arg1, (float)height[, (Anim)animator]) -> None`

Setter for property height

**Parameters:**
- height (double) – Dome pointer’s height position on screen. Unit : degrees usually in range [0;90]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((DomePointer)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the dome pointer. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((DomePointer)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current used pointer model. See ‘PointerType’ enumeration for all available values.

### `setPosition((DomePointer)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – Dome pointer’s position (Azimut, height, rool) on screen. Unit : degrees
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRoll((DomePointer)arg1, (float)roll[, (Anim)animator]) -> None`

Setter for property roll

**Parameters:**
- roll (double) – Dome pointer’s roll. Unit : degrees usually in range [0;360]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property apparentSize`

Apparent size in degree of the pointer on the screen.

### property: `property azimuth`

Dome pointer’s azimut position on screen. Unit : degrees usually in range [-180;180]

### property: `property color`

Color of the pointer. Values are (red, green, blue). Each value must be in range[0;1].

### property: `property height`

Dome pointer’s height position on screen. Unit : degrees usually in range [0;90]

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Intensity of the dome pointer. Usually in range [0;1].

### property: `property pointerType`

Current used pointer model. See ‘PointerType’ enumeration for all available values.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property roll`

Dome pointer’s roll. Unit : degrees usually in range [0;360]

---

# skyExplorer.DrawableInsert

## class skyExplorer.DrawableInsert

### class BrushType

InvalidBrushType

Eraser

Pen

### class DrawableInsertName

InvalidDrawableInsert

DrawableInsert2D001

DrawableInsert2D002

DrawableInsert2D003

DrawableInsertCount

### `beginDraw((DrawableInsert)arg1) -> None`

Start a new draw. End drawing of the previous line.

### `clearAll((DrawableInsert)arg1, (Anim)anim) -> None`

Clear all drawing on this insert.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `endDraw((DrawableInsert)arg1) -> None`

End current drawing.

### `load((DrawableInsert)arg1, (object)file, (Anim)anim) -> None`

Load drawing.

**Parameters:**
- file (str) – File to load
- anim (Anim, optional) – defaults to Anim()

### `redo((DrawableInsert)arg1) -> None`

Redo the last actions previously reverted by ‘undo’.

### `remove((DrawableInsert)arg1) -> None`

Remove the drawable insert from the scene graph.

### `save((DrawableInsert)arg1, (object)file) -> None`

Save drawing.

**Parameters:**
- file (str) – File to save

### `setBrushColor((DrawableInsert)arg1, (Vec3)brushColor) -> None`

Setter for property brushColor

**Parameters:**
- brushColor (Vec3) – Color of the pencil tool. Values are (red, green, blue). Each value must be in range [0;1]

### `setBrushPosition((DrawableInsert)arg1, (Vec3)brushPosition) -> None`

Move the brush to the given position. If selected brush is ‘Pen’ straight line will be drawn from current position to targetPosition, else if Eraser is selected, erase a line from current position to targetPosition

**Parameters:**
- brushPosition (Vec3) – Target brush position. Unit is degrees. Values are (azimut Usually in range [-180;180], height Usually in range[0;90], 0)

### `setBrushSize((DrawableInsert)arg1, (float)brushSize) -> None`

Setter for property brushSize

**Parameters:**
- brushSize (double) – Size of drawing tools in degree.

### `setBrushType((DrawableInsert)arg1, (DrawableInsert.BrushType)brushType) -> None`

Setter for property brushType

**Parameters:**
- brushType (BrushType) – Current selected brush type. See ‘BrushType’ enumeration documentation for available values.

### `setIntensity((DrawableInsert)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the drawable insert. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((DrawableInsert)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of drawable isert’s parent port.

### `undo((DrawableInsert)arg1) -> None`

Undo the last actions (between the last calls to ‘beginDraw’).

### property: `property brushColor`

Color of the pencil tool. Values are (red, green, blue). Each value must be in range [0;1]

### property: `property brushSize`

Size of drawing tools in degree.

### property: `property brushType`

Current selected brush type. See ‘BrushType’ enumeration documentation for available values.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the drawable insert. Usually in range [0;1]

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of drawable isert’s parent port.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.DwarfPlanet

## class skyExplorer.DwarfPlanet

### class DwarfPlanetName

InvalidDwarfPlanet

Pluto

Ceres

Eris

Haumea

Makemake

PlutoBarycenter

DwarfPlanetCount

### class DwarfPlanetPort

InvalidDwarfPlanetPort

Ecliptic

Equatorial

EquatorialSynchronous

Galactic

OrbitalMeanEquinox

EquatorialJ2000

NoonEcliptic

NoonEquatorial

### class PatchLayer

InvalidPatchLayer

Layer_01

Layer_02

### class TerrainModel

InvalidTerrainModel

DefaultTerrain

Basic

NewHorizons

DawnHamo

DawnLamo

### `addChild((DwarfPlanet)arg1, (int)child, (DwarfPlanet.DwarfPlanetPort)port) -> None`

Add a child object to the dwarf planet scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (DwarfPlanetPort) – Coordinate system to use for adding child. See ‘DwarfPlanetPort’ documentation for available ports.

### `patchLayerAdd((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (int)patchId, (Anim)anim) -> None`

Add a layer to planet patch

**Parameters:**
- layerId (PatchLayer)
- patchId (int)
- anim (Anim, optional) – defaults to Anim()

### `patchLayerClear((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (Anim)anim) -> None`

Remove all patch layer from planet

**Parameters:**
- layerId (PatchLayer)
- anim (Anim, optional) – defaults to Anim()

### `portId((DwarfPlanet)arg1, (DwarfPlanet.DwarfPlanetPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (DwarfPlanetPort) – Name of the port. See ‘DwarfPlanetPort’ documentation for more information.

### `setElevationScale((DwarfPlanet)arg1, (float)elevationScale[, (Anim)animator]) -> None`

Setter for property elevationScale

**Parameters:**
- elevationScale (double) – Modify elevation scale of dwarf planet’s reliefs. In some modelsets of dwarf planets do not use this property.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFlatteningFactor((DwarfPlanet)arg1, (float)flatteningFactor[, (Anim)animator]) -> None`

Setter for property flatteningFactor

**Parameters:**
- flatteningFactor (double) – Flattening factor of the dwarf planet.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((DwarfPlanet)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the dwarf planet. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((DwarfPlanet)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the dwarf planet’s label. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchBottomLeft((DwarfPlanet)arg1, (Vec3)livePatchBottomLeft[, (Anim)animator]) -> None`

Setter for property livePatchBottomLeft

**Parameters:**
- livePatchBottomLeft (Vec3) – South west LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchGamma((DwarfPlanet)arg1, (Vec3)livePatchGamma[, (Anim)animator]) -> None`

Setter for property livePatchGamma

**Parameters:**
- livePatchGamma (Vec3) – Gamma correction for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchHsv((DwarfPlanet)arg1, (Vec3)livePatchHsv[, (Anim)animator]) -> None`

Setter for property livePatchHsv

**Parameters:**
- livePatchHsv (Vec3) – Hue, Saturation and Lightness value used for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchIntensity((DwarfPlanet)arg1, (float)livePatchIntensity[, (Anim)animator]) -> None`

Setter for property livePatchIntensity

**Parameters:**
- livePatchIntensity (double) – Intensity of the live patch. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchKeyColor((DwarfPlanet)arg1, (Vec4)livePatchKeyColor[, (Anim)animator]) -> None`

Setter for property livePatchKeyColor

**Parameters:**
- livePatchKeyColor (Vec4) – Color to remove from patch texture (RGB + tolerance).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchRotation((DwarfPlanet)arg1, (float)livePatchRotation[, (Anim)animator]) -> None`

Setter for property livePatchRotation

**Parameters:**
- livePatchRotation (double) – Rotation of the patch around center point in degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchTexture((DwarfPlanet)arg1, (object)livePatchTexture) -> None`

Setter for property livePatchTexture

**Parameters:**
- livePatchTexture (str) – Texture to apply on the live patch.

### `setLivePatchTopRight((DwarfPlanet)arg1, (Vec3)livePatchTopRight[, (Anim)animator]) -> None`

Setter for property livePatchTopRight

**Parameters:**
- livePatchTopRight (Vec3) – North east LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchVibrance((DwarfPlanet)arg1, (float)livePatchVibrance[, (Anim)animator]) -> None`

Setter for property livePatchVibrance

**Parameters:**
- livePatchVibrance (double) – Vibrance value used in coordination with HSV value.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((DwarfPlanet)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double) – Intensity of the dwarf planet’s orbit. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPatchLayerGamma((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (Vec3)gamma, (Anim)anim) -> None`

Gamma correction for the patc layerh.

**Parameters:**
- layerId (PatchLayer)
- gamma (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerHsv((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (Vec3)hsv, (Anim)anim) -> None`

Hue, Saturation and Lightness value used for the patch layer.

**Parameters:**
- layerId (PatchLayer)
- hsv (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerKeyColor((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (Vec4)keColor, (Anim)anim) -> None`

Color to remove from patch texture (RGB + tolerance).

**Parameters:**
- layerId (PatchLayer)
- keColor (Vec4)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerOpacity((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (float)opacity, (Anim)anim) -> None`

Intensity of the patch layer. Usually in range [0;1]

**Parameters:**
- layerId (PatchLayer)
- opacity (double)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerVibrance((DwarfPlanet)arg1, (DwarfPlanet.PatchLayer)layerId, (float)vibrance, (Anim)anim) -> None`

Vibrance value used in coordination with HSV value of the patch layer.

**Parameters:**
- layerId (PatchLayer)
- vibrance (double)
- anim (Anim, optional) – defaults to Anim()

### `setPointerIntensity((DwarfPlanet)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the dwarf planet’s pointer. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((DwarfPlanet)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current dwarf planet pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setSeaLevel((DwarfPlanet)arg1, (float)seaLevel[, (Anim)animator]) -> None`

Setter for property seaLevel

**Parameters:**
- seaLevel (double) – Sea level level of the sea level in meter.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSeaLevelRenderingMode((DwarfPlanet)arg1, (object)seaLevelRenderingMode[, (Anim)animator]) -> None`

Setter for property seaLevelRenderingMode

**Parameters:**
- seaLevelRenderingMode (str) – Sea level rendering mode use ‘NONE’ for off.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowContrast((DwarfPlanet)arg1, (float)shadowContrast[, (Anim)animator]) -> None`

Setter for property shadowContrast

**Parameters:**
- shadowContrast (double) – Contrast of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowStrength((DwarfPlanet)arg1, (float)shadowStrength[, (Anim)animator]) -> None`

Setter for property shadowStrength

**Parameters:**
- shadowStrength (double) – Strength of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainModel((DwarfPlanet)arg1, (DwarfPlanet.TerrainModel)terrainModel[, (Anim)animator]) -> None`

Setter for property terrainModel

**Parameters:**
- terrainModel (TerrainModel)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainRenderingMode((DwarfPlanet)arg1, (object)terrainRenderingMode[, (Anim)animator]) -> None`

Setter for property terrainRenderingMode

**Parameters:**
- terrainRenderingMode (str) – Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTopographicGradientTextureFilename((DwarfPlanet)arg1, (object)topographicGradientTextureFilename) -> None`

Setter for property topographicGradientTextureFilename

**Parameters:**
- topographicGradientTextureFilename (str) – Texture to use to color planet in topographic mode.

### `setTrajectoryIntensity((DwarfPlanet)arg1, (float)trajectoryIntensity[, (Anim)animator]) -> None`

Setter for property trajectoryIntensity

**Parameters:**
- trajectoryIntensity (double) – Intensity of dwarf planet’s trajectory. Usually in range [0;1]. If set to positive value, the dwarf planet will draw a line according to it’s movement on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property elevationScale`

Modify elevation scale of dwarf planet’s reliefs. In some modelsets of dwarf planets do not use this property.

### property: `property flatteningFactor`

Flattening factor of the dwarf planet.

### property: `property flatteningOriginal`

[Read-only]

Read-only original flattening (0 means no flattening).

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the dwarf planet. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the dwarf planet’s label. Usually in range [0;1].

### property: `property livePatchBottomLeft`

South west LBR point of the patch. Unit : degrees.

### property: `property livePatchGamma`

Gamma correction for the patch.

### property: `property livePatchHsv`

Hue, Saturation and Lightness value used for the patch.

### property: `property livePatchIntensity`

Intensity of the live patch. Usually in range [0;1]

### property: `property livePatchKeyColor`

Color to remove from patch texture (RGB + tolerance).

### property: `property livePatchRotation`

Rotation of the patch around center point in degrees.

### property: `property livePatchTexture`

Texture to apply on the live patch.

### property: `property livePatchTopRight`

North east LBR point of the patch. Unit : degrees.

### property: `property livePatchVibrance`

Vibrance value used in coordination with HSV value.

### property: `property name`

Returns the name.

### property: `property orbitIntensity`

Intensity of the dwarf planet’s orbit. Usually in range [0;1].

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Intensity of the dwarf planet’s pointer. Usually in range [0;1].

### property: `property pointerType`

Current dwarf planet pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the body in ICRF coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property seaLevel`

Sea level level of the sea level in meter.

### property: `property seaLevelRenderingMode`

Sea level rendering mode use ‘NONE’ for off.

### property: `property shadowContrast`

Contrast of the planet’s shadow. Usually in range [0;1]

### property: `property shadowStrength`

Strength of the planet’s shadow. Usually in range [0;1]

### property: `property terrainModel`

None( (skyExplorer.DwarfPlanet)arg1) -> object

### property: `property terrainRenderingMode`

Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.

### property: `property topographicGradientTextureFilename`

Texture to use to color planet in topographic mode.

### property: `property trajectoryIntensity`

Intensity of dwarf planet’s trajectory. Usually in range [0;1]. If set to positive value, the dwarf planet will draw a line according to it’s movement on the dome.

---

# skyExplorer.Ephemeris

## class skyExplorer.Ephemeris

### class EphemerisName

InvalidEphemeris

Ephemeris001

Ephemeris002

Ephemeris003

Ephemeris004

Ephemeris005

Ephemeris006

Ephemeris007_Tonight

Ephemeris008_Dynamic

Ephemeris009_Sunrise

Ephemeris010_Sunset

EphemerisCount

### class EventType

InvalidEventType

CompatibilityRise

Rise

Set

Transit

### class OffsetType

InvalidOffsetType

CompatibilityHour

Hour

Height

### `setDayLimit((Ephemeris)arg1, (int)dayLimit) -> None`

Setter for property dayLimit

**Parameters:**
- dayLimit (int) – Limit of day to search an ephemeris

### `setEventType((Ephemeris)arg1, (Ephemeris.EventType)eventType) -> None`

Setter for property eventType

**Parameters:**
- eventType (EventType) – Type of ephemeris event. See EphemerisEvent enum for details.

### `setOffset((Ephemeris)arg1, (float)offset) -> None`

Setter for property offset

**Parameters:**
- offset (double) – Offset used for event may be hours or degrees from horizon (depending on offset type)

### `setOffsetType((Ephemeris)arg1, (Ephemeris.OffsetType)offsetType) -> None`

Setter for property offsetType

**Parameters:**
- offsetType (OffsetType) – Type of ephemeris event offset. See OffsetType enum for details

### `setStartDate((Ephemeris)arg1, (float)startDate) -> None`

Setter for property startDate

**Parameters:**
- startDate (double) – Start julian date to search for an ephemeris. Must be used with useSimulationTime = True.

### `setTargetBody((Ephemeris)arg1, (int)targetBody) -> None`

Setter for property targetBody

**Parameters:**
- targetBody (int) – Reference body of the ephemeris (ex: Sun for sun set / sun rise).

### `setTimeOffset((Ephemeris)arg1, (float)timeOffset) -> None`

Setter for property timeOffset

**Parameters:**
- timeOffset (double) – Time offset in day (added to current time value). For example -1 will search for previous rise, set or transit. Default: 0.0

### `setUseSimulationTime((Ephemeris)arg1, (bool)useSimulationTime) -> None`

Setter for property useSimulationTime

**Parameters:**
- useSimulationTime (bool) – Use the simulation time (or not) to compute ephemeris dates.

### property: `property date`

[Read-only]

Date of the event.

### property: `property dayLimit`

Limit of day to search an ephemeris

### property: `property eventType`

Type of ephemeris event. See EphemerisEvent enum for details.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property isValid`

[Read-only]

An event may be invalid if the body is circumpolar during more than a day (e.g if it never rise or set in a day).

### property: `property name`

Returns the name.

### property: `property offset`

Offset used for event may be hours or degrees from horizon (depending on offset type)

### property: `property offsetType`

Type of ephemeris event offset. See OffsetType enum for details

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property riseDate`

[Read-only]

Date of the next rise of the body.

### property: `property setDate`

[Read-only]

Date of the next set of the body.

### property: `property startDate`

Start julian date to search for an ephemeris. Must be used with useSimulationTime = True.

### property: `property targetBody`

Reference body of the ephemeris (ex: Sun for sun set / sun rise).

### property: `property timeOffset`

Time offset in day (added to current time value). For example -1 will search for previous rise, set or transit. Default: 0.0

### property: `property transitDate`

[Read-only]

Date of the next meridian transit of the body. (TODO: UTC date ?)

### property: `property useSimulationTime`

Use the simulation time (or not) to compute ephemeris dates.

---

# skyExplorer.FreeDomeManager

## class skyExplorer.FreeDomeManager

### `load((FreeDomeManager)arg1, (object)scene) -> None`

**Parameters:**
- scene (str)

### `setIntensity((FreeDomeManager)arg1, (float)intensity, (float)duration) -> None`

**Parameters:**
- intensity (double)
- duration (double)

### `setUseAlpha((FreeDomeManager)arg1, (bool)useAlpha) -> None`

**Parameters:**
- useAlpha (bool)

---

# skyExplorer.Galaxy

## class skyExplorer.Galaxy

### class GalaxyName

InvalidGalaxy

MilkyWay

LMC

SMC

SgrDSph

And

CenA

M32

M110

GalaxyCount

### class GalaxyPort

InvalidGalaxyPort

Galactic

### class Model

InvalidModel

Model_Default

Model_Basic

Model_veRTIGE

Model_veRTIGE_HighRes

Model_veRTIGE_APOD

Model_veRTIGE_APOD_HighRes

Model_veRTIGE_IR

Model_veRTIGE_IR_HighRes

Model_veRTIGE_RGB_UV

Model_veRTIGE_RGB_UV_HighRes

Model_veRTIGE_UV

Model_veRTIGE_UV_HighRes

Model_veRTIGE_Visible

Model_veRTIGE_Visible_HighRes

Model_veRTIGE_NearIR

Model_veRTIGE_NearIR_HighRes

Model_veRTIGE_Local_HD

Model_veRTIGE_Blackhole_HD

Model_IR

Model_HighRes

Model_Infrared

Model_veRTIGE_Near_Infrared

### class Model2D

InvalidModel2D

Model2D_Default

Model2D_Basic

Model2D_2MASS

Model2D_Brunier_2010

Model2D_Fermi

Model2D_Iras_Cobe

Model2D_Mellinger_1999

Model2D_Spizer_Glimpse

Model2D_Spizer_Mipsgal

Model2D_Mellinger_1999_RAW

Model2D_Mellinger_2016_RsaCosmos

Model2D_Mellinger_2016_RsaCosmos_DSO

Model2D_GaiaDR2_HDR

Model2D_GaiaDR3_HDR

Model2D_Mellinge_2016_RsaCosmos

Model2D_Mellinge_2016_RsaCosmos_DSO

Model2D_Gaia_HDR

### `addChild((Galaxy)arg1, (int)child, (Galaxy.GalaxyPort)port) -> None`

Add a child object to the galaxy scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (GalaxyPort) – Coordinate system to use for adding child. See GalaxyPort documentation for more information.

### `defaultModel2D((Galaxy)arg1) -> int`

### `defaultModel2DPath((Galaxy)arg1) -> object`

### `model2DPath((Galaxy)arg1) -> object`

### `portId((Galaxy)arg1, (Galaxy.GalaxyPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (GalaxyPort) – Name of the port. See ‘GalaxyPort’ documentation for more information.

### `setBlackLevel((Galaxy)arg1, (float)blackLevel[, (Anim)animator]) -> None`

Setter for property blackLevel

**Parameters:**
- blackLevel (double) – Galaxy black level
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setColorBalance((Galaxy)arg1, (Vec3)colorBalance[, (Anim)animator]) -> None`

Setter for property colorBalance

**Parameters:**
- colorBalance (Vec3) – Galaxy color balance
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setColorSaturation((Galaxy)arg1, (float)colorSaturation[, (Anim)animator]) -> None`

Setter for property colorSaturation

**Parameters:**
- colorSaturation (double) – Galaxy saturation
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setExposure((Galaxy)arg1, (float)exposure[, (Anim)animator]) -> None`

Setter for property exposure

**Parameters:**
- exposure (double) – Galaxy exposure
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHybridRatio((Galaxy)arg1, (float)hybridRatio[, (Anim)animator]) -> None`

Setter for property hybridRatio

**Parameters:**
- hybridRatio (double) – Used to define which device will display the galaxy. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Galaxy)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the galaxy. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity2D((Galaxy)arg1, (float)intensity2D[, (Anim)animator]) -> None`

Setter for property intensity2D

**Parameters:**
- intensity2D (double) – Intensity of the galaxy’s 2D representation. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Galaxy)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the galaxy’s label. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModel((Galaxy)arg1, (Galaxy.Model)model[, (Anim)animator]) -> None`

Setter for property model

**Parameters:**
- model (Model) – Galaxy modelset. See Model documentation for available values.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModel2D((Galaxy)arg1, (Galaxy.Model2D)model2D[, (Anim)animator]) -> None`

Setter for property model2D

**Parameters:**
- model2D (Model2D) – Galaxy 2D modelset. See Model documentation for available values.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModel2DCustom((Galaxy)arg1, (object)modelPath) -> None`

**Parameters:**
- modelPath (str)

### `setModel2Dlegacy((Galaxy)arg1, (int)legacyModelid, (Anim)anim) -> None`

**Parameters:**
- legacyModelid (int)
- anim (Anim, optional) – defaults to Anim()

### `setPointerIntensity((Galaxy)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the galaxy’s pointer. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Galaxy)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current galaxy pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setUseHybridRatio((Galaxy)arg1, (float)useHybridRatio[, (Anim)animator]) -> None`

Setter for property useHybridRatio

**Parameters:**
- useHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property blackLevel`

Galaxy black level

### property: `property colorBalance`

Galaxy color balance

### property: `property colorSaturation`

Galaxy saturation

### property: `property exposure`

Galaxy exposure

### property: `property hybridRatio`

Used to define which device will display the galaxy. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the galaxy. Usually in range [0;1].

### property: `property intensity2D`

Intensity of the galaxy’s 2D representation. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the galaxy’s label. Usually in range [0;1].

### property: `property model`

Galaxy modelset. See Model documentation for available values.

### property: `property model2D`

Galaxy 2D modelset. See Model documentation for available values.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Intensity of the galaxy’s pointer. Usually in range [0;1].

### property: `property pointerType`

Current galaxy pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the galaxy in ICRF coordinate system.

### property: `property radiusRatio`

[Read-only]

Radius ratio of the galaxy according to the unit of it’s coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property useHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.

---

# skyExplorer.GlobularCluster

## class skyExplorer.GlobularCluster

### class GlobularClusterName

InvalidGlobularCluster

NGC104_47Tuc

NGC288

NGC362

NGC1261

Pal1

AM1_E1

Eridanus

Pal2

NGC1851

NGC1904_M79

NGC2298

NGC2419

Pyxis

NGC2808

E3

Pal3

NGC3201

Pal4

NGC4147

NGC4372

Rup106

NGC4590_M68

NGC4833

NGC5024_M53

NGC5053

NGC5139_omegaCen

NGC5272_M3

NGC5286

AM4

NGC5466

NGC5634

NGC5694

IC4499

NGC5824

Pal5

NGC5897

NGC5904_M5

NGC5927

NGC5946

BH176

NGC5986

Lynga7

Pal14_AvdB

NGC6093_M80

NGC6121_M4

NGC6101

NGC6144

NGC6139

Terzan3

NGC6171_M107

ESO452_SC11

NGC6205_M13

NGC6229

NGC6218_M12

NGC6235

NGC6254_M10

NGC6256

Pal15

NGC6266_M62

NGC6273_M19

NGC6284

NGC6287

NGC6293

NGC6304

NGC6316

NGC6341_M92

NGC6325

NGC6333_M9

NGC6342

NGC6356

NGC6355

NGC6352

IC1257

Terzan2_HP3

NGC6366

Terzan4_HP4

HP1_BH229

NGC6362

Liller1

Terzan1_HP2

Ton2_Pismis26

NGC6388

NGC6402_M14

NGC6401

NGC6397

Pal6

NGC6426

Djorg1

Terzan5_Terzan11

NGC6440

NGC6441

Terzan6_HP5

NGC6453

UKS1

NGC6496

Terzan9

Djorg2_E456_SC38

NGC6517

Terzan10

NGC6522

NGC6535

NGC6528

NGC6539

NGC6540_Djorg3

NGC6544

NGC6541

NGC6553

NGC6558

IC1276_Pal7

NGC6569

NGC6584

NGC6624

NGC6626_M28

NGC6638

NGC6637_M69

NGC6642

NGC6652

NGC6656_M22

Pal8

NGC6681_M70

NGC6712

NGC6715_M54

NGC6717_Pal9

NGC6723

NGC6749

NGC6752

NGC6760

NGC6779_M56

Terzan7

Pal10

Arp2

NGC6809_M55

Terzan8

Pal11

NGC6838_M71

NGC6864_M75

NGC6934

NGC6981_M72

NGC7006

NGC7078_M15

NGC7089_M2

NGC7099_M30

Pal12

Pal13

NGC7492

Whiting1

Crater

BH140

FSR1716

FSR1735

FSR1758

NGC6380

VVV_CL001

_2MASS_GC01

ESO280_SC06

_2MASS_GC02

Terzan12

BH261

Laevens3

FSR1767

Kosopov1

Kosopov2

GlobularClusterCount

### class GlobularClusterPort

InvalidGlobularClusterPort

Ecliptic

Galactic

### `addChild((GlobularCluster)arg1, (int)child, (GlobularCluster.GlobularClusterPort)port) -> None`

Add a child object to the globular cluster scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (GlobularClusterPort) – Coordinate system to use for adding child. See GlobularClusterPort documentation for more information.

### `portId((GlobularCluster)arg1, (GlobularCluster.GlobularClusterPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (GlobularClusterPort) – Name of the port. See ‘GlobularClusterPort’ documentation for more information.

### `setIntensity((GlobularCluster)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the globular cluster. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((GlobularCluster)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the label of the globular cluster. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((GlobularCluster)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the pointer of the globular cluster. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((GlobularCluster)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current globular cluster pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setScale((GlobularCluster)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the globular cluster. It can be used to enlarge apparent size of the globular cluster.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the globular cluster. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the label of the globular cluster. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Intensity of the pointer of the globular cluster. Usually in range [0;1].

### property: `property pointerType`

Current globular cluster pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the globular cluster in the ICRF coordinate system.

### property: `property radiusRatio`

[Read-only]

Radius ratio of the globular cluster according to the unit of it’s coordinate system. In most case, value is globular cluster radius in kilometers.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property scale`

Scale factor of the globular cluster. It can be used to enlarge apparent size of the globular cluster.

---

# skyExplorer.IndividualStar

## class skyExplorer.IndividualStar

### class Cycle

InvalidCycle

Cycle_2097

Cycle_2165

Cycle_2232

Cycle_custom

### class Filter

InvalidFilter

Filter_Visible

Filter_304

Filter_Intensitygram

### class IndividualStarName

InvalidIndividualStar

Sun

CD3715492

HD142

Alpheratz

Caph

EpsilonPhe

ThetaScl

Algenib

L72222A

HD1237

ThetaAnd

SigmaAnd

GJ15A

HD1461

HD1502

DenebKaitosShemali

ZetaTuc

HD1605

HD1666

HD1690

IotaScl

HD2039

BetaHyi

KappaPhe

Ankaa

HIP2247

HD2638

BetaTucanaeABCD

BetaTucanaeC

BetaTucanaeP

KappaCas

HD2952

PiAnd

Fulu

EpsilonAnd

DeltaAnd

HD3651

Schedar

HD4113

EtaPhe

Diphda

HD4208

HD4308

HD4203

HD4313

ZetaAnd

DeltaPsc

EtaCassiopeiaeA

VanMaanen2

HD4732

NuAnd

HD5319

HD5388

GammaCassiopeiae

MuAnd

HD5608

AlphaScl

HD5891

EpsilonPsc

HD6434

HIP5158

HD6654

HD6718

MuCassiopeiae

ZetaPhe

EtaCet

PhiAnd

Mirach

HD7199

Marfak

ChiPsc

TauPsc

L72532

Revati

PhiPsc

HD7449

UpsilonPsc

HD7924

Adhil

HD8535

ThetaCet

HD8574

Ruchbah

GammaPhe

MuPsc

DeltaPhe

AlFarg

HD9446

UpsilonAndromedae

WASP18

Achernar

HD10180

_51And

NuPsc

PiScl

HD10647

PhiPer

TauCeti

HD10697

TorcularisSeptentrionalis

BatenKaitos

HD11506

Mothallah

Mesarthim

PsiPhe

Segin

Sheratan

HD11977

ChiEri

HD11964

AlphaHyi

HD11755

UpsilonCet

Alrescha

_50Cas

Almach

NuFor

HD12661

AlphaAri

BetaTri

GJ86

EtaArietis

MuFor

PhiEri

HD13931

GammaTri

Misam2

HD13908

HD12648

Mira

DeltaHyi

WASP33

KappaEri

Xi2Cet

PolarisA

_75Cet

OmegaFor

HD16141

_30AriB

HD16417

HD16175

EtaHor

_81Cet

DeltaCet

EpsilonCet

EpsilonHyi

HD16754

ZetaHor

IotaEri

HD16760

IotaHor

Kaffaljidhma

PiCet

ThetaPer

MuCet

Tau1Eri

HIP12961

BetaFor

HD17156

Bharani

_16Per

Miram

Angetenar

_20Per

TauPer

Azha

Acamar

GorgoneaSecunda

BetaHor

EpsilonAri

Menkar

HD18742

Menkar2

Tau3Eri

MuHor

GammaPer

GorgoneaTertia

Algol

IotaPer

Misam

HIP14810

GorgoneaQuarta

Botein

AlphaFor

HD19994

Zibal

Tau4Eri

_82GEridani

HD20782

HD20868

_32Per

Mirfak

OmicronTau

XiTauriA

HD21203

_5Tau

EpsilonEri

HD139691CD

Tau5Eri

PsiPer

_10Tau

HD22663

HD23127

HD23079

HD22781

DeltaFor

DeltaPer

Rana

BetaRet

Atik

Celaeno

Electra

NuPer

Taygeta

Maia

Asterope

SteropeII

Merope

Tau6Eri

GammaHyi

Alcyone

HD23596

HD24071

Atlas

Pleione

HD24160

GammaCam

HD24040

ZetaPersei

HD25171

HD24064

EpsilonPer

Zaurak

DeltaRet

Menkib

Tau9Eri

LamdaTau

GammaRet

NuTau

_37Tau

LamdaPer

HD285507

_48Per

GJ163

Beid

AlphaHor

AlphaRet

MuPer

OmicronEridaniA

MuTau

GammaDor

EpsilonRet

Upsilon4Eri

HyadumI

HD27894

HyadumII

_66Tau

Beemim

HD28254

KappaTau

Delta3Tau

HD28185

Theta1Tau

EpsilonTau

Theta2Tau

DeltaCae

Stein2051A

HD28678

Upsilon1Eri

AlphaDor

Theemin

_88Tau

Aldebaran

NuEri

_58Per

RDoradus

_51Eri

_90Tau

Sceptrum

AlphaCae

HD30177

BetaCae

TauTau

GJ176

MuEri

HD30562

Tabit

HD30856

Pi2Ori

Pi4Ori

GJ179

OmegaEri

HD30555

Pi5Ori

HD31253

Pi1Ori

EtaMen

Omicron2Ori

Hassaleh

_7Cam

Pi6Ori

EpsilonAurigae

Saclateni

BetaMen

BetaCam

GammaCae

Eta2Pic

EpsilonLep

ZetaDor

Haedus

HD33142

Cursa

HD32963

HD33283

LamdaEri

HD32518

KapteynsStar

HD33636

IotaLep

HD33844

MuLep

KELT7

KappaLep

Rigel

Capella

TauOri

HD34445

LamdaLep

HD33564

HD290327

EtaOri

Bellatrix

Elnath

BetaLeporis

EpsilonCol

Wolf1453

GammaMen

Thabit

MintakaAB

Arneb

BetaDor

Meissa

Hatysa

Alnilam

HD38283

HD37124

HD39091

Tianguan

SigmaOri

_49Ori

Phact

HD37605

Alnitak

Ross47

GammaLep

DeltaDor

HD38529

ZetaLep

BetaPic

Saiph

HD38801

GammaPic

KappaMen

Wazn

DeltaLep

HD40307

HD40409

Chi1Ori

Betelgeuse

EtaLep

GammaCol

EtaCol

DeltaAur

Menkalinan

Mahasim

MuOri

HD40981

Propus3

HD40979

NuOri

AlphaMensae

L66821A

KELT2A

XiOri

HD43197

GammaMon

Propus

KappaCol

HD42818

HD43691

_2Lyn

HD44219

Furud

DeltaCol

Mirzam

Tejat

EpsilonMon

Canopus

HD45364

LambdaCMa

HD45350

BetaMon

NuGem

HD45652

Ross614A

_6Lyn

Ksi1CMa

_13Mon

HD46375

HD47186

_7CMa

Alhena

NuPup

HD48265

Mebsuta

Sirius

Alzirr

_18Mon

AlphaPic

KappaCMa

TauPup

HD49674

HD50499

ThetaGem

Omicron1CMa

ThetaCMa

HD50554

Wolf294

Isida

IotaCMa

ThetaMen

_15Lyn

Adhara

HD49878

HD52265

SigmaCMa

Omicron2CMa

Muliphein

Mekbuda

Wezen

Gamma2Vol

TauGem

DeltaMon

_71Pup

HD56022

L2Puppis

OmegaCMa

DeltaVol

PiPup

LamdaGem

TauCMa

Wasat

EtaCanisMajoris

Propus2

_21Lyn

Gomeisa

LuytensStar

RhoGem

SigmaPup

HD59890

HD60532

Castor

HD60863

UpsilonGem

Markeb2

Jishui

Procyon

HD63454

AlphaMon

ZetaVol

KappaGem

Ross882

HD63032

Pollux

HD63765

HD63922

Azmidiske

HD64440

HD64760

HD65216

ChiCar

_11Pup

_27Mon

HD66428

NaosZetaPuppis

Tureis

HD67087

EpsilonVol

ZetaMon

_16Pup

GammaVelorum

_19Pup

Tegmine

BetCnc

HD68988

HD69830

AlphaCha

ThetaCha

HD70642

Avior

Alsciaukat

HD71155

BetaVol

OmicronUMa

ThetaCnc

EtaCnc

HD72659

HD73267

HD73256

HD73526

HD73634

DeltaHya

AlMinliaralShuja

Muscida

HD73534

BetaPyx

_4UMa

OmicronVel

Praesepe

HD74180

HD74156

EtaHya

AsellusBorealis

AlphaPyx

HD74772

AsellusAustralis

DeltaVel

HD75063

IotaCancriB

IotaCancriA

EpsilonHya

HD75289

RhoHya

GammaPyx

HD75784

_55Cancri

HD75898

HD76700

HD76728

GJ328

ZetaHya

Acubens

Talitha

HD76943

HD77338

AlphaVol

KappaUMa

HD78004

HD77912

Suhail

Sigma2UMa

HD79351

HD79447

Miaplacidus

ThetaHya

HD79498

Markeb

Aspidiske

_38Lyn

AlphaLyn

KappaVel

HD80606

HD81040

AlMinliaralAsad

Alphard

HD81688

EpsilonAnt

PsiVel

HD82668

_23UMa

Alterf

ThetaUMa

_10LMi

HD82943

HD82886

HD83443

IotaHya

Subra

ThetaAnt

HD84810

RasElasedAustralis

UpsilonCar

HD85390

UpsilonUMa

HD85512

Zhang

PhiUMa

GammaSex

MuLeo

HD86081

PhiVel

HD86264

EtaAnt

BD082823

Upsilon2Hya

Aldzhabkhakh

_21LMi

_31Leo

AlphaSex

Regulus

HD87883

HD88133

LamdaHya

Groombridge1618

OmegaCar

HD88955

Adhafera

HD89388

TaniaBorealis

HD89307

GammaLeoA

HD89744

TaniaAustralis

_24Sex

HD90156

MuHya

AlphaAnt

HD90853

BetaLMi

DeltaSex

BetaSex

HD91465

HD91233

GammaCha

HD92139

HD92788

ThetaCar

HD93083

Delta2Cha

MuVel

NuHya

Praecipua

HD94510

IotaAnt

HD95086

HD95089

UrsaeMajoris

HD95127

Alkes

Merak

Lalande21185

Dubhe

HD96063

HD96167

Chi01Hya

Lalande21258A

HD96127

V382Carinae

PsiUMa

BetaCrt

Zosma

Chertan

HD97658

HD98219

AlulaBorealis

Labr

PiCen

SigmaLeo

TVCraterisA

IotaLeo

HD99109

EpsilonCrt

GammaCrt

HD99492

HD99706

Giausar

XiHya

HD100655

GJ433

LamdaCen

HD100777

ThetaCrt

UPsilonLeo

HIP57050

GJ436

HD101930

HIP57274

ZetaCrt

HD102117

LamdaMus

L145141

HD102195

NuVir

Taiyangshou

HD102272

HD102350

HD102365

HD102329

G25429

Ross128

Denebola

Zavijava

HD102956

HD103197

BetaHya

ArgelandersStar

Phecda

EtaCrt

HD103774

HD104067

OmicronVir

HD104985

DeltaCen

Alchiba

Minkar

RhoCen

HD106252

HD106270

DeltaCru

Megrez

Gienah

EpsilonMus

BetaCha

HD107148

Zaniah

_11Com

EpsilonCru

HD108147

Acrux

GammaCom

HD108341

SigmaCen

Algorab

HD108863

HD108874

Gacrux

EtaCrv

HD109246

GammaMus

KappaDra

Chara

Kraz

AlphaMus

HD109749

TauCen

GammaCen

Porrima

RhoVir

BetaMus

Tianyi

Mimosa

HD111232

HD112028

HD111915

HD111968

Alioth

Taiyi

Minelauva

CorCaroli

HD113337

Vindemiatrix

DeltaMus

HD113703

ThetaVir

Diadem

HD114386

BetaCom

HD114613

HD114762

HD114783

HD114729

GJ504

_61Virginis

GammaHya

IotaCen

HD116029

MizarAlcorABMizar

Spica

MizarAlcorCAlcor

_70Vir

HD117207

HD117440

HD117618

HD118203

Heze

EpsilonCen

HD120084

Lalande25372

TauBoo

Alkaid

_2Cen

UpsilonBoo

NuCen

MuCen

HIP67851

Muphrid

ZetaCen

HD121504

PhiCen

Upsilon1Cen

TauVir

UPsilon2Cen

BetaCentauri

Thuban

ChiCen

PiHya

Menkent

Kang

AsellusTertius

Arcturus

Syrma

AsellusSecondus

Xuange

Kkhambaliya

IotaLup

PsiCen

HD125612

HD125595

HD125823

AsellusPrimus

HD126614A

DeltaOct

AlphaCentauriC

RhoBoo

Seginus

Wolf1481

EtaCen

HD128311

RhoLup

AlphaCentauriB

AlphaCentauriA

Pi1Boo

ZetaBoo

Men

HD129116

AlphaCir

RijlalAwwa

HD129456

Izar

_109Vir

HD130322

AlphaAps

Merga

_58Hya

Alpha1Lib

BetUMi

Zubenelgenubi

HD131496

_8UMi

HD132406

Lalande27173B

Lalande27173A

HD132563B

BetaLup

KappaCen

HD131664

ZubenElakribi

Nekkar

Brachium

PiLup

ZubenHakrabi

Kappa1Lup

IotaLib

ZetaLup

HD134987

Printseps

Zubeneschamali

_11UMi

BetaCir

_2Lup

MuLup

GammaTrA

HD136118

HD136418

Gliese581

OmicronCrB

Pherkad

DeltaLup

Phi1Lup

EpsilonLup

GammaCir

Alkalurops

IotaDra

Nusakan

CD409712

ThetaCrB

Alphecca

DeltaSer

GammaLup

HD139357

ZubenElakrab

HD137388

UpsilonLib

Ceginus

OmegaLup

HD139691AB

TauLib

GammaCrB

ZetaUMi

EtaLib

Unukalhai

BetaSer

LambdaSer

KappaSer

DeltaCrB

MuSer

HD330075

OmegaSer

EpsilonSer

ChiLup

KappaCrB

HD141937

ChiHer

HD142245

ThetaLib

BetaTrA

GammaSer

RhoSco

EpsilonCrB

HD142415

_48Lib

Fang

EtaLup

Dschubba

RhoCrB

IotaCrB

HD143361

ThetaDra

EtaNor

Iota1Nor

Acrab

DeltaNor

ThetaLup

Omega1Sco

_11Sco

Marsic

PhiHer

HD145457

HD142022

_14Her

HD145377

NuScorpiiAB

HIP79431

KappaNor

YedPrior

DeltaTrA

EtaUMi

YedPosterior

TauHer

Gamma2Nor

Delta1Aps

Delta2Aps

HATP2

OmicronScorpii

Alniyat

GammaHer

HD147018

EtaDra

HD147513

Cujam

EpsilonNor

HD148349

HD148156

HD148427

Antares

Kornephoros

Wolf1061

HD149026

Marfik

PhiOph

OmegaOph

HD149143

GammaAps

SigmaHer

HD149382

Alniyat2

Khan

ZetaHer

EtaHer

BetaAps

EpsilonUMi

Atria

EtaAra

EpsilonSco

Mu1Sco

Mu2Sco

HD152581

Grafias

KappaOph

GJ649

ZetaAra

Epsilon1Ara

EpsilonHer

HD154345

HD153950

Alrakis

Aldhibah

HD155358

HD154672

Sabik

HD155233

HD154857

EtaSco

HD156279

Rasalgethi

Sarin

PiHer

_36OphiuchiA

_36OphiuchiC

HD156668

Gliese667AB

HD156411

HD156846

NuSer

XiOph

ThetaOph

RhoHer

BetaAra

GammaAra

HD158038

_44Oph

_45Oph

GJ674

GJ676A

Rastaban

Maasym

Lesath

DeltaAra

AlphaAra

Kuma2

Yildun

Kuma

HD159243

Shaula

Rasalhague

GJ687

CD4411909

Sargas

XiSer

MuOph

HD159868

IotaHer

OmicronSer

Dziban

KappaSco

Cebalrai

MuArae

EtaPav

MuHer

L205128

_3Sgr

Iota1Sco

GammaOph

Fuyue

HD162020

Grumium

HD163607

ThetaHer

Eltanin

XiHer

BarnardsStar

NuHer

Sinistra

_67Oph

HD164509

HD164922

HD164604

Nash

_70OphiuchiA

Alnasl

ThetaAra

_72Oph

OmicronHer

PiPav

_102Her

HD167042

EpsilonTel

HD167225

EtaSgr

HD168443

PhiDra

KausMedia

ChiDra

EtaSer

HD168746

XiPav

ZetaSct

_109Her

KausAustralis

Alathfar

_42Dra

AlphaTel

HD169830

KausBorealis

ZetaTel

HD170469

GammaSct

HD171238

AlphaSct

HIP91258

Vega

DeltaSct

Struve2398A

Struve2398B

ZetaPav

HD173416

LambdaCrA

Epsilon1LyraeA

Epsilon2LyraeC

Zeta1Lyr

PhiSgr

_110Her

_111Her

BetaSct

Ross154

Sheliak

LamdaPav

AinAlRami

Delta2Lyr

Nunki

HD175541

Alya

Xi2Sgr

EpsilonCrA

Sulafat

DenebelOkab

HD175167

_12Aql

Ascella

ZetaCrA

Manubrij

HD177830

DenebelOkab2

LamdaAql

GammaCrA

TauSgr

DeltaCrA

HD178911B

Kepler21

AlfeccaMeridiana

Albaldah

BetaCrA

HD179079

Altais

Aladfar

HD180314

HD179949

TauDra

_1Vul

Wolf1055A

KappaCyg

_43Sgr

Kepler444

HD180902

HD181342

Rho1Sgr

ArkabPrior

EtaTel

HD181720

ArkabPosterior

Rukbat

HD181433

DenebOkab

HD183263

Anser

Iota2Cyg

Albireo

AlbireoB

HD231701

SigmaDraconis

MuAql

ThetaCyg

_52Sgr

IotaAql

HD185269

PhiCyg

Sham

BetaSge

_16CygB

DeltaCyg

HIP97233

Tarazed

HD187123

DeltaSge

Tyl

HD187085

ChiCyg

Altair

HATP11

HD188015

EtaAquilae

_13Vul

XiAql

HIP98001A

IotaSgr

Alshain

Terebellum2

PhiAql

EtaCyg

Terebellum3

GammaSge

Terebellum4

Theta1Sgr

EpsilonPav

HD189733

Terebellum

HD190228

HD190360

HD190647

KsiTel

DeltaPavonis

KappaCep

CD3613940A

ThetaAql

_31Cyg

HD192263

RhoAql

RDelphini

HD192310

_32Cyg

HD192699

PrimaGiedi

Algedi

Alshat

Dabih

GammaCygni

Peacock

Okul

HD195019

ThetaCep

Ruchba

Ruchba2

DenebDulfim

Rotanev

AlphaInd

HD196050

HD197037

Sualocin

HD196885

Deneb

DeltaDel

EtaInd

BetaPav

EtaCep

PsiCap

Aljanah

Gamma1delphini

Gamma2delphini

Albali

IotaMic

AlphaMic

OmegaCap

_31Vul

LP81660

MuAqr

BetaInd

NuCyg

_18Del

GammaMic

Arm

XiCyg

ThetaCap

HD200964

_61CygniA

_61CygniB

_24Cap

SigmaOctantis

GammaEqu

ZetaCyg

BD144559

DeltaEqu

TauCyg

HD202206

Kitalpha

Lacaille8760

EpsilonMic

Alderamin

ThetaInd

Theta1Mic

_1Peg

IotaCap

BetaEqu

HIP105854

GammaPav

ZetaCap

HD204313

Alfirk

Sadalsuud

HD204941

GJ832

Kastra

HD205739

Nashira

NuOct

Azelfafage

HD206610

Erakis

Enif

_9Peg

KappaPeg

IotaPsA

NuCephei

DenebAlgedi

ThetaPsA

HD207832

AlDanab

HD208527

HD208487

DeltaInd

EtaPsA

HD209458

EpsilonIndiA

Kurhah

Sadalmelik

LamdaGru

IotaAqr

IotaPeg

Alnair

MuPsA

HD210277

GJ849

PiPeg

Biham

_38Aqr

ZetaCep

HD210702

HD211073

LamdaPsA

EpsilonCep

Mu1Gru

_1Lac

Mu2Gru

Ancha

AlphaTuc

_2Lac

Sadachbia

RWCephei

BetaLac

_4Lac

PiAqr

HD212771

DeltaTuc

HD212301

Kruger60A

Zeta1Aqr

DeltaCephei

Delta1Gru

_5Lac

Delta2Gru

AlKalbalRai

_6Lac

HD213240

AlphaLac

BetaPsA

EtaAqr

Situla

_11Lac

EpsilonPsA

Homam

BetaGru

Matar

BetaOct

LamdaPeg

HD215497

XiPeg

BD434305

EpsilonGru

Tau2Aqr

IotaCep

Sadalbari

GammaPsA

LamdaAqr

Gliese876

TauGru

Skat

HD216437

HD216770

DeltaPsA

_51Peg

Fomalhaut

HD217107

ZetaGru

OmicronAnd

HD217786

Scheat

FumAlSamakah

Markab

Lacaille9352

_86Aqr

ThetaGru

HR8799

HD218566

_88Aqr

IotaGru

PhiAqr

_91Aqr

GammaPsc

GammaTuc

HD219828

GammaScl

HD220074

_7Psc

Kerb

_98Aqr

_99Aqr

HD220773

KappaPsc

ThetaPsc

_14And

HD221287

BetaScl

IotaPhe

HIP116454

LamdaAnd

HD222095

HD222155

IotaAnd

GammaCep

IotaPsc

KappaAnd

HD222582

LambdaPsc

Omega2Aqr

_19Psc

DeltaScl

Lalande46650

PiPhe

OmegaPsc

HD224693

EpsilonTuc

NGC4349127

BD202457

HD13189

NGC24233

M67SAND364

HD240210

HD216536

HD17092

BD48738

TYC14226141

Kepler432

Kepler815

Kepler1004

HD10442

Kepler1270

Kepler435

Kepler278

Kepler637

Kepler1394

Kepler643

Kepler774

WASP71

Kepler433

HATP40

WASP78

WASP82

Kepler1274

Kepler1580

HD171028

Kepler40

WASP88

XO3

WASP73

Kepler541

Kepler1452

Kepler14

Kepler462

Kepler1434

Kepler959

Kepler516

WASP100

Kepler1298

Kepler911

Kepler522

HATP7

Kepler1158

Kepler1517

Kepler1171

Kepler1219

Kepler1518

Kepler50

WASP63

Kepler1626

Kepler1137

HATP49

WASP54

Kepler33

Kepler1360

TrES4

Kepler644

Kepler1015

Kepler471

CoRoT26

Kepler1300

Kepler1375

Kepler1364

CoRoT28

Kepler1244

WASP99

PH1

Kepler1586

WASP48

WASP66

Kepler1326

Kepler880

Kepler338

Kepler1502

Kepler1115

Kepler1051

Kepler1382

WASP72

Kepler812

KOI13

WASP68

HATP41

Kepler470

Kepler1543

Kepler1618

Kepler642

Kepler805

CoRoT19

WASP74

Kepler129

WASP79

Kepler849

HATP33

WASP12

Kepler36

Kepler1487

HATP39

Kepler448

CoRoT23

Kepler1121

HATP4

Kepler464

KELT6

HATP8

WASP13

Kepler1002

Kepler381

Kepler1239

HATP13

CoRoT3

Kepler1345

Kepler853

Kepler997

Kepler1112

Kepler493

Kepler44

WASP1

Kepler289

CoRoT17

Kepler1533

Kepler74

Kepler635

Kepler1000

HATS9

HATP57

Kepler910

Kepler1622

Kepler627

Kepler100

Kepler8

Kepler4

Kepler12

KELT3

Kepler1238

WASP15

HATP14

Kepler483

Kepler117

Kepler791

HATP6

Kepler521

Kepler527

Kepler1442

Kepler103

Kepler514

Kepler1383

WASP103

HATP35

HATP56

Kepler1421

Kepler1640

Kepler1154

Kepler1340

Kepler758

Kepler43

Kepler510

Kepler1515

Kepler79

Kepler1104

HATS3

Kepler1311

Kepler1483

Kepler1597

Kepler1571

HATP46

Kepler1569

Kepler1323

Kepler930

WASP106

WASP20

Kepler39

Kepler907

Kepler794

Kepler915

Kepler434

Kepler1209

Kepler467

CoRoT11

Kepler1256

WASP94A

HATP31

Kepler1275

Kepler820

Kepler1602

Kepler1079

OGLETR56

Kepler1428

WASP61

Kepler127

Kepler126

Kepler410A

Kepler1163

Kepler650

Kepler136

Kepler104

Kepler885

Kepler427

WASP94B

WASP38

WASP26

Kepler480

Kepler1373

Kepler1100

Kepler473

Kepler1054

Kepler1616

Kepler1279

WASP24

Kepler631

Kepler1435

OGLETR132

Kepler1527

Kepler1633

Kepler1072

Kepler1070

Kepler784

Kepler1280

Kepler596

Kepler507

HATP9

Kepler109

HATP45

HATP24

Kepler25

WASP3

WASP14

Kepler1488

Kepler1603

Kepler839

Kepler718

Kepler887

Kepler1370

Kepler1385

Kepler1336

Kepler798

Kepler512

Kepler639

Kepler1288

Kepler1501

Kepler1181

Kepler1511

Kepler1493

Kepler982

Kepler465

WASP101

Kepler412

Kepler135

Kepler1159

Kepler769

Kepler1592

Kepler1475

WASP62

Kepler1249

Kepler1285

Kepler1349

Kepler1293

Kepler1084

Kepler1510

Kepler628

Kepler1443

Kepler923

Kepler1609

Kepler1412

Kepler535

Kepler1496

Kepler854

Kepler1445

Kepler873

Kepler1531

Kepler703

Kepler1396

Kepler494

WASP75

WASP31

Kepler1283

Kepler1524

Kepler508

Kepler904

Kepler1589

Kepler1472

Kepler1233

Kepler889

Kepler68

WASP7

Kepler1620

Kepler750

Kepler1354

Kepler1581

Kepler1271

Kepler144

Kepler788

Kepler741

Kepler1422

HATP16

Kepler924

Kepler655

Kepler1621

Kepler1201

Kepler584

Kepler634

Kepler811

Kepler1169

Kepler1395

Kepler909

HATP29

Kepler937

Kepler814

Kepler502

Kepler972

Kepler606

Kepler1617

Kepler1551

Kepler1587

Kepler620

Kepler824

Kepler1508

Kepler1514

Kepler544

Kepler1224

HATP32

HATP30

WASP70A

Kepler1213

CoRoT14

Kepler1276

Kepler1248

Kepler1346

Kepler645

Kepler1193

Kepler1607

Kepler919

Kepler1094

HATP23

KIC11442793

Kepler509

WASP17

HATP34

Kepler653

Kepler1641

Kepler1632

Kepler1267

Kepler1433

Kepler1093

Kepler848

Kepler669

Kepler511

Kepler1568

Kepler1225

Kepler1056

CoRoT25

CoRoT16

Kepler506

CoRoT5

Kepler1547

Kepler624

Kepler998

Kepler132

Kepler1639

Kepler1398

Kepler1165

WASP58

OGLETR10

WASP117

Kepler1289

Kepler1189

Kepler105

Kepler685

Kepler1278

Kepler1119

Kepler1113

Kepler1591

Kepler1557

Kepler1590

Kepler1106

Kepler1003

HATP5

Kepler1080

Kepler1199

Kepler886

Kepler1352

Kepler806

Kepler690

Kepler557

Kepler852

Kepler914

Kepler956

WASP47

Kepler766

Kepler633

Kepler1407

Kepler1403

WTS1

Kepler1103

Kepler826

Kepler525

Kepler1212

Kepler590

Kepler965

Kepler1269

Kepler1416

Kepler546

Kepler1111

Kepler526

WASP60

Kepler1085

OGLETR182

Kepler602

Kepler641

Kepler1063

Kepler1082

CoRoT22

Kepler1584

Kepler890

Kepler996

Kepler1344

Kepler1050

Kepler1147

Kepler1432

Kepler529

Kepler874

Kepler757

Kepler610

Kepler918

Kepler609

Kepler1025

Kepler1180

Kepler871

HATP1

Pr201

Kepler420

Kepler1047

WASP95

WASP22

Kepler130

Kepler1255

Kepler714

Kepler1031

Kepler1613

Kepler803

Kepler1486

Kepler792

Kepler1316

Kepler490

Kepler1406

Kepler1397

Kepler197

Kepler1485

Kepler908

CoRoT12

WASP56

CoRoT1

Kepler1535

Kepler619

Kepler912

Kepler1449

Kepler680

Kepler1401

Kepler1391

Kepler1253

Kepler497

Kepler748

Kepler1550

Kepler654

Kepler593

Kepler1057

Kepler835

Kepler830

Kepler1044

Kepler1561

Kepler772

Kepler875

HATS10

HATP21

HATP28

Kepler524

Kepler1218

HATP36

WASP28

Kepler488

Kepler796

Kepler978

Kepler1272

Kepler850

Kepler431

Kepler1187

Kepler1598

Kepler481

Kepler1436

Kepler476

Kepler1252

Kepler1268

Kepler485

Kepler881

WASP32

Kepler520

WASP35

Kepler1473

Kepler883

Kepler983

HATP15

Kepler1088

Kepler618

Kepler990

Kepler696

Kepler1230

Kepler540

Kepler754

Kepler762

Kepler822

Kepler1307

Kepler825

Kepler1368

Kepler474

CoRoT27

Kepler1594

Kepler1041

Kepler1260

Kepler872

Kepler1574

Kepler1217

Kepler1061

Kepler647

Kepler1424

Kepler545

Kepler454

Kepler1576

Kepler1405

Kepler513

Kepler1429

Kepler1601

Kepler860

Kepler1184

Kepler765

Kepler1005

Kepler1516

Kepler1141

Kepler840

Kepler1188

Kepler891

Kepler731

Kepler807

Kepler1207

Kepler1109

Kepler1478

Kepler1555

Kepler528

WASP55

WASP97

Kepler980

WASP21

WASP64

Kepler10

XO5

Kepler804

Kepler1182

Kepler722

Kepler1615

Kepler1444

Kepler1468

Kepler626

Kepler466

WASP83

Kepler1365

Kepler666

WASP96

Kepler1338

Kepler771

Kepler17

Kepler1562

Kepler1525

Kepler1046

HATP22

Kepler630

HATS1

Kepler106

Kepler1202

Kepler1431

Kepler855

Kepler1174

Kepler1495

Kepler1386

Kepler745

Kepler1474

Kepler715

Kepler1091

Kepler843

Kepler1538

Kepler810

Kepler759

Kepler836

Kepler555

Kepler817

Kepler1052

Kepler1204

Kepler1327

Kepler1348

Kepler897

Kepler501

Kepler1155

Kepler604

Kepler592

Kepler552

Kepler1528

Kepler1131

Kepler131

Kepler500

Kepler491

WASP5

CoRoT6

Kepler1417

Kepler223

Kepler789

Kepler1560

Kepler1637

Kepler1645

Kepler879

Kepler1226

Kepler929

Kepler1176

Kepler664

Kepler1636

Kepler1077

Kepler950

Kepler1466

Kepler870

Kepler1426

Kepler966

Kepler906

CoRoT20

Kepler780

Kepler96

Kepler573

XO2S

M67YBP1194

Kepler782

CoRoT13

Kepler773

Kepler603

Kepler1129

Kepler581

Kepler1092

Kepler657

Kepler1427

Kepler154

Kepler1016

Kepler1623

Kepler864

Kepler1149

Kepler611

Kepler1303

Kepler588

Kepler608

Kepler1573

Kepler1619

Kepler1419

Kepler1068

Kepler1073

Kepler1462

Kepler1464

Kepler730

Kepler926

Kepler1231

Kepler1500

Kepler503

Kepler1629

Kepler1441

Kepler1457

TrES2

WASP37

Kepler1099

CoRoT18

Kepler1156

HD95872

Kepler1098

Kepler857

Kepler927

Kepler1328

Kepler1060

Kepler1369

Kepler1509

Kepler1220

Kepler1297

Kepler670

Kepler677

Kepler1451

Kepler952

Kepler713

Kepler1491

Kepler1183

Kepler1258

Kepler893

Kepler1563

Kepler1599

Kepler77

Kepler953

Kepler1542

Kepler537

Kepler423

Kepler1588

WASP19

Kepler517

Kepler986

Kepler534

Kepler648

Kepler556

Kepler1250

Kepler1264

Kepler719

Kepler1069

Kepler1479

Kepler1262

Kepler1286

Kepler809

Kepler1066

Kepler1216

Kepler1390

WASP49

Kepler616

XO2

Kepler831

Kepler1177

Kepler41

Kepler1438

Kepler708

Kepler1035

Kepler1142

Kepler1294

Kepler1399

Kepler1196

Kepler1548

Kepler1306

Kepler704

Kepler1523

Kepler199

Kepler1118

Kepler945

Kepler829

Kepler903

Kepler576

Kepler823

Kepler613

WASP104

Kepler1240

Kepler612

Kepler498

Kepler1513

Kepler1440

Kepler700

Kepler688

Kepler1476

Kepler579

Kepler1372

Kepler793

Kepler1305

Kepler1376

Kepler625

WASP135

Kepler795

Kepler1144

Kepler838

Kepler940

Kepler981

Kepler1040

HATP25

WASP77A

Kepler46

Kepler694

Kepler1631

Kepler565

Kepler597

Kepler539

Kepler575

HATP44

Kepler1572

Kepler1463

Kepler1556

Kepler1447

Kepler1497

Kepler869

Kepler1425

Kepler671

Kepler559

Kepler1227

Kepler683

Kepler863

Kepler797

Kepler1638

Kepler1127

WASP16

WASP8

WASP45

WASP36

Kepler1055

Kepler591

Kepler1625

Kepler767

Kepler1102

Kepler649

Kepler424

Kepler1287

Kepler1381

Kepler1494

Kepler884

Kepler1211

Kepler640

Kepler1458

CoRoT9

Kepler1546

Kepler1186

Kepler1125

XO1

Kepler1116

Kepler1065

Kepler1243

Kepler948

Kepler1067

Kepler1087

Kepler69

Kepler946

Kepler585

Kepler561

Kepler308

Kepler1135

Kepler1330

Kepler638

Kepler1612

Kepler1380

Kepler1453

Kepler1611

HATS14

Kepler799

Kepler1215

Kepler1126

Kepler744

Kepler984

Kepler902

Kepler761

Kepler1339

Kepler1117

Kepler1343

Kepler1471

Kepler1522

Kepler1448

Kepler1506

Kepler569

Kepler746

Kepler728

WASP34

Kepler1290

Kepler1292

Kepler856

Kepler922

Kepler1567

Kepler813

WASP44

HATS4

HATP38

Kepler554

Kepler1596

Kepler93

Kepler1138

Kepler1312

Kepler1277

Kepler1411

Kepler1575

Kepler686

Kepler865

Kepler1033

Kepler770

Kepler426

Kepler586

Kepler1393

Kepler1078

Kepler818

Kepler1095

Kepler564

Kepler1484

Kepler672

Kepler1194

Kepler720

Kepler1333

WASP25

Kepler1210

WASP46

WASP4

Kepler1583

Kepler867

Kepler582

Kepler1585

Kepler943

Kepler646

Kepler1101

Kepler1334

Kepler1325

Kepler729

Kepler574

Kepler492

Kepler1139

Kepler827

Kepler987

Kepler678

Kepler461

Kepler1273

Kepler583

Kepler710

Kepler1519

Kepler1012

Kepler1128

Kepler921

Kepler1299

Kepler846

Kepler858

Kepler698

Kepler899

Kepler548

CoRoT2

Kepler63

Kepler1437

Kepler1133

Kepler1332

Kepler739

Kepler1342

Kepler888

Kepler802

Kepler571

Kepler961

Kepler1198

CoRoT29

Kepler1489

Kepler463

Kepler1235

Kepler832

Kepler1357

Kepler1043

Kepler542

Kepler538

Kepler1123

Kepler562

Kepler1564

Kepler1237

Kepler570

HATS2

WASP39

Kepler1570

Kepler1023

Kepler723

Kepler1282

Kepler536

Kepler1634

Kepler1469

Kepler1036

Kepler936

Kepler1160

Kepler868

Kepler1295

Kepler530

Kepler1251

Kepler764

Kepler938

Kepler1122

Kepler783

Kepler1172

Kepler587

Kepler1232

Kepler682

HATS13

Kepler1018

Kepler75

Kepler652

Kepler1532

Kepler487

Kepler697

WASP89

Kepler1310

Kepler1011

Kepler1153

Kepler1001

Kepler605

Kepler518

Kepler1643

Kepler689

Kepler1530

HATP37

HATS5

WASP67

WASP41

Kepler594

Kepler947

Kepler1402

Kepler740

Kepler1610

Kepler1185

Kepler1017

Kepler1490

Kepler963

Kepler882

Kepler1257

WASP6

CoRoT7

Kepler468

Kepler484

Kepler667

Kepler1322

Kepler1028

Kepler651

HATP27

Pr211

TrES5

Kepler439

M67YBP1514

Kepler1175

Kepler1644

Kepler425

Kepler684

Kepler941

Kepler1454

Kepler598

Kepler1578

Kepler1021

Kepler949

Kepler523

Kepler958

Kepler724

Kepler1534

Kepler623

Kepler1505

Kepler727

Kepler1606

Kepler733

Kepler962

Kepler692

Kepler1166

Kepler905

Kepler702

Kepler920

Kepler1507

Kepler760

Kepler851

Kepler816

Kepler894

Kepler743

Kepler717

Kepler19

Kepler1392

Kepler553

Kepler726

Kepler1313

Kepler971

Kepler939

Kepler1151

WASP42

Kepler985

Kepler1635

WASP50

Kepler629

Kepler1162

Kepler775

Kepler955

Kepler1014

Kepler549

Kepler701

Kepler1108

Kepler862

Kepler1642

Kepler751

Kepler673

Kepler1482

Kepler679

Kepler632

Kepler964

Kepler1549

Kepler1415

WASP2

Kepler725

Kepler1627

Kepler1081

Kepler932

Kepler933

Kepler706

HATP17

WASP57

HATP3

OGLETR111

Kepler248

Kepler1281

Kepler1114

Kepler979

Kepler1038

Kepler515

Kepler589

Kepler499

Kepler1371

Kepler1245

Kepler752

Kepler944

Kepler977

Kepler1132

Kepler1296

Kepler1192

Kepler578

Kepler1355

Kepler550

Kepler495

Kepler595

Kepler976

Qatar1

Kepler969

Kepler1467

Kepler1600

Kepler663

Kepler1168

Kepler668

Kepler1377

Kepler1236

Kepler1090

Kepler1221

Kepler1302

Kepler1173

HATP19

Kepler496

Kepler1107

Kepler1027

Kepler656

Kepler1559

Kepler800

Kepler738

Kepler1605

Kepler1010

Kepler1045

Kepler1247

WASP69

TrES3

Kepler1130

Kepler1304

Kepler819

Kepler1134

Kepler614

Kepler1554

Kepler1205

Kepler600

Kepler1566

Kepler931

Kepler479

Kepler1498

Kepler1301

Kepler1071

Kepler896

Kepler841

Kepler1504

Kepler1553

Kepler837

Kepler736

Kepler558

Kepler1480

Kepler1191

Kepler1374

Kepler1541

Kepler916

Kepler1179

Kepler877

WASP29

TrES1

Kepler519

Kepler607

Kepler1214

Kepler995

Kepler735

Kepler1404

Kepler636

Kepler821

Kepler967

Kepler1545

Kepler711

Kepler1595

Kepler1020

Kepler1413

Kepler1241

Kepler1263

Kepler1309

Kepler790

Kepler695

Kepler1291

Kepler1034

Kepler428

Kepler1539

Kepler478

Kepler1222

Kepler763

Kepler1317

WASP52

Kepler566

Kepler411

Kepler1347

Kepler1064

Kepler1097

Kepler532

Kepler1358

Kepler572

Kepler1164

Kepler1558

CoRoT10

Kepler1379

Kepler1409

Kepler477

Kepler756

Kepler599

Kepler475

Kepler1420

Kepler601

Kepler1361

Kepler567

Kepler1284

HATP26

Kepler712

Kepler1477

Kepler721

Kepler699

Kepler781

Kepler768

Kepler989

Kepler1024

Kepler1400

Kepler747

Kepler734

Kepler1037

Kepler1552

Kepler1008

Kepler776

Kepler1356

Kepler716

Kepler973

Kepler861

Kepler1499

Kepler472

OGLETR113

Kepler1529

Kepler1261

CoRoT8

Kepler1259

Kepler1537

Kepler1029

Kepler778

Kepler563

Kepler1143

Kepler755

Kepler1593

Kepler878

Kepler1083

Kepler37

Kepler934

Kepler859

Kepler828

Kepler876

Kepler847

Kepler1148

Kepler709

Kepler1387

WASP23

Kepler1521

Kepler954

Kepler1013

Kepler1266

Kepler917

Kepler1604

Kepler1030

WTS2

Kepler1208

Kepler1170

Kepler681

Kepler489

Kepler707

Kepler1614

Kepler1470

Kepler1234

Kepler421

Kepler1254

Kepler531

Kepler1167

Kepler1026

Kepler675

Kepler749

Kepler1423

Kepler957

Kepler1481

Kepler845

Kepler1315

Kepler1206

Kepler975

Kepler1145

Kepler942

Kepler1223

Kepler1414

Kepler486

Kepler1178

Kepler1446

HATP18

WASP84

BD103166

Kepler102

Kepler1228

Kepler1362

Kepler1320

Kepler1384

Kepler659

Kepler1335

Kepler78

Kepler1120

Kepler662

Kepler1242

Kepler1039

WASP11

Kepler1544

Kepler1577

Kepler1459

Kepler1389

Kepler665

Kepler1076

Kepler992

Kepler1461

Kepler1503

Kepler1006

Kepler786

Kepler1324

Kepler1565

Kepler1140

Kepler842

Kepler547

Kepler951

Kepler935

Kepler577

Kepler900

Kepler687

Kepler167

Kepler1059

Kepler1430

Kepler693

Kepler482

Kepler1150

Kepler1363

Kepler892

Kepler1353

Kepler533

Kepler960

Kepler1608

Kepler925

Kepler1418

Kepler1190

Kepler1492

Kepler1341

Kepler1359

Kepler1042

Kepler1197

Qatar2

Kepler1465

Kepler660

Kepler1032

Kepler866

Kepler742

Kepler1520

Kepler1195

Kepler808

Kepler785

Kepler1157

Kepler443

HATP12

WASP98

Kepler1007

Kepler436

Kepler1146

Kepler1110

Kepler968

Kepler928

Kepler1318

Kepler1048

Kepler1200

Kepler1579

Kepler1062

WASP10

HATP20

Kepler1329

Kepler1540

Kepler1526

Kepler1246

Kepler1058

Kepler1053

Kepler1265

Kepler1331

Kepler615

Kepler621

Kepler1105

Kepler437

Kepler1136

Kepler1450

Kepler1022

Kepler1460

Kepler543

Kepler1536

Kepler1351

Kepler1337

Kepler1378

Kepler1019

Kepler661

Kepler970

Kepler1512

Kepler1086

Kepler834

Kepler753

Kepler62

Kepler580

Kepler801

Kepler551

Kepler1630

Kepler1096

Kepler898

Kepler833

Kepler61

Kepler1456

Kepler787

HATP54

WASP59

Kepler913

Kepler622

Kepler1388

Kepler991

Kepler1203

Kepler895

Kepler1455

K221

Kepler1366

Kepler1367

Kepler658

Kepler1410

Kepler442

WASP43

Kepler1314

WASP80

HATS6

K222

Kepler844

Kepler1161

Kepler901

Kepler1074

Kepler1009

Kepler674

K23

Kepler777

Kepler440

Kepler441

Kepler45

Kepler994

Kepler1075

Kepler1319

Kepler993

Kepler32

Kepler505

Kepler568

Kepler1152

Kepler1350

Kepler988

Kepler1321

Kepler438

Kepler1628

Kepler1229

Kepler705

KOI4427

GJ3470

Kepler691

Kepler974

Kepler676

Kepler1089

Kepler1049

Kepler617

Kepler737

Kepler186

Kepler1624

Kepler732

Kepler779

GJ3341

GJ3634

Kepler1439

GJ3293

Kepler1308

Kepler1124

Kepler504

Kepler560

Kepler1582

K225

Kepler1646

Kepler446

GJ1214

Kepler445

Kepler42

Kepler1408

GJ317

XO4

OGLE05169L

BetaPhe

HD21291

AlphaCam

_3Pup

RhoLeo

KsiUMa

Zeta1Sco

MuSgr

SiriusA

SiriusB

CastorA

CastorB

CastorAa

CastorAb

CastorBa

CastorBb

Kepler16

Kepler16A

Kepler16B

ProcyonA

ProcyonB

MiraA

MiraB

EpsilonAurigaeA

EpsilonAurigaeB

Polaris

PolarisB

PolarisAa

PolarisAb

Gliese667

Gliese667C

Gliese667A

Gliese667B

AlphaCentauri

AlphaCentauriAB

HIP98001

HIP98001B

HIP98001Aa

HIP98001Ab

XiTauri

XiTauriB

XiTauriAab

XiTauriAc

XiTauriAa

XiTauriAb

MizarAlcor

MizarAlcorABMizarA

MizarAlcorABMizarB

MizarAlcorABMizarAa

MizarAlcorABMizarAb

MizarAlcorABMizarBa

MizarAlcorABMizarBb

MizarAlcorCaAlcor

MizarAlcorCbAlcor

TVCrateris

TVCraterisB

TVCraterisAa

TVCraterisAb

TVCraterisBa

TVCraterisBb

Mintaka

MintakaC

MintakaA

MintakaB

MintakaCa

MintakaCb

MintakaAa

MintakaAb

BetaTucanae

BetaTucanaeAB

BetaTucanaeCD

BetaTucanaeA

BetaTucanaeB

BetaTucanaeD

BetaTucanaeQ

HD139691

HD139691A

HD139691B

HD139691Aa

HD139691Ab

HD139691C

HD139691D

HD139691CDa

HD139691Db

NuScorpii

NuScorpiiCD

NuScorpiiA

NuScorpiiB

NuScorpiiAab

NuScorpiiAc

NuScorpiiAa

NuScorpiiAb

NuScorpiiC

NuScorpiiD

NuScorpiiDa

NuScorpiiDb

BetaTucanaePQ

CastorAB

CastorC

CastorCa

CastorCb

Kepler20

Kepler22

Kepler11

Trappist1

HR9088

HR9088A

HR9088B

HR9091

HR9091A

HR9091B

HR24

HR24A

HR24B

HR159

HR159A

HR159B

HR193

HR193A

HR193B

HR219

HR219A

HR219B

HR258

HR258A

HR258B

HR321

HR321A

HR321B

HR391

HR391A

HR391B

HR404

HR404A

HR404B

HR563

HR563A

HR563B

GJ9071

GJ9071A

GJ9071B

GJ91_1

GJ91_1A

GJ91_1B

GJ98

GJ98A

GJ98B

HR731

HR731A

HR731B

HR788

HR788A

HR788B

GJ125

GJ125A

GJ125B

GJ130_1

GJ130_1A

GJ130_1B

HR1175

HR1175A

HR1175B

GJ9127

GJ9127A

GJ9127B

HR1199

HR1199A

HR1199B

HR1331

HR1331A

HR1331B

HR1394

HR1394A

HR1394B

HR2282

HR2282A

HR2282B

HR2372

HR2372A

HR2372B

HR2392

HR2392A

HR2392B

HR2439

HR2439A

HR2439B

HR2560

HR2560A

HR2560B

GJ282C

GJ282CA

GJ282CB

GJ301A

GJ301AA

GJ301AB

HR3627

HR3627A

HR3627B

HR4100

HR4100A

HR4100B

GJ400

GJ400A

GJ400B

GJ9372

GJ9372A

GJ9372B

HR4819

HR4819A

HR4819B

GJ3761

GJ3761A

GJ3761B

GJ509_1

GJ509_1A

GJ509_1B

GJ3788

GJ3788A

GJ3788B

HR5209

HR5209A

HR5209B

GJ533

GJ533A

GJ533B

HR5273

HR5273A

HR5273B

HR5544

HR5544A

HR5544B

HR5633

HR5633A

HR5633B

GJ609_2

GJ609_2A

GJ609_2B

GJ616_2

GJ616_2A

GJ616_2B

GJ623

GJ623A

GJ623B

GJ629_2A

GJ629_2AA

GJ629_2AB

HR6247

HR6247A

HR6247B

HR6516

HR6516A

HR6516B

GJ4024

GJ4024A

GJ4024B

HR6752

HR6752A

HR6752B

HR6775

HR6775A

HR6775B

GJ9624

GJ9624A

GJ9624B

HR6901

HR6901A

HR6901B

HR6890

HR6890A

HR6890B

GJ725A

GJ725AA

GJ725AB

HR7041

HR7041A

HR7041B

HR7261

HR7261A

HR7261B

HR7637

HR7637A

HR7637B

GJ791_2

GJ791_2A

GJ791_2B

GJ802

GJ802A

GJ802B

HR8246

HR8246A

HR8246B

HR8264

HR8264A

HR8264B

HR8384

HR8384A

HR8384B

Epsilon1Lyrae

Epsilon1LyraeB

Epsilon2Lyrae

Epsilon2LyraeD

GenericStar001

GenericStar002

GenericStar003

GenericStar004

GenericStar005

GenericStar006

GenericStar007

GenericStar008

GenericStar009

GenericStar010

GenericStar011

GenericStar012

GenericStar013

GenericStar014

GenericStar015

GenericStar016

GenericStar017

GenericStar018

GenericStar019

GenericStar020

GenericStar021

GenericStar022

GenericStar023

GenericStar024

GenericStar025

GenericStar026

GenericStar027

GenericStar028

GenericStar029

GenericStar030

GenericStar031

GenericStar032

GenericStar033

GenericStar034

GenericStar035

GenericStar036

GenericStar037

GenericStar038

GenericStar039

GenericStar040

GenericStar041

GenericStar042

GenericStar043

GenericStar044

GenericStar045

GenericStar046

GenericStar047

GenericStar048

GenericStar049

GenericStar050

IndividualStarCount

### class IndividualStarPort

InvalidIndividualStarPort

Ecliptic

### class InternalRepresentation

InvalidInternalRepresentation

IR_Zones

IR_Layers

### class Model

InvalidModel

DefaultModel

DidSliced

HDR

Photosphere

RAW

Visible

Internal

SDO

SDOStatic

### `addChild((IndividualStar)arg1, (int)child, (IndividualStar.IndividualStarPort)port) -> None`

Add a child object to the individual star scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (IndividualStarPort) – Coordinate system to use for adding child. See IndividualStarPort documentation for more information.

### `portId((IndividualStar)arg1, (IndividualStar.IndividualStarPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (IndividualStarPort) – Name of the port. See ‘IndividualStarPort’ documentation for more information.

### `setCatalogId((IndividualStar)arg1, (object)catalogId) -> None`

Setter for property catalogId

**Parameters:**
- catalogId (str) – Catalog id/designation of a star, only available to generic stars

### `setColor((IndividualStar)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3) – Actual color of the star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCoronaIntensity((IndividualStar)arg1, (float)coronaIntensity[, (Anim)animator]) -> None`

Setter for property coronaIntensity

**Parameters:**
- coronaIntensity (double) – Intensity of the star’s corona. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCycle((IndividualStar)arg1, (IndividualStar.Cycle)cycle[, (Anim)animator]) -> None`

Setter for property cycle

**Parameters:**
- cycle (Cycle)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFilter((IndividualStar)arg1, (IndividualStar.Filter)filter[, (Anim)animator]) -> None`

Setter for property filter

**Parameters:**
- filter (Filter)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGalacticBandIntensity((IndividualStar)arg1, (float)galacticBandIntensity[, (Anim)animator]) -> None`

Setter for property galacticBandIntensity

**Parameters:**
- galacticBandIntensity (double) – Intensity of the galactic mark band. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGalacticGridIntensity((IndividualStar)arg1, (float)galacticGridIntensity[, (Anim)animator]) -> None`

Setter for property galacticGridIntensity

**Parameters:**
- galacticGridIntensity (double) – Intensity of the galactic mark grid. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGalacticMarkLineIntensity((IndividualStar)arg1, (float)galacticMarkLineIntensity[, (Anim)animator]) -> None`

Setter for property galacticMarkLineIntensity

**Parameters:**
- galacticMarkLineIntensity (double) – Intensity of the galactic mark line. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHabitableZoneColor((IndividualStar)arg1, (Vec3)habitableZoneColor[, (Anim)animator]) -> None`

Setter for property habitableZoneColor

**Parameters:**
- habitableZoneColor (Vec3) – Color of the habitable zone of the star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHabitableZoneIntensity((IndividualStar)arg1, (float)habitableZoneIntensity[, (Anim)animator]) -> None`

Setter for property habitableZoneIntensity

**Parameters:**
- habitableZoneIntensity (double) – Intensity of the habitable zone of the star. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHybridRatio((IndividualStar)arg1, (float)hybridRatio[, (Anim)animator]) -> None`

Setter for property hybridRatio

**Parameters:**
- hybridRatio (double) – Used to define which device will display the individual star. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((IndividualStar)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the star. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setInternalRepresentation((IndividualStar)arg1, (IndividualStar.InternalRepresentation)internalRepresentation[, (Anim)animator]) -> None`

Setter for property internalRepresentation

**Parameters:**
- internalRepresentation (InternalRepresentation)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((IndividualStar)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the label of the star. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMagneticLinesIntensity((IndividualStar)arg1, (float)magneticLinesIntensity[, (Anim)animator]) -> None`

Setter for property magneticLinesIntensity

**Parameters:**
- magneticLinesIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMagnetogramIntensity((IndividualStar)arg1, (float)magnetogramIntensity[, (Anim)animator]) -> None`

Setter for property magnetogramIntensity

**Parameters:**
- magnetogramIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModel((IndividualStar)arg1, (IndividualStar.Model)model[, (Anim)animator]) -> None`

Setter for property model

**Parameters:**
- model (Model)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMotionVectorIntensity((IndividualStar)arg1, (float)motionVectorIntensity[, (Anim)animator]) -> None`

Setter for property motionVectorIntensity

**Parameters:**
- motionVectorIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMotionVectorThickness((IndividualStar)arg1, (float)motionVectorThickness[, (Anim)animator]) -> None`

Setter for property motionVectorThickness

**Parameters:**
- motionVectorThickness (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMotionVectorTrail((IndividualStar)arg1, (float)motionVectorTrail[, (Anim)animator]) -> None`

Setter for property motionVectorTrail

**Parameters:**
- motionVectorTrail (double) – Length of the trail in years representing proper motion (default is 25800)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOpening((IndividualStar)arg1, (float)opening[, (Anim)animator]) -> None`

Setter for property opening

**Parameters:**
- opening (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPhotosphereIntensity((IndividualStar)arg1, (float)photosphereIntensity[, (Anim)animator]) -> None`

Setter for property photosphereIntensity

**Parameters:**
- photosphereIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((IndividualStar)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the pointer of the star. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((IndividualStar)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current individual star pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setSaturationFactor((IndividualStar)arg1, (float)saturationFactor[, (Anim)animator]) -> None`

Setter for property saturationFactor

**Parameters:**
- saturationFactor (double) – Saturation factor of the star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setScale((IndividualStar)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the star. It can be used to enlarge apparent size of the star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTrajectoryIntensity((IndividualStar)arg1, (float)trajectoryIntensity[, (Anim)animator]) -> None`

Setter for property trajectoryIntensity

**Parameters:**
- trajectoryIntensity (double) – Intensity of the trajectory of the star. Usually in range [0;1]. If set to positive value, the star will draw a line according to it’s movement on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUseHybridRatio((IndividualStar)arg1, (float)useHybridRatio[, (Anim)animator]) -> None`

Setter for property useHybridRatio

**Parameters:**
- useHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUserCycleFilename((IndividualStar)arg1, (object)userCycleFilename[, (Anim)animator]) -> None`

Setter for property userCycleFilename

**Parameters:**
- userCycleFilename (str)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setZodiacalLightIntensity((IndividualStar)arg1, (float)zodiacalLightIntensity[, (Anim)animator]) -> None`

Setter for property zodiacalLightIntensity

**Parameters:**
- zodiacalLightIntensity (double) – Intensity of the star’s zodiacal light. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setZodiacalLightScatteringIntensity((IndividualStar)arg1, (float)zodiacalLightScatteringIntensity[, (Anim)animator]) -> None`

Setter for property zodiacalLightScatteringIntensity

**Parameters:**
- zodiacalLightScatteringIntensity (double) – Scattering intensity of the star’s zodiacal light. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property catalogId`

Catalog id/designation of a star, only available to generic stars

### property: `property color`

Actual color of the star.

### property: `property coronaIntensity`

Intensity of the star’s corona. Usually in range [0;1].

### property: `property cycle`

None( (skyExplorer.IndividualStar)arg1) -> object

### property: `property filter`

None( (skyExplorer.IndividualStar)arg1) -> object

### property: `property galacticBandIntensity`

Intensity of the galactic mark band. Usually in range [0;1]

### property: `property galacticGridIntensity`

Intensity of the galactic mark grid. Usually in range [0;1]

### property: `property galacticMarkLineIntensity`

Intensity of the galactic mark line. Usually in range [0;1]

### property: `property habitableZoneColor`

Color of the habitable zone of the star.

### property: `property habitableZoneIntensity`

Intensity of the habitable zone of the star. Usually in range [0;1].

### property: `property height`

[Read-only]

Return height of star on dome in degrees. Available only for Sun Star.

### property: `property hybridRatio`

Used to define which device will display the individual star. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the star. Usually in range [0;1].

### property: `property internalRepresentation`

None( (skyExplorer.IndividualStar)arg1) -> object

### property: `property labelIntensity`

Intensity of the label of the star. Usually in range [0;1].

### property: `property magneticLinesIntensity`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property magnetogramIntensity`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property model`

None( (skyExplorer.IndividualStar)arg1) -> object

### property: `property motionVectorIntensity`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property motionVectorThickness`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property motionVectorTrail`

Length of the trail in years representing proper motion (default is 25800)

### property: `property name`

Returns the name.

### property: `property opening`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property osgId`

Returns the osgId.

### property: `property photosphereIntensity`

None( (skyExplorer.IndividualStar)arg1) -> float

### property: `property pointerIntensity`

Intensity of the pointer of the star. Usually in range [0;1].

### property: `property pointerType`

Current individual star pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the star in the ICRF coordinate system.

### property: `property radiusRatio`

[Read-only]

Radius ratio of the star according to the unit of it’s coordinate system. In most case, value is 1.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property saturationFactor`

Saturation factor of the star.

### property: `property scale`

Scale factor of the star. It can be used to enlarge apparent size of the star.

### property: `property sourceId`

None( (skyExplorer.IndividualStar)arg1) -> int

### property: `property trajectoryIntensity`

Intensity of the trajectory of the star. Usually in range [0;1]. If set to positive value, the star will draw a line according to it’s movement on the dome.

### property: `property useHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.

### property: `property userCycleFilename`

None( (skyExplorer.IndividualStar)arg1) -> object

### property: `property zodiacalLightIntensity`

Intensity of the star’s zodiacal light. Usually in range [0;1].

### property: `property zodiacalLightScatteringIntensity`

Scattering intensity of the star’s zodiacal light. Usually in range [0;1].

---

# skyExplorer.Insert2D

## class skyExplorer.Insert2D

### class Insert2DName

InvalidInsert2D

Insert2D001

Insert2D002

Insert2D003

Insert2D004

Insert2D005

Insert2D006

Insert2D007

Insert2D008

Insert2D009

Insert2D010

Insert2D011

Insert2D012

Insert2D013

Insert2D014

Insert2D015

Insert2D016

Insert2D017

Insert2D018

Insert2D019

Insert2D020

Insert2D021

Insert2D022

Insert2D023

Insert2D024

Insert2D025

Insert2D026

Insert2D027

Insert2D028

Insert2D029

Insert2D030

Insert2D031

Insert2D032

Insert2D033

Insert2D034

Insert2D035

Insert2D036

Insert2D037

Insert2D038

Insert2D039

Insert2D040

Insert2D041

Insert2D042

Insert2D043

Insert2D044

Insert2D045

Insert2D046

Insert2D047

Insert2D048

Insert2D049

Insert2D050

Insert2D051_ConsoleSlideshow1

Insert2D052_ConsoleSlideshow2

Insert2D053_ConsoleVideo

Insert2D054_ConsoleSkyline

Insert2D055_Console

Insert2D056_AV

Insert2D057_AV

Insert2D058_AV

Insert2D059_AV

Insert2D060_AV

Insert2D061_AV

Insert2D062_AV

Insert2D063_AV

Insert2D064_AV

Insert2D065_AV

Insert2D066_AV

Insert2D067_AV

Insert2D068_AV

Insert2D069_AV

Insert2D070_AV

Insert2D071_AV

Insert2D072_AV

Insert2D073_AV

Insert2D074_AV

Insert2D075_AV

Insert2D076_LightPollution

Insert2D077_Preload

Insert2D078_Slideshow

Insert2D079_Slideshow

Insert2D080_Slideshow

Insert2D081_Slideshow

Insert2D082_Slideshow

Insert2D083_Slideshow

Insert2D084_Slideshow

Insert2D085_Slideshow

Insert2D086_Slideshow

Insert2D087_Slideshow

Insert2D088_Slideshow

Insert2D089_Slideshow

Insert2D090_Slideshow

Insert2D091_Slideshow

Insert2D092_Slideshow

Insert2D093_Slideshow

Insert2D094_Slideshow

Insert2D095_Slideshow

Insert2D096_Slideshow

Insert2D097_Slideshow

Insert2D098_Slideshow

Insert2D099_Slideshow

Insert2D100_Slideshow

Insert2D101_Slideshow

Insert2D102_Slideshow

Insert2D103_Slideshow

Insert2D104_Slideshow

Insert2D105_Slideshow

Insert2D106_Slideshow

Insert2D107_Slideshow

Insert2D108_Slideshow

Insert2D109_Slideshow

Insert2D110_Slideshow

Insert2D111_Slideshow

Insert2D112_Slideshow

Insert2D113_Slideshow

Insert2D114_Slideshow

Insert2D115_Slideshow

Insert2D116_Slideshow

Insert2D117_Slideshow

Insert2D118_Slideshow

Insert2D119_Slideshow

Insert2D120_Slideshow

Insert2D121_Slideshow

Insert2D122_Slideshow

Insert2D123_Slideshow

Insert2D124_Slideshow

Insert2D125_Slideshow

Insert2D126_Slideshow

Insert2D127_Slideshow

Insert2D128_Slideshow

Insert2D129_Slideshow

Insert2D130_Slideshow

Insert2D131_Slideshow

Insert2D132_Slideshow

Insert2D133_Slideshow

Insert2D134_Slideshow

Insert2D135_Slideshow

Insert2D136_Slideshow

Insert2D137_Slideshow

Insert2D138_Slideshow

Insert2D139_Slideshow

Insert2D140_Slideshow

Insert2D141_Slideshow

Insert2D142_Slideshow

Insert2D143_Slideshow

Insert2D144_Slideshow

Insert2D145_Slideshow

Insert2D146_Slideshow

Insert2D147_Slideshow

Insert2D148_Slideshow

Insert2D149_Slideshow

Insert2D150_Slideshow

Insert2D151_Slideshow

Insert2D152_Slideshow

Insert2D153_Slideshow

Insert2D154_Slideshow

Insert2D155_Slideshow

Insert2D156_Slideshow

Insert2D157_Slideshow

Insert2D158_Slideshow

Insert2D159_Slideshow

Insert2D160_Slideshow

Insert2D161_Slideshow

Insert2D162_Slideshow

Insert2D163_Slideshow

Insert2D164_Slideshow

Insert2D165_Slideshow

Insert2D166_Slideshow

Insert2D167_Slideshow

Insert2D168_Slideshow

Insert2D169_Slideshow

Insert2D170_Slideshow

Insert2D171_Slideshow

Insert2D172_Slideshow

Insert2D173_Slideshow

Insert2D174_Slideshow

Insert2D175_Slideshow

Insert2D176_Slideshow

Insert2D177_Slideshow

Insert2D178_Target

Insert2D179_Logo

Insert2D180_Rain

Insert2D181_Snow

Insert2D182_LightningLeft

Insert2D183_LightningCenter

Insert2D184_LightningRight

Insert2D185

Insert2D186

Insert2D187

Insert2D188

Insert2D189

Insert2D190

Insert2D191

Insert2D192

Insert2D193

Insert2D194

Insert2D195

Insert2D196

Insert2D197

Insert2D198

Insert2D199

Insert2D200

Insert2D201

Insert2D202

Insert2D203

Insert2D204

Insert2D205

Insert2D206

Insert2D207

Insert2D208

Insert2D209

Insert2D210

Insert2D211

Insert2D212

Insert2D213

Insert2D214

Insert2D215

Insert2D216

Insert2D217

Insert2D218

Insert2D219

Insert2D220

Insert2D221_SOS

Insert2D222_SOS

Insert2D223_SOS

Insert2D224_SOS

Insert2D225_SOS

Insert2D226_SOS

Insert2D227_SOS

Insert2D228_SOS

Insert2D229_SOS

Insert2D230_SOS

Insert2D231_SOS

Insert2D232_SOS

Insert2D233_SOS

Insert2D234_SOS

Insert2D235_SOS

Insert2D236_SOS

Insert2D237_SOS

Insert2D238_SOS

Insert2D239_SOS

Insert2D240_SOS

Insert2D241_NDI

Insert2D242_NDI

Insert2D243_NDI

Insert2D244_NDI

Insert2D245_NDI

Insert2D246_NDI

Insert2D247_NDI

Insert2D248_NDI

Insert2D249_NDI

Insert2D250_NDI

Insert2D251_Credits

Insert2DCount

### class Insert2DPort

InvalidInsert2DPort

CenteredPort

### class Orientation

InvalidOrientation

Out

In

### class TransitionType

InvalidTransitionType

Fade

CenterOutWipe

CenterInWipe

VerticalOutWipe

VerticalInWipe

HorizontalOutWipe

HorizontalInWipe

PushUp

PushDown

PushLeft

PushRight

SlideUp

SlideDown

SlideLeft

SlideRight

SlideUpLeft

SlideUpRight

SlideDownLeft

SlideDownRight

### class Type

InvalidType

Conic

FakeTypeDoNotUse

Spherical

Fisheye

Avm

### class VideoState

InvalidVideoState

VideoStateStop

VideoStatePlay

VideoStatePause

VideoStatePlayLoop

### `portId((Insert2D)arg1, (Insert2D.Insert2DPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (Insert2DPort) – Name of the port. See ‘Insert2DPort’ documentation for more information.

### `remove((Insert2D)arg1) -> None`

Remove the insert2D from the scene graph.

### `setChromaKey((Insert2D)arg1, (Vec3)chromaKey, (float)tolerance) -> None`

Change the chroma key used for transparency

**Parameters:**
- chromaKey (Vec3) – Color that will become transparent. (red, green, blue) in range [0;1].
- tolerance (double) – Tolerance value. Must be in range[0;1]. Greyscale tolerance used to match chroma key.

### `setColor((Insert2D)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3) – Color of the insert2d. If insert is textured, texture color will be multiplied by color value.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDistance((Insert2D)arg1, (float)distance[, (Anim)animator]) -> None`

Setter for property distance

**Parameters:**
- distance (double) – Distance of the insert from it’s parent.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFisheyeFOV((Insert2D)arg1, (float)fisheyeFOV[, (Anim)animator]) -> None`

Setter for property fisheyeFOV

**Parameters:**
- fisheyeFOV (double) – Fish eye field of view of the insert. Used only with ‘Fisheye’ geometry type.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Insert2D)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the insert 2D. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientation((Insert2D)arg1, (Insert2D.Orientation)orientation) -> None`

Setter for property orientation

**Parameters:**
- orientation (Orientation)

### `setParent((Insert2D)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the insert’s parent port in database.

### `setPosition((Insert2D)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – Position of the insert relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSize((Insert2D)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Size factor of the insert. Used only with ‘Conic’ geometry type
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSphericalBottomAngle((Insert2D)arg1, (float)sphericalBottomAngle[, (Anim)animator]) -> None`

Setter for property sphericalBottomAngle

**Parameters:**
- sphericalBottomAngle (double) – Minimum height to display panorama image. Unit is degrees, usually in range [0;90]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSphericalLeftAngle((Insert2D)arg1, (float)sphericalLeftAngle[, (Anim)animator]) -> None`

Setter for property sphericalLeftAngle

**Parameters:**
- sphericalLeftAngle (double) – Minimum azimut to display panorama image. Unit is degrees, usually in range [-180;180]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSphericalRightAngle((Insert2D)arg1, (float)sphericalRightAngle[, (Anim)animator]) -> None`

Setter for property sphericalRightAngle

**Parameters:**
- sphericalRightAngle (double) – Maximum azimut to display panorama image. Unit is degrees, usually in range [-180;180]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSphericalTopAngle((Insert2D)arg1, (float)sphericalTopAngle[, (Anim)animator]) -> None`

Setter for property sphericalTopAngle

**Parameters:**
- sphericalTopAngle (double) – Maximum height to display panorama image. Unit is degrees, usually in range [0;90]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTexture((Insert2D)arg1, (object)texture) -> None`

Setter for property texture

**Parameters:**
- texture (str) – Filepath of the texture to display on the insert. Path must be relative to user folder.

### `setType((Insert2D)arg1, (Insert2D.Type)type) -> None`

Setter for property type param type: type type: Type

setType( (Insert2D)arg1, (Insert2D.Type)key, (Insert2D.Orientation)value) -> None :Change the type of insert’s geometry. param key: New geometry type of insert. See ‘Type’ documentation for available values. type key: Type param value: New texture orientation type. Used only with ‘Conic’ geometry type. See ‘Orientation’ documentation for available values. type value: Orientation

### `setVideoState((Insert2D)arg1, (Insert2D.VideoState)videoState[, (Anim)animator]) -> None`

Setter for property videoState

**Parameters:**
- videoState (VideoState) – Current state of the video. See ‘VideoState’ documentation for available values.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setVolume((Insert2D)arg1, (float)volume[, (Anim)animator]) -> None`

Setter for property volume

**Parameters:**
- volume (double) – Audio volume when playing video file with audio tracks 0 by default.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property chromaKey`

[Read-only]

Chroma key of the insert. Values are (red, green, blue, tolerance). Each values are in range [0;1]

### property: `property color`

Color of the insert2d. If insert is textured, texture color will be multiplied by color value.

### property: `property fisheyeFOV`

Fish eye field of view of the insert. Used only with ‘Fisheye’ geometry type.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the insert 2D. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property orientation`

None( (skyExplorer.Insert2D)arg1) -> object

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of the insert’s parent port in database.

### property: `property position`

Position of the insert relative to it’s parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property size`

Size factor of the insert. Used only with ‘Conic’ geometry type

### property: `property sphericalBottomAngle`

Minimum height to display panorama image. Unit is degrees, usually in range [0;90]

### property: `property sphericalLeftAngle`

Minimum azimut to display panorama image. Unit is degrees, usually in range [-180;180]

### property: `property sphericalRightAngle`

Maximum azimut to display panorama image. Unit is degrees, usually in range [-180;180]

### property: `property sphericalTopAngle`

Maximum height to display panorama image. Unit is degrees, usually in range [0;90]

### property: `property texture`

Filepath of the texture to display on the insert. Path must be relative to user folder.

### property: `property type`

None( (skyExplorer.Insert2D)arg1) -> object

### property: `property videoDuration`

[Read-only]

Duration of the video in seconds, in case of video file have been loaded on insert.

### property: `property videoPosition`

[Read-only]

Position in seconds inside video. It have no effect if no video is loaded.

### property: `property videoStartTime`

[Read-only]

Time at which the video starts to play.

### property: `property videoState`

Current state of the video. See ‘VideoState’ documentation for available values.

### property: `property volume`

Audio volume when playing video file with audio tracks 0 by default.

---

# skyExplorer.Insert3D

## class skyExplorer.Insert3D

### class Insert3DName

InvalidInsert3D

Insert3D001

Insert3D002

Insert3D003

Insert3D004

Insert3D005

Insert3D006

Insert3D007

Insert3D008

Insert3D009

Insert3D010

Insert3D011

Insert3D012

Insert3D013

Insert3D014

Insert3D015

Insert3D016

Insert3D017

Insert3D018

Insert3D019

Insert3D020

Insert3D021

Insert3D022

Insert3D023

Insert3D024

Insert3D025

Insert3D026

Insert3D027

Insert3D028

Insert3D029

Insert3D030

Insert3D031

Insert3D032

Insert3D033

Insert3D034

Insert3D035

Insert3D036

Insert3D037

Insert3D038

Insert3D039

Insert3D040

Insert3D041

Insert3D042

Insert3D043

Insert3D044

Insert3D045

Insert3D046

Insert3D047

Insert3D048

Insert3D049

Insert3D050

Insert3D051

Insert3D052

Insert3D053_LivePatchGizmoBottomLeft

Insert3D054_LivePatchGizmoTopRight

Insert3D055_LivePatchGizmoRotation

Insert3D056_LivePatchGizmoDisplacement

Insert3D057_LivePatchGizmoBottomRight

Insert3D058_LivePatchGizmoTopLeft

Insert3D059

Insert3D060

Insert3D061

Insert3D062

Insert3D063

Insert3D064

Insert3D065

Insert3D066

Insert3D067

Insert3D068

Insert3D069_ZoomFovTarget

Insert3D070_LiveAtlas

Insert3D071_LiveAtlas

Insert3D072_LiveAtlas

Insert3D073_LiveAtlas

Insert3D074_LiveAtlas

Insert3D075_LiveAtlas

Insert3D076_LiveAtlas

Insert3D077_LiveAtlas

Insert3D078_LiveAtlas

Insert3D079_LiveAtlas

Insert3D080_LiveAtlas

Insert3D081_LiveAtlas

Insert3D082_LiveAtlas

Insert3D083_LiveAtlas

Insert3D084_LiveAtlas

Insert3D085_LiveAtlas

Insert3D086_LiveAtlas

Insert3D087_LiveAtlas

Insert3D088_LiveAtlas

Insert3D089_LiveAtlas

Insert3D090_LiveAtlas

Insert3D091_LiveAtlas

Insert3D092_LiveAtlas

Insert3D093_LiveAtlas

Insert3D094_LiveAtlas

Insert3D095_LiveAtlas

Insert3D096_LiveAtlas

Insert3D097_LiveAtlas

Insert3D098_LiveAtlas

Insert3D099_LiveAtlas

Insert3D100_LiveAtlas

Insert3D101_LiveAtlas

Insert3D102_LiveAtlas

Insert3D103_LiveAtlas

Insert3D104_LiveAtlas

Insert3D105_LiveAtlas

Insert3D106_LiveAtlas

Insert3D107_LiveAtlas

Insert3D108_LiveAtlas

Insert3D109_LiveAtlas

Insert3D110_LiveAtlas

Insert3D111_LiveAtlas

Insert3D112_LiveAtlas

Insert3D113_LiveAtlas

Insert3D114_LiveAtlas

Insert3D115_LiveAtlas

Insert3D116_LiveAtlas

Insert3D117_LiveAtlas

Insert3D118_LiveAtlas

Insert3D119_LiveAtlas

Insert3D120_LiveAtlas

Insert3D121_LiveAtlas

Insert3D122_LiveAtlas

Insert3D123_LiveAtlas

Insert3D124_LiveAtlas

Insert3D125_LiveAtlas

Insert3D126_LiveAtlas

Insert3D127_LiveAtlas

Insert3D128_LiveAtlas

Insert3D129_LiveAtlas

Insert3D130_LiveAtlas

Insert3D131_LiveAtlas

Insert3D132_LiveAtlas

Insert3D133_LiveAtlas

Insert3D134_LiveAtlas

Insert3D135_LiveAtlas

Insert3D136_LiveAtlas

Insert3D137_LiveAtlas

Insert3D138_LiveAtlas

Insert3D139_LiveAtlas

Insert3D140_LiveAtlas

Insert3D141_LiveAtlas

Insert3D142_LiveAtlas

Insert3D143_LiveAtlas

Insert3D144_LiveAtlas

Insert3D145_LiveAtlas

Insert3D146_LiveAtlas

Insert3D147_LiveAtlas

Insert3D148_LiveAtlas

Insert3D149_LiveAtlas

Insert3D150_LiveAtlas

Insert3D151_LiveAtlas

Insert3D152_LiveAtlas

Insert3D153_LiveAtlas

Insert3D154_LiveAtlas

Insert3D155_LiveAtlas

Insert3D156_LiveAtlas

Insert3D157_LiveAtlas

Insert3D158_LiveAtlas

Insert3D159_LiveAtlas

Insert3D160_LiveAtlas

Insert3D161_LiveAtlas

Insert3D162_LiveAtlas

Insert3D163_LiveAtlas

Insert3D164_LiveAtlas

Insert3D165_LiveAtlas

Insert3D166_LiveAtlas

Insert3D167_LiveAtlas

Insert3D168_LiveAtlas

Insert3D169_LiveAtlas

Insert3D170_HudGrid

Insert3D171_HudAxis

Insert3D172_LiveAtlas

Insert3D173_LiveAtlas

Insert3D174_LiveAtlas

Insert3D175_LiveAtlas

Insert3D176_LiveAtlas

Insert3D177_LiveAtlas

Insert3D178_LiveAtlas

Insert3D179_LiveAtlas

Insert3D180_LiveAtlas

Insert3D181_LiveAtlas

Insert3D182_LiveAtlas

Insert3D183_LiveAtlas

Insert3D184_LiveAtlas

Insert3D185_LiveAtlas

Insert3D186_LiveAtlas

Insert3D187_LiveAtlas

Insert3D188_LiveAtlas

Insert3D189_LiveAtlas

Insert3D190_LiveAtlas

Insert3D191_LiveAtlas

Insert3D192_LiveAtlas

Insert3D193_LiveAtlas

Insert3D194_LiveAtlas

Insert3D195_LiveAtlas

Insert3D196_LiveAtlas

Insert3D197_LiveAtlas

Insert3D198_LiveAtlas

Insert3D199_LiveAtlas

Insert3D200_LiveAtlas

Insert3D201_LiveAtlas

Insert3D202_LiveAtlas

Insert3D203_LiveAtlas

Insert3D204_LiveAtlas

Insert3D205_LiveAtlas

Insert3D206_LiveAtlas

Insert3D207_LiveAtlas

Insert3D208_LiveAtlas

Insert3D209_LiveAtlas

Insert3D210_LiveAtlas

Insert3D211_LiveAtlas

Insert3D212_LiveAtlas

Insert3D213_LiveAtlas

Insert3D214_LiveAtlas

Insert3D215_LiveAtlas

Insert3D216_LiveAtlas

Insert3D217_LiveAtlas

Insert3D218_LiveAtlas

Insert3D219_LiveAtlas

Insert3D220_LiveAtlas

Insert3D221_LiveAtlas

Insert3D222_LiveAtlas

Insert3D223_LiveAtlas

Insert3D224_LiveAtlas

Insert3D225_LiveAtlas

Insert3D226_LiveAtlas

Insert3D227_LiveAtlas

Insert3D228_LiveAtlas

Insert3D229_LiveAtlas

Insert3D230_LiveAtlas

Insert3D231_LiveAtlas

Insert3D232_LiveAtlas

Insert3D233_LiveAtlas

Insert3D234_LiveAtlas

Insert3D235_LiveAtlas

Insert3D236_LiveAtlas

Insert3D237_LiveAtlas

Insert3D238_LiveAtlas

Insert3D239_LiveAtlas

Insert3D240_LiveAtlas

Insert3D241_LiveAtlas

Insert3D242_LiveAtlas

Insert3D243_LiveAtlas

Insert3D244_LiveAtlas

Insert3D245_LiveAtlas

Insert3D246_LiveAtlas

Insert3D247_LiveAtlas

Insert3D248_LiveAtlas

Insert3D249_LiveAtlas

Insert3D250_LiveAtlas

Insert3D251_LiveAtlas

Insert3D252_LiveAtlas

Insert3D253_LiveAtlas

Insert3D254_LiveAtlas

Insert3D255_LiveAtlas

Insert3D256_LiveAtlas

Insert3D257_LiveAtlas

Insert3D258_LiveAtlas

Insert3D259_LiveAtlas

Insert3D260_LiveAtlas

Insert3D261_LiveAtlas

Insert3D262_LiveAtlas

Insert3D263_LiveAtlas

Insert3D264_LiveAtlas

Insert3D265_LiveAtlas

Insert3D266_LiveAtlas

Insert3D267_LiveAtlas

Insert3D268_LiveAtlas

Insert3D269_LiveAtlas

Insert3DCount

### class LoadingStatus

InvalidLoadingStatus

Loaded

LoadedPendingDependencies

Loading

Empty

Error

### class TextureFace

InvalidTextureFace

PositiveX

NegativeX

PositiveY

NegativeY

PositiveZ

NegativeZ

### class VideoState

InvalidVideoState

VideoStateStop

VideoStatePlay

VideoStatePause

VideoStatePlayLoop

### `getIntrospection((Insert3D)arg1) -> None`

Introspect current 3d model to find uniform and animation node result available in instrospectionOutput property.

### `modifyUniform((Insert3D)arg1, (object)uniformName, (Vec4)value, (Anim)anim) -> None`

Change insert3d uniform value, get uniform name and value by introspection

**Parameters:**
- uniformName (str) – Name of the uniform.
- value (Vec4) – New uniform value
- anim (Anim, optional) – Animator to animate uniform change, defaults to Anim()

### `remove((Insert3D)arg1) -> None`

Remove the insert3d from the scene graph.

### `rotateMatrix((Insert3D)arg1, (object)matrixName, (Vec3)value, (Anim)anim) -> None`

Rotate insert3d matrix, get matrix name by introspection

**Parameters:**
- matrixName (str) – Name of the matrix.
- value (Vec3) – Rotation value of the matrix
- anim (Anim, optional) – defaults to Anim()

### `scaleMatrix((Insert3D)arg1, (object)matrixName, (Vec3)value, (Anim)anim) -> None`

Scale insert3d matrix, get matrix name by introspection

**Parameters:**
- matrixName (str) – Name of the matrix.
- value (Vec3) – Scale value of the matrix
- anim (Anim, optional) – defaults to Anim()

### `setAnimationEvolution((Insert3D)arg1, (float)animationEvolution[, (Anim)animator]) -> None`

Setter for property animationEvolution

**Parameters:**
- animationEvolution (double) – Current position in animation. Must be in range[0:1]. It has no effect if the insert doesn’t have any animation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAnimationName((Insert3D)arg1, (object)animationName[, (Anim)animator]) -> None`

Setter for property animationName

**Parameters:**
- animationName (str) – Name of the animation currently controlled, an empty string means all the animations are controlled
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAnimationStartTime((Insert3D)arg1, (float)animationStartTime[, (Anim)animator]) -> None`

Setter for property animationStartTime

**Parameters:**
- animationStartTime (double) – Julian date use to automatically start the insert’s animation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setExposure((Insert3D)arg1, (float)exposure[, (Anim)animator]) -> None`

Setter for property exposure

**Parameters:**
- exposure (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Insert3D)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the insert3D. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensityIDV((Insert3D)arg1, (float)intensityIDV[, (Anim)animator]) -> None`

Setter for property intensityIDV

**Parameters:**
- intensityIDV (double) – Intensity of the insert3D on interactive dome view layer. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModelFilename((Insert3D)arg1, (object)modelFilename[, (Anim)animator]) -> None`

Setter for property modelFilename

**Parameters:**
- modelFilename (str) – 3D model file path. Must be a relative file path to user.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrientationHPR((Insert3D)arg1, (Vec3)orientationHPR[, (Anim)animator]) -> None`

Setter for property orientationHPR

**Parameters:**
- orientationHPR (Vec3) – HPR orientation of the 3d model relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((Insert3D)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the insert3D parent port in database.

### `setPointExposure((Insert3D)arg1, (float)pointExposure[, (Anim)animator]) -> None`

Setter for property pointExposure

**Parameters:**
- pointExposure (double) – Point exposure of the model (when model is a point cloud).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointSize((Insert3D)arg1, (float)pointSize[, (Anim)animator]) -> None`

Setter for property pointSize

**Parameters:**
- pointSize (double) – Point size of the model (when model is a point cloud).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointSizeFactor((Insert3D)arg1, (float)pointSizeFactor[, (Anim)animator]) -> None`

Setter for property pointSizeFactor

**Parameters:**
- pointSizeFactor (double) – Point size factor of the model (when model is a point cloud).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPositionLBR((Insert3D)arg1, (Vec3)positionLBR[, (Anim)animator]) -> None`

Setter for property positionLBR

**Parameters:**
- positionLBR (Vec3) – LBR position of the 3d model relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPositionXYZ((Insert3D)arg1, (Vec3)positionXYZ[, (Anim)animator]) -> None`

Setter for property positionXYZ

**Parameters:**
- positionXYZ (Vec3) – XYZ position of the 3d model relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setScale((Insert3D)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the insert3D.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowStrength((Insert3D)arg1, (float)shadowStrength[, (Anim)animator]) -> None`

Setter for property shadowStrength

**Parameters:**
- shadowStrength (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUniform((Insert3D)arg1, (object)uniformName, (Vec4)value, (Anim)anim) -> None`

Scale insert3d matrix, get matrix name by introspection

**Parameters:**
- uniformName (str) – Name of the uniform.
- value (Vec4) – New value of the uniform
- anim (Anim, optional) – defaults to Anim()

### `setVideoSpeed((Insert3D)arg1, (float)videoSpeed) -> None`

Setter for property videoSpeed

**Parameters:**
- videoSpeed (double) – Speed factor of the video (2 means 2 times faster).

### `setVideoState((Insert3D)arg1, (Insert3D.VideoState)state, (Anim)anim) -> None`

Current state of the video. See ‘VideoState’ documentation for available values.

**Parameters:**
- state (VideoState)
- anim (Anim, optional) – defaults to Anim()

### `translateMatrix((Insert3D)arg1, (object)matrixName, (Vec3)value, (Anim)anim) -> None`

Translate insert3d matrix, get matrix name by introspection

**Parameters:**
- matrixName (str) – Name of the matrix.
- value (Vec3) – Translation value of the matrix
- anim (Anim, optional) – defaults to Anim()

### `updateTexture((Insert3D)arg1, (object)nodeName, (object)texture, (int)unit, (Insert3D.TextureFace)face) -> None`

Update a texture associated with a node, get node name by introspection

**Parameters:**
- nodeName (str) – Name of the node to change the texture
- texture (str) – Path to the new texture
- unit (int) – Unit of the texture to update
- face (TextureFace, optional) – Face of the cubemap texture (if necessary), defaults to PositiveX

### property: `property animationEvolution`

Current position in animation. Must be in range[0:1]. It has no effect if the insert doesn’t have any animation.

### property: `property animationName`

Name of the animation currently controlled, an empty string means all the animations are controlled

### property: `property exposure`

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property instrospectionOutput`

[Read-only]

3D model introspection result.

### property: `property intensity`

Intensity of the insert3D. Usually in range [0;1].

### property: `property intensityIDV`

Intensity of the insert3D on interactive dome view layer. Usually in range [0;1].

### property: `property loadingStatus`

[Read-only]

### property: `property modelFilename`

3D model file path. Must be a relative file path to user.

### property: `property modelRadius`

[Read-only]

Radius of the insert3D.

### property: `property name`

Returns the name.

### property: `property orientationHPR`

HPR orientation of the 3d model relative to it’s parent coordinate system.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of the insert3D parent port in database.

### property: `property parentRadius`

[Read-only]

Radius of the parent.

### property: `property pointExposure`

Point exposure of the model (when model is a point cloud).

### property: `property pointSize`

Point size of the model (when model is a point cloud).

### property: `property pointSizeFactor`

Point size factor of the model (when model is a point cloud).

### property: `property positionLBR`

LBR position of the 3d model relative to it’s parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property scale`

Scale factor of the insert3D.

### property: `property shadowStrength`

### property: `property videoSpeed`

Speed factor of the video (2 means 2 times faster).

---

# skyExplorer.InsertText

## class skyExplorer.InsertText

### class GeometryType

InvalidGeometryType

Plane

Cylinder

Spheroid

Fisheye

### class InsertTextName

InvalidInsertText

InsertText001

InsertText002

InsertText003

InsertText004

InsertText005

InsertText006

InsertText007

InsertText008

InsertText009

InsertText010

InsertText011

InsertText012

InsertText013

InsertText014

InsertText015

InsertText016

InsertText017

InsertText018

InsertText019

InsertText020

InsertText021

InsertText022

InsertText023

InsertText024

InsertText025

InsertText026

InsertText027

InsertText028

InsertText029

InsertText030

InsertText031

InsertText032

InsertText033

InsertText034

InsertText035

InsertText036

InsertText037

InsertText038

InsertText039

InsertText040

InsertText041

InsertText042

InsertText043

InsertText044

InsertText045

InsertText046

InsertText047_Date

InsertText048_Time

InsertText049_Position

InsertText050

InsertText051_Subtitles

InsertText052_Vote

InsertText053_Vote

InsertText054_Vote

InsertText055_Vote

InsertText056_Vote

InsertText057_Vote

InsertText058_Vote

InsertText059_Vote

InsertText060_Vote

InsertText061_Vote

InsertText062_SiderealTime

InsertText063

InsertText064

InsertText065

InsertText066

InsertText067

InsertText068

InsertText069

InsertText070

InsertText071

InsertText072

InsertText073

InsertText074

InsertText075

InsertText076

InsertText077

InsertText078

InsertText079

InsertText080

InsertText081

InsertText082

InsertText083

InsertText084

InsertText085

InsertText086

InsertText087

InsertText088

InsertText089

InsertText090

InsertText091

InsertText092

InsertText093

InsertText094

InsertText095

InsertText096

InsertText097

InsertText098

InsertText099

InsertText100

InsertText101

InsertText102

InsertText103

InsertText104

InsertText105

InsertText106

InsertText107

InsertText108

InsertText109

InsertText110

InsertText111

InsertText112

InsertText113

InsertText114

InsertText115

InsertText116

InsertText117

InsertText118

InsertText119

InsertText120

InsertText121

InsertText122

InsertText123

InsertText124

InsertText125

InsertText126

InsertText127

InsertText128

InsertText129

InsertText130

InsertText131

InsertText132

InsertText133

InsertText134

InsertText135

InsertText136

InsertText137

InsertText138

InsertText139

InsertText140

InsertText141

InsertText142

InsertText143

InsertText144

InsertText145

InsertText146

InsertText147

InsertText148

InsertText149

InsertText150

InsertText151

InsertText152

InsertText153

InsertText154

InsertText155

InsertText156

InsertText157

InsertText158

InsertText159

InsertText160

InsertText161

InsertText162

InsertText163

InsertText164

InsertText165

InsertText166

InsertText167

InsertText168

InsertText169

InsertText170

InsertText171

InsertText172

InsertText173

InsertText174

InsertText175

InsertText176

InsertText177

InsertText178

InsertText179

InsertText180

InsertText181

InsertText182

InsertText183

InsertText184

InsertText185

InsertText186

InsertText187

InsertText188

InsertText189

InsertText190

InsertText191

InsertText192

InsertText193

InsertText194

InsertText195

InsertText196

InsertText197

InsertText198

InsertText199

InsertText200

InsertText201

InsertText202

InsertText203

InsertText204

InsertText205

InsertText206

InsertText207

InsertText208

InsertText209

InsertText210

InsertText211

InsertText212

InsertText213

InsertText214

InsertText215

InsertText216

InsertText217

InsertText218

InsertText219

InsertText220

InsertText221

InsertText222

InsertText223

InsertText224

InsertText225

InsertText226

InsertText227

InsertText228

InsertText229

InsertText230

InsertText231

InsertText232

InsertText233

InsertText234

InsertText235

InsertText236

InsertText237

InsertText238

InsertText239

InsertText240

InsertText241

InsertText242

InsertText243

InsertText244

InsertText245

InsertText246

InsertText247

InsertText248

InsertText249

InsertText250

InsertText251

InsertText252

InsertText253

InsertText254

InsertText255

InsertText256

InsertText257

InsertText258

InsertText259

InsertText260

InsertText261

InsertText262

InsertText263

InsertText264

InsertText265

InsertText266

InsertText267

InsertText268

InsertText269

InsertText270

InsertText271

InsertText272

InsertText273

InsertText274

InsertText275

InsertText276

InsertText277

InsertText278

InsertText279

InsertText280

InsertText281

InsertText282

InsertText283

InsertText284

InsertText285

InsertText286

InsertText287

InsertText288

InsertText289

InsertText290

InsertText291

InsertText292

InsertText293

InsertText294

InsertText295

InsertText296

InsertText297

InsertText298

InsertText299

InsertText300

InsertText301

InsertText302

InsertText303

InsertText304

InsertText305

InsertText306

InsertText307

InsertText308

InsertText309

InsertText310

InsertText311

InsertText312

InsertText313

InsertText314

InsertText315

InsertText316

InsertText317

InsertText318

InsertText319

InsertText320

InsertText321

InsertText322

InsertText323

InsertText324

InsertText325

InsertText326

InsertText327

InsertText328

InsertText329

InsertText330

InsertText331

InsertText332

InsertText333

InsertText334

InsertText335

InsertText336

InsertText337

InsertText338

InsertText339

InsertText340

InsertText341

InsertText342

InsertText343

InsertText344

InsertText345

InsertText346

InsertText347

InsertText348

InsertText349

InsertText350

InsertText351

InsertText352

InsertText353

InsertText354

InsertText355

InsertText356

InsertText357

InsertText358

InsertText359

InsertText360

InsertText361

InsertText362

InsertText363

InsertText364

InsertText365

InsertText366

InsertText367

InsertText368

InsertText369

InsertText370

InsertText371

InsertText372

InsertText373

InsertText374

InsertText375

InsertText376

InsertText377

InsertText378

InsertText379

InsertText380

InsertText381

InsertText382

InsertText383

InsertText384

InsertText385

InsertText386

InsertText387

InsertText388

InsertText389

InsertText390

InsertText391

InsertText392

InsertText393

InsertText394

InsertText395

InsertText396

InsertText397

InsertText398

InsertText399

InsertText400

InsertText401

InsertText402

InsertText403

InsertText404

InsertText405

InsertText406

InsertText407

InsertText408

InsertText409

InsertText410

InsertText411

InsertText412

InsertText413

InsertText414

InsertText415

InsertText416

InsertText417

InsertText418

InsertText419

InsertText420

InsertText421

InsertText422

InsertText423

InsertText424

InsertText425

InsertText426

InsertText427

InsertText428

InsertText429

InsertText430

InsertText431

InsertText432

InsertText433

InsertText434

InsertText435

InsertText436

InsertText437

InsertText438

InsertText439

InsertText440

InsertText441

InsertText442

InsertText443

InsertText444

InsertText445

InsertText446

InsertText447

InsertText448

InsertText449

InsertText450

InsertText451

InsertText452

InsertText453

InsertText454

InsertText455

InsertText456

InsertText457

InsertText458

InsertText459

InsertText460

InsertText461

InsertText462

InsertText463

InsertText464

InsertText465

InsertText466

InsertText467

InsertText468

InsertText469

InsertText470

InsertText471

InsertText472

InsertText473

InsertText474

InsertText475

InsertText476

InsertText477

InsertText478

InsertText479

InsertText480

InsertText481

InsertText482

InsertText483

InsertText484

InsertText485

InsertText486

InsertText487

InsertText488

InsertText489

InsertText490

InsertText491

InsertText492

InsertText493

InsertText494

InsertText495

InsertText496

InsertText497

InsertText498

InsertText499

InsertText500

InsertText501_Tiles3DCredits

InsertTextCount

### class InvertTextureType

InvalidInvertTextureType

InvertAuto

InvertOut

InvertIn

### `setColor((InsertText)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3) – Color of the text. Values are (red, green, blue). Each value must be in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDistance((InsertText)arg1, (float)distance[, (Anim)animator]) -> None`

Setter for property distance

**Parameters:**
- distance (double) – Distance of the insert text from it’s parent.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFontFilename((InsertText)arg1, (object)fontFilename) -> None`

Setter for property fontFilename

**Parameters:**
- fontFilename (str) – Text font to display on insert.

### `setGeometryType((InsertText)arg1, (InsertText.GeometryType)geometryType) -> None`

Setter for property geometryType

**Parameters:**
- geometryType (GeometryType) – Type of the geometry used to render the text. See ‘GeometryType’ enumeration documentation for available values.

### `setIntensity((InsertText)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the insert text. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setInvertTexture((InsertText)arg1, (InsertText.InvertTextureType)invertTexture) -> None`

Setter for property invertTexture

**Parameters:**
- invertTexture (InvertTextureType) – Type of texture inversion used to render the text. See ‘InvertTextureType’ for available values.

### `setParent((InsertText)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the text’s current parent port.

### `setPosition((InsertText)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – LBR position of the insert text relative to it’s parent coordinate system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSize((InsertText)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Size of the insertText on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setText((InsertText)arg1, (object)text) -> None`

Setter for property text

**Parameters:**
- text (str) – Text value to display on insert.

### `setTextOffset((InsertText)arg1, (Vec3)textOffset[, (Anim)animator]) -> None`

Setter for property textOffset

**Parameters:**
- textOffset (Vec3) – Adds an offset to the text position. Unit is degrees. Values are (azimut, height, 0)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property color`

Color of the text. Values are (red, green, blue). Each value must be in range [0;1]

### property: `property distance`

Distance of the insert text from it’s parent.

### property: `property fontFilename`

Text font to display on insert.

### property: `property geometryType`

Type of the geometry used to render the text. See ‘GeometryType’ enumeration documentation for available values.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the insert text. Usually in range [0;1].

### property: `property invertTexture`

Type of texture inversion used to render the text. See ‘InvertTextureType’ for available values.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Id of the text’s current parent port.

### property: `property position`

LBR position of the insert text relative to it’s parent coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property size`

Size of the insertText on the dome.

### property: `property text`

Text value to display on insert.

### property: `property textOffset`

Adds an offset to the text position. Unit is degrees. Values are (azimut, height, 0)

---

# skyExplorer.Light

## class skyExplorer.Light

### `setColor((Light)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3) – Color of the virtual cove. Values are (red, green, blue). Each values are in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFixtureChannelValue((Light)arg1, (int)fixture, (int)channel, (float)value, (Anim)anim) -> None`

**Parameters:**
- fixture (int)
- channel (int)
- value (double)
- anim (Anim, optional) – defaults to Anim()

### `setFixtureValue((Light)arg1, (int)fixture, (Vec4)value, (Anim)anim) -> None`

**Parameters:**
- fixture (int)
- value (Vec4)
- anim (Anim, optional) – defaults to Anim()

### `setWhite((Light)arg1, (float)white[, (Anim)animator]) -> None`

Setter for property white

**Parameters:**
- white (double) – Brightness of the white light [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property color`

Color of the virtual cove. Values are (red, green, blue). Each values are in range [0;1]

### property: `property white`

Brightness of the white light [0;1].

---

# skyExplorer.Line

## class skyExplorer.Line

### class LineName

InvalidLine

Line001

Line002

Line003

Line004

Line005

Line006

Line007

Line008

Line009

Line010

Line011

Line012

Line013

Line014

Line015

Line016

Line017

Line018

Line019

Line020

Line021

Line022

Line023

Line024

Line025

Line026

Line027

Line028

Line029

Line030

Line031

Line032

Line033

Line034

Line035

Line036

Line037

Line038

Line039

Line040

Line041

Line042

Line043

Line044

Line045

Line046

Line047

Line048

Line049

Line050

Line051

Line052

Line053

Line054

Line055

Line056

Line057

Line058

Line059

Line060

Line061

Line062

Line063

Line064

Line065

Line066

Line067

Line068

Line069

Line070

Line071

Line072

Line073

Line074

Line075

Line076

Line077

Line078

Line079

Line080

Line081

Line082

Line083

Line084

Line085

Line086

Line087

Line088

Line089

Line090

Line091

Line092

Line093

Line094

Line095

Line096

Line097

Line098

Line099

Line100

Line101

Line102

Line103

Line104

Line105

Line106

Line107

Line108

Line109

Line110

Line111

Line112

Line113

Line114

Line115

Line116

Line117

Line118

Line119

Line120

Line121

Line122

Line123

Line124

Line125

Line126

Line127

Line128

Line129

Line130

Line131

Line132

Line133

Line134

Line135

Line136

Line137

Line138

Line139

Line140

Line141

Line142

Line143

Line144

Line145

Line146

Line147

Line148

Line149

Line150

Line151

Line152

Line153

Line154

Line155

Line156

Line157

Line158

Line159

Line160

Line161

Line162

Line163

Line164

Line165

Line166

Line167

Line168

Line169

Line170

Line171

Line172

Line173

Line174

Line175

Line176

Line177

Line178

Line179

Line180

Line181

Line182

Line183

Line184

Line185

Line186

Line187

Line188

Line189

Line190

Line191

Line192

Line193

Line194

Line195

Line196

Line197

Line198

Line199

Line200

LineCount

### `setAdvancement((Line)arg1, (float)advancement[, (Anim)animator]) -> None`

Setter for property advancement

**Parameters:**
- advancement (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAdvancementDivisor((Line)arg1, (float)advancementDivisor) -> None`

Setter for property advancementDivisor

**Parameters:**
- advancementDivisor (double)

### `setContinuousMode((Line)arg1, (bool)continuousMode) -> None`

Setter for property continuousMode

**Parameters:**
- continuousMode (bool)

### `setEndPoint((Line)arg1, (int)endPoint) -> None`

Setter for property endPoint

**Parameters:**
- endPoint (int) – Id of the body representing the ending point

### `setGraduationSize((Line)arg1, (float)graduationSize[, (Anim)animator]) -> None`

Setter for property graduationSize

**Parameters:**
- graduationSize (double) – Size of the line graduation (when using 3D line)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Line)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the line. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabel((Line)arg1, (object)label) -> None`

Setter for property label

**Parameters:**
- label (str)

### `setLabelColor((Line)arg1, (Vec3)labelColor[, (Anim)animator]) -> None`

Setter for property labelColor

**Parameters:**
- labelColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Line)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLineColor((Line)arg1, (Vec3)lineColor[, (Anim)animator]) -> None`

Setter for property lineColor

**Parameters:**
- lineColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLineMode((Line)arg1, (object)lineMode) -> None`

Setter for property lineMode

**Parameters:**
- lineMode (LineMode) – True when line is used in 2D mode, false for 3D mode

### `setLineThickness((Line)arg1, (float)lineThickness[, (Anim)animator]) -> None`

Setter for property lineThickness

**Parameters:**
- lineThickness (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setStartPoint((Line)arg1, (int)startPoint) -> None`

Setter for property startPoint

**Parameters:**
- startPoint (int) – Id of the body representing the starting point

### property: `property advancement`

None( (skyExplorer.Line)arg1) -> float

### property: `property advancementDivisor`

None( (skyExplorer.Line)arg1) -> float

### property: `property continuousMode`

None( (skyExplorer.Line)arg1) -> bool

### property: `property endPoint`

Id of the body representing the ending point

### property: `property graduationSize`

Size of the line graduation (when using 3D line)

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the line. Usually in range [0;1].

### property: `property label`

None( (skyExplorer.Line)arg1) -> object

### property: `property labelColor`

None( (skyExplorer.Line)arg1) -> skyExplorer.Vec3

### property: `property labelIntensity`

None( (skyExplorer.Line)arg1) -> float

### property: `property lineColor`

None( (skyExplorer.Line)arg1) -> skyExplorer.Vec3

### property: `property lineMode`

True when line is used in 2D mode, false for 3D mode

### property: `property lineThickness`

None( (skyExplorer.Line)arg1) -> float

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property startPoint`

Id of the body representing the starting point

---

# skyExplorer.Lut

## class skyExplorer.Lut

### class LutName

InvalidLut

Lut001

Lut002

Lut003

Lut004

Lut005

LutCount

### `addPoint((Lut)arg1, (Vec2)point) -> None`

**Parameters:**
- point (Vec2)

### `clear((Lut)arg1) -> None`

### `copyFrom((Lut)arg1, (int)lutToCopy) -> None`

**Parameters:**
- lutToCopy (int)

### `createPSF((Lut)arg1, (int)sampleCount, (float)magnitudeMin, (float)magnitudeMax, (float)sizeMax) -> None`

**Parameters:**
- sampleCount (int)
- magnitudeMin (double)
- magnitudeMax (double)
- sizeMax (double)

### `removePoint((Lut)arg1, (int)index) -> None`

**Parameters:**
- index (int)

### `setColorPalette((Lut)arg1, (object)filename, (float)magnitudeMin, (float)magnitudeMax) -> None`

**Parameters:**
- filename (str)
- magnitudeMin (double)
- magnitudeMax (double)

### `setDiameterScale((Lut)arg1, (float)diameterScale[, (Anim)animator]) -> None`

Setter for property diameterScale

**Parameters:**
- diameterScale (double) – Lut gamma.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPoint((Lut)arg1, (int)index, (Vec2)point) -> None`

**Parameters:**
- index (int)
- point (Vec2)

### `setPoints((Lut)arg1, (object)points) -> None`

Setter for property points

**Parameters:**
- points (vec2Vector)

### `setSmoothSizeLimit((Lut)arg1, (float)smoothSizeLimit[, (Anim)animator]) -> None`

Setter for property smoothSizeLimit

**Parameters:**
- smoothSizeLimit (double) – Lut gamma.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSpriteScale((Lut)arg1, (float)spriteScale[, (Anim)animator]) -> None`

Setter for property spriteScale

**Parameters:**
- spriteScale (double) – Lut gamma.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSpriteSizeLimit((Lut)arg1, (float)spriteSizeLimit[, (Anim)animator]) -> None`

Setter for property spriteSizeLimit

**Parameters:**
- spriteSizeLimit (double) – Lut gamma.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSpriteTexture((Lut)arg1, (object)spriteTexture[, (Anim)animator]) -> None`

Setter for property spriteTexture

**Parameters:**
- spriteTexture (str) – Lut sprite texture path
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTransitionBandWidth((Lut)arg1, (float)transitionBandWidth[, (Anim)animator]) -> None`

Setter for property transitionBandWidth

**Parameters:**
- transitionBandWidth (double) – Lut gamma.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property diameterScale`

Lut gamma.

### property: `property gamma`

[Read-only]

Lut gamma.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property points`

None( (skyExplorer.Lut)arg1) -> object

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property smoothSizeLimit`

Lut gamma.

### property: `property spriteScale`

Lut gamma.

### property: `property spriteSizeLimit`

Lut gamma.

### property: `property spriteTexture`

Lut sprite texture path

### property: `property transitionBandWidth`

Lut gamma.

---

# skyExplorer.Mark

## class skyExplorer.Mark

### class Language

InvalidLanguage

defaultLanguage

fr_FR

en_US

la_LA

es_ES

it_IT

nl_NL

el_GR

ja_JP

ko_KR

de_DE

ro_RO

ru_RU

uk_UA

zh_CN

ar_EG

pt_BR

cs_CZ

pt_PT

sk_SK

hu_HU

fa_IR

eu_ES

tr_TR

hi_IN

kn_IN

ml_IN

bn_IN

ta_IN

pl_PL

### class MarkName

InvalidMark

Mark001

Mark002

Mark003

Mark004

Mark005

Mark006

Mark007

Mark008

Mark009

Mark010

Mark011

Mark012

Mark013

Mark014

Mark015

Mark016

Mark017

Mark018

Mark019

Mark020

Mark021

Mark022

Mark023

Mark024

Mark025

Mark026

Mark027

Mark028

Mark029

Mark030

Mark031

Mark032

Mark033

Mark034

Mark035

Mark036

Mark037

Mark038

Mark039

Mark040

Mark041

Mark042

Mark043

Mark044

Mark045

Mark046

Mark047

Mark048

Mark049

Mark050

Mark051_WelcomeGrid

Mark052_WelcomeGrid

Mark053_WelcomeGrid

MarkCount

### class PositionType

InvalidPositionType

FiniteGrid

InfiniteGrid

### class RepresentationType

InvalidRepresentationType

None

Grid

Graduation

GraduatedGrid

TextOnly

GridWithText

GraduationWithText

GraduatedGridWithText

### class TextFormat

InvalidTextFormat

FormatManual

Hour

Degree

Year

Month

CardinalPoints

### class TextOrientationMode

InvalidTextOrientationMode

OrientationNone

Auto

Zenith

Pole

Target

### class TextPosition

InvalidTextPosition

PositionNone

Centered

Min

Max

Manual

### `remove((Mark)arg1) -> None`

Remove the mark from the scene graph.

### `setAzimuth((Mark)arg1, (float)azimuth[, (Anim)animator]) -> None`

Setter for property azimuth

**Parameters:**
- azimuth (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setColor((Mark)arg1, (Vec3)color[, (Anim)animator]) -> None`

Setter for property color

**Parameters:**
- color (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFontFilename((Mark)arg1, (object)fontFilename) -> None`

Setter for property fontFilename

**Parameters:**
- fontFilename (str)

### `setGraduationSize((Mark)arg1, (float)graduationSize[, (Anim)animator]) -> None`

Setter for property graduationSize

**Parameters:**
- graduationSize (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Mark)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the mark. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLanguage((Mark)arg1, (Mark.Language)language) -> None`

Setter for property language

**Parameters:**
- language (Language)

### `setLineWidth((Mark)arg1, (float)lineWidth[, (Anim)animator]) -> None`

Setter for property lineWidth

**Parameters:**
- lineWidth (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMaxAzimuth((Mark)arg1, (float)maxAzimuth[, (Anim)animator]) -> None`

Setter for property maxAzimuth

**Parameters:**
- maxAzimuth (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMaxHeight((Mark)arg1, (float)maxHeight[, (Anim)animator]) -> None`

Setter for property maxHeight

**Parameters:**
- maxHeight (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeridianCount((Mark)arg1, (int)meridianCount) -> None`

Setter for property meridianCount

**Parameters:**
- meridianCount (int) – Number of meridian of the mark geometry.

### `setMeridianGraduationCount((Mark)arg1, (int)meridianGraduationCount) -> None`

Setter for property meridianGraduationCount

**Parameters:**
- meridianGraduationCount (int) – Number of graduation per meridian of the mark geometry.

### `setMeridianSubGraduationCount((Mark)arg1, (int)meridianSubGraduationCount) -> None`

Setter for property meridianSubGraduationCount

**Parameters:**
- meridianSubGraduationCount (int)

### `setMinAzimuth((Mark)arg1, (float)minAzimuth[, (Anim)animator]) -> None`

Setter for property minAzimuth

**Parameters:**
- minAzimuth (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMinHeight((Mark)arg1, (float)minHeight[, (Anim)animator]) -> None`

Setter for property minHeight

**Parameters:**
- minHeight (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParallelCount((Mark)arg1, (int)parallelCount) -> None`

Setter for property parallelCount

**Parameters:**
- parallelCount (int) – Number of parallel of the mark geometry.

### `setParallelGraduationCount((Mark)arg1, (int)parallelGraduationCount) -> None`

Setter for property parallelGraduationCount

**Parameters:**
- parallelGraduationCount (int) – Number of graduation per parralel of the mark geometry.

### `setParallelSubGraduationCount((Mark)arg1, (int)parallelSubGraduationCount) -> None`

Setter for property parallelSubGraduationCount

**Parameters:**
- parallelSubGraduationCount (int)

### `setParent((Mark)arg1, (int)parent) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Id of the mark’s parent port in database.

### `setPositionType((Mark)arg1, (Mark.PositionType)positionType) -> None`

Setter for property positionType

**Parameters:**
- positionType (PositionType)

### `setRadius((Mark)arg1, (float)radius[, (Anim)animator]) -> None`

Setter for property radius

**Parameters:**
- radius (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRepresentationType((Mark)arg1, (Mark.RepresentationType)representationType) -> None`

Setter for property representationType

**Parameters:**
- representationType (RepresentationType)

### `setSubGraduationSize((Mark)arg1, (float)subGraduationSize[, (Anim)animator]) -> None`

Setter for property subGraduationSize

**Parameters:**
- subGraduationSize (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTextColor((Mark)arg1, (Vec3)textColor[, (Anim)animator]) -> None`

Setter for property textColor

**Parameters:**
- textColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTextOrientationMode((Mark)arg1, (Mark.TextOrientationMode)textOrientationMode) -> None`

Setter for property textOrientationMode

**Parameters:**
- textOrientationMode (TextOrientationMode)

### `setTextSize((Mark)arg1, (float)textSize[, (Anim)animator]) -> None`

Setter for property textSize

**Parameters:**
- textSize (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property azimuth`

None( (skyExplorer.Mark)arg1) -> float

### property: `property color`

None( (skyExplorer.Mark)arg1) -> skyExplorer.Vec3

### property: `property fontFilename`

None( (skyExplorer.Mark)arg1) -> object

### property: `property graduationSize`

None( (skyExplorer.Mark)arg1) -> float

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the mark. Usually in range [0;1].

### property: `property lineWidth`

None( (skyExplorer.Mark)arg1) -> float

### property: `property maxAzimuth`

None( (skyExplorer.Mark)arg1) -> float

### property: `property maxHeight`

None( (skyExplorer.Mark)arg1) -> float

### property: `property meridianCount`

Number of meridian of the mark geometry.

### property: `property meridianGraduationCount`

Number of graduation per meridian of the mark geometry.

### property: `property meridianSubGraduationCount`

None( (skyExplorer.Mark)arg1) -> int

### property: `property minAzimuth`

None( (skyExplorer.Mark)arg1) -> float

### property: `property minHeight`

None( (skyExplorer.Mark)arg1) -> float

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parallelCount`

Number of parallel of the mark geometry.

### property: `property parallelGraduationCount`

Number of graduation per parralel of the mark geometry.

### property: `property parallelSubGraduationCount`

None( (skyExplorer.Mark)arg1) -> int

### property: `property parent`

Id of the mark’s parent port in database.

### property: `property positionType`

None( (skyExplorer.Mark)arg1) -> object

### property: `property radius`

None( (skyExplorer.Mark)arg1) -> float

### property: `property representationType`

None( (skyExplorer.Mark)arg1) -> object

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property subGraduationSize`

None( (skyExplorer.Mark)arg1) -> float

### property: `property textColor`

None( (skyExplorer.Mark)arg1) -> skyExplorer.Vec3

### property: `property textOrientationMode`

None( (skyExplorer.Mark)arg1) -> object

### property: `property textSize`

None( (skyExplorer.Mark)arg1) -> float

---

# skyExplorer.Mat

## attribute: `skyExplorer.Mat`

alias of Mat4x4

---

# skyExplorer.Mat4x4

## class skyExplorer.Mat4x4

4×4 matrix of doubles.

### `column((Mat4x4)arg1, (int)index) -> Vec4`

Returns the column at given index as a Vec4.

### `determinant((Mat4x4)arg1) -> float`

### `fill((Mat4x4)arg1, (float)value) -> None`

Fills entire matrix with the given value

### `frustum((Mat4x4)arg1, (float)left, (float)right, (float)bottom, (float)top, (float)nearPlane, (float)farPlane) -> None`

Multiplies current matrix by a perspective frustum matrix.

### `isAffine((Mat4x4)arg1) -> bool`

### `isIdentity((Mat4x4)arg1) -> bool`

Returns true if matrix is an identity matrix. Otherwise, returns false.

### `lookAt((Mat4x4)arg1, (Vec3)eye, (Vec3)center, (Vec3)up) -> None`

Multiplies current matrix by a look at orientation matrix.

### `ortho((Mat4x4)arg1, (float)left, (float)right, (float)bottom, (float)top, (float)nearPlane, (float)farPlane) -> None`

Multiplies current matrix by an orthographic projection matrix.

### `perspective((Mat4x4)arg1, (float)verticalAngle, (float)aspectRatio, (float)nearPlane, (float)farPlane) -> None`

Multiplies current matrix by a perspective projection matrix.

### `rotate((Mat4x4)arg1, (float)angle, (Vec3)vec3) -> None`

Multiplies current matrix by a rotation matrix of angle degrees around axis

### `row((Mat4x4)arg1, (int)index) -> Vec4`

Returns the row at given index as a Vec4

### `scale((Mat4x4)arg1, (Vec3)vec3) -> None`

Multiplies current matrix by a scale matrix according to given vector.

### `setColumn((Mat4x4)arg1, (int)index, (Vec4)value) -> None`

Sets the column at given index with given Vec4.

### `setRow((Mat4x4)arg1, (int)index, (Vec4)value) -> None`

Sets the row at given index with given Vec4

### `setToIdentity((Mat4x4)arg1) -> None`

Set the current matrix to an identity matrix.

### `translate((Mat4x4)arg1, (Vec3)vec3) -> None`

Multiplies current matrix by a translation matrix according to given vector

---

# skyExplorer.Messier

## class skyExplorer.Messier

### class MessierName

InvalidMessier

M1

M2

M3

M4

M5

M6

M7

M8

M9

M10

M11

M12

M13

M14

M15

M16

M17

M18

M19

M20

M21

M22

M23

M24

M25

M26

M27

M28

M29

M30

M31

M32

M33

M34

M35

M36

M37

M38

M39

M40

M41

M42

M43

M44

M45

M46

M47

M48

M49

M50

M51

M52

M53

M54

M55

M56

M57

M58

M59

M60

M61

M62

M63

M64

M65

M66

M67

M68

M69

M70

M71

M72

M73

M74

M75

M76

M77

M78

M79

M80

M81

M82

M83

M84

M85

M86

M87

M88

M89

M90

M91

M92

M93

M94

M95

M96

M97

M98

M99

M100

M101

M102

M103

M104

M105

M106

M107

M108

M109

M110

LMC

SMC

MessierCount

### class MessierPort

InvalidMessierPort

Ecliptic

LineOfSightLocal

### `addChild((Messier)arg1, (int)child, (Messier.MessierPort)port) -> None`

Add a child object to the Messier object scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (MessierPort) – Coordinate system to use for adding child. See MessierPort documentation for more information.

### `portId((Messier)arg1, (Messier.MessierPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (MessierPort) – Name of the port. See ‘MessierPort’ documentation for more information.

### `setIntensity((Messier)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the Messier object. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Messier)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the default label of the Messier object. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setScale((Messier)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the Messier object. It can be used to enlarge apparent size of the Messier object.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSize((Messier)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Scale factor of the Messier object. It can be used to enlarge apparent size of the Messier object.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the Messier object. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the default label of the Messier object. Usually in range [0;1]

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property position`

[Read-only]

Position of the Messier object in the ICRF coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property size`

Scale factor of the Messier object. It can be used to enlarge apparent size of the Messier object.

---

# skyExplorer.NGC

## class skyExplorer.NGC

### class NGCName

InvalidNGC

NGC40

NGC185

NGC246

NGC253

NGC281

NGC457

NGC663

NGC772

NGC869_NGC884

NGC891

NGC936

NGC1023

NGC1232

NGC1501

NGC1514

NGC1535

NGC1788

NGC1931

NGC2022

NGC2024

NGC2194

NGC2237

NGC2261

NGC2359

NGC2371_NGC2372

NGC2392

NGC2403

NGC2438

NGC2440

NGC2539

NGC2655

NGC2683

NGC2841

NGC2903

NGC3003

NGC3079

NGC3115

NGC3184

NGC3242

NGC3344

NGC3384

NGC3432

NGC3521

NGC3607

NGC3628

NGC3675

NGC3877

NGC3941

NGC4026

NGC4038_NGC4039

NGC4088

NGC4111

NGC4157

NGC4214

NGC4216

NGC4244

NGC4274

NGC4361

NGC4388

NGC4414

NGC4435_NGC4438

NGC4449

NGC4490

NGC4494

NGC4517

NGC4526

NGC4535

NGC4559

NGC4565

NGC4567_NGC4568

NGC4605

NGC4631

NGC4656_NGC4657

NGC4699

NGC4725

NGC4762

NGC5005

NGC5033

NGC5128

NGC5139

NGC5466

NGC5746

NGC5907

NGC6207

NGC6210

NGC6369

NGC6503

NGC6520

NGC6543

NGC6572

NGC6633

NGC6712

NGC6781

NGC6802

NGC6818

NGC6826

NGC6939

NGC6940

NGC6946

NGC6960_NGC6992_NGC6995

NGC7009

NGC7027

NGC7129

NGC7243

NGC7293

NGC7317_NGC7318_NGC7320

NGC7331

NGC7635

NGC7662

NGC7789

NGCCount

### class NGCPort

InvalidNGCPort

Ecliptic

LineOfSightLocal

### `addChild((NGC)arg1, (int)child, (NGC.NGCPort)port) -> None`

Add a child object to the NGC object scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (NGCPort) – Coordinate system to use for adding child. See NGCPort documentation for more information.

### `portId((NGC)arg1, (NGC.NGCPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (NGCPort) – Name of the port. See ‘NGCPort’ documentation for more information.

### `setIntensity((NGC)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the NGC object. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((NGC)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the default label of the NGC object. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setScale((NGC)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the NGC object. It can be used to enlarge apparent size of the NGC object.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSize((NGC)arg1, (float)size[, (Anim)animator]) -> None`

Setter for property size

**Parameters:**
- size (double) – Scale factor of the NGC object. It can be used to enlarge apparent size of the NGC object.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the NGC object. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the default label of the NGC object. Usually in range [0;1]

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property position`

[Read-only]

Position of the NGC object in the ICRF coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property size`

Scale factor of the NGC object. It can be used to enlarge apparent size of the NGC object.

---

# skyExplorer.Nebula

## class skyExplorer.Nebula

### class NebulaName

InvalidNebula

Helix

BUG

ROTTENEGG

CATEYE

REDRECTANGLE

SATURN

BUTTERFLY

ANT

SNR0509_67_5

ABELL39

DUMBBELL

LITTLEDUMBBELL

OWL

NGC2346

ESKIMO

EIGHTBURST

GHOSTOFJUPITER

SOUTHERNER

REDSPIDER

GLOWINGEYE

BLINKINGNEBULA

NGC7027

ORION

HH47

EAGLE

CRAB

HORSEHEAD

PLEIADES

NebulaCount

### class NebulaPort

InvalidNebulaPort

Ecliptic

LineOfSightEcliptic

LineOfSightLocal

### `addChild((Nebula)arg1, (int)child, (Nebula.NebulaPort)port) -> None`

Add a child object to the nebula scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (NebulaPort) – Coordinate system to use for adding child. See NebulaPort documentation for more information.

### `portId((Nebula)arg1, (Nebula.NebulaPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (NebulaPort) – Name of the port. See ‘NebulaPort’ documentation for more information.

### `setIntensity((Nebula)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the nebula. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Nebula)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the label of the nebula. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((Nebula)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the pointer of the nebula. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Nebula)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current nebula pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setScale((Nebula)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the nebula. It can be used to enlarge apparent size of the nebula.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the nebula. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the label of the nebula. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pointerIntensity`

Intensity of the pointer of the nebula. Usually in range [0;1].

### property: `property pointerType`

Current nebula pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the nebula in the ICRF coordinate system.

### property: `property radiusRatio`

[Read-only]

Radius ratio of the nebula according to the unit of it’s coordinate system. In most case, value is nebula radius in kilometers.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property scale`

Scale factor of the nebula. It can be used to enlarge apparent size of the nebula.

---

# skyExplorer.OrbitalPlace

## class skyExplorer.OrbitalPlace

### class OrbitalPlaceName

InvalidOrbitalPlace

OrbitalPlace001

OrbitalPlace002

OrbitalPlace003

OrbitalPlace004

OrbitalPlace005

OrbitalPlace006

OrbitalPlace007

OrbitalPlace008

OrbitalPlace009

OrbitalPlace010

OrbitalPlace011

OrbitalPlace012

OrbitalPlace013

OrbitalPlace014

OrbitalPlace015

OrbitalPlace016

OrbitalPlace017

OrbitalPlace018

OrbitalPlace019

OrbitalPlace020

OrbitalPlace021

OrbitalPlace022

OrbitalPlace023

OrbitalPlace024

OrbitalPlace025

OrbitalPlace026

OrbitalPlace027

OrbitalPlace028

OrbitalPlace029

OrbitalPlace030

OrbitalPlace031

OrbitalPlace032

OrbitalPlace033

OrbitalPlace034

OrbitalPlace035

OrbitalPlace036

OrbitalPlace037

OrbitalPlace038

OrbitalPlace039

OrbitalPlace040

OrbitalPlace041

OrbitalPlace042

OrbitalPlace043

OrbitalPlace044

OrbitalPlace045

OrbitalPlace046

OrbitalPlace047

OrbitalPlace048

OrbitalPlace049

OrbitalPlace050

OrbitalPlaceCount

### `setArgumentOfPeriapsis((OrbitalPlace)arg1, (float)argumentOfPeriapsis[, (Anim)animator]) -> None`

Setter for property argumentOfPeriapsis

**Parameters:**
- argumentOfPeriapsis (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAscendingNodeLongitude((OrbitalPlace)arg1, (float)ascendingNodeLongitude[, (Anim)animator]) -> None`

Setter for property ascendingNodeLongitude

**Parameters:**
- ascendingNodeLongitude (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setBstar((OrbitalPlace)arg1, (float)bstar[, (Anim)animator]) -> None`

Setter for property bstar

**Parameters:**
- bstar (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDistanceToPeriapsis((OrbitalPlace)arg1, (float)distanceToPeriapsis[, (Anim)animator]) -> None`

Setter for property distanceToPeriapsis

**Parameters:**
- distanceToPeriapsis (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEccentricity((OrbitalPlace)arg1, (float)eccentricity[, (Anim)animator]) -> None`

Setter for property eccentricity

**Parameters:**
- eccentricity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEpoch((OrbitalPlace)arg1, (float)epoch[, (Anim)animator]) -> None`

Setter for property epoch

**Parameters:**
- epoch (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEpochDays((OrbitalPlace)arg1, (float)epochDays[, (Anim)animator]) -> None`

Setter for property epochDays

**Parameters:**
- epochDays (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEpochYears((OrbitalPlace)arg1, (float)epochYears[, (Anim)animator]) -> None`

Setter for property epochYears

**Parameters:**
- epochYears (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setInclination((OrbitalPlace)arg1, (float)inclination[, (Anim)animator]) -> None`

Setter for property inclination

**Parameters:**
- inclination (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLastPeriapsisTime((OrbitalPlace)arg1, (float)lastPeriapsisTime[, (Anim)animator]) -> None`

Setter for property lastPeriapsisTime

**Parameters:**
- lastPeriapsisTime (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeanAnomaly((OrbitalPlace)arg1, (float)meanAnomaly[, (Anim)animator]) -> None`

Setter for property meanAnomaly

**Parameters:**
- meanAnomaly (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeanLongitude((OrbitalPlace)arg1, (float)meanLongitude[, (Anim)animator]) -> None`

Setter for property meanLongitude

**Parameters:**
- meanLongitude (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeanMotion((OrbitalPlace)arg1, (float)meanMotion[, (Anim)animator]) -> None`

Setter for property meanMotion

**Parameters:**
- meanMotion (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeanMotionDt((OrbitalPlace)arg1, (float)meanMotionDt[, (Anim)animator]) -> None`

Setter for property meanMotionDt

**Parameters:**
- meanMotionDt (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitColor((OrbitalPlace)arg1, (Vec3)orbitColor[, (Anim)animator]) -> None`

Setter for property orbitColor

**Parameters:**
- orbitColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((OrbitalPlace)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitThickness((OrbitalPlace)arg1, (float)orbitThickness[, (Anim)animator]) -> None`

Setter for property orbitThickness

**Parameters:**
- orbitThickness (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((OrbitalPlace)arg1, (int)parent[, (Anim)animator]) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Parent database Id+Port.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPeriapsisLongitude((OrbitalPlace)arg1, (float)periapsisLongitude[, (Anim)animator]) -> None`

Setter for property periapsisLongitude

**Parameters:**
- periapsisLongitude (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSemiMajorAxis((OrbitalPlace)arg1, (float)semiMajorAxis[, (Anim)animator]) -> None`

Setter for property semiMajorAxis

**Parameters:**
- semiMajorAxis (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property argumentOfPeriapsis`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property ascendingNodeLongitude`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property bstar`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property distanceToPeriapsis`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property eccentricity`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property epoch`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property epochDays`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property epochYears`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property inclination`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property lastPeriapsisTime`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property meanAnomaly`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property meanLongitude`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property meanMotion`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property meanMotionDt`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property name`

Returns the name.

### property: `property orbitColor`

None( (skyExplorer.OrbitalPlace)arg1) -> skyExplorer.Vec3

### property: `property orbitIntensity`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property orbitThickness`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Parent database Id+Port.

### property: `property parentFamily`

[Read-only]

Parent Family.

### property: `property parentIndex`

[Read-only]

Parent Index (in its family).

### property: `property periapsisLongitude`

None( (skyExplorer.OrbitalPlace)arg1) -> float

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property semiMajorAxis`

None( (skyExplorer.OrbitalPlace)arg1) -> float

---

# skyExplorer.ParameterizationLut

## class skyExplorer.ParameterizationLut

### class AttributeName

InvalidAttributeName

AzimuthHeight

Color

Intensity

Opacity

Position

LinesColor

ManualIntensity

TrackingIntensity

ParameterizationSunHeight

ParameterizationOpacity

### class AuxiliaryProjector

InvalidAuxiliaryProjector

CardinalPoints

EclipticCoordinates

EquatorialCoordinates

MeridianCoordinates

Azimuth

PrecessionCircle

CelestialPole

LightPollution

MoonLight

StarballIntensity

### class KeyType

InvalidKeyType

Double

Vec2

Vec3

Vec4

### class ParameterizationLutName

InvalidParameterizationLut

ParameterizationLut001

ParameterizationLut002

ParameterizationLut003

ParameterizationLut004

ParameterizationLut005

ParameterizationLut006

ParameterizationLut007

ParameterizationLut008

ParameterizationLut009

ParameterizationLut010

ParameterizationLut011

ParameterizationLut012

ParameterizationLut013

ParameterizationLut014

ParameterizationLut015

ParameterizationLut016

ParameterizationLut017

ParameterizationLut018

ParameterizationLut019

ParameterizationLut020

ParameterizationLut021

ParameterizationLut022

ParameterizationLut023

ParameterizationLut024

ParameterizationLut025

ParameterizationLut026

ParameterizationLut027

ParameterizationLut028

ParameterizationLut029

ParameterizationLut030

ParameterizationLut031

ParameterizationLut032

ParameterizationLut033

ParameterizationLut034

ParameterizationLut035

ParameterizationLut036

ParameterizationLut037

ParameterizationLut038

ParameterizationLut039

ParameterizationLut040

ParameterizationLut041

ParameterizationLut042

ParameterizationLut043

ParameterizationLut044

ParameterizationLut045

ParameterizationLut046

ParameterizationLut047

ParameterizationLut048

ParameterizationLut049

ParameterizationLut050

ParameterizationLut051_AllConstellationLines

ParameterizationLut052_AllConstellationPictures

ParameterizationLut053_AllConstellationLabels

ParameterizationLut054_AllConstellationBoundaries

ParameterizationLut055_SliderConstellationLines

ParameterizationLut056_SliderConstellationPictures

ParameterizationLut057_SliderConstellationLabels

ParameterizationLut058_SliderStarsLabels

ParameterizationLut059_StarrySkyAutoExposure

ParameterizationLut060_StarrySkyAutoContrast

ParameterizationLut061_WeatherEffectRain

ParameterizationLut062_WeatherEffectSnow

ParameterizationLutCount

### class PostBehavior

InvalidPostBehavior

DoNothing

SetOriginValue

SetGivenValue

### class Sn88ProjectorIndex

InvalidSn88ProjectorIndex

AllProjectors

Sunrise

Sunset

MorningTwilight

EveningTwilight

### `addKey((ParameterizationLut)arg1, (float)keyPosition, (Vec4)key, (ParameterizationLut.KeyType)keyType) -> None`

Add a key to the LUT.

**Parameters:**
- keyPosition (double) – Position of the key in the LUT
- key (Vec4) – Source attribute value key to add to the LUT.
- keyType (KeyType) – Type of key to Add. See ‘KeyType’ enumeration for list of available values.

### `addTargetAttribute((ParameterizationLut)arg1, (int)targetHandler, (ParameterizationLut.AttributeName)targetAttribute) -> None`

Add an attribute to pilot with the LUT.

param targetHandler: ID of the target attribute’s handler. type targetHandler: int param targetAttribute: Name of the target attribute to pilot. See ‘AttributeName’ enumeration for list of available values. type targetAttribute: AttributeName

addTargetAttribute( (ParameterizationLut)arg1, (int)targetHandler, (object)targetAttribute, (bool)automatic) -> None :Add an attribute to pilot with the LUT (advanced use). param targetHandler: ID of the target attribute’s handler. type targetHandler: int param targetAttribute: Name of the target attribute to pilot. type targetAttribute: str param automatic: Set to ON to manage automaticaly this attribute., defaults to false type automatic: bool, optional

### `addTargetAuxiliaryProjectorAttribute((ParameterizationLut)arg1, (ParameterizationLut.AuxiliaryProjector)targetProjector) -> None`

Add an auxiliary projector attribute (using starball handler) to pilot with the LUT.

**Parameters:**
- targetProjector (AuxiliaryProjector) – Id of the target auxiliary projector.

### `addTargetSn88Attribute((ParameterizationLut)arg1, (ParameterizationLut.Sn88ProjectorIndex)targetHandler, (ParameterizationLut.AttributeName)targetAttribute) -> None`

Add an attribute (using starball handler) to pilot with the LUT.

**Parameters:**
- targetHandler (Sn88ProjectorIndex) – starball handler to use.
- targetAttribute (AttributeName) – Name of the target attribute to pilot. See ‘AttributeName’ enumeration for list of available values.

### `clearKey((ParameterizationLut)arg1) -> None`

Remove all keys of the parameterization LUT.

### `clearTargetAttributes((ParameterizationLut)arg1) -> None`

Remove all target attributes of the parameterization LUT.

### `removeKey((ParameterizationLut)arg1, (float)keyPosition) -> None`

Remove a key from the LUT.

**Parameters:**
- keyPosition (double) – Position of the key to remove from the LUT

### `removeTargetAttribute((ParameterizationLut)arg1, (int)targetHandler, (ParameterizationLut.AttributeName)targetAttribute) -> None`

Remove given attribute of the parameterization LUT.

param targetHandler: ID of the target attribute’s handler. type targetHandler: int param targetAttribute: Name of the target attribute to remove from LUT. See ‘AttributeName’ enumeration for list of available values. type targetAttribute: AttributeName

removeTargetAttribute( (ParameterizationLut)arg1, (int)targetHandler, (object)targetAttribute) -> None :Remove given attribute of the parameterization LUT (advanced use). param targetHandler: ID of the target attribute’s handler. type targetHandler: int param targetAttribute: Name of the target attribute to remove from LUT. type targetAttribute: str

### `removeTargetAuxiliaryProjectorAttribute((ParameterizationLut)arg1, (ParameterizationLut.AuxiliaryProjector)targetHandler) -> None`

Remove given ausiliary projector attribute of the parameterization LUT (using starball handler).

**Parameters:**
- targetHandler (AuxiliaryProjector) – Id of the target auxiliary projector.

### `removeTargetSn88Attribute((ParameterizationLut)arg1, (ParameterizationLut.Sn88ProjectorIndex)targetHandler, (ParameterizationLut.AttributeName)targetAttribute) -> None`

Remove given attribute of the parameterization LUT (using starball handler).

**Parameters:**
- targetHandler (Sn88ProjectorIndex) – starball target handler.
- targetAttribute (AttributeName) – Name of the target attribute to remove from LUT. See ‘AttributeName’ enumeration for list of available values.

### `restore((ParameterizationLut)arg1) -> None`

Restore control on all target attributes of the parameterization lut.

### `setEnabled((ParameterizationLut)arg1, (bool)enabled) -> None`

Setter for property enabled

**Parameters:**
- enabled (bool) – Flag use to enable or disable the LUT parameterization

### `setInternalValue((ParameterizationLut)arg1, (float)internalValue[, (Anim)animator]) -> None`

Setter for property internalValue

**Parameters:**
- internalValue (double) – Input value to use for basic parameterization
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPostBehavior((ParameterizationLut)arg1, (ParameterizationLut.PostBehavior)postBehaviorType, (Vec4)postBehavior) -> None`

Change post behavior of the LUT.

**Parameters:**
- postBehaviorType (PostBehavior) – Type of post behavior to use. See ‘PostBehavior’ enumeration for list of available values.
- postBehavior (Vec4) – Post behavior value to use.

### `setSourceAttributeId((ParameterizationLut)arg1, (int)sourceHandler, (ParameterizationLut.AttributeName)sourceAttribute, (int)componentIndex) -> None`

Change the source attribute of the LUT.

param sourceHandler: Source attribute’s handler. type sourceHandler: int param sourceAttribute: Name of the source attribute of LUT. See ‘AttributeName’ enumeration for list of available values. type sourceAttribute: AttributeName param componentIndex: Component index of the source attribute. type componentIndex: int

setSourceAttributeId( (ParameterizationLut)arg1, (int)sourceHandler, (object)sourceAttribute, (int)componentIndex) -> None :Change the source attribute of the LUT (advanced use). param sourceHandler: Source attribute’s handler. type sourceHandler: int param sourceAttribute: Name of the source attribute of LUT. type sourceAttribute: str param componentIndex: Component index of the source attribute. type componentIndex: int

### `setSourceSunHeight((ParameterizationLut)arg1) -> None`

Set the source attribute of the LUT to ‘ParameterizationSunHeight’. Equivalent to setSourceAttributeId(SunId, ParameterizationLut.ParameterizationSunHeight)

### property: `property attributeList`

[Read-only]

List of all attributes currently contained by the parameterization LUT.

### property: `property enabled`

Flag use to enable or disable the LUT parameterization

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property internalValue`

Input value to use for basic parameterization

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pilotedAttributeList`

[Read-only]

List of all attributes currently piloted by the parameterization LUT.

### property: `property postBehavior`

[Read-only]

Behavior of the attribute at end of parameterization

### property: `property postValue`

[Read-only]

Value of the attribute at end of parameterization. When using a SetGivenValue post behavior

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property srcAttributID`

[Read-only]

Name of the source attribute of the LUT parameterization

### property: `property srcComponentIndex`

None( (skyExplorer.ParameterizationLut)arg1) -> int

### property: `property srcHandlerID`

[Read-only]

ID of the source handler of the LUT parameterization

---

# skyExplorer.Patch

## class skyExplorer.Patch

### class PatchName

InvalidPatch

Patch001

Patch002

Patch003

Patch004

Patch005

Patch006

Patch007

Patch008

Patch009

Patch010

Patch011

Patch012

Patch013

Patch014

Patch015

Patch016

Patch017

Patch018

Patch019

Patch020

Patch021

Patch022

Patch023

Patch024

Patch025

Patch026

Patch027

Patch028

Patch029

Patch030

Patch031

Patch032

Patch033

Patch034

Patch035

Patch036

Patch037

Patch038

Patch039

Patch040

Patch041

Patch042

Patch043

Patch044

Patch045

Patch046

Patch047

Patch048

Patch049

Patch050

Patch051

Patch052

Patch053

Patch054

Patch055

Patch056

Patch057

Patch058

Patch059

Patch060

PatchCount

### `setFilename((Patch)arg1, (object)filename[, (Anim)animator]) -> None`

Setter for property filename

**Parameters:**
- filename (str) – Texture to apply on the live patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGamma((Patch)arg1, (Vec3)gamma[, (Anim)animator]) -> None`

Setter for property gamma

**Parameters:**
- gamma (Vec3) – Gamma correction for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHsv((Patch)arg1, (Vec3)hsv[, (Anim)animator]) -> None`

Setter for property hsv

**Parameters:**
- hsv (Vec3) – Hue, Saturation and Lightness value used for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setKeyColor((Patch)arg1, (Vec4)keyColor[, (Anim)animator]) -> None`

Setter for property keyColor

**Parameters:**
- keyColor (Vec4) – Color to remove from patch texture (RGB + tolerance).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOpacity((Patch)arg1, (float)opacity[, (Anim)animator]) -> None`

Setter for property opacity

**Parameters:**
- opacity (double) – Intensity of the live patch. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setVibrance((Patch)arg1, (float)vibrance[, (Anim)animator]) -> None`

Setter for property vibrance

**Parameters:**
- vibrance (double) – Vibrance value used in coordination with HSV value.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property filename`

Texture to apply on the live patch.

### property: `property gamma`

Gamma correction for the patch.

### property: `property hsv`

Hue, Saturation and Lightness value used for the patch.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property keyColor`

Color to remove from patch texture (RGB + tolerance).

### property: `property name`

Returns the name.

### property: `property opacity`

Intensity of the live patch. Usually in range [0;1]

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property vibrance`

Vibrance value used in coordination with HSV value.

---

# skyExplorer.Place2D

## class skyExplorer.Place2D

### class CSMode

Coordinate System Mode

InvalidCSMode

DefaultCSMode

Spherical

Planetocentric

Planetographic

### class CardinalPointRepresentation

InvalidCardinalPointRepresentation

Level1

Level2

Level3

### class Place2DName

InvalidPlace2D

Place2D001

Place2D002

Place2D003

Place2D004

Place2D005

Place2D006

Place2D007

Place2D008

Place2D009

Place2D010

Place2D011

Place2D012

Place2D013

Place2D014

Place2D015

Place2D016

Place2D017

Place2D018

Place2D019

Place2D020

Place2D021

Place2D022

Place2D023

Place2D024

Place2D025

Place2D026

Place2D027

Place2D028

Place2D029

Place2D030

Place2D031

Place2D032

Place2D033

Place2D034

Place2D035

Place2D036

Place2D037

Place2D038

Place2D039

Place2D040

Place2D041

Place2D042

Place2D043

Place2D044

Place2D045

Place2D046

Place2D047

Place2D048

Place2D049

Place2D050

Place2DCount

### class Place2DPort

InvalidPlace2DPort

CenteredPort

### `addChild((Place2D)arg1, (int)child, (Place2D.Place2DPort)port) -> None`

Add a child object to the place2D scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (Place2DPort) – Coordinate system to use for adding child. See Place2DPort documentation for more information.

### `portId((Place2D)arg1, (Place2D.Place2DPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (Place2DPort) – Name of the port. See ‘Place2DPort’ documentation for more information.

### `remove((Place2D)arg1) -> None`

Remove the place2D from the scene graph.

### `setAltitude((Place2D)arg1, (float)altitude[, (Anim)animator]) -> None`

Setter for property altitude

**Parameters:**
- altitude (double) – Altitude of the place2D relative to it’s parent. Same value as position(2).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAzimuthGridIntensity((Place2D)arg1, (float)azimuthGridIntensity[, (Anim)animator]) -> None`

Setter for property azimuthGridIntensity

**Parameters:**
- azimuthGridIntensity (double) – Intensity of the meridian marks.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAzimuthIntensity((Place2D)arg1, (float)azimuthIntensity[, (Anim)animator]) -> None`

Setter for property azimuthIntensity

**Parameters:**
- azimuthIntensity (double) – Intensity of the meridian marks.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCardinalPointsIntensity((Place2D)arg1, (float)cardinalPointsIntensity[, (Anim)animator]) -> None`

Setter for property cardinalPointsIntensity

**Parameters:**
- cardinalPointsIntensity (double) – Intensity of the cardinal points.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCardinalPointsRepresentation((Place2D)arg1, (Place2D.CardinalPointRepresentation)cardinalPointsRepresentation) -> None`

Setter for property cardinalPointsRepresentation

**Parameters:**
- cardinalPointsRepresentation (CardinalPointRepresentation) – Level used to display cardinal points (Level 1 will display four cardinal points, Level 2 eight…).

### `setCircumpolarIntensity((Place2D)arg1, (float)circumpolarIntensity[, (Anim)animator]) -> None`

Setter for property circumpolarIntensity

**Parameters:**
- circumpolarIntensity (double) – Intensity of the circumpolar marks.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCsMode((Place2D)arg1, (Place2D.CSMode)csMode) -> None`

Setter for property csMode

**Parameters:**
- csMode (CSMode) – Coordinate system mode for interpreting latitude and altitude of the place2D.

### `setHourAngleGridIntensity((Place2D)arg1, (float)hourAngleGridIntensity[, (Anim)animator]) -> None`

Setter for property hourAngleGridIntensity

**Parameters:**
- hourAngleGridIntensity (double) – Intensity of the hour angle mark grid.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHourAngleLineIntensity((Place2D)arg1, (float)hourAngleLineIntensity[, (Anim)animator]) -> None`

Setter for property hourAngleLineIntensity

**Parameters:**
- hourAngleLineIntensity (double) – Intensity of the hour angle mark line.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHourAngleMeridianIntensity((Place2D)arg1, (float)hourAngleMeridianIntensity[, (Anim)animator]) -> None`

Setter for property hourAngleMeridianIntensity

**Parameters:**
- hourAngleMeridianIntensity (double) – Intensity of the hour angle mark meridian.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLatitude((Place2D)arg1, (float)latitude[, (Anim)animator]) -> None`

Setter for property latitude

**Parameters:**
- latitude (double) – Latitude of the place2D relative to it’s parent. Same value as position(0).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLongitude((Place2D)arg1, (float)longitude[, (Anim)animator]) -> None`

Setter for property longitude

**Parameters:**
- longitude (double) – Longitude of the place2D relative to it’s parent. Same value as position(1).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMeridianIntensity((Place2D)arg1, (float)meridianIntensity[, (Anim)animator]) -> None`

Setter for property meridianIntensity

**Parameters:**
- meridianIntensity (double) – Intensity of the meridian marks.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setParent((Place2D)arg1, (int)parent[, (Anim)animator]) -> None`

Setter for property parent

**Parameters:**
- parent (int) – Parent database Id+Port.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPosition((Place2D)arg1, (Vec3)position[, (Anim)animator]) -> None`

Setter for property position

**Parameters:**
- position (Vec3) – Position of the place2D relative to it’s parent.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPositionFromGeocentric((Place2D)arg1, (Vec3)geocentricPos, (Anim)anim) -> None`

Position the Place2D on the surface of current ellipsoid, with coordinates in current mode matching input spherical coordinates.

**Parameters:**
- geocentricPos (Vec3) – Spherical position (x=latitude, y=longitude, z=altitude). z is currently ignored.
- anim (Anim, optional) – defaults to Anim()

### `setZenithIntensity((Place2D)arg1, (float)zenithIntensity[, (Anim)animator]) -> None`

Setter for property zenithIntensity

**Parameters:**
- zenithIntensity (double) – Intensity of the zenith/nadir.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `switchCSMode((Place2D)arg1, (Place2D.CSMode)targetMode) -> None`

Change the mode of the Place2D without changing its XYZ position.

**Parameters:**
- targetMode (CSMode) – Destination coordinate system mode.

### `switchParent((Place2D)arg1, (int)parent) -> None`

**Parameters:**
- parent (int)

### `toGround((Place2D)arg1, (Anim)anim) -> None`

Put the place2D at the surface of it’s parent body.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### property: `property altitude`

Altitude of the place2D relative to it’s parent. Same value as position(2).

### property: `property azimuthGridIntensity`

Intensity of the meridian marks.

### property: `property azimuthIntensity`

Intensity of the meridian marks.

### property: `property cardinalPointsIntensity`

Intensity of the cardinal points.

### property: `property cardinalPointsRepresentation`

Level used to display cardinal points (Level 1 will display four cardinal points, Level 2 eight…).

### property: `property circumpolarIntensity`

Intensity of the circumpolar marks.

### property: `property csMode`

Coordinate system mode for interpreting latitude and altitude of the place2D.

### property: `property hourAngleGridIntensity`

Intensity of the hour angle mark grid.

### property: `property hourAngleLineIntensity`

Intensity of the hour angle mark line.

### property: `property hourAngleMeridianIntensity`

Intensity of the hour angle mark meridian.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property latitude`

Latitude of the place2D relative to it’s parent. Same value as position(0).

### property: `property longitude`

Longitude of the place2D relative to it’s parent. Same value as position(1).

### property: `property meridianIntensity`

Intensity of the meridian marks.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property parent`

Parent database Id+Port.

### property: `property parentFamily`

[Read-only]

Parent Family.

### property: `property parentIndex`

[Read-only]

Parent Index (in its family).

### property: `property position`

Position of the place2D relative to it’s parent.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property zenithIntensity`

Intensity of the zenith/nadir.

---

# skyExplorer.Place3D

## class skyExplorer.Place3D

### class DrawingMode

InvalidDrawingMode

Default

Deprecated_Dashes

Lines

Deprecated_Points

Trail

### class Place3DName

InvalidPlace3D

Place3D001

Place3D002

Place3D003

Place3D004

Place3D005

Place3D006

Place3D007

Place3D008

Place3D009

Place3D010

Place3D011

Place3D012

Place3D013

Place3D014

Place3D015

Place3D016

Place3D017

Place3D018

Place3D019

Place3D020

Place3D021

Place3D022

Place3D023

Place3D024

Place3D025

Place3D026

Place3D027

Place3D028

Place3D029

Place3D030

Place3D031

Place3D032

Place3D033

Place3D034

Place3D035

Place3D036

Place3D037

Place3D038

Place3D039

Place3D040

Place3D041

Place3D042

Place3D043

Place3D044

Place3D045

Place3D046

Place3D047

Place3D048

Place3D049

Place3D050

Place3DCount

### class PlayMode

InvalidPlayMode

Simulation

Live

Play

ConstantSpeed

### `load((Place3D)arg1, (object)file) -> None`

Load Path.

**Parameters:**
- file (str) – TSV File

### `setEvolution((Place3D)arg1, (float)evolution[, (Anim)animator]) -> None`

Setter for property evolution

**Parameters:**
- evolution (double) – Path evolution (with Live play mode). Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Place3D)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Global intensity (path, position keys, orientation keys). Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLineColor((Place3D)arg1, (Vec3)lineColor[, (Anim)animator]) -> None`

Setter for property lineColor

**Parameters:**
- lineColor (Vec3) – Path Color. Values are (red, green, blue). Each value must be in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLineDrawingMode((Place3D)arg1, (Place3D.DrawingMode)lineDrawingMode) -> None`

Setter for property lineDrawingMode

**Parameters:**
- lineDrawingMode (DrawingMode) – Path drawing mode {Default, Line, Trail}.

### `setLineThickness((Place3D)arg1, (float)lineThickness[, (Anim)animator]) -> None`

Setter for property lineThickness

**Parameters:**
- lineThickness (double) – Path thickness (in pixels). Must be a positive number.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPlayMode((Place3D)arg1, (Place3D.PlayMode)playMode) -> None`

Setter for property playMode

**Parameters:**
- playMode (PlayMode) – Path play mode {Simulation, Live, Play, ConstantSpeed}.

### `setShowPath((Place3D)arg1, (bool)showPath) -> None`

Setter for property showPath

**Parameters:**
- showPath (bool) – Show/Hide path. {True, False}.

### property: `property evolution`

Path evolution (with Live play mode). Usually in range [0;1].

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Global intensity (path, position keys, orientation keys). Usually in range [0;1].

### property: `property lineColor`

Path Color. Values are (red, green, blue). Each value must be in range [0;1].

### property: `property lineDrawingMode`

Path drawing mode {Default, Line, Trail}.

### property: `property lineThickness`

Path thickness (in pixels). Must be a positive number.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property playMode`

Path play mode {Simulation, Live, Play, ConstantSpeed}.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property showPath`

Show/Hide path. {True, False}.

---

# skyExplorer.Planet

## class skyExplorer.Planet

### class CloudModel

InvalidCloudModel

DefaultCloud

BasicCloud

SlicedCloud

DidSlicedCloud

RawCloud

CassiniJuno

Volumetric

VolumetricLowRes

### class EclipticGraduation

Type of graduation for ecliptic 2D infinite parallel.

InvalidEclipticGraduation

Angle

Month

### class PatchLayer

InvalidPatchLayer

Layer_01

Layer_02

### class PlanetName

InvalidPlanet

Mercury

Venus

Earth

Mars

Jupiter

Saturn

Uranus

Neptune

HD142_b

HD1237_b

HD1461_b

HD1502_b

HD1690_b

HD2039_b

HIP2247_b

HD2638_b

HD3651_b

HD4113_b

HD4208_b

HD4308_b

HD4203_b

HD4313_b

HD4732_b

HD4732_c

HD5319_b

HD5388_b

HD5891_b

HD6434_b

HIP5158_b

HD6718_b

HD7199_b

HD7449_b

HD7924_b

HD8535_b

HD8574_b

HD9446_b

HD9446_c

UpsilonAndromedae_d

UpsilonAndromedae_b

UpsilonAndromedae_c

WASP18_b

HD10180_b

HD10180_h

HD10180_g

HD10180_f

HD10180_e

HD10180_d

HD10180_c

HD10647_b

HD10697_b

HD11506_b

HD11977_b

HD11964_c

HD11964_b

HD12661_c

HD12661_b

AlphaAri_b

HD13189_b

GJ86_b

HD13931_b

WASP33_b

HD16141_b

_30AriB_b

HD16417_b

HD16175_b

_81Cet_b

HD16760_b

IotaHor_b

HIP12961_b

HD17156_b

HD18742_b

HIP14810_c

HIP14810_b

HIP14810_d

HD19994_b

_82GEridani_c

_82GEridani_b

_82GEridani_d

HD20782_b

HD20868_b

EpsilonEri_b

HD23127_b

HD23079_b

HD22781_b

HD23596_b

HD24040_b

HD25171_b

EpsilonRet_b

HD27894_b

HD28254_b

HD28185_b

EpsilonTau_b

HD28678_b

HD30177_b

GJ176_b

HD30562_b

HD30856_b

GJ179_b

HD31253_b

HD33142_b

HD33283_b

HD32518_b

HD33636_b

HD34445_b

HD33564_b

HD290327_b

HD38283_b

HD37124_b

HD37124_d

HD37124_c

HD39091_b

HD37605_c

HD37605_b

HD38529_b

HD38529_c

HD38801_b

HD40307_d

HD40307_b

HD40307_c

HD40979_b

HD43197_b

HD43691_b

HD44219_b

HD45364_b

HD45364_c

HD45350_b

HD45652_b

_6Lyn_b

HD46375_b

HD47186_c

HD47186_b

_7CMa_b

HD48265_b

HD49674_b

HD50499_b

HD50554_b

HD52265_b

HD60532_c

HD60532_b

HD63454_b

Pollux_b

HD63765_b

HD65216_b

HD66428_b

HD68988_b

HD69830_c

HD69830_d

HD69830_b

HD70642_b

HD72659_b

HD73267_b

HD73256_b

HD73526_c

HD73526_b

HD73534_b

_4UMa_b

HD74156_b

HD74156_c

HD75289_b

_55Cancri_c

_55Cancri_f

_55Cancri_b

_55Cancri_e

_55Cancri_d

HD75898_b

HD76700_b

HD79498_b

HD80606_b

HD81040_b

HD81688_b

HD82943_b

HD82943_c

HD82886_b

HD83443_b

HD85390_b

HD85512_b

HD86081_b

HD86264_b

BD082823_b

BD082823_c

HD87883_b

HD88133_b

HD89307_b

GammaLeoA_b

HD89744_b

_24Sex_b

_24Sex_c

HD90156_b

HD92788_b

HD93083_b

HD95089_b

UrsaeMajoris_c

UrsaeMajoris_b

HD96063_b

HD96167_b

HD96127_b

HD97658_b

HD98219_b

HD99109_b

HD99492_b

HD99706_b

HD100655_b

GJ433_b

HD100777_b

HIP57050_b

GJ436_b

HD101930_b

HIP57274_d

HIP57274_b

HIP57274_c

HD102117_b

HD102195_b

HD102272_b

HD102365_b

HD102329_b

HD102956_b

HD103197_b

HD104067_b

HD104985_b

HD106252_b

HD106270_b

HD107148_b

_11Com_b

HD108147_b

HD108863_b

HD108874_c

HD108874_b

HD109246_b

HD109749_b

HD111232_b

HD114386_b

HD114762_b

HD114783_b

HD114729_b

_61Virginis_d

_61Virginis_b

_61Virginis_c

HD116029_b

_70Vir_b

HD117207_b

HD117618_b

HD118203_b

TauBoo_b

HD121504_b

HD125612_c

HD125612_b

HD125595_b

HD126614A_b

HD128311_b

HD128311_c

AlphaCentauriB_b

HD130322_b

HD131496_b

HD132406_b

HD132563B_b

HD131664_b

HD134987_b

HD134987_c

_11UMi_b

HD136118_b

HD136418_b

Gliese581_d

Gliese581_b

Gliese581_c

Gliese581_e

IotaDra_b

HD139357_b

HD137388_b

HD330075_b

KappaCrB_b

HD141937_b

HD142245_b

EpsilonCrB_b

HD142415_b

RhoCrB_b

HD143361_b

HD145457_b

HD142022_b

_14Her_b

HD145377_b

HIP79431_b

HATP2_b

HD147018_b

HD147018_c

HD147513_b

HD148156_b

HD148427_b

HD149026_b

HD149143_b

HD152581_b

GJ649_b

HD154345_b

HD153950_b

HD155358_b

HD155358_c

HD154672_b

HD154857_b

HD156279_b

HD156668_b

HD156411_b

HD156846_b

HD158038_b

GJ674_b

GJ676A_b

HD159868_c

HD159868_b

MuArae_e

MuArae_b

MuArae_c

MuArae_d

HD162020_b

HD163607_c

HD163607_b

HD164509_b

HD164922_b

HD164604_b

HD167042_b

HD168443_b

HD168443_c

HD168746_b

_42Dra_b

HD169830_c

HD169830_b

HD170469_b

HD171238_b

HD173416_b

HD175541_b

HD175167_b

HD177830_b

HD178911B_b

Kepler21_b

HD179079_b

HD180314_b

HD179949_b

HD180902_b

HD181342_b

HD181720_b

HD181433_d

HD181433_c

HD181433_b

HD183263_c

HD183263_b

HD231701_b

HD185269_b

_16CygB_b

HD187123_b

HD187123_c

HD187085_b

HATP11_b

HD188015_b

XiAql_b

HD189733_b

HD190228_b

HD190360_c

HD190360_b

HD190647_b

HD192263_b

HD192310_c

HD192699_b

HD195019_b

HD196050_b

HD197037_b

HD196885_b

_18Del_b

HD200964_c

HD200964_b

BD144559_b

HD202206_b

HD202206_c

HD204313_b

HD204313_d

HD204941_b

GJ832_b

HD205739_b

HD206610_b

HD208527_b

HD208487_b

HD209458_b

HD210277_b

GJ849_b

HD210702_b

HD212771_b

HD212301_b

HD213240_b

HD215497_c

HD215497_b

Gliese876_e

Gliese876_d

Gliese876_b

Gliese876_c

TauGru_b

HD216437_b

HD216770_b

_51Peg_b

HD217107_b

HD217107_c

HD217786_b

HR8799_e

HD218566_b

HD219828_b

HD220074_b

HD220773_b

_14And_b

HD221287_b

HD222155_b

GammaCep_b

HD222582_b

HD224693_b

BetCnc_b

NGC4349127_b

BetUMi_b

HD24064_b

BD202457_b

BD202457_c

HD11755_b

NGC24233_b

M67SAND364_b

HD95127_b

HD240210_b

EtaCet_c

EtaCet_b

OmicronUMa_b

HD216536_b

OmegaSer_b

HD17092_b

BD48738_b

HD2952_b

MuLeo_b

_91Aqr_b

HD120084_b

OmicronCrB_b

_75Cet_b

_8UMi_b

HD12648_b

HIP105854_b

TYC14226141_b

TYC14226141_c

HIP67851_b

HD5608_b

HIP97233_b

HD33844_b

HD33844_c

HD155233_b

Kepler432_b

Kepler432_c

HD5319_c

HD1605_c

HD1605_b

Kepler815_b

Kepler1004_b

HD10442_b

Kepler1270_b

HD75784_b

Kepler435_b

Kepler278_b

Kepler278_c

Kepler637_b

Kepler1394_b

Kepler643_b

Kepler774_b

WASP71_b

Kepler433_b

HATP40_b

WASP78_b

WASP82_b

Kepler1274_b

Kepler1580_b

HD171028_b

Kepler40_b

WASP88_b

XO3_b

WASP73_b

Kepler541_b

Kepler1452_b

Kepler14_b

Kepler462_b

Kepler1434_b

Kepler959_b

Kepler516_b

WASP100_b

Kepler1298_b

Kepler911_b

Kepler522_b

HATP7_b

Kepler1158_b

Kepler1517_b

Kepler1171_b

Kepler1219_b

HD1666_b

HD114613_b

Kepler1518_b

Kepler50_c

Kepler50_b

WASP63_b

HD154857_c

Kepler1626_b

Fomalhaut_b

Kepler1137_b

HATP49_b

WASP54_b

KELT2A_b

Kepler33_b

Kepler33_d

Kepler33_e

Kepler1360_b

Kepler33_f

Kepler33_c

TrES4_b

Kepler644_b

Kepler1015_b

Kepler471_b

CoRoT26_b

Kepler1300_b

Kepler1375_b

Kepler1364_b

CoRoT28_b

Kepler1244_b

WASP99_b

PH1_b

Kepler1586_b

WASP48_b

WASP66_b

Kepler1326_b

Kepler880_b

Kepler338_d

Kepler338_c

Kepler338_b

KELT7_b

Kepler1502_b

Kepler1115_b

Kepler1051_b

Kepler1382_b

WASP72_b

Kepler812_b

KOI13_b

WASP68_b

HATP41_b

HD13908_b

HD13908_c

Kepler470_b

Kepler1543_b

Kepler1618_b

Kepler642_b

Kepler805_b

CoRoT19_b

WASP74_b

Kepler129_c

WASP79_b

Kepler129_b

Kepler849_b

HATP33_b

WASP12_b

Kepler36_b

Kepler36_c

Kepler1487_b

HATP39_b

Kepler448_b

CoRoT23_b

Kepler1121_b

HATP4_b

Kepler464_b

KELT6_b

HATP8_b

WASP13_b

Kepler1002_b

Kepler381_c

Kepler1239_b

Kepler381_b

HATP13_c

HATP13_b

CoRoT3_b

Kepler1345_b

Kepler853_b

Kepler997_b

HD67087_b

Kepler1112_b

Kepler493_b

Kepler44_b

WASP1_b

Kepler289_d

CoRoT17_b

Kepler1533_b

Kepler74_b

Kepler635_b

Kepler1000_b

HATS9_b

HATP57_b

Kepler910_b

HD113337_b

Kepler1622_b

Kepler627_b

Kepler100_c

Kepler8_b

Kepler4_b

Kepler12_b

KELT3_b

Kepler1238_b

WASP15_b

HATP14_b

Kepler483_b

Kepler117_b

Kepler117_c

Kepler791_b

HATP6_b

Kepler521_b

Kepler527_b

HR8799_d

HR8799_c

HR8799_b

Kepler1442_b

Kepler103_b

Kepler103_c

Kepler514_b

Kepler1383_b

WASP103_b

HATP35_b

HD103774_b

HATP56_b

Kepler1421_b

Kepler1640_b

Kepler1154_b

Kepler1340_b

Kepler758_d

Kepler758_b

Kepler1154_c

Kepler758_e

Kepler758_c

Kepler43_b

Kepler510_b

Kepler1515_b

Kepler79_e

Kepler79_d

Kepler1104_b

HATS3_b

Kepler1311_b

Kepler1483_b

Kepler1597_b

Kepler1571_b

HATP46_b

Kepler1569_b

Kepler1323_b

Kepler1311_c

Kepler930_b

WASP106_b

WASP20_b

Kepler39_b

Kepler907_b

Kepler794_b

Kepler915_b

Kepler434_b

Kepler1209_b

Kepler467_b

CoRoT11_b

Kepler1256_b

WASP94A_b

HATP31_b

Kepler1275_b

Kepler820_b

Kepler1602_b

Kepler1079_b

OGLETR56_b

Kepler1428_b

WASP61_b

Kepler127_d

Kepler127_b

Kepler127_c

Kepler126_b

Kepler126_d

Kepler126_c

Kepler410A_b

Kepler1163_b

Kepler650_b

Kepler136_c

Kepler136_b

Kepler104_c

Kepler885_b

Kepler104_d

Kepler427_b

WASP94B_b

WASP38_b

WASP26_b

Kepler480_b

Kepler1373_b

Kepler1100_b

Kepler473_b

Kepler1054_b

Kepler1616_b

Kepler1279_b

WASP24_b

HD11506_c

Kepler631_b

Kepler1435_b

OGLETR132_b

Kepler1527_b

Kepler1633_b

Kepler1072_b

Kepler1070_b

Kepler784_b

Kepler1280_b

Kepler596_b

Kepler507_b

HATP9_b

Kepler109_b

Kepler109_c

HATP45_b

HATP24_b

Kepler25_c

WASP3_b

Kepler25_b

WASP14_b

Kepler1488_b

Kepler1603_b

Kepler839_b

Kepler718_b

Kepler887_b

Kepler1370_c

Kepler1385_b

Kepler1336_b

Kepler798_b

Kepler887_c

Kepler512_b

Kepler1370_b

Kepler639_b

Kepler1288_b

Kepler1501_b

Kepler1336_c

Kepler1181_b

Kepler1511_b

Kepler1493_b

Kepler982_b

Kepler465_b

WASP101_b

Kepler412_b

Kepler135_b

Kepler1159_b

Kepler769_c

Kepler769_b

Kepler1592_b

Kepler1475_b

WASP62_b

Kepler1249_b

Kepler135_c

Kepler1285_b

Kepler1349_b

Kepler1293_b

Kepler1084_b

Kepler1510_b

Kepler628_b

Kepler1443_b

Kepler923_b

Kepler1609_b

Kepler1412_b

Kepler535_b

Kepler1496_b

Kepler854_b

Kepler1445_b

Kepler873_b

Kepler1531_b

Kepler703_b

Kepler1396_b

Kepler494_b

WASP75_b

WASP31_b

Kepler1283_b

Kepler1524_b

Kepler508_b

Kepler904_b

Kepler1589_b

Kepler1472_b

Kepler1233_b

Kepler889_b

Kepler68_d

Kepler68_c

Kepler68_b

WASP7_b

Kepler1620_b

Kepler750_c

Kepler1354_b

Kepler1581_b

Kepler1271_b

Kepler144_b

Kepler788_b

Kepler750_b

Kepler741_b

Kepler1422_b

HATP16_b

Kepler924_b

Kepler655_b

Kepler1621_b

Kepler1201_b

Kepler584_b

Kepler144_c

Kepler634_b

Kepler811_b

Kepler1169_b

Kepler1395_b

Kepler909_b

HATP29_b

Kepler937_c

Kepler814_b

Kepler502_b

Kepler972_b

Kepler937_b

Kepler606_b

Kepler1617_b

Kepler1551_b

Kepler1587_b

Kepler620_b

Kepler824_b

Kepler1508_b

Kepler1514_b

Kepler544_b

Kepler1224_b

HATP32_b

HATP30_b

WASP70A_b

Kepler1213_b

CoRoT14_b

Kepler1276_b

Kepler1248_b

Kepler1346_b

Kepler645_b

Kepler1193_b

Kepler1607_b

Kepler919_b

Kepler1094_b

HATP23_b

KIC11442793_c

KIC11442793_d

KIC11442793_e

Kepler509_b

KIC11442793_b

KIC11442793_f

KIC11442793_g

KIC11442793_h

WASP17_b

HATP34_b

Kepler653_c

Kepler1641_b

Kepler1632_b

Kepler1267_b

Kepler1433_b

Kepler1093_b

Kepler848_b

Kepler1641_c

Kepler669_b

Kepler1093_c

Kepler511_b

Kepler1568_b

Kepler1225_b

Kepler653_b

Kepler1056_b

CoRoT25_b

CoRoT16_b

Kepler506_b

CoRoT5_b

Kepler1547_b

Kepler624_b

Kepler998_b

Kepler132_e

Kepler132_c

Kepler132_b

Kepler1639_b

Kepler1398_c

Kepler132_d

Kepler1398_b

Kepler1165_b

WASP58_b

OGLETR10_b

WASP117_b

Kepler1289_b

Kepler1189_b

Kepler105_c

Kepler685_b

Kepler1278_b

Kepler1119_b

Kepler1113_b

Kepler1591_b

Kepler1557_b

Kepler1590_b

Kepler1106_b

Kepler1003_b

HATP5_b

Kepler1080_b

Kepler1199_b

Kepler886_b

Kepler1352_b

Kepler806_b

Kepler690_b

Kepler557_b

Kepler852_b

Kepler914_b

Kepler956_b

WASP47_d

Kepler766_b

Kepler633_b

Kepler1407_b

WASP47_b

Kepler1403_b

WTS1_b

Kepler1103_b

Kepler826_b

Kepler525_b

Kepler1212_b

Kepler590_b

Kepler965_b

WASP47_c

Kepler1269_b

Kepler1416_b

Kepler546_b

Kepler1111_b

Kepler526_b

WASP60_b

Kepler1085_b

OGLETR182_b

Kepler602_b

Kepler641_b

Kepler1063_b

Kepler1082_b

CoRoT22_b

Kepler1584_b

Kepler890_b

Kepler996_b

Kepler1344_b

Kepler1050_b

Kepler1147_b

Kepler1050_c

Kepler1432_b

Kepler529_b

Kepler874_b

Kepler529_c

Kepler757_b

Kepler610_c

Kepler610_b

Kepler918_b

Kepler609_b

Kepler1025_b

Kepler1180_b

Kepler871_b

HATP1_b

Pr201_b

Kepler420_b

Kepler1047_b

WASP95_b

WASP22_b

Kepler1047_c

Kepler130_d

Kepler130_b

Kepler1255_b

Kepler714_b

Kepler1031_b

Kepler1613_b

Kepler803_b

Kepler1486_b

Kepler792_b

Kepler1316_b

Kepler490_b

Kepler1406_b

Kepler1397_b

HD159243_c

Kepler197_b

Kepler1485_b

Kepler197_d

HD159243_b

Kepler908_b

Kepler197_c

Kepler197_e

CoRoT12_b

WASP56_b

CoRoT1_b

Kepler1535_b

Kepler619_b

Kepler912_b

Kepler79_c

Kepler1449_b

Kepler680_b

Kepler1401_b

Kepler1391_b

Kepler1253_b

Kepler497_b

Kepler748_b

Kepler1550_b

Kepler654_b

Kepler593_b

Kepler1057_b

Kepler835_b

Kepler830_b

Kepler1044_b

Kepler1561_b

Kepler79_b

Kepler772_b

Kepler875_b

Kepler619_c

HATS10_b

HATP21_b

HATP28_b

Kepler524_c

Kepler1218_b

Kepler524_b

HATP36_b

WASP28_b

Kepler488_b

Kepler796_b

Kepler978_b

Kepler1272_b

Kepler850_b

Kepler431_d

Kepler1187_b

Kepler1598_b

Kepler431_c

Kepler481_b

Kepler431_b

Kepler1436_b

Kepler476_b

Kepler1252_b

Kepler1268_b

Kepler485_b

Kepler881_b

WASP32_b

Kepler520_c

WASP35_b

Kepler1473_b

Kepler520_b

Kepler883_b

Kepler983_b

HATP15_b

Kepler1088_b

Kepler618_b

Kepler990_b

Kepler696_b

Kepler1230_b

Kepler540_b

Kepler754_b

Kepler762_b

Kepler822_b

Kepler1307_b

Kepler825_b

Kepler1368_b

Kepler474_b

CoRoT27_b

Kepler825_c

Kepler1594_b

Kepler1041_b

Kepler1260_b

Kepler872_b

Kepler990_c

Kepler1574_b

Kepler1217_b

Kepler1061_b

Kepler647_b

Kepler1424_b

Kepler545_b

Kepler454_c

Kepler454_b

Kepler1576_b

Kepler1405_b

Kepler513_b

Kepler1429_b

Kepler1601_b

Kepler860_b

Kepler1184_b

Kepler765_b

Kepler1005_b

Kepler1516_b

Kepler1141_b

Kepler840_b

Kepler1188_b

Kepler891_b

Kepler731_b

Kepler807_b

Kepler1207_b

Kepler1109_b

Kepler1478_b

Kepler1555_b

Kepler528_b

WASP55_b

WASP97_b

Kepler980_b

WASP21_b

WASP64_b

Kepler10_c

Kepler10_b

XO5_b

Kepler804_c

Kepler1182_b

Kepler722_c

Kepler1615_b

Kepler804_b

Kepler1444_b

Kepler1468_b

Kepler626_b

Kepler466_b

WASP83_b

Kepler1365_c

Kepler1468_c

Kepler666_b

WASP96_b

Kepler1338_b

Kepler722_b

Kepler466_c

Kepler771_b

Kepler17_b

Kepler1365_b

Kepler1562_b

Kepler1525_b

Kepler1046_b

HATP22_b

Kepler630_b

HATS1_b

Kepler106_e

Kepler1202_b

Kepler1431_b

Kepler855_b

Kepler1174_b

Kepler1495_b

Kepler1386_b

Kepler745_b

Kepler1474_b

Kepler715_b

Kepler1091_b

Kepler843_b

Kepler1538_b

Kepler810_b

Kepler759_b

Kepler836_b

Kepler106_b

Kepler555_b

Kepler817_b

Kepler1052_b

Kepler1204_b

Kepler1327_b

Kepler1348_b

Kepler897_b

Kepler501_b

Kepler1155_b

Kepler604_b

Kepler592_b

Kepler552_b

Kepler106_c

Kepler1528_b

Kepler1131_b

Kepler131_b

Kepler500_b

Kepler131_c

Kepler491_b

WASP5_b

CoRoT6_b

Kepler1417_b

Kepler223_b

Kepler789_b

Kepler1560_b

Kepler1637_b

Kepler223_e

Kepler1645_b

Kepler879_b

Kepler1226_b

Kepler929_b

Kepler1176_b

Kepler223_d

Kepler664_b

Kepler1636_b

Kepler1077_b

Kepler223_c

Kepler950_b

Kepler1466_b

Kepler870_b

Kepler1426_b

Kepler966_b

Kepler906_b

CoRoT20_b

Kepler780_b

Kepler96_b

Kepler573_b

XO2S_b

XO2S_c

M67YBP1194_b

Kepler782_b

CoRoT13_b

Kepler773_b

Kepler603_c

Kepler1129_b

Kepler581_b

Kepler1092_b

Kepler657_b

Kepler1427_b

Kepler154_b

Kepler603_b

Kepler1129_c

Kepler1016_b

Kepler1016_c

Kepler1623_b

Kepler154_f

Kepler864_b

Kepler1149_b

Kepler611_b

Kepler1303_b

Kepler588_b

Kepler154_c

Kepler608_b

Kepler1573_b

Kepler1619_b

Kepler1419_b

Kepler154_d

Kepler154_e

Kepler603_d

Kepler1068_b

Kepler1073_c

Kepler1462_b

Kepler1464_b

Kepler730_b

Kepler926_b

Kepler1231_b

Kepler1500_b

Kepler503_b

Kepler1629_b

Kepler1073_b

Kepler1441_b

Kepler1464_c

Kepler1457_b

TrES2_b

WASP37_b

Kepler1099_b

CoRoT18_b

HIP91258_b

Kepler1156_b

HD95872_b

Kepler1098_b

Kepler857_b

Kepler927_b

Kepler1328_b

Kepler1060_b

Kepler1369_b

Kepler1509_b

Kepler1220_b

Kepler1297_b

Kepler670_b

Kepler677_b

Kepler1451_b

Kepler952_b

Kepler713_b

Kepler1491_b

Kepler1183_b

Kepler1258_b

Kepler893_b

Kepler1563_b

Kepler1599_b

Kepler77_b

Kepler953_c

Kepler1542_b

Kepler953_b

Kepler537_b

Kepler1542_e

Kepler423_b

Kepler1542_c

Kepler1588_b

Kepler1542_d

WASP19_b

HD32963_b

Kepler517_b

Kepler986_b

Kepler534_b

Kepler648_b

Kepler556_b

Kepler1250_b

Kepler1264_b

Kepler719_b

Kepler1069_b

Kepler1479_b

Kepler1262_b

Kepler1286_b

Kepler809_b

Kepler1066_b

Kepler1216_b

Kepler1390_b

WASP49_b

Kepler616_c

XO2_b

Kepler831_b

Kepler616_b

Kepler1177_b

Kepler41_b

Kepler1438_b

Kepler708_b

Kepler1035_b

Kepler1142_b

Kepler1294_b

Kepler1399_b

Kepler1196_b

Kepler1548_b

Kepler1306_b

Kepler704_b

Kepler1523_b

Kepler199_c

Kepler1118_b

Kepler945_b

Kepler829_b

Kepler903_b

Kepler576_b

Kepler199_b

Kepler903_c

Kepler823_b

Kepler613_b

WASP104_b

Kepler1240_b

Kepler612_b

Kepler498_b

Kepler1513_b

Kepler1440_b

Kepler700_b

Kepler688_b

Kepler1476_b

Kepler579_b

Kepler1372_b

Kepler793_b

Kepler1305_b

Kepler1376_b

Kepler625_b

Kepler625_c

WASP135_b

Kepler795_b

Kepler1144_b

Kepler838_b

Kepler940_b

Kepler981_b

Kepler1040_b

HATP25_b

WASP77A_b

Kepler46_c

Kepler694_b

Kepler1631_b

Kepler565_b

Kepler597_b

Kepler539_b

Kepler575_b

HATP44_b

Kepler1572_b

Kepler1463_b

Kepler1556_b

Kepler1447_b

Kepler1497_b

Kepler869_b

Kepler1425_b

Kepler671_b

Kepler559_b

Kepler1227_b

Kepler683_b

Kepler863_b

Kepler797_b

Kepler1638_b

Kepler1127_b

WASP16_b

WASP8_b

WASP45_b

WASP36_b

Kepler1055_b

Kepler591_b

Kepler1625_b

Kepler767_b

Kepler1102_b

Kepler649_b

Kepler424_c

Kepler1287_b

Kepler1381_b

Kepler1494_b

Kepler884_b

Kepler1211_b

Kepler640_b

Kepler1458_b

CoRoT9_b

Kepler424_b

Kepler46_b

Kepler1546_b

Kepler1186_b

Kepler1125_b

XO1_b

Kepler1116_b

Kepler1065_b

Kepler1243_b

Kepler948_b

Kepler1067_b

Kepler1087_b

Kepler69_c

Kepler946_b

Kepler585_b

Kepler561_c

Kepler561_b

Kepler308_b

Kepler1135_b

Kepler308_c

Kepler1330_b

Kepler638_b

Kepler69_b

Kepler1612_b

Kepler1380_b

Kepler1065_c

Kepler1453_b

Kepler1611_b

HATS14_b

Kepler799_b

Kepler1215_b

Kepler1126_b

Kepler744_b

Kepler984_b

Kepler902_b

Kepler761_b

Kepler1339_b

Kepler1117_b

Kepler1343_b

Kepler1471_b

Kepler1522_b

Kepler1448_b

Kepler1506_b

Kepler569_b

Kepler746_b

Kepler728_b

WASP34_b

Kepler1290_b

Kepler1292_b

Kepler856_b

Kepler922_b

Kepler1567_b

Kepler813_b

WASP44_b

HATS4_b

HATP38_b

Kepler554_b

Kepler1596_b

Kepler93_b

Kepler1138_b

Kepler1312_b

Kepler1277_b

Kepler1411_b

Kepler1575_b

Kepler686_b

Kepler865_b

Kepler1033_b

Kepler770_d

Kepler426_b

Kepler586_b

Kepler1393_b

Kepler770_c

Kepler1078_b

Kepler818_b

Kepler1095_b

Kepler564_b

Kepler1484_b

Kepler770_b

Kepler672_b

Kepler1194_b

Kepler720_b

Kepler1333_b

WASP25_b

Kepler1210_b

WASP46_b

WASP4_b

GJ504_b

Kepler1583_b

Kepler867_b

Kepler582_b

Kepler1585_b

Kepler943_b

Kepler646_b

Kepler1101_b

Kepler1334_b

Kepler1325_b

Kepler729_b

Kepler574_b

Kepler492_b

Kepler1139_b

Kepler827_b

Kepler987_b

Kepler678_b

Kepler461_b

Kepler1273_b

Kepler583_b

Kepler710_b

Kepler1519_b

Kepler1012_b

Kepler1128_b

Kepler921_b

Kepler1299_b

Kepler846_b

Kepler858_b

Kepler698_b

Kepler899_b

Kepler548_b

CoRoT2_b

HD207832_b

Kepler63_b

HD207832_c

Kepler1437_b

Kepler1133_b

Kepler1332_b

Kepler739_b

Kepler1342_b

Kepler888_b

Kepler802_b

Kepler571_b

Kepler961_b

Kepler1198_b

CoRoT29_b

Kepler1489_b

Kepler463_b

Kepler1235_b

Kepler832_b

Kepler1357_b

Kepler1043_b

Kepler542_b

Kepler538_b

Kepler1123_b

Kepler562_b

Kepler1564_b

Kepler1237_b

Kepler570_b

HATS2_b

WASP39_b

Kepler1570_b

Kepler1023_b

Kepler723_b

Kepler1282_b

Kepler536_b

Kepler1634_b

Kepler1469_b

Kepler1036_b

Kepler936_b

Kepler1160_b

Kepler868_b

Kepler1295_b

Kepler530_b

Kepler1251_b

Kepler764_b

Kepler938_b

Kepler1122_b

Kepler783_b

Kepler1172_b

Kepler587_b

Kepler1232_b

Kepler682_b

HATS13_b

Kepler1018_b

Kepler75_b

Kepler652_b

Kepler1532_b

Kepler487_b

Kepler697_b

WASP89_b

Kepler1310_b

Kepler1011_b

Kepler1153_b

Kepler1001_b

Kepler605_c

HD77338_b

Kepler518_b

Kepler1643_b

Kepler689_b

Kepler1530_c

Kepler1530_b

Kepler605_b

Kepler487_c

HATP37_b

HATS5_b

WASP67_b

WASP41_b

Kepler594_b

Kepler947_b

Kepler1402_b

Kepler740_b

Kepler1610_b

Kepler1185_b

Kepler1017_b

Kepler1490_b

Kepler963_b

WASP41_c

Kepler882_b

Kepler1257_b

WASP6_b

CoRoT7_b

Kepler468_b

Kepler484_b

Kepler667_b

Kepler1322_b

Kepler1028_b

Kepler651_b

HATP27_b

Pr211_b

TrES5_b

Kepler439_b

M67YBP1514_b

Kepler1175_b

Kepler1644_b

Kepler425_b

Kepler684_b

Kepler941_b

Kepler1454_b

Kepler598_b

Kepler1578_b

Kepler1021_b

Kepler949_b

Kepler523_b

Kepler958_b

Kepler724_b

Kepler1534_b

Kepler623_b

Kepler1505_b

Kepler727_b

Kepler1606_b

Kepler733_b

Kepler962_b

Kepler692_b

Kepler1166_b

Kepler905_b

Kepler702_b

Kepler920_b

Kepler1507_b

Kepler760_c

Kepler851_b

Kepler816_b

Kepler894_b

Kepler743_b

Kepler717_b

Kepler19_b

Kepler1392_b

Kepler553_c

Kepler760_b

Kepler726_b

Kepler1313_b

Kepler920_c

Kepler971_b

Kepler939_b

Kepler1151_b

WASP42_b

Kepler985_b

Kepler1635_b

Kepler553_b

HD192310_b

WASP50_b

Kepler629_b

Kepler1162_b

Kepler775_b

Kepler955_b

Kepler1014_b

Kepler549_c

Kepler701_b

Kepler1108_b

Kepler862_b

Kepler1642_c

Kepler751_b

Kepler673_b

Kepler1482_b

Kepler679_b

Kepler632_b

Kepler964_b

Kepler1549_b

Kepler1415_b

WASP2_b

Kepler725_b

Kepler1627_b

Kepler1081_b

Kepler932_b

Kepler933_b

Kepler706_b

Kepler549_b

Kepler1642_b

HATP17_b

WASP57_b

HATP3_b

OGLETR111_b

Kepler248_c

Kepler248_b

Kepler1281_b

Kepler1114_b

Kepler979_b

Kepler1038_b

Kepler515_b

Kepler589_b

Kepler499_b

Kepler1371_b

Kepler1245_c

Kepler752_b

Kepler1371_c

Kepler944_b

Kepler1245_b

Kepler977_b

Kepler1132_b

Kepler1296_b

Kepler1192_b

Kepler578_b

Kepler1355_b

Kepler550_b

Kepler495_b

Kepler595_b

Kepler976_b

Qatar1_b

Kepler969_b

Kepler969_c

Kepler1467_b

Kepler1600_b

Kepler663_b

Kepler1168_b

Kepler668_b

Kepler1377_b

Kepler1236_b

Kepler1090_b

Kepler1221_b

Kepler1302_b

Kepler1173_b

HATP19_b

Kepler496_b

Kepler1107_b

Kepler1027_b

Kepler656_b

Kepler1559_b

Kepler800_b

Kepler738_b

Kepler1605_b

Kepler1010_b

Kepler1045_b

Kepler1247_b

WASP69_b

TrES3_b

Kepler1130_b

Kepler1304_b

Kepler819_b

Kepler1134_b

Kepler614_b

Kepler1554_b

Kepler1205_b

Kepler600_b

Kepler1566_b

Kepler931_b

Kepler479_b

Kepler1498_b

Kepler1301_b

Kepler1071_b

Kepler896_b

Kepler841_b

Kepler1504_b

Kepler1553_b

Kepler837_b

Kepler736_b

Kepler558_b

Kepler1480_b

Kepler1191_b

Kepler1374_b

Kepler1541_b

Kepler916_b

Kepler1179_b

Kepler877_b

WASP29_b

TrES1_b

Kepler519_b

Kepler607_b

Kepler1214_b

Kepler995_b

Kepler735_b

Kepler1404_b

Kepler636_b

Kepler821_b

Kepler967_c

Kepler1545_b

Kepler711_b

Kepler1595_b

Kepler1020_b

Kepler1413_b

Kepler1241_b

Kepler1263_b

Kepler1309_b

Kepler790_b

Kepler695_b

Kepler1291_b

Kepler1034_b

Kepler428_b

Kepler1539_b

Kepler478_b

Kepler1222_b

Kepler763_b

Kepler967_b

Kepler1317_b

WASP52_b

Kepler566_b

Kepler411_c

Kepler1347_b

Kepler1064_b

Kepler1097_b

Kepler532_b

Kepler1358_b

Kepler572_b

Kepler1164_b

Kepler1558_b

CoRoT10_b

Kepler1379_b

Kepler1409_b

Kepler477_b

Kepler756_b

Kepler599_b

Kepler475_b

Kepler1420_b

HD108341_b

Kepler601_b

Kepler1361_b

Kepler567_b

Kepler1284_b

HATP26_b

HD7924_d

HD7924_c

Kepler712_b

Kepler1477_b

Kepler721_b

Kepler699_b

Kepler781_b

Kepler768_b

Kepler989_b

Kepler1024_b

Kepler712_c

Kepler1400_b

Kepler747_b

Kepler734_b

Kepler1037_b

Kepler1552_b

Kepler1008_b

Kepler776_b

Kepler1356_b

Kepler716_b

Kepler973_b

Kepler861_b

Kepler1499_b

Kepler472_b

OGLETR113_b

Kepler1529_b

Kepler1261_b

CoRoT8_b

Kepler1259_b

Kepler1537_b

Kepler1029_b

Kepler778_b

Kepler563_b

Kepler1143_b

Kepler1143_c

Kepler755_c

Kepler1593_b

Kepler878_b

Kepler755_b

Kepler1083_b

Kepler37_b

Kepler934_b

Kepler37_c

Kepler859_b

Kepler828_b

Kepler876_b

Kepler847_b

Kepler1148_b

Kepler37_d

Kepler709_b

Kepler1387_b

WASP23_b

Kepler1521_b

Kepler954_b

Kepler1013_b

Kepler1266_b

Kepler917_b

Kepler1604_b

Kepler1030_b

WTS2_b

Kepler1208_b

Kepler1170_b

Kepler681_b

Kepler489_b

Kepler707_b

Kepler1614_b

Kepler1470_b

Kepler1234_b

Kepler421_b

Kepler444_f

Kepler444_e

Kepler444_d

Kepler444_c

Kepler444_b

Kepler1254_c

Kepler531_b

Kepler1254_b

Kepler1167_b

Kepler1026_b

Kepler675_b

Kepler749_b

Kepler1423_b

Kepler957_b

Kepler1481_b

Kepler845_b

Kepler1254_d

Kepler1315_b

Kepler1206_b

Kepler975_b

Kepler1145_b

Kepler942_b

Kepler1223_b

Kepler1414_b

Kepler486_b

Kepler1178_b

Kepler1446_b

HATP18_b

WASP84_b

BD103166_b

Kepler102_b

Kepler1228_b

Kepler1362_b

Kepler1320_b

Kepler1384_b

Kepler659_b

Kepler1335_b

Kepler78_b

Kepler102_e

Kepler102_f

Kepler1120_b

Kepler102_d

Kepler662_b

Kepler1242_b

Kepler1039_b

WASP11_b

Kepler1544_b

Kepler1577_b

Kepler1459_b

Kepler1389_b

Kepler665_b

Kepler1076_b

Kepler992_b

Kepler1461_b

Kepler1503_b

Kepler1006_b

Kepler786_b

Kepler1324_b

Kepler1565_b

Kepler1140_b

Kepler842_b

Kepler547_b

Kepler951_b

Kepler935_b

Kepler577_b

Kepler900_b

Kepler687_b

Kepler167_c

Kepler167_b

Kepler1059_b

Kepler1430_b

Kepler693_b

Kepler482_b

Kepler1150_b

Kepler1363_b

Kepler892_b

Kepler1353_b

Kepler533_b

Kepler960_b

Kepler1608_b

Kepler925_b

Kepler1418_b

Kepler1190_b

Kepler1492_b

Kepler1341_b

Kepler1359_b

Kepler1042_b

Kepler1197_b

HIP116454_b

Qatar2_b

Kepler1465_b

Kepler660_b

Kepler1032_b

Kepler866_b

Kepler742_b

Kepler1520_b

Kepler1195_b

Kepler808_b

Kepler785_b

Kepler1157_b

Kepler443_b

HATP12_b

WASP98_b

Kepler1007_b

Kepler436_c

Kepler1146_b

Kepler1110_b

Kepler968_c

Kepler968_b

Kepler928_b

Kepler1318_b

Kepler1048_b

Kepler1200_b

Kepler1579_b

Kepler1062_b

WASP10_b

Kepler436_b

HATP20_b

Kepler1329_b

Kepler1540_b

Kepler1526_b

Kepler1246_b

Kepler1058_b

Kepler1053_b

Kepler1265_b

Kepler1331_b

Kepler615_b

Kepler621_b

Kepler1105_b

Kepler437_b

Kepler1136_b

Kepler1450_b

Kepler1022_b

Kepler1460_b

Kepler543_b

Kepler1536_b

Kepler1351_b

Kepler1337_b

Kepler1378_b

Kepler1019_b

Kepler661_b

Kepler970_b

Kepler1512_b

Kepler1086_b

Kepler834_b

Kepler1086_c

HD285507_b

Kepler753_b

Kepler62_f

Kepler580_b

Kepler62_c

Kepler62_e

Kepler62_d

Kepler62_b

Kepler801_b

Kepler551_b

Kepler1630_b

Kepler1096_b

Kepler898_b

Kepler833_b

Kepler61_b

Kepler1456_b

Kepler787_b

HATP54_b

WASP59_b

Kepler913_b

Kepler622_b

Kepler1388_c

Kepler991_b

Kepler1388_d

Kepler1203_b

Kepler1388_e

Kepler1388_b

Kepler895_b

Kepler1455_b

K221_c

Kepler1366_b

Kepler1367_b

Kepler658_b

Kepler1410_b

K221_b

Kepler442_b

WASP43_b

Kepler1314_b

WASP80_b

HATS6_b

K222_b

Kepler844_b

Kepler1161_b

Kepler901_b

Kepler1074_b

Kepler1009_b

Kepler674_b

K23_d

K23_c

K23_b

Kepler777_b

Kepler440_b

Kepler441_b

Kepler45_b

Kepler994_b

Kepler1075_b

Kepler1319_b

Kepler993_b

Kepler32_b

Kepler32_c

Kepler505_b

Kepler568_b

Kepler1152_b

Kepler32_e

Kepler1350_c

Kepler988_b

Kepler32_d

Kepler1321_b

Kepler1321_c

Kepler1350_b

Kepler32_f

Kepler438_b

Kepler1628_b

Kepler1229_b

Kepler705_b

KOI4427_b

GJ3470_b

Kepler691_b

Kepler974_b

Kepler676_b

Kepler1089_b

Kepler1049_b

Kepler617_b

Kepler737_b

Kepler186_e

Kepler186_b

Kepler186_f

Kepler186_d

Kepler186_c

Kepler1624_b

Kepler732_b

Kepler732_c

Kepler779_b

GJ3341_b

GJ3634_b

Kepler1439_b

GJ687_b

GJ3293_c

GJ3293_b

GJ15A_b

Kepler1308_b

Kepler1124_b

Kepler504_b

Kepler560_b

Kepler1582_b

K225_b

Kepler1646_b

Kepler446_c

Kepler446_b

Kepler446_d

GJ1214_b

Kepler445_b

Kepler445_d

Kepler445_c

Kepler42_d

Kepler42_b

Kepler42_c

Kepler1408_b

GJ317_b

XO4_b

GJ163_d

BetaPic_b

GJ832_c

GJ163_b

HD95086_b

_51Eri_b

OGLE05169L_b

GJ163_c

GJ328_b

Kepler16_b

Gliese667C_c

Gliese667C_b

Kepler11_b

Kepler11_c

Kepler11_d

Kepler11_e

Kepler11_f

Kepler11_g

Kepler20_b

Kepler20_c

Kepler20_d

Kepler20_e

Kepler20_f

Kepler22_b

Trappist1_b

Trappist1_c

Trappist1_d

Trappist1_e

Trappist1_f

Trappist1_g

Trappist1_h

AlphaCentauriC_b

PlanetCount

### class PlanetPort

InvalidPlanetPort

Ecliptic

Equatorial

EquatorialSynchronous

Galactic

OrbitalMeanEquinox

EquatorialJ2000

NoonEcliptic

NoonEquatorial

### class RingModel

InvalidRingModel

DefaultRing

BasicRing

Asteroids

Asteroids_3_0

### class ShadowConeArea

InvalidShadowConeArea

UmbraBefore

UmbraAfter

PenumbraBefore

PenumbraAfter

Antumbra

### class ShadowConeLineDrawingMode

InvalidShadowConeLineDrawingMode

Default

DotsLine

Line

Dots

Trail

### class ShadowConeRepresentation

InvalidShadowConeRepresentation

COLOR_2D

COLOR_3D

OCCULTATION_2D

### class TerrainModel

InvalidTerrainModel

DefaultTerrain

BasicTerrain

BMNG_Ocean

BMNG_Seasons

BMNG_Summer

BMNG_Winter

DidSliced

Geoid

Magellan

MagellanBW

Messenger

MOC

PlanetObserver

PlanetObserverDEM30

Sliced

Themis

Topography

Viking

CTX

CTXColorized

### `addChild((Planet)arg1, (int)child, (Planet.PlanetPort)port) -> None`

Add a child object to the planet’s scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (PlanetPort) – Coordinate system to use for adding child. See ‘PlanetPort’ documentation for more information.

### `assignLut((Planet)arg1, (int)lutId, (Anim)anim) -> None`

**Parameters:**
- lutId (int)
- anim (Anim, optional) – defaults to Anim()

### `distanceFromGroundAt((Planet)arg1, (Vec3)lbr, (int)port) -> float`

Return current elevation under the given point (in meter)

**Parameters:**
- lbr (Vec3)
- port (int)

### `patchLayerAdd((Planet)arg1, (Planet.PatchLayer)layerId, (int)patchId, (Anim)anim) -> None`

Add a layer to planet patch

**Parameters:**
- layerId (PatchLayer)
- patchId (int)
- anim (Anim, optional) – defaults to Anim()

### `patchLayerClear((Planet)arg1, (Planet.PatchLayer)layerId, (Anim)anim) -> None`

Remove all patch layer from planet

**Parameters:**
- layerId (PatchLayer)
- anim (Anim, optional) – defaults to Anim()

### `portId((Planet)arg1, (Planet.PlanetPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (PlanetPort) – Name of the port. See ‘PlanetPort’ documentation for more information.

### `resetRevolutionSpeedScale((Planet)arg1) -> None`

Restore default planet’s revolution speed factor.

### `resetRotationSpeedScale((Planet)arg1) -> None`

Restore default planet’s rotation speed factor.

### `setAntumbraAreaColor((Planet)arg1, (Vec3)antumbraAreaColor[, (Anim)animator]) -> None`

Setter for property antumbraAreaColor

**Parameters:**
- antumbraAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAntumbraAreaIntensity((Planet)arg1, (float)antumbraAreaIntensity[, (Anim)animator]) -> None`

Setter for property antumbraAreaIntensity

**Parameters:**
- antumbraAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAntumbraLineIntensity((Planet)arg1, (float)antumbraLineIntensity[, (Anim)animator]) -> None`

Setter for property antumbraLineIntensity

**Parameters:**
- antumbraLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAtmosphereHaloIntensity((Planet)arg1, (float)atmosphereHaloIntensity[, (Anim)animator]) -> None`

Setter for property atmosphereHaloIntensity

**Parameters:**
- atmosphereHaloIntensity (double) – Intensity of star and satellite halos observed through the Atmosphere. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAtmosphereIntensity((Planet)arg1, (float)atmosphereIntensity[, (Anim)animator]) -> None`

Setter for property atmosphereIntensity

**Parameters:**
- atmosphereIntensity (double) – Intensity of the planet’s atmosphere if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAtmosphericRefractionFactor((Planet)arg1, (float)atmosphericRefractionFactor[, (Anim)animator]) -> None`

Setter for property atmosphericRefractionFactor

**Parameters:**
- atmosphericRefractionFactor (double) – Earth only, atmospheric refraction factor, 0 -> no refraction, 1 -> normal refraction (goes up to 5), only works when atmosphere and planet is on
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAuroraIntensity((Planet)arg1, (float)auroraIntensity[, (Anim)animator]) -> None`

Setter for property auroraIntensity

**Parameters:**
- auroraIntensity (double) – Intensity of the planet’s auroras if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudAltitude((Planet)arg1, (float)cloudAltitude[, (Anim)animator]) -> None`

Setter for property cloudAltitude

**Parameters:**
- cloudAltitude (double) – Altitude of the clouds.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudCoverage((Planet)arg1, (float)cloudCoverage[, (Anim)animator]) -> None`

Setter for property cloudCoverage

**Parameters:**
- cloudCoverage (double) – Percentage of the cloud coverage of the planet’s clouds (only applicable to the Earth). In range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudDirection((Planet)arg1, (float)cloudDirection) -> None`

Setter for property cloudDirection

**Parameters:**
- cloudDirection (double) – Direction of clouds movement. Warning: Must be used during initialization when clouds are OFF.

### `setCloudLightPollution((Planet)arg1, (float)cloudLightPollution[, (Anim)animator]) -> None`

Setter for property cloudLightPollution

**Parameters:**
- cloudLightPollution (double) – LightPollution of the clouds.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudModel((Planet)arg1, (Planet.CloudModel)cloudModel[, (Anim)animator]) -> None`

Setter for property cloudModel

**Parameters:**
- cloudModel (CloudModel)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudRaininess((Planet)arg1, (float)cloudRaininess[, (Anim)animator]) -> None`

Setter for property cloudRaininess

**Parameters:**
- cloudRaininess (double) – Percentage of the cloud raininess of the planet’s clouds (only applicable to the Earth). In range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudSpeed((Planet)arg1, (float)cloudSpeed) -> None`

Setter for property cloudSpeed

**Parameters:**
- cloudSpeed (double) – Speed factor of clouds (default : 1.0). Warning: Must be used during initialization when clouds are OFF.

### `setCloudThickness((Planet)arg1, (float)cloudThickness[, (Anim)animator]) -> None`

Setter for property cloudThickness

**Parameters:**
- cloudThickness (double) – Thickness of the clouds.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudsIntensity((Planet)arg1, (float)cloudsIntensity[, (Anim)animator]) -> None`

Setter for property cloudsIntensity

**Parameters:**
- cloudsIntensity (double) – Intensity of the planet’s clouds if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCollisionOffset((Planet)arg1, (float)collisionOffset[, (Anim)animator]) -> None`

Setter for property collisionOffset

**Parameters:**
- collisionOffset (double) – Minimun distance camera can approch to the planet surface in meters.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipseShapeIntensity((Planet)arg1, (float)eclipseShapeIntensity[, (Anim)animator]) -> None`

Setter for property eclipseShapeIntensity

**Parameters:**
- eclipseShapeIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticBandIntensity((Planet)arg1, (float)eclipticBandIntensity[, (Anim)animator]) -> None`

Setter for property eclipticBandIntensity

**Parameters:**
- eclipticBandIntensity (double) – Intensity of the planet’s ecliptic band (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticEquinoxesIntensity((Planet)arg1, (float)eclipticEquinoxesIntensity[, (Anim)animator]) -> None`

Setter for property eclipticEquinoxesIntensity

**Parameters:**
- eclipticEquinoxesIntensity (double) – Intensity of the planet’s ecliptic equinoxes (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticGraduationType((Planet)arg1, (Planet.EclipticGraduation)eclipticGraduationType) -> None`

Setter for property eclipticGraduationType

**Parameters:**
- eclipticGraduationType (EclipticGraduation)

### `setEclipticGridIntensity((Planet)arg1, (float)eclipticGridIntensity[, (Anim)animator]) -> None`

Setter for property eclipticGridIntensity

**Parameters:**
- eclipticGridIntensity (double) – Intensity of the planet’s ecliptic grid if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticMarkIntensity((Planet)arg1, (float)eclipticMarkIntensity[, (Anim)animator]) -> None`

Setter for property eclipticMarkIntensity

**Parameters:**
- eclipticMarkIntensity (double) – Intensity of the planet’s ecliptic mark if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticMeridianIntensity((Planet)arg1, (float)eclipticMeridianIntensity[, (Anim)animator]) -> None`

Setter for property eclipticMeridianIntensity

**Parameters:**
- eclipticMeridianIntensity (double) – Intensity of the planet’s ecliptic meridian (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticPoleAxisIntensity((Planet)arg1, (float)eclipticPoleAxisIntensity[, (Anim)animator]) -> None`

Setter for property eclipticPoleAxisIntensity

**Parameters:**
- eclipticPoleAxisIntensity (double) – Intensity of the planet’s ecliptic pole axis (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticPoleAxisScale((Planet)arg1, (float)eclipticPoleAxisScale[, (Anim)animator]) -> None`

Setter for property eclipticPoleAxisScale

**Parameters:**
- eclipticPoleAxisScale (double) – Scale of the planet’s ecliptic pole axis (if available).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipticPolePointerIntensity((Planet)arg1, (float)eclipticPolePointerIntensity[, (Anim)animator]) -> None`

Setter for property eclipticPolePointerIntensity

**Parameters:**
- eclipticPolePointerIntensity (double) – Intensity of the planet’s ecliptic Poles pointers if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setElevationScale((Planet)arg1, (float)elevationScale[, (Anim)animator]) -> None`

Setter for property elevationScale

**Parameters:**
- elevationScale (double) – Modify elevation scale of planet’s reliefs. In some modelsets of planets do not use this property.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialEquinoxesIntensity((Planet)arg1, (float)equatorialEquinoxesIntensity[, (Anim)animator]) -> None`

Setter for property equatorialEquinoxesIntensity

**Parameters:**
- equatorialEquinoxesIntensity (double) – Intensity of the planet’s equatorial equinoxes (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialGridIntensity((Planet)arg1, (float)equatorialGridIntensity[, (Anim)animator]) -> None`

Setter for property equatorialGridIntensity

**Parameters:**
- equatorialGridIntensity (double) – Intensity of the planet’s equatorial grid if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialJ2000EquinoxesIntensity((Planet)arg1, (float)equatorialJ2000EquinoxesIntensity[, (Anim)animator]) -> None`

Setter for property equatorialJ2000EquinoxesIntensity

**Parameters:**
- equatorialJ2000EquinoxesIntensity (double) – Intensity of the planet’s equatorial J2000 equinoxess (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialJ2000GridIntensity((Planet)arg1, (float)equatorialJ2000GridIntensity[, (Anim)animator]) -> None`

Setter for property equatorialJ2000GridIntensity

**Parameters:**
- equatorialJ2000GridIntensity (double) – Intensity of the planet’s equatorial J2000 grid (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialJ2000MeridianIntensity((Planet)arg1, (float)equatorialJ2000MeridianIntensity[, (Anim)animator]) -> None`

Setter for property equatorialJ2000MeridianIntensity

**Parameters:**
- equatorialJ2000MeridianIntensity (double) – Intensity of the planet’s equatorial J2000 prime meridian (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialJ2000PoleIntensity((Planet)arg1, (float)equatorialJ2000PoleIntensity[, (Anim)animator]) -> None`

Setter for property equatorialJ2000PoleIntensity

**Parameters:**
- equatorialJ2000PoleIntensity (double) – Intensity of the planet’s equatorial J2000 pole (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialMarkIntensity((Planet)arg1, (float)equatorialMarkIntensity[, (Anim)animator]) -> None`

Setter for property equatorialMarkIntensity

**Parameters:**
- equatorialMarkIntensity (double) – Intensity of the planet’s equatorial mark if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialMeridianIntensity((Planet)arg1, (float)equatorialMeridianIntensity[, (Anim)animator]) -> None`

Setter for property equatorialMeridianIntensity

**Parameters:**
- equatorialMeridianIntensity (double) – Intensity of the planet’s equatorial meridian (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialPoleAxisIntensity((Planet)arg1, (float)equatorialPoleAxisIntensity[, (Anim)animator]) -> None`

Setter for property equatorialPoleAxisIntensity

**Parameters:**
- equatorialPoleAxisIntensity (double) – Intensity of the planet’s equatorial pole axis (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialPoleAxisScale((Planet)arg1, (float)equatorialPoleAxisScale[, (Anim)animator]) -> None`

Setter for property equatorialPoleAxisScale

**Parameters:**
- equatorialPoleAxisScale (double) – Scale of the planet’s equatorial pole axis (if available).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialPolePointerIntensity((Planet)arg1, (float)equatorialPolePointerIntensity[, (Anim)animator]) -> None`

Setter for property equatorialPolePointerIntensity

**Parameters:**
- equatorialPolePointerIntensity (double) – Intensity of the planet’s equatorial Poles pointers if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncGraticuleIntensity((Planet)arg1, (float)equatorialSyncGraticuleIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncGraticuleIntensity

**Parameters:**
- equatorialSyncGraticuleIntensity (double) – Intensity of the planet’s equatorial synchronous graticule (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncMagneticPolesIntensity((Planet)arg1, (float)equatorialSyncMagneticPolesIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncMagneticPolesIntensity

**Parameters:**
- equatorialSyncMagneticPolesIntensity (double) – Intensity of the planet’s equatorial synchronous magnetic poles (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncMarkIntensity((Planet)arg1, (float)equatorialSyncMarkIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncMarkIntensity

**Parameters:**
- equatorialSyncMarkIntensity (double) – Intensity of the planet’s equatorial synchronous mark (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncMeridianIntensity((Planet)arg1, (float)equatorialSyncMeridianIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncMeridianIntensity

**Parameters:**
- equatorialSyncMeridianIntensity (double) – Intensity of the planet’s equatorial synchronous prime meridian (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncPolarCirclesIntensity((Planet)arg1, (float)equatorialSyncPolarCirclesIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncPolarCirclesIntensity

**Parameters:**
- equatorialSyncPolarCirclesIntensity (double) – Intensity of the planet’s equatorial synchronous polar circles (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEquatorialSyncTropicsIntensity((Planet)arg1, (float)equatorialSyncTropicsIntensity[, (Anim)animator]) -> None`

Setter for property equatorialSyncTropicsIntensity

**Parameters:**
- equatorialSyncTropicsIntensity (double) – Intensity of the planet’s equatorial synchronous tropics (if available). Range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFlatteningFactor((Planet)arg1, (float)flatteningFactor[, (Anim)animator]) -> None`

Setter for property flatteningFactor

**Parameters:**
- flatteningFactor (double) – Flattening factor.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHybridRatio((Planet)arg1, (float)hybridRatio[, (Anim)animator]) -> None`

Setter for property hybridRatio

**Parameters:**
- hybridRatio (double) – Used to define which device will display the planet. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Planet)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the planet. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelColor((Planet)arg1, (Vec3)labelColor[, (Anim)animator]) -> None`

Setter for property labelColor

**Parameters:**
- labelColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Planet)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the planet’s label. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLightPollutionIntensity((Planet)arg1, (float)lightPollutionIntensity[, (Anim)animator]) -> None`

Setter for property lightPollutionIntensity

**Parameters:**
- lightPollutionIntensity (double) – Intensity of the planet’s light pollution map if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchBottomLeft((Planet)arg1, (Vec3)livePatchBottomLeft[, (Anim)animator]) -> None`

Setter for property livePatchBottomLeft

**Parameters:**
- livePatchBottomLeft (Vec3) – South west LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchGamma((Planet)arg1, (Vec3)livePatchGamma[, (Anim)animator]) -> None`

Setter for property livePatchGamma

**Parameters:**
- livePatchGamma (Vec3) – Gamma correction for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchHsv((Planet)arg1, (Vec3)livePatchHsv[, (Anim)animator]) -> None`

Setter for property livePatchHsv

**Parameters:**
- livePatchHsv (Vec3) – Hue, Saturation and Lightness value used for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchIntensity((Planet)arg1, (float)livePatchIntensity[, (Anim)animator]) -> None`

Setter for property livePatchIntensity

**Parameters:**
- livePatchIntensity (double) – Intensity of the live patch. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchKeyColor((Planet)arg1, (Vec4)livePatchKeyColor[, (Anim)animator]) -> None`

Setter for property livePatchKeyColor

**Parameters:**
- livePatchKeyColor (Vec4) – Color to remove from patch texture (RGB + tolerance).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchRotation((Planet)arg1, (float)livePatchRotation[, (Anim)animator]) -> None`

Setter for property livePatchRotation

**Parameters:**
- livePatchRotation (double) – Rotation of the patch around center point in degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchTexture((Planet)arg1, (object)livePatchTexture) -> None`

Setter for property livePatchTexture

**Parameters:**
- livePatchTexture (str) – Texture to apply on the live patch.

### `setLivePatchTopRight((Planet)arg1, (Vec3)livePatchTopRight[, (Anim)animator]) -> None`

Setter for property livePatchTopRight

**Parameters:**
- livePatchTopRight (Vec3) – North east LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchVibrance((Planet)arg1, (float)livePatchVibrance[, (Anim)animator]) -> None`

Setter for property livePatchVibrance

**Parameters:**
- livePatchVibrance (double) – Vibrance value used in coordination with HSV value.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMagnetosphereIntensity((Planet)arg1, (float)magnetosphereIntensity[, (Anim)animator]) -> None`

Setter for property magnetosphereIntensity

**Parameters:**
- magnetosphereIntensity (double) – Intensity of the planet’s magnetosphere if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setNightLightsIntensity((Planet)arg1, (float)nightLightsIntensity[, (Anim)animator]) -> None`

Setter for property nightLightsIntensity

**Parameters:**
- nightLightsIntensity (double) – Intensity of the planet’s night lights if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((Planet)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double) – Intensity of the planet’s orbit. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPatchLayerGamma((Planet)arg1, (Planet.PatchLayer)layerId, (Vec3)gamma, (Anim)anim) -> None`

Gamma correction for the patc layerh.

**Parameters:**
- layerId (PatchLayer)
- gamma (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerHsv((Planet)arg1, (Planet.PatchLayer)layerId, (Vec3)hsv, (Anim)anim) -> None`

Hue, Saturation and Lightness value used for the patch layer.

**Parameters:**
- layerId (PatchLayer)
- hsv (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerKeyColor((Planet)arg1, (Planet.PatchLayer)layerId, (Vec4)keColor, (Anim)anim) -> None`

Color to remove from patch texture (RGB + tolerance).

**Parameters:**
- layerId (PatchLayer)
- keColor (Vec4)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerOpacity((Planet)arg1, (Planet.PatchLayer)layerId, (float)opacity, (Anim)anim) -> None`

Intensity of the patch layer. Usually in range [0;1]

**Parameters:**
- layerId (PatchLayer)
- opacity (double)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerVibrance((Planet)arg1, (Planet.PatchLayer)layerId, (float)vibrance, (Anim)anim) -> None`

Vibrance value used in coordination with HSV value of the patch layer.

**Parameters:**
- layerId (PatchLayer)
- vibrance (double)
- anim (Anim, optional) – defaults to Anim()

### `setPenumbraAfterAreaColor((Planet)arg1, (Vec3)penumbraAfterAreaColor[, (Anim)animator]) -> None`

Setter for property penumbraAfterAreaColor

**Parameters:**
- penumbraAfterAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraAfterAreaIntensity((Planet)arg1, (float)penumbraAfterAreaIntensity[, (Anim)animator]) -> None`

Setter for property penumbraAfterAreaIntensity

**Parameters:**
- penumbraAfterAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraAfterLineIntensity((Planet)arg1, (float)penumbraAfterLineIntensity[, (Anim)animator]) -> None`

Setter for property penumbraAfterLineIntensity

**Parameters:**
- penumbraAfterLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeAreaColor((Planet)arg1, (Vec3)penumbraBeforeAreaColor[, (Anim)animator]) -> None`

Setter for property penumbraBeforeAreaColor

**Parameters:**
- penumbraBeforeAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeAreaIntensity((Planet)arg1, (float)penumbraBeforeAreaIntensity[, (Anim)animator]) -> None`

Setter for property penumbraBeforeAreaIntensity

**Parameters:**
- penumbraBeforeAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeLineIntensity((Planet)arg1, (float)penumbraBeforeLineIntensity[, (Anim)animator]) -> None`

Setter for property penumbraBeforeLineIntensity

**Parameters:**
- penumbraBeforeLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPlanetShineStrength((Planet)arg1, (float)planetShineStrength[, (Anim)animator]) -> None`

Setter for property planetShineStrength

**Parameters:**
- planetShineStrength (double) – Intensity of the planet’s ecliptic polar circle if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointSaturation((Planet)arg1, (float)pointSaturation[, (Anim)animator]) -> None`

Setter for property pointSaturation

**Parameters:**
- pointSaturation (double) – Saturation of the planet when viewed as a point
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((Planet)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the planet’s pointer. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Planet)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current planet pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setPolarCircleIntensity((Planet)arg1, (float)polarCircleIntensity[, (Anim)animator]) -> None`

Setter for property polarCircleIntensity

**Parameters:**
- polarCircleIntensity (double) – Intensity of the planet’s ecliptic polar circle if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRainbowIntensity((Planet)arg1, (float)rainbowIntensity[, (Anim)animator]) -> None`

Setter for property rainbowIntensity

**Parameters:**
- rainbowIntensity (double) – Percentage of the rainbow intensity of the planet’s clouds (only applicable to the Earth). In range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRevolutionSpeedScale((Planet)arg1, (float)revolutionSpeedScale) -> None`

Setter for property revolutionSpeedScale

**Parameters:**
- revolutionSpeedScale (double) – Speed factor of the planet’s revolution.

### `setRingModel((Planet)arg1, (Planet.RingModel)ringModel[, (Anim)animator]) -> None`

Setter for property ringModel

**Parameters:**
- ringModel (RingModel)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRockyCliffIntensity((Planet)arg1, (float)rockyCliffIntensity[, (Anim)animator]) -> None`

Setter for property rockyCliffIntensity

**Parameters:**
- rockyCliffIntensity (double) – Rocky cliff intensity of the planet. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRotationSpeedScale((Planet)arg1, (float)rotationSpeedScale) -> None`

Setter for property rotationSpeedScale

**Parameters:**
- rotationSpeedScale (double) – Speed factor of the planet’s rotation.

### `setScale((Planet)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the planet. It can be used to enlarge apparent size of the planet.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setScatteringIntensity((Planet)arg1, (float)scatteringIntensity[, (Anim)animator]) -> None`

Setter for property scatteringIntensity

**Parameters:**
- scatteringIntensity (double) – Planet’s atmosphere scattering intensity. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSeaLevel((Planet)arg1, (float)seaLevel[, (Anim)animator]) -> None`

Setter for property seaLevel

**Parameters:**
- seaLevel (double) – Sea level level of the sea level in meter.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSeaLevelRenderingMode((Planet)arg1, (object)seaLevelRenderingMode[, (Anim)animator]) -> None`

Setter for property seaLevelRenderingMode

**Parameters:**
- seaLevelRenderingMode (str) – Sea level rendering mode use ‘NONE’ for off.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeAntumbraAdvancement((Planet)arg1, (float)shadowConeAntumbraAdvancement[, (Anim)animator]) -> None`

Setter for property shadowConeAntumbraAdvancement

**Parameters:**
- shadowConeAntumbraAdvancement (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeAreaColor((Planet)arg1, (Planet.ShadowConeArea)area, (Vec3)color, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- color (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeAreaIntensity((Planet)arg1, (Planet.ShadowConeArea)area, (float)intensity, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- intensity (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeIntensity((Planet)arg1, (float)shadowConeIntensity[, (Anim)animator]) -> None`

Setter for property shadowConeIntensity

**Parameters:**
- shadowConeIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeLineColor((Planet)arg1, (Planet.ShadowConeArea)area, (Vec3)intensity, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- intensity (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineDrawingMode((Planet)arg1, (Planet.ShadowConeArea)area, (Planet.ShadowConeLineDrawingMode)representation, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- representation (ShadowConeLineDrawingMode)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineIntensity((Planet)arg1, (Planet.ShadowConeArea)area, (float)color, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- color (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineThickness((Planet)arg1, (Planet.ShadowConeArea)area, (float)thickness, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- thickness (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConePenumbraAdvancement((Planet)arg1, (float)shadowConePenumbraAdvancement[, (Anim)animator]) -> None`

Setter for property shadowConePenumbraAdvancement

**Parameters:**
- shadowConePenumbraAdvancement (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeRepresentationType((Planet)arg1, (Planet.ShadowConeRepresentation)representation, (Anim)anim) -> None`

**Parameters:**
- representation (ShadowConeRepresentation)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeSectionDistance((Planet)arg1, (float)shadowConeSectionDistance[, (Anim)animator]) -> None`

Setter for property shadowConeSectionDistance

**Parameters:**
- shadowConeSectionDistance (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeSectionIntensity((Planet)arg1, (float)shadowConeSectionIntensity[, (Anim)animator]) -> None`

Setter for property shadowConeSectionIntensity

**Parameters:**
- shadowConeSectionIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowContrast((Planet)arg1, (float)shadowContrast[, (Anim)animator]) -> None`

Setter for property shadowContrast

**Parameters:**
- shadowContrast (double) – Contrast of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowStrength((Planet)arg1, (float)shadowStrength[, (Anim)animator]) -> None`

Setter for property shadowStrength

**Parameters:**
- shadowStrength (double) – Strength of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSupergalacticBandIntensity((Planet)arg1, (float)supergalacticBandIntensity[, (Anim)animator]) -> None`

Setter for property supergalacticBandIntensity

**Parameters:**
- supergalacticBandIntensity (double) – Intensity of the supergalactic mark band. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSupergalacticGridIntensity((Planet)arg1, (float)supergalacticGridIntensity[, (Anim)animator]) -> None`

Setter for property supergalacticGridIntensity

**Parameters:**
- supergalacticGridIntensity (double) – Intensity of the supergalactic mark grid. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSupergalacticMarkLineIntensity((Planet)arg1, (float)supergalacticMarkLineIntensity[, (Anim)animator]) -> None`

Setter for property supergalacticMarkLineIntensity

**Parameters:**
- supergalacticMarkLineIntensity (double) – Intensity of the supergalactic mark line. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainIntensity((Planet)arg1, (float)terrainIntensity[, (Anim)animator]) -> None`

Setter for property terrainIntensity

**Parameters:**
- terrainIntensity (double) – Intensity of the planet’s terrain if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainModel((Planet)arg1, (Planet.TerrainModel)terrainModel[, (Anim)animator]) -> None`

Setter for property terrainModel

**Parameters:**
- terrainModel (TerrainModel)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainRenderingMode((Planet)arg1, (object)terrainRenderingMode[, (Anim)animator]) -> None`

Setter for property terrainRenderingMode

**Parameters:**
- terrainRenderingMode (str) – Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTilesetDistanceMax((Planet)arg1, (float)tilesetDistanceMax[, (Anim)animator]) -> None`

Setter for property tilesetDistanceMax

**Parameters:**
- tilesetDistanceMax (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTilesetDistanceMin((Planet)arg1, (float)tilesetDistanceMin[, (Anim)animator]) -> None`

Setter for property tilesetDistanceMin

**Parameters:**
- tilesetDistanceMin (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTilesetIntensity((Planet)arg1, (float)tilesetIntensity[, (Anim)animator]) -> None`

Setter for property tilesetIntensity

**Parameters:**
- tilesetIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTilesetUrl((Planet)arg1, (object)tilesetUrl) -> None`

Setter for property tilesetUrl

**Parameters:**
- tilesetUrl (str) – 3D Tiles URL

### `setTopographicGradientTextureFilename((Planet)arg1, (object)topographicGradientTextureFilename) -> None`

Setter for property topographicGradientTextureFilename

**Parameters:**
- topographicGradientTextureFilename (str) – Texture to use to color planet in topographic mode.

### `setTrajectoryIntensity((Planet)arg1, (float)trajectoryIntensity[, (Anim)animator]) -> None`

Setter for property trajectoryIntensity

**Parameters:**
- trajectoryIntensity (double) – Intensity of the planet’s trajectory. Usually in range [0;1] if set to positive value, planet will draw a line according to it’s movement on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTreeDensity((Planet)arg1, (float)treeDensity[, (Anim)animator]) -> None`

Setter for property treeDensity

**Parameters:**
- treeDensity (double) – Tree density.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTreeIntensity((Planet)arg1, (float)treeIntensity[, (Anim)animator]) -> None`

Setter for property treeIntensity

**Parameters:**
- treeIntensity (double) – Tree intensity.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTreeMaxDistance((Planet)arg1, (float)treeMaxDistance[, (Anim)animator]) -> None`

Setter for property treeMaxDistance

**Parameters:**
- treeMaxDistance (double) – Tree fade out distance.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterAreaColor((Planet)arg1, (Vec3)umbraAfterAreaColor[, (Anim)animator]) -> None`

Setter for property umbraAfterAreaColor

**Parameters:**
- umbraAfterAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterAreaIntensity((Planet)arg1, (float)umbraAfterAreaIntensity[, (Anim)animator]) -> None`

Setter for property umbraAfterAreaIntensity

**Parameters:**
- umbraAfterAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterLineIntensity((Planet)arg1, (float)umbraAfterLineIntensity[, (Anim)animator]) -> None`

Setter for property umbraAfterLineIntensity

**Parameters:**
- umbraAfterLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeAreaColor((Planet)arg1, (Vec3)umbraBeforeAreaColor[, (Anim)animator]) -> None`

Setter for property umbraBeforeAreaColor

**Parameters:**
- umbraBeforeAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeAreaIntensity((Planet)arg1, (float)umbraBeforeAreaIntensity[, (Anim)animator]) -> None`

Setter for property umbraBeforeAreaIntensity

**Parameters:**
- umbraBeforeAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeLineIntensity((Planet)arg1, (float)umbraBeforeLineIntensity[, (Anim)animator]) -> None`

Setter for property umbraBeforeLineIntensity

**Parameters:**
- umbraBeforeLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUseHybridRatio((Planet)arg1, (float)useHybridRatio[, (Anim)animator]) -> None`

Setter for property useHybridRatio

**Parameters:**
- useHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setWaterSpecularIntensity((Planet)arg1, (float)waterSpecularIntensity[, (Anim)animator]) -> None`

Setter for property waterSpecularIntensity

**Parameters:**
- waterSpecularIntensity (double) – Water shininess intensity of the planet. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setWaterSpecularShininess((Planet)arg1, (float)waterSpecularShininess[, (Anim)animator]) -> None`

Setter for property waterSpecularShininess

**Parameters:**
- waterSpecularShininess (double) – Water shininess of the planet. Usually in range [0;128]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property antumbraAreaColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property antumbraAreaIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property antumbraLineIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property atmosphereHaloIntensity`

Intensity of star and satellite halos observed through the Atmosphere. Usually in range [0;1]

### property: `property atmosphereIntensity`

Intensity of the planet’s atmosphere if available. Usually in range [0;1]

### property: `property atmosphericRefractionFactor`

Earth only, atmospheric refraction factor, 0 -> no refraction, 1 -> normal refraction (goes up to 5), only works when atmosphere and planet is on

### property: `property auroraIntensity`

Intensity of the planet’s auroras if available. Usually in range [0;1]

### property: `property cloudAltitude`

Altitude of the clouds.

### property: `property cloudCoverage`

Percentage of the cloud coverage of the planet’s clouds (only applicable to the Earth). In range [0;1]

### property: `property cloudDirection`

Direction of clouds movement. Warning: Must be used during initialization when clouds are OFF.

### property: `property cloudLightPollution`

LightPollution of the clouds.

### property: `property cloudModel`

None( (skyExplorer.Planet)arg1) -> object

### property: `property cloudRaininess`

Percentage of the cloud raininess of the planet’s clouds (only applicable to the Earth). In range [0;1]

### property: `property cloudSpeed`

Speed factor of clouds (default : 1.0). Warning: Must be used during initialization when clouds are OFF.

### property: `property cloudThickness`

Thickness of the clouds.

### property: `property cloudsIntensity`

Intensity of the planet’s clouds if available. Usually in range [0;1]

### property: `property collisionOffset`

Minimun distance camera can approch to the planet surface in meters.

### property: `property eclipseShapeIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property eclipticBandIntensity`

Intensity of the planet’s ecliptic band (if available). Range [0;1]

### property: `property eclipticEquinoxesIntensity`

Intensity of the planet’s ecliptic equinoxes (if available). Range [0;1]

### property: `property eclipticGraduationType`

### property: `property eclipticGridIntensity`

Intensity of the planet’s ecliptic grid if available. Usually in range [0;1]

### property: `property eclipticMarkIntensity`

Intensity of the planet’s ecliptic mark if available. Usually in range [0;1]

### property: `property eclipticMeridianIntensity`

Intensity of the planet’s ecliptic meridian (if available). Range [0;1]

### property: `property eclipticPoleAxisIntensity`

Intensity of the planet’s ecliptic pole axis (if available). Range [0;1]

### property: `property eclipticPoleAxisScale`

Scale of the planet’s ecliptic pole axis (if available).

### property: `property eclipticPolePointerIntensity`

Intensity of the planet’s ecliptic Poles pointers if available. Usually in range [0;1]

### property: `property elevationScale`

Modify elevation scale of planet’s reliefs. In some modelsets of planets do not use this property.

### property: `property equatorialEquinoxesIntensity`

Intensity of the planet’s equatorial equinoxes (if available). Range [0;1]

### property: `property equatorialGridIntensity`

Intensity of the planet’s equatorial grid if available. Usually in range [0;1]

### property: `property equatorialJ2000EquinoxesIntensity`

Intensity of the planet’s equatorial J2000 equinoxess (if available). Range [0;1]

### property: `property equatorialJ2000GridIntensity`

Intensity of the planet’s equatorial J2000 grid (if available). Range [0;1]

### property: `property equatorialJ2000MeridianIntensity`

Intensity of the planet’s equatorial J2000 prime meridian (if available). Range [0;1]

### property: `property equatorialJ2000PoleIntensity`

Intensity of the planet’s equatorial J2000 pole (if available). Range [0;1]

### property: `property equatorialMarkIntensity`

Intensity of the planet’s equatorial mark if available. Usually in range [0;1]

### property: `property equatorialMeridianIntensity`

Intensity of the planet’s equatorial meridian (if available). Range [0;1]

### property: `property equatorialPoleAxisIntensity`

Intensity of the planet’s equatorial pole axis (if available). Range [0;1]

### property: `property equatorialPoleAxisScale`

Scale of the planet’s equatorial pole axis (if available).

### property: `property equatorialPolePointerIntensity`

Intensity of the planet’s equatorial Poles pointers if available. Usually in range [0;1]

### property: `property equatorialSyncGraticuleIntensity`

Intensity of the planet’s equatorial synchronous graticule (if available). Range [0;1]

### property: `property equatorialSyncMagneticPolesIntensity`

Intensity of the planet’s equatorial synchronous magnetic poles (if available). Range [0;1]

### property: `property equatorialSyncMarkIntensity`

Intensity of the planet’s equatorial synchronous mark (if available). Range [0;1]

### property: `property equatorialSyncMeridianIntensity`

Intensity of the planet’s equatorial synchronous prime meridian (if available). Range [0;1]

### property: `property equatorialSyncPolarCirclesIntensity`

Intensity of the planet’s equatorial synchronous polar circles (if available). Range [0;1]

### property: `property equatorialSyncTropicsIntensity`

Intensity of the planet’s equatorial synchronous tropics (if available). Range [0;1]

### property: `property flatteningFactor`

Flattening factor.

### property: `property flatteningOriginal`

[Read-only]

Read-only original flattening (0 means no flattening).

### property: `property hybridRatio`

Used to define which device will display the planet. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the planet. Usually in range [0;1].

### property: `property labelColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property labelIntensity`

Intensity of the planet’s label. Usually in range [0;1].

### property: `property lightPollutionIntensity`

Intensity of the planet’s light pollution map if available. Usually in range [0;1]

### property: `property livePatchBottomLeft`

South west LBR point of the patch. Unit : degrees.

### property: `property livePatchGamma`

Gamma correction for the patch.

### property: `property livePatchHsv`

Hue, Saturation and Lightness value used for the patch.

### property: `property livePatchIntensity`

Intensity of the live patch. Usually in range [0;1]

### property: `property livePatchKeyColor`

Color to remove from patch texture (RGB + tolerance).

### property: `property livePatchRotation`

Rotation of the patch around center point in degrees.

### property: `property livePatchTexture`

Texture to apply on the live patch.

### property: `property livePatchTopRight`

North east LBR point of the patch. Unit : degrees.

### property: `property livePatchVibrance`

Vibrance value used in coordination with HSV value.

### property: `property magnetosphereIntensity`

Intensity of the planet’s magnetosphere if available. Usually in range [0;1]

### property: `property name`

Returns the name.

### property: `property nightLightsIntensity`

Intensity of the planet’s night lights if available. Usually in range [0;1]

### property: `property orbitIntensity`

Intensity of the planet’s orbit. Usually in range [0;1]

### property: `property osgId`

Returns the osgId.

### property: `property penumbraAfterAreaColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property penumbraAfterAreaIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property penumbraAfterLineIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property penumbraBeforeAreaColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property penumbraBeforeAreaIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property penumbraBeforeLineIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property planetShineStrength`

Intensity of the planet’s ecliptic polar circle if available. Usually in range [0;1]

### property: `property pointSaturation`

Saturation of the planet when viewed as a point

### property: `property pointerIntensity`

Intensity of the planet’s pointer. Usually in range [0;1].

### property: `property pointerType`

Current planet pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property polarCircleIntensity`

Intensity of the planet’s ecliptic polar circle if available. Usually in range [0;1]

### property: `property position`

[Read-only]

Position of the planet in ICRF coordinate system.

### property: `property rainbowIntensity`

Percentage of the rainbow intensity of the planet’s clouds (only applicable to the Earth). In range [0;1]

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property revolutionSpeedScale`

Speed factor of the planet’s revolution.

### property: `property ringModel`

None( (skyExplorer.Planet)arg1) -> object

### property: `property rockyCliffIntensity`

Rocky cliff intensity of the planet. Usually in range [0;1]

### property: `property rotationSpeedScale`

Speed factor of the planet’s rotation.

### property: `property scale`

Scale factor of the planet. It can be used to enlarge apparent size of the planet.

### property: `property scatteringIntensity`

Planet’s atmosphere scattering intensity. Usually in range [0;1]

### property: `property seaLevel`

Sea level level of the sea level in meter.

### property: `property seaLevelRenderingMode`

Sea level rendering mode use ‘NONE’ for off.

### property: `property shadowConeAntumbraAdvancement`

None( (skyExplorer.Planet)arg1) -> float

### property: `property shadowConeIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property shadowConePenumbraAdvancement`

None( (skyExplorer.Planet)arg1) -> float

### property: `property shadowConeSectionDistance`

None( (skyExplorer.Planet)arg1) -> float

### property: `property shadowConeSectionIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property shadowContrast`

Contrast of the planet’s shadow. Usually in range [0;1]

### property: `property shadowStrength`

Strength of the planet’s shadow. Usually in range [0;1]

### property: `property supergalacticBandIntensity`

Intensity of the supergalactic mark band. Usually in range [0;1]

### property: `property supergalacticGridIntensity`

Intensity of the supergalactic mark grid. Usually in range [0;1]

### property: `property supergalacticMarkLineIntensity`

Intensity of the supergalactic mark line. Usually in range [0;1]

### property: `property terrainIntensity`

Intensity of the planet’s terrain if available. Usually in range [0;1]

### property: `property terrainModel`

None( (skyExplorer.Planet)arg1) -> object

### property: `property terrainRenderingMode`

Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.

### property: `property tilesetDistanceMax`

None( (skyExplorer.Planet)arg1) -> float

### property: `property tilesetDistanceMin`

None( (skyExplorer.Planet)arg1) -> float

### property: `property tilesetIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property tilesetUrl`

3D Tiles URL

### property: `property topographicGradientTextureFilename`

Texture to use to color planet in topographic mode.

### property: `property trajectoryIntensity`

Intensity of the planet’s trajectory. Usually in range [0;1] if set to positive value, planet will draw a line according to it’s movement on the dome.

### property: `property treeDensity`

Tree density.

### property: `property treeIntensity`

Tree intensity.

### property: `property treeMaxDistance`

Tree fade out distance.

### property: `property umbraAfterAreaColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property umbraAfterAreaIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property umbraAfterLineIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property umbraBeforeAreaColor`

None( (skyExplorer.Planet)arg1) -> skyExplorer.Vec3

### property: `property umbraBeforeAreaIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property umbraBeforeLineIntensity`

None( (skyExplorer.Planet)arg1) -> float

### property: `property useHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.

### property: `property waterSpecularIntensity`

Water shininess intensity of the planet. Usually in range [0;1]

### property: `property waterSpecularShininess`

Water shininess of the planet. Usually in range [0;128]

---

# skyExplorer.RemoteShow

## class skyExplorer.RemoteShow

### `pause((RemoteShow)arg1, (int)id) -> None`

Pause a spc script file, identified by it’s id.

**Parameters:**
- id (int) – Id of the spc file.

### `play((RemoteShow)arg1, (object)filename) -> None`

Play a spc script file.

**Parameters:**
- filename (str) – Spc file path. it can be neither a full path nor a relative path to user folder.

### `playInstantaneous((RemoteShow)arg1, (object)filename) -> None`

Play a spc script file instantaneously.

**Parameters:**
- filename (str) – Spc file path. it can be neither a full path nor a relative path to user folder.

### `playLoop((RemoteShow)arg1, (object)filename) -> None`

Play a spc script in loop mode.

**Parameters:**
- filename (str) – Spc file path. it can be neither a full path nor a relative path to user folder.

### `resume((RemoteShow)arg1, (int)id) -> None`

Resume a paused spc script file, identified by it’s id.

**Parameters:**
- id (int) – Id of the spc file.

### `stop((RemoteShow)arg1, (int)id) -> None`

Stop a spc script file, identified by it’s id.

**Parameters:**
- id (int) – Id of the spc file.

---

# skyExplorer.Satellite

## class skyExplorer.Satellite

### class PatchLayer

InvalidPatchLayer

Layer_01

Layer_02

### class SatelliteName

InvalidSatellite

Moon

Phobos

Deimos

Io

Europa

Ganymede

Callisto

Mimas

Enceladus

Tethys

Dione

Rhea

Titan

Hyperion

Iapetus

Atlas

Pan

Miranda

Ariel

Umbriel

Titania

Oberon

Triton

Charon

Nix

Hydra

SatelliteCount

### class SatellitePort

InvalidSatellitePort

EquatorialSynchronous

Galactic

EquatorialJ2000

Equatorial

NoonEcliptic

NoonEquatorial

OrbitalMeanEquinox

### class ShadowConeArea

InvalidShadowConeArea

UmbraBefore

UmbraAfter

PenumbraBefore

PenumbraAfter

Antumbra

### class ShadowConeLineDrawingMode

InvalidShadowConeLineDrawingMode

Default

DotsLine

Line

Dots

Trail

### class ShadowConeRepresentation

InvalidShadowConeRepresentation

COLOR_2D

COLOR_3D

OCCULTATION_2D

### class TerrainModel

InvalidTerrainModel

DefaultTerrain

Basic

Cassini

Clementine

DidSliced

Galileo

LROC

NewHorizons

RAW

Sliced

Topography

Voyager

CassiniBW

### `addChild((Satellite)arg1, (int)child, (Satellite.SatellitePort)port) -> None`

Add a child object to the satellite scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (SatellitePort) – Coordinate system to use for adding child. See SatellitePort documentation for more information.

### `patchLayerAdd((Satellite)arg1, (Satellite.PatchLayer)layerId, (int)patchId, (Anim)anim) -> None`

Add a layer to planet patch

**Parameters:**
- layerId (PatchLayer)
- patchId (int)
- anim (Anim, optional) – defaults to Anim()

### `patchLayerClear((Satellite)arg1, (Satellite.PatchLayer)layerId, (Anim)anim) -> None`

Remove all patch layer from planet

**Parameters:**
- layerId (PatchLayer)
- anim (Anim, optional) – defaults to Anim()

### `portId((Satellite)arg1, (Satellite.SatellitePort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (SatellitePort) – Name of the port. See ‘SatellitePort’ documentation for more information.

### `setAntumbraAreaColor((Satellite)arg1, (Vec3)antumbraAreaColor[, (Anim)animator]) -> None`

Setter for property antumbraAreaColor

**Parameters:**
- antumbraAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAntumbraAreaIntensity((Satellite)arg1, (float)antumbraAreaIntensity[, (Anim)animator]) -> None`

Setter for property antumbraAreaIntensity

**Parameters:**
- antumbraAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setAntumbraLineIntensity((Satellite)arg1, (float)antumbraLineIntensity[, (Anim)animator]) -> None`

Setter for property antumbraLineIntensity

**Parameters:**
- antumbraLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCloudsIntensity((Satellite)arg1, (float)cloudsIntensity[, (Anim)animator]) -> None`

Setter for property cloudsIntensity

**Parameters:**
- cloudsIntensity (double) – Intensity of the satelite’s clouds if available. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setCollisionOffset((Satellite)arg1, (float)collisionOffset[, (Anim)animator]) -> None`

Setter for property collisionOffset

**Parameters:**
- collisionOffset (double) – Minimun distance camera can approch to the satellite surface in meters.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setEclipseShapeIntensity((Satellite)arg1, (float)eclipseShapeIntensity[, (Anim)animator]) -> None`

Setter for property eclipseShapeIntensity

**Parameters:**
- eclipseShapeIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setElevationScale((Satellite)arg1, (float)elevationScale[, (Anim)animator]) -> None`

Setter for property elevationScale

**Parameters:**
- elevationScale (double) – Modify elevation scale of satelite’s reliefs. In some modelsets of planets do not use this property.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFlatteningFactor((Satellite)arg1, (float)flatteningFactor[, (Anim)animator]) -> None`

Setter for property flatteningFactor

**Parameters:**
- flatteningFactor (double) – Flattening factor.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHybridRatio((Satellite)arg1, (float)hybridRatio[, (Anim)animator]) -> None`

Setter for property hybridRatio

**Parameters:**
- hybridRatio (double) – Used to define which device will display the satellite. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Satellite)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the satellite. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLabelIntensity((Satellite)arg1, (float)labelIntensity[, (Anim)animator]) -> None`

Setter for property labelIntensity

**Parameters:**
- labelIntensity (double) – Intensity of the label of the satellite. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchBottomLeft((Satellite)arg1, (Vec3)livePatchBottomLeft[, (Anim)animator]) -> None`

Setter for property livePatchBottomLeft

**Parameters:**
- livePatchBottomLeft (Vec3) – South west LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchGamma((Satellite)arg1, (Vec3)livePatchGamma[, (Anim)animator]) -> None`

Setter for property livePatchGamma

**Parameters:**
- livePatchGamma (Vec3) – Gamma correction for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchHsv((Satellite)arg1, (Vec3)livePatchHsv[, (Anim)animator]) -> None`

Setter for property livePatchHsv

**Parameters:**
- livePatchHsv (Vec3) – Hue, Saturation and Lightness value used for the patch.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchIntensity((Satellite)arg1, (float)livePatchIntensity[, (Anim)animator]) -> None`

Setter for property livePatchIntensity

**Parameters:**
- livePatchIntensity (double) – Intensity of the live patch. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchKeyColor((Satellite)arg1, (Vec4)livePatchKeyColor[, (Anim)animator]) -> None`

Setter for property livePatchKeyColor

**Parameters:**
- livePatchKeyColor (Vec4) – Color to remove from patch texture (RGB + tolerance).
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchRotation((Satellite)arg1, (float)livePatchRotation[, (Anim)animator]) -> None`

Setter for property livePatchRotation

**Parameters:**
- livePatchRotation (double) – Rotation of the patch around center point in degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchTexture((Satellite)arg1, (object)livePatchTexture) -> None`

Setter for property livePatchTexture

**Parameters:**
- livePatchTexture (str) – Texture to apply on the live patch.

### `setLivePatchTopRight((Satellite)arg1, (Vec3)livePatchTopRight[, (Anim)animator]) -> None`

Setter for property livePatchTopRight

**Parameters:**
- livePatchTopRight (Vec3) – North east LBR point of the patch. Unit : degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setLivePatchVibrance((Satellite)arg1, (float)livePatchVibrance[, (Anim)animator]) -> None`

Setter for property livePatchVibrance

**Parameters:**
- livePatchVibrance (double) – Vibrance value used in coordination with HSV value.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setManualMoonPhase((Satellite)arg1, (bool)manualMoonPhase) -> None`

Setter for property manualMoonPhase

**Parameters:**
- manualMoonPhase (bool) – Enable or disable manual moon phase mode.

### `setManualSurfaceColor((Satellite)arg1, (bool)manualSurfaceColor) -> None`

Setter for property manualSurfaceColor

**Parameters:**
- manualSurfaceColor (bool) – Set the surface color. Need to use manual surface color mode

### `setMoonAge((Satellite)arg1, (float)moonAge[, (Anim)animator]) -> None`

Setter for property moonAge

**Parameters:**
- moonAge (double) – Combined with manualMoonPhase. Setup moon age to display phase. In range [0;29.5]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setOrbitIntensity((Satellite)arg1, (float)orbitIntensity[, (Anim)animator]) -> None`

Setter for property orbitIntensity

**Parameters:**
- orbitIntensity (double) – Intensity of the orbit of the satellite. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPatchLayerGamma((Satellite)arg1, (Satellite.PatchLayer)layerId, (Vec3)gamma, (Anim)anim) -> None`

Gamma correction for the patc layerh.

**Parameters:**
- layerId (PatchLayer)
- gamma (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerHsv((Satellite)arg1, (Satellite.PatchLayer)layerId, (Vec3)hsv, (Anim)anim) -> None`

Hue, Saturation and Lightness value used for the patch layer.

**Parameters:**
- layerId (PatchLayer)
- hsv (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerKeyColor((Satellite)arg1, (Satellite.PatchLayer)layerId, (Vec4)keColor, (Anim)anim) -> None`

Color to remove from patch texture (RGB + tolerance).

**Parameters:**
- layerId (PatchLayer)
- keColor (Vec4)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerOpacity((Satellite)arg1, (Satellite.PatchLayer)layerId, (float)opacity, (Anim)anim) -> None`

Intensity of the patch layer. Usually in range [0;1]

**Parameters:**
- layerId (PatchLayer)
- opacity (double)
- anim (Anim, optional) – defaults to Anim()

### `setPatchLayerVibrance((Satellite)arg1, (Satellite.PatchLayer)layerId, (float)vibrance, (Anim)anim) -> None`

Vibrance value used in coordination with HSV value of the patch layer.

**Parameters:**
- layerId (PatchLayer)
- vibrance (double)
- anim (Anim, optional) – defaults to Anim()

### `setPenumbraAfterAreaColor((Satellite)arg1, (Vec3)penumbraAfterAreaColor[, (Anim)animator]) -> None`

Setter for property penumbraAfterAreaColor

**Parameters:**
- penumbraAfterAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraAfterAreaIntensity((Satellite)arg1, (float)penumbraAfterAreaIntensity[, (Anim)animator]) -> None`

Setter for property penumbraAfterAreaIntensity

**Parameters:**
- penumbraAfterAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraAfterLineIntensity((Satellite)arg1, (float)penumbraAfterLineIntensity[, (Anim)animator]) -> None`

Setter for property penumbraAfterLineIntensity

**Parameters:**
- penumbraAfterLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeAreaColor((Satellite)arg1, (Vec3)penumbraBeforeAreaColor[, (Anim)animator]) -> None`

Setter for property penumbraBeforeAreaColor

**Parameters:**
- penumbraBeforeAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeAreaIntensity((Satellite)arg1, (float)penumbraBeforeAreaIntensity[, (Anim)animator]) -> None`

Setter for property penumbraBeforeAreaIntensity

**Parameters:**
- penumbraBeforeAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPenumbraBeforeLineIntensity((Satellite)arg1, (float)penumbraBeforeLineIntensity[, (Anim)animator]) -> None`

Setter for property penumbraBeforeLineIntensity

**Parameters:**
- penumbraBeforeLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPlanetShineStrength((Satellite)arg1, (float)planetShineStrength[, (Anim)animator]) -> None`

Setter for property planetShineStrength

**Parameters:**
- planetShineStrength (double) – Strength of the planet shine. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerIntensity((Satellite)arg1, (float)pointerIntensity[, (Anim)animator]) -> None`

Setter for property pointerIntensity

**Parameters:**
- pointerIntensity (double) – Intensity of the pointer of the satellite. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointerType((Satellite)arg1, (Body.PointerType)pointerType) -> None`

Setter for property pointerType

**Parameters:**
- pointerType (PointerType) – Current satellite pointer type. See ‘Body.PointerType’ documentation for vailable values.

### `setScale((Satellite)arg1, (float)scale[, (Anim)animator]) -> None`

Setter for property scale

**Parameters:**
- scale (double) – Scale factor of the satellite. It can be used to enlarge apparent size of the satellite.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSeaLevel((Satellite)arg1, (float)seaLevel[, (Anim)animator]) -> None`

Setter for property seaLevel

**Parameters:**
- seaLevel (double) – Sea level level of the sea level in meter.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSeaLevelRenderingMode((Satellite)arg1, (object)seaLevelRenderingMode[, (Anim)animator]) -> None`

Setter for property seaLevelRenderingMode

**Parameters:**
- seaLevelRenderingMode (str) – Sea level rendering mode use ‘NONE’ for off.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeAntumbraAdvancement((Satellite)arg1, (float)shadowConeAntumbraAdvancement[, (Anim)animator]) -> None`

Setter for property shadowConeAntumbraAdvancement

**Parameters:**
- shadowConeAntumbraAdvancement (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeAreaColor((Satellite)arg1, (Satellite.ShadowConeArea)area, (Vec3)color, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- color (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeAreaIntensity((Satellite)arg1, (Satellite.ShadowConeArea)area, (float)intensity, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- intensity (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeIntensity((Satellite)arg1, (float)shadowConeIntensity[, (Anim)animator]) -> None`

Setter for property shadowConeIntensity

**Parameters:**
- shadowConeIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeLineColor((Satellite)arg1, (Satellite.ShadowConeArea)area, (Vec3)intensity, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- intensity (Vec3)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineDrawingMode((Satellite)arg1, (Satellite.ShadowConeArea)area, (Satellite.ShadowConeLineDrawingMode)representation, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- representation (ShadowConeLineDrawingMode)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineIntensity((Satellite)arg1, (Satellite.ShadowConeArea)area, (float)color, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- color (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeLineThickness((Satellite)arg1, (Satellite.ShadowConeArea)area, (float)thickness, (Anim)anim) -> None`

**Parameters:**
- area (ShadowConeArea)
- thickness (double)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConePenumbraAdvancement((Satellite)arg1, (float)shadowConePenumbraAdvancement[, (Anim)animator]) -> None`

Setter for property shadowConePenumbraAdvancement

**Parameters:**
- shadowConePenumbraAdvancement (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeRepresentationType((Satellite)arg1, (Satellite.ShadowConeRepresentation)representation, (Anim)anim) -> None`

**Parameters:**
- representation (ShadowConeRepresentation)
- anim (Anim, optional) – defaults to Anim()

### `setShadowConeSectionDistance((Satellite)arg1, (float)shadowConeSectionDistance[, (Anim)animator]) -> None`

Setter for property shadowConeSectionDistance

**Parameters:**
- shadowConeSectionDistance (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowConeSectionIntensity((Satellite)arg1, (float)shadowConeSectionIntensity[, (Anim)animator]) -> None`

Setter for property shadowConeSectionIntensity

**Parameters:**
- shadowConeSectionIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowContrast((Satellite)arg1, (float)shadowContrast[, (Anim)animator]) -> None`

Setter for property shadowContrast

**Parameters:**
- shadowContrast (double) – Contrast of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setShadowStrength((Satellite)arg1, (float)shadowStrength[, (Anim)animator]) -> None`

Setter for property shadowStrength

**Parameters:**
- shadowStrength (double) – Strength of the planet’s shadow. Usually in range [0;1]
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setSurfaceColor((Satellite)arg1, (Vec3)surfaceColor[, (Anim)animator]) -> None`

Setter for property surfaceColor

**Parameters:**
- surfaceColor (Vec3) – Set the surface color. Need to use manual surface color mode
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainModel((Satellite)arg1, (Satellite.TerrainModel)terrainModel[, (Anim)animator]) -> None`

Setter for property terrainModel

**Parameters:**
- terrainModel (TerrainModel)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTerrainRenderingMode((Satellite)arg1, (object)terrainRenderingMode[, (Anim)animator]) -> None`

Setter for property terrainRenderingMode

**Parameters:**
- terrainRenderingMode (str) – Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTrajectoryIntensity((Satellite)arg1, (float)trajectoryIntensity[, (Anim)animator]) -> None`

Setter for property trajectoryIntensity

**Parameters:**
- trajectoryIntensity (double) – Intensity of the trajectory of the satellite. Usually in range [0;1]. If set to positive value, the satellite will draw a line according to it’s movement on the dome.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterAreaColor((Satellite)arg1, (Vec3)umbraAfterAreaColor[, (Anim)animator]) -> None`

Setter for property umbraAfterAreaColor

**Parameters:**
- umbraAfterAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterAreaIntensity((Satellite)arg1, (float)umbraAfterAreaIntensity[, (Anim)animator]) -> None`

Setter for property umbraAfterAreaIntensity

**Parameters:**
- umbraAfterAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraAfterLineIntensity((Satellite)arg1, (float)umbraAfterLineIntensity[, (Anim)animator]) -> None`

Setter for property umbraAfterLineIntensity

**Parameters:**
- umbraAfterLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeAreaColor((Satellite)arg1, (Vec3)umbraBeforeAreaColor[, (Anim)animator]) -> None`

Setter for property umbraBeforeAreaColor

**Parameters:**
- umbraBeforeAreaColor (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeAreaIntensity((Satellite)arg1, (float)umbraBeforeAreaIntensity[, (Anim)animator]) -> None`

Setter for property umbraBeforeAreaIntensity

**Parameters:**
- umbraBeforeAreaIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUmbraBeforeLineIntensity((Satellite)arg1, (float)umbraBeforeLineIntensity[, (Anim)animator]) -> None`

Setter for property umbraBeforeLineIntensity

**Parameters:**
- umbraBeforeLineIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUseHybridRatio((Satellite)arg1, (float)useHybridRatio[, (Anim)animator]) -> None`

Setter for property useHybridRatio

**Parameters:**
- useHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property antumbraAreaColor`

None( (skyExplorer.Satellite)arg1) -> skyExplorer.Vec3

### property: `property antumbraAreaIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property antumbraLineIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property cloudsIntensity`

Intensity of the satelite’s clouds if available. Usually in range [0;1]

### property: `property collisionOffset`

Minimun distance camera can approch to the satellite surface in meters.

### property: `property eclipseShapeIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property elevationScale`

Modify elevation scale of satelite’s reliefs. In some modelsets of planets do not use this property.

### property: `property flatteningFactor`

Flattening factor.

### property: `property flatteningOriginal`

[Read-only]

Read-only original flattening (0 means no flattening).

### property: `property hybridRatio`

Used to define which device will display the satellite. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the satellite. Usually in range [0;1].

### property: `property labelIntensity`

Intensity of the label of the satellite. Usually in range [0;1].

### property: `property livePatchBottomLeft`

South west LBR point of the patch. Unit : degrees.

### property: `property livePatchGamma`

Gamma correction for the patch.

### property: `property livePatchHsv`

Hue, Saturation and Lightness value used for the patch.

### property: `property livePatchIntensity`

Intensity of the live patch. Usually in range [0;1]

### property: `property livePatchKeyColor`

Color to remove from patch texture (RGB + tolerance).

### property: `property livePatchRotation`

Rotation of the patch around center point in degrees.

### property: `property livePatchTexture`

Texture to apply on the live patch.

### property: `property livePatchTopRight`

North east LBR point of the patch. Unit : degrees.

### property: `property livePatchVibrance`

Vibrance value used in coordination with HSV value.

### property: `property manualMoonPhase`

Enable or disable manual moon phase mode.

### property: `property manualSurfaceColor`

Set the surface color. Need to use manual surface color mode

### property: `property moonAge`

Combined with manualMoonPhase. Setup moon age to display phase. In range [0;29.5]

### property: `property name`

Returns the name.

### property: `property orbitIntensity`

Intensity of the orbit of the satellite. Usually in range [0;1].

### property: `property osgId`

Returns the osgId.

### property: `property penumbraAfterAreaColor`

None( (skyExplorer.Satellite)arg1) -> skyExplorer.Vec3

### property: `property penumbraAfterAreaIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property penumbraAfterLineIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property penumbraBeforeAreaColor`

None( (skyExplorer.Satellite)arg1) -> skyExplorer.Vec3

### property: `property penumbraBeforeAreaIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property penumbraBeforeLineIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property planetShineStrength`

Strength of the planet shine. Usually in range [0;1]

### property: `property pointerIntensity`

Intensity of the pointer of the satellite. Usually in range [0;1].

### property: `property pointerType`

Current satellite pointer type. See ‘Body.PointerType’ documentation for vailable values.

### property: `property position`

[Read-only]

Position of the satellite in ICRF coordinate system.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property scale`

Scale factor of the satellite. It can be used to enlarge apparent size of the satellite.

### property: `property seaLevel`

Sea level level of the sea level in meter.

### property: `property seaLevelRenderingMode`

Sea level rendering mode use ‘NONE’ for off.

### property: `property shadowConeAntumbraAdvancement`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property shadowConeIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property shadowConePenumbraAdvancement`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property shadowConeSectionDistance`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property shadowConeSectionIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property shadowContrast`

Contrast of the planet’s shadow. Usually in range [0;1]

### property: `property shadowStrength`

Strength of the planet’s shadow. Usually in range [0;1]

### property: `property surfaceColor`

Set the surface color. Need to use manual surface color mode

### property: `property terrainModel`

None( (skyExplorer.Satellite)arg1) -> object

### property: `property terrainRenderingMode`

Terrain rendering mode use TOPOGRAPHY OR PHOTOGRAY.

### property: `property trajectoryIntensity`

Intensity of the trajectory of the satellite. Usually in range [0;1]. If set to positive value, the satellite will draw a line according to it’s movement on the dome.

### property: `property umbraAfterAreaColor`

None( (skyExplorer.Satellite)arg1) -> skyExplorer.Vec3

### property: `property umbraAfterAreaIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property umbraAfterLineIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property umbraBeforeAreaColor`

None( (skyExplorer.Satellite)arg1) -> skyExplorer.Vec3

### property: `property umbraBeforeAreaIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property umbraBeforeLineIntensity`

None( (skyExplorer.Satellite)arg1) -> float

### property: `property useHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.

---

# skyExplorer.SceneGraph

## class skyExplorer.SceneGraph

### class ConnexionState

InvalidConnexionState

Disconnected

Connected

### `executeDebugCommand((SceneGraph)arg1, (object)command) -> None`

**Parameters:**
- command (str)

### `reset((SceneGraph)arg1, (int)reinitId) -> None`

Reset skyExplorer system.

**Parameters:**
- reinitId (int, optional) – Index of reinit script., defaults to 1

### `setDefaultTextFont((SceneGraph)arg1, (object)defaultTextFont[, (Anim)animator]) -> None`

Setter for property defaultTextFont

**Parameters:**
- defaultTextFont (str) – Default skyExplorer font file path. Must be relative to user folder.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMultipipeConfig((SceneGraph)arg1, (object)multipipeConfig) -> None`

Setter for property multipipeConfig

**Parameters:**
- multipipeConfig (str)

### `setOculusRoomDiameterInclination((SceneGraph)arg1, (Vec2)oculusRoomDiameterInclination) -> None`

Setter for property oculusRoomDiameterInclination

**Parameters:**
- oculusRoomDiameterInclination (Vec2)

### `setOculusRoomModel((SceneGraph)arg1, (object)oculusRoomModel) -> None`

Setter for property oculusRoomModel

**Parameters:**
- oculusRoomModel (str)

### `setOculusRoomOffset((SceneGraph)arg1, (Vec3)oculusRoomOffset[, (Anim)animator]) -> None`

Setter for property oculusRoomOffset

**Parameters:**
- oculusRoomOffset (Vec3)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property connexionState`

[Read-only]

Current network connection state.

### property: `property multipipeConfig`

None( (skyExplorer.SceneGraph)arg1) -> object

### property: `property oculusRoomDiameterInclination`

None( (skyExplorer.SceneGraph)arg1) -> skyExplorer.Vec2

### property: `property oculusRoomModel`

None( (skyExplorer.SceneGraph)arg1) -> object

### property: `property oculusRoomOffset`

None( (skyExplorer.SceneGraph)arg1) -> skyExplorer.Vec3

### property: `property resetWatcher`

None( (skyExplorer.SceneGraph)arg1) -> float

---

# skyExplorer.ShootingStar

## class skyExplorer.ShootingStar

### class Model

InvalidModel

None

Default

Gradient

### class Referential

InvalidReferential

TargetedForeground

RaDec

### class ShootingStarName

InvalidShootingStar

ShootingStar001

ShootingStar002

ShootingStar003

ShootingStar004

ShootingStar005

ShootingStar006

ShootingStar007

ShootingStar008

ShootingStar009

ShootingStar010

ShootingStar011

ShootingStar012

ShootingStar013

ShootingStar014

ShootingStar015

ShootingStar016

ShootingStar017

ShootingStar018

ShootingStar019

ShootingStar020

ShootingStar021

ShootingStar022

ShootingStar023

ShootingStar024

ShootingStar025

ShootingStar026

ShootingStar027

ShootingStar028

ShootingStar029

ShootingStar030

ShootingStar031

ShootingStar032

ShootingStar033

ShootingStar034

ShootingStar035

ShootingStar036

ShootingStar037

ShootingStar038

ShootingStar039

ShootingStar040

ShootingStar041

ShootingStar042

ShootingStar043

ShootingStar044

ShootingStar045

ShootingStar046

ShootingStar047

ShootingStar048

ShootingStar049

ShootingStar050

ShootingStar051

ShootingStar052

ShootingStar053

ShootingStar054

ShootingStar055

ShootingStar056

ShootingStar057

ShootingStar058

ShootingStar059

ShootingStar060

ShootingStar061

ShootingStar062

ShootingStar063

ShootingStar064

ShootingStar065

ShootingStar066

ShootingStar067

ShootingStar068

ShootingStar069

ShootingStar070

ShootingStar071

ShootingStar072

ShootingStar073

ShootingStar074

ShootingStar075

ShootingStar076

ShootingStar077

ShootingStar078

ShootingStar079

ShootingStar080

ShootingStar081

ShootingStar082

ShootingStar083

ShootingStar084

ShootingStar085

ShootingStar086

ShootingStar087

ShootingStar088

ShootingStar089

ShootingStar090

ShootingStar091

ShootingStar092

ShootingStar093

ShootingStar094

ShootingStar095

ShootingStar096

ShootingStar097

ShootingStar098

ShootingStar099

ShootingStar100

ShootingStarCount

### `setAdvancing((ShootingStar)arg1, (float)advancing[, (Anim)animator]) -> None`

Setter for property advancing

**Parameters:**
- advancing (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setArrivalPosition((ShootingStar)arg1, (Vec2)arrivalPosition[, (Anim)animator]) -> None`

Setter for property arrivalPosition

**Parameters:**
- arrivalPosition (Vec2) – Shooting star arrival position on screen. Azimuth / Height in degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setBrightness((ShootingStar)arg1, (float)brightness[, (Anim)animator]) -> None`

Setter for property brightness

**Parameters:**
- brightness (double) – Shooting stars brightness. It will affect the width of the line representing the shooting star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGradientPoint((ShootingStar)arg1, (float)gradientPoint) -> None`

Setter for property gradientPoint

**Parameters:**
- gradientPoint (double) – Position of the point where the gradient begins. usually in range [0;1].

### `setRainChaosGradientPoint((ShootingStar)arg1, (float)rainChaosGradientPoint[, (Anim)animator]) -> None`

Setter for property rainChaosGradientPoint

**Parameters:**
- rainChaosGradientPoint (double) – Radius of the circle (in degrees) from which the shooting stars are generated.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRainGradientPoint((ShootingStar)arg1, (Vec2)rainGradientPoint[, (Anim)animator]) -> None`

Setter for property rainGradientPoint

**Parameters:**
- rainGradientPoint (Vec2) – Position of the center of the circle from which the shooting stars are generated.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRainSeed((ShootingStar)arg1, (int)rainSeed) -> None`

Setter for property rainSeed

**Parameters:**
- rainSeed (int) – Seed used to generate random shooting star. Use 0 to stop shooting star. Other values will generate a new shooting star.

### `setRainSpeed((ShootingStar)arg1, (float)rainSpeed[, (Anim)animator]) -> None`

Setter for property rainSpeed

**Parameters:**
- rainSpeed (double) – Speed of the shooting star. Duration of the trail will be randomized between 0.5/rainSpeed and 2.5/rainSpeed.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setReferential((ShootingStar)arg1, (ShootingStar.Referential)referential) -> None`

Setter for property referential

**Parameters:**
- referential (Referential) – Referential of the shooting stars. Targeted foreground [default] : Shooting stars are generated from a circle in dome space. RaDec Shooting stars are generated from a Circle (in starry sky referential).

### `setRepresentationType((ShootingStar)arg1, (ShootingStar.Model)representationType) -> None`

Setter for property representationType

**Parameters:**
- representationType (Model) – Type of the shooting star’s trail.

### `setStartPosition((ShootingStar)arg1, (Vec2)startPosition[, (Anim)animator]) -> None`

Setter for property startPosition

**Parameters:**
- startPosition (Vec2) – Shooting star start position on screen. Azimuth / Height in degrees.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTrailLength((ShootingStar)arg1, (float)trailLength[, (Anim)animator]) -> None`

Setter for property trailLength

**Parameters:**
- trailLength (double) – Shooting stars tail length. Delay in seconds from the start point of the shooting star.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setZenithalHourlyRate((ShootingStar)arg1, (float)zenithalHourlyRate[, (Anim)animator]) -> None`

Setter for property zenithalHourlyRate

**Parameters:**
- zenithalHourlyRate (double) – Mean number of shooting stars to be drawn per hour
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property advancing`

None( (skyExplorer.ShootingStar)arg1) -> float

### property: `property arrivalPosition`

Shooting star arrival position on screen. Azimuth / Height in degrees.

### property: `property brightness`

Shooting stars brightness. It will affect the width of the line representing the shooting star.

### property: `property gradientPoint`

Position of the point where the gradient begins. usually in range [0;1].

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property rainChaosGradientPoint`

Radius of the circle (in degrees) from which the shooting stars are generated.

### property: `property rainGradientPoint`

Position of the center of the circle from which the shooting stars are generated.

### property: `property rainSeed`

Seed used to generate random shooting star. Use 0 to stop shooting star. Other values will generate a new shooting star.

### property: `property rainSpeed`

Speed of the shooting star. Duration of the trail will be randomized between 0.5/rainSpeed and 2.5/rainSpeed.

### property: `property referential`

Referential of the shooting stars. Targeted foreground [default] : Shooting stars are generated from a circle in dome space. RaDec Shooting stars are generated from a Circle (in starry sky referential).

### property: `property representationType`

Type of the shooting star’s trail.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property startPosition`

Shooting star start position on screen. Azimuth / Height in degrees.

### property: `property trailLength`

Shooting stars tail length. Delay in seconds from the start point of the shooting star.

### property: `property zenithalHourlyRate`

Mean number of shooting stars to be drawn per hour

---

# skyExplorer.ShowEngineManager

## class skyExplorer.ShowEngineManager

### class State

InvalidState

StateIdle

StatePlaying

StatePaused

### `availableSessions((ShowEngineManager)arg1, (object)ipServer, (int)portServer) -> None`

send a request to get the list of launched sessions.

**Parameters:**
- ipServer (str) – Ip address of the DomeCasting server
- portServer (int) – Port of the DomeCasting server

### `pauseAllShows((ShowEngineManager)arg1) -> None`

Pause all running shows.

### `playAllShows((ShowEngineManager)arg1) -> None`

Play all launched shows.

### `playRemoteShow((ShowEngineManager)arg1, (object)fileName) -> None`

Play an spc script file.

**Parameters:**
- fileName (str) – File path to the spc script. It can be neither a full file path nor a relative path to user.

### `startRecording((ShowEngineManager)arg1, (object)filename) -> None`

Start command recording.

**Parameters:**
- filename (str) – Output SPC file

### `stopAllShows((ShowEngineManager)arg1) -> None`

Stop all running shows.

### `stopRecording((ShowEngineManager)arg1) -> None`

Stop command recording.

---

# skyExplorer.SkySurvey

## class skyExplorer.SkySurvey

### class SkySurveyName

InvalidSkySurvey

SkySurvey001

SkySurveyCount

### `setIntensity((SkySurvey)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the sky survey. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUrl((SkySurvey)arg1, (object)url[, (Anim)animator]) -> None`

Setter for property url

**Parameters:**
- url (str) – Url of the sky survey server.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the sky survey. Usually in range [0;1].

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property url`

Url of the sky survey server.

---

# skyExplorer.SlideShowHandler

## class skyExplorer.SlideShowHandler

### class SlideShowHandlerName

InvalidSlideShowHandler

MainSlideShowHandler

SlideShowHandlerCount

### class UserAction

InvalidUserAction

NO_ACTION

PREVIOUS

NEXT

PAUSE

### `setLoad((SlideShowHandler)arg1, (object)load) -> None`

Setter for property load

**Parameters:**
- load (str) – Load an XML file representing a slide show. Path must be relative to user folder.

### `setPause((SlideShowHandler)arg1, (bool)pause) -> None`

Setter for property pause

**Parameters:**
- pause (bool) – Pause current playing slide show. If no slide show currently playing, it has no effect.

### `setStop((SlideShowHandler)arg1, (int)stop) -> None`

Setter for property stop

**Parameters:**
- stop (int) – Stop current playing slide show. If no slide show currently playing, it has no effect.

### `setUserAction((SlideShowHandler)arg1, (SlideShowHandler.UserAction)userAction) -> None`

Setter for property userAction

**Parameters:**
- userAction (UserAction) – Trigger a user action, see ‘UserAction’ documentation for available values.

### property: `property beginningOfSlideShow`

[Read-only]

True if the first animation of slide show has not been played and False else.

### property: `property currentLoadedSlideShow`

[Read-only]

Path to the current loaded slide show. If no slide showLoaded, it will contains an empty string

### property: `property endOfSlideShow`

[Read-only]

True if the last animation of slide show has been played and False else.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pause`

Pause current playing slide show. If no slide show currently playing, it has no effect.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

---

# skyExplorer.SoftwareManager

## class skyExplorer.SoftwareManager

### class HostId

HostId_All

### class HostType

HostType_All

HostType_Master

HostType_IG

HostType_Mult

HostType_Hybrid

### class LogLevel

Debug

Warning

Critical

Fatal

Info

### class SoftwareId

InvalidSoftwareId

SkyExplorer

Studio

FreeDome

AutoCal

ProjectionDesigner

### class Source

Source_Default

Source_SkyExplorer

Source_ViPlayer

### class ZOrder

Background

Foreground

### `bringToForeground((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (int)source) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- softwareId (int)
- source (int)

### `exec((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (object)command) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- command (str)

### `getInfo((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)

### `heartbeat((SoftwareManager)arg1) -> None`

### `reboot((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)

### `sendToBackground((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (int)source) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- softwareId (int)
- source (int)

### `setOpacity((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (int)source, (float)opacity, (float)duration_s) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- softwareId (int)
- source (int)
- opacity (double)
- duration_s (double)

### `setUseAlpha((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (int)source, (bool)useAlpha) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- softwareId (int)
- source (int)
- useAlpha (bool)

### `shutdown((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)

### `softArgsAdd((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (object)arg) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- arg (str)

### `softArgsClear((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)

### `softBringToForeground((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (int)source) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- source (int)

### `softExe((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (object)exe) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- exe (str)

### `softName((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (object)name) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- name (str)

### `softReset((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)

### `softSendToBackground((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (int)source) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- source (int)

### `softSetOpacity((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (int)source, (float)opacity, (float)duration_s) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- source (int)
- opacity (double)
- duration_s (double)

### `softSetUseAlpha((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (int)source, (bool)useAlpha) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- source (int)
- useAlpha (bool)

### `softSrcsAdd((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (int)source) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- source (int)

### `softSrcsClear((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)

### `softStart((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (float)delay_s) -> None`

param hostType: type hostType: HostType param hostId: type hostId: int param dynamicIndex: type dynamicIndex: int param delay_s: type delay_s: double

softStart( (SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (float)delay_s, (int)source0, (float)opacity0, (bool)useAlpha0) -> None :

param hostType: type hostType: HostType param hostId: type hostId: int param dynamicIndex: type dynamicIndex: int param delay_s: type delay_s: double param source0: type source0: int param opacity0: type opacity0: double param useAlpha0: type useAlpha0: bool

softStart( (SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (float)delay_s, (int)source0, (float)opacity0, (bool)useAlpha0, (int)source1, (float)opacity1, (bool)useAlpha1) -> None :

param hostType: type hostType: HostType param hostId: type hostId: int param dynamicIndex: type dynamicIndex: int param delay_s: type delay_s: double param source0: type source0: int param opacity0: type opacity0: double param useAlpha0: type useAlpha0: bool param source1: type source1: int param opacity1: type opacity1: double param useAlpha1: type useAlpha1: bool

### `softStop((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)

### `softVarsAdd((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (object)var) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- var (str)

### `softVarsClear((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)

### `softWorkingDir((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)dynamicIndex, (object)workingDir) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- dynamicIndex (int)
- workingDir (str)

### `start((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (float)delay_s) -> None`

param hostType: type hostType: HostType param hostId: type hostId: int param softwareId: type softwareId: int param delay_s: type delay_s: double

start( (SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (float)delay_s, (int)source0, (float)opacity0, (bool)useAlpha0) -> None :

param hostType: type hostType: HostType param hostId: type hostId: int param softwareId: type softwareId: int param delay_s: type delay_s: double param source0: type source0: int param opacity0: type opacity0: double param useAlpha0: type useAlpha0: bool

start( (SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId, (float)delay_s, (int)source0, (float)opacity0, (bool)useAlpha0, (int)source1, (float)opacity1, (bool)useAlpha1) -> None :

param hostType: type hostType: HostType param hostId: type hostId: int param softwareId: type softwareId: int param delay_s: type delay_s: double param source0: type source0: int param opacity0: type opacity0: double param useAlpha0: type useAlpha0: bool param source1: type source1: int param opacity1: type opacity1: double param useAlpha1: type useAlpha1: bool

### `stop((SoftwareManager)arg1, (SoftwareManager.HostType)hostType, (int)hostId, (int)softwareId) -> None`

**Parameters:**
- hostType (HostType)
- hostId (int)
- softwareId (int)

---

# skyExplorer.Stars

## class skyExplorer.Stars

### class Catalog

InvalidCatalog

GJ

HD

HIP

HR

TYC

SAO

DM

BAD

### class Comparator

InvalidComparator

EqualTo

NotEqualTo

LessThanOrEqualTo

LessThan

GreatherThanOrEqualTo

GreatherThan

### class Filter

InvalidFilter

Distance

AbsoluteMagnitude

ApparentMagnitude

Velocity

EffectiveTemperature

RightAscension

Declination

Radius

Age

Metallicity

ProperMotion

RadialVelocity

### class LogicOperator

InvalidLogicOperator

And

Or

### class LuminosityClass

InvalidLuminosityClass

I

II

III

IV

V

VI

VII

### class Modelset

InvalidModelset

Hipparcos

GaiaDR2

### class SpectralType

InvalidSpectralType

O

B

A

F

G

K

M

Other

### class StarsName

InvalidStars

StarrySky

StarsCount

### class StarsPort

InvalidStarsPort

Ecliptic

TerrestrialEquatorialJ2000

### `addChild((Stars)arg1, (int)child, (Stars.StarsPort)port) -> None`

Add a child object to the stars scene graph.

**Parameters:**
- child (int) – Id of the child object to add.
- port (StarsPort) – Coordinate system to use for adding child. See StarsPort documentation for more information.

### `assignLut((Stars)arg1, (int)lutId, (Anim)anim) -> None`

**Parameters:**
- lutId (int)
- anim (Anim, optional) – defaults to Anim()

### `filterAdd((Stars)arg1, (Stars.Filter)filter, (float)value, (Stars.Comparator)comp, (Stars.LogicOperator)op) -> None`

Add filter. Only with Gaia model

**Parameters:**
- filter (Filter)
- value (double)
- comp (Comparator)
- op (LogicOperator)

### `filterCatalogAdd((Stars)arg1, (Stars.Catalog)catalog, (Stars.Comparator)comp, (Stars.LogicOperator)op) -> None`

Add filter. Only with Gaia model

**Parameters:**
- catalog (Catalog)
- comp (Comparator)
- op (LogicOperator)

### `filterClear((Stars)arg1) -> None`

Clear all filters. Only with Gaia model

### `filterEvaluate((Stars)arg1) -> None`

Evaluate/Apply all filters. Only with Gaia model

### `filterLuminosityClassAdd((Stars)arg1, (Stars.LuminosityClass)luminosityClass, (Stars.Comparator)comp, (Stars.LogicOperator)op) -> None`

Add filter. Only with Gaia model

**Parameters:**
- luminosityClass (LuminosityClass)
- comp (Comparator)
- op (LogicOperator)

### `filterSpectralTypeAdd((Stars)arg1, (Stars.SpectralType)spectralType, (float)subType, (Stars.Comparator)comp, (Stars.LogicOperator)op) -> None`

Add filter. Only with Gaia model

**Parameters:**
- spectralType (SpectralType)
- subType (double)
- comp (Comparator)
- op (LogicOperator)

### `portId((Stars)arg1, (Stars.StarsPort)portName) -> int`

Return the id of the given port

**Parameters:**
- portName (StarsPort) – Name of the port. See ‘StarsPort’ documentation for more information.

### `setContrast((Stars)arg1, (float)contrast[, (Anim)animator]) -> None`

Setter for property contrast

**Parameters:**
- contrast (double) – Contrast. Only with Gaia model
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setDefaultLabelIntensity((Stars)arg1, (float)defaultLabelIntensity[, (Anim)animator]) -> None`

Setter for property defaultLabelIntensity

**Parameters:**
- defaultLabelIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setExposure((Stars)arg1, (float)exposure[, (Anim)animator]) -> None`

Setter for property exposure

**Parameters:**
- exposure (double) – Exposure. Only with Gaia model
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setFilterHighlight((Stars)arg1, (bool)filterHighlight) -> None`

Setter for property filterHighlight

**Parameters:**
- filterHighlight (bool) – ON: higlight stars passing filter. OFF: hide stars not passing filter. Only with Gaia model

### `setHybridRatio((Stars)arg1, (float)hybridRatio[, (Anim)animator]) -> None`

Setter for property hybridRatio

**Parameters:**
- hybridRatio (double) – Used to define which device will display the star catalog. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setIntensity((Stars)arg1, (float)intensity[, (Anim)animator]) -> None`

Setter for property intensity

**Parameters:**
- intensity (double) – Intensity of the star catalog. Usually in range [0;1].
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setModelset((Stars)arg1, (Stars.Modelset)modelset) -> None`

Setter for property modelset

**Parameters:**
- modelset (Modelset) – Modelset (Hipparcos, GaiaDR2).

### `setMotionVectorIntensity((Stars)arg1, (float)motionVectorIntensity[, (Anim)animator]) -> None`

Setter for property motionVectorIntensity

**Parameters:**
- motionVectorIntensity (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMotionVectorThickness((Stars)arg1, (float)motionVectorThickness[, (Anim)animator]) -> None`

Setter for property motionVectorThickness

**Parameters:**
- motionVectorThickness (double)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setMotionVectorTrail((Stars)arg1, (float)motionVectorTrail[, (Anim)animator]) -> None`

Setter for property motionVectorTrail

**Parameters:**
- motionVectorTrail (double) – Length of the trail in years representing proper motion (default is 25800)
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setPointSaturation((Stars)arg1, (float)pointSaturation[, (Anim)animator]) -> None`

Setter for property pointSaturation

**Parameters:**
- pointSaturation (double) – Change stars dot saturation.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setProperMotion((Stars)arg1, (bool)properMotion[, (Anim)animator]) -> None`

Setter for property properMotion

**Parameters:**
- properMotion (bool) – Turn ON/OFF the proper motion
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setProperMotionOffset((Stars)arg1, (float)properMotionOffset[, (Anim)animator]) -> None`

Setter for property properMotionOffset

**Parameters:**
- properMotionOffset (double) – Set up the time offset of proper motion (in years). Automatically enable or disable the proper motion
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setProperMotionOffsetInYears((Stars)arg1, (float)properMotionOffsetInYears[, (Anim)animator]) -> None`

Setter for property properMotionOffsetInYears

**Parameters:**
- properMotionOffsetInYears (double) – Set up the time offset of proper motion (in years). Require to manually activate the proper motion first
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setRealTwinklingAmplitude((Stars)arg1, (float)realTwinklingAmplitude[, (Anim)animator]) -> None`

Setter for property realTwinklingAmplitude

**Parameters:**
- realTwinklingAmplitude (double) – Real twinkling amplitude of stars without pre-treatment.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setTwinklingAmplitude((Stars)arg1, (float)twinklingAmplitude[, (Anim)animator]) -> None`

Setter for property twinklingAmplitude

**Parameters:**
- twinklingAmplitude (double) – Twinkling amplitude of stars. Be carefull, if set to 0, stars will stop twinkling immediatly.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setUseHybridRatio((Stars)arg1, (float)useHybridRatio[, (Anim)animator]) -> None`

Setter for property useHybridRatio

**Parameters:**
- useHybridRatio (double) – Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setVariability((Stars)arg1, (bool)variability[, (Anim)animator]) -> None`

Setter for property variability

**Parameters:**
- variability (bool) – Activate or not the variability of stars.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property contrast`

Contrast. Only with Gaia model

### property: `property defaultLabelIntensity`

None( (skyExplorer.Stars)arg1) -> float

### property: `property exposure`

Exposure. Only with Gaia model

### property: `property filterHighlight`

ON: higlight stars passing filter. OFF: hide stars not passing filter. Only with Gaia model

### property: `property hybridRatio`

Used to define which device will display the star catalog. Set to 0 to use digital device or 1 to use optical device. This value musn’t be used on non hybrid system.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property intensity`

Intensity of the star catalog. Usually in range [0;1].

### property: `property isProperMotionActive`

[Read-only]

Flag use to know if stars proper motion is currently activated.

### property: `property isTwinklingActive`

[Read-only]

Flag use to know if stars twinkling is enabled

### property: `property modelset`

Modelset (Hipparcos, GaiaDR2).

### property: `property motionVectorIntensity`

None( (skyExplorer.Stars)arg1) -> float

### property: `property motionVectorThickness`

None( (skyExplorer.Stars)arg1) -> float

### property: `property motionVectorTrail`

Length of the trail in years representing proper motion (default is 25800)

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property pointSaturation`

Change stars dot saturation.

### property: `property position`

[Read-only]

Position of the star catalog in ICRF coordinate system.

### property: `property properMotion`

Turn ON/OFF the proper motion

### property: `property properMotionOffset`

Set up the time offset of proper motion (in years). Automatically enable or disable the proper motion

### property: `property properMotionOffsetInYears`

Set up the time offset of proper motion (in years). Require to manually activate the proper motion first

### property: `property realTwinklingAmplitude`

Real twinkling amplitude of stars without pre-treatment.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property twinklingAmplitude`

Twinkling amplitude of stars. Be carefull, if set to 0, stars will stop twinkling immediatly.

### property: `property useHybridRatio`

Used to define how value will be handled. Set to 0 to let the system choose the device or to 1 to manually choose the device (using ‘hybrid ratio’ value). This value musn’t be used on non hybrid system.

### property: `property variability`

Activate or not the variability of stars.

---

# skyExplorer.Universe

## class skyExplorer.Universe

### class UniverseName

InvalidUniverse

MainUniverse

UniverseCount

### `object2objectMatrix((Universe)arg1, (int)src, (int)dest) -> Mat4x4`

Returns the matrix that translate position in src cordinate system to destination cordinate system.

**Parameters:**
- src (int)
- dest (int)

### `setGamma((Universe)arg1, (Vec3)gamma[, (Anim)animator]) -> None`

Setter for property gamma

**Parameters:**
- gamma (Vec3) – Global gamma filter of the scene graph.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGlobalIntensity((Universe)arg1, (float)globalIntensity[, (Anim)animator]) -> None`

Setter for property globalIntensity

**Parameters:**
- globalIntensity (double) – Global intensity of the scene graph.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setGlobalIntensityAv((Universe)arg1, (float)globalIntensityAv[, (Anim)animator]) -> None`

Setter for property globalIntensityAv

**Parameters:**
- globalIntensityAv (double) – Global intensity of the scene graph in the AV layer.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setHsv((Universe)arg1, (Vec3)hsv[, (Anim)animator]) -> None`

Setter for property hsv

**Parameters:**
- hsv (Vec3) – Global HSV filter of the scene graph.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setVibrance((Universe)arg1, (float)vibrance[, (Anim)animator]) -> None`

Setter for property vibrance

**Parameters:**
- vibrance (double) – Global vibrance of the scene graph.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### property: `property gamma`

Global gamma filter of the scene graph.

### property: `property globalIntensity`

Global intensity of the scene graph.

### property: `property globalIntensityAv`

Global intensity of the scene graph in the AV layer.

### property: `property hsv`

Global HSV filter of the scene graph.

### property: `property id`

Returns the osgId. DEPRECATED: please use osgId instead.

### property: `property name`

Returns the name.

### property: `property osgId`

Returns the osgId.

### property: `property reserved`

Indicates whether the body is reserved for system use. Returns true if reserved, false otherwise.

### property: `property vibrance`

Global vibrance of the scene graph.

---

# skyExplorer.Vec

## attribute: `skyExplorer.Vec`

alias of Vec3

---

# skyExplorer.Vec2

## class skyExplorer.Vec2

2D vector of doubles.

### `distanceToLine((Vec2)arg1, (Vec2)point, (Vec2)direction) -> float`

Returns distance to a line (defined by a point and a direction)

### `distanceToPoint((Vec2)arg1, (Vec2)point) -> float`

Returns distance from a given Vec2.

### `dot((Vec2)arg1, (Vec2)vec) -> float`

Returns dot (scalar) product with a given Vec2.

### `isNull((Vec2)arg1) -> bool`

Returns true all components (x, y) are zero. Otherwise, returns false.

### `length((Vec2)arg1) -> float`

Returns length.

### `lengthSquared((Vec2)arg1) -> float`

Returns squared length.

### `normalize((Vec2)arg1) -> None`

Normalizes vector.

### `normalized((Vec2)arg1) -> Vec2`

Returns a normalized copy of the vector.

### `toVec((Vec2)arg1) -> Vec3`

[deprecated] Please prefer toVec3 over toVec.

### `toVec3((Vec2)arg1) -> Vec3`

Conversion to Vec3.

### `toVec4((Vec2)arg1) -> Vec4`

Conversion to Vec4.

### property: `property x`

None( (skyExplorer.Vec2)arg1) -> float

### property: `property y`

None( (skyExplorer.Vec2)arg1) -> float

---

# skyExplorer.Vec3

## class skyExplorer.Vec3

3D vector of doubles.

### `cross((Vec3)arg1, (Vec3)vec) -> Vec3`

Returns cross product with a given Vec3.

### `distanceToPoint((Vec3)arg1, (Vec3)point) -> float`

Returns distance from a given Vec3.

### `dot((Vec3)arg1, (Vec3)vec) -> float`

Returns dot (scalar) product with a given Vec3.

### `isNull((Vec3)arg1) -> bool`

Returns true all components (x, y, z) are zero. Otherwise, returns false.

### `length((Vec3)arg1) -> float`

Returns length.

### `lengthSquared((Vec3)arg1) -> float`

Returns squared length.

### `normalize((Vec3)arg1) -> None`

Normalizes vector.

### `normalized((Vec3)arg1) -> Vec3`

Returns a normalized copy of the vector.

### `toVec2((Vec3)arg1) -> Vec2`

Conversion to Vec2.

### `toVec4((Vec3)arg1) -> Vec4`

Conversion to Vec4.

### property: `property x`

None( (skyExplorer.Vec3)arg1) -> float

### property: `property y`

None( (skyExplorer.Vec3)arg1) -> float

### property: `property z`

None( (skyExplorer.Vec3)arg1) -> float

---

# skyExplorer.Vec4

## class skyExplorer.Vec4

4D vector of doubles.

### `dot((Vec4)arg1, (Vec4)vec) -> float`

Returns dot (scalar) product with a given Vec4.

### `isNull((Vec4)arg1) -> bool`

Returns true all components (x, y, z, w) are zero. Otherwise, returns false.

### `length((Vec4)arg1) -> float`

Returns length.

### `lengthSquared((Vec4)arg1) -> float`

Returns squared length.

### `normalize((Vec4)arg1) -> None`

Normalizes vector.

### `normalized((Vec4)arg1) -> Vec4`

Returns a normalized copy of the vector.

### `toVec((Vec4)arg1) -> Vec3`

[deprecated] Please prefer toVec3 over toVec.

### `toVec2((Vec4)arg1) -> Vec2`

Conversion to Vec2.

### `toVec3((Vec4)arg1) -> Vec3`

Conversion to Vec3.

### property: `property w`

None( (skyExplorer.Vec4)arg1) -> float

### property: `property x`

None( (skyExplorer.Vec4)arg1) -> float

### property: `property y`

None( (skyExplorer.Vec4)arg1) -> float

### property: `property z`

None( (skyExplorer.Vec4)arg1) -> float

---

# skyExplorer.VideoPlayer

## class skyExplorer.VideoPlayer

### class Eye

InvalidEye

Both

Left

Right

### class LoopMode

InvalidLoopMode

NoLoop

RepeatPlayList

RepeateFile

RandomNoRepeat

RandomReapeat

### class SpeedMode

InvalidSpeedMode

PauseSpeed

QuarterSpeed

HalfSpeed

NormalSpeed

DoubleSpeed

FourSpeed

### class VideoState

InvalidVideoState

LegacyInvalidState

UnloadedState

StopState

PlayState

PauseState

### `load((VideoPlayer)arg1, (object)filename, (Anim)anim, (VideoPlayer.Eye)eye) -> None`

Load a video file in viPlayer mode.

**Parameters:**
- filename (str) – Video file path to load. Must be relative to user folder.
- anim (Anim, optional) – defaults to Anim()
- eye (Eye, optional) – defaults to Both

### `loadSubtitle((VideoPlayer)arg1, (object)filename, (Anim)anim) -> None`

Load a subtitle file.

**Parameters:**
- filename (str) – Subtitle file path to load. Must be relative to user folder.
- anim (Anim, optional) – defaults to Anim()

### `pause((VideoPlayer)arg1) -> None`

Pause the current playing video. Has no effect if no video is currently loaded.

### `play((VideoPlayer)arg1, (Anim)anim) -> None`

Play the current video file. The function load must have been called previously.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `reset((VideoPlayer)arg1, (Anim)anim) -> None`

Reset the video player. Playing video will be stop, all video file will be unloaded and opacity set to 0.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `seek((VideoPlayer)arg1, (float)time, (Anim)anim) -> None`

Change the current playing position in the video.

**Parameters:**
- time (double) – Position to reach in the video file (in seconds).
- anim (Anim, optional) – defaults to Anim()

### `setOpacity((VideoPlayer)arg1, (float)opacity[, (Anim)animator]) -> None`

Setter for property opacity

**Parameters:**
- opacity (double) – Opacity of the video player. Set to 0 to see SkyExplorer view, and to 1 to see video player.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `setVolume((VideoPlayer)arg1, (float)volume[, (Anim)animator]) -> None`

Setter for property volume

**Parameters:**
- volume (double) – Audo volume of current video if they have audio track [0 1] default 0.
- animator (Anim, optional) – Anim used for property interpolation, defaults to Anim()

### `stop((VideoPlayer)arg1, (Anim)anim) -> None`

Stops the current playing video.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### `unLoad((VideoPlayer)arg1, (Anim)anim) -> None`

Unload a video file in viPlayer.

**Parameters:**
- anim (Anim, optional) – defaults to Anim()

### property: `property duration`

[Read-only]

Current video state of the player. See ‘VideoState’ enumeration documentation for available values.

### property: `property loopMode`

[Read-only]

Current loop mode of the video player. See ‘LoopMode’ enumeration documentation for available values.

### property: `property opacity`

Opacity of the video player. Set to 0 to see SkyExplorer view, and to 1 to see video player.

### property: `property position`

[Read-only]

Current video length.

### property: `property speedMode`

[Read-only]

Current speed mode of the video player. See ‘SpeedMode’ enumeration documentation for available values.

### property: `property state`

[Read-only]

Current video state of the player. See ‘VideoState’ enumeration documentation for available values.

### property: `property videoFile`

[Read-only]

Current video player loaded video file.

### property: `property videoStartTime`

[Read-only]

Time at which the video starts to play.

### property: `property volume`

Audo volume of current video if they have audio track [0 1] default 0.

---

# studio 모듈

## Classes

| Class | Description |
|---|---|
| `studio.Action` |  |
| `studio.AdvancedCamera` | Use advanced camera to make smart movements. |
| `studio.AudienceResponseSystem` | Main class to manage votes in python scripts |
| `studio.Configuration` |  |
| `studio.Data` |  |
| `studio.DataManager` |  |
| `studio.QObject` |  |
| `studio.ShowMonitor` |  |
| `studio.Vec2` |  |
| `studio.VotingDevice` |  |

---

# studio.Action

## class studio.Action

### class Type

Invalid

Properties

Clear

Add

Remove

Tag

Untag

Export

Share

Unshare

ShowInFolder

OpenFile

Activate

Load

Apply

Edit

EditStart

EditStop

GoTo

FadeTo

StraightGoTo

ConnectTo

LookAt

GoToPlace

FadeToPlace

FadeToObservation

FadeToDate

FadeToParent

OnOff

On

Off

OrbitOnOff

OrbitOn

OrbitOff

LabelOnOff

LabelOn

LabelOff

PointerOnOff

PointerOn

PointerOff

LineOnOff

LineOn

LineOff

PictureOnOff

PictureOn

PictureOff

BoundaryOnOff

BoundaryOn

BoundaryOff

TrajectoryOnOff

TrajectoryOn

TrajectoryOff

PlayPause

PlayStop

Play

PlayInstant

PlayLoop

PlayAdvanced

Pause

Stop

Start

ScaleUpDown

ScaleUp

ScaleDown

SOS_Update

Page_Open

Page_Edit

Page_Import

### `trigger((Action)arg1) -> None`

Launch corresponding action.

---

# studio.AdvancedCamera

## class studio.AdvancedCamera

Use advanced camera to make smart movements.

### `move((AdvancedCamera)arg1, (Vec2)speed) -> None`

Makes camera moves according to speed vector. The camera movement will continue until stop function is called.

**Parameters:**
- speed (Vec2) – Speed vector of the camera in X and Y coordinate, affected by dynamism.

### `roll((AdvancedCamera)arg1, (float)speed) -> None`

Makes camera roll. The camera movement will continue until stop function is called.

**Parameters:**
- speed (float) – Roll speed of the camera, affected by dynamism.

### `setGuessMode((AdvancedCamera)arg1) -> None`

Let camera to choose the most suitable state.

### `setModeFreeFly((AdvancedCamera)arg1) -> None`

Change camera state to free fly.

### `setModeTerrainView((AdvancedCamera)arg1) -> None`

Change camera state to terrain view.

### `stop((AdvancedCamera)arg1) -> None`

Stop current camera movement. This function must be call after calling One of the following functions : move, zoom, tilt or roll

### `takeOffOn((AdvancedCamera)arg1) -> None`

The camera will automatically choose to take off or on according to it’s position.

### `tilt((AdvancedCamera)arg1, (float)speed) -> None`

Makes camera tilt. The camera movement will continue until stop function is called.

**Parameters:**
- speed (float) – Tilt speed of the camera, affected by dynamism.

### `toggleFreeFlyMode((AdvancedCamera)arg1) -> None`

Toggle camera state from free fly to trackball, or from trackball to free fly

### `zoom((AdvancedCamera)arg1, (float)speed) -> None`

Makes camera get closer to the looking point. The camera movement will continue until stop function is called.

**Parameters:**
- speed (float) – Zoom speed of the camera, affected by dynamism.

---

# studio.AudienceResponseSystem

## class studio.AudienceResponseSystem

Main class to manage votes in python scripts

### `cancelVote((AudienceResponseSystem)arg1) -> None`

Cancel the current playing vote.

Discarding results of the vote.

### `endVote((AudienceResponseSystem)arg1) -> None`

Ends the current playing vote.

### `startVote((AudienceResponseSystem)arg1, (object)vote) -> None`

Load and play a vote (XML format).

**Parameters:**
- vote (str) – Path to the vote file, can be relative to user folder

### `sync((AudienceResponseSystem)arg1) -> None`

### `waitForResponse((AudienceResponseSystem)arg1[, (float)timeout=-1]) -> VotingDevice`

Wait for a response from a voter. WARNING: This method locks current script until a voter gives a response, or timeout is reached.

**Parameters:**
- timeout (double, optional) – Maximum time to wait (s). Negative value means no timeout, defaults to -1

### `waitForVote((AudienceResponseSystem)arg1[, (float)timeout=-1.0]) -> bool`

Wait for a vote in progress. WARNING: This method locks current script until a vote is in progress, or timeout is reached.

**Parameters:**
- timeout (double, optional) – Maximum time to wait (s). Negative value means no timeout, defaults to -1

### `waitReady((AudienceResponseSystem)arg1[, (float)timeout=-1.0]) -> bool`

Wait until a vote can be launched. WARNING: This method locks current script until a vote can be launched, or timeout is reached.

**Parameters:**
- timeout (double, optional) – Maximum time to wait (s). Negative value means no timeout, defaults to -1

### property: `property currentVote`

None( (studio.AudienceResponseSystem)arg1) -> object

### property: `property devices`

None( (studio.AudienceResponseSystem)arg1) -> object

### property: `property synced`

None( (studio.AudienceResponseSystem)arg1) -> bool

### property: `property voteInProgress`

Returns whenever a vote is currently in progress or not.

### property: `property voteReady`

Returns whenever the system is ready to run a new vote or not

---

# studio.Configuration

## class studio.Configuration

### `configuration() -> Configuration`

Reference to the Studio configuration

### `igAddress((Configuration)arg1, (int)arg2) -> object`

Get ip address of the given ig.

**Parameters:**
- igIndex (int) – Index of the ig in configuration ig list. Must be in range [0:igCount-1]

### `igUserFolder((Configuration)arg1, (int)arg2) -> object`

Get user folder location of the given ig (used when deploying files to the system).

**Parameters:**
- igIndex (int) – Index of the ig in configuration ig list. Must be in range [0:igCount-1]

### property: `property igCount`

Number of ig of the system.

### property: `property localUserFolder`

Get the local user folder. (used when deploying files to the system)

---

# studio.Data

## class studio.Data

### class Type

InvalidType

DatumType

SdkObjectType

AstronomicalObjectType

GalaxyType

StarType

PlanetType

SatelliteType

DwarfPlanetType

CometType

AsteroidType

NebulaType

AudioType

FullDomeVideoType

MovieType

TrailerType

ScriptType

SpcType

ConstellationType

DateType

FontType

DeepSkyObjectType

ImageType

ImageStandardType

ImageFisheyeType

ImagePanoramaType

Model3DType

PlaceType

CityType

GenericPlaceType

MountainType

VolcanoType

CraterType

PlanetariumType

SlideShowType

GlobularClusterType

VoteType

QuestionVoteType

QuizzVoteType

Legacy_BuzzerVoteType

DecisionVoteType

ManipulatorVoteType

DatasetType

PythonScriptType

BookmarkType

DrawingType

MessierType

NgcType

GenericGroupType

PatchType

AsterismType

ShootingStarType

JPLHorizonsType

SkySurveyType

DatasetGroupType

Model3DAstroType

JsScriptType

SkyQualityType

BolideType

StarColorsType

StarFiltersType

LightType

PluginType

SOSType

PageType

ModuleType

TypeCount

### `action((Data)arg1, (Action.Type)arg2) -> Action`

Return data action according to the action type.

**Parameters:**
- actionType (Action::Type) – Type of the requested action

### `defaultAction((Data)arg1) -> Action`

[Read-only] Default action of the datum.

### property: `property id`

[Read-only] Id of the data in database

---

# studio.DataManager

## class studio.DataManager

### `availableActions((DataManager)arg1, (Data)data) -> None`

Print all available actions for given data to stdout

**Parameters:**
- data (Data) – Data used to print action list.

### `data((DataManager)arg1, (Data.Type)arg2, (object)arg3) -> Data`

Get data from database

**Parameters:**
- type (Data.Type) – Type of requested data. see ‘Data.Type’ documentation for available values.
- name (str) – Name of the requested data. It can be an aproximative name.

### `database() -> DataManager`

Reference to the Studio database

### `lockManipulator((DataManager)arg1, (float)arg2) -> None`

Lock the Studio camera manipulator

**Parameters:**
- duration (double) – Duration to lock manipulator in seconds.

### `unlockManipulator((DataManager)arg1) -> None`

Unlock the Studio camera manipulator

---

# studio.QObject

## class studio.QObject

---

# studio.ShowMonitor

## class studio.ShowMonitor

### class ErrorCode

NoError

CyclicInclusion

FileNotFound

LoadFailed

InstantLoop

### class State

Play

Pause

Stop

### `error((ShowMonitor)arg1, (int)index) -> ShowMonitor.ErrorCode`

Return error code associated with given script.

**Parameters:**
- index (int) – Index of the script to query error.

### `instance() -> ShowMonitor`

Reference to the show monitor

### `resumeScript((ShowMonitor)arg1, (int)index) -> None`

Resume the paused script.

**Parameters:**
- index (int) – Index of the script to resume.

### `scriptState((ShowMonitor)arg1, (int)index) -> ShowMonitor.State`

Get the current state of a running script.

**Parameters:**
- index (int) – Index of the script to query state.

### `stopScript((ShowMonitor)arg1, (int)index) -> None`

Stop a running script.

**Parameters:**
- index (int) – Index of the script to stop.

### property: `property runningSriptCount`

Return the number of currently running scripts

---

# studio.Vec2

## class studio.Vec2

### `normalize((Vec2)arg1) -> None`

### property: `property x`

None( (studio.Vec2)arg1) -> float

### property: `property y`

None( (studio.Vec2)arg1) -> float

---

# studio.VotingDevice

## class studio.VotingDevice

### property: `property id`

None( (studio.VotingDevice)arg1) -> int

### property: `property response`

List of responses from VotingDevice.

Returns a list of boolean representing state of each button

### property: `property responseTime`

Time (s) of the voter response

### property: `property rightResponse`

Does the device response correspond to good answer

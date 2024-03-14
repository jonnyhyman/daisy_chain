"""
    These types describe the DaVinci Resolve Python API
    without implementing any of the methods directly

    For the implementations of remote call executions,
    see the "DaisyChain Host.py"

    For the implementation of remote call requests,
    see the client libraries:
    - `js/daisychain`
    - `lua/daisychain`
    - `python/daisychain`

    Modified directly from [pedrolabonia/pydavinci](https://github.com/pedrolabonia/pydavinci/blob/bd40574085f19245a79111988df171041f530808/pydavinci/wrappers/_resolve_stubs.pyi)
"""

from typing import Any, Dict, List, Optional, Union

class BMD:
    """ BMD UI API functions & types """
    def UIDispatcher(self, ui: "UIManager")->Any: return

class Resolve(object):
    """ Resolve API functions and types """
    def Fusion(self) -> "Fusion": return Fusion()
    def GetMediaStorage(self) -> "MediaStorage": return MediaStorage()
    def GetProjectManager(self) -> "ProjectManager": return ProjectManager()
    def OpenPage(self, pageName: str) -> bool: return bool()
    def GetCurrentPage(self) -> str: return str()
    def GetProductName(self) -> str: return str()
    def GetVersion(self) -> List[Any]: return list()
    def GetVersionString(self) -> str: return str()
    def LoadLayoutPreset(self, presetName: str) -> bool: return bool()
    def UpdateLayoutPreset(self, presetName: str) -> bool: return bool()
    def ExportLayoutPreset(self, presetName: str, presetFilePath: str) -> bool: return bool()
    def DeleteLayoutPreset(self, presetName: str) -> bool: return bool()
    def SaveLayoutPreset(self, presetName: str) -> bool: return bool()
    def ImportLayoutPreset(self, presetFilePath: str, presetName: str) -> bool: return bool()
    def Quit(self) -> None: return None

class ProjectManager(object):
    def CreateProject(self, projectName: str) -> "Project": return Project()
    def DeleteProject(self, projectName: str) -> bool: return bool()
    def LoadProject(self, projectName: str) -> "Project": return Project()
    def GetCurrentProject(self) -> "Project": return Project()
    def SaveProject(self) -> bool: return bool()
    def CloseProject(self, project: "Project") -> bool: return bool()
    def CreateFolder(self, folderName: str) -> bool: return bool()
    def DeleteFolder(self, folderName: str) -> bool: return bool()
    def GetProjectListInCurrentFolder(self) -> List[str]: return list()
    def GetFolderListInCurrentFolder(self) -> List[str]: return list()
    def GotoRootFolder(self) -> bool: return bool()
    def GotoParentFolder(self) -> bool: return bool()
    def GetCurrentFolder(self) -> str: return str()
    def OpenFolder(self, folderName: str) -> bool: return bool()
    def ImportProject(self, filePath: str) -> bool: return bool()
    def ExportProject(self, projectName: str, filePath: str, withStillsAndLUTs: bool) -> bool: return bool()
    def RestoreProject(self, filePath: str) -> bool: return bool()
    def GetCurrentDatabase(self) -> Dict[Any, Any]: return {}
    def GetDatabaseList(self) -> List[Dict[Any, Any]]: return []
    def SetCurrentDatabase(self, dbInfo: Dict[Any, Any]) -> bool: return bool()

class Project(object):
    def GetMediaPool(self) -> "MediaPool": return MediaPool()
    def GetTimelineCount(self) -> int: return int()
    def GetTimelineByIndex(self, idx: int) -> "Timeline": return Timeline()
    def GetCurrentTimeline(self) -> "Timeline": return Timeline()
    def SetCurrentTimeline(self, timeline: "Timeline") -> bool: return bool()
    def GetGallery(self) -> Optional[Any]: return None
    def GetName(self) -> str: return str()
    def SetName(self, projectName: str) -> bool: return bool()
    def GetPresetList(self) -> List[Any]: return list()
    def SetPreset(self, presetName: str) -> bool: return bool()
    def AddRenderJob(self) -> str: return str()
    def DeleteRenderJob(self, jobId: str) -> bool: return bool()
    def DeleteAllRenderJobs(self) -> bool: return bool()
    def GetRenderJobList(self) -> List[Any]: return list()
    def GetRenderPresetList(self) -> List[Any]: return list()
    def StartRendering(self, jobids: Optional[List[str]] = None, isInteractiveMode: bool = False) -> bool: return bool()
    def StopRendering(self) -> None: return None
    def IsRenderingInProgress(self) -> bool: return bool()
    def LoadRenderPreset(self, presetName: str) -> bool: return bool()
    def SaveAsNewRenderPreset(self, presetName: str) -> bool: return bool()
    def SetRenderSettings(self, settings: Dict[Any, Any]) -> bool: return bool()
    def GetRenderJobStatus(self, jobId: str) -> Dict[Any, Any]: return {}
    def GetSetting(self, settingName: Optional[str] = None) -> Any: return {}
    def SetSetting(self, settingName: str, settingValue: Any) -> bool: return bool()
    def GetRenderFormats(self) -> Dict[Any, Any]: return {}
    def GetRenderCodecs(self, renderFormat: str) -> Dict[Any, Any]: return {}
    def GetCurrentRenderFormatAndCodec(self) -> Dict[Any, Any]: return {}
    def SetCurrentRenderFormatAndCodec(self, format: str, codec: str) -> bool: return bool()
    def GetCurrentRenderMode(self) -> int: return int()
    def SetCurrentRenderMode(self, renderMode: int) -> bool: return bool()
    def GetRenderResolutions(self, format: Optional[str] = None, codec: Optional[str] = None) -> List[Dict[Any, Any]]: return []
    def RefreshLUTList(self) -> bool: return bool()

class MediaStorage(object):
    def GetMountedVolumeList(self) -> List[Any]: return list()
    def GetSubFolderList(self, folderPath: str) -> List[Any]: return list()
    def GetFileList(self, folderPath: str) -> List[Any]: return list()
    def RevealInStorage(self, path: str) -> bool: return bool()
    def AddItemListToMediaPool(self, items: List[Any]) -> List[Any]: return list()
    def AddClipMattesToMediaPool(self, MediaPoolItem: "MediaPoolItem", paths: List[Any], stereoEye: str) -> bool: return bool()
    def AddTimelineMattesToMediaPool(self, paths: List[Any]) -> List[Any]: return list()

class MediaPool(object):
    def GetRootFolder(self) -> "Folder": return Folder()
    def AddSubFolder(self, folder: "Folder", name: str) -> "Folder": return Folder()
    def CreateEmptyTimeline(self, name: str) -> "Timeline": return Timeline()
    def AppendToTimeline(self, clips: List["MediaPoolItem"]) -> List["TimelineItem"]: return list()
    def CreateTimelineFromClips(self, name: str, clips: List["MediaPoolItem"]) -> "Timeline": return Timeline()
    def ImportTimelineFromFile(self, filePath: str, options: Optional[Dict[Any, Any]] = None) -> "Timeline": return Timeline()
    def DeleteTimelines(self, timelines: List["Timeline"]) -> bool: return bool()
    def GetCurrentFolder(self) -> "Folder": return Folder()
    def SetCurrentFolder(self, folder: "Folder") -> bool: return bool()
    def DeleteClips(self, clips: List["MediaPoolItem"]) -> bool: return bool()
    def DeleteFolders(self, subfolder: List["Folder"]) -> bool: return bool()
    def MoveClips(self, clips: List["MediaPoolItem"], targetFolder: "Folder") -> bool: return bool()
    def MoveFolders(self, folder: List["Folder"], targetFolder: "Folder") -> bool: return bool()
    def GetClipMatteList(self, MediaPoolItem: "MediaPoolItem") -> List[str]: return list()
    def GetTimelineMatteList(self, folder: "Folder") -> List["MediaPoolItem"]: return list()
    def DeleteClipMattes(self, MediaPoolItem: "MediaPoolItem", paths: List[str]) -> bool: return bool()
    def RelinkClips(self, clips: List["MediaPoolItem"], folderPath: str) -> bool: return bool()
    def UnlinkClips(self, clips: List["MediaPoolItem"]) -> bool: return bool()
    def ImportMedia(self, path: List[str]) -> List["MediaPoolItem"]: return list()
    def ExportMetadata(self, fileName: str, clips: Optional[List["MediaPoolItem"]] = None) -> bool: return bool()

class Folder(object):
    def GetClipList(self) -> List["MediaPoolItem"]: return list()
    def GetName(self) -> str: return str()
    def GetSubFolderList(self) -> List["Folder"]: return list()

class MediaPoolItem(object):
    def GetName(self) -> str: return str()
    def GetMetadata(self, metadataType: Optional[Any] = None) -> Union[Dict[Any, Any], str]: return {} if metadataType is None else str()
    def SetMetadata(self, metadata: Dict[Any, Any]) -> bool: return bool()
    def GetMediaId(self) -> str: return str()
    def AddMarker(self, frameid: int, color: str, name: str, note: str, duration: int, customData: str) -> bool: return bool()
    def GetMarkers(self) -> Dict[Any, Any]: return {}
    def GetMarkerByCustomData(self, customData: str) -> Dict[Any, Any]: return {}
    def UpdateMarkerCustomData(self, frameId: int, customData: str) -> bool: return bool()
    def GetMarkerCustomData(self, frameId: int) -> str: return str()
    def DeleteMarkersByColor(self, color: str) -> bool: return bool()
    def DeleteMarkerAtFrame(self, frameNum: int) -> bool: return bool()
    def DeleteMarkerByCustomData(self, customData: str) -> bool: return bool()
    def AddFlag(self, color: str) -> bool: return bool()
    def GetFlagList(self) -> List[str]: return list()
    def ClearFlags(self, color: str) -> bool: return bool()
    def GetClipColor(self) -> str: return str()
    def SetClipColor(self, colorName: str) -> bool: return bool()
    def ClearClipColor(self) -> bool: return bool()
    def GetClipProperty(self) -> Union[str, Dict[Any, Any]]: return {}  # Modified to fit the context
    def SetClipProperty(self, propertyName: str, propertyValue: Any) -> bool: return bool()
    def LinkProxyMedia(self, proxyMediaFilePath: str) -> bool: return bool()
    def UnlinkProxyMedia(self) -> bool: return bool()
    def ReplaceClip(self, filePath: str) -> bool: return bool()

class Timeline(object):
    def GetName(self) -> str: return str()
    def SetName(self, timelineName: str) -> bool: return bool()
    def GetStartFrame(self) -> int: return int()
    def GetEndFrame(self) -> int: return int()
    def GetTrackCount(self, trackType: str) -> int: return int()
    def GetItemListInTrack(self, trackType: str, index: int) -> List["TimelineItem"]: return list()
    def AddMarker(self, frameid: int, color: str, name: str, note: str, duration: int, customData: str) -> bool: return bool()
    def GetMarkers(self) -> Dict[Any, Any]: return {}
    def GetMarkerByCustomData(self, customData: str) -> Dict[Any, Any]: return {}
    def UpdateMarkerCustomData(self, frameId: int, customData: str) -> bool: return bool()
    def GetMarkerCustomData(self, frameId: int) -> str: return str()
    def DeleteMarkersByColor(self, color: str) -> bool: return bool()
    def DeleteMarkerAtFrame(self, frameNum: int) -> bool: return bool()
    def DeleteMarkerByCustomData(self, customData: str) -> bool: return bool()
    def ApplyGradeFromDRX(self, path: str, gradeMode: int, items: List["TimelineItem"]) -> bool: return bool()
    def GetCurrentTimecode(self) -> str: return str()
    def SetCurrentTimecode(self, timecode: str) -> bool: return bool()
    def GetCurrentVideoItem(self) -> "TimelineItem": return TimelineItem()
    def GetCurrentClipThumbnailImage(self) -> Dict[Any, Any]: return {}
    def GetTrackName(self, trackType: str, trackIndex: int) -> str: return str()
    def SetTrackName(self, trackType: str, trackIndex: int, name: str) -> bool: return bool()
    def DuplicateTimeline(self, timelineName: Optional[str] = None) -> "Timeline": return Timeline()
    def CreateCompoundClip(self, items: List["TimelineItem"], clipinfo: Optional[Dict[Any, Any]] = None) -> "TimelineItem": return TimelineItem()
    def CreateFusionClip(self, items: List["TimelineItem"]) -> "TimelineItem": return TimelineItem()
    def ImportIntoTimeline(self, filePath: str, importOptions: Optional[Dict[Any, Any]] = None) -> bool: return bool()
    def Export(self, fileName: str, exportType: float, exportSubtype: Optional[float] = None) -> bool: return bool()
    def GetSetting(self, settingName: Optional[Union[str, Dict[Any, Any]]] = None) -> Dict[Any, Any]: return {}
    def SetSetting(self, settingName: str, settingValue: Union[str, float, int, Dict[Any, Any]]) -> bool: return bool()
    def InsertGeneratorIntoTimeline(self, generatorName: str) -> "TimelineItem": return TimelineItem()
    def InsertFusionGeneratorIntoTimeline(self, generatorName: str) -> "TimelineItem": return TimelineItem()
    def InsertOFXGeneratorIntoTimeline(self, generatorName: str) -> "TimelineItem": return TimelineItem()
    def InsertTitleIntoTimeline(self, titleName: str) -> "TimelineItem": return TimelineItem()
    def InsertFusionTitleIntoTimeline(self, titleName: str) -> "TimelineItem": return TimelineItem()
    def GrabStill(self) -> Any: return {}
    def GrabAllStills(self, stillFrameSource: int) -> Any: return {}

class TimelineItem(object):
    def GetName(self) -> str: return str()
    def GetDuration(self) -> int: return int()
    def GetEnd(self) -> int: return int()
    def GetFusionCompCount(self) -> int: return int()
    def GetFusionCompByIndex(self, compIndex: int) -> Any: return {}
    def GetFusionCompNameList(self) -> List[str]: return list()
    def GetFusionCompByName(self, compName: str) -> Any: return {}
    def GetLeftOffset(self) -> int: return int()
    def GetRightOffset(self) -> int: return int()
    def GetStart(self) -> int: return int()
    def SetProperty(self, propertyKey: str, propertyValue: Union[str, int, float]) -> bool: return bool()
    def GetProperty(self, propertyKey: Optional[str] = None) -> Dict[Any, Any]: return {}
    def AddMarker(self, frameid: int, color: str, name: str, note: str, duration: int, customData: str) -> bool: return bool()
    def GetMarkers(self) -> Dict[Any, Any]: return {}
    def GetMarkerByCustomData(self, customData: str) -> Dict[Any, Any]: return {}
    def UpdateMarkerCustomData(self, frameId: int, customData: str) -> bool: return bool()
    def GetMarkerCustomData(self, frameId: int) -> str: return str()
    def DeleteMarkersByColor(self, color: str) -> bool: return bool()
    def DeleteMarkerAtFrame(self, frameNum: int) -> bool: return bool()
    def DeleteMarkerByCustomData(self, customData: str) -> bool: return bool()
    def AddFlag(self, color: str) -> bool: return bool()
    def GetFlagList(self) -> List[str]: return list()
    def ClearFlags(self, color: str) -> bool: return bool()
    def GetClipColor(self) -> str: return str()
    def SetClipColor(self, colorName: str) -> bool: return bool()
    def ClearClipColor(self) -> bool: return bool()
    def AddFusionComp(self) -> Any: return {}
    def ImportFusionComp(self, path: str) -> Any: return {}
    def ExportFusionComp(self, path: str, compIndex: int) -> bool: return bool()
    def DeleteFusionCompByName(self, compName: str) -> bool: return bool()
    def LoadFusionCompByName(self, compName: str) -> Any: return {}
    def RenameFusionCompByName(self, oldName: str, newName: str) -> bool: return bool()
    def AddVersion(self, versionName: str, versionType: int) -> bool: return bool()
    def GetCurrentVersion(self) -> Dict[str, int]: return {}
    def DeleteVersionByName(self, versionName: str, versionType: int) -> bool: return bool()
    def LoadVersionByName(self, versionName: str, versionType: int) -> bool: return bool()
    def RenameVersionByName(self, oldName: str, newName: str, versionType: int) -> bool: return bool()
    def GetVersionNameList(self, versionType: int) -> List[str]: return list()
    def GetMediaPoolItem(self) -> "MediaPoolItem": return MediaPoolItem()
    def GetStereoConvergenceValues(self) -> Dict[Any, Any]: return {}
    def GetStereoLeftFloatingWindowParams(self) -> Dict[Any, Any]: return {}
    def GetStereoRightFloatingWindowParams(self) -> Dict[Any, Any]: return {}
    def GetNumNodes(self) -> int: return int()
    def SetLUT(self, nodeIndex: int, lutPath: str) -> bool: return bool()
    def GetLUT(self, nodeIndex: int) -> str: return str()
    def SetCDL(self, cdl: Dict[str, str]) -> bool: return bool()
    def AddTake(self, mediapoolitem: "MediaPoolItem", startFrame: Optional[int] = None, endFrame: Optional[int] = None) -> bool: return bool()
    def GetSelectedTakeIndex(self) -> int: return int()
    def GetTakesCount(self) -> int: return int()
    def GetTakeByIndex(self, idx: int) -> Dict[Any, Any]: return {}
    def DeleteTakeByIndex(self, idx: int) -> bool: return bool()
    def SelectTakeByIndex(self, idx: int) -> bool: return bool()
    def FinalizeTake(self) -> bool: return bool()
    def CopyGrades(self, items: List["TimelineItem"]) -> bool: return bool()

class Timer:

    def Start(self):
        pass

    def Stop(self):
        pass

class UIManager:
    """ TODO: Fill with functions and types of UI Manager """
    
    def VGroup(*args, **kwargs):
        pass

    def Label(*args, **kwargs):
        pass

    def Font(*args, **kwargs):
        pass

    def Timer(*args, **kwargs)->Timer:
        return Timer()

class Fusion:
    """ Fusion API functions and types """
    
    UIManager: UIManager

from typing import Any, List, Optional, Dict, Union
import asyncio
import json

'''
--- RPC Functionality
'''

HOST = "127.0.0.1"
PORT = "65432"

class RPCError(Exception):
    """ Exception raised on RPC Errors """

async def rpc_connection(message):
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(message.encode())
    data = await reader.read(1024)
    writer.close()
    return data.decode()

def rpc_request(rqst):
    rqst = json.dumps(rqst)
    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(rpc_connection(rqst))
    resp = json.loads(resp)
    return resp

def rpc(root:dict, impl:str, *args, **kwargs) -> Any:
    """ Connect to the DaisyChain RPC Host,
        request to execute a command,
        return results or raise errors
    """
    rqst = {
            "root": root,
            "impl": impl,
            "args": list(args),
            "kwgs": dict(kwargs)
    }

    # do request
    resp = rpc_request(rqst)

    # raise errors if they occured
    if resp["error"] is not None:
        raise(RPCError(resp['error']))
    
    # get results
    return resp["value"]

def rpc_init() -> dict:
    ''' 
        Get `resolve` root reference
    '''
    return rpc({}, "daisychain_init")

'''
--- API mirror with types and docstrings
'''

class API_Object:
    '''
        Superclass for API Objects
        to retain object references
        and execute remote functions
    '''
    def __init__(self, object_reference:dict):
        self.root = object_reference

    def rpc(self, impl:str, *args, **kwargs):
        ''' Request `root.impl(*args, **kwargs)` '''
        return rpc(self.root, impl, *args, **kwargs)

class Resolve(API_Object):
    '''
        Resolve API functions and types including various 
        export types for timelines and subtypes for AAF and EDL exports.
    '''
    def fusion(self) -> "Fusion":
        """Returns the Fusion object. Starting point for Fusion scripts."""
        return Fusion(self.rpc("Fusion"))

    def get_media_storage(self) -> "MediaStorage":
        """Returns the media storage object to query and act on media locations."""
        return MediaStorage(self.rpc("GetMediaStorage"))

    def get_project_manager(self) -> "ProjectManager":
        """Returns the project manager object for currently open database."""
        return ProjectManager(self.rpc("GetProjectManager"))

    def open_page(self, page_name: str) -> bool:
        """Switches to indicated page in DaVinci Resolve. Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver")."""
        return self.rpc("OpenPage", page_name)

    def get_current_page(self) -> Optional[str]:
        """Returns the page currently displayed in the main window. Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None)."""
        return self.rpc("GetCurrentPage")

    def get_product_name(self) -> str:
        """Returns product name."""
        return self.rpc("GetProductName")

    def get_version(self) -> List[str]:
        """Returns list of product version fields in [major, minor, patch, build, suffix] format."""
        return self.rpc("GetVersion")

    def get_version_string(self) -> str:
        """Returns product version in "major.minor.patch[suffix].build" format."""
        return self.rpc("GetVersionString")

    def load_layout_preset(self, preset_name: str) -> bool:
        """Loads UI layout from saved preset named 'presetName'."""
        return self.rpc("LoadLayoutPreset", preset_name)

    def update_layout_preset(self, preset_name: str) -> bool:
        """Overwrites preset named 'presetName' with current UI layout."""
        return self.rpc("UpdateLayoutPreset", preset_name)

    def export_layout_preset(self, preset_name: str, preset_file_path: str) -> bool:
        """Exports preset named 'presetName' to path 'presetFilePath'."""
        return self.rpc("ExportLayoutPreset", preset_name, preset_file_path)

    def delete_layout_preset(self, preset_name: str) -> bool:
        """Deletes preset named 'presetName'."""
        return self.rpc("DeleteLayoutPreset", preset_name)

    def save_layout_preset(self, preset_name: str) -> bool:
        """Saves current UI layout as a preset named 'presetName'."""
        return self.rpc("SaveLayoutPreset", preset_name)

    def import_layout_preset(self, preset_file_path: str, preset_name: Optional[str] = None) -> bool:
        """Imports preset from path 'presetFilePath'. The optional argument 'presetName' specifies how the preset shall be named. If not specified, the preset is named based on the filename."""
        return self.rpc("ImportLayoutPreset", preset_file_path, preset_name)

    def quit(self) -> None:
        """Quits the application."""
        self.rpc("Quit")

class Fusion(API_Object):
    """ Fusion API """
    # TODO: port the types and stubs from 
    # https://github.com/EmberLightVFX/BMD-Fusion-Scripting-Stubs
    # or perhaps pulling directly from:
    # https://emberlightvfx.github.io/Fusion-Script-Docs/#/

class MediaStorage(API_Object):
    def get_mounted_volume_list(self) -> List[str]:
        """Returns list of folder paths corresponding to mounted volumes displayed in Resolve's Media Storage."""
        return self.rpc("GetMountedVolumeList")

    def get_subfolder_list(self, folder_path: str) -> List[str]:
        """Returns list of absolute folder paths in the given absolute folder path."""
        return self.rpc("GetSubFolderList", folder_path)

    def get_file_list(self, folder_path: str) -> List[str]:
        """Returns list of media and file listings in the given absolute folder path. Note that media listings may be logically consolidated entries."""
        return self.rpc("GetFileList", folder_path)

    def reveal_in_storage(self, path: str) -> bool:
        """Expands and displays given file/folder path in Resolve's Media Storage."""
        return self.rpc("RevealInStorage", path)

    def add_item_list_to_media_pool(self, *items: str) -> List["MediaPoolItem"]:
        """Adds specified file/folder paths from Media Storage into current Media Pool folder. Input is one or more file/folder paths. Returns a list of the MediaPoolItems created."""
        return [MediaPoolItem(item) for item in self.rpc("AddItemListToMediaPool", list(items))]

    def add_clip_mattes_to_media_pool(self, media_pool_item: "MediaPoolItem", paths: List[str], stereo_eye: Optional[str] = None) -> bool:
        """Adds specified media files as mattes for the specified MediaPoolItem. StereoEye is an optional argument for specifying which eye to add the matte to for stereo clips ("left" or "right"). Returns True if successful."""
        return self.rpc("AddClipMattesToMediaPool", media_pool_item, paths, stereo_eye)

    def add_timeline_mattes_to_media_pool(self, paths: List[str]) -> List["MediaPoolItem"]:
        """Adds specified media files as timeline mattes in current media pool folder. Returns a list of created MediaPoolItems."""
        return [MediaPoolItem(item) for item in self.rpc("AddTimelineMattesToMediaPool", paths)]


class MediaPoolFolder(API_Object):
    def get_clip_list(self) -> List["MediaPoolItem"]:
        """Returns a list of clips (items) within the folder."""
        return [MediaPoolItem(item) for item in self.rpc("GetClipList")]

    def get_name(self) -> str:
        """Returns the media folder name."""
        return self.rpc("GetName")

    def get_subfolder_list(self) -> List["MediaPoolFolder"]:
        """Returns a list of subfolders in the folder."""
        return [MediaPoolFolder(folder) for folder in self.rpc("GetSubFolderList")]

    def get_is_folder_stale(self) -> bool:
        """Returns true if folder is stale in collaboration mode, false otherwise."""
        return self.rpc("GetIsFolderStale")

    def get_unique_id(self) -> str:
        """Returns a unique ID for the media pool folder. Added in Resolve 18."""
        return self.rpc("GetUniqueId")

class ProjectManager(API_Object):

    def archive_project(
        self,
        project_name: str,
        file_path: str,
        is_archive_src_media: bool = False,
        is_archive_render_cache: bool = False,
        is_archive_proxy_media: bool = False,
    ) -> bool:
        """Archives project to provided file path with the configuration as provided by the optional arguments."""
        return self.rpc(
            "ArchiveProject",
            project_name,
            file_path,
            is_archive_src_media,
            is_archive_render_cache,
            is_archive_proxy_media,
        )

    def create_project(self, project_name: str) -> Optional["Project"]:
        """Creates and returns a project if projectName (string) is unique, and None if it is not."""
        project = self.rpc("CreateProject", project_name)
        return Project(project) if project else None

    def delete_project(self, project_name: str) -> bool:
        """Delete project in the current folder if not currently loaded."""
        return self.rpc("DeleteProject", project_name)

    def load_project(self, project_name: str) -> Optional["Project"]:
        """Loads and returns the project with name = projectName (string) if there is a match found, and None if there is no matching Project."""
        project = self.rpc("LoadProject", project_name)
        return Project(project) if project else None

    def get_current_project(self) -> "Project":
        """Returns the currently loaded Resolve project."""
        return Project(self.rpc("GetCurrentProject"))

    def save_project(self) -> bool:
        """Saves the currently loaded project with its own name. Returns True if successful."""
        return self.rpc("SaveProject")

    def close_project(self, project: "Project") -> bool:
        """Closes the specified project without saving."""
        return self.rpc("CloseProject", project)

    def create_folder(self, folder_name: str) -> bool:
        """Creates a folder if folderName (string) is unique."""
        return self.rpc("CreateFolder", folder_name)

    def delete_folder(self, folder_name: str) -> bool:
        """Deletes the specified folder if it exists. Returns True in case of success."""
        return self.rpc("DeleteFolder", folder_name)

    def get_project_list_in_current_folder(self) -> List[str]:
        """Returns a list of project names in current folder."""
        return self.rpc("GetProjectListInCurrentFolder")

    def get_folder_list_in_current_folder(self) -> List[str]:
        """Returns a list of folder names in current folder."""
        return self.rpc("GetFolderListInCurrentFolder")

    def goto_root_folder(self) -> bool:
        """Opens root folder in database."""
        return self.rpc("GotoRootFolder")

    def goto_parent_folder(self) -> bool:
        """Opens parent folder of current folder in database if current folder has parent."""
        return self.rpc("GotoParentFolder")

    def get_current_folder(self) -> str:
        """Returns the current folder name."""
        return self.rpc("GetCurrentFolder")

    def open_folder(self, folder_name: str) -> bool:
        """Opens folder under given name."""
        return self.rpc("OpenFolder", folder_name)

    def import_project(self, file_path: str, name: Optional[str] = None) -> bool:
        """Imports a project from the file path provided with given project name, if any. Returns True if successful."""
        return self.rpc("ImportProject", file_path, name)

    def export_project(self, project_name: str, file_path: str, with_stills_and_luts: bool = True) -> bool:
        """Exports project to provided file path, including stills and LUTs if withStillsAndLUTs is True (enabled by default). Returns True in case of success."""
        return self.rpc("ExportProject", project_name, file_path, with_stills_and_luts)

    def restore_project(self, file_path: str, name: Optional[str] = None) -> bool:
        """Restores a project from the file path provided with given project name, if any. Returns True if successful."""
        return self.rpc("RestoreProject", file_path, name)

    def get_current_database(self) -> Dict[str, str]:
        """Returns a dictionary (with keys 'DbType', 'DbName' and optional 'IpAddress') corresponding to the current database connection."""
        return self.rpc("GetCurrentDatabase")

    def get_database_list(self) -> List[Dict[str, str]]:
        """Returns a list of dictionary items (with keys 'DbType', 'DbName' and optional 'IpAddress') corresponding to all the databases added to Resolve."""
        return self.rpc("GetDatabaseList")

    def set_current_database(self, db_info: Dict[str, str]) -> bool:
        """Switches current database connection to the database specified by the keys below, and closes any open project."""
        return self.rpc("SetCurrentDatabase", db_info)

class Project(API_Object):

    def get_media_pool(self) -> "MediaPool":
        """Returns the Media Pool object."""
        return MediaPool(self.rpc("GetMediaPool"))

    def get_timeline_count(self) -> int:
        """Returns the number of timelines currently present in the project."""
        return self.rpc("GetTimelineCount")

    # def get_timeline_by_index(self, idx: int) -> "Timeline":
    #     """Returns timeline at the given index, 1 <= idx <= project.GetTimelineCount()."""
    #     return Timeline(self.rpc("GetTimelineByIndex", idx))
    #
    # def get_current_timeline(self) -> "Timeline":
    #     """Returns the currently loaded timeline."""
    #     return Timeline(self.rpc("GetCurrentTimeline"))
    #
    # def set_current_timeline(self, timeline: "Timeline") -> bool:
    #     """Sets given timeline as current timeline for the project. Returns True if successful."""
    #     return self.rpc("SetCurrentTimeline", timeline)
    #
    # def get_gallery(self) -> "Gallery":
    #     """Returns the Gallery object."""
    #     return Gallery(self.rpc("GetGallery"))
    #
    def get_name(self) -> str:
        """Returns project name."""
        return self.rpc("GetName")

    def set_name(self, project_name: str) -> bool:
        """Sets project name if given projectname (string) is unique."""
        return self.rpc("SetName", project_name)

    def get_preset_list(self) -> List[Dict[str, Union[str, int]]]:
        """Returns a list of presets and their information."""
        return self.rpc("GetPresetList")

    def set_preset(self, preset_name: str) -> bool:
        """Sets preset by given presetName (string) into project."""
        return self.rpc("SetPreset", preset_name)

    def add_render_job(self) -> str:
        """Adds a render job based on current render settings to the render queue. Returns a unique job id (string) for the new render job."""
        return self.rpc("AddRenderJob")

    def delete_render_job(self, job_id: str) -> bool:
        """Deletes render job for input job id (string)."""
        return self.rpc("DeleteRenderJob", job_id)

    def delete_all_render_jobs(self) -> bool:
        """Deletes all render jobs in the queue."""
        return self.rpc("DeleteAllRenderJobs")

    # def get_render_job_list(self) -> List["RenderJob"]:
    #     """Returns a list of render jobs and their information."""
    #     return [RenderJob(job) for job in self.rpc("GetRenderJobList")]
    #
    def get_render_preset_list(self) -> List[str]:
        """Returns a list of render presets and their information."""
        return self.rpc("GetRenderPresetList")

    def start_rendering(self, *job_ids: str, is_interactive_mode: bool = False) -> bool:
        """Starts rendering jobs indicated by the input job ids."""
        return self.rpc("StartRendering", list(job_ids), is_interactive_mode)

    def stop_rendering(self) -> None:
        """Stops any current render processes."""
        self.rpc("StopRendering")

    def is_rendering_in_progress(self) -> bool:
        """Returns True if rendering is in progress."""
        return self.rpc("IsRenderingInProgress")

    def load_render_preset(self, preset_name: str) -> bool:
        """Sets a preset as current preset for rendering if presetName (string) exists."""
        return self.rpc("LoadRenderPreset", preset_name)

    def save_as_new_render_preset(self, preset_name: str) -> bool:
        """Creates new render preset by given name if presetName(string) is unique."""
        return self.rpc("SaveAsNewRenderPreset", preset_name)

    def set_render_settings(self, settings: Dict[str, Union[str, int, bool]]) -> bool:
        """Sets given settings for rendering. Settings is a dict, with support for the keys specified in the RenderSetting class."""
        return self.rpc("SetRenderSettings", settings)

    # def get_render_job_status(self, job_id: str) -> "RenderJobStatus":
    #     """Returns a dict with job status and completion percentage of the job by given jobId (string)."""
    #     return RenderJobStatus(self.rpc("GetRenderJobStatus", job_id))
    #
    def get_setting(self, setting_name: Optional[str] = None) -> Union[Dict[str, Union[str, int, bool]], str, int, bool]:
        """Returns value of project setting (indicated by settingName, string). Check the ProjectSetting class for more information."""
        if setting_name is None:
            return self.rpc("GetSetting")
        else:
            return self.rpc("GetSetting", setting_name)

    def set_setting(self, setting_name: str, setting_value: Union[str, int, bool]) -> bool:
        """Sets the project setting (indicated by settingName, string) to the value (settingValue, string). Check the ProjectSetting class for more information."""
        return self.rpc("SetSetting", setting_name, setting_value)

    def get_render_formats(self) -> Dict[str, str]:
        """Returns a dict (format -> file extension) of available render formats."""
        return self.rpc("GetRenderFormats")

    def get_render_codecs(self, render_format: str) -> Dict[str, str]:
        """Returns a dict (codec description -> codec name) of available codecs for given render format (string)."""
        return self.rpc("GetRenderCodecs", render_format)

    def get_current_render_format_and_codec(self) -> Dict[str, str]:
        """Returns a dict with currently selected format 'format' and render codec 'codec'."""
        return self.rpc("GetCurrentRenderFormatAndCodec")

    def set_current_render_format_and_codec(self, format: str, codec: str) -> bool:
        """Sets given render format (string) and render codec (string) as options for rendering."""
        return self.rpc("SetCurrentRenderFormatAndCodec", format, codec)

    def get_current_render_mode(self) -> int:
        """Returns the render mode: 0 - Individual clips, 1 - Single clip."""
        return self.rpc("GetCurrentRenderMode")

    def set_current_render_mode(self, render_mode: int) -> bool:
        """Sets the render mode. Specify renderMode = 0 for Individual clips, 1 for Single clip."""
        return self.rpc("SetCurrentRenderMode", render_mode)

    def get_render_resolutions(self, format: str, codec: str) -> List[Dict[str, int]]:
        """Returns list of resolutions applicable for the given render format (string) and render codec (string). Returns full list of resolutions if no argument is provided. Each element in the list is a dictionary with 2 keys "Width" and "Height"."""
        return self.rpc("GetRenderResolutions", format, codec)

    def refresh_lut_list(self) -> bool:
        """Refreshes LUT List."""
        return self.rpc("RefreshLUTList")

    def get_unique_id(self) -> str:
        """Returns a unique ID for the project item. Added in Resolve 18."""
        return self.rpc("GetUniqueId")

    def insert_audio_to_current_track_at_playhead(self, media_path: str, start_offset_in_samples: int, duration_in_samples: int) -> bool:
        """Inserts the media specified by mediaPath (string) with startOffsetInSamples (int) and durationInSamples (int) at the playhead on a selected track on the Fairlight page. Returns True if successful, otherwise False."""
        return self.rpc("InsertAudioToCurrentTrackAtPlayhead", media_path, start_offset_in_samples, duration_in_samples)

class MediaPool(API_Object):
    def get_root_folder(self) -> "MediaPoolFolder":
        """Returns root Folder of Media Pool."""
        return MediaPoolFolder(self.rpc("GetRootFolder"))

    def add_sub_folder(self, folder: "MediaPoolFolder", name: str) -> "MediaPoolFolder":
        """Adds new subfolder under specified Folder object with the given name."""
        return MediaPoolFolder(self.rpc("AddSubFolder", folder, name))

    def refresh_folders(self) -> bool:
        """Updates the folders in collaboration mode."""
        return self.rpc("RefreshFolders")

    # def create_empty_timeline(self, name: str) -> "Timeline":
    #     """Adds new timeline with given name."""
    #     return Timeline(self.rpc("CreateEmptyTimeline", name))
    #
    # def append_to_timeline(self, *clips: "MediaPoolItem") -> List["TimelineItem"]:
    #     """Appends specified MediaPoolItem objects in the current timeline. Returns the list of appended timelineItems."""
    #     return [TimelineItem(item) for item in self.rpc("AppendToTimeline", list(clips))]
    #
    # def create_timeline_from_clips(self, name: str, *clips: "MediaPoolItem") -> "Timeline":
    #     """Creates new timeline with specified name, and appends the specified MediaPoolItem objects."""
    #     return Timeline(self.rpc("CreateTimelineFromClips", name, list(clips)))
    #
    # def import_timeline_from_file(self, file_path: str, import_options: Dict[str, Any]) -> "Timeline":
    #     """Creates timeline based on parameters within given file and optional importOptions dict."""
    #     return Timeline(self.rpc("ImportTimelineFromFile", file_path, import_options))
    #
    # def delete_timelines(self, timelines: List["Timeline"]) -> bool:
    #     """Deletes specified timelines in the media pool."""
    #     return self.rpc("DeleteTimelines", timelines)
    #
    def get_current_folder(self) -> "MediaPoolFolder":
        """Returns currently selected Folder."""
        return MediaPoolFolder(self.rpc("GetCurrentFolder"))

    def set_current_folder(self, folder: "MediaPoolFolder") -> bool:
        """Sets current folder by given Folder."""
        return self.rpc("SetCurrentFolder", folder)

    def delete_clips(self, clips: List["MediaPoolItem"]) -> bool:
        """Deletes specified clips or timeline mattes in the media pool."""
        return self.rpc("DeleteClips", clips)

    def delete_folders(self, subfolders: List["MediaPoolFolder"]) -> bool:
        """Deletes specified subfolders in the media pool."""
        return self.rpc("DeleteFolders", subfolders)

    def move_clips(self, clips: List["MediaPoolItem"], target_folder: "MediaPoolFolder") -> bool:
        """Moves specified clips to target folder."""
        return self.rpc("MoveClips", clips, target_folder)

    def move_folders(self, folders: List["MediaPoolFolder"], target_folder: "MediaPoolFolder") -> bool:
        """Moves specified folders to target folder."""
        return self.rpc("MoveFolders", folders, target_folder)

    def get_clip_matte_list(self, media_pool_item: "MediaPoolItem") -> List[str]:
        """Get mattes for specified MediaPoolItem, as a list of paths to the matte files."""
        return self.rpc("GetClipMatteList", media_pool_item)

    def get_timeline_matte_list(self, folder: "MediaPoolFolder") -> List["MediaPoolItem"]:
        """Get mattes in specified Folder, as list of MediaPoolItems."""
        return [MediaPoolItem(item) for item in self.rpc("GetTimelineMatteList", folder)]

    def delete_clip_mattes(self, media_pool_item: "MediaPoolItem", paths: List[str]) -> bool:
        """Delete mattes based on their file paths, for specified MediaPoolItem. Returns True on success."""
        return self.rpc("DeleteClipMattes", media_pool_item, paths)

    def relink_clips(self, media_pool_items: List["MediaPoolItem"], folder_path: str) -> bool:
        """Update the folder location of specified media pool clips with the specified folder path."""
        return self.rpc("RelinkClips", media_pool_items, folder_path)

    def unlink_clips(self, media_pool_items: List["MediaPoolItem"]) -> bool:
        """Unlink specified media pool clips."""
        return self.rpc("UnlinkClips", media_pool_items)

    def import_media(self, items: List[str]) -> List["MediaPoolItem"]:
        """Imports specified file/folder paths into current Media Pool folder. Input is an array of file/folder paths. Returns a list of the MediaPoolItems created."""
        return [MediaPoolItem(item) for item in self.rpc("ImportMedia", items)]

    def export_metadata(self, file_name: str, clips: List["MediaPoolItem"]) -> bool:
        """Exports metadata of specified clips to 'fileName' in CSV format. If no clips are specified, all clips from media pool will be used."""
        return self.rpc("ExportMetadata", file_name, clips)

    def get_unique_id(self) -> str:
        """Returns a unique ID for the media pool. Added in Resolve 18."""
        return self.rpc("GetUniqueId")

class MediaPoolItem(API_Object):
    def get_name(self) -> str:
        """Returns the clip name."""
        return self.rpc("GetName")

    def get_metadata(self, metadata_type: Optional[str] = None) -> Union[Dict[str, str], str]:
        """Returns the metadata value for the key 'metadataType'. If no argument is specified, a dict of all set metadata properties is returned."""
        if metadata_type is None:
            return self.rpc("GetMetadata")
        else:
            return self.rpc("GetMetadata", metadata_type)

    def set_metadata(self, metadata_type: Optional[str] = None, metadata_value: Optional[str] = None, meta_data: Optional[Dict[str, str]] = None) -> bool:
        """Sets the given metadata to metadataValue (string). Returns True if successful."""
        if metadata_type is not None and metadata_value is not None:
            return self.rpc("SetMetadata", metadata_type, metadata_value)
        elif meta_data is not None:
            return self.rpc("SetMetadata", meta_data)
        else:
            raise ValueError("Either metadata_type and metadata_value, or meta_data must be provided.")

    def get_media_id(self) -> str:
        """Returns the unique ID for the MediaPoolItem."""
        return self.rpc("GetMediaId")

    def add_marker(self, frame_id: int, color: str, name: str, note: str, duration: int, custom_data: str) -> bool:
        """Creates a new marker at given frameId position and with given marker information. 'customData' is optional and helps to attach user specific data to the marker."""
        return self.rpc("AddMarker", frame_id, color, name, note, duration, custom_data)

    def get_markers(self) -> Dict[int, Dict[str, Union[str, int]]]:
        """Returns a dict (frameId -> {information}) of all markers and dicts with their information."""
        return self.rpc("GetMarkers")

    def get_marker_by_custom_data(self, custom_data: str) -> Dict[int, Dict[str, Union[str, int]]]:
        """Returns marker {information} for the first matching marker with specified customData."""
        return self.rpc("GetMarkerByCustomData", custom_data)

    def update_marker_custom_data(self, frame_id: int, custom_data: str) -> bool:
        """Updates customData (string) for the marker at given frameId position. CustomData is not exposed via UI and is useful for scripting developer to attach any user specific data to markers."""
        return self.rpc("UpdateMarkerCustomData", frame_id, custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        """Returns customData string for the marker at given frameId position."""
        return self.rpc("GetMarkerCustomData", frame_id)

    def delete_markers_by_color(self, color: str) -> bool:
        """Delete all markers of the specified color from the media pool item. "All" as argument deletes all color markers."""
        return self.rpc("DeleteMarkersByColor", color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Delete marker at frame number from the media pool item."""
        return self.rpc("DeleteMarkerAtFrame", frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        """Delete first matching marker with specified customData."""
        return self.rpc("DeleteMarkerByCustomData", custom_data)

    def add_flag(self, color: str) -> bool:
        """Adds a flag with given color (string)."""
        return self.rpc("AddFlag", color)

    def get_flag_list(self) -> List[str]:
        """Returns a list of flag colors assigned to the item."""
        return self.rpc("GetFlagList")

    def clear_flags(self, color: str) -> bool:
        """Clears the flag of the given color if one exists. An "All" argument is supported and clears all flags."""
        return self.rpc("ClearFlags", color)

    def get_clip_color(self) -> str:
        """Returns the item color as a string."""
        return self.rpc("GetClipColor")

    def set_clip_color(self, color_name: str) -> bool:
        """Sets the item color based on the colorName (string)."""
        return self.rpc("SetClipColor", color_name)

    def clear_clip_color(self) -> bool:
        """Clears the item color."""
        return self.rpc("ClearClipColor")

    def get_clip_property(self, property_name: Optional[str] = None) -> Union[Dict[str, Union[str, int, bool]], str, int, bool]:
        """Returns the property value for the key 'propertyName'. If no argument is specified, a dict of all clip properties is returned."""
        if property_name is None:
            return self.rpc("GetClipProperty")
        else:
            return self.rpc("GetClipProperty", property_name)

    def set_clip_property(self, property_name: str, property_value: Union[str, int, bool]) -> bool:
        """Sets the given property to propertyValue (string). Check the MediaPoolItemProperties class for more information."""
        return self.rpc("SetClipProperty", property_name, property_value)

    def link_proxy_media(self, proxy_media_file_path: str) -> bool:
        """Links proxy media located at path specified by arg 'proxyMediaFilePath' with the current clip. 'proxyMediaFilePath' should be absolute clip path."""
        return self.rpc("LinkProxyMedia", proxy_media_file_path)

    def unlink_proxy_media(self) -> bool:
        """Unlinks any proxy media associated with clip."""
        return self.rpc("UnlinkProxyMedia")

    def replace_clip(self, file_path: str) -> bool:
        """Replaces the underlying asset and metadata of MediaPoolItem with the specified absolute clip path."""
        return self.rpc("ReplaceClip", file_path)

    def get_unique_id(self) -> str:
        """Returns a unique ID for the media pool item. Added in DaVinci Resolve 18."""
        return self.rpc("GetUniqueId")

# --------------------------
# initialize resolve object
# --------------------------
resolve = Resolve(rpc_init())

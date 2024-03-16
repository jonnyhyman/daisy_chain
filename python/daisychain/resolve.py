from typing import List, Optional, Dict, Union, Any
from daisychain.remote import API_Object
from daisychain.fusion import Fusion

'''
# Resolve API
_Mirror for daisychain remote procedure call with type hints and docstrings_
(for Fusion see fusion.py)

    API_Object Classes
    - ✅ MediaPoolItem
    - ✅ TimelineItem
    - ✅ Timeline
    - ✅ MediaStorage
    - ✅ MediaPoolFolder
    - ✅ MediaPool
    - ✅ Project
    - ✅ ProjectManager
    - ✅ Gallery
    - ✅ GalleryStillAlbum
    - ✅ Resolve

Based on the official Resolve documentation
along with the hard work of [Brad Cordiero](https://gist.github.com/bradcordeiro/2f00120fad252a1b2bffcb882c9c941b)
'''

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

    def get_timeline_by_index(self, idx: int) -> "Timeline":
        """Returns timeline at the given index, 1 <= idx <= project.GetTimelineCount()."""
        return Timeline(self.rpc("GetTimelineByIndex", idx))

    def get_current_timeline(self) -> "Timeline":
        """Returns the currently loaded timeline."""
        return Timeline(self.rpc("GetCurrentTimeline"))

    def set_current_timeline(self, timeline: "Timeline") -> bool:
        """Sets given timeline as current timeline for the project. Returns True if successful."""
        return self.rpc("SetCurrentTimeline", timeline)

    def get_gallery(self) -> "Gallery":
        """Returns the Gallery object."""
        return Gallery(self.rpc("GetGallery"))

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

    def get_render_job_list(self) -> List["RenderJob"]:
        """Returns a list of render jobs and their information."""
        return [RenderJob(job) for job in self.rpc("GetRenderJobList")]
    
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

    def get_render_job_status(self, job_id: str) -> "RenderJobStatus":
        """Returns a dict with job status and completion percentage of the job by given jobId (string)."""
        return RenderJobStatus(self.rpc("GetRenderJobStatus", job_id))

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

    def create_empty_timeline(self, name: str) -> "Timeline":
        """Adds new timeline with given name."""
        return Timeline(self.rpc("CreateEmptyTimeline", name))

    def append_to_timeline(self, *clips: "MediaPoolItem") -> List["TimelineItem"]:
        """Appends specified MediaPoolItem objects in the current timeline. Returns the list of appended timelineItems."""
        return [TimelineItem(item) for item in self.rpc("AppendToTimeline", list(clips))]

    def create_timeline_from_clips(self, name: str, *clips: "MediaPoolItem") -> "Timeline":
        """Creates new timeline with specified name, and appends the specified MediaPoolItem objects."""
        return Timeline(self.rpc("CreateTimelineFromClips", name, list(clips)))

    def import_timeline_from_file(self, file_path: str, import_options: Dict[str, Any]) -> "Timeline":
        """Creates timeline based on parameters within given file and optional importOptions dict."""
        return Timeline(self.rpc("ImportTimelineFromFile", file_path, import_options))

    def delete_timelines(self, timelines: List["Timeline"]) -> bool:
        """Deletes specified timelines in the media pool."""
        return self.rpc("DeleteTimelines", timelines)

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

class TimelineItem(API_Object):
    def get_name(self) -> str:
        """Returns the item name."""
        return self.rpc("GetName")

    def get_duration(self) -> int:
        """Returns the item duration."""
        return self.rpc("GetDuration")

    def get_end(self) -> int:
        """Returns the end frame position on the timeline."""
        return self.rpc("GetEnd")

    def get_fusion_comp_count(self) -> int:
        """Returns number of Fusion compositions associated with the timeline item."""
        return self.rpc("GetFusionCompCount")

    def get_fusion_comp_by_index(self, comp_index: int) -> "FusionComp":
        """Returns the Fusion composition object based on given index. 1 <= compIndex <= timelineItem.GetFusionCompCount()"""
        return FusionComp(self.rpc("GetFusionCompByIndex", comp_index))

    def get_fusion_comp_name_list(self) -> List[str]:
        """Returns a list of Fusion composition names associated with the timeline item."""
        return self.rpc("GetFusionCompNameList")

    def get_fusion_comp_by_name(self, comp_name: str) -> "FusionComp":
        """Returns the Fusion composition object based on given name."""
        return FusionComp(self.rpc("GetFusionCompByName", comp_name))

    def get_left_offset(self) -> int:
        """Returns the maximum extension by frame for clip from left side."""
        return self.rpc("GetLeftOffset")

    def get_right_offset(self) -> int:
        """Returns the maximum extension by frame for clip from right side."""
        return self.rpc("GetRightOffset")

    def get_start(self) -> int:
        """Returns the start frame position on the timeline."""
        return self.rpc("GetStart")

    def set_property(self, property_key: str, property_value: Union[str, int, bool]) -> bool:
        """Sets the value of property "propertyKey" to value "propertyValue"."""
        return self.rpc("SetProperty", property_key, property_value)

    def get_property(self, property_key: Optional[str] = None) -> Union[Dict[str, Union[str, int, bool]], str, int]:
        """Returns the value of the specified key if no key is specified, the method returns a dictionary(python) or table(lua) for all supported keys."""
        if property_key is None:
            return self.rpc("GetProperty")
        else:
            return self.rpc("GetProperty", property_key)

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
        """Delete all markers of the specified color from the timeline item. "All" as argument deletes all color markers."""
        return self.rpc("DeleteMarkersByColor", color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Delete marker at frame number from the timeline item."""
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
        """Clear flags of the specified color. An "All" argument is supported to clear all flags."""
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

    def add_fusion_comp(self) -> "FusionComp":
        """Adds a new Fusion composition associated with the timeline item."""
        return FusionComp(self.rpc("AddFusionComp"))

    def import_fusion_comp(self, path: str) -> "FusionComp":
        """Imports a Fusion composition from given file path by creating and adding a new composition for the item."""
        return FusionComp(self.rpc("ImportFusionComp", path))

    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        """Exports the Fusion composition based on given index to the path provided."""
        return self.rpc("ExportFusionComp", path, comp_index)

    def delete_fusion_comp_by_name(self, comp_name: str) -> bool:
        """Deletes the named Fusion composition."""
        return self.rpc("DeleteFusionCompByName", comp_name)

    def load_fusion_comp_by_name(self, comp_name: str) -> "FusionComp":
        """Loads the named Fusion composition as the active composition."""
        return FusionComp(self.rpc("LoadFusionCompByName", comp_name))

    def rename_fusion_comp_by_name(self, old_name: str, new_name: str) -> bool:
        """Renames the Fusion composition identified by oldName."""
        return self.rpc("RenameFusionCompByName", old_name, new_name)

    def add_version(self, version_name: str, version_type: int) -> bool:
        """Adds a new color version for a video clipbased on versionType (0 - local, 1 - remote)."""
        return self.rpc("AddVersion", version_name, version_type)

    def get_current_version(self) -> Dict[str, Union[str, int]]:
        """Returns the current version of the video clip. The returned value will have the keys versionName and versionType (0 - local, 1 - remote)."""
        return self.rpc("GetCurrentVersion")

    def delete_version_by_name(self, version_name: str, version_type: int) -> bool:
        """Deletes a color version by name and versionType (0 - local, 1 - remote)."""
        return self.rpc("DeleteVersionByName", version_name, version_type)

    def load_version_by_name(self, version_name: str, version_type: int) -> bool:
        """Loads a named color version as the active version. versionType: 0 - local, 1 - remote."""
        return self.rpc("LoadVersionByName", version_name, version_type)

    def rename_version_by_name(self, old_name: str, new_name: str, version_type: int) -> bool:
        """Renames the color version identified by oldName and versionType (0 - local, 1 - remote)."""
        return self.rpc("RenameVersionByName", old_name, new_name, version_type)

    def get_version_name_list(self, version_type: int) -> List[str]:
        """Returns a list of all color versions for the given versionType (0 - local, 1 - remote)."""
        return self.rpc("GetVersionNameList", version_type)

    def get_media_pool_item(self) -> Optional["MediaPoolItem"]:
        """Returns the media pool item corresponding to the timeline item if one exists."""
        media_pool_item = self.rpc("GetMediaPoolItem")
        if media_pool_item:
            return MediaPoolItem(media_pool_item)
        else:
            return None

    def get_stereo_convergence_values(self) -> Dict[int, float]:
        """Returns a dict (offset -> value) of keyframe offsets and respective convergence values."""
        return self.rpc("GetStereoConvergenceValues")

    def get_stereo_left_floating_window_params(self) -> Dict[int, Dict[str, float]]:
        """For the LEFT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. Value at particular offset includes the left, right, top and bottom floating window values."""
        return self.rpc("GetStereoLeftFloatingWindowParams")

    def get_stereo_right_floating_window_params(self) -> Dict[int, Dict[str, float]]:
        """For the RIGHT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. Value at particular offset includes the left, right, top and bottom floating window values."""
        return self.rpc("GetStereoRightFloatingWindowParams")

    def get_num_nodes(self) -> int:
        """Returns the number of nodes in the current graph for the timeline item."""
        return self.rpc("GetNumNodes")

    def set_lut(self, node_index: int, lut_path: str) -> bool:
        """Sets LUT on the node mapping the node index provided, 1 <= nodeIndex <= total number of nodes."""
        return self.rpc("SetLUT", node_index, lut_path)

    def get_lut(self, node_index: int) -> str:
        """Gets relative LUT path based on the node index provided, 1 <= nodeIndex <= total number of nodes."""
        return self.rpc("GetLUT", node_index)

    def set_cdl(self, cdl_map: Dict[str, Union[str, int]]) -> bool:
        """Keys of map are: "NodeIndex", "Slope", "Offset", "Power", "Saturation", where 1 <= NodeIndex <= total number of nodes."""
        return self.rpc("SetCDL", cdl_map)

    def add_take(self, media_pool_item: "MediaPoolItem", start_frame: Optional[int] = None, end_frame: Optional[int] = None) -> bool:
        """Adds mediaPoolItem as a new take. Initializes a take selector for the timeline item if needed. By default, the full clip extents is added. startFrame (int) and endFrame (int) are optional arguments used to specify the extents."""
        return self.rpc("AddTake", media_pool_item, start_frame, end_frame)

    def get_selected_take_index(self) -> int:
        """Returns the index of the currently selected take, or 0 if the clip is not a take selector."""
        return self.rpc("GetSelectedTakeIndex")

    def get_takes_count(self) -> int:
        """Returns the number of takes in take selector, or 0 if the clip is not a take selector."""
        return self.rpc("GetTakesCount")

    def get_take_by_index(self, idx: int) -> Dict[str, Union[int, "MediaPoolItem"]]:
        """Returns a dict (keys "startFrame", "endFrame" and "mediaPoolItem") with take info for specified index."""
        take_info = self.rpc("GetTakeByIndex", idx)
        take_info["mediaPoolItem"] = MediaPoolItem(take_info["mediaPoolItem"])
        return take_info

    def delete_take_by_index(self, idx: int) -> bool:
        """Deletes a take by index, 1 <= idx <= number of takes."""
        return self.rpc("DeleteTakeByIndex", idx)

    def select_take_by_index(self, idx: int) -> bool:
        """Selects a take by index, 1 <= idx <= number of takes."""
        return self.rpc("SelectTakeByIndex", idx)

    def finalize_take(self) -> bool:
        """Finalizes take selection."""
        return self.rpc("FinalizeTake")

    def copy_grades(self, tgt_timeline_items: List["TimelineItem"]) -> bool:
        """Copies the current grade to all the items in tgtTimelineItems list. Returns True on success and False if any error occurred."""
        return self.rpc("CopyGrades", tgt_timeline_items)

    def update_sidecar(self) -> bool:
        """Updates sidecar file for BRAW clips or RMD file for R3D clips. Added in Resolve 18."""
        return self.rpc("UpdateSidecar")

    def get_unique_id(self) -> str:
        """Returns a unique ID for the timeline item. Added in Resolve 18."""
        return self.rpc("GetUniqueId")

class Timeline(API_Object):

    def get_name(self) -> str:
        """Returns the timeline name."""
        return self.rpc("GetName")

    def set_name(self, timeline_name: str) -> bool:
        """Sets the timeline name if timelineName (string) is unique. Returns True if successful."""
        return self.rpc("SetName", timeline_name)

    def get_start_frame(self) -> int:
        """Returns the frame number at the start of timeline."""
        return self.rpc("GetStartFrame")

    def get_end_frame(self) -> int:
        """Returns the frame number at the end of timeline."""
        return self.rpc("GetEndFrame")

    def set_start_timecode(self, timecode: str) -> bool:
        """Set the start timecode of the timeline to the string 'timecode'. Returns true when the change is successful, false otherwise."""
        return self.rpc("SetStartTimecode", timecode)

    def get_start_timecode(self) -> str:
        """Returns the start timecode for the timeline."""
        return self.rpc("GetStartTimecode")

    def get_track_count(self, track_type: str) -> int:
        """Returns the number of tracks for the given track type ("audio", "video" or "subtitle")."""
        return self.rpc("GetTrackCount", track_type)

    def get_item_list_in_track(self, track_type: str, index: int) -> List["TimelineItem"]:
        """Returns a list of timeline items on that track (based on trackType and index). 1 <= index <= GetTrackCount(trackType)."""
        return [TimelineItem(item) for item in self.rpc("GetItemListInTrack", track_type, index)]

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
        """Deletes all timeline markers of the specified color. An "All" argument is supported and deletes all timeline markers."""
        return self.rpc("DeleteMarkersByColor", color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Deletes the timeline marker at the given frame number."""
        return self.rpc("DeleteMarkerAtFrame", frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        """Delete first matching marker with specified customData."""
        return self.rpc("DeleteMarkerByCustomData", custom_data)

    def apply_grade_from_drx(self, path: str, grade_mode: int, *items: "TimelineItem") -> bool:
        """Loads a still from given file path (string) and applies grade to Timeline Items with gradeMode (int): 0 - "No keyframes", 1 - "Source Timecode aligned", 2 - "Start Frames aligned"."""
        return self.rpc("ApplyGradeFromDRX", path, grade_mode, list(items))

    def get_current_timecode(self) -> str:
        """Returns a string timecode representation for the current playhead position, while on Cut, Edit, Color and Deliver pages."""
        return self.rpc("GetCurrentTimecode")

    def set_current_timecode(self, timecode: str) -> bool:
        """Sets current playhead position from input timecode for Cut, Edit, Color, Fairlight and Deliver pages."""
        return self.rpc("SetCurrentTimecode", timecode)

    def get_current_video_item(self) -> "TimelineItem":
        """Returns the current video timeline item."""
        return TimelineItem(self.rpc("GetCurrentVideoItem"))

    def get_current_clip_thumbnail_image(self) -> Dict[str, Union[int, str]]:
        """Returns a dict (keys "width", "height", "format" and "data") with data containing raw thumbnail image data (RGB 8-bit image data encoded in base64 format) for current media in the Color Page."""
        return self.rpc("GetCurrentClipThumbnailImage")

    def get_track_name(self, track_type: str, track_index: int) -> str:
        """Returns the track name for track indicated by trackType ("audio", "video" or "subtitle") and index. 1 <= trackIndex <= GetTrackCount(trackType)."""
        return self.rpc("GetTrackName", track_type, track_index)

    def set_track_name(self, track_type: str, track_index: int, name: str) -> bool:
        """Sets the track name (string) for track indicated by trackType ("audio", "video" or "subtitle") and index. 1 <= trackIndex <= GetTrackCount(trackType)."""
        return self.rpc("SetTrackName", track_type, track_index, name)

    def duplicate_timeline(self, timeline_name: Optional[str] = None) -> "Timeline":
        """Duplicates the timeline and returns the created timeline, with the (optional) timelineName, on success."""
        return Timeline(self.rpc("DuplicateTimeline", timeline_name))

    def create_compound_clip(self, timeline_items: List["TimelineItem"], clip_info: Dict[str, str]) -> "TimelineItem":
        """Creates a compound clip of input timeline items with an optional clipInfo map: {"startTimecode" : "00:00:00:00", "name" : "Compound Clip 1"}. It returns the created timeline item."""
        return TimelineItem(self.rpc("CreateCompoundClip", timeline_items, clip_info))

    def create_fusion_clip(self, timeline_items: List["TimelineItem"]) -> "TimelineItem":
        """Creates a Fusion clip of input timeline items. It returns the created timeline item."""
        return TimelineItem(self.rpc("CreateFusionClip", timeline_items))

    def import_into_timeline(self, file_path: str, import_options: Dict[str, Any]) -> bool:
        """Imports timeline items from an AAF file and optional importOptions dict into the timeline."""
        return self.rpc("ImportIntoTimeline", file_path, import_options)

    def export(self, file: str, type: str, subtype: Optional[str] = None) -> bool:
        """Exports timeline to 'file' as per input type & subtype format."""
        return self.rpc("Export", file, type, subtype)

    def get_setting(self, setting_name: str) -> str:
        """Returns value of timeline setting (indicated by settingName : string). Check the section below for more information."""
        return self.rpc("GetSetting", setting_name)

    def set_setting(self, setting_name: str, setting_value: str) -> bool:
        """Sets timeline setting (indicated by settingName : string) to the value (settingvalue : string). Check the section below for more information."""
        return self.rpc("SetSetting", setting_name, setting_value)

    def insert_generator_into_timeline(self, generator_name: str) -> "TimelineItem":
        """Inserts a generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.rpc("InsertGeneratorIntoTimeline", generator_name))

    def insert_fusion_generator_into_timeline(self, generator_name: str) -> "TimelineItem":
        """Inserts a Fusion generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.rpc("InsertFusionGeneratorIntoTimeline", generator_name))

    def insert_fusion_composition_into_timeline(self) -> "TimelineItem":
        """Inserts a Fusion composition into the timeline."""
        return TimelineItem(self.rpc("InsertFusionCompositionIntoTimeline"))

    def insert_ofx_generator_into_timeline(self, generator_name: str) -> "TimelineItem":
        """Inserts an OFX generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.rpc("InsertOFXGeneratorIntoTimeline", generator_name))

    def insert_title_into_timeline(self, title_name: str) -> "TimelineItem":
        """Inserts a title (indicated by titleName : string) into the timeline."""
        return TimelineItem(self.rpc("InsertTitleIntoTimeline", title_name))

    def insert_fusion_title_into_timeline(self, title_name: str) -> "TimelineItem":
        """Inserts a Fusion title (indicated by titleName : string) into the timeline."""
        return TimelineItem(self.rpc("InsertFusionTitleIntoTimeline", title_name))

    def grab_still(self) -> "GalleryStill":
        """Grabs still from the current video clip. Returns a GalleryStill object."""
        return GalleryStill(self.rpc("GrabStill"))

    def grab_all_stills(self, still_frame_source: int) -> List["GalleryStill"]:
        """Grabs stills from all the clips of the timeline at 'stillFrameSource' (1 - First frame, 2 - Middle frame). Returns the list of GalleryStill objects."""
        return [GalleryStill(still) for still in self.rpc("GrabAllStills", still_frame_source)]

    def get_unique_id(self) -> str:
        """Returns a unique ID for the timeline. Added in Resolve 18."""
        return self.rpc("GetUniqueId")

class RenderJob(API_Object):
    """ Descriptor for the Render Job settings

    Attributes:
    - AudioCodec: str
    - AudioSampleRate: int
    - VideoFormat: str
    - IsExportAudio: bool
    - ExportAlpha: bool
    - FormatHeight: int
    - FrameRate: str
    - VideoCodec: str
    - FormatWidth: int
    - MarkOut: int
    - JobId: str
    - MarkIn: int
    - TargetDir: str
    - IsExportVideo: bool
    - AudioBitDepth: int
    - TimelineName: str
    - OutputFilename: str
    - PixelAspectRatio: float
    - RenderMode: str
    - PresetName: str
    - RenderJobName: str 
    """
    
    AudioCodec: str
    AudioSampleRate: int
    VideoFormat: str
    IsExportAudio: bool
    ExportAlpha: bool
    FormatHeight: int
    FrameRate: str
    VideoCodec: str
    FormatWidth: int
    MarkOut: int
    JobId: str
    MarkIn: int
    TargetDir: str
    IsExportVideo: bool
    AudioBitDepth: int
    TimelineName: str
    OutputFilename: str
    PixelAspectRatio: float
    RenderMode: str
    PresetName: str
    RenderJobName: str 

class RenderJobStatus(API_Object):
    """ Descriptor for a Render Job's status 
        (Undocumented, shaped by trial-and-error) 
    
    Attributes:
        - CompletionPercentage: float
        - JobStatus: str # 'Ready' | 'Rendering' | 'Cancelled' | 'Complete' | 'Failed'
        - TimeTakenToRenderInMs: Optional[int]
        - EstimatedTimeRemainingInMs: Optional[int]
        - Error: Optional[str]
    """
    CompletionPercentage: float
    JobStatus: str # 'Ready' | 'Rendering' | 'Cancelled' | 'Complete' | 'Failed'
    TimeTakenToRenderInMs: Optional[int]
    EstimatedTimeRemainingInMs: Optional[int]
    Error: Optional[str]

class FusionComp(API_Object):
    """ Return or argument type for some TimelineItem methods but otherwise undocumented """

# TODO:❔ should the above really be daisychain.fusion.Composition type?
# ie `FusionComp = daisychain.fusion.Composition`

class GalleryStill(API_Object):
    """ Return or argument type for some TimelineItem methods but otherwise undocumented """

class Gallery(API_Object):
    def get_album_name(self, gallery_still_album: "GalleryStillAlbum") -> str:
        """Returns the name of the GalleryStillAlbum object 'galleryStillAlbum'."""
        return self.rpc("GetAlbumName", gallery_still_album)

    def set_album_name(self, gallery_still_album: "GalleryStillAlbum", album_name: str) -> bool:
        """Sets the name of the GalleryStillAlbum object 'galleryStillAlbum' to 'albumName'."""
        return self.rpc("SetAlbumName", gallery_still_album, album_name)

    def get_current_still_album(self) -> "GalleryStillAlbum":
        """Returns current album as a GalleryStillAlbum object."""
        return GalleryStillAlbum(self.rpc("GetCurrentStillAlbum"))

    def set_current_still_album(self, gallery_still_album: "GalleryStillAlbum") -> bool:
        """Sets current album to GalleryStillAlbum object 'galleryStillAlbum'."""
        return self.rpc("SetCurrentStillAlbum", gallery_still_album)

    def get_gallery_still_albums(self) -> List["GalleryStillAlbum"]:
        """Returns the gallery albums as a list of GalleryStillAlbum objects."""
        return [GalleryStillAlbum(album) for album in self.rpc("GetGalleryStillAlbums")]

class GalleryStillAlbum(API_Object):
    def get_stills(self) -> List["GalleryStill"]:
        """Returns the list of GalleryStill objects in the album."""
        return [GalleryStill(still) for still in self.rpc("GetStills")]

    def get_label(self, gallery_still: "GalleryStill") -> str:
        """Returns the label of the galleryStill."""
        return self.rpc("GetLabel", gallery_still)

    def set_label(self, gallery_still: "GalleryStill", label: str) -> bool:
        """Sets the new 'label' to GalleryStill object 'galleryStill'."""
        return self.rpc("SetLabel", gallery_still, label)

    def export_stills(self, gallery_stills: List["GalleryStill"], path: str, file_prefix: str, format: str) -> bool:
        """
        Exports list of GalleryStill objects '[galleryStill]' to directory 'folderPath', with filename prefix 'filePrefix',
        using file format 'format' (supported formats: dpx, cin, tif, jpg, png, ppm, bmp, xpm).
        """
        return self.rpc("ExportStills", gallery_stills, path, file_prefix, format)

    def delete_stills(self, gallery_stills: List["GalleryStill"]) -> bool:
        """Deletes specified list of GalleryStill objects '[galleryStill]'."""
        return self.rpc("DeleteStills", gallery_stills)

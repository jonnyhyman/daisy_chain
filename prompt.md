The following typescript definitions need to be translated
into Python types and functions including docstrings,
each with an implementation to call a function called rpc.

For example:

```ts
class MediaPoolItem {
    /** Returns the clip name. */
    GetName() : string;
}
```

translates to:

```python
class MediaPoolItem(API_Object):
    def get_name(self) -> str:
        """ Returns the clip name. """
        return self.rpc("GetName")
```

and

```ts
class MediaPool {
    /** Imports specified file/folder paths into current Media Pool folder. Input is an array of file/folder paths. Returns a list of the MediaPoolItems created. */
    ImportMedia(items: string[]) : MediaPoolItem[];
    ImportMedia(clipInfo: MediaPoolItemClipInfo[]) : MediaPoolItem[];
}
```
translates to:
```python
class MediaPool(API_Object):
    def import_media(self, path: List[str | Path]) -> List["MediaPoolItem"]:
        path = [str(Path(p).resolve()) for p in path]
        print(path, type(path))
        outs = self.rpc("ImportMedia", path)
        print(outs, type(outs))
        return [MediaPoolItem(c) for c in outs]
```

Can you translate the definitions:
```ts
class Resolve {
    /** Returns the Fusion object. Starting point for Fusion scripts. Returns Fusion */
    Fusion() : unknown;

    /** Returns the media storage object to query and act on media locations. Returns MediaStorage */
    GetMediaStorage() : MediaStorage;

    /** Returns the project manager object for currently open database. Returns ProjectManager */
    GetProjectManager() : ProjectManager;

    /** Switches to indicated page in DaVinci Resolve. Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver"). */
    OpenPage(pageName: PageName) : boolean;

    /** Returns the page currently displayed in the main window. Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None). */
    GetCurrentPage() : PageName;

    /** Returns product name. */
    GetProductName() : string;

    /** Returns list of product version fields in [major, minor, patch, build, suffix] format. */
    GetVersion() : string[];

    /** Returns product version in "major.minor.patch[suffix].build" format. */
    GetVersionString() : string;

    /** Loads UI layout from saved preset named 'presetName'. */
    LoadLayoutPreset(presetName: string) : boolean;

    /** Overwrites preset named 'presetName' with current UI layout. */
    UpdateLayoutPreset(presetName: string) : boolean;

    /** Exports preset named 'presetName' to path 'presetFilePath'. */
    ExportLayoutPreset(presetName: string, presetFilePath: string) : boolean;

    /** Deletes preset named 'presetName'. */
    DeleteLayoutPreset(presetName: string) : boolean;

    /** Saves current UI layout as a preset named 'presetName'. */
    SaveLayoutPreset(presetName: string) : boolean;

    /** Imports preset from path 'presetFilePath'. The optional argument 'presetName' specifies how the preset shall be named. If not specified, the preset is named based on the filename. */
    ImportLayoutPreset(presetFilePath: string, presetName: string) : boolean;

    /** */
    Quit() : void;
  }
```

# 🌼 DaisyChain
__Script and workflow manager for DaVinci Resolve__


## Goals
- _Make DaVinci Resolve/Fusion scripting better: faster, less tedious, and reliable_
- _Write scripts with full autocompletion, and in-IDE documentation/hover-docs_
- _Turn your one-off script automations into ongoing organized workflows_
- _Experiment with Resolve scripts safely, on an unbounded undo tree_ (Future goal, not currently implemented)
- _Share your workflows and use those that others have shared_ (A script manager, not currently implemented)

## Status
Alpha, but used in production 🤞 
(warning: Resolve script executions are irreversible!)

|Language|Resolve API|Fusion API|Tests|
|--|--|--|--|
|Python| ✅ | 🚧 | ❌ |
|Lua | ❌ | ❌ | ❌ |
|JS/TS| ❌ | ❌ | ❌ |
|Rust| ❌ | ❌ | ❌ |

## Batteries included 🔋

Any of these can be run on your commandline as soon as you've installed daisychain and started the Host.
- `copycat` A script to copy from a current-timeline-item metadata field to clipboard on a timer, called CopyCat
- `bindive` A script to auto-import anything added to a watch folder into current media bin `bindive --watch /path/to/watch`
- `collate` A script to (recursively!) copy or move all media files on disk into a central location, mirroring Media Bin structure

see the implementations in `python/daisychain/scripts/` for more details

## Script ideas 💭

- 🚧 A Chromium / WebKit extension to "Download to Media Pool" from internet, called CreditsDue
- 🚧 A more accurate transcription workflow than Resolve's trashy one, using OpenAI Whisper
- 🚧 `py-auto-gui` madness to automate repetitive edit tasks (vim-macros, basically)
- 🚧 Removing silence from a clip automatically (via ffmpeg or some loopback)


## Why? 🤔
Blackmagic's API for Resolve and Fusion is extensive and powerful,
but woefully undocumented and behind-the-times architecturally.
From locking users into antiquated Python versions, to non-existent
(or silent) errors/exceptions/tracebacks, to documentation in a .txt
file without any IDE / language-server support, scripting is _not fun_.

DaisyChain makes it so you can use the Resolve/Fusion API
from any language you like (Python __3.6-3.12+__, Lua, JS, TS, Rust),
in any execution environment you like (terminal, localhost web app, ...)
while retaining full in-editor documentation stubs and types.

It does this by hosting a remote procedure call server within Resolve,
and defining a serialized interface for the entire API surface.
The Resolve API itself is actually an RPC server, so this is really
like an RPC of an RPC. While a little bit ridiculous, this allows us
to write and use the API in an efficient way with full documentation!

Types, documentation, and RPC connection is written in each client language,
see the status of your favorite language in the Status table above.

## Audience
- Lazy video editors with coding experience
- Production houses with workflow programmers

## Installation

0. Download this repo
1. Set Resolve External Scripting to *either* Local or Network
2. Install Python
3. Ensure that the PYTHONHOME env variable is set at system level,
    to point to the directory where you will find the python3.exe,
    or symlink that path with /usr/local/bin/python3
4. Copy the DaisyChain Host script into Resolve's watch folder for scripts
    macOS

    ```
    cp "./python/DaisyChain Host.py" "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility"
    ```
    
    Windows
    📁 "%AppData%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Utility"

    Linux
    📁 "~/.local/share/DaVinciResolve/Fusion/Scripts/Utility"

    Restart Resolve if it was open
5. Run the DaisyChain host from the `Workspaces > Scripts` dropdown in Resolve
6. Install daisychain to python by running `pip install -e .` (editable install) in the repo

## Roadmap

__Milestone 1__ Python server and client
- [x] Python RPC Server
- [x] Python RPC client with Resolve API coverage, types, and docstrings
- [ ] Python RPC client with Fusion API coverage, types, and docstrings < This would be awesome because you could run Fusion scripts from the Edit view, potentially game changing in some workflows

__Milestone 2__ multi-language
- [ ] JS RPC client with API coverage, types, and documentation
- [ ] Lua RPC client with API coverage

__Milestone 3__ reversibility & safety
- [ ] RPC Server should
    - [ ] Validate all input types before executing any function in the API
    - [ ] Retain an infinite undo-tree (with timestamps) for reverting to previous states

__Milestone 3__ user interface & sharing 
- [ ] Build a workflow scheduler & package/script manager UI and package manager
- [ ] Determine if you even need a workflow scheduler UI or if Warp/tmux/nu is just fine?

## Contribution

Feel free to report bugs / issues, but do not expect any serious support on the Issues page.

If you would like to contribute a client package for your favorite language, or a suite of tests for existing code, please feel free to submit a pull request!


## Technical notes

Since it seems like the Resolve API is designed for syncronous execution, let's stick to
having syncronous execution of the RPC server, so that we can't overload the integration API. 
With that said, it would be worth doing some testing to see what happens with multiple servers
running at the same time, and what the maximum refresh rate / transaction rate of the API is.


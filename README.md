# 🌼 DaisyChain
__Script and workflow manager for DaVinci Resolve__

## Audience
- Jonny mostly, for now
- Later, video editors with coding experience
- Later, production houses with workflow programmers on staff

## Features
- [ ] _Resolve Workflow Integration_ interface to manage scripts:
    - [x] Write scripts in your favorite text editor in JS, TS, Python, or Lua
    - [ ] Queue scripts in DaisyChain to run in sequence or isolation
        - [ ] Specify runtime input arguments (command-line args)
        - [ ] Specify whether output propogates to next in sequence
    - [ ] Chain queues together to build pipelines of execution
    - [ ] Save collections of pipelines/queues/scripts to build project-specific workflows
- [ ] Script error and log management
- [ ] Typed and documented Resolve API wrapper with reversible function calls
    - [ ] Python
    - [ ] JS/TS
    - [ ] Lua
- [ ] Package manager written in Rust to add other's scripts & workflows to your environment
    - [ ] Similar to neovim package managers, plugins are simply git repos with defined structure
    - [ ] No opaque scripts, all scripts must be human readable

## Goals
- _Turn your one-off script automations into ongoing organized workflows_
- _Experiment with non-destructively on an unbounded undo tree_
- _Share your workflows and use those that others have shared_

## Design

1. Remote procedure call (RPC) servers in Python, Lua, and JS from within Resolve, which:
    - Execute commands from clients (if they are valid)
    - Serialize outputs of execution back to client (if necessary)

2. RPC client packages (Py/Lua/JS) dispatch commands and retrieve results

3. DaisyChain UI (Rust) -- essentially a commandline workflow manger (maybe you just need Warp/tmux/nu?)
    - Select a script on disk
    - Specify cmdline args in text fields
    - Build queue chains
    - Manage stderr & stdout
    - Save pipelines/queues
    - Install new pipelines/queues via the package manager

## Use-cases

- An ongoing process to copy from current-clip metadata field to clipboard
- A Chromium / WebKit extension to "Download to Media Pool" from internet
- A more accurate transcription workflow using Whisper (for subtitles)
- Removing silence from a clip automatically (via ffmpeg or some loopback)
- `py-auto-gui` madness to automate repetitive edit tasks (macros, basically)

## Roadmap

Milestone 1
- [ ] Prototype JS DaisyChain RPC Server & Client
- [ ] Prototype Python DaisyChain RPC Server & Client
- [ ] Prototype Lua DaisyChain RPC Server & Client

Milestone 2
- [ ] JS/TS full coverage of API with types and docstrings
- [ ] Python RPC Server `py_host` & client `py_api` with API coverage, types, and docstrings
- [ ] Lua RPC Server `lua_host` & client `lua_api` with API coverage, types, and docstrings

Milestone 3
- [ ] Determine if you even need a workflow scheduler UI or if Warp/tmux/nu is just fine?

## Technical notes


Since it seems like the Resolve API is designed for syncronous execution, let's stick to
having syncronous execution of the RPC servers, so that we can't overload the integration API. 
With that said, it would be worth doing some testing to see if the 

Limitations: 
- Fusion is inaccessible via the JS/TS API unless you call into Python, which would be weird


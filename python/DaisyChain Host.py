from pathlib import Path
from datetime import datetime
import traceback
import sys
import os
import socket
import select
import json
import re
import hashlib

from typing import Union, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from resolve_types import BMD, Resolve, Fusion
else:
    # code is unreachable by LSP here
    # not a problem because these variables
    # are injected by Resolve at runtime
    BMD = type(bmd)  # noqa
    Resolve = type(resolve)  # noqa
    Fusion = type(fusion)  # noqa

# cp "python/DaisyChain Host.py" "~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/DaisyChain Host.py"

"""
    #🌼 Welcome to DaisyChain! 

    This is the entry point for the DaisyChain host
    as launched from the Scripts menu in Resolve,
    as long as this file (and its imports) are 
    placed in:

    macOS
    📁 "~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility"
    
    Windows
    📁 "%AppData%\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility"

    Linux
    📁 "~/.local/share/DaVinciResolve/Fusion/Scripts/Utility"

    
    ### What this code does:

    - Initializes the connection to Resolve
        - Starts a UI window to see status

    - Hosts a TCP server for command requests

    - On command request:
        - Deserializes the command and its args
            from the json bytes on the wire
        - Reconstructs it into a function call
            if all args are valid (else error)
        - Performs the requested command
        - Serializes the results into json
        - Sends the result back over the wire

"""

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
RATE = 50  # Milliseconds per update


def script_init() -> Tuple[BMD, Resolve, Fusion]:
    if not TYPE_CHECKING:
        # code is unreachable by LSP here
        # not a problem because these variables
        # are injected by Resolve at runtime
        return bmd, resolve, fusion  # type: ignore

    else:
        return BMD(), Resolve(), Fusion()


bmd, resolve, fusion = script_init()

log_dir = Path.home()


def log_to_file(log_string: str):
    preamble = f"\nDAISY CHAIN EXCEPTION LOG ---- {datetime.now()}"
    preamble += "\n----\n"
    with open(log_dir / "daisy_chain_error_log.txt", "a") as log_file:
        log_file.write(preamble)
        log_file.write(log_string)
        log_file.write("\n")


class API_Object:
    def GetUniqueId(self) -> str:
        return str()


API_Value = Union[str, int, float, bool, list, dict, None]
API_Roots = Union[Resolve, Fusion]

API_ObjType = Union[API_Object, API_Roots]
# this is an ongoing cache which can be
# reset by clicking the clear cache btn
API_Objects: dict[str, API_ObjType] = {}


def serialize(
    obj: Union[API_Value, API_Object, API_Roots], error: Optional[str] = None
):
    global API_Objects

    if error is not None:
        print(f"❌ Execution error > {error}")

    if isinstance(obj, list):
        # recurse through args to ensure they
        # are serialized if API_Objects
        obj = [json.loads(serialize(elem))["value"] for elem in obj]

    if isinstance(obj, dict):
        # recurse through args to ensure they
        # are serialized if API_Objects
        obj = {k: json.loads(serialize(v))["value"] for k, v in obj.items()}

    if not isinstance(obj, API_Value):
        # obj is an api object!
        try:
            # key by repr
            key_obj = str(obj)
            typ_obj = re.findall(r"^\w+", str(obj))[0]

            # generate a unique id for the key obj
            key_obj = hashlib.sha256(key_obj.encode()).hexdigest()
            jsn_obj = {"API_Object": {"type": typ_obj, "uuid": key_obj}}

            # retain reference to obj
            API_Objects[key_obj] = obj
            print(f"👍 Added {typ_obj} to API_Objects")

        except TypeError:
            jsn_obj = None
            error = f"TypeError: {obj} cannot be serialized"

    else:
        jsn_obj = obj

    return json.dumps(
        {
            "value": jsn_obj,
            "error": error,
        }
    )


def deserialize(desc: dict):
    """
    Get the object described by `desc`
    by retrieving it from the hash map

    """
    global API_Objects

    if desc["uuid"] in API_Objects.keys():
        return API_Objects[desc["uuid"]]
    else:
        return None


def reset_cache():
    """
    Clear the API_Objects cache
    """
    global API_Objects
    API_Objects = {}


def execute_remote_command(raw_cmd: bytes) -> str:
    """Validate and execute the remote command call
    from its json encoded in utf-8 bytes over TCP.

    Schema must exactly match:
    - root: dict - object lookup {'API_Object': {'type':str, 'uuid':str}}
    - impl: str  - the name of the type's impl to be called
    - args: list[API_Value] - the values of the func args
    - kwgs: dict[str, API_Value] - the values of the func kwgs

    Example 1: Get version string
    ```
    {
        'root': {'API_Object':{'type':"Resolve", 'uuid':"..."}},
        'impl': 'GetVersionString'
        'args': [],
        'kwgs': {},
    }
    ```
    Example 1: Import into media pool
    ```
    {
        'root': {'API_Object':{'type':"MediaPool", 'uuid':"..."}},
        'impl': 'ImportMedia'
        'args': ['./wow.mp4', './pie.jpg'],
        'kwgs': {},
    }
    ```

    where API_Value: str | int | float | bool | list | dict

    if the API_Value is a dict and it has key "API_Object",
        then we will reconstruct a python object with its
        keys as attributes of the object, an exact mirror
        of the object which exists in the Resolve API

    If the function signature doesn't match any known functions
        in the Resolve API, we will raise KeyError / TypeError

    """

    # decode json bytes to python dictionary
    cmd: dict = json.loads(raw_cmd.decode())

    # validate the command schema and types
    # (basics)
    try:
        assert "root" in cmd.keys() and isinstance(cmd["root"], dict)
    except AssertionError:
        return serialize(None, error=f"TypeError: invalid command type: {cmd}")

    try:
        assert "impl" in cmd.keys() and isinstance(cmd["impl"], str)
    except AssertionError:
        return serialize(None, error=f"TypeError: invalid command type: {cmd}")

    try:
        assert ("args" in cmd.keys()) and isinstance(cmd["args"], list)
    except AssertionError:
        return serialize(None, error=f"TypeError: invalid command args: {cmd}")

    try:
        assert ("kwgs" in cmd.keys()) and isinstance(cmd["kwgs"], dict)
    except AssertionError:
        return serialize(None, error=f"TypeError: invalid command kwgs: {cmd}")

    # detect if this is an initialization requst (`daisychain_init`)
    # in which case we simply return the root ref resolve
    if cmd["impl"] == "daisychain_init":
        print("🌼 Initializing:", cmd)
        return serialize(resolve)

    # validate that the type exists and the impl exists for that type
    src_desc = cmd["root"]["API_Object"]
    src_root = deserialize(src_desc)
    src_call = getattr(src_root, cmd["impl"])
    # ^ Resolve API things that every object has every attribute,
    # but if it actually does not, src_call will be None, not a function

    # TODO: validate that the resulting type is equivalent

    if src_call is None:
        return serialize(
            None, error=f'AttributeError: {src_root} has no impl {cmd["impl"]}'
        )

    # TODO: validate input argument types

    # deserialize any args or kwgs which are API_Objects
    for a, value in enumerate(cmd["args"]):
        cmd["args"][a] = (
            deserialize(value["API_Object"])
            if hasattr(value, "__iter__") and "API_Object" in value
            else value
        )

    for n, value in cmd["kwgs"]:
        cmd["kwgs"][n] = (
            deserialize(value["API_Object"])
            if hasattr(value, "__iter__") and "API_Object" in value
            else value
        )

    # execute command in resolve API, retreive its values
    print("🌼 Running:", cmd)

    try:
        output = src_call(*cmd["args"], **cmd["kwgs"])
        output = serialize(output)
    except Exception as e:
        # fail with error to the output
        output = serialize(None, error=str(e))

    print("🌼 Returning:", output)

    return output


try:
    # fill the objects cache with just resolve and fusion
    reset_cache()

    # build the tiny ui
    ui = fusion.UIManager  # type: ignore
    dispatcher = bmd.UIDispatcher(ui)  # type: ignore

    layout = ui.VGroup(
        [
            ui.Label(
                {
                    "ID": "status_line",
                    "Text": "🌼 DaisyChain starting...",
                    # 'Weight': 0.1,
                    # 'Font': ui.Font({ 'Family': "Helvetica" })
                }
            ),
            ui.Button(
                {
                    "ID": "reset_btn",
                    "Text": "Reset Cache",
                }
            ),
        ]
    )

    def set_status(s: str):
        wnd.Find("status_line").Text = f"🌼 DaisyChain {s}"

    wnd_id = "com.blackmagicdesign.resolve.DaisyChain"
    wnd = dispatcher.AddWindow(
        {
            "ID": wnd_id,
            "Geometry": [100, 100, 250, 75],
            "WindowTitle": "DaisyChain Host",
        },
        layout,
    )

    class DaisyContext:

        """Context manager for application state.
        Opens and closes:
            - socket (tcp)
            - window (fusion ui)
            - timers (fusion ui)
        """

        def __init__(self, host: str, port: int, rate: int):
            # all timeouts go to the context loop!
            dispatcher["On"]["Timeout"] = lambda event: self.loop(event)
            self.timer = ui.Timer({"ID": "main", "Interval": rate})

            # bind to the socket!
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((host, port))

            # no self.clients yet!
            self.sockets: list[socket.SocketType] = [self.socket]
            self.clients: dict[socket.SocketType, str] = {}

        def __enter__(self):
            self.socket.listen()
            self.socket.setblocking(False)
            self.timer.Start()
            print("🌼 Running")
            wnd.Show()
            return self

        def loop(self, _):
            """RPC Server Loop"""
            set_status("ready")

            read_sockets: list[socket.SocketType]
            error_sockets: list[socket.SocketType]

            read_sockets, _, error_sockets = select.select(
                self.sockets, [], self.sockets, 0
            )

            # process any reads / writes
            for notified_socket in read_sockets:
                # read or write from sockets
                if notified_socket == self.socket:
                    client_socket, client_address = self.socket.accept()
                    print(f"🌼 Received request from {client_address}")
                    self.sockets.append(client_socket)
                    self.clients[client_socket] = client_address
                else:
                    message = notified_socket.recv(16384)

                    if message:
                        print(f"🌼 Executing remote command: {message}")
                        set_status("executing")
                        reply = execute_remote_command(message)
                        set_status("responding")
                        notified_socket.send(reply.encode())
                    else:
                        self.sockets.remove(notified_socket)
                        del self.clients[notified_socket]

            # process any exceptions in sockets
            for notified_socket in error_sockets:
                client_info = self.clients.get(notified_socket, "Unknown client")
                try:
                    # Attempt to get more information on the error if possible
                    # This is a bit of a simplification; specifics may depend on the socket type and state
                    error_code = notified_socket.getsockopt(
                        socket.SOL_SOCKET, socket.SO_ERROR
                    )
                    error_msg = os.strerror(error_code)
                    print(
                        f"❌ Exception on {client_info}: {error_msg} (code {error_code})"
                    )

                except OSError as e:
                    print(f"❌ OS error on {client_info}: {e}")

                finally:
                    if notified_socket in self.sockets:
                        self.sockets.remove(notified_socket)
                    if notified_socket in self.clients:
                        del self.clients[notified_socket]
                    notified_socket.close()

        def __exit__(self, *_):
            print("🌼 Quitting")
            self.socket.close()
            self.timer.Stop()
            wnd.Hide()
            return False

    # register function to exit from RunLoop()
    wnd.On[wnd_id].Close = lambda _: dispatcher.ExitLoop()

    print("🌼 Starting")
    with DaisyContext(HOST, PORT, RATE) as ctx:
        dispatcher.RunLoop()  # blocking event loop

except Exception as _:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_str = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    log_to_file(traceback_str)

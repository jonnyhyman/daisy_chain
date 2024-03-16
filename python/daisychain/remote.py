from typing import Any
import asyncio
import json

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
    """ Get `resolve` root reference """
    return rpc({}, "daisychain_init")

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



from daisychain.remote import rpc_init
from daisychain.resolve import Resolve


def get_resolve() -> Resolve:
    """
    Initialize Resolve connection

    ```
    resolve: Resolve = get_resolve()
    ```

    ```
    async def main():
        resolve: Resolve = await get_resolve()
    ```
    """
    link = Resolve(rpc_init())

    if link is None:
        raise (RuntimeError("Resolve not found! Is the Host running?"))

    return link


# async def get_resolve_async() -> Resolve:
#     data = await rpc_init_async()
#     return Resolve(data)

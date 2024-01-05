from aiohttp import ClientSession


async def get_json(url: str, **kwargs):
    """
    Sends a GET request and return the JSON body asynchronously

    :param url: The URL
    :param kwargs: Other keyword arguments to pass to aiohttp.ClientSession.get()
    """
    async with ClientSession() as session:
        async with session.get(url, **kwargs) as res:
            return await res.json()

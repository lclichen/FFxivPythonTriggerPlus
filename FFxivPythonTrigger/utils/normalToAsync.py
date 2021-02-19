import asyncio
import functools

loop = asyncio.get_event_loop()


async def normal_to_async(call, *args, **kwargs):
    return await loop.run_in_executor(None, functools.partial(call, *args, **kwargs))

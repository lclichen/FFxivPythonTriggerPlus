import functools

async def normal_to_async(loop, call, *args, **kwargs):
    return await loop.run_in_executor(None, functools.partial(call, *args, **kwargs))

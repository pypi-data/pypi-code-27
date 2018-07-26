def run_async (coroutine):
	"""
	Asynchronously runs coroutine (function, defind with 'async def') until it completes.
	"""
	import asyncio
	loop = asyncio.get_event_loop	()
	loop.run_until_complete			(coroutine())

import asyncio

from .taxi import TaxiApp

loop = asyncio.get_event_loop()
loop.run_until_complete(TaxiApp().async_run())
loop.close()

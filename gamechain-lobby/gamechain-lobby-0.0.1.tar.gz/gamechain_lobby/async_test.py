#
# import asyncio
# import time
#
#
# class InitiatorMonitor:
#     async def wait_for_lfg(self):
#         print("PRE")
#         time.sleep(1)
#         print("POST")
#         yield 123
#
#
# async def main():
#     im = InitiatorMonitor()
#     v = await im.wait_for_lfg()
#
#     print(v)
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())



import asyncio
import datetime

class InitiatorMonitor:
    async def display_date(self, loop):
        end_time = loop.time() + 5.0
        while True:
            print(datetime.datetime.now())
            if (loop.time() + 1.0) >= end_time:
                return 123
                break
            await asyncio.sleep(1)

im = InitiatorMonitor()

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
x = loop.run_until_complete(im.display_date(loop))
print(x)
loop.close()
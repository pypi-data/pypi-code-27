import asyncio
import functools

#every coroutine
async def coromask(coro, args, fargs):
    """
    A coroutine who mask another coroutine  callback with args, and a
    function callbacks who manage input/output of corotine callback
    """
    try:
        _in=args
        msg=("Coromask args %s in coro %s" %(args, coro) )
        obtained=await coro(*args)
        if isinstance(obtained, Exception):
            raise Exception()
        else:
            result=fargs(_in, obtained)
            return result
    except Exception:
        print(msg)
        raise Exception
   
def renew(task, coro, fargs, *args):
    """
    A simple function who manages the scheduled task and set the
    renew of the task
    """
    if task.exception():
        print("Excepcion")
        raise task.result()
    else:
        result=task.result()
        loop=asyncio.get_event_loop()
        task=loop.create_task(coromask(coro, result, fargs))
        task.add_done_callback(functools.partial(renew, task, coro, fargs))

   
def renew_quamash(task, coro, fargs, loop, *args):
    """
    A simple function who manages the scheduled task and set the
    renew of the task
    """
    if task.exception():
        print("Excepcion")
        raise task.result()
    else:
        result=task.result()
        task=loop.create_task(coromask(coro, result, fargs))
        task.add_done_callback(functools.partial(renew_quamash, task, coro, fargs,loop))

def simple_fargs(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return _in
    """
    return _in


def simple_fargs_out(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return obtained
    """
    return obtained

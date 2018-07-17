# standar library
import asyncio
import functools

# contrib
from networktools.library import my_random_string
from networktools.colorprint import gprint, bprint, rprint

# same module
from .taskloop import coromask, renew, simple_fargs, simple_fargs_out


class TaskScheduler:
    """
    This class is a generic tasks scheduler that uses
    asyncio and multiprocessing
    For every new process activate M idle coro tasks
    until when are assigned by a function that send
    an id

    """
    def __init__(self, *args, **kwargs):
        if 'ipt' in kwargs.keys():
            self.ipt = kwargs['ipt']
        if 'ico' in kwargs.keys():
            self.ico = kwargs['ico']
        if 'assigned_tasks' in kwargs.keys():
            self.assigned_tasks = kwargs['assigned_tasks']
        if 'nproc' in kwargs.keys():
            self.lnproc = kwargs['nproc']
        if 'sta_init' in kwargs.keys():
            # dict
            self.sta_init = kwargs["sta_init"]

    def set_ipt(self, uin=4):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        ipt = my_random_string(uin)
        while True:
            if ipt not in self.ipt:
                self.ipt.append(ipt)
                break
            else:
                ipt = my_random_string(uin)
        return ipt

    def set_ico(self, uin=4):
        """
        Defines a new id for task related to collect data
        inside a worker, check if exists
        """
        ico = my_random_string(uin)
        while True:
            if ico not in self.ico:
                self.ico.append(ico)
                break
            else:
                ico = my_random_string(uin)
        return ico

    async def run_task(self, *args):
        print("There are no new *run_task* coroutine assigned")
        await asyncio.sleep(.1)
        return args

    def set_new_run_task(self, coro_callback):
        if asyncio.iscoroutinefunction(coro_callback):
            self.run_task = coro_callback
        else:
            print("The callback is not a coroutine")

    async def process_sta_task(self, ipt, ico, *args):
        # Process gather data for ids station
        # rprint("Generating PROCESS STA TASK")
        # bprint("Tasks avalaibles %s" %self.assigned_tasks[ipt] )
        assigned_task = None
        if ico in self.assigned_tasks[ipt].keys():
            assigned_task = self.assigned_tasks[ipt][ico]
            # assigned task -> ids
            # That is an ids code
        result = None
        bprint("Assigned task %s" %assigned_task)
        if assigned_task:
            # change
            # print("ST Station %s assigned to task %s on process %s"
            # %(assigned_task, ico, ipt), flush=True)
            # print("ST args", flush=True)
            # print(args)
            #print("St INIT %s" %self.sta_init[assigned_task])
            if not self.sta_init[assigned_task]:
                args = self.set_pst(assigned_task, args)
                # print("ST ARGS to gather...._> %s"
                # %args, flush=True)
            #rprint("SCHEDULER_PROCESS_STA_TASK On task, pre call gather_data")
            result = await self.run_task(*args)
            #gprint("SCHEDULER_PROCESS_STA_TASK On task, post call gather_data %s" %result)

        else:
            # Every N secs check if there are new station to add
            # gprint("Process data avoid \n")
            await asyncio.sleep(1)
            result = args
        rprint("To next iteration %s" %[ipt, ico, *result])
        return [ipt, ico, *result]

    async def process_sta_manager(self, ipt):
        # Manage asignation of station to task inside ipt process
        ids_list = self.proc_tasks[ipt]
        ass_tasks = self.assigned_tasks[ipt]
        # gprint("IDS LIST::::::: MANAGER::::%s" %ids_list)
        for ids in ids_list:
            # gprint("ids %s on assg tasks  %s"
            # %(ids, self.assigned_tasks[ipt].values()))
            if not ids in self.assigned_tasks[ipt].values():
                # bprint("Keys on ass tasks %s" %self.assigned_tasks[ipt].keys())
                for ico in self.assigned_tasks[ipt].keys():
                    value = self.assigned_tasks[ipt][ico]
                    if value is None:
                        # rprint("In process %s, task %s,  station %s" %(ipt,ico, ids))
                        ass_tasks.update({ico: ids})
                        break
        self.assigned_tasks[ipt] = ass_tasks
            #ids, loop, sta

        await asyncio.sleep(1)
        print("sta manager out %s" %ipt)
        return [ipt]

    def set_pst(self, ids, args):
        print("Basic pst")
        return [ids, args[1], args[2]]

    def set_init_args(self):
        print("Basic init args")
        return [None, None, None, None]

    def add_task(self, ids, ipt):
        self.proc_tasks[ipt] += [ids]

    def manage_tasks(self, ipt):
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # print("WS Gather data ok for %s" %ipt)
        v = 1
        tasks = []
        # bprint("Collect task ipt: %s" %ipt)
        try:
            #create signal manager <- GatherSignal
            #
            self.assigned_tasks[ipt]={}
            new_dict={}
            for i in range(self.lnproc):
                ico = self.set_ico()
                nd = {ico: None}
                #bprint("Ico generated %s" %nd)
                new_dict.update(nd)
            #rprint("New dict %s" %new_dict)
            self.assigned_tasks[ipt] = new_dict
            # rprint("Assigned tasks: %s"%self.assigned_tasks[ipt])
            for ico in self.assigned_tasks[ipt]:
                # Over limited tasks on process<=lnproc
                stax = self.set_init_args()
                sargs = [None, stax]
                # gprint("Code process: %s" %ipt)
                args = [ipt, ico, *sargs]
                task = loop.create_task(
                    coromask(
                        self.process_sta_task,
                        args,
                        simple_fargs_out)
                )
                task.add_done_callback(
                    functools.partial(renew,
                                      task,
                                      self.process_sta_task,
                                      simple_fargs_out)
                )
                tasks.append(task)
        except Exception as exec:
            print(
                "Error en collect_task, gather stations %s, error %s"
                %(ipt, exec))
            print(exec)
            raise exec

        #Task manager
        try:
            args=[ipt]
            print("Args to sta manager %s" %args)
            task=loop.create_task(
                coromask(
                self.process_sta_manager,
                args,
                simple_fargs_out)
            )
            task.add_done_callback(
                functools.partial(renew,
                                  task,
                                  self.process_sta_manager,
                                  simple_fargs_out)
            )
            tasks.append(task)
        except Exception as exec:
            print("Error en collect_task, manager %s, error %s" %(ipt, exec))
            print(exec)
            raise exec
        if not loop.is_running():
            #loop.run_until_complete(asyncio.gahter(*tasks))
            loop.run_forever()




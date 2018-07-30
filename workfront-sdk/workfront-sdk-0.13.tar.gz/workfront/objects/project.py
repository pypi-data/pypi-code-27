from workfront.objects.codes import WFObjCode
from workfront.objects.generic_object_param_value import WFParamValuesObject
import workfront.objects.task
import workfront.objects.program


def crt_from_template(wf, template_id, name):
    js = {
        "name": name,
        "templateID": template_id
    }
    data = wf.post_object(WFObjCode.project, js)
    return WFProject(wf, data["ID"])


def create_new(wf, params):
    data = wf.post_object(WFObjCode.project, params)
    return WFProject(wf, data["ID"])


class WFProject(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the project
        '''
        super(WFProject, self).__init__(wf, WFObjCode.project, idd)

    def get_template_id(self):
        '''
        @return: the template id of the project. None if it was not created
        from a template.
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id, ["template:ID"])
        try:
            return r.json()["data"]["template"]["ID"]
        except Exception:
            return None

    def get_tasks(self):
        '''
        @return: A list of WFTask objects which belongs to this project. The
        tasks are returned in order (first task in project will be first in the
        list; last task in project will be last in this list).
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id, ["tasks:ID",
                                                           "tasks:name",
                                                           "tasks:taskNumber"])
        self._raise_if_not_ok(r)

        ord_tasks = r.json()["data"]["tasks"]
        ord_tasks.sort(key=lambda tsk: tsk["taskNumber"])

        tasks = []
        for tdata in ord_tasks:
            t = workfront.objects.task.WFTask.create_from_js(self.wf, tdata)
            tasks.append(t)
        return tasks

    def get_program(self):
        r = self.wf.get_object(self.obj_code, self.wf_id, ["program:ID"])
        self._raise_if_not_ok(r)

        proj_id = r.json()["data"]["program"]["ID"]
        return workfront.objects.program.WFProgram(self.wf, proj_id)

    def get_program_id(self):
        r = self.wf.get_object(self.obj_code, self.wf_id, ["program:ID"])
        self._raise_if_not_ok(r)

        return r.json()["data"]["program"]["ID"]

    def get_portfolio_id(self):
        r = self.wf.get_object(WFObjCode.project, self.wf_id, ["portfolio:ID"])
        self._raise_if_not_ok(r)

        return r.json()["data"]["portfolio"]["ID"]

    def set_portfolio_id(self, portfolio_id):
        self.set_fields({'portfolioID': portfolio_id})

    def set_status(self, status):
        '''
        @param idd: project id
        @param status: status code
        '''
        r = self.wf.put_object(WFObjCode.project,
                               self.wf_id,
                               {"status": status})
        self._raise_if_not_ok(r)

    def reset_until(self, reset_point_task_id, func=None):
        '''
        @summary: From back until the reset point (included) the task are reset
        (set to new state). Tasks that has 'Automatic' custom form 
        @param reset_point_task_id: point until the tasks will be re-set to
        new. This task is also set to new.
        @param func: function to be applied to each WF task is being reset.
        '''
        tasks = self.get_tasks()

        reset_point_task = filter(lambda t: t.wf_id == reset_point_task_id,
                                  tasks)
        if len(reset_point_task) == 0:
            raise RuntimeError("Reset point %s not find in project %s",
                               reset_point_task_id, self.wf_id)
        reset_point_task = reset_point_task[0]
        reset_task_number = tasks.index(reset_point_task)

        # Go through the tasks in reverse order and reset them
        for index in range(len(tasks)-1, reset_task_number-1, -1):
            task = tasks[index]
            task.reset()
            if func is not None:
                func(task)

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF PROJECT from the API.
        It should at least have the "ID" field.
        '''
        p = WFProject(wf, js["ID"])
        p._init_fields(js)
        return p

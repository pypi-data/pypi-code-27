from termcolor import colored, cprint


C = lambda x,y : colored(' ' + x+ ' ', on_color='on_'+ y) if x.strip() else ''

class TestBase:
    ins = []
    def __init__(self, target):
        self.target = target
        self.__class__.ins.append(self)

    def __del__(self):
        if self in self.__class__.ins:
            self.__class__.ins.remove(self)


    @classmethod
    def run(cls, Obj):

        hs = [i.target for i in cls.ins]
        if hasattr(Obj, '__name__'):
            cls.log("use :" , Obj.__name__)
        res = Obj.test(hs)
        if res:
            cls.log(res)

    @classmethod
    def log(cls,*args, label='green', **kwargs):
        """
        l,g,bg
        """
        head = colored("[+]", 'red', attrs=['bold'])
        print(head, *args, **kwargs)
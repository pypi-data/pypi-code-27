import graphene

class sharedql:
    query_classes = []
    
    def __init__(self, cls):
        self.cls = cls
        sharedql.query_classes.append(cls)

    def __call__(self):
        self.cls()
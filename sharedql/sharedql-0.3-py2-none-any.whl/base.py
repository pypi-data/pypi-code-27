import graphene

class sharedql_query:
    query_classes = []
    
    def __init__(self, cls):
        self.cls = cls
        sharedql_query.query_classes.append(cls)

    def __call__(self):
        self.cls()

class sharedql_mutation:
    mutation_classes = []
    
    def __init__(self, cls):
        self.cls = cls
        sharedql_mutation.mutation_classes.append(cls)

    def __call__(self):
        self.cls()

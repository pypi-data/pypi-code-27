EXPECTED = {'E': {'extensibility-implied': False,
       'imports': {},
       'object-classes': {},
       'object-sets': {},
       'tags': 'AUTOMATIC',
       'types': {'A': {'type': 'ENUMERATED',
                       'values': [('a', 0), ('b', 1), None, ('c', 2)]},
                 'B': {'type': 'ENUMERATED',
                       'values': [('a', 1),
                                  ('b', 2),
                                  ('c', 0),
                                  None,
                                  ('d', 3)]},
                 'C': {'type': 'ENUMERATED',
                       'values': [('a', 0),
                                  ('b', 1),
                                  None,
                                  ('c', 3),
                                  ('d', 4)]},
                 'D': {'type': 'ENUMERATED',
                       'values': [('a', 0), ('z', 25), None, ('d', 1)]},
                 'E': {'type': 'ENUMERATED',
                       'values': [('a', 1),
                                  ('b', 2),
                                  ('c', 0),
                                  ('d', 3),
                                  ('e', 25),
                                  ('f', 4),
                                  None,
                                  ('g', 5)]},
                 'F': {'type': 'ENUMERATED', 'values': [('a', 0), None]}},
       'values': {}}}
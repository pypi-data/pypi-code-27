from ixnetwork_restpy.connection import Connection


class Multivalue(object):
    def __init__(self, connection, href):
        self._connection = connection
        self._properties = {
            'href': href,
        }
        self._pattern = None
        self._nests = Nests(self._connection, self._properties['href'])

    def _format_value(self, value):
        if self._properties['format'] == 'bool':
            return '%s%s' % (value[0].upper(), value[1:])
        return value

    @property
    def pattern(self):
        """The current pattern represented as a string.

        Returns: str
        """
        if self._pattern is None:
            self._select()
        if self._properties['pattern'] == 'singleValue':
            self._pattern = self._format_value(self._properties['singleValue']['value'])
        elif self._properties['pattern'] == 'counter':
            start = self._format_value(self._properties['counter']['start'])
            step = self._format_value(self._properties['counter']['step'])
            if self._properties['counter']['direction'] == 'decrement':
                self._pattern = 'Dec: %s, %s' % (start, step)
            else:
                self._pattern = 'Inc: %s, %s' % (start, step)
        elif self._properties['pattern'] == 'valueList':
            self._pattern = 'List: %s' % (', '.join(self._properties['values']))
        elif self._properties['pattern'] == 'repeatableRandomRange':
            min_value = self._properties['repeatableRandomRange']['min']
            max_value = self._properties['repeatableRandomRange']['max']
            step_value = self._properties['repeatableRandomRange']['step']
            seed = self._properties['repeatableRandomRange']['seed']
            self._pattern = 'Randr: %s, %s, %s, %s' % (min_value, max_value, step_value, seed)
        elif self._properties['pattern'] == 'repeatableRandom':
            fixed_value = self._properties['repeatableRandom']['fixed']
            mask_value = self._properties['repeatableRandom']['mask']
            seed = self._properties['repeatableRandom']['seed']
            count = self._properties['repeatableRandom']['count']
            self._pattern = 'Randb: %s, %s, %s, %s' % (fixed_value, mask_value, seed, count)
        elif self._properties['pattern'] == 'random':
            self._pattern = 'Rand'
        elif self._properties['pattern'] == 'alternate':
            self._pattern = 'Alt: %s' % self._format_value(self._properties['alternate']['value'])
        elif self._properties['pattern'] == 'customDistributed':
            values = []
            for value_pair in self._properties['customDistributed']['values']:
                values.append('(%s, %s)' % (self._format_value(value_pair['arg1']), value_pair['arg2']))
            algorithm = self._properties['customDistributed']['algorithm']
            mode = self._properties['customDistributed']['mode']
            self._pattern = 'Dist: %s, %s, [%s]' % (algorithm, mode, ','.join(values))
        elif self._properties['pattern'] == 'custom':
            increments = []
            if 'increment' in self._properties['custom'].keys():
                self._add_increments(increments, self._properties['custom']['increment'])
            start = self._properties['custom']['start']
            step = self._properties['custom']['step']
            self._pattern = 'Custom: %s, %s, [%s]' % (start, step, ','.join(increments))
        elif self._properties['pattern'] == 'string':
            self._pattern = self._properties['string']['pattern']
        return self._pattern

    def _add_increments(self, increments, increment):
        for item in increment:
            child_increments = []
            if 'increment' in item.keys():
                self._add_increments(child_increments, item['increment'])     
            increments.append('(%s, %s, [%s])' % (item['value'], item['count'], ','.join(child_increments)))

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return self.pattern

    def __eq__(self, other):
        return self.pattern == other

    @property
    def info(self):
        info = 'Multivalue: %s\n' % self.source
        info += '\tFormat: %s\n' % self.format
        info += '\tCount: %s\n' % self.count
        info += '\tValid Patterns: %s\n' % ' '.join(self.availablePatterns)
        return info

    @property
    def format(self):
        self.pattern
        return self._properties['format']

    @property
    def source(self):
        self.pattern
        return self._properties['source']
    
    @property
    def count(self):
        self.pattern
        return self._properties['count']

    @property
    def availablePatterns(self):
        """list(str): returns a list of methods in this class that are valid for setting a pattern for this multivalue"""
        self.pattern
        for unsupported in ['shared', 'subset']:
            self._properties['availablePatterns'].remove(unsupported)
        return self._properties['availablePatterns']

    @property
    def availableEnums(self):
        """list(str): if the format of the multivalue is enum this will return a list of possible enum choices that can be used when setting patterns"""
        self.pattern
        return self._properties['enums']

    @property
    def values(self):
        """list(str): returns a list of the values encapsulated by the pattern, format and count"""
        self.pattern
        return self._properties['values']

    def single(self, value):
        """Set the pattern to a single value"""
        self._set_pattern('singleValue', {'value': value})

    def alternate(self, alternating_value):
        """Set the pattern to alternating"""
        self._set_pattern('alternate', {'value': alternating_value})

    def increment(self, start_value=None, step_value=None):
        """Set the pattern to incrementing"""
        payload = {
            'direction': 'increment'
        }
        if start_value is not None:
            payload['start'] = start_value
        if step_value is not None:
            payload['step'] = step_value
        self._set_pattern('counter', payload)

    def decrement(self, start_value=None, step_value=None):
        """Set the pattern to decrementing"""
        payload = {
            'direction': 'decrement'
        }
        if start_value is not None:
            payload['start'] = start_value
        if step_value is not None:
            payload['step'] = step_value
        self._set_pattern('counter', payload)

    def value_list(self, values):
        """Set the pattern to valueList"""
        self._set_pattern('valueList', {'values': values})

    def randomRange(self, min_value=None, max_value=None, step_value=None, seed=None):
        """Set the repeatable random range pattern

        Args:
            min_value (str): Minimum value according to the format property
            max_value (str): Maximum value according to the format property
            step_value (str): Step value accoroding to the format property
            seed (int): Seed value
        """
        payload = {
            'min': min_value,
            'max': max_value,
            'step': step_value,
            'seed': seed
        }
        self._set_pattern('repeatableRandomRange', payload)

    def randomMask(self, fixed_value=None, mask_value=None, seed=None, count=None):
        """Set the repeatable random pattern

        Args:
            fixed_value (str): Minimum value according to the format property
            mask_value (str): Maximum value according to the format property
            seed (int): Seed value 
            count (int): Count value
        """        
        payload = {
            'fixed': fixed_value,
            'mask': mask_value,
            'seed': seed,
            'count': count
        }
        self._set_pattern('repeatableRandom', payload)

    def random(self):
        self._set_pattern('random')

    def distributed(self, algorithm=None, mode=None, values=None):
        """Set the pattern to customDistributed

        Args:
            algorithm (str[enum:percentage|weighted|autoEven|autoGeometric]): The algorithm of the distribution
            mode (str[enum:perDevice|perTopology|perPort]): The mode of the distribution
            values (list[tuple(value, weight)]): A list of values and weights
        """
        formatted_values = None
        if values is not None:
            formatted_values = []
            for value in values:
                formatted_values.append({'arg1': self._format_value(value[0]), 'arg2': value[1]})
        payload = {
            'algorithm': algorithm,
            'mode': mode,
            'values': formatted_values
        }
        self._set_pattern('customDistributed', payload)

    def valueList(self, values=None):
        """Set the pattern to valueList
        """
        formatted_values = None
        if values is not None:
            formatted_values = []
            for value in values:
                formatted_values.append(self._format_value(value))
        payload = {
            'values': formatted_values
        }
        self._set_pattern('valueList', payload)

    def string(self, string_pattern=None):
        """Set the pattern to a string pattern

        Args:
            string_pattern (str): A string pattern
                Examples:
                    Test-{Inc:1,1}
                    Test-{"A", "B", "C"}
                    hex_{Dec:0xFFFF}
                    Test-{Inc:100}-{"A", "B"}-{Dec:3, 1, 3}
        """
        payload = {
            'pattern': string_pattern
        }
        self._set_pattern('string', payload)

    def custom(self, start_value=None, step_value=None, increments=None):
        """Set the pattern to custom

        Args:
            start_value (str): A start value according to the format
            step_value (str): A step value according to the format
            increments (list[tuple(value, count, list[increments])]): Customize the start and step values by adding sibling and/or nested increments.
                The list contains 0..n increments.
                Each increment is a tuple that consists of a value according to the format, a count and any nested increments.
        """
        payload = {
            'start': start_value,
            'step': step_value
        }
        self._set_pattern('custom', payload)
        self._connection._delete('%s/custom/increment' % self._properties['href'])
        self._add_custom_increments('%s/custom' % self._properties['href'], increments)
        self._select()

    def _add_custom_increments(self, href, increments):
        if increments is not None:
            href = '%s/increment' % href
            for increment in increments:
                payload = {
                    'value': increment[0],
                    'count': increment[1]
                }
                
                response = self._connection._create(href, payload)
                self._add_custom_increments(response['links'][0]['href'], increment[2])

    @property
    def nests(self):
        return self._nests

    def _set_pattern(self, pattern, payload=None):
        self.pattern
        href = '%s/%s' % (self._properties['href'], pattern)
        if payload is not None:
            for key in payload.copy():
                if payload[key] is None:
                    payload.pop(key)
        if bool(payload) is False:
            payload = None
        if pattern == self._properties['pattern']:
            self._connection._update(href, payload)
        elif payload is not None:
            self._connection._create(href, payload)
        else:
            self._connection._update(self._properties['href'], {'pattern': pattern})
        self._select()

    def _select(self):
        payload = {
            'selects': [
                {
                    'from': self._properties['href'],
                    'properties': ['*'],
                    'children': [
                        {
                            'child': '(singleValue|alternate|random|repeatableRandom|repeatableRandomRange|counter|valueList|custom|customDistributed|increment|string)',
                            'properties': ['*'],
                            'filters': []
                        }
                    ],
                    'inlines': []
                }
            ]
        }
        end = self._properties['href'].index('ixnetwork') + len('ixnetwork')
        url = '%s/operations/select' % self._properties['href'][0:end]
        self._properties = self._connection._execute(url, payload)[0]

class Nests(object):
    def __init__(self, connection, href):
        self._connection = connection
        self._href = '%s/nest' % href
        self._response = []
        
        # description, owner, enabled, step

    def __iter__(self):
        self._response = self._connection.read(self._href)
        self._current = 1
        return self

    def __next__(self):
        if self._current > len(self._response):
            raise StopIteration
        self._nest = self._response[self._current - 1]
        return self
    
    def next(self):
        return self.__next__()

    def _get_value(self, name):
        if self._current > len(self._response):
            return None
        return self._nest[name]

    def _set_value(self, name, value):
        if self._current > len(self._response):
            return
        self._nest[name] = value
        self._connection._update('%s/%s' % (self._href, self._nest['id']), {name: value})

    @property
    def description(self):
        return self._get_value('description')

    @property
    def owner(self):
        return self._get_value('owner')

    @property
    def enabled(self):
        return self._get_value('enabled')
    @enabled.setter
    def enabled(self, enabled):
        self._set_value('enabled', enabled)

    @property
    def step(self):
        return self._get_value('step')
    @step.setter
    def step(self, value):
        self._set_value('step', value)


class Module:
    def set(self, uid, name, code):
        '''
        Browse the database for existing module.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        module_in_db = self.cursor.execute(self.query_list.select_module.text, (uid, name, code)).fetchone()
        if module_in_db is not None:
            self.uid = module_in_db[0]
            self.name = module_in_db[1]
            self.code = module_in_db[2]
            self.description = module_in_db[3]
            self.active = True
            self.output_control.print(self.output_control.DATA_SET, ('Module','name', self.name, ', Code: ', self.code,'',''))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Module', 'name', self.name, ', Code: ', self.code,'',''))

    def insert(self):
        '''
        Browse the database for existing module.
        1) If not found, saves the module to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        module_in_db = self.cursor.execute(self.query_list.select_module.text, ('%', self.name, self.code)).fetchone()
        if module_in_db is None:
            self.cursor.execute(self.query_list.insert_module.text, (self.name, self.code, self.description, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Module', 'name', self.name, ', Code: ', self.code,'',''))
        else:
            self.uid = module_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Module', 'name', self.name, ', Code: ', self.code,'',''))

    def __init__(self, query_list = None, cursor=None, uid='%', name='%', code='%', description = '%', active = True, output_control=None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.name = name
        self.code = code
        self.description = description
        self.active = active
        self.output_control = output_control

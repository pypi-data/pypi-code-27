class ExternalModule:
    def set(self, uid, name, active):
        '''
        Browse the database for existing external module.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        ext_module_in_db = self.cursor.execute(self.query_list.select_external_module.text, (uid, name)).fetchone()
        if ext_module_in_db is not None:
            self.uid = ext_module_in_db[0]
            self.name = ext_module_in_db[1]
            self.active = ext_module_in_db[2]
            self.output_control.print(self.output_control.DATA_SET, ('External module', 'ID: ', self.uid, ', Name: ', self.name,'',''))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('External module', 'ID: ', self.uid, ', Name: ', self.name,'',''))

    def insert(self):
        '''
        Browse the database for existing external module.
        1) If not found, saves the external module to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        ext_module_in_db = self.cursor.execute(self.query_list.select_external_module.text, ('%', self.name)).fetchone()
        if ext_module_in_db is None:
            self.cursor.execute(self.query_list.insert_external_module.text, (self.name, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('External module', 'ID: ', self.uid, ', Name: ', self.name,'',''))       
        else:
            self.uid = ext_module_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('External module', 'ID: ', self.uid, ', Name: ', self.name,'',''))    
            
    def __init__(self, query_list = None, cursor=None, uid='%', name='%', active = True, output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.name = name
        self.active = active
        self.output_control = output_control

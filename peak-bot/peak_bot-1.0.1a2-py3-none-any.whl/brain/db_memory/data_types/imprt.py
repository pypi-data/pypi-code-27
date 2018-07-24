class Imprt:
    def set(self, uid, command_id, external_module_id):
        '''
        Browse the database for existing import.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        imprt_in_db = self.cursor.execute(self.query_list.select_import.text, (uid, command_id, external_module_id)).fetchone()
        if imprt_in_db is not None:
            self.uid = imprt_in_db[0]
            self.command_id = imprt_in_db[1]
            self.external_module_id = imprt_in_db[2]
            self.output_control.print(self.output_control.DATA_SET, ('Import', 'Command ID: ', self.command_id, ', External Module\'s ID: ', self.external_module_id,'',''))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Import', 'Command ID: ', self.command_id, ', External Module\'s ID: ', self.external_module_id,'',''))

    def insert(self):
        '''
        Browse the database for existing import.
        1) If not found, saves the import to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        imprt_in_db = self.cursor.execute(self.query_list.select_import.text, ('%', self.command_id, self.external_module_id)).fetchone()
        if imprt_in_db is None:
            self.cursor.execute(self.query_list.insert_import.text, (self.command_id, self.external_module_id))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Import', 'Command ID: ', self.command_id, ', External Module\'s ID: ', self.external_module_id,'',''))        
        else:
            self.uid = imprt_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Import', 'Command ID: ', self.command_id, ', External Module\'s ID: ', self.external_module_id,'',''))
    def __init__(self, query_list = None, cursor = None, uid = '%', command_id = '%', external_module_id = '%', output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.command_id = command_id
        self.external_module_id = external_module_id
        self.output_control = output_control

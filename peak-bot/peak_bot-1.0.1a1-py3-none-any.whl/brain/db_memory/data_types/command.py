class Command:
    def set(self, uid, module_id, name, code, programming_language):
        '''
        Browse the database for existing command.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        command_in_db = self.cursor.execute(self.query_list.select_command.text, (uid, module_id, name, code, programming_language)).fetchone()
        if command_in_db is not None:
            self.uid = command_in_db[0]
            self.module_id = command_in_db[1]
            self.name = command_in_db[2]
            self.code = command_in_db[3]
            self.programming_language = command_in_db[4]
            self.definition = command_in_db[5]
            self.script_url = command_in_db[6]
            self.description = command_in_db[7]
            self.active = command_in_db[8]
            self.output_control.print(self.output_control.DATA_SET, ('Command ', 'ID: ', self.uid, ', Name: ', self.name, ', Code: ', self.code))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Command ', 'ID: ', self.uid, ', Name: ', self.name, ', Code: ', self.code))

    def insert(self):
        '''
        Browse the database for existing command.
        1) If not found, saves the command to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        command_in_db = self.cursor.execute(self.query_list.select_command.text, ('%', self.module_id, self.name, self.code, self.programming_language)).fetchone()
        if command_in_db is None:
            self.cursor.execute(self.query_list.insert_command.text, (self.module_id, self.name, self.code, self.programming_language, self.definition, self.script_url, self.description, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Command ', 'ID: ', self.uid, ', Name: ', self.name, ', Code: ', self.code))
        else:
            self.uid = command_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Command ', 'ID: ', self.uid, ', Name: ', self.name, ', Code: ', self.code))

    def __init__(self, query_list = None, cursor = None, uid = '%', module_id = '%', name = '%', code = '%', programming_language='%', definition = '', script_url = '', description = '', active = True, output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.module_id = module_id
        self.name = name
        self.code = code
        self.programming_language = programming_language
        self.definition = definition
        self.script_url = script_url
        self.description = description
        self.active = active
        self.output_control = output_control

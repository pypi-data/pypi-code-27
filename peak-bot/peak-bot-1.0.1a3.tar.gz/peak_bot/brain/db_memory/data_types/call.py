class Call:
    def set(self, uid, command_id, language_id, response, active):
        '''
        Browse the database for existing call.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        call_in_db = self.cursor.execute(self.query_list.select_call.text, (uid, command_id, language_id, response, active)).fetchone()
        if call_in_db is not None:
            self.uid = call_in_db[0]
            self.command_id = call_in_db[1]
            self.language_id = call_in_db[2]
            self.response = call_in_db[3]
            self.active = call_in_db[4]
            self.output_control.print(self.output_control.DATA_SET, ('Call ', 'ID: ', self.uid, ', Command ID: ', self.command_id,', Response: ', self.response))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Call ', 'ID: ', self.uid, ', Command ID: ', self.command_id,', Response: ', self.response))

    def insert(self):
        '''
        Browse the database for existing call.
        1) If not found, saves the call to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        call_in_db = self.cursor.execute(self.query_list.select_call.text, ('%', self.command_id, self.language_id, self.response, self.active)).fetchone()
        if call_in_db is None:
            self.cursor.execute(self.query_list.insert_call.text, (self.command_id, self.language_id, self.response, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Call ', 'ID: ', self.uid, ', Command ID: ', self.command_id,', Response: ', self.response))
        else:
            self.uid = call_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Call ', 'ID: ', self.uid, ', Command ID: ', self.command_id,',, Response: ', self.response))
            
            
    def __init__(self, query_list = None, cursor = None, uid = '%', command_id = '%', language_code = 'en-US', response = 0,  active = True, output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.command_id = command_id
        self.language_id = 1 
        lang_in_db = self.cursor.execute(query_list.select_language.text, ('%', language_code, '%', "True")).fetchone()
        if lang_in_db is not None:
            self.language_id = lang_in_db[0]
        self.response = response
        self.active = active
        self.output_control = output_control

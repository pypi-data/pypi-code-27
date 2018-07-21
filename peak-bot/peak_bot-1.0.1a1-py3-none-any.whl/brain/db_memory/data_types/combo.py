class Combo:
    def set(self, uid, call_id, word_id, variable_length, optional, position):
        '''
        Browse the database for existing combo.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        combo_in_db = self.cursor.execute(self.query_list.select_combo.text, (uid, call_id, word_id, position)).fetchone()
        if combo_in_db is not None:
            self.uid = combo_in_db[0]
            self.call_id = combo_in_db[1]
            self.word_id = combo_in_db[2]
            self.variable_length = combo_in_db[3]
            self.optional = combo_in_db[4]
            self.position = combo_in_db[5]
            self.output_control.print(self.output_control.DATA_SET, ('Combo ', 'Call ID: ', self.call_id, ', Word ID: ', self.word_id,', Position: ', self.position))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Combo ', 'Call ID: ', self.call_id, ', Word ID: ', self.word_id,', Position: ', self.position))

    def insert(self):
        '''
        Browse the database for existing combo.
        1) If not found, saves the combo to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        combo_in_db = self.cursor.execute(self.query_list.select_combo.text, ('%', self.call_id, self.word_id, self.position)).fetchone()
        if combo_in_db is None:
            self.cursor.execute(self.query_list.insert_combo.text, (self.call_id, self.word_id, self.variable_length, self.optional, self.position))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Combo ', 'Call ID: ', self.call_id, ', Word ID: ', self.word_id,', Position: ', self.position))
        else:
            self.uid = combo_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Combo ', 'Call ID: ', self.call_id, ', Word ID: ', self.word_id,', Position: ', self.position))

    def __init__(self, query_list = None, cursor = None, uid = '%', call_id = '%', word_id = '%', variable_length = '%', optional = '%', position = '%', output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.call_id = call_id
        self.word_id = word_id
        self.variable_length = variable_length
        self.optional = optional
        self.position = position
        self.output_control = output_control

class Word:
    def set(self, uid, text, active):
        '''
        Browse the database for existing word.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        word_in_db = self.cursor.execute(self.query_list.select_word.text, (uid, text, active)).fetchone()
        if word_in_db is not None:
            self.uid = word_in_db[0]
            self.text = word_in_db[1]
            self.active = word_in_db[2]
            self.output_control.print(self.output_control.DATA_SET, ('Word ','ID: ', self.uid,' Text: ', self.text,'',''))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Word ', 'ID: ', self.uid,' Text: ', self.text,'',''))

    def insert(self):
        '''
        Browse the database for existing word.
        1) If not found, saves the word to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        word_in_db = self.cursor.execute(self.query_list.select_word.text, ('%', self.text, self.active)).fetchone()
        if word_in_db is None:
            self.cursor.execute(self.query_list.insert_word.text, (self.text, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Word ', 'ID: ', self.uid,' Text: ', self.text,'',''))
        else:
            #if self.text == 'var':
            self.uid = word_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Word ', 'ID: ', self.uid,' Text: ', self.text,'',''))

    def __init__(self, query_list = None, cursor = None, uid = '%', text = '%', active = True, output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.text = text
        self.active = active
        self.output_control = output_control

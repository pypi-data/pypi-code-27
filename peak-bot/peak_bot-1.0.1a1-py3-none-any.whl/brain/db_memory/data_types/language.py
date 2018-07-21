class Language:
    def set(self, uid, code, name, active):
        '''
        Browse the database for existing language.
        if not found, populates variables with provided values, 
        makes them ready for insert() function.
        '''
        lang_in_db = self.cursor.execute(self.query_list.select_language.text, (uid, code, name, active)).fetchone()
        if lang_in_db is not None:
            self.uid = lang_in_db[0]
            self.code = lang_in_db[1]
            self.name = lang_in_db[2]
            self.active = lang_in_db[3]
            self.output_control.print(self.output_control.DATA_SET, ('Language','name', self.name,'','','',''))
        else:
            self.output_control.print(self.output_control.DATA_NOT_FOUND, ('Language', 'name', self.name,'','','',''))
            print('Language with ID:{0} not found.'.format(self.uid))

    def insert(self):
        '''
        Browse the database for existing language.
        1) If not found, saves the language to the database,
        and populates the uid variable with newly formed id in the database.
        2) If found, populates the uid variable with found id in the database. 
        '''
        lang_in_db = self.cursor.execute(self.query_list.select_language.text, (self.uid, self.code, self.name, self.active)).fetchone()
        if lang_in_db is None:
            self.cursor.execute(self.query_list.insert_language.text, (self.code, self.name, self.active))
            self.uid = self.cursor.lastrowid
            self.output_control.print(self.output_control.DATA_INSRT, ('Language', 'name', self.name,'','','',''))
        else:
            self.uid = lang_in_db[0]
            self.output_control.print(self.output_control.DATA_EXISTS, ('Language', 'name', self.name,'','','',''))

    def __init__(self, query_list = None, cursor=None, uid='%', code = '%', name='%', active = True, output_control = None):
        self.query_list = query_list
        self.cursor = cursor
        self.uid = uid
        self.code = code 
        self.name = name
        self.active = active
        self.output_control = output_control


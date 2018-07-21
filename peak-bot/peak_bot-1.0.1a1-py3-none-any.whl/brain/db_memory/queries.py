import sqlite3

class Query:
    def __init__(self, usage, supported_engines, description, text):
        self.usage = usage
        self.supported_engines = supported_engines
        self.description = description
        self.text = text

class QueryList:
    create_languages = Query(1, ('SQLite3', 'MySQL'), 'This table holds the languages of the command calls.', \
        'CREATE TABLE IF NOT EXISTS languages ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        name VARCHAR(32), \
        code VARCHAR(16), \
        active BOOLEAN \
        );')

    create_modules = Query(1, ('SQLite3', 'MySQL'), 'Creates the "modules", a table which holds the names of command chunks.', \
        'CREATE TABLE IF NOT EXISTS modules ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        name VARCHAR(32), \
        code VARCHAR(16), \
        description VARCHAR(1024), \
        active BOOLEAN \
        );')

    create_commands = Query(1, ('SQLite3', 'MySQL'), 'Creates the "commands" table. Multiple commands are binded by one module.', \
        'CREATE TABLE IF NOT EXISTS commands ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        module_id INTEGER NOT NULL, \
        name VARCHAR(32), \
        code VARCHAR(16), \
        programming_language VARCHAR(32), \
        definition VARCHAR(8192), \
        script_url VARCHAR(128), \
        description VARCHAR(1024), \
        active BOOLEAN DEFAULT True, \
        FOREIGN KEY (module_id) REFERENCES modules(id) \
        );')

    create_external_modules = Query(1, ('SQLite3', 'MySQL'), 'Creates table for usage with commands - to be imported at execution', \
        'CREATE TABLE IF NOT EXISTS external_modules ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        name VARCHAR(32), \
        active BOOLEAN \
        );')

    create_imports = Query(1, ('SQLite3', 'MySQL'), 'Table for connecting commands and external modules', \
        'CREATE TABLE IF NOT EXISTS imports ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        external_module_id INTEGER NOT NULL, \
        command_id INTEGER NOT NULL, \
        active BOOLEAN DEFAULT True, \
        FOREIGN KEY (external_module_id) REFERENCES external_modules(id) \
        FOREIGN KEY (command_id) REFERENCES commands(id) \
        );')

    create_calls = Query(1, ('SQLite3', 'MySQL'), 'Creates the "calls" table, used for connecting words into a single command combo - call', \
        'CREATE TABLE IF NOT EXISTS calls ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        command_id INTEGER NOT NULL, \
        language_id INTEGER NOT NULL, \
        response INTEGER DEFAULT 0, \
        active BOOLEAN DEFAULT True, \
        FOREIGN KEY (language_id) REFERENCES languages(id) \
        FOREIGN KEY (command_id) REFERENCES commands(id) \
        );')

    create_words = Query(1, ('SQLite3', 'MySQL'), 'Creates the "words" table.', \
        'CREATE TABLE IF NOT EXISTS words ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        text VARCHAR(128), \
        active BOOLEAN DEFAULT True \
        );')

    create_combos = Query(1, ('SQLite3', 'MySQL'), 'Creates the "combos" table. Used for connecting calls and words.', \
        'CREATE TABLE IF NOT EXISTS combos ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        call_id INTEGER NOT NULL, \
        word_id INTEGER NOT NULL, \
        variable_length INTEGER DEFAULT 0, \
        optional BOOLEAN DEFAULT False, \
        position INTEGER, \
        FOREIGN KEY (word_id) REFERENCES words(id) \
        FOREIGN KEY (call_id) REFERENCES call(id) \
        );')

    insert_language = Query(3, ('SQLite3', 'MySQL'), 'Inserts a single language.', \
        'INSERT INTO languages \
        (code, name, active) \
        VALUES \
        (?, ?, ?);')

    insert_module = Query(3, ('SQLite3', 'MySQL'), 'Inserts a single module.', \
        'INSERT INTO modules \
        (name, code, description, active) \
        VALUES \
        (?, ?, ?, ?);')

    insert_command = Query(1, ('SQLite3', 'MySQL'), 'Inserts a single command.', \
        'INSERT INTO commands \
        (module_id, name, code, programming_language, definition, script_url, description,  active) \
        VALUES \
        (?, ?, ?, ?, ?, ?, ?, ?);')

    insert_external_module = Query(3, ('SQLite3', 'MySQL'), 'Inserts a single external module.', \
        'INSERT INTO external_modules \
        (name, active) \
        VALUES \
        (?, ?);')

    insert_import = Query(8, ('SQLite3', 'MySQL'), 'Inserts a single command combo.', \
        'INSERT INTO imports \
        (command_id, external_module_id) \
        VALUES \
        (?, ?);')

    insert_call = Query(7, ('SQLite3', 'MySQL'), 'Inserts a single call.', \
        'INSERT INTO calls \
        (command_id, language_id, response, active) \
        VALUES \
        (?, ?, ?, ?);')
    
    insert_word = Query(8, ('SQLite3', 'MySQL'), 'Inserts a single word.', \
        'INSERT INTO words \
        (text, active) \
        VALUES \
        (?, ?);')

    insert_combo = Query(8, ('SQLite3', 'MySQL'), 'Inserts a single command combo.', \
        'INSERT INTO combos \
        (call_id, word_id, variable_length, optional, position) \
        VALUES \
        (?, ?, ?, ?, ?);')

    select_language = Query(4, ('SQLite3', 'MySQL'), 'Selects a language from passed variables.', \
        'SELECT lan.* \
        FROM languages AS lan \
        WHERE lan.id LIKE ? \
        AND lan.code LIKE ? \
        AND lan.name LIKE ? \
        AND lan.active == ?;')

    select_module = Query(4, ('SQLite3', 'MySQL'), 'Selects a single module', \
        'SELECT mod.* \
        FROM modules AS mod \
        WHERE mod.id LIKE ? \
        AND mod.name LIKE ? \
        AND mod.code LIKE ? \
        AND mod.active == "True";')

    select_external_module = Query(4, ('SQLite3', 'MySQL'), 'Selects a single external module', \
        'SELECT em.* \
        FROM external_modules AS em \
        WHERE em.id LIKE ? \
        AND em.name LIKE ? \
        AND em.active == "True";')

    select_external_modules_by_command_id = Query(10, ('SQLite3', 'MySQL'), 'Used for collecting modules before import', ' \
        SELECT em.name AS nameo \
        FROM imports AS im \
        LEFT JOIN external_modules AS em ON em.id = im.external_module_id \
        WHERE im.command_id = ?;')


    select_module_by_name = Query(2, ('SQLite3', 'MySQL'), 'Gets the modules uid.', ' \
        SELECT mo.id AS module_id \
        FROM modules AS mo \
        WHERE mo.name = ?;')

    select_import = Query(8, ('SQLite3', 'MySQL'), 'Selects an import ', \
        'SELECT im.* \
        FROM imports AS im \
        WHERE im.id LIKE ? \
        AND im.command_id LIKE ? \
        AND im.external_module_id LIKE ? \
        AND im.active == "True";')

    select_command = Query(8, ('SQLite3', 'MySQL'), 'Selects a command from db', \
        'SELECT com.* \
        FROM commands  AS com \
        WHERE com.id LIKE ? \
        AND com.module_id LIKE ? \
        AND com.name LIKE ? \
        AND com.code LIKE ? \
        AND com.programming_language LIKE ? \
        AND com.active == "True";')

    select_command_by_id = Query(10, ('SQLite3', 'MySQL'), 'Used for finding a single command with provided id', ' \
        SELECT co.name AS name, co.programming_language AS language, co.definition AS definition \
        FROM commands AS co \
        WHERE co.id = ?;')

    select_combo = Query(8, ('SQLite3', 'MySQL'), 'Selects a combo from db', \
        'SELECT cmb.* \
        FROM combos AS cmb \
        WHERE cmb.id LIKE ? \
        AND cmb.call_id LIKE ? \
        AND cmb.word_id LIKE ? \
        AND cmb.position LIKE ?;')

    select_call = Query(8, ('SQLite3', 'MySQL'), 'Selects a call from db', \
        'SELECT cal.* \
        FROM calls AS cal \
        WHERE cal.id LIKE ? \
        AND cal.command_id LIKE ? \
        AND cal.language_id LIKE ? \
        AND cal.response LIKE ? \
        AND cal.active == ?;')

    select_word = Query(8, ('SQLite3', 'MySQL'), 'Selects a word from db', \
        'SELECT wor.* \
        FROM words AS wor \
        WHERE wor.id LIKE ? \
        AND wor.text LIKE ? \
        AND wor.active == ?;')

    select_words_by_position = Query(10, ('SQLite3', 'MySQL'), 'Gets the combinations of words.', ' \
        SELECT w.text \
        FROM command AS com \
        LEFT JOIN combos AS ca ON ca.command_id = co.id \
        LEFT JOIN words AS w ON ca.word_id = w.id \
        WHERE ca.position = ?, co.module_id = ? AND w.language_id = ?;')

    select_responses_by_command_id = Query(10, ('SQLite3', 'MySQL'), 'Used for collecting responses with a recognized command', ' \
        SELECT resp.response, wo.text \
        FROM calls AS resp \
        LEFT JOIN commands AS co ON resp.command_id = co.id \
        LEFT JOIN combos AS cb ON cb.call_id = resp.id \
        LEFT JOIN words AS wo ON wo.id = cb.word_id \
        LEFT JOIN languages AS lan on resp.language_id = lan.id \
        WHERE co.id = ? AND resp.response BETWEEN ? AND ? AND lan.active = "True" \
        ORDER BY resp.response;')

    select_known_calls = Query(10, ('SQLite3', 'MySQL'), 'Used for collecting pre-recognition calls', '    SELECT\n')

    def construct_skc_query(self, number_of_calls):
        '''
        Updates "select_known_calls" query to return exact number of calls.
        '''
        for word_index in range(1, number_of_calls+1):
            self.select_known_calls.text = '{0}    wo{1}.text, cb{1}.variable_length,\n'.format(self.select_known_calls.text, str(word_index))

        self.select_known_calls.text = '{0}    co.id\n\
    FROM modules AS mod\n\
    LEFT JOIN commands AS co ON co.module_id = mod.id \n\
    LEFT JOIN calls AS cal ON cal.command_id = co.id AND cal.response BETWEEN 0 AND 25 \n\
    LEFT JOIN languages AS lan ON lan.id = cal.language_id \n'.format(self.select_known_calls.text)

        for word_index in range(1, number_of_calls+1):
            self.select_known_calls.text = '{0}    LEFT JOIN combos AS cb{1} ON cb{1}.call_id = cal.id AND cb{1}.position == {1}\n\
    LEFT JOIN words AS wo{1} ON wo{1}.id = cb{1}.word_id\n'.format(self.select_known_calls.text, str(word_index))

        self.select_known_calls.text = '{0}    WHERE mod.active = "True" AND lan.active = "True" \n\
        GROUP BY cal.id, wo1.text;'.format(self.select_known_calls.text)


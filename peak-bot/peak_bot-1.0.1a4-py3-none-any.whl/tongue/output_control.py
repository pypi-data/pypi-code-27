import os

class OutputControl:
    #STRING_NAME = ('Some text', output GROUP, VERBOSITY required to print, success SIGN)
    signs = {}
    txt_to_speech = False
    '''
    output_groups:
    main/general = 0
    peak_bot = 1
    file_handler = 2
    database = 3
    listener = 4 
    transcriber = 5
    executioner = 6 
    '''
    verbosity_level = 0
    output_groups = ()
    signs = ('     ', ' >>  ', ' ??  ', ' !!  ', ' **  ', ' xx  ', '  ')
    '''
    Main/General
    output_group: 0
    '''
    WELCOME_MSG = ('Application started.', 0, 3, 1)
    PLAT_NOT_SUP = ('{0} is not supported.', 0, 6, 5)
    SPLITTER = ('-------------------------------', 0, 3, 6)
    '''
    PeakBot class
    output_group: 1 
    '''
    SETT_FILE_NOT_FOUND = ('File {0} not found.', 2, 3, 4)
    USING_DB = ('Using database {0}', 1, 2, 1)
    ENGINE_NOT_SUP = ('Engine {0} is not yet supported. Skipping...', 1, 3, 0)
    UNKNOWN_ENGINE = ('Unknown database engine: {0}. Skipping...', 1, 3, 0)
    INACTIVE_DB = ('Database {0} is not active. Skipping...', 1, 3, 0)
    DIR_WITH_COMS = ('{0} directory contains commands', 1, 3, 1)
    COM_LST = ('Command list: {0}', 1, 5, 0)
    SKIP_DIRS = ('Skip directories: {0}', 1, 4, 0)
    NO_JSON_FILE = ('{0} does not have a coresponding .json file in "/modules"', 1, 3, 4)
    DB_PATH_SET_ATT = ('Attempting to set the path for the database...', 1, 3, 4)
    DB_PATH_SET = ('Database path is set.', 1, 3, 1)
    DB_PATH_NOT_SET = ('Database path could not be set.\nException: {0}', 1, 1, 5)
    JSON_EXISTS = ('Directory {0} have a coresponding file {1}{2}.json', 1, 3, 1)
    MOD_COM_SET_ATT = ('Attempting to set modules and commands...', 1, 3, 4)
    MOD_COM_SET = ('Modules and commands are set.', 1, 3, 1)
    MOD_COM_NOT_SET = ('Modules and commands could not be set.\nException: {0}.', 1, 1, 5)
    INIT_ATT = ('Attempting to initiate the {0}...', 1, 3, 4)
    INIT = ('{0} is initiated.', 1, 3, 1)
    NOT_INIT = ('{0} could not be initiated.\nException: {1}.', 1, 1, 5)
    SPEECH_PRC = ('Speech is processed.', 1, 3, 1)
    COM_EXEC = ('Command is executed.', 1, 3, 1)
    COM_NOT_EXEC = ('Command could not be executed.\nException: {0}.', 1, 1, 5)
    DB_CON_CLOSED = ('Database connection is closed.', 1, 3, 1)
    '''
    FileHandler class
    output_group: 2 
    '''
    COULD_NOT_LOAD = ('Could not load the file {0}.', 2, 3, 4)
    FILE_NOT_FOUND = ('File {0} not found.', 2, 3, 4)
    FILE_PATH = ('File path: {0}.', 2, 4, 0)
    FILE_CHECK = ('Checking if {0} is a file...', 2, 3, 2)
    FILE_ADDED_COMS = ('Content of .json file is added to the list of commands.', 2, 3, 1)
    WRONG_EXT = ('Not .JSON extension. Skipping...', 2, 3, 5)
    IS_DIR = ('{0} is a directory.', 2, 3, 1)
    '''
    Database class
    output_group: 3
    '''
    COM_OK = ('Command {0} in working condidion.', 3, 3, 1)
    EXM_OK = ('External module {0} in working condition.', 3, 3, 1)
    IMPRT_OK = ('Import {0} in working condition {1}.', 3, 3, 1) 
    COM_DICT = ('Command dictionary: {0}', 3, 5, 0)
    QUERY_CONSTR = ('Constructed query with {0} skc level', 3, 3, 1)
    '''
    Listener class
    output_group:4 
    '''
    EARS_READY = ('Ready for input...', 4, 1, 1)
    VOICE_DTC = ('Voice detected. Listening started...', 4, 4, 1)
    SILENCE = ('Silence: {0}/25.', 4, 4, 4)
    '''
    Transcriber class
    output_group: 5
    '''
    TRANSC = ('Transcribing {0}:', 5, 2, 0)

    BFR_COM_WORDS = ('Command words (before formatting): {0}', 5, 4, 0)
    AFT_COM_WORDS = ('Command words (after formatting): {0}', 5, 4, 0)
    CALL_LISTN = ('Listening for a command call...', 5, 1, 4)
    READ_CRED = ('Reading credentials...', 5, 3, 4)
    SEND_AUDIO = ('Uploading audio file...', 5, 3, 4)
    LOCAL_RECOGN = ('Recognizing localy...', 5, 3, 4)
    EXPECT_CALLS = ('Expected calls: {0}.', 5, 5, 1)
    RSTORE_EXPECT_CALLS = ('Restoring expected calls to a bare state...', 5, 3, 4)
    VAR_POS_EQ = ('variable[0]({0}) + total_index({1}) =  var_position({2})', 5, 5, 0)
    VAR_INDEX = ('Variable index: {0}', 5, 4, 0)
    VAR_POS = ('Variable position: {0}', 5, 4, 0)
    VAR_INSTD = ('Inserted variable at position {0}', 5, 3, 1)
    TOTAL_INDEX = ('Total index: {0}', 5, 4, 0)
    CHECK_CALL = ('Check call: {0}', 5, 3, 6)
    NO_OF_VARS = ('Number of variables: {0}', 5, 4, 0)
    SKIP_POSS = ('Skip positions: {0}', 5, 4, 0)
    WORD_GOOD = ('Word {0} at position {1} good, not a variable.', 5, 3, 1)
    CUR_ARGS = ('Current command arguments: {0}', 5, 4, 0)
    PASSD_VAR = ('Passed variable {0} at position {1}.', 5, 3, 1)
    WORD_MISS = ('Word missmatch at position {0}: {1} != {2}.', 5, 3, 4)
    POS_NOT_FOUND = ('Position {0} not found in list of variable positions {1}.', 5, 3, 4)
    UNEQUAL_WORDS_NO = ('This command have {0} words. {1} provided.', 5, 3, 4)
    CALL_PASS = ('Call passed.', 5, 3, 1)
    CALL_DIDNT_PASS = ('Call didn\'t pass.', 5, 3, 5)
    RECOGN_COMS = ('Recognized commands:', 5, 1, 0)
    RECOGN_COM_DATA = ('ID: {0}  Text: {1}', 5, 1, 1)
    NO_COMS_PASSED = ('No commands passed', 5, 1, 5)
    TIMED_OUT = ('Audio read timed out.\nException: {0}', 5, 1, 5)
    COULD_NOT_UNDRS = ('Could not understand audio.\nException: {0}', 5, 1, 5)
    COULD_NOT_TRANS = ('Counld not transmit audio.\nException: {0}', 5, 1, 5)
    '''
    Executor class
    output_group: 6
    '''
    MOD_ATT_IMPORT = ('Attempting to import module "{0}".', 6, 1, 1)
    MOD_IMPORT = ('Module "{0}" imported.', 6, 3, 1)
    MOD_NOT_IMPORT = ('Unable to import the module: "{0}".\nException: {1}.', 6, 1, 5)
    SUC_RESP = ('{0}', 5, 0, 0)
    '''
    Data classes
    output_group: 7
        - Languages
        - Modules
        - External Modules
        - Imports
        - Commands
        - Calls
        - Combos
        - Words
    '''
    DATA_SET = ('{0} with values {1}{2}{3}{4}{5}{6} is set.', 7, 3, 1)
    DATA_NOT_FOUND = ('{0} with values {1}{2}{3}{4}{5}{6} is not found in the database.', 7, 1, 5)
    DATA_INSRT = ('{0} with values {1}{2}{3}{4}{5}{6} is inserted.', 7, 3, 1)
    DATA_EXISTS = ('{0} with values {1}{2}{3}{4}{5}{6} is already in the database.', 7, 3, 1)
    '''
    Input class
    output_group: 8
    '''
    CHAR_ADDED = ('Added "{0}" to position {1}.', 8, 4, 1)
    

    '''
    Output function with 5 level verbosity (0-4).
    Level 5 is comment alike... It never prints.
    '''
    def print(self, output, args=()):
        '''
	Checks if verbosity is larger than potential output.
	Prepares "text" variable to be printed.
	Checks if it shoud print or speak the response.
        '''
        if int(output[2]) <= int(self.verbosity_level) and output[1] in self.output_groups:
            text = output[0].format(*args)
            if self.txt_to_speech:
                pass
            else:
                # To remove tab-signs from command output: 
                # Uncomment:
                #print('{0}'.format(text))
                # Comment out:
                print('{0}{1}'.format(self.signs[output[3]], text))


    def __init__(self, output_groups, verbosity_level):
        self.output_groups = output_groups
        self.verbosity_level = verbosity_level
    

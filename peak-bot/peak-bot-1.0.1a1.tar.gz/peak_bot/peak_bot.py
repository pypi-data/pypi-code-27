#!/usr/bin/env python3
import os
import sys

from .brain.db_memory.database import Database
from .brain.fs_memory.file_handler import FileHandler
from .brain.processing.command_finder import CommandFinder
from .brain.processing.executor import Executor
from .ears.listener import Listener
from .ears.input_control import InputControl
from .antenna.google_transcriber import GoogleTranscriber
from .antenna.bing_transcriber import BingTranscriber

class PeakBot:
    module_dicts = []
    command_list = []
    database_path = ""
    def set_database_path(self):
        '''
        Function for extracting a database path.
        Assumes only one database is active.
        '''
        oc = self.output_control
        oc.print(oc.DB_PATH_SET_ATT)
        try:
            if 'databases' in self.settings_dict:
                for database_data in self.settings_dict['databases']:
                    if database_data['database_active'] == 'True':
                        if database_data['database_engine'] == 'sqlite3':
                            self.database_path = ('{0}{1}'.format(database_data['database_dir'], database_data['database_filename']))
                            oc.print(oc.USING_DB, (database_data['database_filename'],))
                            break
                        elif database_data['database_engine'] in ('MS SQL Server', 'MySql', 'MySql/MariaDB', 'MongoDB'):
                            oc.print(oc.ENGINE_NOT_SUP, (database_data['database_engine'],))
                        else:
                            oc.print(oc.UNKNOWN_ENGINE, (database_data['database_engine'],))
                    else:
                        oc.print(oc.INACTIVE_DB, (database_data['database_filename']),)
                oc.print(oc.DB_PATH_SET)
        except Exception as e:
            oc.print(oc.DB_PATH_NOT_SET, (str(e),))

    def set_modules_and_commands(self, library_path):
        '''
        This function is looking for modules and commands in the defined directory.
        'get_modules_and_commands' is using 'FileHandler' class, and it's 'check_path' function.
        '''
        oc = self.output_control
        oc.print(oc.MOD_COM_SET_ATT)

        (self.module_dicts, self.directories) = self.file_handler.read_library(library_path) 
        print('GOT MODULE DICT: \n' + str(self.module_dicts))
        print('\n \n GOT DIRECTORIES: \n' + str(self.directories))
        try:
            for directory in self.directories:
                print('\n DIRECTORY CHECK: \n' + str(directory))
                if ('{0}.json'.format(directory)) in os.listdir(library_path):
                    oc.print(oc.JSON_EXISTS, (directory, library_path, directory))
                    (command_dict, self.skip_directories) = self.file_handler.read_library('{0}{1}/'.format(library_path, directory))
                    self.command_list.append(command_dict)
                    oc.print(oc.DIR_WITH_COMS, (directory,))
                    oc.print(oc.SKIP_DIRS, (self.skip_directories,))
                else:
                    print('\n ITS DIRECTORY...: \n')
                    self.skip_directories.append(directory)
                    self.directories.remove(directory)
                    oc.print(oc.NO_JSON_FILE, (directory,))
            oc.print(oc.MOD_COM_SET)
        except Exception as e:
            oc.print(oc.MOD_COM_NOT_SET, (str(e),))
                
    def init_database(self):
        '''
        Initiates a new database.
        '''
        self.output_control.print(self.output_control.INIT_ATT, ('database',))
        #try:
        if True:
            self.database = Database(self.output_control, self.database_path, self.languages_dict, self.module_dicts, self.command_list)
            self.output_control.print(self.output_control.INIT, ('Database',))
        else:
            e=''
        #except Exception as e:
            self.output_control.print(self.output_control.NOT_INIT, ('Database', str(e)))

    def init_listener(self, audio_wav_path):
        '''
        Initiates a new listener.
        '''
        self.output_control.print(self.output_control.INIT_ATT, ('listener',))
        try:
            self.listener = Listener(self.output_control, self.audio_settings_dict, audio_wav_path)
            self.output_control.print(self.output_control.INIT, ('Listener',))
        except Exception as e:
            self.output_control.print(self.output_control.NOT_INIT, ('Listener', str(e)))
            sys.exit()

    def init_command_finder(self):
        '''
        Initiates a new command_finder.
        '''
        self.output_control.print(self.output_control.INIT_ATT, ('command finder',))
        try:
            self.command_finder = CommandFinder(self.output_control, self.input_control, self.database)
            self.output_control.print(self.output_control.INIT, ('Command finder',))
        except Exception as e:
            self.output_control.print(self.output_control.NOT_INIT, ('Command finder', str(e)))
            sys.exit()

    def init_transcriber(self, expected_calls):
        '''
        Initiates a new transcriber.

        '''
        speech_apis_dict = {
                'GOOGL': GoogleTranscriber,
                'BING': BingTranscriber
                }
        self.output_control.print(self.output_control.INIT_ATT, ('transcriber',))
        try:
            for speech_api in self.settings_dict['speech_apis']:
                if speech_api['active']:
                    transcriber_type = speech_apis_dict[speech_api['code']]
                    break
            
            self.transcriber = transcriber_type(self.output_control, self.audio_settings_dict, expected_calls)
            self.output_control.print(self.output_control.INIT, ('Transcriber',))
        except Exception as e:
            self.output_control.print(self.output_control.TRANSC_NOT_INIT, ('Transcriber', str(e)))
            sys.exit()


    def init_executor(self):
        '''
        Initiates a new executor.
        '''
        self.output_control.print(self.output_control.INIT_ATT, ('executor',))
        try:
            self.executor = Executor(self.output_control, self.database)
            self.output_control.print(self.output_control.INIT, ('Executor',))
        except Exception as e:
            self.output_control.print(self.output_control.NOT_INIT, ('Executor', str(e),))
            sys.exit()

        #RESPONSE INDEX IS THE NUMBER OF ALREADY INPUTED ARGUMENTS (BY INITIAL CALL) - RARELY 0!!! 
    def get_additional_args(self, response_index):
        additional_args = ()
        noninitial_responses = self.database.cursor.execute(self.database.query_list.select_responses_by_command_id.text, (str(self.command_finder.command_id), 26, 50)).fetchall()
        if not noninitial_responses:
            noninitial_responses = ''
        while response_index < len(noninitial_responses):
            response_number = noninitial_responses[response_index][0]
            response_text = noninitial_responses[response_index][1]

            #This was COUNT(word.id) .... ????
            #number_of_words = noninitial_responses[response_index][2]

            '''
            expected_answers=()
            if number_of_words>1:
                for words_index in range(number_of_words):
                    expected_answers = expected_answers + (noninitial_responses[response_index + words_index][1],)
                response_index += number_of_words
            '''

            response_index += 1
            self.listener.record()
            #if len(expected_answers) > 0:
                #send to transcriber as expected words!!!

            alternatives = self.transcriber.transcribe(self.listener.file_path)
            response = self.input_control.format_input(alternatives[0].transcript)
            additional_args = additional_args + (response[0],)
        return additional_args

    def run_peak_bot(self):
        self.exit = False
        while not self.exit:
            self.listener.record()
            alternatives = self.transcriber.transcribe(self.listener.file_path)
            transcript = ''

            '''
            Higher confidence:
            confidence = 0.3
            for alternative in alternatives:
                if alternative.confidence > confidence:
                    transcript = alternative.transcript
                    confidence = alternative.confidence

            By index:
            '''
            for alternative in alternatives:
                if alternative.confidence>0.9:
                    transcript = alternative.transcript
                    break

            self.output_control.print(self.output_control.BFR_COM_WORDS, (transcript,))
            response = self.input_control.format_input(transcript)
            self.output_control.print(self.output_control.AFT_COM_WORDS, (response,))
            self.command_finder.find_commands(response)
            args = self.command_finder.command_args
            args = args + self.get_additional_args(len(args))

            self.executor.execute_command(self.command_finder.command_id, args)
            self.database.connection.commit()
            self.exit = True

    def __init__(self, fundamental_directories, output_control):
        self.output_control = output_control
        oc = output_control
        self.file_handler = FileHandler(output_control)
        self.settings_dict = self.file_handler.load_from_path(fundamental_directories[0])
        self.audio_settings_dict = self.file_handler.load_from_path(fundamental_directories[1])  
        self.languages_dict = self.file_handler.load_from_path(fundamental_directories[2])
        self.input_control = InputControl(output_control)
        self.set_database_path()
        self.set_modules_and_commands(fundamental_directories[3])

        self.init_database()
        self.init_listener(fundamental_directories[4])
        self.init_command_finder()
        self.init_transcriber(self.command_finder.expected_calls)
        self.init_executor()

        self.run_peak_bot()

        self.database.connection.close()
        self.output_control.print(self.output_control.DB_CON_CLOSED)

import sqlite3
#import json

#LOCAL FILES
from .queries import QueryList
from .data_types.language import Language
from .data_types.module import Module
from .data_types.command import Command
from .data_types.external_module import ExternalModule
from .data_types.imprt import Imprt
from .data_types.call import Call 
from .data_types.word import Word
from .data_types.combo import Combo

class Database:
    skc_level = 0
    def create_structure(self):
        '''
        Creates a database, if one's structure is not already created.
        It is called on initial app start, or if database does not have a proper format.
        '''
        structure_queries_text = (
                self.query_list.create_languages.text,
                self.query_list.create_modules.text,
                self.query_list.create_external_modules.text,
                self.query_list.create_commands.text,
                self.query_list.create_imports.text,
                self.query_list.create_calls.text,
                self.query_list.create_words.text,
                self.query_list.create_combos.text)
        for structure_query_text in structure_queries_text:
            self.cursor.execute(structure_query_text)

    def insert_language_data(self, languages_dict):
        '''
        Initiates new Languages objects,
        populates their values from the languages_dict parameter,
        and saves them to the database.
        '''
        for language_data in languages_dict['languages']:
            language = Language(self.query_list,
                    cursor = self.cursor,
                    code = language_data['code'],
                    name = language_data['name'],
                    active = language_data['active'],
                    output_control = self.output_control)
            language.insert()

    def insert_command_data(self, command_data, module_uid):
        '''
        Initiates new Command, ExternalModules, Imprts, Calls, Words, Combos objects,
        populates their values from the command_data adn module_uid parameters,
        and saves them to the database.
        '''
        oc = self.output_control
        command = Command(self.query_list,
                cursor = self.cursor,
                module_id = module_uid,
                name = command_data['name'],
                code = command_data['code'],
                programming_language = command_data['programming_language'],
                script_url = command_data['script_url'],
                definition = command_data['definition'],
                description = command_data['description'],
                active = command_data['active'],
                output_control = self.output_control)
        command.insert()
        oc.print(oc.COM_OK, (command.name,))
        for external_module_data in command_data['external_modules']:
            external_module = ExternalModule(self.query_list,
                    cursor = self.cursor,
                    name = external_module_data['name'],
                    active = external_module_data['active'],
                    output_control = self.output_control)
            external_module.insert()
            oc.print(oc.EXM_OK, (external_module.name,))
            imprt = Imprt(self.query_list,
                    cursor = self.cursor,
                    command_id = command.uid,
                    external_module_id = external_module.uid,
                    output_control = self.output_control)
            imprt.insert()
            oc.print(oc.IMPRT_OK, (external_module.name, command.name))
        for call_data in command_data['calls']:
            if len(call_data['words'])>self.skc_level:
                self.skc_level = len(call_data['words'])
            call = Call(self.query_list,
                    cursor = self.cursor,
                    command_id = command.uid,
                    language_code = call_data['language'],
                    response = call_data['response'],
                    active = call_data['active'],
                    output_control = self.output_control)
            call.insert()
            for word_data in call_data['words']:
                word = Word(self.query_list,
                        cursor = self.cursor,
                        text = word_data['text'],
                        active = call.active,
                        output_control = self.output_control)
                word.insert()
                combo = Combo(self.query_list,
                        cursor = self.cursor,
                        call_id = call.uid,
                        word_id = word.uid,
                        variable_length = word_data['variable_length'],
                        optional = word_data['optional'],
                        position = word_data['position'],
                        output_control = self.output_control)
                combo.insert()

    def insert_module_data(self, module_dict):
        '''
        Initiates a new Module object,
        populates it's values from the module_dict parameter,
        saves it to the database,
        and calls Database.insert_command_data() on the same database.
        '''
        module_meta = module_dict['module']['metadata']
        module = Module(self.query_list,
                cursor = self.cursor,
                name = module_meta['name'],
                code = module_meta['code'],
                description = module_meta['description'],
                active = module_meta['active'],
                output_control = self.output_control)
        module.insert()
        for command_data in module_dict['module']['commands']:
            self.insert_command_data(command_data, module.uid)

    def __init__(self, output_control, file_path, languages_dict, module_dicts, command_list):
        self.output_control = output_control
        self.connection = sqlite3.connect(file_path)
        self.cursor = self.connection.cursor()
        self.query_list = QueryList()
        self.create_structure()
        self.insert_language_data(languages_dict)
        for module_dict  in module_dicts:
            self.insert_module_data(module_dict)

        for command_dicts in command_list:
            for command_dict in command_dicts:
                #self.output_control.print(self.output_control.COM_DICT, (json.dumps(command_dict, sort_keys=True, indent=2),))
                module_uid = self.cursor.execute(self.query_list.select_module_by_name.text, (command_dict['command']['module_name'],)).fetchone()
                self.insert_command_data(command_dict['command'], module_uid[0])

        self.query_list.construct_skc_query(self.skc_level)
        self.output_control.print(self.output_control.QUERY_CONSTR, (self.skc_level,))
        #self.connection.commit()

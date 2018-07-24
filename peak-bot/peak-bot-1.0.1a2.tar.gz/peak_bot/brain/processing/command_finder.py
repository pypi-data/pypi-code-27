import json
import os

#from pocketsphinx.pocketsphinx import Decoder

class CommandFinder:
    command_id = 0
    command_args = ()
    command_args_list = []
    check_calls = []
    passed_calls = []
    expected_calls = []

    def set_calls(self):
        '''
        Retreives command calls from the database.
        These calls are, later on, used for comparison with user input.
        Argument "sic_level" determines the number of words to be retreived 
        per command call. It should always be equal to the number 
        of words in the longest command call.
        '''
        #Select calls that are already written in the database: Only active, non-response (response = 0) commands.
        known_calls = (self.database.cursor.execute(self.database.query_list.select_known_calls.text)).fetchall()
        #Clean the variables
        self.check_calls = [] 
        current_call_text = ""
        current_call_vars = [] 
        for known_call in known_calls:
            call_id = known_call[len(known_call)-1]
            for position_in_tuple in range(0, len(known_call)-1, 2):
                call_word = known_call[position_in_tuple]
                call_variable_length = known_call[position_in_tuple+1]
                if call_word is not None:
                    if call_variable_length == 0:
                        current_call_text = current_call_text + known_call[position_in_tuple] + " "
                    elif call_variable_length > 0:
                        current_call_vars.append((int(position_in_tuple/2+1), call_variable_length))

            self.check_calls.append((current_call_text[:-1], tuple(current_call_vars), call_id))

            if current_call_text[:-1] not in self.expected_calls:
                self.expected_calls.append(current_call_text[:-1])
            current_call_text = ""
            current_call_vars = []
        self.output_control.print(self.output_control.EXPECT_CALLS, (self.expected_calls,))

    def __init__(self, output_control, input_control, database):
        self.output_control = output_control
        self.input_control = input_control
        self.database = database
        self.expected_calls = list(self.input_control.hardcoded_dict.keys())
        self.set_calls()

    def get_skip_positions(self, call_variables, check_words):
        oc = self.output_control
        total_index = 0 
        skip_positions = ()
        for variable in call_variables:
            var_position = variable[0] + total_index
            oc.print(oc.VAR_POS_EQ, (str(variable[0]), str(total_index), str(var_position)))
            var_length = variable[1]
            for var_index in range(0, var_length):
                oc.print(oc.VAR_INDEX, (str(var_index),))
                oc.print(oc.VAR_POS, (str(var_position),))
                skip_positions = skip_positions + (var_position + var_index,)
                check_words.insert(var_position + var_index + 1, 'var_space')
                oc.print(oc.VAR_INSTD, (var_position + var_index,))
            total_index = total_index + var_length - 1
            oc.print(oc.TOTAL_INDEX, (str(total_index),))
        oc.print(oc.SKIP_POSS, (str(skip_positions),))
        return skip_positions

    def call_passed(self, command_call, skip_positions, check_words):
        '''
        This function checks if the passed command_call matches the "explicit" users input.
        It's doing so by comparing lengths first and values second.
        This should be changed once the machine learning is implemented.
        '''
        oc = self.output_control
        cc = command_call
        #Check if the number of words are the same.

        if len(cc) == len(check_words):
            clear_index = 0
            for clear_position in range(len(cc)):
                if cc[clear_position] == check_words[clear_position - clear_index]:
                    oc.print(oc.WORD_GOOD, (cc[clear_position], clear_position + 1))

                elif (clear_position+1) in skip_positions:
                    oc.print(oc.PASSD_VAR, (cc[clear_position], clear_position + 1))
                    self.command_args = self.command_args + (cc[clear_position],)
                    clear_index += 1

                else:
                    oc.print(oc.WORD_MISS, (clear_position+1,cc[clear_position], check_words[clear_position-clear_index]))
                    oc.print(oc.POS_NOT_FOUND, (clear_position + 1, str(skip_positions)))
                    oc.print(oc.CALL_DIDNT_PASS)
                    return False
                    break

            if self.command_args != ():
                self.command_args_list.append(self.command_args)
                self.command_args = ()

            return True
        else:
            oc.print(oc.UNEQUAL_WORDS_NO, (len(check_words), len(cc)))
            oc.print(oc.CALL_DIDNT_PASS)
            return False

    def find_commands(self, result):
        oc = self.output_control
        ic = self.input_control
        oc.print(oc.AFT_COM_WORDS, (result,))
        skip_positions = ()
        for check_call in self.check_calls:
            check_words = check_call[0].split(" ")
            check_variables = check_call[1]
            number_of_check_variables = len(check_variables)
            oc.print(oc.SPLITTER)
            oc.print(oc.CHECK_CALL, (check_call,))
            oc.print(oc.SPLITTER)
            oc.print(oc.NO_OF_VARS, (number_of_check_variables,))
            skip_positions = self.get_skip_positions(check_call[1], check_words)
            if self.call_passed(result, skip_positions, check_words):
                self.passed_calls.append(check_call)

        #Check if any calls passed:
        if len(self.passed_calls)>0:

            if len(self.passed_calls)==1:
                self.command_id = self.passed_calls[0][2]
                    
                #Check if there are any passed arguments:
                if len(self.command_args_list)>0:
                    #Take the first (and only) tuple from command_args_list
                    self.command_args = self.command_args_list[0]

                oc.print(oc.RECOGN_COMS)
                for passed_call in self.passed_calls:
                    oc.print(oc.RECOGN_COM_DATA, (passed_call[2], passed_call[0]))

            #If multiple calls passed:
            else:
                for passed_call in self.passed_calls:
                    print(passed_call)
        #If no calls passed:
        else:
            oc.print(oc.NO_COMS_PASSED)
            #Prompt for a creation of new command.
        oc.print(oc.SPEECH_PRC)

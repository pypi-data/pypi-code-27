import sys

class InputControl:

    def concat_words(self, command_words, command_position):
        '''
        Invokes on 'concat'.
        Can concat multiple words or characters depending on a skip count. 

        '''
        command_words[command_position] = command_words[command_position] + command_words[command_position+1]
        del command_words[command_position+1]

    def upper_word(self, command_words, command_position):
        '''
        Invokes on 'upper'.
        Uppercases the whole word.
        '''
        command_words.insert(command_position, command_words[command_position].upper())
        del command_words[command_position+1]
        command_words.insert(len(command_words), '')

    def lower_word(self, command_words, command_position):
        '''
        Invokes on 'lower'.
        Lowercases the whole word.
        '''
        command_words.insert(command_position, command_words[command_position].lower())
        del command_words[command_position+1]
        command_words.insert(len(command_words), '')
    
    def capital_word(self, command_words, command_position):
        '''
        Invokes on 'capital'.
        Capitalizes the next word.
        If the first letter is already Uppercased,
        function reinserts the same word.
        '''
        command_words.insert(command_position, command_words[command_position].capitalize())
        del command_words[command_position+1]
        command_words.insert(len(command_words), '')

    def tilde(self, command_words, command_position):
        '''
        Invokes on 'tilde'.
        Adds tilde (~) character to the input.
        '''
        command_words.insert(command_position, '~')
        self.output_control.print(self.output_control.CHAR_ADDED, ('~', command_position))

    def slash(self, command_words, command_position):
        '''
        Invokes on 'slash'.
        Adds slash (/) character to the input.
        '''
        command_words.insert(command_position, '/')
        self.output_control.print(self.output_control.CHAR_ADDED, ('/', command_position))
    
    def multiply_words(self, command_words, command_position):
        '''
        Invokes in 'multiply'.
        Multiplication of the next 2 words.
        Tries to convert the input to floats and return their product.
        '''
        try:
            command_words[command_position] = float(command_words[command_position]) * float(command_words[command_position+1])
        except:
            pass

    def ignore_skip(self, command_words, command_position):
        '''
        Invokes on 'ignore'.
        Deactivates the rest of the words under the pre-activated skip.
        '''
        pass

    def skip(self, command_words, command_position):
        '''
        Invokes on "skip skip". 
        As the first skip is removed before the invokation, 
        the second is being ignored.

        '''
        pass
        

    hardcoded_dict = {
    'concat':concat_words,
    'upper':upper_word,
    'lower':lower_word,
    'capital':capital_word,
    'tilde':tilde,
    'slash':slash,
    'multiply':multiply_words,
    'ignore':ignore_skip,
    'skip':skip
    }

    def format_input(self, input_string):
        '''
        Input is being re-written by the usage of the "skip" variable.
        1) To write "skip", say the word twice: "skip skip"
        2) To concat multiple words/letters, say "skip [Number of the words/letters] [first_word] [second_word]..."
        3) To write a special character like %, say "skip percent"
        4) To concat this character with another word/letter, use it inside "skip INTEGER ...",
            For example, to write "10%" say "skip 2 10 percent"
        5) upper, lower, capital and other word modifiers need to be inside "skip", but they don't take a number of words/letters.
            Output of "skip 5 capital downloads slash hello . txt" is "Downloads/hello.txt"
            Output of "skip 5 downloads slash hello . txt" is "downloads/hello.txt"
            Output of "skip 6 capital downloads slash hello . txt" should be an error, - too few words. 
            Output of "skip 4 downloads slash hello . txt" should be an error, - too many words.
        '''

        try:
            oc = self.output_control
            cc  = input_string.rstrip().split(" ")
            oc.print(oc.BFR_COM_WORDS, cc)
            clear_position = 0
            command_count = 0
            while clear_position < len(cc):
                hardcoded_commands = []
                concat_tuple = ()
                if cc[clear_position] == 'skip':
                    del cc[clear_position]

                    if cc[clear_position] == 'skip':
                        pass

                    elif cc[clear_position] in self.hardcoded_dict.keys():
                        hardcoded_command = self.hardcoded_dict[cc[clear_position]]
                        del cc[clear_position]
                        hardcoded_command(self, cc, clear_position)

                    elif (cc[clear_position]).isdigit():
                        command_count = int(cc[clear_position])
                        del cc[clear_position]

                        for command_index in range(clear_position, clear_position + command_count):
                            if cc[command_index] in self.hardcoded_dict:
                                hardcoded_command = self.hardcoded_dict[cc[command_index]]
                                del cc[command_index]
                                hardcoded_command(self, cc, command_index)

                        command_index = 0
                        while command_index < command_count-1:
                            self.concat_words(cc, clear_position)
                            command_index +=1

                    else:
                        print('Command not found, or "skip" at the end.')
                        break
                clear_position += 1
            cc = list(filter(None, cc))
            return (cc)
        except:
            pass

    def __init__(self, output_control):
        self.output_control = output_control

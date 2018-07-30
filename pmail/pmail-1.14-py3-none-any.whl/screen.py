import os


# Abstraction of IO device
class Screen:
    # Set to true to prevent any output to console
    silent = False

    # Clears the screen
    @staticmethod
    def clear():
        if not Screen.silent:
            os.system('cls' if os.name == 'nt' else 'clear')

    # Waits for the user to enter a value
    @staticmethod
    def input(prompt="", allowed=[]):
        if not Screen.silent:
            finish = False
            value = None
            while not finish:
                value = input(prompt)
                finish = value.lower() in allowed if allowed else True
                if allowed and not finish:
                    print("Invalid value!")
            return value

    # Waits for the user to enter a number
    @staticmethod
    def inputnumber(prompt="", allowed=[]):
        if not Screen.silent:
            finish = False
            value = None
            while not finish:
                try:
                    text = input(prompt)
                    value = int(text)
                    finish = value in allowed if allowed else True
                except:
                    print("Invalid number!")
            return value

    @staticmethod
    def print(text=None):
        if not Screen.silent:
            if text:
                print(text)
            else:
                print()
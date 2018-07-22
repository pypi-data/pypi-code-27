import readline
from re import match


def ask(question):
    '''
    Infinite loop to get yes or no answer or quit the script.
    '''
    while True:
        ans = input(question)
        ans = ans.lower()
        if match('^y(es)?$', ans):
            return True
        elif match('^n(o)?$', ans):
            return False
        elif match('^q(uit)?$', ans):
            quit()
        else:
            print("%s is invalid. Enter (y)es, (n)o or (q)uit." % ans)

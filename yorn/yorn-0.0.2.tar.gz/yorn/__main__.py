import readline
from argparse import ArgumentParser
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


def main():
    parser = ArgumentParser(description='Answer yes or no to a question.')
    parser.add_argument("question", type=str, help="A question to ask.")
    args = parser.parse_args()

    question = str(args.question)
    if ask(question):
        print("You answered yes.")
    else:
        print("You answered no.")


if __name__ == '__main__':
    main()

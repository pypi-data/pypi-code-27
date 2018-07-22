from argparse import ArgumentParser
from .ask import ask


def main():
    parser = ArgumentParser(description='Answer yes or no to a question.')
    parser.add_argument("question", type=str, help="A question to ask.")
    args = parser.parse_args()

    question = args.question
    if ask(question):
        print("You answered yes.")
    else:
        print("You answered no.")


if __name__ == '__main__':
    main()

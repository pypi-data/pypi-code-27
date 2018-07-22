from argparse import ArgumentParser
from .ask import ask


def main():
    parser = ArgumentParser(description='Answer yes or no to a question.')
    parser.add_argument("question", type=str, help="A question to ask.")
    args = parser.parse_args()

    question = "\n" + args.question

    if ask(question):
        print("\nYou answered yes.\n")
    else:
        print("\nYou answered no.\n")


if __name__ == '__main__':
    main()

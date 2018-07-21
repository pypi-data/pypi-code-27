import argparse

from yorn.ask import ask


def main():
    parser = argparse.ArgumentParser(
        description='Answer yes or no to a given question.')
    parser.add_argument("question", type=str, help="A question to ask.")
    args = parser.parse_args()

    question = str(args.question)
    if ask(question):
        print("You answered yes.")
    else:
        print("You answered no.")


# this means that if this script is executed, then main() will be executed
if __name__ == '__main__':
    main()

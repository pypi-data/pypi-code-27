import fnmatch
import os
import re
import readline


def menu(options, chosen):
    '''
    Takes a list of options and selections as an argument and presents a
    checkbox menu with previously selected items still selected.

    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print("\nEnter option names (wildcards accepted), or numbers, to toggle " +
          "selections.\n" +
          "Enter t to toggle all, r to reset, a to accept selections, or q to" +
          " quit.\n")

    for option in options:
        index = options.index(option)
        print("{0:>1} {1:>2}) {2:}".format(chosen[index], index+1,  option))


def get_matches(list1, list2):
    '''
    Takes two lists and compares them, for each item in the first list we see
    how many items in the second list it matches with globbing or with explicit
    number selection (based on the human readable, not 0 indexing!).

    Returns a tuple:

    The first element of which is a list of indexes of the second list that the
    first list matches.

    The second of which is a boolean that indicates whether or not any items in
    the first list failed to match with any items in the second.

    The Third element of which is the item of the first list that didn't match
    against any items in the second list.

    '''
    boolean = False
    matches = []
    invalid = ""

    for items1 in list1:
        count = 0
        total = len(list2)
        for items2 in list2:
            index = list2.index(items2)
            number = index + 1
            number = str(number)
            regex = fnmatch.translate(items1)  # convert globs to regex
            if re.match(regex, items2) or re.match(regex, number):
                boolean = False
                matches.append(index)
            else:
                invalid = items1
                count += 1

        if count == total:
            boolean = True

    return (matches, boolean, invalid)


def chopt(options):
    ''' takes a list of options as an argument and returns a list of selected
    options from that list.'''
    # initialize marked to be same length as options but with empty items
    marked = [""] * len(options)
    chosen = []
    markall = False
    output = ""

    while True:

        menu(options, marked)

        if output:
            print(output)

        # get list of inputs split on spaces
        inputs = input("\n----> ").split(" ")

        if re.match('^t(oggle)?$', inputs[0]):
            invalid = False
            if markall:
                for o in options:
                    marked[options.index(o)] = ""
                    markall = False
            else:
                for o in options:
                    marked[options.index(o)] = "+"
                    markall = True
        elif re.match('r(eset)?$', inputs[0]):
            invalid = False
            for o in options:
                marked[options.index(o)] = ""
        elif re.match('a(ccept)?$', inputs[0]):
            invalid = False
            print()
            break
        elif re.match('q(uit)?$', inputs[0]):
            invalid = False
            print()
            quit()
        else:
            matches = get_matches(inputs, options)
            matched = matches[0]
            invalid = matches[1]
            invalid_input = matches[2]

            for m in matched:
                if marked[m]:
                    marked[m] = ""
                else:
                    marked[m] = "+"

            # check if all options are chosen or not
            for o in options:
                if marked[options.index(o)]:
                    markall = True
                else:
                    markall = False
                    break

        if invalid:
            fmt = "\n{0:>5} not found."
            msg = invalid_input
        else:
            fmt, msg = ("",)*2

        output = fmt.format(msg)

    for o in options:
        if marked[options.index(o)]:
            chosen.append(o)

    return chosen

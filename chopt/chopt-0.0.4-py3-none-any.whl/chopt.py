import fnmatch
import os
import re
import readline


def cats():
    '''
    CLEAR ALL THE SCREENS!
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def menu(options, chosen):
    '''
    Takes a list of options and selections as an argument and presents a
    checkbox menu with previously selected items still selected.
    '''
    cats()

    msg = '''
    Enter option names (wildcards accepted), or numbers (ranges accepted), to
    toggle selections.

    Enter t to toggle all, r to reset, a to accept selections, or q to quit.
    '''

    print(msg)

    for option in options:
        index = options.index(option)
        print("{0:>1} {1:>2}) {2:}".format(chosen[index], index+1,  option))


def insert_range(element, inputs, nums):
    '''
    Remove element of original list that defines range, then insert integers in
    the range of the first and last elements of a list created by the defining
    element of original list back into original list.
    '''
    inputs.remove(element)
    for n in range(nums[0], nums[len(nums) - 1] + 1):
        # append after remove, means we'll end up skipping the next
        # element, and we don't need to iterate over added elements.
        inputs.insert(0, str(n))
    return inputs


def get_ranges(inputs):
    '''
    Find any numeric ranges in a list. A numeric range is defined as two numbers
    separated either by two periods or a dash.

    If we find a numeric range element, use list comprehension to extract the
    integers, remove the original element, and then insert a new element for
    every number in that range back into the original list.
    '''
    for i in inputs:
        if re.match('^\d+\.\.\d+$', i):
            nums = [int(n) for n in i.split("..") if n.isdigit()]
            inputs = insert_range(i, inputs, nums)
        elif re.match('^\d+-\d+$', i):
            nums = [int(n) for n in i.split("-") if n.isdigit()]
            inputs = insert_range(i, inputs, nums)
    return inputs


def get_matches(inputs, options):
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

    for i in inputs:
        count = 0
        total = len(options)
        for j in options:
            index = options.index(j)
            number = index + 1
            number = str(number)
            regex = fnmatch.translate(str(i))  # convert globs to regex
            if re.match(regex, j) or re.match(regex, number):
                boolean = False
                matches.append(index)
            else:
                invalid = i
                count += 1

        if count == total:
            boolean = True

    return (matches, boolean, invalid)


def mark(matched, marked):
    for m in matched:
        if marked[m]:
            marked[m] = ""
        else:
            marked[m] = "+"
    return marked


def chkmrk(options, marked):
    # check if all options are chosen or not
    for o in options:
        if not marked[options.index(o)]:
            return False
    return True


def chopt(options):
    '''
    Takes a list of options as an argument and returns a list of selected
    options from that list.
    '''
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
            matches = get_matches(get_ranges(inputs), options)
            matched = matches[0]
            invalid = matches[1]
            invalid_input = matches[2]
            marked = mark(matched, marked)
            markall = chkmrk(options, marked)

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

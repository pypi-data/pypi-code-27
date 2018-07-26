import fnmatch
import os
import re
import readline


def prtheader():
    from textwrap import dedent, fill
    width = os.get_terminal_size()[0]
    head = '''
           Enter option names (wildcards accepted), or numbers (ranges accepted),
           to toggle selections.
           '''
    keys = '(t)oggle all, (r)esets, (a)ccept choices, (q)uit'
    msg = dedent(head).strip()
    print("\n" + fill(msg, width=width) + "\n\n" + keys + "\n")


def menu(options, chosen):
    from columns import prtcols
    '''
    Takes a list of options and selections as an argument and presents a
    checkbox menu with previously selected items still selected.
    '''
    optstrs = []
    os.system('cls') if os.name == 'nt' else os.system('clear')
    prtheader()
    for option in options:
        index = options.index(option)
        # print("{0:>1} {1:>2}) {2:}".format(chosen[index], index+1,  option))
        optstrs.append(chosen[index] + str(index + 1) + ") " + option)
    prtcols(optstrs, 10)


def insert_range(element, inputs, options, nums):
    '''
    Remove element of original list that defines range, then insert integers in
    the range of the first and last elements of a list created by the defining
    element of original list back into original list.
    '''
    # catch attempts to mark outside options
    if len(options) >= nums[len(nums) - 1]:
        inputs.remove(element)
        for n in range(nums[0], nums[len(nums) - 1] + 1):
            # append after remove, means we'll end up skipping the next
            # element, and we don't need to iterate over added elements.
            inputs.insert(0, str(n))
    return inputs


def get_ranges(inputs, options):
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
            inputs = insert_range(i, inputs, options, nums)
        elif re.match('^\d+\.\.$', i):
            nums = [int(n) for n in i.split("..") if n.isdigit()]
            nums.append(len(options))
            inputs = insert_range(i, inputs, options, nums)
        elif re.match('^\.\.\d+$', i):
            nums = [int(n) for n in i.split("..") if n.isdigit()]
            nums.insert(0, 1)
            inputs = insert_range(i, inputs, options, nums)
        elif re.match('^\d+-\d+$', i):
            nums = [int(n) for n in i.split("-") if n.isdigit()]
            inputs = insert_range(i, inputs, options, nums)
        elif re.match('^\d+-$', i):
            nums = [int(n) for n in i.split("-") if n.isdigit()]
            nums.append(len(options))
            inputs = insert_range(i, inputs, options, nums)
        elif re.match('^-\d+$', i):
            nums = [int(n) for n in i.split("-") if n.isdigit()]
            nums.insert(0, 1)
            inputs = insert_range(i, inputs, options, nums)
    return inputs


def get_matches(inputs, options):
    '''
    Compares two lists.

    For each item in the first list we see how many items in the second list match
    - with globbing or number selection.

    Returns a tuple:

    The first element of which is a list of indexes of the second list that the
    first list matches.

    The second is a list of items of the first list that failed to match
    against any items in the second list.

    The third is a boolean that indicates whether or not any items in
    the first list failed to match with any items in the second.
    '''
    matches = []
    invalid = []
    failed = False

    for i in inputs:
        count = 0
        total = len(options)
        for j in options:
            index = options.index(j)
            number = index + 1
            number = str(number)
            regex = fnmatch.translate(str(i))  # convert globs to regex
            if re.match(regex, j) or re.match(regex, number):
                matches.append(index)
            else:
                count += 1

        # if we failed to match an input against any of the options.
        if count == total:
            invalid.append(i)
            failed = True

    return matches, invalid, failed


def mark(matched, chosen):
    '''
    Populate list of chosen options based on output of get_matches
    '''
    for m in matched:
        if chosen[m] == " + ":
            chosen[m] = "   "
        elif chosen[m] == "   ":
            chosen[m] = " + "
    return chosen


def chkmrk(options, chosen):
    '''
    Check if all options are chosen or not.
    '''
    for o in options:
        if chosen[options.index(o)] == "   ":
            return False
    return True


def chopt(options):
    '''
    Takes a list of options as an argument and returns a list of selected
    options from that list.
    '''
    # initialize chosen to be same length as options but with empty items
    chosen = ["   "] * len(options)
    markall = False
    output = ""

    while True:
        failed = False

        menu(options, chosen)

        if output:
            print(output)

        # get list of inputs split on spaces
        inputs = input("\n----> ").split(" ")

        if re.match('^t(oggle)?$', inputs[0], re.IGNORECASE):
            if markall:
                for o in options:
                    chosen[options.index(o)] = "   "
            else:
                for o in options:
                    chosen[options.index(o)] = " + "
        elif re.match('r(eset)?$', inputs[0], re.IGNORECASE):
            for o in options:
                chosen[options.index(o)] = "   "
        elif re.match('a(ccept)?$', inputs[0], re.IGNORECASE):
            # list comprehension that returns all chosen options
            return [o for o in options if chosen[options.index(o)] == " + "]
        elif re.match('q(uit)?$', inputs[0], re.IGNORECASE):
            return
        else:
            inputs = get_ranges(inputs, options)
            matched, invalid, failed = get_matches(inputs, options)
            chosen = mark(matched, chosen)

        markall = chkmrk(options, chosen)

        if failed:
            fmt = "\nINVALID INPUTS: {}"
            msg = ", ".join(invalid)
        else:
            fmt, msg = ("",)*2

        output = fmt.format(msg)

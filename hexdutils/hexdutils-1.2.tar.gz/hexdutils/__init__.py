from random import randint

__hex_letters= {"a":10,
        "b":11,
        "c":12,
        "d":13,
        "e":14,
        "f":15}

__alphabet = [" "]+[x for x in "abcdefghijklmnopqrstuvwxyz"]

def intohex(number, hex_prefix=False, uppercase=False):
    if type(number) is not int:
        raise TypeError("Value to convert must be int")
    def hexdivide(target):
        if target%16 > 9:
            for item in __hex_letters:
                if __hex_letters[item] == (target%16):
                    if uppercase:
                        return(item.upper())
                    else:
                        return(item)
            return(target%16)
        return(target%16)

    values = []
    while (number//16) is not 0:
        values.insert(0, hexdivide(number))
        number = number//16
    values.insert(0, hexdivide(number))
    if hex_prefix:
        return("0x" + ("".join(str(item) for item in values)))
    else:
        return("".join(str(item) for item in values))


def hextoint(target):
    if type(target) is not str:
        raise TypeError ("Argument must be str")
    decimals = []
    if target[:2] is "0x":
        target = target[2:]
    power_of_sixteen = len(target)-1
    for item in target:
        try:
            decimals.append(int(item)*(16**power_of_sixteen))
        except:
            if item.lower() in __hex_letters:
                decimals.append(__hex_letters[item.lower()]*(16**power_of_sixteen))
            else:
                raise ValueError (item, "doesn't belong to hex system")

        power_of_sixteen -= 1
    else:
        return(sum(decimals))


def abctohex(target, conversion="alphabet", verbose=False, encrypt=False):
    if type(target) is not str:
        raise ValueError("Target must be string")
    result_list = []
    result_str = None

    if conversion == "alphabet":
        for item in target:
                if item in [str(x) for x in list(range(0, 10))]:
                    result_list.append(item)
                else:
                    result_list.append(intohex(__alphabet.index(item.lower())))
                #print(item, __alphabet.index(item), intohex(__alphabet.index(item), True))
        #print("".join(item for item in result_list))
        result_str = "".join(item for item in result_list)

    elif conversion == "ord":
         for item in target:
                result_list.append(intohex(ord(item)))
                #print(item, ord(item), intohex(ord(item), True))
        #print("".join(item for item in result_list))
         result_str = "".join(item for item in result_list)
    else:
        raise ValueError("conversion has to be \'alphabet\' or \'ord\'")

    if encrypt is not False:
        if (type(encrypt) is not list):
            raise ValueError("encrypt value has to be a list")
        if (len(encrypt) < 2) or (len(encrypt) > 2):
            raise ValueError("encrypt must contain two integers: [max_range>5, number_of_iterations]")
        if (type(encrypt[0]) is not int) or (type(encrypt[1]) is not int):
            raise ValueError("encrypt list items have to be integers")
        if encrypt[0] < 5:
            raise ValueError("encrypt first argument has to be greater than 4")
        if encrypt[1] < 0:
            raise ValueError("encrypt second argument value has to be at least 0")

        result_list.clear()
        counter = 0
        original_result_str = result_str

        while(counter < encrypt[1]):
            randoval = str(randint(2, encrypt[0]))
            #print("Iteration #" + str(counter) + ":", result_str, "*", randoval)
            #print(hex_multiply(result_str, randoval, True ), "=", hex_multiply(result_str, randoval, False))
            result_str = hex_multiply(result_str, randoval, True )
            counter += 1
        if verbose:
           print("Executed", counter, "iteration(s). Result is:\n" + result_str, "\nFrom:", original_result_str)
        return(result_str)
    return(result_str)



def hex_add(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        print("#1 arg type:", type(first),"\n#2 arg type:", type(second))
        raise TypeError ("Addend type must be str. Use intohex(int value)")
    result = hextoint(first) + hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


def hex_subtract(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError ("Addend type must be str. Use intohex(int value)")
    result = hextoint(first) - hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


def hex_multiply(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        print("#1 arg type:", type(first),"\n#2 arg type:", type(second))
        raise TypeError ("Addend type must be str. Use intohex(int value)")
    result = hextoint(first) * hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

def hex_divide(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError ("Addend type must be str. Use intohex(int value)")
    result = hextoint(first) // hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


def hex_floor(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError ("Addend type must be str. Use intohex(int value)")
    result = hextoint(first) % hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

def print_lol(the_list, indent=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for num in range(level):
                    print('\t', end='')
            print(each_item)


if __name__ == '__main__':
    movies = [
        'The Holy Grail', 1975, 91,
        [
            'Tgraham Chapman',
            ['Michael Palin', 'John Cleese']
        ]
    ]
    print_lol(movies, True)


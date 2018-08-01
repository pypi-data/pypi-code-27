"""Módulo 'nesterlists.py', fornece uma função chamada print_lol() que
retorna os itens em listas que podem ou não incluir listas aninhadas."""


def print_lol(the_list):
    """Percorremos a lista, caso exista outra lista dentro da
     lista, será exibida pela chamada da própria função em if."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

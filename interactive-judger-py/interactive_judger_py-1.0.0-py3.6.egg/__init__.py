def start_judge():
    from . import judge
    return judge.main()


def remove_config():
    from . import conf_generator
    import sys
    return conf_generator.remove_config(sys.argv)


def add_config():
    from . import conf_generator
    return conf_generator.main()

import json
import os


class ConfigKeys:
    UNIQUE_PROGRAM_LIST = 'unique_program_list'
    PROGRAM_NAME_PREFIX = 'program_prefix'
    TIME_LIMIT = 'time_limit'
    NUMBER_OF_TEST_CASES = 'cnt_test_cases'
    NUMBER_OF_TARGET_METHOD_PARAMETERS = 'cnt_params'
    TEST_CASE_FILE = 'test_case_file'
    TARGET_METHOD_NAME = 'method_name'
    ANSWER_FILE = 'answers'
    SRC_DIR = 'source_directory'
    DATA_DIR = 'data_directory'
    RESULT_DIR = 'result_directory'


def _alternative_input(msg: str, default: str):
    result = input(msg)
    if result == '':
        return default
    return result


def remove_config(argv):
    from .judge import get_conf_path
    conf_path = get_conf_path()

    def input_until(msg, func):
        result = int(input(msg))
        while not func(result):
            result = int(input(msg))
        return result

    conf_files = list(filter(lambda x: x.endswith('.json'), os.listdir(conf_path)))
    if len(conf_files) == 0:
        return print('Nothing to do...')
    if len(argv) == 1:
        for (i, c) in enumerate(conf_files):
            print('[{}]\t{}'.format(i + 1, c))
        selected = input_until('Use id to select a config: ', lambda x: 0 < x <= len(conf_files))
        confirm = input('Are you sure?Y/[n]: ')
        if confirm.lower() == 'y':
            os.remove(os.path.join(conf_path, conf_files[selected - 1]))
        else:
            print('OK, remain untamed.')
            exit(0)
    else:
        remove_list = list(filter(lambda x: x in conf_files, argv[1:]))
        if not remove_list:
            exit(0)
        else:
            print(('Selected: \n' + '\n'.join(['{}'] * len(remove_list))).format(*remove_list))
            confirm = input('Are you sure?Y/[n]: ')
            if confirm.lower() == 'y':
                list(map(lambda x: os.remove(os.path.join(conf_path, x)), remove_list))
            else:
                print('OK, remain untamed.')
                exit(0)


def main():
    from .judge import get_conf_path
    config_dict = dict()
    file_name = input('Name of this config: ')
    while os.path.exists(os.path.join(get_conf_path(), '{}.json'.format(file_name))):
        prompt = input('*{}.json* found, overwrite? [Y/n]: '.format(file_name))
        if prompt.lower() == 'y':
            break
        else:
            file_name = input('Name of this config: ')
    config_dict[ConfigKeys.PROGRAM_NAME_PREFIX] = input('Prefix of programs: ')
    config_dict[ConfigKeys.UNIQUE_PROGRAM_LIST] = list(filter(lambda x: len(x) > 0,
                                                              input('Any other programs to '
                                                                    'test(prefix only, '
                                                                    'use space to split): ').split(' ')))
    config_dict[ConfigKeys.TIME_LIMIT] = int(input('Time limit(seconds): '))
    config_dict[ConfigKeys.NUMBER_OF_TEST_CASES] = int(input('Number of test cases: '))
    config_dict[ConfigKeys.TARGET_METHOD_NAME] = input('Name of method to test: ')
    config_dict[ConfigKeys.NUMBER_OF_TARGET_METHOD_PARAMETERS] = int(input('Number of target method parameters: '))
    config_dict[ConfigKeys.TEST_CASE_FILE] = input('File that stores test cases: ')
    config_dict[ConfigKeys.ANSWER_FILE] = input('File that stores expected answers: ')
    config_dict[ConfigKeys.DATA_DIR] = _alternative_input('Custom data directory'
                                                          '({}/data): '.format(os.environ['HOME']),
                                                          os.path.join(os.environ['HOME'], 'data'))
    config_dict[ConfigKeys.SRC_DIR] = _alternative_input('Custom source '
                                                         'file directory({}/src)'.format(os.environ['HOME']),
                                                         os.path.join(os.environ['HOME'], 'src'))
    config_dict[ConfigKeys.RESULT_DIR] = _alternative_input('Custom result output '
                                                            'directory({}/result):'.format(os.environ['HOME']),
                                                            os.path.join(os.environ['HOME'], 'result'))
    conf_path = get_conf_path()
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    if not os.path.exists(config_dict[ConfigKeys.SRC_DIR]):
        os.mkdir(config_dict[ConfigKeys.SRC_DIR])
    if not os.path.exists(config_dict[ConfigKeys.DATA_DIR]):
        os.mkdir(config_dict[ConfigKeys.DATA_DIR])
    if not os.path.exists(config_dict[ConfigKeys.RESULT_DIR]):
        os.mkdir(config_dict[ConfigKeys.RESULT_DIR])
    json.dump(config_dict, open(os.path.join(conf_path, '{}.json'.format(file_name)), 'w'))
    print('Successfully saved to {}.json'.format(file_name))


if __name__ == '__main__':
    main()

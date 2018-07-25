import random
import os


class UtilityFile:
    """

    """

    @staticmethod
    def line_generator(file_path):
        with file_path.open('r') as file:
            while True:
                line = file.readline()
                if line:
                    yield line
                else:
                    return

    @staticmethod
    def line_shuffle(file_path):
        # read
        with file_path.open('r') as file:
            info_list = file.readlines()

        # shuffle
        random.shuffle(info_list)

        # write
        with file_path.open('w') as file:
            for info in info_list:
                file.write(info)

    @staticmethod
    def get_files(files_dir, shuffle):

        file_list = os.listdir(files_dir.__str__())

        if shuffle:
            random.shuffle(file_list)

        return file_list

    @staticmethod
    def get_lines(file_path, shuffle):

        print(file_path.__str__())

        if shuffle:
            UtilityFile.line_shuffle(file_path)

        return UtilityFile.line_generator(file_path)

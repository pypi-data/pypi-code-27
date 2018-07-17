class OptionException(Exception):
    pass


class UploadConflictException(Exception):
    def __init__(self, destination_path):
        self.message = "Conflict. File {} exists on remote server.".format(destination_path)


class AsperaExecutableNotFound(Exception):
    message = "Aspera executable 'ascp' is not found. Please add path to 'ascp' into PATH environment variable."


class AsperaUploadFailed(Exception):
    def __init__(self, return_code):
        self.message = "'ascp' returned non successful code {}.".format(return_code)

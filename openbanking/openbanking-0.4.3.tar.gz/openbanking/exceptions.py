class OpenBankingBaseError(Exception):
    """Base class for all Open Banking errors."""
    pass


class ConfigurationException(OpenBankingBaseError):
    pass

class UnsupportedException(OpenBankingBaseError):
    pass

class JSONDecodeError(OpenBankingBaseError):
    pass

class DecodeError(OpenBankingBaseError):
    pass

class PathFileError(OpenBankingBaseError):
    pass


class SSAError(OpenBankingBaseError):
    pass
from os import path
import datetime
import logging
import logging.config
import logmatic
import socket


class integration:
    def __init__(self, integration, logPath, configFile, configPath, logger=None):
        self.dateNow = datetime.datetime.now().strftime("%Y-%m-%d")
        self.integration = integration
        self.configDict = {}
        self.configFile = configFile
        self.configPath = path.join(configPath, self.configFile)
        self.logger = logger or logging.getLogger(self.integration)
        self.logPath = path.join(logPath, "{}_{}.log".format(self.integration, self.dateNow))
        self.noExtra = {"hostname": socket.gethostname(), "ipaddress": socket.gethostbyname(socket.gethostname())}
        self.checkAndCreateFile()
        self.loadLoggingConfig()

    def merge_two_dicts(self, x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    def checkAndCreateFile(self):
        if not path.isfile(self.logPath):
            f = open(self.logPath, 'a+')
            f.close()

    def loadLoggingConfig(self):
        fmt = "%(created)f %(msecs)d %(relativeCreated)d %(asctime)s %(levelname)s %(levelno)s %(filename)s" \
              "%(args) %(funcName)s %(lineno)d %(module)s %(name)s %(pathname)s %(process)d %(processName)s " \
              "%(thread)d %(threadName)s %(msg) %(message)s %(exc_info)"
        handler = logging.FileHandler(self.logPath)
        handler.setFormatter(logmatic.JsonFormatter(fmt=fmt))
        self.logger.addHandler(handler)

    def criticalLogger(self, message, extraFields=None):
        if extraFields is not None:
            extraFields = self.merge_two_dicts(extraFields, self.noExtra)
            self.logger.error(message, exrta=extraFields,)
        else:
            self.logger.critical(self, message, extra=self.noExtra,)

    def errorLogger(self, message, extraFields=None):
        if extraFields is not None:
            extraFields = self.merge_two_dicts(extraFields, self.noExtra)
            self.logger.error(message, exc_info=True, extra=extraFields)
        else:
            self.logger.error(message, exc_info=True, extra=self.noExtra)

    def warningLogger(self, message, extraFields=None):
        if extraFields is not None:
            extraFields = self.merge_two_dicts(extraFields, self.noExtra)
            self.logger.error(message, exrta=extraFields,)
        else:
            self.logger.warning(message, extra=self.noExtra,)

    def infoLogger(self, message, extraFields=None):
        if extraFields is not None:
            extraFields = self.merge_two_dicts(extraFields, self.noExtra)
            self.logger.error(message, exrta=extraFields,)
        else:
            self.logger.info(message, extra=self.noExtra,)

    def debugLogger(self, message, extraFields=None):
        if extraFields is not None:
            extraFields = self.merge_two_dicts(extraFields, self.noExtra)
            self.logger.error(message, exrta=extraFields,)
        else:
            self.logger.debug(message, extra=self.noExtra,)

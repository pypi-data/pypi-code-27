import sys
import logging

LOG = logging.getLogger(name='MURANO_CLIENT')
LOG_FORMAT = "%(asctime)s-%(levelname)s-%(name)s:%(funcName)s:%(lineno)d ::> %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
streamh = logging.StreamHandler(sys.stdout)
streamh.setFormatter(FORMATTER)
LOG.addHandler(streamh)
LOG.propagate = False

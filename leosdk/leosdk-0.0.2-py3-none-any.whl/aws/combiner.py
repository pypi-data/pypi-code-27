import logging

logger = logging.getLogger(__name__)


class Combiner:

    def __init__(self):
        logger.info("combiner!")

    def reset(self):
        logger.info("reset!")

    def reset_current(self):
        logger.info("reset_current!")

    def reset_batch(self):
        logger.info("reset batch!")

    def add_current_record(self):
        logger.info("add current record!")

    def submit_batch(self):
        logger.info("submit batch!")

    def write(self):
        logger.info("write!")

    def end(self):
        logger.info("end!")

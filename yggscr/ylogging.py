import logging


def consolelog(self, name, loglevel):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s "
                                  "- %(message)s [%(filename)s:%(lineno)s]")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(loglevel)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

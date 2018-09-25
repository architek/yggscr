import logging


def consolelog(name, loglevel):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)20s - %(levelname)9s "
                                  "- %(message)-70s [%(filename)s:%(lineno)s]")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(loglevel)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.debug("Starting logger at level {}".format(loglevel))
    return logger

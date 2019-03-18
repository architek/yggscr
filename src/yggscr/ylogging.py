""" Logger object - As logging, we only need and enforce a single instance """
import logging


def get_logger():
    """ Return yggscr logger """
    return logging.getLogger("yggscr")


def set_log_debug(logger, debug=True):
    """ Update logger level WARN/DEBUG """
    logger.setLevel(logging.DEBUG if debug else logging.WARN)
    print("logger {} level is now set to debug:{}".format(logger, debug))


def loggerlevel_as_text(logger):
    """ Get debug level as text """
    return logging.getLevelName(logger.level)


def add_stdout_handler(logger):
    """ If no handlers already registered, add a stream formatted handler, level WARN """
    return
    if not logger.handlers:
        logger.propagate = False
        logger.setLevel(logging.WARN)

        formatter = logging.Formatter("%(asctime)s - %(name)20s - %(levelname)9s "
                                      "- %(message)-70s [%(filename)s:%(lineno)s]")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)


def init_default_logger():
    """ Used in non OO calling to create logger and add a stream handler """
    logger = get_logger()
    add_stdout_handler(logger)
    logger.error("init_default_logger called from:", stack_info=True)
    return logger

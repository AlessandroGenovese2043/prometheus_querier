import logging


def set_logger(name):
    # logger = logging.getLogger(name)
    # logger.setLevel(logging.DEBUG)
    logger = logging.Logger(name, level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

import logging


def setup_logger():
    """
    Singleton logger setup helper function
    """
    logger = logging.getLogger("chronicle")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

import logging

def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(process)d %(asctime)s  %(name)s: %(levelname)s  %(message)s')
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(level)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.setLevel(level)
    return logger
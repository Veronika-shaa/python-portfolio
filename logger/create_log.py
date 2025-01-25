import logging


class CustomFilter(logging.Filter):
    def filter(self, record):
        return "get" in record.funcName


def create_logger(s, f):
    new_logger = logging.getLogger(__name__)
    new_logger.setLevel(logging.DEBUG)
    new_logger.propagate = False

    formater = logging.Formatter("%(asctime)s\t%(levelname)s\t%(funcName)s\t%(message)s")
    custom_format = logging.Formatter("time: [%(asctime)s]\tlvl: [%(levelno)s]\tmessage: '%(message)s'", datefmt='%Y/%m/%d %H:%M:%S')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(custom_format)

    file_handler = logging.FileHandler("cache.log", mode="w", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formater)

    for handler in new_logger.handlers[:]:
        new_logger.removeHandler(handler)

    for filt in new_logger.filters[:]:
        new_logger.removeFilter(filt)

    if s:
        new_logger.addHandler(stream_handler)
    if f:
        file_handler.addFilter(CustomFilter())

    new_logger.addHandler(file_handler)

    return new_logger

import logging

def setup_logger():
    logging.basicConfig(
        filename='toolbox.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    return logging.getLogger("logger")

logger = setup_logger()
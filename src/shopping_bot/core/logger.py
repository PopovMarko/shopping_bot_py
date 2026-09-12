import logging


def configure_logger(level: str):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s : %(lineno)d %(levelname)s - %(message)s",
    )

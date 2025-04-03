import os
import sys
import logging

def setup_logger(name: str) -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(__file__), "..", "log")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, "fireguard.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if reused
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode='a')
        stream_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

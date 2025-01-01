import logging

class customLogger:
    def __new__(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("log/app.log", mode="w", encoding="utf-8")
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        formatter = logging.Formatter("{asctime} - {name} - {levelname} - {message}", 
                                      style="{", 
                                      datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)
        console_handler.setLevel("INFO")
        file_handler.setFormatter(formatter)
        file_handler.setLevel("DEBUG")

        return logger
import logging
import sys

DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(logger_name: str, level: int = logging.DEBUG, formatter: str = DEFAULT_FORMAT, log_file: str = None):
    """
    获取一个日志记录器，避免重复添加处理器，支持控制台和文件日志输出。

    Args:
        logger_name (str): 日志记录器名称。
        level (int): 日志级别，默认 DEBUG。
        formatter (str): 日志格式，默认标准格式。
        log_file (str): 可选的日志文件路径。如果提供，则输出到文件。

    Returns:
        logging.Logger: 配置好的日志记录器。
    """
    # 获取 logger 实例
    logger = logging.getLogger(logger_name)

    # 避免重复添加处理器
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # 创建日志格式
    log_formatter = logging.Formatter(formatter)

    # 控制台日志输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # 文件日志输出（可选）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    return logger

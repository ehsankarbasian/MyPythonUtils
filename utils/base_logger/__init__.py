from utils.base_logger.base_logger import Logger as setup_logger


class Logger:
    setup_logger = setup_logger


# How to setup logger:
app_logic_logger = Logger.setup_logger(name='app_logic', log_file='logs/sys.log', project='bale_bot', log_type='result', console_logger_enable=True)
inner_logic_logger = Logger.setup_logger(name='inner_logic', log_file='logs/inner_logic.log', project='bale_bot', log_type='result', console_logger_enable=False)

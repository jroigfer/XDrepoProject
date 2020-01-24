import logging, os
import logging.config

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'resources/logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger('dev')
logger.info('Logging actived!')
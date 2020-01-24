import logging, os
import logging.config

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, '../resources/log.conf'), disable_existing_loggers=False)
#logging.config.fileConfig(fname='src/resources/log.conf')

logger = logging.getLogger('dev')
logger.info('This is an information message')
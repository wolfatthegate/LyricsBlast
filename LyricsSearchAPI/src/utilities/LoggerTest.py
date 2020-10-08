import logging

# logging.basicConfig()
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.critical('this better be bad')
# logger.error('more serious problem')
# logger.warning('an unexpected event')
# logger.info('show user flow through program')
# logger.debug('used to track variable')
# 
# logFormatter = '%(asctime)s - %(user)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=logFormatter, level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# handler = logging.FileHandler('archived_tweets/myLogs.log')
# 
# logger.addHandler(handler)
# logger.info('purchase completed by WL', extra={'user': 'Waylon Luo'})
# logger.info('purchase completed by SP', extra={'user': 'Sid Panjwani'})


logFormatter = '%(asctime)s - %(user)s - %(levelname)s - %(message)s'

logging.basicConfig(filename='archived_tweets/myLogs.log',level=logging.DEBUG, format='%(asctime)s %(user)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('This message should go to the log file',  extra={'user': 'Waylon Luo'})
logging.info('So should this',  extra={'user': 'Waylon Luo'})
logging.warning('And this, too',  extra={'user': 'Waylon Luo'})
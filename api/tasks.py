from celery import shared_task
from celery.utils.log import get_task_logger
# from .services import Utils


logger = get_task_logger(__name__)

@shared_task(name='load_prices')
def task_load_prices():
    logger.info("Fetching BTC data")
    # Utils().load_closes('BRLBTC', 1)
    logger.info("Fetching ETH data")
    # Utils().load_closes('BRLETH', 1)

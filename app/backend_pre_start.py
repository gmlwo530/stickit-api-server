from app.db.database import get_database
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        get_database()
    except Exception as e:
        logger.error(e)
        raise e


def backend_pre_start() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")

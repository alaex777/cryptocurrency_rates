import logging

from src.db.managers.manager import DBManager

logger = logging.getLogger(__name__)


class SerivceAdapter:
    def __init__(self, db_manager: DBManager) -> None:
        self._db_manager = db_manager

    async def healthcheck(self) -> bool:
        db_healthcheck_result = await self._db_manager.healthcheck()
        logger.info(f'db healthcheck result: {db_healthcheck_result=}')

        if not db_healthcheck_result:
            logger.error('db healthcheck failed')
            return False

        return True

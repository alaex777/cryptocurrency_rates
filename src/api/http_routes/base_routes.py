from src.bl.bl_manager import BLManager

BASE_PATH = '/api/v{api_version}/'


class BaseRoutes:
    def __init__(self, bl_manager: BLManager) -> None:
        self._bl_manager = bl_manager

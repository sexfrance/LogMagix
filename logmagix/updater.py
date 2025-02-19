import requests
import subprocess
import sys
from packaging import version
from .logger import Logger
from .version import __version__

class AutoUpdater:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, package_name: str, logger: Logger = None):
        if not AutoUpdater._initialized:
            self.package_name = package_name
            self.logger = logger or Logger()
            self.current_version = __version__
            self.pypi_version = self.get_pypi_version()
            self._checked_version = version.parse(self.current_version)
            self._latest_version = version.parse(self.pypi_version)
            self._update_checked = False
            AutoUpdater._initialized = True

    def _get_installed_version(self) -> str:
        return __version__

    def get_pypi_version(self) -> str:
        try:
            response = requests.get(f"https://pypi.org/pypi/{self.package_name}/json")
            if response.status_code == 200:
                return response.json()["info"]["version"]
        except Exception as e:
            self.logger.warning(f"Failed to fetch PyPI version: {e}")
        return "0.0.0"

    def update_available(self) -> bool:
        if not hasattr(self, '_checked_version'):
            self._checked_version = version.parse(self.current_version)
            self._latest_version = version.parse(self.pypi_version)
        return self._latest_version > self._checked_version

    def update(self, force: bool = False) -> bool:
        if not force and not self.update_available():
            self.logger.info(f"Already running latest version ({self.current_version})")
            return False

        try:
            self.logger.info(f"Updating {self.package_name} from {self.current_version} to {self.pypi_version}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                f"{self.package_name}=={self.pypi_version}", "--upgrade"
            ])
            self.current_version = self.pypi_version
            self._checked_version = version.parse(self.current_version)
            self.logger.success(f"Successfully updated to version {self.pypi_version}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update: {e}")
            return False

    def check_for_updates(self, auto_update: bool = False) -> None:
        if self._update_checked:
            return

        if self.update_available():
            if auto_update:
                self.update()
    
        
        self._update_checked = True

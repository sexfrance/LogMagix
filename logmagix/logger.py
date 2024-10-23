# logmagix/logger.py

import datetime
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style
from shutil import get_terminal_size

class Logger:
    def __init__(self, prefix: str = ".gg/bestnitro"):
        self.WHITE = "\u001b[37m"
        self.MAGENTA = "\033[38;5;97m"
        self.MAGENTAA = "\033[38;2;157;38;255m"
        self.RED = "\033[38;5;196m"
        self.GREEN = "\033[38;5;40m"
        self.YELLOW = "\033[38;5;220m"
        self.BLUE = "\033[38;5;21m"
        self.PINK = "\033[38;5;176m"
        self.CYAN = "\033[96m"
        self.prefix = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}] "

    def get_time(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def message3(self, level: str, message: str) -> str:
        time = self.get_time()
        return f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {self.CYAN}{message}{Fore.RESET}"

    def success(self, message: str, level: str = "Success") -> None:
        print(self.message3(f"{self.GREEN}{level}", f"{self.GREEN}{message}"))

    def failure(self, message: str, level: str = "Failure") -> None:
        print(self.message3(f"{self.RED}{level}", f"{self.RED}{message}"))

    def warning(self, message: str, level: str = "Warning") -> None:
        print(self.message3(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}"))

log = Logger()

class Loader:
    def __init__(self, desc="Loading...", end="\r", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.time = datetime.datetime.now().strftime("%H:%M:%S")

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{log.PINK}[{log.MAGENTA}.gg/bestnitro{log.PINK}] [{log.MAGENTAA}{self.time}{log.PINK}] [{log.GREEN}{self.desc}{Fore.RESET}] {c}", flush=True, end="")
            time.sleep(self.timeout)

    def stop(self):
        self.done = True
        print(f"\r{self.end}", flush=True)


# Credits: discord.cyberious.xyz, github.com/sexfrance, t.

# Logging inspired by github.com/DXVVAY

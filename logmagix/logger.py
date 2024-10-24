import datetime
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style

class Logger:
    def __init__(self, prefix: str = "discord.cyberious.xyz"):
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

    def message3(self, level: str, message: str, start: int = None, end: int = None) -> str:
        time = self.get_time()
        return f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {self.CYAN}{message}{Fore.RESET}"

    def success(self, message: str, start: int = None, end: int = None, level: str = "Success") -> None:
        print(self.message3(f"{self.GREEN}{level}", f"{self.GREEN}{message}", start, end))

    def failure(self, message: str, start: int = None, end: int = None, level: str = "Failure") -> None:
        print(self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end))
    
    def warning(self, message: str, start: int = None, end: int = None, level: str = "Warning") -> None:
        print(self.message3(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}", start, end))

    def message(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]")
        else:
            print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] [{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
    
    def message2(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]", end="\r")
        else:
            print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {self.PINK}[{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}", end="\r")

    def question(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        i = input(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {Fore.RESET} {self.PINK}[{Fore.BLUE}?{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
        return i

    def info(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {Fore.RESET} {self.PINK}[{Fore.BLUE}!{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
    
    def debug(self, message: str, start: int = None, end: int = None) -> None:
            time = self.get_time()
            print(f"{self.prefix}[{self.MAGENTAA}{time}{self.PINK}] {Fore.RESET} {self.PINK}[{Fore.YELLOW}DEBUG{self.PINK}] -> {Fore.RESET} {self.GREEN}{message}{Fore.RESET}")


log = Logger()

class Loader:
    def __init__(self, prefix: str = "discord.cyberious.xyz", desc="Loading...", end="\r", timeout=0.1):
        self.desc = desc
        self.end = end
        self.prefix = prefix
        self.timeout = timeout
        self.time = datetime.datetime.now().strftime("%H:%M:%S")

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.MAGENTAA}{self.time}{log.PINK}] [{log.GREEN}{self.desc}{log.PINK}]{Fore.RESET} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def stop(self):
        self.done = True
        if self.end != "\r":
            print(f"\n{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.MAGENTAA}{self.time}{log.PINK}] {log.GREEN} {self.end}", flush=True)
        else:
            print(self.end, flush=True)
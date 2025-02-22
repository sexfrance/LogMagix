import datetime
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style
import os
import getpass
from .font import ascii_art
from pystyle import Write, System, Colors
from enum import Enum
import re

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    SUCCESS = 4
    FAILURE = 5
    CRITICAL = 6

class Logger:
    def __new__(cls, style: int = 1, *args, **kwargs):
        if cls is Logger:
            if style == 2:
                return SimpleLogger(*args, **kwargs)
            return ColorLogger(*args, **kwargs)
        return super().__new__(cls)
        
    def __init__(self, style: int = 1, prefix: str | None = "discord.cyberious.xyz", github_repository: str = None, level: LogLevel = LogLevel.DEBUG, log_file: str | None = None, auto_update: bool = True):
        self.level = level
        self.repo_url = github_repository
        self.log_file = log_file
        self.prefix = prefix

        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            self._write_to_log(f"=== Logging started at {datetime.datetime.now()} ===\n")

        if auto_update:
            from .updater import AutoUpdater
            updater = AutoUpdater("logmagix", self)
            updater.check_for_updates(auto_update=True)

    def _extract_github_username(self, url: str) -> str | None:
        url = url.replace('https://', '').replace('http://', '').replace('www.', '')
        patterns = [
            r'^github\.com/([^/]+)(?:/.*)?$',  # github.com/username or username/repo
            r'^([^/]+)(?:/.*)?$',              # username or username/repo
            r'^@(.+)$'                         # @username
        ]
        for pattern in patterns:
            if match := re.search(pattern, url):
                return match.group(1).rstrip('/ \t\n\r')
        return None

    def _write_to_log(self, message: str) -> None:
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    clean_message = self._strip_ansi(message)
                    f.write(clean_message + '\n')
            except Exception as e:
                print(f"Error writing to log file: {e}")

    def _strip_ansi(self, text: str) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def get_time(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _should_log(self, message_level: LogLevel) -> bool:
        return message_level.value >= self.level.value

class ColorLogger(Logger):
    def __init__(self, *args, **kwargs):
        self.WHITE = "\u001b[37m"
        self.MAGENTA = "\033[38;5;97m"
        self.BRIGHT_MAGENTA = "\033[38;2;157;38;255m"
        self.LIGHT_CORAL = "\033[38;5;210m"
        self.RED = "\033[38;5;196m"
        self.GREEN = "\033[38;5;40m"
        self.YELLOW = "\033[38;5;220m"
        self.BLUE = "\033[38;5;21m"
        self.PINK = "\033[38;5;176m"
        self.CYAN = "\033[96m"
        super().__init__(*args, **kwargs)
        self.prefix = f"{self.PINK}[{self.MAGENTA}{self.prefix}{self.PINK}] " if self.prefix else f"{self.PINK}"

        if self.repo_url:
            username = self._extract_github_username(self.repo_url)
            if username:
                self.info(f"Developed by {username} - {self.repo_url}")
            else:
                self.info(f"GitHub Repository: {self.repo_url}")

    def message3(self, level: str, message: str, start: int = None, end: int = None) -> str:
        current_time = self.get_time()
        return f"{self.prefix}[{self.BRIGHT_MAGENTA}{current_time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {self.CYAN}{message}{Fore.RESET}"

    def success(self, message: str, start: int = None, end: int = None, level: str = "Success") -> None:
        if self._should_log(LogLevel.SUCCESS):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = self.message3(f"{self.GREEN}{level}", f"{self.GREEN}{message}", start, end) + timer
            print(log_message)
            self._write_to_log(log_message)

    def failure(self, message: str, start: int = None, end: int = None, level: str = "Failure") -> None:
        if self._should_log(LogLevel.FAILURE):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end) + timer
            print(log_message)
            self._write_to_log(log_message)
    
    def error(self, message: str, start: int = None, end: int = None, level: str = "Error") -> None:
        if self._should_log(LogLevel.FAILURE):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end) + timer
            print(log_message)
            self._write_to_log(log_message)
    
    def warning(self, message: str, start: int = None, end: int = None, level: str = "Warning") -> None:
        if self._should_log(LogLevel.WARNING):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = self.message3(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}", start, end) + timer
            print(log_message)
            self._write_to_log(log_message)

    def message(self, level: str, message: str, start: int = None, end: int = None) -> None:
        timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
        log_message = f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}] [{self.CYAN}{level}{self.PINK}] -> [{self.CYAN}{message}{self.PINK}]{timer}"
        print(log_message)
        self._write_to_log(log_message)
    
    def message2(self, level: str, message: str, start: int = None, end: int = None) -> None: 
        if start and end:
            print(f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]", end="\r")
        else:
            print(f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}] {self.PINK}[{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}", end="\r")

    def question(self, message: str, start: int = None, end: int = None) -> None:
        question_message = f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}]{Fore.RESET} {self.PINK}[{Fore.BLUE}?{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}"
        print(question_message, end='')
        i = input()
        self._write_to_log(f"{question_message}")
        self._write_to_log(f"User Answer: {i}")
        
        return i

    def critical(self, message: str, start: int = None, end: int = None, level: str = "CRITICAL", exit_code: int = 1) -> None:
        if self._should_log(LogLevel.CRITICAL):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}]{Fore.RESET} {self.PINK}[{self.RED}{level}{self.PINK}] -> {self.LIGHT_CORAL}{message}{Fore.RESET}" + timer
            print(log_message)
            input()
            self._write_to_log(log_message)
            self._write_to_log(f"=== Program terminated with exit code {exit_code} at {datetime.datetime.now()} ===")
            exit(exit_code)

    def info(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.INFO):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}]{Fore.RESET} {self.PINK}[{Fore.BLUE}!{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}" + timer
            print(log_message)
            self._write_to_log(log_message)
    
    def debug(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.DEBUG):
            timer = f" {self.BRIGHT_MAGENTA}In{self.WHITE} -> {self.BRIGHT_MAGENTA}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
            log_message = f"{self.prefix}[{self.BRIGHT_MAGENTA}{self.get_time()}{self.PINK}]{Fore.RESET} {self.PINK}[{Fore.YELLOW}DEBUG{self.PINK}] -> {Fore.RESET} {self.GREEN}{message}{Fore.RESET}" + timer
            print(log_message)
            self._write_to_log(log_message)

class SimpleLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = f"{Fore.BLACK}{self.get_time()} » {Fore.RESET}"

        if self.repo_url:
            username = self._extract_github_username(self.repo_url)
            if username:
                self.info(f"Developed by {username} - {self.repo_url}")
            else:
                self.info(f"GitHub Repository: {self.repo_url}")

    def success(self, message: str, start: int = None, end: int = None, level: str = "SUCCESS") -> None:
        if self._should_log(LogLevel.SUCCESS):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTGREEN_EX}{level} {Fore.BLACK}➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def failure(self, message: str, start: int = None, end: int = None, level: str = "FAILURE") -> None:
        if self._should_log(LogLevel.FAILURE):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTRED_EX}{level} {Fore.BLACK}  ➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def error(self, message: str, start: int = None, end: int = None, level: str = "ERROR") -> None:
        if self._should_log(LogLevel.FAILURE):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTRED_EX}{level} {Fore.BLACK}  ➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def warning(self, message: str, start: int = None, end: int = None, level: str = "WARNING") -> None:
        if self._should_log(LogLevel.WARNING):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTYELLOW_EX}{level} {Fore.BLACK}➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)
    
    def message(self, message: str, start: int = None, end: int = None, level: str = "MESSAGE") -> None:
        if self._should_log(LogLevel.WARNING):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTMAGENTA_EX}{level} {Fore.BLACK}➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def info(self, message: str, start: int = None, end: int = None, level: str = "INFO") -> None:
        if self._should_log(LogLevel.INFO):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.LIGHTBLUE_EX}{level} {Fore.BLACK}   ➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def debug(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.DEBUG):
            timer = f" (In {str(end - start)[:5]}s)" if start and end else ""
            log_message = f"{self.prefix}{Fore.GREEN}[{Fore.YELLOW}DEBUG{Fore.GREEN}] {Fore.BLACK}➔ {Fore.RESET} {message}{timer}"
            print(log_message)
            self._write_to_log(log_message)

    def question(self, message: str, level: str = "QUESTION") -> None:
        question_message = f"{self.prefix}{Fore.LIGHTCYAN_EX}{level} {Fore.BLACK}➔ {Fore.RESET} {message}"
        print(question_message, end='')
        i = input()
        self._write_to_log(f"{question_message}")
        self._write_to_log(f"User Answer: {i}")
        return i

log = Logger()

class Loader:
    def __init__(self, prefix: str = "discord.cyberious.xyz", desc="Loading...", end="\r", timeout=0.1):
        self.desc = desc
        self.end = end
        self.prefix = prefix
        self.timeout = timeout
        self.time = None  # Remove time initialization
        self.start_time = datetime.datetime.now()

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
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time each iteration
            loader_message = f"\r{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.BRIGHT_MAGENTA}{current_time}{log.PINK}] [{log.GREEN}{self.desc}{log.PINK}]{Fore.RESET} {c}"
            print(loader_message, flush=True, end="")
            time.sleep(self.timeout)

    def stop(self):
        self.done = True
        if (self.end != "\r"):
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time for stop message
            end_message = f"\n{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.BRIGHT_MAGENTA}{current_time}{log.PINK}] {log.GREEN} {self.end} {Fore.RESET}"
            print(end_message, flush=True)
        else:
            print(self.end, flush=True)

class Home:
    def __init__(self, text, align="left", adinfo1=None, adinfo2=None, credits=None, clear=True):
        self.text = text
        self.align = align
        self.adinfo1 = adinfo1
        self.adinfo2 = adinfo2
        self.credits = credits
        self.clear = clear
        self.username = getpass.getuser()

    def _get_char_art(self):
        char_arts = []
        max_height = 8

        for char in self.text:
            char_art = ascii_art.get(char, [" " * 8] * 8)

            if char.islower() and len(char_art) == 6:
                char_art = [" " * 8] * 1 + char_art

            char_arts.append(char_art)

        return char_arts, max_height

    def _align_text(self, lines, terminal_width, alignment, block_width):
        aligned_result = []
        for line in lines:
            stripped_line = line.rstrip()
            if alignment == "center":
                padding = max(0, (terminal_width - block_width) // 2)
                aligned_line = " " * padding + stripped_line
            elif alignment == "right":
                padding = max(0, terminal_width - block_width)
                aligned_line = " " * padding + stripped_line
            else:
                aligned_line = stripped_line
            aligned_result.append(aligned_line)
        return aligned_result

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self):
        char_arts, max_height = self._get_char_art()
        result = [""] * max_height

        for i in range(max_height):
            line = "".join([char_art[i] if i < len(char_art) else " " * 8 for char_art in char_arts])
            result[i] = line

        max_line_width = max(len(line) for line in result)

        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            terminal_width = 80
        
        aligned_result = self._align_text(result, terminal_width, self.align, max_line_width)
        if self.clear:
            self._clear()

        for line in aligned_result:
            Write.Print(line + "\n", Colors.red_to_blue, interval=0.000)

        self._display_adinfo(aligned_result, terminal_width)
        self._display_welcome(terminal_width, max_line_width)

    def _display_adinfo(self, aligned_result, terminal_width):
        if not (self.adinfo1 or self.adinfo2):
            return

        ascii_art_width = max(len(line.rstrip()) for line in aligned_result)
        adinfo_text = self._construct_adinfo_text(ascii_art_width)
        adinfo_block_width = len(adinfo_text)
        aligned_adinfo = self._align_text([adinfo_text], terminal_width, self.align, adinfo_block_width)

        for line in aligned_adinfo:
            Write.Print(line + "\n", Colors.red_to_blue, interval=0.000)

    def _construct_adinfo_text(self, ascii_art_width):
        if self.adinfo1 and self.adinfo2:
            total_adinfo_length = len(self.adinfo1) + len(self.adinfo2)
            remaining_space = ascii_art_width - total_adinfo_length
            if (remaining_space > 0):
                padding_between = '  ' * (remaining_space // 3)
                return self.adinfo1 + padding_between + self.adinfo2
            else:
                return self.adinfo1 + '   ' + self.adinfo2
        return self.adinfo1 or self.adinfo2 or ''

    def _display_welcome(self, terminal_width, block_width):
        welcome_message = f"Welcome {self.username}"
        if self.credits:
            welcome_message += f" | {self.credits}"

        welcome_message_with_tildes = f"    {welcome_message}    "
        tilde_line = "~" * len(welcome_message_with_tildes)

        welcome_padding = max(0, (terminal_width - len(welcome_message_with_tildes)) // 2)
        tilde_padding = max(0, (terminal_width - len(tilde_line)) // 2)

        welcome_line = " " * welcome_padding + welcome_message_with_tildes
        tilde_line_aligned = " " * tilde_padding + tilde_line

        Write.Print(f"{welcome_line}\n", Colors.red_to_blue, interval=0.000)
        Write.Print(f"{tilde_line_aligned}\n", Colors.red_to_blue, interval=0.000)

        equals_line = "═" * terminal_width
        Write.Print(f"{equals_line}\n", Colors.red_to_blue, interval=0.000)

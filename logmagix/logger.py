import datetime
import time
from threading import Thread, Lock
from itertools import cycle
from enum import Enum
from typing import Optional, List
import logging.handlers
from colorama import Fore, Style
import os
from sys import exit
import getpass
from .font import ascii_art
from pystyle import Write, Colors

class LogLevel(Enum):
    """Enumeration of available logging levels."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    SUCCESS = 3
    ERROR = 4
    CRITICAL = 5

class Logger:
    """Advanced logging system with color support and multiple output formats."""

    COLORS = {
        "WHITE": "\u001b[37m",
        "MAGENTA": "\033[38;5;97m",
        "MAGENTA_BRIGHT": "\033[38;2;157;38;255m",
        "RED": "\033[38;5;196m",
        "LIGHT_CORAL": "\033[38;5;210m",
        "GREEN": "\033[38;5;40m",
        "YELLOW": "\033[38;5;220m",
        "BLUE": "\033[38;5;21m",
        "PINK": "\033[38;5;176m",
        "CYAN": "\033[96m"
    }

    def __init__(
        self, 
        prefix: Optional[str] = "discord.cyberious.xyz",
        log_file: Optional[str] = None,
        max_file_size: int = 10_000_000,
        backup_count: int = 5
    ) -> None:
        """Initialize the logger with the given configuration."""
        self._setup_colors()
        self.prefix = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}] " if prefix else f"{self.PINK}"
        self.log_lock = Lock()
        self.message_buffer: List[tuple] = []
        self._min_level = LogLevel.DEBUG
        self._batch_messages = []
        self._batch_mode = False
        
        self.file_handler = self._setup_file_handler(log_file, max_file_size, backup_count) if log_file else None

    def _setup_colors(self) -> None:
        """Set up color attributes from COLORS dictionary."""
        for name, value in self.COLORS.items():
            setattr(self, name, value)

    def _setup_file_handler(
        self, 
        log_file: str, 
        max_file_size: int, 
        backup_count: int
    ) -> logging.handlers.RotatingFileHandler:
        """Configure and return a file handler for logging."""
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        return handler

    def set_min_level(self, level: LogLevel) -> None:
        """Set minimum log level. Messages below this level will not be displayed."""
        if not isinstance(level, LogLevel):
            raise ValueError("Level must be a LogLevel enum value")
        self._min_level = level

    def _should_log(self, level):
        """Check if message should be logged based on minimum level."""
        return level.value >= self._min_level.value

    def batch(self) -> None:
        """Start batch logging - messages will be stored but not displayed"""
        self._batch_mode = True
        self._batch_messages = []

    def flush(self) -> None:
        """Flush all stored messages and display them"""
        if not self._batch_mode:
            return
            
        with self.log_lock:
            for msg_data in self._batch_messages:
                level_str, color, message = msg_data
                display_level = level_str.capitalize()
                print(self.message3(f"{color}{display_level}", f"{color}{message}"))
                if self.file_handler:
                    level = getattr(LogLevel, level_str)
                    self._log_to_file(level, message)
            self._batch_messages.clear()
        self._batch_mode = False

    def _log(self, level: LogLevel, message: str, start: int = None, end: int = None) -> None:
        """Internal logging method that handles both console and file output."""
        if not self._should_log(level):
            return

        # Map log levels to colors and display names
        level_colors = {
            LogLevel.DEBUG: self.BLUE,
            LogLevel.INFO: self.CYAN,
            LogLevel.WARNING: self.YELLOW,
            LogLevel.SUCCESS: self.GREEN,
            LogLevel.ERROR: self.RED,
            LogLevel.CRITICAL: self.LIGHT_CORAL
        }

        color = level_colors.get(level, self.WHITE)
        formatted_message = self.message3(f"{color}{level.name}", f"{color}{message}", start, end)
        
        with self.log_lock:
            print(formatted_message)
            if self.file_handler:
                stripped_message = self._strip_colors(formatted_message)
                self.file_handler.emit(
                    logging.LogRecord(
                        name="logger",
                        level=level.value * 10,
                        pathname="",
                        lineno=0,
                        msg=stripped_message,
                        args=(),
                        exc_info=None
                    )
                )

    def _strip_colors(self, message: str) -> str:
        """Remove ANSI color codes from message."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', message)

    def success(self, message: str, start: int = None, end: int = None, level: str = "Success") -> None:
        if self._should_log(LogLevel.SUCCESS):
            self._log(LogLevel.SUCCESS, message, start, end)

    def failure(self, message: str, start: int = None, end: int = None, level: str = "Failure") -> None:
        if self._should_log(LogLevel.ERROR):
            self._log(LogLevel.ERROR, message, start, end)

    def critical(self, message: str, start: int = None, end: int = None, level: str = "CRITICAL", exit_code: int = 1) -> None:
        input(self.message3(f"{self.LIGHT_CORAL}{level}", f"{self.LIGHT_CORAL}{message}", start, end))
        self._log_to_file(LogLevel.CRITICAL, message)
        exit(exit_code)
    
    def warning(self, message: str, start: int = None, end: int = None, level: str = "Warning") -> None:
        if self._should_log(LogLevel.WARNING):
            self._log(LogLevel.WARNING, message, start, end)

    def info(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.INFO):
            self._log(LogLevel.INFO, message, start, end)
    
    def debug(self, message: str, start: int = None, end: int = None) -> None:
        if self._should_log(LogLevel.DEBUG):
            self._log(LogLevel.DEBUG, message, start, end)

    def _log_to_file(self, level: LogLevel, message: str) -> None:
        """Helper method to handle file logging"""
        if not self.file_handler:
            return
            
        if level.value >= self._min_level.value:
            stripped_message = self._strip_colors(message)
            self.file_handler.emit(
                logging.LogRecord(
                    name="logger",
                    level=level.value * 10,
                    pathname="",
                    lineno=0,
                    msg=stripped_message,
                    args=(),
                    exc_info=None
                )
            )

    def get_time(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def message(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        timer = f" {self.MAGENTA_BRIGHT}In{self.WHITE} -> {self.MAGENTA_BRIGHT}{str(end - start)[:5]} Seconds {Fore.RESET}" if start and end else ""
        print(f"{self.prefix}[{self.MAGENTA_BRIGHT}{time}{self.PINK}] [{self.CYAN}{level}{self.PINK}] -> [{self.CYAN}{message}{self.PINK}]{timer}")
    
    def message2(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.MAGENTA_BRIGHT}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]", end="\r")
        else:
            print(f"{self.prefix}[{self.MAGENTA_BRIGHT}{time}{self.PINK}] {self.PINK}[{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}", end="\r")

    def message3(self, level: str, message: str, start: int = None, end: int = None) -> str:
        time = self.get_time()
        return f"{self.prefix}[{self.MAGENTA_BRIGHT}{time}{self.PINK}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {self.CYAN}{message}{Fore.RESET}"

    def question(self, message: str, start: int = None, end: int = None) -> str:
        time = self.get_time()
        i = input(f"{self.prefix}[{self.MAGENTA_BRIGHT}{time}{self.PINK}]{Fore.RESET} {self.PINK}[{Fore.BLUE}?{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
        return i

log = Logger()

class Loader:
    """Animated loading indicator with customizable appearance."""

    SPINNER_CHARS = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]

    def __init__(
        self,
        prefix: Optional[str] = "discord.cyberious.xyz",
        desc: str = "Loading...",
        end: str = "\r",
        timeout: float = 0.1
    ) -> None:
        self.desc = desc
        self.end = end
        self.prefix = prefix
        self.timeout = timeout
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        
        self._thread = Thread(target=self._animate, daemon=True)
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
        for c in cycle(self.SPINNER_CHARS):
            if self.done:
                break
            prefix_str = f"[{log.MAGENTA}{self.prefix}{log.PINK}] " if self.prefix is not None else ""
            print(f"\r{log.PINK}{prefix_str}[{log.MAGENTA_BRIGHT}{self.time}{log.PINK}] [{log.GREEN}{self.desc}{log.PINK}]{Fore.RESET} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def stop(self):
        self.done = True
        if self.end != "\r":
            prefix_str = f"[{log.MAGENTA}{self.prefix}{log.PINK}] " if self.prefix is not None else ""
            print(f"\n{log.PINK}{prefix_str}[{log.MAGENTA_BRIGHT}{self.time}{log.PINK}] {log.GREEN} {self.end} {Fore.RESET}", flush=True)
        else:
            print(self.end, flush=True)

class Home:
    """ASCII art text display with customizable formatting and layout."""

    def __init__(
        self,
        text: str,
        align: str = "left",
        adinfo1: Optional[str] = None,
        adinfo2: Optional[str] = None,
        credits: Optional[str] = None,
        clear: bool = True
    ) -> None:
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
            if remaining_space > 0:
                padding_between = '  ' * (remaining_space // 3)
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

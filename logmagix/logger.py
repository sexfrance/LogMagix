import datetime
import time
from threading import Thread
from itertools import cycle
from colorama import Fore, Style
import os
import getpass
from .font import ascii_art
from pystyle import Write, System, Colors

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
            print(f"\n{log.PINK}[{log.MAGENTA}{self.prefix}{log.PINK}] [{log.MAGENTAA}{self.time}{log.PINK}] {log.GREEN} {self.end} {Fore.RESET}", flush=True)
        else:
            print(self.end, flush=True)

class Home:
    def __init__(self, text, align="left", adinfo1=None, adinfo2=None, credits=None):
        self.text = text
        self.align = align
        self.adinfo1 = adinfo1
        self.adinfo2 = adinfo2
        self.credits = credits
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

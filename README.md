# LogMagix

**LogMagix** is a custom Python logging package that offers styled, colorful log messages for various logging levels such as success, warning, failure, and more. It also features an animated loader class for providing a visual indicator during long-running operations in the terminal. Additionally, the `Home` class offers customizable ASCII art displays for greeting users with special messages, branding, or system information.

## 🔥 Features

- Log messages for various levels: success, warning, failure, debug, critical, info, and more.
- Color customization using ANSI escape sequences.
- Time-stamped log messages for better tracking.
- Built-in animated loader for visually appealing loading spinners.
- Log saving to file with optional log file paths.
- Customizable log and loader prefixes.
- ASCII art display for personalized greetings, system info, and branding.
- Simple and flexible API with multiple ways to use the `Loader` class.
- Customizable text alignment for the `Home` ASCII art display.

## ⚙️ Installation

To install the package locally, clone the repository and run:

```bash
pip install .
```

You can also install it via `pip` from PyPI:

```bash
pip install logmagix
```

## 🔧 Usage

### Importing the Package

```python
from logmagix import Logger, Loader, Home
```

### Logging

Initialize the `Logger` class to log messages with different levels:

```python
log = Logger()

# Success message
log.success("Operation completed successfully!")

# Failure message
log.failure("Something went wrong!")

# Warning message
log.warning("This is a warning!")

# Informational message
log.info("Informational log message")

# Debug message
log.debug("Debugging log message")

# Critical message (also terminates the program with optional exit code)
log.critical("Critical failure encountered", exit_code=1)
```

### Log Levels

LogMagix provides several logging levels to help categorize the severity and type of log messages. You can configure the minimum log level to display based on your requirements:

- `DEBUG`: For detailed debug messages.
- `INFO`: For informational messages.
- `WARNING`: For warning messages.
- `SUCCESS`: For successful operations.
- `FAILURE`: For non-critical errors.
- `CRITICAL`: For critical errors; may terminate the program.

You can set the minimum logging level on initialization by passing a `LogLevel` value to the `Logger` constructor. For example:

```python
from logmagix import Logger, LogLevel

log = Logger(level=LogLevel.WARNING)
```

With this setting, only `WARNING`, `SUCCESS`, `FAILURE`, and `CRITICAL` messages will display.

### Log File Saving

You can specify a log file path to save logs to a file for further review or debugging. The logger will automatically strip ANSI color codes from messages saved to the log file for readability. Log files are appended with each new logging session.

```python
log = Logger(log_file="logs/app.log")
log.success("This message will also be saved to app.log")
```

To view logs saved to the file, open the specified path and review the recorded entries, which include timestamped log messages for tracking system state over time.

### Loading Animation

The `Loader` class can be used in two ways:

#### Using a context manager:

```python
from time import sleep

with Loader(desc="Loading with context manager..."):
    for i in range(10):
        sleep(0.25)
```

#### Using `start()` and `stop()` methods:

```python
loader = Loader(desc="Loading with object...", end="That was fast!", timeout=0.05).start()
for i in range(10):
    sleep(0.25)
loader.stop()
```

### Custom Log and Loader Prefix

Both the `Logger` and `Loader` classes allow for customizing the prefix shown before each message:

#### Logger Prefix:

```python
log = Logger(prefix=".myapp/logs")
log.success("This message has a custom log prefix!")
```

#### Loader Prefix:

```python
loader = Loader(prefix=".myapp/loader", desc="Loading with a custom loader prefix...")
loader.start()
time.sleep(5)  # Simulate a task
loader.stop()
```

### ASCII Art and Greeting (New `Home` Class)

The `Home` class lets you display customized ASCII art text along with system information, such as a welcome message, username, or credits.

#### Using the `Home` Class:

```python
home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="discord.cyberious.xyz",
    adinfo2="v1.0",
    credits="Developed by sexfrance",
    clear = False, # To clear the console, default is True
)

home_screen.display()
```

This will display the ASCII art version of "LogMagix" in the center of the terminal, along with optional `adinfo1` and `adinfo2` texts at the bottom. The terminal width is automatically detected to align the text properly.

### Full Example

Here’s an example showing both logging, loader, and the new `Home` class functionality:

```python
from logmagix import Logger, Loader, Home
import time
import uuid

log = Logger(prefix="custom/log/prefix")
start_time = time.time()

# Log messages
log.success("Everything is running smoothly!")
log.warning("Watch out, something might happen!")
log.failure("Critical error occurred!")
log.info("System is working properly")
log.debug(f"The system uuid is {uuid.getnode()}")

# Use loader with custom prefix and context manager
with Loader(prefix="custom/loader/prefix", desc="Processing data..."):
    time.sleep(2)  # Simulate task

# Use loader with custom prefix and start/stop methods
loader = Loader(prefix="custom/loader/prefix", desc="Saving files...", end="Done !", timeout=0.05).start()
time.sleep(2)  # Simulate task
loader.stop()

home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="discord.cyberious.xyz",
    adinfo2="v1.0",
    credits="Developed by sexfrance"
)

home_screen.display()

log.success("Processing completed!")
```

### Customization in `Home` Class

- **text**: The text to be displayed in ASCII art.
- **align**: Align the ASCII art text to "left", "center", or "right" in the terminal.
- **adinfo1** and **adinfo2**: Additional information displayed below the ASCII art.
- **credits**: Optional credits or user information.

## ❗ Requirements

LogMagix requires:

- `colorama` for cross-platform color support in the terminal.
- `pystyle` for creating the colored text effects.

To install dependencies, run:

```bash
pip install colorama pystyle
```

## ©️ License

LogMagix is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🖥️ Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## 👤 Author

LogMagix is developed and maintained by **sexfrance**.

# LogMagix

**LogMagix** is a custom Python logging package that provides styled, colorful log messages for various logging levels, such as success, warning, failure, and more. It includes advanced features such as batch logging, file logging, customizable animated loaders, and ASCII art displays through the `Home` class, perfect for adding visual appeal to terminal-based applications.

## 🔥 Features

- **Enhanced Logging Levels**: Support for `LogLevel` enumeration, including `DEBUG`, `INFO`, `WARNING`, `SUCCESS`, `ERROR`, and `CRITICAL`, allowing fine-grained control over log output.
- **Batch Logging Mode**: Queue messages to batch display them at once.
- **File Logging**: Optionally log messages to a file with rotating log handlers.
- **Color Customization**: ANSI escape sequences for colorful terminal output.
- **Timestamped Messages**: Precise logging with time-based messages.
- **Loader with Animation**: Built-in animated loader for long-running operations with customizable text and style.
- **ASCII Art Display**: Display ASCII art with custom messages, branding, or system information.
- **User Welcome**: Personalized greetings in the ASCII art screen.

## ⚙️ Installation

Install LogMagix locally:

```bash
pip install .
```

Or via PyPI:

```bash
pip install logmagix
```

## 🔧 Usage

### Importing the Package

```python
from logmagix import Logger, Loader, Home, LogLevel
```

### Logging

Initialize the `Logger` class and log messages at different levels. You can now also set the minimum log level, batch log messages, and write them to a file:

```python
log = Logger(log_file="app.log", prefix="myapp/logs")

# Set minimum log level to control the output (optional)
log.set_min_level(LogLevel.INFO)

# Log levels
log.success("Operation completed successfully!")
log.failure("Something went wrong!")
log.warning("This is a warning!")
log.info("Informational log message")
log.debug("Debugging log message")
log.critical("Critical error encountered", exit_code=1)  # Exits after logging
log.message("Custom", "Custom message with prefix")

# Batch Logging Example
log.batch()  # Start batch mode
log.success("Batch message 1")
log.info("Batch message 2")
log.flush()  # Output all batched messages
```

### File Logging

Save logs to a file with rotation options:

```python
log = Logger(
    log_file="my_app.log",
    max_file_size=5_000_000,  # 5MB max file size
    backup_count=3            # Keep 3 backup files
)
log.info("Logging to file with rotation setup!")
```

### Loading Animation

Use the `Loader` class in two ways:

1. **Context Manager**:

   ```python
   from time import sleep

   with Loader(desc="Loading data..."):
       sleep(2)
   ```

2. **Start/Stop Methods**:

   ```python
   loader = Loader(desc="Saving files...", end="Done!").start()
   sleep(2)
   loader.stop()
   ```

### ASCII Art and Welcome Display

The `Home` class allows you to display ASCII art along with user greetings and system information.

```python
home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="logmagix.io",
    adinfo2="v1.2",
    credits="Developed by sexfrance"
)
home_screen.display()
```

### Full Example

Here’s an example showing logging, loader, and the `Home` ASCII art functionality:

```python
from logmagix import Logger, Loader, Home
import time

log = Logger(log_file="app.log", prefix="myapp")

# Logging
log.success("Everything is running smoothly!")
log.warning("This is just a warning!")
log.failure("A critical error occurred.")
log.debug("System debug message")

# Loader with context manager
with Loader(prefix="myapp/loader", desc="Processing data..."):
    time.sleep(2)

# ASCII Art Home screen
home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="https://logmagix.io",
    adinfo2="v1.2",
    credits="Developed by sexfrance"
)
home_screen.display()
```

## 🛠️ Configuration Options

### Logger

- **Log Levels**: Control which levels to log using `LogLevel` enumeration, including `DEBUG`, `INFO`, `WARNING`, `SUCCESS`, `ERROR`, and `CRITICAL`. Set a minimum level to ignore lower-priority messages.
- **prefix**: Custom prefix before each log message.
- **log_file**: File path to log messages.
- **max_file_size**: Maximum size for log files (default is 10MB).
- **backup_count**: Number of backup log files to keep.

### Loader

- **desc**: Description displayed alongside the loading animation.
- **end**: Text displayed after the loader stops.
- **timeout**: Delay between animation frames (in seconds).

### Home

- **text**: ASCII text to display.
- **align**: Text alignment in the terminal ("left", "center", "right").
- **adinfo1 / adinfo2**: Additional info displayed below the ASCII art.
- **credits**: Custom credits or developer name.

## 🖥️ Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request for review.

For major changes, please open an issue first to discuss what you’d like to change.

## ©️ License

LogMagix is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👤 Author

LogMagix is developed and maintained by **sexfrance**.

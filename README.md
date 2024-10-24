# LogMagix

**LogMagix** is a custom Python logging package that offers styled, colorful log messages for various logging levels such as success, warning, failure, and more. It also features an animated loader class for providing a visual indicator during long-running operations in the terminal.

## 🔥 Features

- Log messages for success, warning, failure, and informational levels.
- Customize message colors using ANSI escape sequences.
- Time-stamped log messages for better tracking.
- Built-in animated loader for visually appealing loading spinners.
- Customizable log and loader prefixes.
- Simple and flexible API with multiple ways to use the `Loader` class.

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
from logmagix import Logger, Loader
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

# Question input
log.question("This is an input question!")
```

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

Both the `Logger` and `Loader` classes allow for customizing the prefix that is shown before each message:

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

### Full Example

Here’s an example showing both logging and loader functionality:

```python
from logmagix import Logger, Loader
import time

log = Logger(prefix="custom/log/prefix")

# Log messages
log.success("Everything is running smoothly!")
log.warning("Watch out, something might happen!")
log.failure("Critical error occurred!")

# Use loader with custom prefix and context manager
with Loader(prefix="custom/loader/prefix", desc="Processing data..."):
    time.sleep(5)  # Simulate task

# Use loader with custom prefix and start/stop methods
loader = Loader(prefix="custom/loader/prefix", desc="Saving files...", end="Done!", timeout=0.05).start()
time.sleep(5)  # Simulate task
loader.stop()

log.success("Processing completed!")
```

## ❗ Requirements

LogMagix requires:

- `colorama` for cross-platform color support in the terminal.

To install `colorama`, run:

```bash
pip install colorama
```

## ©️ License

LogMagix is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🖥️ Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## 👤 Author

LogMagix is developed and maintained by **sexfrance**.

---

Enjoy bringing more color and animation to your Python logging with **LogMagix**!



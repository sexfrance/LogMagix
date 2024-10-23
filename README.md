# LogMagix

**LogMagix** is a custom Python logging package that provides colorful and styled log messages for success, warnings, failures, and more. It also includes a loader class for displaying animated loading sequences in the terminal.

## 🔥 Features

- Log messages with success, warning, failure, and informational levels.
- Customize log message colors using ANSI color codes.
- Time-stamped log messages for tracking events.
- Animated loading spinner for long-running operations.
- Flexible message format and easy-to-use API.

## ⚙️ Installation

To install the package locally, clone the repository and run:

```bash
pip install .
```

Alternatively, once published, you can install it via `pip` from PyPI:

```bash
pip install logmagix
```

## 🔧 Usage

### Import the Package

```python
from logmagix import Logger, Loader
```

### Basic Logging

Create an instance of the `Logger` class and log messages with different levels:

```python
log = Logger()

# Success message
log.success("Operation completed successfully!")

# Failure message
log.failure("Something went wrong!")

# Warning message
log.warning("This is a warning!")

# Information message
log.info("Informational log message")

# Debug message
log.debug("Debugging log message")
```

### Loading Animation

Use the `Loader` class to display an animated loading spinner during long-running operations:

```python
from logmagix import Loader
import time

loader = Loader(desc="Connecting to server...")
with loader:
    time.sleep(5)  # Simulate a task that takes 5 seconds
```

### Customizing Log Prefix

You can customize the prefix used in log messages by passing it as a parameter to the `Logger`:

```python
log = Logger(prefix=".myapp/logs")
log.success("Custom prefix message")
```

## 🔎 Example

Here’s a full example demonstrating both logging and loader:

```python
from logmagix import Logger, Loader
import time

# Initialize the logger
log = Logger()

# Log different types of messages
log.success("Everything is running smoothly!")
log.warning("This is a warning message.")
log.failure("Critical failure detected!")

# Use a loader for a long-running task
loader = Loader(desc="Processing data...")
with loader:
    time.sleep(5)  # Simulate a task that takes 5 seconds

log.success("Task completed!")
```

## ❗ Requirements

LogMagix requires the following Python package:

- `colorama` for cross-platform color support in the terminal.

Install `colorama` if it’s not already installed:

```bash
pip install colorama
```

## ©️ License

LogMagix is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🖥️ Contributing

Contributions are welcome! If you would like to contribute to the project, feel free to fork the repository and submit a pull request.

## 👤 Author

LogMagix is developed and maintained by **sexfrance**.

---

Enjoy using **LogMagix** to bring color and style to your Python logging!

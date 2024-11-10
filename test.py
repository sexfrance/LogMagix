from logmagix.logger import Logger, Loader, Home, LogLevel
import time
import uuid

log = Logger(prefix=None)
start_time = time.time()

# Log messages
log.success("Everything is running smoothly!")
log.warning("Watch out, something might happen!")
log.failure("Critical error occurred!")
log.info("System is working properly")
log.debug(f"The system uuid is {uuid.getnode()}")
log.message("Dad", f"How are you? I'm gonna come soon!", start=start_time, end=time.time())
log.question("How old are you? ")


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
    adinfo1="Test Suite",
    adinfo2="v1.0.0",
    credits="Testing Framework",
    clear=True
)
home.display()

# Test loader animation
with Loader(prefix="TestLoader", desc="Initializing tests...", timeout=0.1):
    time.sleep(2)

# Test all log levels
logger.info("Starting test suite")
logger.debug("Debug information")
logger.warning("Warning message")
logger.success("Success message")
logger.failure("Failure message")

# Test log level filtering
logger.info("Testing log level filtering...")
logger.set_min_level(LogLevel.WARNING)  # Only show WARNING and above
logger.debug("This debug message should not appear")
logger.info("This info message should not appear")
logger.warning("This warning message should appear")
logger.success("This success message should appear")
logger.failure("This error message should appear")

# Reset log level
logger.set_min_level(LogLevel.DEBUG)

# Test batch logging
logger.info("Testing batch logging...")
logger.batch()
for i in range(2):
    logger.info(f"Batch message {i+1}")
    logger.success(f"Batch success {i+1}")
    logger.warning(f"Batch warning {i+1}")
    logger.failure(f"Batch failure {i+1}")
    time.sleep(0.5)
logger.flush()

# Test message format with precise timing
logger.message("FORMAT1", "Testing message format 1")
start = time.time()
time.sleep(0.456)
end = time.time()
logger.message("FORMAT2", "Testing message format 2", start=start, end=end)

# Test user input
answer = logger.question("Would you like to test critical exit? (y/n)")
if answer.lower() == 'y':
    logger.critical("Critical exit test", exit_code=1)

# Test loader with different end messages
with Loader(prefix="TestLoader", desc="Processing", end="Process completed!", timeout=0.05):
    time.sleep(1)

with Loader(prefix="TestLoader", desc="Analyzing", end="Analysis done!", timeout=0.15):
    time.sleep(1)

# Test Home with different alignments
home = Home(
    text="TEST",
    align="right",
    adinfo1="Right Aligned",
    adinfo2="Test",
    credits="Alignment Test",
    clear=False
)
home.display()

# Final loader with completion message
with Loader(prefix="TestLoader", desc="Finalizing", end="Tests completed!"):
    time.sleep(2)

logger.success("All tests completed successfully!")
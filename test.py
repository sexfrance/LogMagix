from logmagix.logger import Logger, Loader, Home, LogLevel
import time
import uuid

log = Logger(prefix=None, log_file="logs/app.log")
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

log.critical("Critical error occurred!")


home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="Test Suite",
    adinfo2="v1.0.0",
    credits="Testing Framework",
    clear=True
)
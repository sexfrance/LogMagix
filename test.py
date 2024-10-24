from logmagix.logger import Logger, Loader
# from logmagix import Logger, Loader
import time
import uuid

log = Logger(prefix="custom/log/prefix")

# Log messages
log.success("Everything is running smoothly!")
log.warning("Watch out, something might happen!")
log.failure("Critical error occurred!")
log.info("System is working properly")
log.debug(f"The system uuid is {uuid.getnode()}")
log.question("How old are you?")

# Use loader with custom prefix and context manager
with Loader(prefix="custom/loader/prefix", desc="Processing data..."):
    time.sleep(2)  # Simulate task

# Use loader with custom prefix and start/stop methods
loader = Loader(prefix="custom/loader/prefix", desc="Saving files...", end="Done !", timeout=0.05).start()
time.sleep(2)  # Simulate task
loader.stop()

log.success("Processing completed!")
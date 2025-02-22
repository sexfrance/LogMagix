from logmagix import Logger, Home, Loader, LogLevel
import time
import uuid

# Test ColorLogger (Style 1 - Default)
log1 = Logger(
    github_repository="https://github.com/sexfrance/LogMagix",
    level=LogLevel.DEBUG,
    log_file="logs/color.log"
)

start_time = time.time()
log1.success("We are running style 1!")
log1.warning("Watch out, something might happen!")
log1.failure("Critical error occurred!")
log1.info("System is working properly")
log1.debug(f"The system uuid is {uuid.getnode()}")
log1.message("Dad", f"How are you? I'm gonna come soon!", start=start_time, end=time.time())
log1.question("How old are you? ")

# Test SimpleLogger (Style 2)
log2 = Logger(
    style=2,
    prefix="SimpleLogger",
    level=LogLevel.INFO,
    log_file="logs/simple.log"
)

start_time = time.time()
log2.success("We are running style 2 !")
log2.info("System is working properly")
log2.error("Critical error occurred!")
log2.warning("Watch out, something might happen!")
log2.message("System is working properly")
log2.debug(f"The system uuid is {uuid.getnode()}")
log2.question("How old are you? ")

# Test loader with custom prefix and context manager
print("\nTesting Loader:")
with Loader(prefix="custom/loader/prefix", desc="Processing data..."):
    time.sleep(2)  # Simulate task

# Use loader with custom prefix and start/stop methods
loader = Loader(prefix="custom/loader/prefix", desc="Saving files...", end="Done !", timeout=0.05).start()
time.sleep(2)  # Simulate task
loader.stop()

# Display home screen
home_screen = Home(
    text="LogMagix",
    align="center",
    adinfo1="Test Suite",
    adinfo2="v1.0.0",
    credits="Testing Framework",
    clear=True
)
home_screen.display()

# Test critical error (commented out as it exits the program)
log1.critical("Critical error occurred!")
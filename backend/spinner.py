import sys
import time
import itertools

def spinning_cursor():
    """Generate a spinning cursor animation."""
    spinner = ['-', '\\', '|', '/']
    for cursor in itertools.cycle(spinner):
        yield cursor

def loading_animation(duration):
    """Show a loading animation for a specified duration."""
    spinner = spinning_cursor()
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(next(spinner))  # Write the next spinner character
        sys.stdout.flush()               # Ensure it appears immediately
        sys.stdout.write('\b')           # Move the cursor back
        time.sleep(0.1)                  # Adjust the speed of the spinner

if __name__ == "__main__":
    print("Loading, please wait...")
    loading_animation(1000)  # Adjust the duration as needed
    print("\nDone!")

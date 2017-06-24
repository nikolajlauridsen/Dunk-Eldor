import time


class CountDown:
    """Generic countdown timer class"""
    def __init__(self):
        self.paused = True
        self.start_time = 0
        self.duration = 0

    def set_duration(self, duration):
        """Set (or reset) the duration of the countdown clock."""
        self.duration = duration

    def start(self):
        """Start/Resume the clock.
        Sets pause flag to false."""
        self.start_time = time.time()
        self.paused = False

    def pause(self):
        """Pause the countdown clock.
        Reduces duration with time elapsed.
        Sets pause flag to true."""
        self.duration -= (time.time() - self.start_time)
        self.paused = True

    def reset(self):
        """Reset the countdown"""
        self.paused = True
        self.start_time = 0
        self.duration = 0

    def expired(self):
        """Check whether the countdown timer has expired.
        Returns: True/False"""
        if not self.paused:
            if time.time() >= self.start_time + self.duration:
                return True
            else:
                return False
        else:
            return False

    def get_duration(self):
        """Return the remaining duration in seconds"""
        if not self.paused:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0

        return self.duration - elapsed

    def get_remaining_string(self):
        """Get the remaining time as a string representation.
        Format: HH:MM:SS
        Returns: Remaining time as a string."""
        remaining = self.get_duration()
        if remaining < 0:
            remaining = 0

        mins = remaining // 60
        s = remaining % 60
        return "{:02}:{:02}".format(int(mins), int(s))

    @staticmethod
    def seconds_to_timestamp(seconds):
        """Convert seconds into a neatly formatted string.
        Format: DD:HH:MM
        Returns: Timestamp string."""
        days = seconds // (3600 * 24)
        hrs = (seconds % (3600 * 24)) // 3600
        mins = (seconds % 3600) // 60
        return "{:02}:{:02}:{:02}".format(int(days), int(hrs), int(mins))

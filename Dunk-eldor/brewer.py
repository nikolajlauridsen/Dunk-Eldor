from .help.Servo import Servo
from .help.countdown import CountDown
import time


class Brewer(Servo):
    def __init__(self, screen, buttons):
        super().__init__(high=13)

        self.screen = screen
        self.buttons = buttons
        self.watch = CountDown()
        self.display_watch = CountDown()

        self.set_position(0)
        self.dipped = False

    def dip(self):
        self.set_position(180)
        self.dipped = True

    def undip(self):
        self.set_position(0)
        self.dipped = False

    def wait(self, duration):
        # Set the clock
        self.watch.set_duration(duration)
        self.watch.start()

        # Wait for it to expire
        while not self.watch.expired():
            self.screen.lcd_display_string(self.display_watch.get_remaining_string()
                                           .center(16), 2)
            time.sleep(0.2)
        # reset the watch again
        self.watch.reset()

    def dunk(self, duration, pause=0.5):
        self.dip()
        self.wait(duration)
        self.undip()
        self.wait(pause)

    def start_cycle(self, name, duration, dunks):
        self.screen.lcd_display_string(name.center(16), 1)
        wait_time = duration / dunks
        for n in range(dunks):
            self.dunk(wait_time)

    def run_cycles(self, cycles):
        """
        List of dictionaries containing information about the cycles
        Format:
        {"name": cycle name,
        "duration": cycle duration.
        "dunks": number of dunks}
        """
        # Calculate total runtime
        runtime = 0
        for cycle in cycles:
            # It takes 0.5 seconds to dunk
            runtime += cycle["duration"] + 0.5 * cycle["dunks"]

        self.display_watch.set_duration(runtime)
        self.display_watch.start()

        for cycle in cycles:
            self.start_cycle(cycle["name"], cycle["duration"], cycle["dunks"])

        self.display_watch.reset()


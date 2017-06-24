import time

import RPi.GPIO as GPIO

from .help import LCD_driver as lcd_driver
from .brewer import Brewer

buttons = {"right": 23,
           "middle": 24,
           "left": 25}

beeper = 22

programs = [{"program_name": "Black Tea",
             "cycles": [{"name": "Soak", "duration": 6, "dunks": 3},
                        {"name": "Steep", "duration": 480, "dunks": 8}]},
            {"program_name": "Test",
             "cycles": [{"name": "Soak", "duration": 4, "dunks": 2},
                        {"name": "Steep", "duration": 10, "dunks": 2}]},
            {"program_name": "Rooibos",
             "cycles": [{"name": "Soak", "duration": 8, "dunks": 4},
                        {"name": "Steep", "duration": 240, "dunks": 4}]}
            ]


def main():
    GPIO.setmode(GPIO.BCM)

    # Set up buttons
    for button in buttons.values():
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(button, GPIO.RISING, bouncetime=300)
    GPIO.setup(beeper, GPIO.OUT, initial=GPIO.LOW)

    # Initiate screen
    screen = lcd_driver.lcd()

    brewer = Brewer(screen, buttons)

    cursor = 0

    while True:
        screen.lcd_display_string("Choose program".center(16), 1)
        screen.lcd_display_string(programs[cursor]["program_name"].center(16), 2)

        if GPIO.event_detected(buttons["middle"]):
            brewer.run_cycles(programs[cursor]["cycles"])
            for n in range(2):
                GPIO.output(beeper, GPIO.HIGH)
                time.sleep(0.3)
                GPIO.output(beeper, GPIO.LOW)
                time.sleep(0.5)
        elif GPIO.event_detected(buttons['left']):
            if cursor > 0:
                cursor -= 1
            else:
                cursor = len(programs) - 1
        elif GPIO.event_detected(buttons['right']):
            if cursor < len(programs) - 1:
                cursor += 1
            else:
                cursor = 0
        time.sleep(0.2)


def cleanup():
    for button in buttons.values():
        GPIO.cleanup(button)
    GPIO.cleanup(beeper)

if __name__ == "__main__":
    main()
    cleanup()

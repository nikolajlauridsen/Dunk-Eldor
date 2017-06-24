import RPi.GPIO as GPIO

SERVO_PIN = 18


class Servo:
    """Control a servo"""
    def __init__(self, low=2.4, high=11):
        GPIO.setup(18, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 50)
        self.pwm.start(2.4)
        self.low = low
        self.high = high

    def set_position(self, angle):
        """Set the position of the servo"""
        duty = self.mapvalue(angle, 0, 180, self.low, self.high)
        print("Lock:\tDuty:" + str(duty))
        self.pwm.ChangeDutyCycle(duty)

    @staticmethod
    def mapvalue(value, leftMin, leftMax, rightMin, rightMax):
        """Maps one range to another.
        Code taken from:
        http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another"""
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)
import RPi.GPIO as GPIO
import time
import yagmail

# Moisture Sensor configuration
MOISTURE_SENSOR_PIN = 5  # D5 pin for the moisture sensor

# Ultrasonic Sensor configuration
ULTRASONIC_PIN = 18  # GPIO 18 pin for the ultrasonic sensor (Trig and Echo combined)

# Email configuration
SENDER_EMAIL = "smirthomeg17@gmail.com"  # Sender's email
APP_PASSWORD = "tjmk ahdn eske qtls"     # App-specific password
RECEIVER_EMAILS = [
    "francisco.ruizsandoval@student.kuleuven.be",
    "changlai.zhang@student.kuleuven.be"
]

# State variable
last_thirsty_alert_sent = False  # Avoid sending duplicate "dog is thirsty" emails


def send_email(subject, content):
    """Send an email notification."""
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
        yag.send(to=RECEIVER_EMAILS, subject=subject, contents=content)
        print(f"Email sent successfully to: {RECEIVER_EMAILS}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def measure_distance():
    """Measure the distance using the ultrasonic sensor."""
    GPIO.setup(ULTRASONIC_PIN, GPIO.OUT)
    # Send Trig signal
    GPIO.output(ULTRASONIC_PIN, True)
    time.sleep(0.00001)  # Send a 10-microsecond pulse
    GPIO.output(ULTRASONIC_PIN, False)

    # Switch to Echo mode
    GPIO.setup(ULTRASONIC_PIN, GPIO.IN)
    start_time = time.time()
    stop_time = time.time()

    # Record the time of the Echo signal
    while GPIO.input(ULTRASONIC_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ULTRASONIC_PIN) == 1:
        stop_time = time.time()

    # Calculate distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound is 343 m/s
    return distance


def read_moisture():
    """Read the moisture sensor status."""
    moisture = GPIO.input(MOISTURE_SENSOR_PIN)
    if moisture == 1:
        print("Moisture Status: Wet (Water detected)")
    else:
        print("Moisture Status: Dry (No water detected)")
    return moisture


def monitor():
    """Main monitoring logic."""
    global last_thirsty_alert_sent

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

        while True:
            # Check moisture sensor status
            moisture = read_moisture()

            # Measure distance using the ultrasonic sensor
            distance = measure_distance()
            print(f"Distance: {distance:.2f} cm")

            # Send an email if the dog is near and the bowl is dry
            if distance < 15 and moisture == 0:  # Dog near and water is dry
                if not last_thirsty_alert_sent:
                    print("Dog is near and water is dry!")
                    send_email("Thirsty Alert", "Your dog is thirsty.")
                    last_thirsty_alert_sent = True
            else:
                last_thirsty_alert_sent = False  # Reset alert state if conditions are not met

            time.sleep(10)  # Check every 10 seconds

    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    monitor()

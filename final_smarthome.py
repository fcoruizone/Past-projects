import RPi.GPIO as GPIO
import time
import yagmail


MOISTURE_SENSOR_PIN = 5  
ULTRASONIC_PIN = 18  


SENDER_EMAIL = "smirthomeg17@gmail.com" 
APP_PASSWORD = "**** **** **** ****"     # Censored App-specific password 
RECEIVER_EMAILS = [
    "francisco.ruizsandoval@student.kuleuven.be",
]

last_thirsty_alert_sent = False 


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

    GPIO.output(ULTRASONIC_PIN, True)
    time.sleep(0.00001)  
    GPIO.output(ULTRASONIC_PIN, False)


    GPIO.setup(ULTRASONIC_PIN, GPIO.IN)
    start_time = time.time()
    stop_time = time.time()

 
    while GPIO.input(ULTRASONIC_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ULTRASONIC_PIN) == 1:
        stop_time = time.time()


    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2 
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
        
            moisture = read_moisture()

           
            distance = measure_distance()
            print(f"Distance: {distance:.2f} cm")

            if distance < 15 and moisture == 0:  
                if not last_thirsty_alert_sent:
                    print("Dog is near and water is dry!")
                    send_email("Thirsty Alert", "Your dog is thirsty.")
                    last_thirsty_alert_sent = True
            else:
                last_thirsty_alert_sent = False 
            time.sleep(10)  

    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    monitor()

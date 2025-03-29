#!/usr/bin/env python

import time
import csv
from datetime import datetime
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor  # Import the Grove Light Sensor
from seeed_dht import DHT

# Initialize sensors
ultrasonic_sensor = GroveUltrasonicRanger(18)  # USS on port D5
light_sensor = GroveLightSensor(0)  # Light sensor on port D16
sensor = DHT('11', 5)

# CSV file setup
csv_filename = "MS3_data.csv"
csv_headers = ["Timestamp", "Ultrasonic Distance (cm)", "Light Sensor Value", "Temperature", "Humidity"]

def write_to_csv(data, filename=csv_filename):
    """Write data to a CSV file."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    # Create the CSV file and write the headers
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

    start_time = time.time()
    while time.time() - start_time < 350:  # Run for 5 minutes
        try:
            # Read sensor data
            distance = ultrasonic_sensor.get_distance()
            light_value = light_sensor.light  # Get light sensor value
            humi, temp = sensor.read()
            
            # Capture the timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Write data to CSV
            data = [timestamp, distance, light_value, humi, temp]
            write_to_csv(data)
            
            # Print data to console for debugging
            print(f"Timestamp: {timestamp}, Distance: {distance} cm, Light Sensor Value: {light_value}, Temperature: {temp}, Humidity: {humi}")
            
            # Wait for a short interval before reading again
            time.sleep(5)
        except Exception as e:
            print(f"Error reading sensors: {e}")
            break

if __name__ == "__main__":
    main()

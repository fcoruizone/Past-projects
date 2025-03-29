

# Subproject created to study data aquisition 

import time
import csv
from datetime import datetime
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor 
from seeed_dht import DHT


ultrasonic_sensor = GroveUltrasonicRanger(18) 
light_sensor = GroveLightSensor(0)  
sensor = DHT('11', 5)


csv_filename = "MS3_data.csv"
csv_headers = ["Timestamp", "Ultrasonic Distance (cm)", "Light Sensor Value", "Temperature", "Humidity"]

def write_to_csv(data, filename=csv_filename):
    """Write data to a CSV file."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

    start_time = time.time()
    while time.time() - start_time < 350:  
        try:
      
            distance = ultrasonic_sensor.get_distance()
            light_value = light_sensor.light 
            humi, temp = sensor.read()
            
        
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
           
            data = [timestamp, distance, light_value, humi, temp]
            write_to_csv(data)
            
         
            print(f"Timestamp: {timestamp}, Distance: {distance} cm, Light Sensor Value: {light_value}, Temperature: {temp}, Humidity: {humi}")
            

            time.sleep(5)
        except Exception as e:
            print(f"Error reading sensors: {e}")
            break

if __name__ == "__main__":
    main()

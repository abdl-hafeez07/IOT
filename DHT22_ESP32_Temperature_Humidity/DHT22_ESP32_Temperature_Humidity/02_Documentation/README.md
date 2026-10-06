# ESP32 + DHT22 Temperature and Humidity Monitoring

## Objective
Develop an ESP32-based system to read temperature and humidity from a DHT22 sensor and display the values through the Serial Monitor.

## Components Required
- ESP32 development board
- DHT22 temperature and humidity sensor
- 10 kΩ resistor (recommended when using a bare 4-pin DHT22)
- Breadboard
- Jumper wires
- USB cable
- Computer with Arduino IDE

## Wiring

### DHT22 4-pin sensor
Looking at the front of the DHT22 sensor:

| DHT22 Pin | Connection |
|---|---|
| Pin 1 - VCC | ESP32 3.3V |
| Pin 2 - DATA | ESP32 GPIO 4 |
| Pin 3 - NC | Not connected |
| Pin 4 - GND | ESP32 GND |

For a bare 4-pin DHT22, connect a 10 kΩ pull-up resistor between VCC and DATA.

> If you are using a DHT22 module, the pull-up resistor may already be included on the module.

## Arduino IDE Setup

1. Install Arduino IDE.
2. Add ESP32 board support if it is not already installed.
3. Select:
   - Board: your ESP32 board (commonly "ESP32 Dev Module")
   - Correct COM port
4. Install the following library:
   - DHT sensor library by Adafruit
5. The Adafruit DHT library may also ask for the Adafruit Unified Sensor library. Install it if prompted.
6. Open:
   `01_Arduino_Code/DHT22_ESP32.ino`
7. Connect the ESP32 using USB.
8. Select the correct board and COM port.
9. Click Upload.
10. Open Serial Monitor.
11. Set baud rate to **115200**.
12. Wait for readings. The DHT22 is read every 2 seconds.

## Expected Serial Monitor Output

ESP32 DHT22 Temperature and Humidity Monitor
--------------------------------------------
Temperature: 28.4 °C   Humidity: 67.2 %
Temperature: 28.5 °C   Humidity: 66.9 %
Temperature: 28.6 °C   Humidity: 66.5 %

The exact readings depend on the room/environment.

## Working

1. ESP32 initializes the DHT22 sensor.
2. DHT22 measures temperature and relative humidity.
3. ESP32 reads the sensor values through GPIO 4.
4. The values are sent to the Serial Monitor at 115200 baud.
5. A 2-second delay is used between readings because DHT22 is a relatively slow sensor.

## Important Exam Points

- Sensor: DHT22
- Controller: ESP32
- Data pin used: GPIO 4
- Supply used: 3.3V
- Serial baud rate: 115200
- Reading interval: 2 seconds
- Temperature unit: °C
- Humidity unit: %

## Result

The ESP32 successfully interfaces with the DHT22 sensor, reads temperature and humidity, and displays the sensor readings on the Serial Monitor.

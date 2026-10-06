# ESP32 + LDR Light Intensity Monitoring

## Objective
Develop an ESP32-based light intensity monitoring system using an LDR sensor and display the sensor readings through the Serial Monitor.

## Components Required
- ESP32 development board
- LDR (Light Dependent Resistor)
- 10 kΩ resistor
- Breadboard
- Jumper wires
- USB cable
- Computer with Arduino IDE

## Important Note
An LDR does not directly provide a digital light-intensity value. It changes its resistance according to the amount of light. Therefore, the LDR is connected with a 10 kΩ resistor as a voltage divider, and the resulting analog voltage is read by the ESP32 ADC.

The program displays the raw ADC value and the corresponding approximate voltage. The ADC value changes with light level.

## Wiring

Use a voltage-divider connection:

3.3V ---- LDR ----+---- GPIO 34
                  |
                 10 kΩ
                  |
                 GND

### Pin connections

| Component | Connection |
|---|---|
| LDR one terminal | ESP32 3.3V |
| LDR other terminal | ESP32 GPIO 34 |
| 10 kΩ resistor one terminal | GPIO 34 |
| 10 kΩ resistor other terminal | ESP32 GND |

GPIO 34 is an input-only ADC pin and is suitable for reading the LDR voltage.

## Arduino IDE Setup

1. Install Arduino IDE.
2. Install ESP32 board support if required.
3. Select the ESP32 board, commonly:
   `ESP32 Dev Module`
4. Select the correct COM port.
5. No external Arduino library is required for this program.
6. Open:
   `01_Arduino_Code/LDR_ESP32.ino`
7. Connect the ESP32 through USB.
8. Upload the program.
9. Open Serial Monitor.
10. Set the baud rate to **115200**.

## Expected Output

Example readings can look like:

LDR ADC Value: 3250   Voltage: 2.62 V
LDR ADC Value: 3180   Voltage: 2.56 V
LDR ADC Value: 2100   Voltage: 1.69 V
LDR ADC Value: 850    Voltage: 0.68 V

The exact values depend on the LDR, resistor, room lighting, and wiring.

## Demonstration

### Bright light
Place the LDR under a bright light. Observe the ADC value.

### Reduced light
Cover the LDR partially with your hand. Observe the ADC value change.

### Dark condition
Cover the LDR completely. The ADC value should change significantly.

> With the wiring used in this project (LDR to 3.3V and resistor to GND), the ADC value generally increases when the LDR is exposed to more light. The exact behavior and range depend on the LDR and resistor.

## Working

1. The LDR resistance changes according to light intensity.
2. The LDR and 10 kΩ resistor form a voltage divider.
3. The voltage divider produces an analog voltage.
4. ESP32 ADC on GPIO 34 reads this analog voltage.
5. ESP32 converts the ADC reading to an approximate voltage.
6. The ADC value and voltage are displayed on the Serial Monitor every second.

## Result

The ESP32 successfully interfaces with the LDR sensor and monitors changes in light level through the analog ADC reading displayed on the Serial Monitor.

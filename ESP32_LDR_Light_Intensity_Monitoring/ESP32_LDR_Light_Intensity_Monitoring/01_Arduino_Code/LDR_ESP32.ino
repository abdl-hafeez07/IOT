/*
  Q - ESP32 Light Intensity Monitoring using LDR
  Board: ESP32
  Sensor: LDR (Light Dependent Resistor)

  The LDR is connected as a voltage divider.
  ADC pin used: GPIO 34
*/

#define LDR_PIN 34

void setup() {
  Serial.begin(115200);
  delay(1000);

  // ESP32 ADC range: 0 to 4095
  analogReadResolution(12);

  Serial.println("ESP32 LDR Light Intensity Monitor");
  Serial.println("---------------------------------");
}

void loop() {
  int ldrValue = analogRead(LDR_PIN);

  // Convert ADC value to approximate voltage.
  float voltage = (ldrValue / 4095.0) * 3.3;

  Serial.print("LDR ADC Value: ");
  Serial.print(ldrValue);

  Serial.print("   Voltage: ");
  Serial.print(voltage, 2);
  Serial.println(" V");

  delay(1000);
}

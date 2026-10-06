/*
  Q1: DHT22 Temperature and Humidity Monitoring
  Board: ESP32
  Sensor: DHT22
*/

#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("ESP32 DHT22 Temperature and Humidity Monitor");
  Serial.println("--------------------------------------------");

  dht.begin();
}

void loop() {
  delay(2000);  // DHT22 needs about 2 seconds between readings

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  // Celsius

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT22 sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature, 1);
  Serial.print(" °C");

  Serial.print("   Humidity: ");
  Serial.print(humidity, 1);
  Serial.println(" %");
}

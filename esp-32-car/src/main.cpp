// In src/main.cpp - A minimal test sketch

#include <Arduino.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_Test");
  Serial.println("Minimal BT sketch running. Ready to pair.");
}

void loop() {
  // Do nothing but keep the connection alive.
  delay(100);
}
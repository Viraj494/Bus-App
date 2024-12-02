// GSM modem setup
#define TINY_GSM_MODEM_SIM800  // Use this for SIM800 series modems

#include <TinyGsmClient.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

// GPRS credentials (APN, user, password for Dialog SIM)
const char apn[]      = "dialogbb";  // APN for Dialog
const char gprsUser[] = "";          // GPRS User (leave blank if not required)
const char gprsPass[] = "";          // GPRS Password (leave blank if not required)

// SIM card PIN (leave blank if not required)
const char simPIN[]   = ""; 

// Server details
const char server[] = "3.86.100.41";  // Server IP
const char resource[] = "/update/-OCh1E_ftKFuVrGk9F0n"; // Resource path
const int  port = 5000;                // HTTP port

// SIM800L pins
#define MODEM_RST            5
#define MODEM_PWKEY          4
#define MODEM_POWER_ON       23
#define MODEM_TX             27
#define MODEM_RX             26

// GPS module setup
TinyGPSPlus gps;
#define GPS_RX_PIN 4  // Adjust to available GPIO pins on your ESP32
#define GPS_TX_PIN 0
HardwareSerial SerialGPS(1);  // Use HardwareSerial1 for GPS communication

// Initialize GSM modem
HardwareSerial SerialAT(2);  // Define SerialAT as Serial2
TinyGsm modem(SerialAT);      // Use SerialAT for GSM communication
TinyGsmClient client(modem);

// Variables for GPS data
float latitude, longitude, speed;
int year, month, date, hour, minute, second;
const int utcOffsetHours = 5;
const int utcOffsetMinutes = 30;

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(MODEM_PWKEY, OUTPUT);
  pinMode(MODEM_RST, OUTPUT);
  pinMode(MODEM_POWER_ON, OUTPUT);
  digitalWrite(MODEM_PWKEY, LOW);
  digitalWrite(MODEM_RST, HIGH);
  digitalWrite(MODEM_POWER_ON, HIGH);

  SerialAT.begin(9600, SERIAL_8N1, MODEM_RX, MODEM_TX);  // Use SerialAT (Serial2)
  delay(3000);

  Serial.println("Initializing modem...");
  if (!modem.restart()) {
    Serial.println("Modem restart failed!");
    while (true);
  }
  Serial.println("Modem initialized.");

  // Signal Quality
  int signalQuality = modem.getSignalQuality();
  Serial.print("Signal Quality: ");
  Serial.println(signalQuality);

  // Network Operator
  String operatorName = modem.getOperator();
  Serial.print("Network Operator: ");
  Serial.println(operatorName);

  if (strlen(simPIN) && modem.getSimStatus() != 3) {
    modem.simUnlock(simPIN);
  }

  Serial.println("Connecting to GPRS...");
  if (!modem.gprsConnect(apn, gprsUser, gprsPass)) {
    Serial.println("Failed to connect to GPRS!");
    while (true);
  }
  Serial.println("GPRS connected.");

  // Initialize GPS module
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);  // Initialize HardwareSerial for GPS
  Serial.println("GPS Module Test");
}

void loop() {
  // Read GPS data
  while (SerialGPS.available() > 0) {
    if (gps.encode(SerialGPS.read())) {
      if (gps.location.isValid() && gps.date.isValid() && gps.time.isValid()) {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
        year = gps.date.year();
        month = gps.date.month();
        date = gps.date.day();
        hour = gps.time.hour();
        minute = gps.time.minute();
        second = gps.time.second();
        speed = gps.speed.kmph();

        // Adjust for time zone offset
        hour += utcOffsetHours;
        if (hour >= 24) {
          hour -= 24;
          date += 1;
        }
        minute += utcOffsetMinutes;
        if (minute >= 60) {
          minute -= 60;
          hour += 1;
        }

        Serial.print("Latitude: ");
        Serial.println(latitude, 6);
        Serial.print("Longitude: ");
        Serial.println(longitude, 6);
        Serial.print("Date: ");
        Serial.printf("%02d/%02d/%04d\n", date, month, year);
        Serial.print("Time: ");
        Serial.printf("%02d:%02d:%02d\n", hour, minute, second);
        Serial.print("Speed: ");
        Serial.println(speed, 2);
      } else {
        Serial.println("GPS data not valid yet...");
      }
    }
  }

  // Check GPS status periodically (every 10 seconds)
  static unsigned long gpsStatusPrevMillis = 0;
  if (millis() - gpsStatusPrevMillis > 10000) {
    gpsStatusPrevMillis = millis();
    if (!gps.location.isValid()) {
      Serial.println("Waiting for GPS signal...");
    }
  }

  // If GPS data is valid, send it to the server
  if (gps.location.isValid()) {
    Serial.println("Sending GPS data to server...");

    // Connect to server
    if (!client.connect(server, port)) {
      Serial.println("Connection failed!");
      delay(10000);
      return;
    }

    // Prepare HTTP POST request data
    String httpRequestData = String("{\"latitude\":") + latitude + 
                             ",\"longitude\":" + longitude + 
                             ",\"speed\":" + speed + "}";

    client.print(String("PUT") + resource + " HTTP/1.1\r\n");
    client.print(String("Host: ") + server + "\r\n");
    //client.println("Connection: close");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(httpRequestData.length());
    client.println();
    client.println(httpRequestData);

    // Read the server response
    unsigned long timeout = millis();
    while (client.connected() && millis() - timeout < 10000L) {
      if (client.available()) {
        char c = client.read();
        Serial.print(c);
        timeout = millis();
      }
    }
    //Serial.println("\nDisconnected from server.");

    //client.stop();  // Stop the client
    //modem.gprsDisconnect();  // Disconnect from GPRS
    //Serial.println("GPRS disconnected.");
  }

  delay(30000);  // Send data every 30 seconds (adjust as needed)
}

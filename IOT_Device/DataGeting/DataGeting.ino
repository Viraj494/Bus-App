#define TINY_GSM_MODEM_SIM800  

#include <TinyGsmClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <TinyGsmClient.h>

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 4); // 16x4 LCD, I2C address 0x27

const char apn[] = "dialogbb";  // APN for Dialog
const char gprsUser[] = "";    
const char gprsPass[] = "";     
const char simPIN[] = "";       

// Server details
const char server[] = "3.86.100.41"; // Server IP (use your IP address)
const char resource[] = "/getdata/-OCw-n1uHEw7KrwxGgHV"; // Resource path (root or your endpoint)
const int port = 5000; // HTTP port

// SIM800L pins
#define MODEM_RST            5
#define MODEM_PWKEY          4
#define MODEM_POWER_ON       23
#define MODEM_TX             27
#define MODEM_RX             26

// Set serial for debug console (Serial Monitor)
#define SerialMon Serial
// Set serial for AT commands (to SIM800L module)
#define SerialAT Serial1

TinyGsm modem(SerialAT);
TinyGsmClient client(modem);

void setup() {
  // Initialize I2C communication
  Wire.begin(21, 22); // SDA = 21, SCL = 22 on ESP32 (adjust if necessary)

  // Initialize LCD
  lcd.begin(16, 4);  // 16x4 LCD
  lcd.backlight();   // Turn on backlight

  // Initialize Serial communication
  SerialMon.begin(115200);
  delay(10);

  pinMode(MODEM_PWKEY, OUTPUT);
  pinMode(MODEM_RST, OUTPUT);
  pinMode(MODEM_POWER_ON, OUTPUT);
  digitalWrite(MODEM_PWKEY, LOW);
  digitalWrite(MODEM_RST, HIGH);
  digitalWrite(MODEM_POWER_ON, HIGH);

  // Initialize SIM800L module
  SerialAT.begin(9600, SERIAL_8N1, MODEM_RX, MODEM_TX);
  delay(3000);

  SerialMon.println("Initializing modem...");
  if (!modem.restart()) {
    SerialMon.println("Modem restart failed!");
    while (true);
  }
  SerialMon.println("Modem initialized.");

  // Signal Quality
  int signalQuality = modem.getSignalQuality();
  SerialMon.print("Signal Quality: ");
  SerialMon.println(signalQuality);

  // Connect to GPRS
  SerialMon.print("Connecting to GPRS...");
  lcd.clear();  // Clear previous content
  lcd.setCursor(0, 0);  // Set cursor to top-left corner
  lcd.print("Searching...");


  if (!modem.gprsConnect(apn, gprsUser, gprsPass)) {
    SerialMon.println("Failed to connect to GPRS!");
    while (true);
  }
  SerialMon.println("GPRS connected.");
}

void loop() {
  // Connect to server
  SerialMon.print("Connecting to ");
  SerialMon.print(server);
  if (!client.connect(server, port)) {
    SerialMon.println("Connection fail!");
     // Connect to GPRS
  lcd.clear();  // Clear previous content
  lcd.print("Connection failed");
  lcd.setCursor(0, 0);  // Set cursor to top-left corner
    delay(10000);
    return;
  }
  SerialMon.println("Connected.");

  // Prepare HTTP GET request with added headers
  client.print("GET " + String(resource) + " HTTP/1.1\r\n");
  client.print("Host: ");
  client.print(server);
  client.print("\r\n");
  client.print("Connection: close\r\n");
  client.print("User-Agent: Mozilla/5.0\r\n");  // Add a User-Agent string
  client.print("Accept: */*\r\n");  // Accept all content types
  client.print("Content-Type: application/json\r\n");  // Adjust as needed
  client.println("\r\n");  // End of headers

  // Read response
  String response = "";
  String statusCode = "";
  unsigned long timeout = millis();
  bool headerEnded = false;

  SerialMon.println("Server response:");

  // Read the response from the server
  while (client.connected() && millis() - timeout < 20000L) {  // Increased timeout
    if (client.available()) {
      char c = client.read();

      // Capture status code (first line of the response)
      if (statusCode.length() == 0 && c == '\n') {
        // Capture status line (e.g., "HTTP/1.1 200 OK")
        statusCode = response;
        response = ""; // Reset for content
      }

      // Check for end of HTTP headers (an empty line signifies end of headers)
      if (c == '\n' && !headerEnded) {
        headerEnded = true;
        continue;  // Skip the empty line after headers
      }

      // Collect the response content after headers
      if (headerEnded) {
        response += c;
      }

      timeout = millis();
    }
  }

  // Display the response content
  if (response.length() == 0) {
    SerialMon.println("No data received from the server.");
  } else {
    // Display status code and body in Serial Monitor
    SerialMon.print("HTTP Status Code: ");
    SerialMon.println(statusCode);
    SerialMon.println("Response:");
    SerialMon.println(response);

    // Parse the JSON response to extract Distance and Passenger_Count
    String distance = "";
    String passengerCount = "";

    // Find the "Distance" and "Passenger_Count" from the response
    int distanceStart = response.indexOf("\"Distance\":\"");
    if (distanceStart != -1) {
      distanceStart += 12;  // Skip the "\"Distance\":\""
      int distanceEnd = response.indexOf("\"", distanceStart);
      distance = response.substring(distanceStart, distanceEnd);
    }

    int passengerCountStart = response.indexOf("\"Passenger_Count\":\"");
    if (passengerCountStart != -1) {
      passengerCountStart += 19;  // Skip the "\"Passenger_Count\":\""
      int passengerCountEnd = response.indexOf("\"", passengerCountStart);
      passengerCount = response.substring(passengerCountStart, passengerCountEnd);
    }

    // Display the data on the LCD
    lcd.clear();  // Clear previous content
    lcd.setCursor(0, 0);  // Set cursor to top-left corner
    lcd.print("Distance: ");
    lcd.print(distance);  // Display the Distance value
    lcd.print("KM"); 
    lcd.setCursor(0, 1);  // Move to the next line
    lcd.print("Passengers: ");
    lcd.print(passengerCount);  // Display the Passenger Count value

    // Add a small delay before the next iteration
    delay(5000);  // 5-second delay
  }

  // Close the connection to the server
 // client.stop();
  //SerialMon.println("Disconnected from server.");
 // delay(10000);  // Wait for 10 seconds before retrying
}

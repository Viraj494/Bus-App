#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>


const char* ssid = "test";
const char* password = "harith1234";


const char* apiKey = "AIzaSyA13MKtYiYORFKZSCMx2PacUHecO2OOKyE";


#define RXD2 4
#define TXD2 0
HardwareSerial gpsSerial(1);
TinyGPSPlus gps;


float destLat = 37.7749;  
float destLng = -122.4194;

void setup() {
    Serial.begin(115200);
    gpsSerial.begin(9600, SERIAL_8N1, RXD2, TXD2);
    Serial.println("Initializing...");

    WiFi.begin(ssid, password);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to Wi-Fi!");
}

void loop() {
    while (gpsSerial.available()) {
        gps.encode(gpsSerial.read());

        if (gps.location.isUpdated()) {
            float currentLat = gps.location.lat();
            float currentLng = gps.location.lng();

            Serial.print("Current Location: ");
            Serial.print(currentLat, 6);
            Serial.print(", ");
            Serial.println(currentLng, 6);

            getDistance(currentLat, currentLng);
            delay(10000); 
        }
    }
}

void getDistance(float originLat, float originLng) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = "https://routes.googleapis.com/directions/v2:computeRoutes";
        http.begin(url);

      
        http.addHeader("Content-Type", "application/json");
        http.addHeader("X-Goog-Api-Key", apiKey);
        http.addHeader("X-Goog-FieldMask", "routes.distanceMeters");

       
        String jsonPayload = "{\"origin\":{\"location\":{\"latLng\":{\"latitude\":" + 
                              String(originLat) + ",\"longitude\":" + 
                              String(originLng) + "}}},\"destination\":{\"location\":{\"latLng\":{\"latitude\":" + 
                              String(destLat) + ",\"longitude\":" + 
                              String(destLng) + "}}},\"travelMode\":\"DRIVE\"}";

        Serial.println("Sending Request...");
        Serial.println(jsonPayload);

        int httpResponseCode = http.POST(jsonPayload);
        if (httpResponseCode == 200) {
            String response = http.getString();
            Serial.println("Response: " + response);

            
            DynamicJsonDocument doc(1024);
            deserializeJson(doc, response);

            if (doc.containsKey("routes")) {
                int distanceMeters = doc["routes"][0]["distanceMeters"];
                Serial.print("Distance: ");
                Serial.print(distanceMeters);
                Serial.println(" meters");
            } else {
                Serial.println("Error: No route found.");
            }
        } else {
            Serial.print("HTTP Error: ");
            Serial.println(httpResponseCode);
        }
        http.end();
    }
}
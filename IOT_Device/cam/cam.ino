#include <Arduino.h>
#include <WiFi.h>
#include <FirebaseClient.h>
#include <esp_camera.h>
#include <SPIFFS.h>

// WiFi Credentials
#define WIFI_SSID "test";
#define WIFI_PASSWORD "harith1234";

// Firebase Storage Bucket
#define STORAGE_BUCKET_ID "espresearch-a73b8.appspot.com"

// OV2640 Camera Pin Config (For AI-Thinker ESP32-CAM)
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM       5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// Firebase No Auth
NoAuth no_auth;
FirebaseApp app;
SSL_CLIENT ssl_client;
using AsyncClient = AsyncClientClass;
AsyncClient aClient(ssl_client);
CloudStorage cstorage;

bool taskComplete = false;

// Function Prototypes
bool initCamera();
bool captureAndSaveImage();
void uploadImage();
void processData(AsyncResult &aResult);

void setup()
{
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println("\nConnected to Wi-Fi!");

    // Initialize SPIFFS
    if (!SPIFFS.begin(true))
    {
        Serial.println("SPIFFS initialization failed!");
        return;
    }

    // Initialize Camera
    if (!initCamera())
    {
        Serial.println("Camera initialization failed!");
        return;
    }

    Serial.println("Firebase Client Version: " + String(FIREBASE_CLIENT_VERSION));
    initializeApp(aClient, app, getAuth(no_auth));
    app.getApp<CloudStorage>(cstorage);

    // Capture Image and Save to SPIFFS
    if (captureAndSaveImage())
    {
        Serial.println("Image captured and saved successfully.");
        uploadImage(); // Upload Image to Firebase
    }
}

void loop()
{
    app.loop();
}

// Initialize Camera
bool initCamera()
{
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;

    if (psramFound())
    {
        config.frame_size = FRAMESIZE_UXGA;
        config.jpeg_quality = 10;
        config.fb_count = 2;
    }
    else
    {
        config.frame_size = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
    }

    esp_err_t err = esp_camera_init(&config);
    return err == ESP_OK;
}

// Capture and Save Image to SPIFFS
bool captureAndSaveImage()
{
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb)
    {
        Serial.println("Failed to capture image!");
        return false;
    }

    File file = SPIFFS.open("/captured.jpg", FILE_WRITE);
    if (!file)
    {
        Serial.println("Failed to open file for writing!");
        esp_camera_fb_return(fb);
        return false;
    }

    file.write(fb->buf, fb->len);
    file.close();
    esp_camera_fb_return(fb);
    Serial.println("Image saved to SPIFFS as captured.jpg");
    return true;
}

// Upload Image to Firebase
void uploadImage()
{
    if (taskComplete)
        return;

unsigned long currentTime = millis();
    taskComplete = true;

    GoogleCloudStorage::UploadOptions options;
    options.mime = "image/jpeg";
    options.uploadType = GoogleCloudStorage::upload_type_simple;

    FileConfig image_file("/captured.jpg", file_operation_callback);
    Serial.println("Uploading image to Firebase...");

    cstorage.upload(aClient, GoogleCloudStorage::Parent(STORAGE_BUCKET_ID, "captured"+currentTime+".jpeg"), getFile(image_file), options, processData, "⬆️ UploadTask");
}

// Process Upload Result
void processData(AsyncResult &aResult)
{
    if (!aResult.isResult())
        return;

    if (aResult.isError())
    {
        Serial.printf("Upload Error: %s (Code: %d)\n", aResult.error().message().c_str(), aResult.error().code());
    }

    if (aResult.uploadProgress())
    {
        Serial.printf("Uploaded: %d%% (%d of %d bytes)\n", aResult.uploadInfo().progress, aResult.uploadInfo().uploaded, aResult.uploadInfo().total);
        if (aResult.uploadInfo().total == aResult.uploadInfo().uploaded)
        {
            Serial.println("Upload complete! ");
            Serial.println("Download URL: " + aResult.uploadInfo().downloadUrl);
        }
    }
}
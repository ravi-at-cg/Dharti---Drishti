# Dharti---Drishti

[PPT](https://docs.google.com/presentation/d/1DIrdumShqwMI7SoRJPezvERtIQ_cikdc-K_2yvy8ow4/edit?usp=sharing)

## Architecture Diagram

```mermaid
graph TB
    subgraph Mobile["Mobile App (Android)"]
        Camera["Camera Module<br/>CameraX + TFLite"]
        CardDetect["Card Detection"]
        GPS["GPS Capture"]
        Upload["Upload Manager"]
        Results["Results Display"]
    end

    subgraph Gateway["API Gateway"]
        Auth["Authentication"]
        RateLimit["Rate Limiting"]
    end

    subgraph Backend["Backend Services"]
        ImageProc["Image Processing<br/>OpenCV"]
        ColorCalib["Color Calibration"]
        TextureAnalysis["Texture Analysis"]
        
        subgraph AI["AI Models"]
            TextureModel["Texture Classifier<br/>ResNet-50"]
            CarbonModel["Organic Carbon<br/>XGBoost"]
            SalinityModel["Salinity Detector<br/>CNN"]
        end
        
        GPSIntel["GPS Intelligence"]
        WeatherAPI["Weather Service<br/>OpenWeatherMap"]
        ActionEngine["Action Engine"]
        Translation["Translation Service"]
    end

    subgraph Data["Data Layer"]
        DB[(PostgreSQL<br/>PostGIS)]
        Cache[(Redis Cache)]
        Storage[("Object Storage<br/>S3")]
    end

    Camera --> CardDetect
    CardDetect --> GPS
    GPS --> Upload
    Upload -->|HTTPS| Auth
    Auth --> RateLimit
    
    RateLimit --> ImageProc
    ImageProc --> ColorCalib
    ColorCalib --> TextureAnalysis
    
    TextureAnalysis --> TextureModel
    TextureAnalysis --> CarbonModel
    TextureAnalysis --> SalinityModel
    
    TextureModel --> ActionEngine
    CarbonModel --> ActionEngine
    SalinityModel --> ActionEngine
    
    GPS --> GPSIntel
    GPSIntel --> WeatherAPI
    WeatherAPI --> Cache
    GPSIntel --> ActionEngine
    
    ActionEngine --> Translation
    Translation --> Results
    
    ImageProc --> Storage
    ActionEngine --> DB
    GPSIntel --> DB
    
    DB --> Results

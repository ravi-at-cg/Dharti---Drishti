# Dharti---Drishti

[PPT](https://docs.google.com/presentation/d/1DIrdumShqwMI7SoRJPezvERtIQ_cikdc-K_2yvy8ow4/edit?usp=sharing)

## Current Architecture Diagram

```mermaid
graph TB
    subgraph Client["🌐 Frontend Layer"]
        UI["Web Interface<br/>(HTML/CSS/JS)"]
        Camera["📸 Image Capture"]
        GPS["📍 GPS Detection<br/>(Browser Geolocation API)"]
        Display["📊 Results Display"]
    end

    subgraph API["🔌 API Layer"]
        Flask["Flask REST API<br/>(Python)"]
        CORS["CORS Middleware"]
        Routes["API Routes<br/>/api/analyze<br/>/api/health"]
    end

    subgraph Processing["🧠 AI Processing Pipeline"]
        Orchestrator["AI Layer Service<br/>(process_image)"]
        
        subgraph SoilAnalysis["Soil Analysis"]
            SoilType["Soil Type Classifier<br/>(Roboflow API)"]
            Carbon["Carbon Content Analyzer<br/>(Google Gemini 3 Flash)"]
        end
        
        subgraph EnvIntel["Environmental Intelligence"]
            EnvParams["Environment Parameters Builder"]
            Terrain["Terrain Analysis<br/>(Elevation, Slope, Aspect)"]
            Climate["Climate Data<br/>(NASA POWER API)"]
            Hydrology["Waterbody Detection<br/>(Overpass API)"]
        end
        
        ActionEngine["Action Engine<br/>(Groq LLM - GPT-OSS-120B)"]
    end

    subgraph Storage["💾 Storage Layer"]
        FileStorage["Local File Storage<br/>(storage_service/soil_images)"]
        OutputStorage["Model Outputs<br/>(storage_service/model_outputs)"]
    end

    subgraph External["🌍 External Services"]
        Roboflow["Roboflow<br/>(Soil Classification)"]
        Gemini["Google Gemini API<br/>(Carbon Analysis)"]
        NASA["NASA POWER API<br/>(Climate Data)"]
        Elevation["Open Elevation API<br/>(Terrain Data)"]
        OSM["Overpass API<br/>(OpenStreetMap Data)"]
        Groq["Groq API<br/>(LLM Inference)"]
    end

    %% User Flow
    UI -->|Upload Image + GPS| Camera
    Camera -->|Capture| GPS
    GPS -->|Form Data| Flask
    
    %% API Processing
    Flask -->|Validate & Route| CORS
    CORS -->|Save Image| FileStorage
    Flask -->|Process Request| Orchestrator
    
    %% AI Pipeline Flow
    Orchestrator -->|1. Image Path| SoilType
    Orchestrator -->|2. Image Path| Carbon
    Orchestrator -->|3. GPS Coords| EnvParams
    
    %% Soil Analysis
    SoilType -->|API Call| Roboflow
    Roboflow -->|Soil Category + Confidence| SoilType
    Carbon -->|API Call| Gemini
    Gemini -->|Carbon Content Level| Carbon
    
    %% Environmental Intelligence
    EnvParams -->|Fetch Terrain| Terrain
    EnvParams -->|Fetch Climate| Climate
    EnvParams -->|Detect Water| Hydrology
    
    Terrain -->|API Call| Elevation
    Climate -->|API Call| NASA
    Hydrology -->|API Call| OSM
    
    Elevation -->|Elevation, Slope, Aspect| Terrain
    NASA -->|Temp, Humidity, Rainfall| Climate
    OSM -->|Waterbody Distance & Type| Hydrology
    
    Terrain -->|Terrain Profile| EnvParams
    Climate -->|Climate Profile| EnvParams
    Hydrology -->|Hydrology Profile| EnvParams
    
    %% Action Engine
    SoilType -->|Soil Type| ActionEngine
    Carbon -->|Carbon Content| ActionEngine
    EnvParams -->|Environment Parameters| ActionEngine
    
    ActionEngine -->|API Call| Groq
    Groq -->|Crop Recommendations JSON| ActionEngine
    ActionEngine -->|Save Output| OutputStorage
    
    %% Response Flow
    ActionEngine -->|JSON Response| Flask
    Flask -->|HTTP Response| UI
    UI -->|Parse & Display| Display
    
    %% Styling
    classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef api fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef ai fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef storage fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class UI,Camera,GPS,Display frontend
    class Flask,CORS,Routes api
    class Orchestrator,SoilType,Carbon,EnvParams,Terrain,Climate,Hydrology,ActionEngine ai
    class FileStorage,OutputStorage storage
    class Roboflow,Gemini,NASA,Elevation,OSM,Groq external
```

## Detailed Component Architecture

```mermaid
graph LR
    subgraph Frontend["Frontend Components"]
        Index["index.html<br/>Main Upload Form"]
        Results["results.html<br/>Results Display"]
        Script["script.js<br/>Form Handler"]
        ResultsJS["results.js<br/>Results Renderer"]
    end

    subgraph Backend["Backend Structure"]
        App["backend/app.py<br/>Flask Server"]
        AILayer["ai_services/ai_layer_service.py<br/>Orchestrator"]
    end

    subgraph AIServices["AI Services"]
        ST["soil_type/soil_type.py<br/>Roboflow Integration"]
        CC["carbon_content/carbon_content.py<br/>Gemini Integration"]
        EP["envrionment_parameters/env_params.py<br/>NASA + OSM + Elevation"]
        AE["action_engine/action_engine.py<br/>Groq LLM Integration"]
    end

    Index -->|User Input| Script
    Script -->|POST /api/analyze| App
    App -->|process_image| AILayer
    AILayer -->|get_soil_category| ST
    AILayer -->|get_carbon_content| CC
    AILayer -->|build_land_profile| EP
    AILayer -->|get_actions| AE
    AE -->|JSON Response| App
    App -->|HTTP Response| Script
    Script -->|Navigate| Results
    Results -->|Load Data| ResultsJS

    classDef fe fill:#e3f2fd,stroke:#1976d2
    classDef be fill:#fff3e0,stroke:#f57c00
    classDef ai fill:#f3e5f5,stroke:#7b1fa2
    
    class Index,Results,Script,ResultsJS fe
    class App,AILayer be
    class ST,CC,EP,AE ai
```

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Flask API
    participant AI Orchestrator
    participant Roboflow
    participant Gemini
    participant NASA/OSM
    participant Groq LLM
    participant Storage

    User->>Frontend: Upload soil image + GPS
    Frontend->>Frontend: Capture GPS coordinates
    Frontend->>Flask API: POST /api/analyze (image, lat, lon, top_crops)
    Flask API->>Storage: Save uploaded image
    Flask API->>AI Orchestrator: process_image(path, lat, lon, top_crops)
    
    par Parallel Analysis
        AI Orchestrator->>Roboflow: get_soil_category(image_path)
        Roboflow-->>AI Orchestrator: soil_type + confidence
    and
        AI Orchestrator->>Gemini: get_carbon_content(image_path)
        Gemini-->>AI Orchestrator: carbon_content_level
    and
        AI Orchestrator->>NASA/OSM: build_land_profile(lat, lon)
        NASA/OSM-->>AI Orchestrator: terrain + climate + hydrology
    end
    
    AI Orchestrator->>Groq LLM: get_actions(soil_type, top_crops, carbon, env_params)
    Groq LLM-->>AI Orchestrator: crop_recommendations_json
    AI Orchestrator->>Storage: Save model output
    AI Orchestrator-->>Flask API: JSON response
    Flask API-->>Frontend: HTTP 200 + analysis data
    Frontend->>Frontend: Store in sessionStorage
    Frontend->>User: Display success + "View Results" button
    User->>Frontend: Click "View Results"
    Frontend->>Frontend: Navigate to results.html
    Frontend->>User: Render detailed recommendations
```

## Key Features & Capabilities

- **Instant Soil Analysis**: Upload soil image and get results in ~30 seconds
- **Multi-Model AI Pipeline**: Combines computer vision, LLM, and geospatial intelligence
- **GPS-Enhanced Recommendations**: Location-aware crop suggestions based on climate and terrain
- **Comprehensive Environmental Profiling**: Elevation, slope, aspect, rainfall, temperature, waterbody proximity
- **Actionable Insights**: Fertilizer recommendations, irrigation methods, month-by-month plans
- **Demo Mode**: Test with pre-loaded sample images
- **Responsive UI**: Works on desktop and mobile browsers

## System Components

### Frontend Layer
- **index.html**: Main upload interface with demo mode support
- **results.html**: Comprehensive results display page
- **script.js**: Handles form submission, GPS capture, and API communication
- **results.js**: Renders detailed crop recommendations and analysis

### API Layer
- **Flask REST API**: Handles HTTP requests and orchestrates processing
- **Endpoints**:
  - `POST /api/analyze`: Main analysis endpoint
  - `GET /api/health`: Health check endpoint
  - `GET /storage_service/soil_images/<filename>`: Serve demo images

### AI Processing Pipeline
1. **Soil Type Classification** (Roboflow): Identifies soil texture and type
2. **Carbon Content Analysis** (Gemini): Estimates organic carbon levels from image
3. **Environmental Intelligence** (NASA/OSM/Elevation APIs):
   - Terrain: Elevation, slope, aspect direction
   - Climate: Temperature, humidity, rainfall patterns
   - Hydrology: Nearby waterbodies and distance
4. **Action Engine** (Groq LLM): Generates actionable farming recommendations

### Storage Layer
- **soil_images/**: Stores uploaded and demo soil images
- **model_outputs/**: Saves timestamped LLM responses for audit trail

## API Integration Details

| Service | Purpose | Data Provided |
|---------|---------|---------------|
| **Roboflow** | Soil classification | Soil type (Alluvial, Clay, Sandy, etc.) + confidence score |
| **Google Gemini** | Carbon analysis | Organic carbon content level from visual analysis |
| **NASA POWER** | Climate data | Temperature, humidity, rainfall, dew point (annual data) |
| **Open Elevation** | Terrain analysis | Elevation, slope degree/percent, aspect direction |
| **Overpass (OSM)** | Waterbody detection | Distance to nearest water source, waterbody type |
| **Groq** | Recommendation engine | Structured JSON with crop suggestions, fertilizers, schedules |

## Processing Flow

1. User uploads soil image with GPS coordinates
2. Flask API saves image and initiates processing
3. Parallel AI analysis:
   - Roboflow classifies soil type
   - Gemini analyzes carbon content
   - NASA/OSM/Elevation APIs build environmental profile
4. Groq LLM synthesizes all data into actionable recommendations
5. Results stored and returned to frontend
6. Frontend displays comprehensive farming guidance

## Output Structure

The system generates detailed recommendations including:
- **Summary**: Overview of soil condition and suitability
- **Land Preparation**: Pre-planting soil amendments
- **Crop Recommendations**: Top N crops with:
  - Expected harvest and growing days
  - Planting and harvest times
  - Fertilizer schedule (before planting + during growth)
  - Watering guide with critical stages
  - Month-by-month task plan
  - Common problems and solutions
  - Harvest tips
- **General Tips**: Soil protection, water saving, cost optimization
- **Rotation Plan**: Multi-year crop rotation strategy

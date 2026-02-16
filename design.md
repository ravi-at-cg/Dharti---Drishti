# Dharti-Drishti Design Document

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌─────────────────┐
│  Mobile App     │
│  (Android)      │
│  - Camera UI    │
│  - Card Detect  │
│  - GPS Capture  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  API Gateway    │
│  - Auth         │
│  - Rate Limit   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ Image  │ │ Soil │ │Weather │ │Action  │
│Process │ │ AI   │ │Service │ │Engine  │
└────────┘ └──────┘ └────────┘ └────────┘
    │         │          │          │
    └─────────┴──────────┴──────────┘
                   ▼
            ┌──────────────┐
            │   Database   │
            │ - User Data  │
            │ - Analysis   │
            │ - History    │
            └──────────────┘
```

### 1.2 Technology Stack

**Mobile App:**
- Platform: Android (Kotlin/Java)
- Camera: CameraX API
- ML: TensorFlow Lite for on-device card detection
- Location: Google Play Services Location API
- UI: Material Design 3

**Backend:**
- API: Node.js/Express or Python/FastAPI
- AI/ML: Python with PyTorch/TensorFlow
- Image Processing: OpenCV, scikit-image
- Database: PostgreSQL + PostGIS for geospatial data
- Cache: Redis for weather data
- Storage: S3-compatible object storage for images

**External Services:**
- Weather API: OpenWeatherMap or IMD API
- Maps: Google Maps API or OpenStreetMap
- Translation: Google Cloud Translation API

## 2. Component Design

### 2.1 Mobile App Components

#### 2.1.1 Camera Module
```
CameraController
├── CardDetector (TFLite model)
│   ├── detectCard()
│   ├── validateCardPosition()
│   └── autoFocus()
├── ImageCapture
│   ├── captureImage()
│   ├── validateQuality()
│   └── compressImage()
└── GPSCapture
    ├── getCurrentLocation()
    └── getLocationAccuracy()
```

**Card Detection Algorithm:**
1. Real-time frame analysis using TFLite model
2. Detect rectangular shape with specific aspect ratio
3. Identify color calibration patches
4. Calculate card orientation and distance
5. Trigger auto-focus when optimal position detected

#### 2.1.2 Upload Module
```
UploadManager
├── QueueManager (offline support)
├── ImageUploader
│   ├── uploadWithRetry()
│   └── trackProgress()
└── MetadataCollector
    ├── collectGPS()
    ├── collectTimestamp()
    └── collectDeviceInfo()
```

#### 2.1.3 Results Display Module
```
ResultsView
├── RecommendationCard
├── SoilMetricsView
├── ActionListView
├── ShareButton
└── HistoryButton
```

### 2.2 Backend Components

#### 2.2.1 Image Processing Pipeline
```python
class ImageProcessor:
    def process(self, image, metadata):
        # 1. Calibration
        calibrated_image = self.calibrate_colors(image)
        
        # 2. Segmentation
        soil_region = self.segment_soil(calibrated_image)
        
        # 3. Feature Extraction
        features = {
            'texture': self.extract_texture(soil_region),
            'color': self.extract_color(soil_region),
            'patterns': self.extract_patterns(soil_region)
        }
        
        return features
```

**Color Calibration:**
- Detect calibration card color patches
- Calculate color transformation matrix
- Apply correction to entire image
- Normalize for lighting conditions

**Texture Analysis:**
- Extract GLCM (Gray-Level Co-occurrence Matrix) features
- Calculate entropy, contrast, homogeneity
- Use CNN for texture classification
- Output: Sandy/Clay/Loamy with confidence score

#### 2.2.2 Soil Analysis AI Models

**Model 1: Texture Classifier**
```
Input: Calibrated soil image (224x224)
Architecture: ResNet-50 or EfficientNet-B0
Output: [Sandy, Clay, Loamy] probabilities
Training: Transfer learning on labeled soil dataset
```

**Model 2: Organic Carbon Estimator**
```
Input: Color features + texture features
Architecture: Random Forest or XGBoost
Output: Organic carbon level (High/Medium/Low)
Features:
  - Mean RGB values
  - Color histogram
  - Texture metrics
  - Regional baseline data
```

**Model 3: Salinity Detector**
```
Input: Soil image patches
Architecture: CNN + LSTM for pattern detection
Output: Salinity indicators (salt crusts, biological crusts)
Detection: Object detection for white salt deposits
```

#### 2.2.3 GPS Intelligence Module
```python
class GPSIntelligence:
    def enrich_analysis(self, gps_coords, soil_features):
        # Fetch contextual data
        weather = self.get_weather_data(gps_coords)
        historical = self.get_regional_data(gps_coords)
        soil_type_regional = self.get_soil_baseline(gps_coords)
        
        # Refine analysis
        adjusted_features = self.adjust_for_region(
            soil_features, 
            historical, 
            soil_type_regional
        )
        
        return {
            'features': adjusted_features,
            'context': {
                'weather': weather,
                'regional_patterns': historical
            }
        }
```

**Data Sources:**
- Real-time weather: Temperature, rainfall, humidity
- Historical data: Crop patterns, soil types in region
- Seasonal data: Monsoon patterns, drought history
- Agricultural data: Common crops, farming practices

#### 2.2.4 Action Engine
```python
class ActionEngine:
    def generate_recommendations(self, analysis_result, context):
        recommendations = []
        
        # Fertilizer recommendations
        if analysis_result['organic_carbon'] == 'Low':
            recommendations.append(
                self.fertilizer_action(analysis_result, context)
            )
        
        # Crop suitability
        suitable_crops = self.match_crops(
            analysis_result['texture'],
            context['weather'],
            context['regional_patterns']
        )
        recommendations.append(
            self.crop_action(suitable_crops)
        )
        
        # Soil improvement
        if analysis_result['salinity'] == 'High':
            recommendations.append(
                self.salinity_action(analysis_result)
            )
        
        # Irrigation
        irrigation = self.irrigation_recommendation(
            analysis_result['texture'],
            context['weather']
        )
        recommendations.append(irrigation)
        
        return self.prioritize(recommendations)
```

**Action Templates:**
```json
{
  "fertilizer": {
    "sandy_low_oc": "Apply 2 bags compost per bigha. Mix well before planting.",
    "clay_medium_oc": "Use balanced NPK 10:26:26. Apply 1 bag per bigha."
  },
  "crops": {
    "sandy_low_water": ["Bajra", "Moong", "Groundnut"],
    "clay_high_water": ["Rice", "Wheat", "Sugarcane"]
  },
  "irrigation": {
    "sandy": "Use drip irrigation. Water daily in small amounts.",
    "clay": "Flood irrigation suitable. Water every 3-4 days."
  },
  "amendments": {
    "high_salinity": "Apply gypsum 5 kg per bigha. Ensure good drainage."
  }
}
```

#### 2.2.5 Translation Module
```python
class TranslationService:
    def translate_recommendations(self, actions, target_language):
        # Use pre-translated templates for common actions
        if self.has_template(actions, target_language):
            return self.get_template(actions, target_language)
        
        # Fallback to API translation
        return self.api_translate(actions, target_language)
```

**Supported Languages:**
- Hindi, Tamil, Telugu, Marathi, Bengali
- Gujarati, Kannada, Malayalam, Punjabi
- Pre-translated templates for common recommendations
- Voice synthesis for audio output

## 3. Data Models

### 3.1 Database Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE,
    preferred_language VARCHAR(10),
    created_at TIMESTAMP
);

-- Soil Analysis
CREATE TABLE soil_analyses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    image_url TEXT,
    gps_location GEOGRAPHY(POINT),
    captured_at TIMESTAMP,
    
    -- Analysis results
    texture VARCHAR(20),
    texture_confidence FLOAT,
    organic_carbon VARCHAR(10),
    salinity_level VARCHAR(10),
    
    -- Context
    weather_data JSONB,
    regional_data JSONB,
    
    -- Recommendations
    recommendations JSONB,
    
    created_at TIMESTAMP
);

-- Recommendations History
CREATE TABLE recommendations (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES soil_analyses(id),
    category VARCHAR(50),
    action_text TEXT,
    language VARCHAR(10),
    priority INTEGER
);

-- Feedback
CREATE TABLE feedback (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES soil_analyses(id),
    rating INTEGER,
    implemented BOOLEAN,
    yield_improvement FLOAT,
    comments TEXT,
    created_at TIMESTAMP
);
```

## 4. API Design

### 4.1 Endpoints

```
POST /api/v1/analyze
Request:
  - image: multipart/form-data
  - gps_lat: float
  - gps_lon: float
  - language: string
  - timestamp: ISO8601

Response:
{
  "analysis_id": "uuid",
  "soil_type": "Loamy",
  "organic_carbon": "Medium",
  "salinity": "Low",
  "recommendations": [
    {
      "category": "fertilizer",
      "priority": 1,
      "action": "Apply 1.5 bags compost per bigha",
      "reason": "Organic carbon is medium, boost for better yield"
    }
  ],
  "suitable_crops": ["Wheat", "Chickpea", "Mustard"],
  "processed_at": "2026-02-16T10:30:00Z"
}

GET /api/v1/history
GET /api/v1/analysis/{id}
POST /api/v1/feedback
```

## 5. Calibration Card Design

### 5.1 Physical Specifications
- Size: 85.6mm × 53.98mm (credit card size)
- Material: Waterproof PVC or laminated cardstock
- Thickness: 0.76mm

### 5.2 Visual Design
```
┌─────────────────────────────────┐
│ ■ ■ ■ ■  [Color Patches]        │
│                                  │
│     DHARTI-DRISHTI              │
│                                  │
│ [QR Code]  [Scale Markers]      │
└─────────────────────────────────┘
```

**Color Patches:**
- 4-6 standardized color patches
- Colors: White, Gray, Black, Brown, Red-Brown
- Used for color calibration and white balance

**QR Code:**
- Links to app download or instructions
- Contains card version for calibration updates

## 6. Deployment Architecture

### 6.1 Cloud Infrastructure
```
Load Balancer
    ├── API Servers (Auto-scaling)
    ├── ML Inference Servers (GPU)
    └── Background Workers (Image processing queue)

Storage
    ├── Object Storage (Images)
    ├── PostgreSQL (Primary DB)
    └── Redis (Cache)

Monitoring
    ├── Application logs
    ├── Performance metrics
    └── Error tracking
```

### 6.2 Scalability Strategy
- Horizontal scaling for API servers
- GPU instances for ML inference
- CDN for static assets and processed images
- Database read replicas for analytics
- Queue-based processing for async tasks

## 7. Security Considerations

- HTTPS for all communications
- JWT-based authentication
- Image encryption in transit
- GPS data anonymization for analytics
- Rate limiting to prevent abuse
- Input validation and sanitization
- Regular security audits

## 8. Future Enhancements

- Offline ML inference on device
- Time-series analysis for soil health tracking
- Community features for farmer knowledge sharing
- Integration with government schemes
- Pest and disease detection from crop photos
- Market price integration for crop recommendations

## Project: Dharti---Drishti

### 1. System Overview
High-level description of the system architecture and design philosophy.

### 2. Architecture

#### 2.1 System Architecture
- Architecture pattern (e.g., MVC, microservices, layered)
- Component diagram
- System boundaries

#### 2.2 Technology Stack
- Frontend technologies
- Backend technologies
- Database technologies
- Infrastructure and deployment

### 3. Component Design

#### 3.1 Frontend Components
- Component hierarchy
- State management approach
- Routing structure

#### 3.2 Backend Components
- API design
- Service layer
- Data access layer

#### 3.3 Database Design
- Data models
- Relationships
- Indexing strategy

### 4. API Design

#### 4.1 Endpoints
```
GET /api/resource
POST /api/resource
PUT /api/resource/:id
DELETE /api/resource/:id
```

#### 4.2 Request/Response Formats
- Request schemas
- Response schemas
- Error formats

### 5. Data Flow
- User interaction flows
- Data processing pipelines
- Integration flows

### 6. Security Design
- Authentication mechanism
- Authorization strategy
- Data encryption
- Security best practices

### 7. Performance Considerations
- Caching strategy
- Optimization techniques
- Load balancing approach

### 8. Error Handling
- Error types
- Error responses
- Logging strategy

### 9. Testing Strategy
- Unit testing approach
- Integration testing approach
- End-to-end testing approach

### 10. Deployment Architecture
- Environment setup
- CI/CD pipeline
- Monitoring and logging

### 11. Design Decisions
- Key architectural decisions
- Trade-offs considered
- Rationale for choices

### 12. Future Considerations
- Scalability plans
- Feature extensibility
- Technical debt items

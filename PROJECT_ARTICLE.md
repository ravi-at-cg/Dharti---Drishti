# Dharti Drishti: An AI-Powered Precision Agriculture Platform

## Overview

Dharti Drishti (which translates to "Earth Vision" in Hindi) is an intelligent agricultural advisory system that combines computer vision, geospatial analysis, and large language models to provide farmers with personalized, actionable crop recommendations. The platform analyzes soil images uploaded by users, combines this with environmental data from their location, and generates comprehensive farming guidance tailored to their specific land conditions.

## The Problem It Solves

Traditional farming often relies on generalized advice that doesn't account for the unique characteristics of individual plots of land. Farmers need to understand:
- What crops will thrive on their specific soil type
- How local climate patterns affect crop selection
- What amendments their soil needs
- When to plant, water, and harvest
- How to manage their land sustainably

Dharti Drishti democratizes access to precision agriculture by making sophisticated soil and environmental analysis accessible through a simple web interface.

## Architecture & Technology Stack

### Frontend Layer
The application features a clean, responsive web interface built with vanilla JavaScript, HTML, and CSS. The user experience is designed to be intuitive:

- **Main Interface** (`index.html`): Users can either upload their own soil images or use demo images for testing
- **Geolocation Integration**: Automatically detects the user's GPS coordinates to gather location-specific environmental data
- **Results Dashboard** (`results.html`): Displays comprehensive analysis results in an organized, visually appealing format

The frontend communicates with the backend through a REST API, with automatic environment detection (localhost vs production).

### Backend Layer
Built on Flask with CORS support, the backend (`backend/app.py`) serves as the orchestration layer:

- Handles image uploads and storage
- Manages demo image serving
- Coordinates the AI analysis pipeline
- Serves static frontend files
- Provides health check endpoints

### AI Services Pipeline

The core intelligence of Dharti Drishti lies in its multi-stage AI analysis pipeline (`ai_services/ai_layer_service.py`), which processes data through four specialized services:

#### 1. Soil Type Classification (`soil_type/soil_type.py`)

This service uses Roboflow's computer vision API to classify soil types from images. The system:
- Sends the soil image to a trained Roboflow model (`soil-type-ladmq/6`)
- Receives predictions for multiple soil categories with confidence scores
- Selects the category with the highest confidence
- Returns both the soil type and confidence level

The classification can identify various soil types including alluvial, clay, sandy, loamy, and other agricultural soil categories.

#### 2. Carbon Content Analysis (`carbon_content/carbon_content.py`)

Using Google's Gemini 3 Flash vision model, this service estimates the organic carbon content of the soil:
- Analyzes soil color and texture from the image
- Acts as a "pedologist" (soil scientist) to assess organic matter
- Returns a numerical score between 0.0 and 1.0
- Categories range from highly oxidized red soils (0.00-0.02) to rich, dark humus soils (0.07-0.15+)

The carbon content is crucial for understanding soil fertility and determining what amendments are needed.

#### 3. Environmental Parameters (`envrionment_parameters/env_params.py`)

This is perhaps the most sophisticated component, gathering comprehensive environmental data from multiple sources:

**NASA POWER API Integration:**
- Fetches historical climate data for the location
- Collects temperature (average, max, min), humidity, dew point, and precipitation data
- Analyzes rainfall patterns to determine if the area is monsoon-dominant or has distributed rainfall
- Calculates weekly temperature averages
- Identifies peak rainfall months and rainy day counts

**Terrain Analysis:**
- Uses Open Elevation API to determine land elevation
- Calculates slope (in degrees and percentage) using elevation gradients
- Determines aspect (the direction the slope faces) and converts it to cardinal directions (N, NE, E, etc.)
- This information is critical for water drainage, sun exposure, and erosion risk

**Hydrology Assessment:**
- Queries OpenStreetMap data via Overpass API
- Searches for nearby water bodies (rivers, lakes, streams) within a 1km radius
- Calculates distance to the nearest water source
- Identifies the type of water body
- This helps determine irrigation needs and water availability

The service combines all this data into a comprehensive land profile that includes terrain characteristics, hydrology, and detailed climate information.

#### 4. Action Engine (`action_engine/action_engine.py`)

The action engine is the synthesis layer that brings everything together:
- Takes soil type, carbon content, and environmental parameters as inputs
- Uses Groq's API with the GPT-OSS-120B model
- Employs a carefully crafted prompt that instructs the AI to act as a practical farming advisor
- Generates comprehensive, structured recommendations in JSON format
- Stores each analysis output with timestamps for record-keeping

The prompt engineering is particularly sophisticated, instructing the AI to:
- Use simple, farmer-friendly language
- Provide specific product names (fertilizers, amendments)
- Include exact quantities and timing
- Create month-by-month action plans
- Address common problems and solutions
- Consider cost-effectiveness and practicality

## Data Flow

1. **User Input**: User uploads soil image and provides location (or uses demo mode)
2. **Image Analysis**: Soil type classification (Roboflow) and carbon content analysis (Gemini) run in parallel
3. **Environmental Data**: System fetches climate, terrain, and hydrology data based on GPS coordinates
4. **Synthesis**: All data feeds into the action engine (Groq LLM)
5. **Output Generation**: AI generates structured JSON with comprehensive farming recommendations
6. **Display**: Frontend renders the recommendations in an organized, user-friendly format

## Output Structure

The system generates incredibly detailed recommendations including:

### Summary
A concise overview of what will grow well on the analyzed land.

### General Land Preparation
Specific products and amounts needed to prepare the soil before planting any crop (lime for acidity, gypsum for drainage, organic matter, etc.).

### Crop-Specific Recommendations
For each recommended crop (user can specify how many top crops to receive):

- **Why it's suitable**: Explanation based on soil type, climate, and terrain
- **Expected harvest**: Realistic yield estimates
- **Planting and harvest timing**: Specific months
- **Growing duration**: Total days from seed to harvest

**What to Add:**
- Before planting: Specific fertilizers (NPK ratios, urea, DAP) with quantities
- During growing: Timed applications with reasons

**Watering Guide:**
- Best irrigation method (drip, sprinkler, flood)
- Watering schedule
- Critical stages when water is most needed
- Total seasonal water requirements

**Month-by-Month Plan:**
- Detailed actions for all 12 months
- Planting, fertilizing, watering, and harvesting schedules

**Common Problems:**
- Pest identification and solutions
- Disease prevention
- Weather-related challenges

**Harvest Tips:**
- Ripeness indicators
- Harvesting techniques
- Storage recommendations

### General Tips
- Soil protection strategies (erosion prevention)
- Water conservation techniques
- Cost-saving measures

### Crop Rotation Plan
A 3-year rotation strategy to maintain soil health and prevent nutrient depletion.

## Deployment & Infrastructure

The application is containerized using Docker with the following setup:

- **Docker Compose**: Orchestrates the application stack
- **Environment Variables**: Manages API keys for Roboflow, Gemini, and Groq
- **Storage Service**: Organized directory structure for soil images and model outputs
- **EC2 Deployment**: Includes comprehensive deployment scripts and documentation for AWS EC2

The project includes multiple deployment guides:
- `DEPLOYMENT.md`: General deployment instructions
- `EC2_DEPLOYMENT_STEPS.md`: Step-by-step EC2 setup
- `EC2_DEPLOYMENT_GITHUB.md`: GitHub Actions integration
- `deploy-to-ec2.sh`: Automated deployment script
- `fix-and-restart.sh`: Quick restart script for updates

## Key Features

### Demo Mode
The application includes a demo mode with pre-loaded soil images, allowing users to test the system without uploading their own images. This is particularly useful for:
- Testing the application
- Understanding the output format
- Demonstrations and presentations

### Geolocation
Automatic GPS detection ensures that environmental data is specific to the user's actual location, making recommendations highly relevant.

### Multi-Language Support
The project includes translation capabilities (`ai_services/translation/translation_call.py`), suggesting plans for internationalization to serve farmers in different regions.

### Responsive Design
The frontend is designed to work across devices, from desktop computers to mobile phones, making it accessible to farmers in the field.

## Technical Considerations

### API Dependencies
The system relies on several external APIs:
- **Roboflow**: Soil classification (requires API key)
- **Google Gemini**: Carbon content analysis (requires API key)
- **Groq**: Recommendation generation (requires API key)
- **NASA POWER**: Climate data (public API)
- **Open Elevation**: Terrain data (public API)
- **Overpass/OpenStreetMap**: Hydrology data (public API)

### Error Handling
The application includes robust error handling:
- Graceful degradation when APIs are unavailable
- Validation of user inputs
- Fallback mechanisms for location detection
- JSON parsing error handling

### Performance Optimization
- Parallel execution of independent AI services (soil type and carbon content)
- Caching of environmental data could be implemented for repeated queries in the same area
- Efficient image handling and storage

### Data Privacy
- Images are stored locally on the server
- GPS coordinates are used only for environmental data fetching
- No personal information is collected or stored

## Use Cases

1. **Small-Scale Farmers**: Get professional-grade soil analysis without expensive lab tests
2. **Agricultural Extension Services**: Provide data-driven recommendations to farming communities
3. **Agricultural Education**: Teach students about soil science and precision agriculture
4. **Land Assessment**: Evaluate land before purchase or lease
5. **Sustainable Farming**: Plan crop rotations and soil management for long-term sustainability

## Future Enhancement Possibilities

Based on the codebase structure, potential enhancements could include:

1. **Historical Tracking**: Store and compare analyses over time to track soil health improvements
2. **Market Integration**: Add crop price data to help farmers make economically optimal decisions
3. **Community Features**: Allow farmers to share experiences and results
4. **Mobile App**: Native mobile applications for better field usability
5. **Offline Mode**: Cache recommendations for areas with poor connectivity
6. **Multi-Language Interface**: Full localization for regional languages
7. **Pest and Disease Detection**: Expand computer vision to identify crop health issues
8. **Weather Forecasting Integration**: Real-time weather alerts and adjusted recommendations
9. **Marketplace Connection**: Link farmers with suppliers for recommended products
10. **Government Scheme Integration**: Inform farmers about applicable subsidies and programs

## Conclusion

Dharti Drishti represents a sophisticated application of modern AI technologies to solve real-world agricultural challenges. By combining computer vision, geospatial analysis, and large language models, it transforms complex scientific data into actionable farming advice. The system's strength lies not just in its technical sophistication, but in its focus on practical, farmer-friendly recommendations that can be immediately implemented.

The modular architecture makes it easy to enhance individual components, swap AI models, or add new data sources. The comprehensive prompt engineering ensures that outputs are consistently useful and accessible to farmers regardless of their technical background.

This platform exemplifies how AI can be leveraged for social good, potentially improving crop yields, reducing resource waste, and supporting sustainable agricultural practices for farmers around the world.

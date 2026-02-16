# Dharti-Drishti Requirements Document

## 1. Project Overview

### 1.1 Vision
Transform soil testing from a weeks-long lab process into an instant, accessible, point-and-shoot mobile experience for Indian farmers.

### 1.2 Problem Statement
- 18,000 farmers depend on a single soil testing lab in India
- Soil reports take up to 4 weeks to arrive
- Reports contain complex technical metrics difficult to interpret
- Existing digital solutions require manual testing, data entry, and digital literacy
- High costs limit accessibility for small farmers

### 1.3 Solution
AI-powered soil intelligence platform that analyzes soil photos with calibration card to deliver actionable farming recommendations in native language.

## 2. Functional Requirements

### 2.1 Image Capture System
- FR-1.1: System shall detect calibration card (credit-card size) in camera frame
- FR-1.2: System shall auto-focus when calibration card is detected
- FR-1.3: System shall capture high-resolution soil image with calibration card
- FR-1.4: System shall validate image quality before upload
- FR-1.5: System shall capture GPS coordinates at time of photo

### 2.2 Soil Analysis Engine
- FR-2.1: System shall classify soil texture (sandy, clay, loamy)
- FR-2.2: System shall estimate water retention capacity based on texture
- FR-2.3: System shall estimate drainage behavior
- FR-2.4: System shall use calibrated color analysis to estimate organic carbon levels
- FR-2.5: System shall categorize organic carbon as High, Medium, or Low
- FR-2.6: System shall detect surface salt crusts
- FR-2.7: System shall identify biological crust patterns
- FR-2.8: System shall flag salinity and soil degradation indicators

### 2.3 GPS-Enriched Intelligence
- FR-3.1: System shall fetch real-time weather data based on GPS location
- FR-3.2: System shall retrieve historical regional agricultural data
- FR-3.3: System shall integrate location data with soil analysis
- FR-3.4: System shall refine recommendations based on regional patterns

### 2.4 Action Engine
- FR-4.1: System shall translate analytical outputs into practical actions
- FR-4.2: System shall provide fertilizer recommendations
- FR-4.3: System shall suggest suitable crops for detected soil type
- FR-4.4: System shall recommend soil improvement strategies
- FR-4.5: System shall suggest irrigation methods (e.g., drip irrigation)
- FR-4.6: System shall recommend amendments (e.g., gypsum for salinity)
- FR-4.7: System shall prioritize cost-effective solutions

### 2.5 Multilingual Output
- FR-5.1: System shall support major Indian languages (Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam, Punjabi)
- FR-5.2: System shall deliver recommendations in farmer's selected language
- FR-5.3: System shall use simple, non-technical language
- FR-5.4: System shall provide voice output option for low-literacy users

### 2.6 User Interface
- FR-6.1: Mobile app shall have simple, intuitive camera interface
- FR-6.2: System shall provide visual guidance for card placement
- FR-6.3: System shall show real-time feedback during capture
- FR-6.4: System shall display results in easy-to-read format
- FR-6.5: System shall allow saving and sharing of recommendations

## 3. Non-Functional Requirements

### 3.1 Performance
- NFR-1.1: Image analysis shall complete within 30 seconds
- NFR-1.2: System shall support offline image capture with delayed upload
- NFR-1.3: App shall work on devices with 2GB RAM minimum
- NFR-1.4: System shall handle 10,000 concurrent users

### 3.2 Usability
- NFR-2.1: Farmer shall complete entire process in under 3 minutes
- NFR-2.2: Interface shall require minimal digital literacy
- NFR-2.3: System shall work in low-connectivity areas (2G/3G)

### 3.3 Accuracy
- NFR-3.1: Soil texture classification shall achieve 85%+ accuracy
- NFR-3.2: Organic carbon estimation shall correlate with lab results within ±15%
- NFR-3.3: Salinity detection shall achieve 80%+ accuracy

### 3.4 Accessibility
- NFR-4.1: Service shall be affordable for small farmers
- NFR-4.2: App size shall be under 50MB
- NFR-4.3: System shall work on Android 8.0+

### 3.5 Security & Privacy
- NFR-5.1: GPS data shall be anonymized for analytics
- NFR-5.2: Farmer data shall be encrypted in transit and at rest
- NFR-5.3: System shall comply with Indian data protection regulations

## 4. System Constraints

### 4.1 Hardware
- Smartphone with camera (5MP minimum)
- GPS capability
- Internet connectivity for upload and results

### 4.2 Calibration Card
- Credit-card size (85.6mm × 53.98mm)
- Standardized color patches for calibration
- Durable, waterproof material
- Low-cost production for mass distribution

## 5. Success Metrics
- 90% user satisfaction rate
- 80%+ recommendation accuracy validated by farmers
- Average analysis time under 30 seconds
- 50% reduction in fertilizer costs for users
- 20% increase in crop yield for users

## Project: Dharti---Drishti

### 1. Project Overview
Brief description of the project's purpose and goals.

### 2. Stakeholders
- Primary users
- Secondary users
- Project team

### 3. Functional Requirements

#### 3.1 Core Features
- Feature 1: [Description]
- Feature 2: [Description]
- Feature 3: [Description]

#### 3.2 User Stories
- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]

### 4. Non-Functional Requirements

#### 4.1 Performance
- Response time requirements
- Throughput requirements
- Resource usage constraints

#### 4.2 Security
- Authentication requirements
- Authorization requirements
- Data protection requirements

#### 4.3 Scalability
- Expected user load
- Growth projections
- Scaling strategy

#### 4.4 Reliability
- Uptime requirements
- Error handling
- Recovery procedures

#### 4.5 Usability
- User interface requirements
- Accessibility standards
- User experience goals

### 5. Technical Requirements
- Platform requirements
- Browser/device compatibility
- Integration requirements
- API requirements

### 6. Constraints
- Budget constraints
- Timeline constraints
- Technical constraints
- Regulatory constraints

### 7. Assumptions and Dependencies
- Key assumptions
- External dependencies
- Third-party services

### 8. Success Criteria
- Measurable goals
- Acceptance criteria
- Key performance indicators

### 9. Out of Scope
- Features explicitly not included
- Future considerations

# 🍌 Banana Leaf Disease Classifier - Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER's WEB BROWSER                      │
│  (Runs in Browser - No Installation Needed)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           FRONTEND (HTML/CSS/JavaScript)                    │
│                                                             │
│  ✓ templates/index.html      (Web page structure)          │
│  ✓ static/style.css          (Beautiful styling)           │
│  ✓ static/script.js          (Upload & results logic)      │
│                                                             │
│  Features:                                                  │
│  • Drag & drop image upload                                │
│  • Live image preview                                      │
│  • Disease diagnosis display                               │
│  • Confidence chart visualization                          │
│  • Treatment recommendations                               │
│  • Mobile responsive design                                │
└──────────────────────────┬──────────────────────────────────┘
                           │ POST /predict (image file)
                           │ GET /health, /api/info
                           ▼
┌─────────────────────────────────────────────────────────────┐
│        BACKEND (Python/Flask - Running on Render)           │
│                                                             │
│  ✓ app.py (Flask Server)                                   │
│     ├─ Serves frontend (HTML)                              │
│     ├─ Loads trained model into memory                     │
│     ├─ Receives image uploads                              │
│     ├─ Validates images (green pixel check)                │
│     ├─ Runs model inference                                │
│     ├─ Returns JSON predictions                            │
│     └─ Keeps model in memory for speed                     │
│                                                             │
│  Features:                                                  │
│  • 3 validation checks (image format, green pixels, conf)  │
│  • Confidence gating (>70% threshold)                      │
│  • Disease information database                            │
│  • RESTful JSON API                                        │
│  • 100-200ms prediction time                               │
└──────────────────────────┬──────────────────────────────────┘
                           │ Load model once
                           │ Keep in memory
                           ▼
┌─────────────────────────────────────────────────────────────┐
│      ML MODEL (ResNet50 - Trained Model.h5)                │
│                                                             │
│  ✓ ResNet50 Base (Pre-trained on ImageNet)               │
│     └─ Frozen layers (transfer learning)                   │
│                                                             │
│  ✓ Custom Head                                             │
│     ├─ GlobalAveragePooling2D                              │
│     ├─ Dense(256) + ReLU activation                        │
│     ├─ Dropout(0.5) for regularization                     │
│     └─ Dense(4) + Softmax for classification               │
│                                                             │
│  Classes:                                                   │
│  • Healthy (✅)                                             │
│  • Cordana Leaf Spot (🟡)                                  │
│  • Pestalotiopsis (🟠)                                     │
│  • Sigatoka (🔴)                                           │
│                                                             │
│  Performance:                                               │
│  • Accuracy: 85-92%                                        │
│  • Training: 10 epochs                                     │
│  • Model size: 95 MB                                       │
│  • Memory: 500 MB in RAM                                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Action                     Application Process
═══════════════════════════════════════════════════════════════

1. User Uploads Image
   │
   ├─→ [Browser] Reads file
   ├─→ Shows preview
   └─→ Sends to /predict endpoint

2. Backend Receives Image
   │
   ├─→ [Flask] Validates format
   ├─→ Converts to PIL Image
   └─→ Triggers validation checks

3. Validation Phase (Sequential)
   │
   ├─→ Check 1: Is file a valid image?
   │   └─ If fail: Return "Invalid file"
   │
   ├─→ Check 2: Does image have green pixels? (Leaf check)
   │   └─ If fail: Return "Not a banana leaf"
   │
   └─→ Check 3: (If passes checks 1-2) Run model

4. Model Inference
   │
   ├─→ Resize image to 224x224
   ├─→ Normalize pixel values
   ├─→ Pass through ResNet50
   ├─→ Get output: [0.05, 0.92, 0.02, 0.01]
   └─→ Extract probabilities

5. Validation Phase (Continued)
   │
   ├─→ Check 4: Is confidence > 70%?
   │   ├─ If fail: Return "Low confidence"
   │   └─ If pass: Continue to results
   └─→ All checks passed ✓

6. Backend Returns Result
   │
   ├─→ JSON with:
   │   ├─ predicted_class: "healthy"
   │   ├─ confidence: 0.92
   │   ├─ all_probabilities: {...}
   │   ├─ disease_info: {...}
   │   └─ recommended_solutions: [...]
   │
   └─→ HTTP 200 (success)

7. Frontend Displays Results
   │
   ├─→ Parse JSON response
   ├─→ Display disease title & emoji
   ├─→ Draw confidence bar chart
   ├─→ Show disease description
   ├─→ List treatment steps
   └─→ Animate results
```

## Deployment Architecture

```
Your Computer          GitHub             Render (Cloud)
═══════════════════════════════════════════════════════════════

Code Files
   │
   ├─→ app.py           ────────→ Repository  ────────→ Pull
   ├─→ train.py                   (Public)               │
   ├─→ requirements.txt                               Build
   ├─→ templates/                                     │
   ├─→ static/                                    CREATE
   └─→ models/                                       │
                                              ┌──────────────┐
                                              │ Build Phase  │
                                              ├──────────────┤
                                              │ • Python 3.11
                                              │ • pip packages
                                              │ • Kaggle keys
                                              └──────────────┘
                                                    │
                                              TRAINING
                                                    │
                                              ┌──────────────┐
                                              │ Train Phase  │
                                              ├──────────────┤
                                              │ 1. Download  │
                                              │ 2. Preprocess│
                                              │ 3. Train     │
                                              │ 4. Evaluate  │
                                              │ 5. Save Model│
                                              └──────────────┘
                                                    │
                                              START SERVER
                                                    │
                                              ┌──────────────┐
                                              │ Web Service  │
                                              ├──────────────┤
                                              │ • flask app  │
                                              │ • model.h5   │
                                              │ • Port 8000  │
                                              │ • Public URL │
                                              └──────────────┘
                                                    │
                                         PUBLIC INTERNET
                                                    │
                                              Users
                                              Access
                                              ...
```

## Request-Response Cycle

```
UPLOAD IMAGE REQUEST
═══════════════════════════════════════════════════════════════

User Browser                                    Flask Server
     │                                               │
     │  POST /predict                               │
     ├──────────────────────────────────────────→  │
     │  Content-Type: multipart/form-data          │
     │  Body: {image: <binary image data>}         │
     │                                              │
     │                                    ┌─────────────────┐
     │                                    │ Processing:     │
     │                                    │ 1. Load image   │
     │                                    │ 2. Validate     │
     │                                    │ 3. Run model    │
     │                                    │ 4. Get results  │
     │                                    └─────────────────┘
     │                                              │
     │  HTTP 200 OK                                │
     │  Content-Type: application/json             │
     │  Body: {                                     │
     │    "status": "success",                      │
     │  ├ "predicted_class": "healthy",             │
     │  ├ "confidence": 0.92,                       │
     │  ├ "all_probabilities": {...},              │
     │  ├ "disease_info": {...},                   │
     │  └ "recommended_solutions": [...]           │
     │  }                                           │
     │←──────────────────────────────────────────  │
     │                                              │
     ├─ Parse JSON                                 │
     ├─ Display results                            │
     └─ Show solutions
```

## Model Architecture Details

```
INPUT IMAGE
(224 × 224 × 3)
     │
     ▼
┌──────────────────────────────────────────────┐
│   ResNet50 (Pre-trained on ImageNet)        │
│                                              │
│  • Conv layer                                │
│  • Batch normalization                       │
│  • Residual blocks (4 stages)                │
│  • Output: (7 × 7 × 2048)                   │
└──────────────────────────────────────────────┘
     │
     ▼ (Features extracted)
┌──────────────────────────────────────────────┐
│   Custom Classification Head                │
│                                              │
│  ├─ GlobalAveragePooling2D                   │
│  │  (7×7×2048) → (2048,)                    │
│  │                                          │
│  ├─ Dense(256, activation='relu')           │
│  │  (2048,) → (256,)                        │
│  │                                          │
│  ├─ Dropout(0.5)                            │
│  │  Random units turned off during training │
│  │                                          │
│  └─ Dense(4, activation='softmax')          │
│     (256,) → (4,)                           │
│                                              │
│  Output: [0.05, 0.92, 0.02, 0.01]           │
│          (cordana, healthy, pest, siga)    │
└──────────────────────────────────────────────┘
     │
     ▼
PREDICTED CLASS: "healthy"
CONFIDENCE: 92%
```

## Deployment Timeline

```
Time    Event                        Duration
════════════════════════════════════════════════════════════
0:00    Click "Deploy" on Render     
0:00    Build begins                 
─────────────────────────────────────────────────────────────
0:00    Install Python 3.11          2 min
0:02    Install pip packages         5 min
        • tensorflow
        • flask
        • scikit-learn
        • kagglehub
0:07    Download from Kaggle         +15 min
        • Complete banana disease dataset (~500MB)
        • Extract and organize files
0:22    ✓ Dataset ready              
─────────────────────────────────────────────────────────────
0:22    Start training               
0:22    Build ResNet50 model         1 min
0:23    Train for 10 epochs          +40 min
        Epoch 1:  ████░░░░ [ 5 min]
        Epoch 2:  ████░░░░ [ 5 min]
        Epoch 3:  ████░░░░ [ 5 min]
        ...
        Epoch 10: ████░░░░ [ 5 min]
1:03    Evaluate on validation set   2 min
1:05    Save model to disk           1 min
1:06    Training complete ✓          
─────────────────────────────────────────────────────────────
1:06    Start Flask server           
1:07    API ready for predictions    
        https://your-app.onrender.com/
✓ TOTAL: ~67 minutes (1 hour 7 minutes)
```

## Performance Metrics

```
Metric                    Value
─────────────────────────────────────────────────────────────
Model Accuracy            85-92%
Training Time (Render)    50-70 min
Inference Time            100-200 ms per image
Model File Size           95 MB
Memory Usage (Loaded)     500-700 MB
Concurrent Users          5-10 (free tier)
Server CPU Usage          Shared
Cost                      $0/month (free tier)
Uptime                    95%+ (Render reliability)
Response Time             <500ms (includes network)
```

## Security Considerations

```
Security Aspect           Implementation
─────────────────────────────────────────────────────────────
API Validation            ✓ File type checking
                          ✓ Image format validation
                          ✓ Size limits

Kaggle Keys              ✓ Build-only env variables
                         ✓ Not available at runtime
                         ✓ Not sent to frontend

Source Code              ✓ Stored on GitHub
                         ✓ Can be public or private
                         ✓ Kaggle keys protected

Model Loading            ✓ Disk-based storage
                         ✓ Check file integrity
                         ✓ Error handling

HTTPS                    ✓ Render provides SSL
                         ✓ Automatic HTTPS
                         ✓ Encrypted in transit
```

## Troubleshooting Flowchart

```
Problem                     Check                    Solution
─────────────────────────────────────────────────────────────
🔴 502 Bad Gateway          → Render logs           Wait for training
                            → Deployment status    Check build phase

🟡 Page loads, no           → Browser console      Model still loading
   predictions              → /health endpoint     Wait 2-3 seconds

🔴 Training fails           → Error message        Check Kaggle creds
                            → Log output           Reduce EPOCHS to 5

🟡 Very slow predictions    → Response time        Upgrade Render plan
   (>5 seconds)             → Server logs          Add more workers

🔴 Out of memory            → Training logs        Reduce BATCH_SIZE
                            → Console errors      Reduce EPOCHS

🟡 Kaggle download error    → Training log         Verify username
                            → Credentials check   Generate new token
```

---

This architecture ensures:
- **Fast Predictions**: Model cached in memory
- **Scalability**: One application, multiple users
- **Reliability**: Error handling and validation
- **Ease of Use**: Beautiful web interface
- **Cost Effective**: Free tier compatible

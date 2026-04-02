# 🍌 Banana Leaf Disease Classifier - Full Stack Application

A complete AI-powered web application for detecting banana leaf diseases with frontend and backend integrated.

## 📊 Technology Stack

**Frontend:**
- HTML5 / CSS3 / JavaScript (Vanilla, no frameworks needed)
- Responsive design (works on mobile, tablet, desktop)
- Real-time image preview and upload
- Interactive result visualization

**Backend:**
- Python 3.11
- Flask (web framework)
- TensorFlow/Keras (ML model)
- ResNet50 (pre-trained deep learning model)

**Deployment:**
- Render (free tier compatible)
- One-click deployment
- Automatic training on first deploy

---

## 🚀 Quick Start (5 Minutes)

### 1. Get Kaggle API Key
- Go to https://www.kaggle.com/settings/account
- Click **Create New Token**
- Save your **KAGGLE_USERNAME** and **KAGGLE_KEY**

### 2. Initialize Git & Push to GitHub
```powershell
cd banana-disease-classifier
git init
git add .
git commit -m "Full stack banana disease classifier"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/banana-disease-classifier.git
git push -u origin main
```

### 3. Deploy on Render
1. Go to https://render.com (create free account)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Fill in details:
   - **Build Command**: `pip install -r requirements.txt && python train.py`
   - **Start Command**: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
5. Add environment variables:
   - `KAGGLE_USERNAME` (build scope)
   - `KAGGLE_KEY` (build scope)
6. Click **Deploy**

**Timeline:** ~1 hour (model trains automatically)

---

## 📁 Project Structure

```
banana-disease-classifier/
├── app.py                    # Flask backend (API + serves frontend)
├── train.py                  # Training script (runs once on deploy)
├── requirements.txt          # Python dependencies
├── render.yaml               # Render config
├── Procfile                  # Deployment config
├── README.md                 # This file
│
├── templates/
│   └── index.html           # Web interface (frontend)
│
├── static/
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
│
└── models/                  # Created at runtime
    ├── banana_disease_model.h5      # Trained model
    └── class_metadata.json          # Class info
```

---

## 🌐 Web Interface Features

### Upload Section
- **Drag & Drop**: Drop image directly on upload area
- **Click Upload**: Click to browse and select image
- **Live Preview**: See selected image before submission
- **Change Image**: Quick button to select different image

### Results Display
- **Disease Diagnosis**: Shows predicted disease with emoji
- **Confidence Meter**: Visual bar chart showing probability for each class
- **Disease Info**: Detailed description of the detected disease
- **Solutions**: Step-by-step treatment recommendations
- **Validation**: Only shows results if image passes quality checks

### Responsive Design
- Mobile-friendly interface
- Adapts to all screen sizes
- Touch-friendly buttons
- Works offline (after initial load)

---

## 🔧 Local Testing

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Kaggle Credentials
```powershell
# Windows PowerShell
$env:KAGGLE_USERNAME = "your_username"
$env:KAGGLE_KEY = "your_api_key"

# Linux/Mac
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

### Step 3: Train Model (One Time)
```bash
python train.py
```
- Downloads dataset (~500MB)
- Trains ResNet50 (30-50 min on CPU)
- Creates `models/banana_disease_model.h5`

### Step 4: Run Flask Server
```bash
python app.py
```
Output:
```
======================================================================
🚀 BANANA LEAF DISEASE CLASSIFIER - API SERVER
======================================================================
Starting Flask server on port 5000...
```

### Step 5: Open Web Browser
```
http://localhost:5000
```

---

## 📡 API Endpoints

All backend endpoints are RESTful JSON APIs:

### 1. Web Interface (Get)
```bash
GET /
```
Returns: HTML web interface

### 2. Health Check (Get)
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_available": 4,
  "classes": ["healthy", "cordana", "pestalotiopsis", "sigatoka"]
}
```

### 3. Model Information (Get)
```bash
GET /api/info
```
Returns: Model details, disease info, thresholds

### 4. Make Prediction (Post)
```bash
curl -X POST -F "image=@leaf.jpg" http://localhost:5000/predict
```

**Success Response (200):**
```json
{
  "status": "success",
  "predicted_class": "healthy",
  "confidence": 0.92,
  "all_probabilities": {
    "healthy": 0.92,
    "cordana": 0.05,
    "pestalotiopsis": 0.02,
    "sigatoka": 0.01
  },
  "disease_info": {
    "emoji": "✅",
    "title": "HEALTHY LEAF",
    "description": "Your banana leaf is perfectly healthy...",
    "recommended_solutions": [
      "Keep watering the plant regularly",
      "Ensure it receives adequate sunlight",
      "Remove dead leaves periodically",
      "Monitor weekly for early disease signs"
    ]
  }
}
```

**Rejected Response (400):**
```json
{
  "status": "rejected",
  "reason": "LOW_CONFIDENCE",
  "message": "Model could not confidently classify this image",
  "confidence": 0.45,
  "required_confidence": 0.70
}
```

---

## 🎨 Frontend How It Works

### 1. User Uploads Image
- Drag & drop or click upload
- Image preview appears
- JavaScript sends image to backend

### 2. Backend Processes Image
- Validates it looks like a banana leaf (green pixel check)
- Resizes to 224x224
- Runs through ResNet50 model
- Checks confidence > 70%

### 3. Frontend Shows Results
- If success: Shows disease, confidence, solutions
- If rejected: Shows why (not a leaf, low confidence)
- If error: Shows error message
- User can try another image

### 4. All in One Application
- No external dependencies needed
- No separate deployment needed
- Frontend and backend together
- Single deployment URL

---

## 🏃‍♂️ How Training Works on Deploy

When you click **Deploy** on Render:

```
1. Build Phase (2-3 min)
   └─ Install Python and packages

2. Training Phase (30-50 min)
   ├─ Download dataset from Kaggle
   ├─ Prepare training data
   ├─ Build ResNet50 model
   ├─ Train for 10 epochs
   ├─ Save model to disk
   └─ Exit successfully

3. Start Phase
   ├─ Flask server starts
   ├─ Loads model into memory on first request
   └─ Ready to serve predictions

4. Serving Phase (Until restart)
   ├─ Model stays in memory
   └─ Fast predictions (no reloading)
```

---

## ⚙️ Configuration

### Modify Training
Edit `train.py`:
```python
IMG_SIZE   = 224      # Image dimensions (keep 224)
BATCH_SIZE = 16       # Reduce if out of memory
EPOCHS     = 10       # Reduce for faster training (5 = 20 min)
```

### Modify Thresholds
Edit `app.py`:
```python
CONFIDENCE_THRESHOLD  = 0.70   # Prediction confidence gate
GREEN_RATIO_THRESHOLD = 0.10   # Leaf detection sensit
```

---

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| First Deploy Time | 1 hour (model training) |
| Model File Size | ~95 MB |
| Model Memory Usage | ~500 MB RAM |
| Training Data | ~3,500 images |
| Prediction Time | 100-200ms per image |
| Expected Accuracy | 85-92% |
| Free Tier Cost | $0/month |

---

## 🐛 Troubleshooting

### "502 Bad Gateway" on Render
**Cause**: Model still training or failed to train
**Fix**: Check Render logs, wait for training to complete

### Web page loads but predictions don't work
**Cause**: Model not loaded yet
**Fix**: Wait 2-3 seconds after first request, then try again

### Slow predictions
**Cause**: Free tier Render has shared CPU
**Fix**: Upgrade to paid plan or optimize model

### Training fails on Render
**Cause**: Kaggle credentials invalid or timed out
**Fix**: 
1. Verify KAGGLE_USERNAME and KAGGLE_KEY are correct
2. Reduce EPOCHS to 5 for faster training
3. Check training_log.txt in logs

### Out of memory errors
**Cause**: BATCH_SIZE too large
**Fix**: Edit train.py, change `BATCH_SIZE = 8`

---

## 🔄 Updating the Application

### Update Code
```bash
# Make changes to app.py, train.py, or frontend files
git add .
git commit -m "Update description"
git push origin main
```

### Redeploy on Render
- In Render dashboard: **Manual Deploy**
- Training reruns automatically
- New model replaces old one

### Only Update Frontend
- Changes to `templates/index.html`, `static/style.css`, `static/script.js`
- Just push to GitHub
- Server automatically restarts with new frontend
- No retraining needed

---

## 🚀 Advanced Features

### Add Custom CSS
Edit `static/style.css` - supports:
- Dark/light themes
- Custom colors
- Animation tweaks
- Mobile optimizations

### Modify Disease Info
Edit `DISEASE_INFO` dictionary in `app.py`:
```python
DISEASE_INFO = {
    "healthy": {...},
    "cordana": {...},
    # Add more here
}
```

### Add More Validation
Edit validation functions in `app.py`:
```python
def is_green_enough(pil_img, threshold=GREEN_RATIO_THRESHOLD):
    """Add custom validation logic"""
    ...
```

---

## 📝 Deployment Checklist

- [ ] Kaggle credentials obtained
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web Service created (not Background Job)
- [ ] Environment variables set (KAGGLE_USERNAME, KAGGLE_KEY)
- [ ] Deployment started
- [ ] Training completed (~1 hour)
- [ ] `/health` endpoint returns healthy
- [ ] Web interface loads at `/`
- [ ] Predictions work with test image

---

## 🎓 Learning Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **ResNet50 Paper**: https://arxiv.org/abs/1512.03385
- **TensorFlow Docs**: https://www.tensorflow.org/
- **Render Deployment**: https://render.com/docs

---

## 📞 Support

### If It Doesn't Work:

1. **Check Render Logs**: Dashboard → Logs tab
2. **Check training_log.txt**: Has detailed training info
3. **Try Locally First**: Test with `python app.py`
4. **Verify Kaggle Keys**: Make sure they're correct
5. **Check Frontend Console**: Browser DevTools F12 → Console

### Common Issues:

| Issue | Solution |
|-------|----------|
| Model loading fails | Check Kaggle credentials |
| Predictions slow | Upgrade to paid Render plan |
| Training timeout | Reduce EPOCHS to 5 |
| Out of memory | Reduce BATCH_SIZE to 8 |

---

## ✨ Features Summary

✅ Full web interface (HTML/CSS/JS)  
✅ Drag & drop image upload  
✅ Real-time image preview  
✅ Disease diagnosis with confidence  
✅ Treatment recommendations  
✅ Responsive design (mobile-friendly)  
✅ Model in-memory caching  
✅ Validation (green pixel + confidence checks)  
✅ One-click Render deployment  
✅ Free tier compatible  
✅ No external framework dependencies  

---

**🎉 You now have a complete AI web application ready to deploy!**

Push to GitHub → Deploy on Render → Done! 🍌

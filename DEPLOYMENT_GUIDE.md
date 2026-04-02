# 🚀 Deployment Guide - Banana Leaf Disease Classifier

## Overview

This project automatically:
1. **Training Phase** (happens once on deploy)
   - Downloads banana leaf dataset from Kaggle
   - Trains ResNet50 model (30-50 minutes)
   - Saves trained model to disk

2. **Serving Phase** (starts after training completes)
   - Flask API loads model into server **memory**
   - Model stays in memory until server restarts
   - Serves predictions via HTTP API
   - No retraining needed between requests

---

## ✅ Quick Deployment (5 Minutes)

### 1. Get Kaggle Credentials (2 min)
- Go to https://www.kaggle.com/settings/account
- Click **Create New Token**
- Download `kaggle.json`
- Note down your **KAGGLE_USERNAME** and **KAGGLE_KEY**

### 2. Fork to GitHub (2 min)
```bash
git init
git add .
git commit -m "Banana leaf classifier"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/banana-disease-classifier.git
git push -u origin main
```

### 3. Deploy on Render (1 min setup, then wait for training)
- Go to https://render.com (create free account)
- Click **New +** → **Web Service**
- Connect your GitHub repository
- Set **Runtime** to **Python 3.11**
- Enter these commands:
  - **Build Command**: `pip install -r requirements.txt && python train.py`
  - **Start Command**: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
- Click **Advanced** → **Add Environment Variable**:
  - Key: `KAGGLE_USERNAME` → Value: your kaggle username
  - Key: `KAGGLE_KEY` → Value: your kaggle key
- Click **Deploy**

### ⏱️ Timeline
- **Minutes 0-2**: Render builds environment
- **Minutes 2-7**: Installs Python packages
- **Minutes 7-25**: Downloads Kaggle dataset (~500MB)
- **Minutes 25-70**: Trains ResNet50 model
- **Minute 70+**: Flask API starts and ready for requests

---

## 🎯 Architecture Explanation

### What Happens on Deploy

```
┌─ BUILD PHASE (Render creates environment)
│  ├─ Install Python 3.11
│  ├─ Install requirements.txt packages
│  └─ Set KAGGLE_USERNAME & KAGGLE_KEY env vars
│
├─ TRAINING PHASE (runs python train.py)
│  ├─ Download dataset from Kaggle (15 min, ~500MB)
│  ├─ Load images and split train/val
│  ├─ Build ResNet50 model
│  ├─ Train for 10 epochs (40 min on CPU)
│  ├─ Evaluate on validation set
│  ├─ Save model to: models/banana_disease_model.h5 (~95MB)
│  └─ Save metadata to: models/class_metadata.json
│
└─ SERVING PHASE (runs gunicorn + Flask)
   ├─ Start Flask API server on port 8000
   ├─ Load model into memory on first request
   ├─ Model stays in memory (not reloaded)
   └─ Serve predictions until server restarts
```

### In-Memory Model Storage

**Why this approach?**
- ✅ Fast predictions (model already in RAM)
- ✅ No disk I/O for each request
- ✅ No retraining needed
- ✅ Works on free tier

**What it means:**
- Model loads once on first API request
- Stays in server memory until restart
- All subsequent requests reuse same model
- Server restart = model reloads from disk

---

## 📡 Using the API

### Base URL
```
https://your-render-url.onrender.com
```

### 1. Health Check
```bash
curl https://your-render-url.onrender.com/health
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

### 2. Get Model Information
```bash
curl https://your-render-url.onrender.com/info
```

### 3. Make a Prediction
```bash
curl -X POST \
  -F "image=@path/to/banana_leaf.jpg" \
  https://your-render-url.onrender.com/predict
```

**Response (if healthy leaf - 200)**:
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
      "Keep watering regularly",
      "Ensure adequate sunlight",
      "Remove dead leaves"
    ]
  }
}
```

**Response (if not confident - 400)**:
```json
{
  "status": "rejected",
  "reason": "LOW_CONFIDENCE",
  "message": "Model could not confidently classify this image",
  "confidence": 0.45,
  "required_confidence": 0.70
}
```

**Response (if not a leaf - 400)**:
```json
{
  "status": "rejected",
  "reason": "NOT_A_LEAF",
  "message": "Image does not contain enough green content to be a banana leaf"
}
```

---

## 🧪 Testing Locally

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Kaggle Credentials
```powershell
# Windows PowerShell
$env:KAGGLE_USERNAME = "your_username"
$env:KAGGLE_KEY = "your_key"

# Linux/Mac Bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_key"
```

### Step 3: Train Model
```bash
python train.py
```
This creates:
- `models/banana_disease_model.h5` (trained model)
- `models/class_metadata.json` (class information)
- `training_log.txt` (training details)

### Step 4: Start API Server
```bash
python app.py
```
Output:
```
======================================================================
🚀 BANANA LEAF DISEASE CLASSIFIER - API SERVER
======================================================================
Starting Flask server on port 5000...
Model will be loaded on first request and kept in memory
```

### Step 5: Test in Another Terminal
```bash
# Health check
curl http://localhost:5000/health

# Make prediction
curl -X POST -F "image=@test_leaf.jpg" http://localhost:5000/predict
```

Or use the test script:
```bash
python test_api.py
```

---

## 🔧 Configuration

Edit `train.py` to adjust:

```python
IMG_SIZE   = 224      # Image dimensions (224x224)
BATCH_SIZE = 16       # Reduce if out of memory
EPOCHS     = 10       # Reduce for faster training
```

Edit `app.py` to adjust:

```python
CONFIDENCE_THRESHOLD  = 0.70   # Prediction confidence gate
GREEN_RATIO_THRESHOLD = 0.10   # Leaf detection threshold
```

---

## ⚠️ Troubleshooting

### "Model not loading error" on Deploy
**Check**: 
1. Verify `python train.py` completed successfully
2. Check Render logs for training errors
3. Ensure Kaggle credentials are correct

**Fix**:
1. Check training_log.txt for errors
2. Redeploy with corrected settings

### Training Times Out (>24 hours)
**Cause**: Free tier Render has 24-hour time limit

**Solutions**:
1. Reduce EPOCHS: Change `EPOCHS = 10` to `EPOCHS = 5` in train.py
2. Reduce BATCH_SIZE for faster training
3. Upgrade to paid Render plan ($7+/month)

### Out of Memory During Training
**Solution**: Edit train.py, reduce BATCH_SIZE:
```python
BATCH_SIZE = 8  # Reduce from 16
```

### Predictions Very Slow
**Cause**: Free tier Render has shared CPU

**Solution**: Upgrade to paid plan for dedicated resources

### Kaggle Download Fails
**Check**:
1. KAGGLE_USERNAME set correctly (exact username)
2. KAGGLE_KEY valid (download new token if expired)
3. Internet connection stable
4. Kaggle dataset exists (try downloading manually)

---

## 🚀 Advanced Features

### Custom Health Checks
The `/health` endpoint returns model status:
- Model loaded: `true/false`
- Classes available: number of disease categories
- Classes list: actual class names

### Confidence Gating
Both checks must pass:
1. **Green Pixel Test**: Ensures image looks like a leaf
2. **Confidence Test**: Model must be >70% confident

Only returns prediction if both pass. Otherwise rejects with error.

### Batch Predictions
To classify multiple images:
```bash
for image in images/*.jpg; do
  curl -X POST -F "image=@$image" \
    https://your-url.onrender.com/predict
done
```

---

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| First Deploy Training Time | 50-70 min |
| Model File Size | ~95 MB |
| Training Data | ~3,500 images |
| Expected Accuracy | 85-92% |
| Inference Time | 100-200ms per image |
| Model Memory Usage | ~500MB RAM |
| Free Tier Cost | $0/month |

---

## 🔄 Retraining the Model

To update the model with new code or retrain:

1. Make changes to `train.py`
2. Push to GitHub:
   ```bash
   git add train.py
   git commit -m "Update training parameters"
   git push
   ```
3. In Render Dashboard: Click **Manual Deploy** or wait for auto-deploy
4. Training runs again, previous model replaced
5. API automatically restarts with new model

---

## 📝 Files Overview

| File | Purpose |
|------|---------|
| `train.py` | Download dataset & train model once |
| `app.py` | Flask API server (loads model in memory) |
| `requirements.txt` | Python package dependencies |
| `render.yaml` | Render deployment configuration |
| `Procfile` | Alternative deployment config (Heroku/Render) |
| `test_api.py` | Local testing script |
| `models/` | Directory for trained model (created at runtime) |

---

## ✅ Deployment Checklist

- [ ] Kaggle API key obtained
- [ ] GitHub repository created and code pushed
- [ ] Render account created
- [ ] Web Service created (not Background Job)
- [ ] Build Command set to: `pip install -r requirements.txt && python train.py`
- [ ] Start Command set to: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
- [ ] KAGGLE_USERNAME environment variable added
- [ ] KAGGLE_KEY environment variable added
- [ ] Deploy button clicked
- [ ] Waiting for training to complete (~1 hour)
- [ ] `/health` endpoint returns `"model_loaded": true`
- [ ] Test prediction with sample image

---

## 📞 Support

If you hit issues:
1. Check Render **Logs** tab for error messages
2. Check `training_log.txt` for training errors
3. Review this guide's **Troubleshooting** section
4. Verify Kaggle credentials in Render environment variables

---

**You're all set! The model trains once on deploy and stays in memory. Happy classifying! 🍌**

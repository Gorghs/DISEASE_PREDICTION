# 🚀 Deployment Guide - Banana Leaf Disease Classifier

## Overview

This is a **pre-trained inference-only deployment**:
- **Model** - Pre-trained ResNet50 (97.84% accuracy, 96.5 MB)
- **Dual Classification** - Primary ResNet50 + optional Gemini Vision fallback
- **No Training Needed** - Model is pre-trained and ready to serve
- **Fast & Memory-Efficient** - Loads once, stays in RAM

---

## ✅ Quick Deployment (2 Minutes)

### 1. Push to GitHub (1 min)
```bash
git add .
git commit -m "Banana leaf classifier with Gemini fallback"
git push origin main
```

### 2. Deploy on Render (1 min setup)
- Go to https://render.com 
- Click **New +** → **Web Service** → Connect GitHub repo
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
- **(Optional)** **Environment Variable** for fallback:
  - Key: `BACKUP_SVC` → Value: [Your Gemini API key from https://ai.google.dev]
- Click **Deploy**

### ⏱️ Timeline
- **0-2 min**: Dependencies install and Flask starts
- **Ready immediately** for predictions (model loads on first request)

---

## 🎯 How It Works

### Two-Model Classification System

```
User Image
    ↓
[PRIMARY] ResNet50 Model
    ↓
Confidence ≥ 70%?
    ├─ YES → Return prediction ✅
    └─ NO  → Try BACKUP SERVICE
           ↓
      [FALLBACK] Gemini Vision API (if enabled)
           ↓
      Return Gemini classification as "backup_validated"
```

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

### 2. Make a Prediction
```bash
curl -X POST \
  -F "image=@path/to/banana_leaf.jpg" \
  https://your-render-url.onrender.com/predict
```

**Response (successful)**:
```json
{
  "status": "success",
  "predicted_class": "healthy",
  "confidence": 0.92,
  "all_probabilities": { ... },
  "disease_info": {
    "emoji": "✅",
    "title": "HEALTHY LEAF",
    "recommended_solutions": [...]
  }
}
```

**Response (using fallback)**:
```json
{
  "status": "success",
  "source": "backup_validated",
  "predicted_class": "cordana",
  "confidence": 0.85,
  ...
}
```

---

## 🧪 Testing Locally

### Step 1: Install Dependencies
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

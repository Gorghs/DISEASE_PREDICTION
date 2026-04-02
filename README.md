# 🍌 Banana Leaf Disease Classifier - Full Stack

A ResNet50-based machine learning API that classifies banana leaf diseases and provides treatment recommendations.

## 🎯 Features

- **Training**: Automatically downloads dataset from Kaggle and trains ResNet50 model
- **Inference**: Flask API that loads trained model into memory on startup
- **Model Persistence**: Model stays in memory until server restart (no retraining needed)
- **Disease Detection**: Classifies 5 categories: healthy, cordana, pestalotiopsis, sigatoka
- **Validation**: Green pixel detection to ensure input is a banana leaf
- **Confidence Gating**: Only returns predictions when model is confident (>70%)
- **Treatment Info**: Provides disease information and recommended solutions

## 📊 Architecture

```
banana-disease-classifier/
├── train.py          # Training script (download dataset → train → save model)
├── app.py            # Flask API server (load model → serve predictions)
├── requirements.txt  # Python dependencies
├── Procfile          # Heroku/Render deployment config
├── render.yaml       # Render-specific config
└── models/           # Directory for trained model & metadata (created at runtime)
    ├── banana_disease_model.h5
    └── class_metadata.json
```

## 🚀 Deployment on Render

### Prerequisites
- GitHub account
- Kaggle account (for dataset access)
- Render account (free or paid)

### Step-by-Step Deployment

1. **Get Kaggle API Key**
   - Go to https://www.kaggle.com/settings/account
   - Click "Create New Token"
   - Save `KAGGLE_USERNAME` and `KAGGLE_KEY`

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Banana leaf disease classifier"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/banana-disease-classifier.git
   git push -u origin main
   ```

3. **Deploy on Render**
   - Go to https://render.com
   - Click **New +** → **Web Service**
   - Connect your GitHub repository
   - Select **Python** runtime
   - Fill in:
     - **Build Command**: `pip install -r requirements.txt && python train.py`
     - **Start Command**: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
   - Add Environment Variables:
     - `KAGGLE_USERNAME` = your kaggle username (build only)
     - `KAGGLE_KEY` = your kaggle API key (build only)
   - Click **Deploy**

### Timeline
- **Build**: 2-3 minutes (install dependencies)
- **Training**: 30-50 minutes (train ResNet50 model)
- **API Ready**: Automatically starts serving after training completes
- **Total**: ~50-70 minutes first deployment

## 📡 API Endpoints

All endpoints return JSON responses.

### 1. **Health Check** - Verify server is running
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

### 2. **Get Info** - Model and disease information
```bash
curl https://your-render-url.onrender.com/info
```

### 3. **Make Prediction** - Classify banana leaf disease
```bash
curl -X POST -F "image=@leaf.jpg" https://your-render-url.onrender.com/predict
```

**Success Response (200)**:
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
      "..."
    ]
  }
}
```

**Rejected Response (400)** - Low confidence:
```json
{
  "status": "rejected",
  "reason": "LOW_CONFIDENCE",
  "message": "Model could not confidently classify this image",
  "confidence": 0.45,
  "required_confidence": 0.7
}
```

**Rejected Response (400)** - Not a leaf:
```json
{
  "status": "rejected",
  "reason": "NOT_A_LEAF",
  "message": "Image does not contain enough green content to be a banana leaf",
  "green_ratio": 0.05,
  "required_ratio": 0.10
}
```

## 🔧 Local Testing

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Kaggle credentials**:
   ```bash
   # Windows PowerShell
   $env:KAGGLE_USERNAME = "your_username"
   $env:KAGGLE_KEY = "your_key"
   
   # Linux/Mac
   export KAGGLE_USERNAME="your_username"
   export KAGGLE_KEY="your_key"
   ```

3. **Train the model**:
   ```bash
   python train.py
   ```
   This will:
   - Download dataset from Kaggle (~500MB)
   - Train ResNet50 model (30-50 min on CPU)
   - Save model to `models/banana_disease_model.h5`
   - Create `models/class_metadata.json`

4. **Start the API server**:
   ```bash
   python app.py
   ```
   - Server runs on http://localhost:5000
   - Model is loaded into memory on first request
   - Test with: `curl http://localhost:5000/health`

5. **Test prediction**:
   ```bash
   curl -X POST -F "image=@path/to/leaf.jpg" http://localhost:5000/predict
   ```

## 📊 Model Details

- **Architecture**: ResNet50 (pre-trained on ImageNet)
- **Base Model**: Frozen (transfer learning)
- **Custom Head**: GlobalAveragePooling2D → Dense(256) → Dropout(0.5) → Dense(num_classes)
- **Input Size**: 224x224 RGB images
- **Classes**: 4 (healthy, cordana, pestalotiopsis, sigatoka)
- **Training Data**: ~3,500 images (80/20 train/val split)
- **Expected Accuracy**: 85-92%

## 🚀 How It Works

### Training Phase (Happens Once on Deploy)
1. Download banana leaf disease dataset from Kaggle
2. Split into 80% training, 20% validation
3. Load ResNet50 with ImageNet weights
4. Add custom classification head
5. Train for 10 epochs
6. Evaluate on validation set
7. Save model as `models/banana_disease_model.h5`
8. Save class names as `models/class_metadata.json`

### Inference Phase (Runs Until Restart)
1. **First API request**: Load model into server memory
2. **Receive image**: Validate it's actually a banana leaf (green pixel check)
3. **Preprocess**: Resize to 224x224, normalize
4. **Predict**: Get class probabilities from ResNet50
5. **Validate**: Check if confidence > 70%
6. **Return**: JSON with prediction, confidence, treatment info
7. **Keep in memory**: Model stays loaded for all future requests (no reload)

## ⚠️ Important Notes

- **One-time Training**: Model trains once on first deploy, doesn't retrain unless you redeploy
- **In-Memory**: Trained model stays in server memory until server restarts
- **No Retraining**: Subsequent API calls use the loaded model, no re-training
- **Free Tier Ready**: Works on Render free tier ($0/month)
- **Auto Scaling**: Can be upgraded to paid plans for faster inference if needed

## 🔄 Updating the Model

To retrain with updated code:
1. Make changes to `train.py`
2. Push to GitHub: `git push origin main`
3. In Render dashboard: Click **Deploy** (re-triggers training)
4. Wait for new model to train and API to restart

## 📝 Environment Variables

Required only during **build/training**:
- `KAGGLE_USERNAME` - Your Kaggle account username
- `KAGGLE_KEY` - Your Kaggle API key (from settings)

These are **cleared after build** for security (not available at runtime).

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not loading | Check logs: `python train.py` completed successfully? |
| Predictions too slow | Need paid plan for faster inference (free tier is shared CPU) |
| Out of memory | Reduce BATCH_SIZE in `train.py` |
| Kaggle download fails | Verify KAGGLE_USERNAME and KAGGLE_KEY are correct |
| Low accuracy | Dataset might be imbalanced - check `training_log.txt` |

## 📚 References

- [Kaggle Dataset](https://www.kaggle.com/datasets/shifatearman/bananalsd)
- [ResNet50 Paper](https://arxiv.org/abs/1512.03385)
- [TensorFlow Docs](https://www.tensorflow.org/guide)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Deployment Guide](https://render.com/docs)

## 📄 License

MIT License - Feel free to use for educational and commercial purposes.

---

**Questions?** Open an issue or check the deployment logs on Render dashboard.

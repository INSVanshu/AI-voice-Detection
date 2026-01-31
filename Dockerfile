FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Step 5: Click "Commit new file"**

---

## 📋 ALSO UPDATE requirements.txt:

While you're there, edit `requirements.txt`:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-core==2.14.1
librosa==0.10.1
soundfile==0.12.1
numpy==1.24.3
scipy==1.11.3
python-multipart==0.0.6
numba==0.58.1


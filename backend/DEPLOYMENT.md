# 🚀 Backend Deployment Guide

## Quick Deployment Options

---

## Option 1: Local Development (Recommended for Testing)

### Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Run
```bash
python app.py
```

Server runs at: `http://localhost:5000`

---

## Option 2: Production with Gunicorn

### Install Gunicorn
```bash
pip install gunicorn
```

### Run
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Options:
- `-w 4`: 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `app:app`: Module:application

### With Nginx (Recommended)

1. Install Nginx
```bash
sudo apt-get install nginx
```

2. Configure Nginx (`/etc/nginx/sites-available/crop-disease-api`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/audio/ {
        alias /path/to/backend/audio_files/generated/;
    }
}
```

3. Enable site
```bash
sudo ln -s /etc/nginx/sites-available/crop-disease-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. Run Gunicorn
```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## Option 3: Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p uploads audio_files/generated

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Build and Run
```bash
# Build image
docker build -t crop-disease-api .

# Run container
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/audio_files:/app/audio_files \
  -v $(pwd)/trained_models:/app/trained_models \
  --name crop-disease-api \
  crop-disease-api

# Check logs
docker logs -f crop-disease-api
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./audio_files:/app/audio_files
      - ./trained_models:/app/trained_models
    environment:
      - DEBUG=False
      - DATABASE_TYPE=mongodb
      - MONGODB_URI=mongodb://mongo:27017/
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

Run with:
```bash
docker-compose up -d
```

---

## Option 4: Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup

1. Create `Procfile`
```
web: gunicorn app:app
```

2. Create `runtime.txt`
```
python-3.9.16
```

3. Update `requirements.txt` (add gunicorn)
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create crop-disease-api

# Set environment variables
heroku config:set DEBUG=False
heroku config:set DATABASE_TYPE=mongodb
heroku config:set MONGODB_URI=your_mongodb_uri

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Option 5: AWS EC2 Deployment

### Launch EC2 Instance
1. Launch Ubuntu 20.04 instance
2. Configure security group (allow port 80, 443, 5000)
3. SSH into instance

### Setup
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3-pip python3-venv nginx

# Clone repository
git clone <your-repo-url>
cd crop-disease-detection/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Install and configure Nginx (see Option 2)

# Run with systemd
sudo nano /etc/systemd/system/crop-disease-api.service
```

### Systemd Service File
```ini
[Unit]
Description=Crop Disease Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/crop-disease-detection/backend
Environment="PATH=/home/ubuntu/crop-disease-detection/backend/venv/bin"
ExecStart=/home/ubuntu/crop-disease-detection/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl start crop-disease-api
sudo systemctl enable crop-disease-api
sudo systemctl status crop-disease-api
```

---

## Option 6: Railway Deployment

### Setup
1. Create account at railway.app
2. Install Railway CLI
```bash
npm i -g @railway/cli
```

3. Login and deploy
```bash
railway login
railway init
railway up
```

4. Set environment variables in Railway dashboard

---

## Environment Variables for Production

```env
# Flask
SECRET_KEY=your-secure-random-key-here
DEBUG=False
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://username:password@host:port/database
# Or for PostgreSQL
# DATABASE_TYPE=postgresql
# POSTGRES_URI=postgresql://username:password@host:port/database

# TTS
TTS_ENGINE=gtts

# Auto-generate audio
AUTO_GENERATE_AUDIO=False
```

---

## Security Checklist

- [ ] Change SECRET_KEY to random secure value
- [ ] Set DEBUG=False in production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (SSL certificate)
- [ ] Configure firewall rules
- [ ] Set up database authentication
- [ ] Implement rate limiting
- [ ] Add API authentication (JWT)
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

---

## Performance Optimization

### 1. Use Gunicorn with multiple workers
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Enable caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### 3. Optimize image processing
- Resize images before processing
- Use efficient image formats
- Implement image compression

### 4. Database optimization
- Add indexes
- Use connection pooling
- Implement query caching

### 5. Use CDN for audio files
- Upload to S3/CloudFront
- Serve static files separately

---

## Monitoring

### Application Logs
```bash
# View logs
tail -f /var/log/crop-disease-api.log

# With systemd
journalctl -u crop-disease-api -f
```

### Health Check Endpoint
```bash
curl http://your-domain.com/api/health
```

### Monitoring Tools
- **Sentry**: Error tracking
- **New Relic**: Performance monitoring
- **Datadog**: Infrastructure monitoring
- **Prometheus + Grafana**: Metrics and dashboards

---

## Backup Strategy

### Database Backup
```bash
# MongoDB
mongodump --uri="mongodb://localhost:27017/crop_disease_db" --out=/backup/

# PostgreSQL
pg_dump crop_disease_db > backup.sql
```

### File Backup
```bash
# Backup uploads and audio files
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/ audio_files/
```

---

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple instances
- Share storage (S3, NFS)
- Use Redis for session management

### Vertical Scaling
- Increase server resources
- Optimize code and queries
- Use caching extensively

---

## Troubleshooting

### Check if server is running
```bash
curl http://localhost:5000/
```

### Check logs
```bash
tail -f /var/log/crop-disease-api.log
```

### Test endpoints
```bash
./test_api.sh
```

### Check port availability
```bash
sudo lsof -i :5000
```

### Restart service
```bash
sudo systemctl restart crop-disease-api
```

---

## Post-Deployment Checklist

- [ ] Server is accessible
- [ ] All endpoints working
- [ ] Database connected
- [ ] ML model loaded
- [ ] TTS generating audio
- [ ] Translation working
- [ ] CORS configured
- [ ] Logs being written
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] SSL certificate installed
- [ ] Domain configured
- [ ] Android app connected

---

## Support

For deployment issues:
- Check logs first
- Test endpoints with curl
- Verify environment variables
- Check firewall rules
- Review security group settings

---

**Happy Deploying! 🚀**

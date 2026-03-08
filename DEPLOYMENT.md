# Dharti-Drishti Deployment Guide

## Prerequisites
- Docker installed on your machine ([Install Docker](https://docs.docker.com/get-docker/))
- Your `.env` file with all API keys and credentials

## Quick Start Commands

### 1. Build the Docker Image
```bash
docker build -t dharti-drishti:latest .
```

### 2. Run the Container (Development)
```bash
docker run -d \
  --name dharti-drishti-app \
  -p 5000:5000 \
  --env-file .env \
  dharti-drishti:latest
```

### 3. Access the Application
- **Frontend**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health
- **API Analyze Endpoint**: http://localhost:5000/api/analyze

### 4. Check if it's Running
```bash
docker ps
```

### 5. View Logs
```bash
docker logs dharti-drishti-app
```

### 6. Test the Application
```bash
curl http://localhost:5000/api/health
```

### 7. Stop the Container
```bash
docker stop dharti-drishti-app
```

### 8. Remove the Container
```bash
docker rm dharti-drishti-app
```

## Environment Variables Setup

### Option 1: Using .env File (Recommended for Local)
Keep your `.env` file in the project root and use `--env-file .env` flag when running.

### Option 2: Pass Variables Individually
```bash
docker run -d \
  --name dharti-drishti-app \
  -p 5000:5000 \
  -e GOOGLE_API_KEY=your_key_here \
  -e GROQ_API_KEY=your_key_here \
  -e AWS_ACCESS_KEY_ID=your_key_here \
  -e AWS_SECRET_ACCESS_KEY=your_key_here \
  dharti-drishti:latest
```

### Option 3: Using Docker Secrets (Production)
For production deployments, use Docker secrets or your cloud provider's secret management.

## Production Deployment Options

### Understanding URLs After Deployment

When you deploy to any cloud platform, you'll get a public URL. Here's how it works:

**Example: If your deployed URL is `https://your-app.example.com`**

- **Frontend (Main App)**: `https://your-app.example.com/`
- **API Health Check**: `https://your-app.example.com/api/health`
- **API Analyze**: `https://your-app.example.com/api/analyze`

The frontend JavaScript automatically detects the domain and uses the correct API URL. No code changes needed!

### Option A: Deploy to Cloud Run (Google Cloud)

1. Install Google Cloud SDK
2. Authenticate:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

3. Build and push to Google Container Registry:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/dharti-drishti
```

4. Deploy to Cloud Run:
```bash
gcloud run deploy dharti-drishti \
  --image gcr.io/YOUR_PROJECT_ID/dharti-drishti \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars "$(cat .env | xargs)"
```

**Your app will be available at**: `https://dharti-drishti-XXXXX-uc.a.run.app`

The frontend will automatically work at the root URL, and API at `/api/*`

### Option B: Deploy to AWS EC2

#### Step 1: Launch EC2 Instance
1. Go to AWS EC2 Console
2. Launch a new instance:
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: t2.small or t2.medium (minimum)
   - **Security Group**: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
3. Download the `.pem` key file

#### Step 2: Connect to EC2
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

#### Step 3: Install Docker on EC2
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Logout and login again for group changes
exit
# SSH back in
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

#### Step 4: Upload Your Code to EC2
```bash
# On your local machine, from project directory
scp -i your-key.pem -r . ubuntu@YOUR_EC2_PUBLIC_IP:~/dharti-drishti/

# Or use git (recommended)
# On EC2:
git clone https://github.com/your-username/dharti-drishti.git
cd dharti-drishti
```

#### Step 5: Create .env File on EC2
```bash
# On EC2
cd ~/dharti-drishti
nano .env
# Paste your environment variables, then Ctrl+X, Y, Enter to save
```

#### Step 6: Build and Run Docker Container
```bash
# Build the image
docker build -t dharti-drishti:latest .

# Run the container on port 80 (standard HTTP port)
docker run -d \
  --name dharti-drishti-app \
  -p 80:5000 \
  --env-file .env \
  --restart unless-stopped \
  dharti-drishti:latest

# Check if running
docker ps
docker logs dharti-drishti-app
```

#### Step 7: Access Your Application

**Using Public IP:**
- Frontend: `http://YOUR_EC2_PUBLIC_IP/`
- API: `http://YOUR_EC2_PUBLIC_IP/api/health`

**Example with IP `54.123.45.67`:**
- Frontend: `http://54.123.45.67/`
- API: `http://54.123.45.67/api/analyze`

#### Step 8: (Optional) Setup Custom Domain

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. Add an A record pointing to your EC2 public IP
3. Your app will be available at: `http://yourdomain.com/`

#### Step 9: (Optional) Setup HTTPS with Let's Encrypt

```bash
# Install nginx
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/dharti-drishti
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/dharti-drishti /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Update Docker to run on port 5000 (nginx will handle port 80)
docker stop dharti-drishti-app
docker rm dharti-drishti-app
docker run -d \
  --name dharti-drishti-app \
  -p 5000:5000 \
  --env-file .env \
  --restart unless-stopped \
  dharti-drishti:latest

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**After HTTPS setup:**
- Frontend: `https://yourdomain.com/`
- API: `https://yourdomain.com/api/analyze`

#### Managing Your EC2 Deployment

**View logs:**
```bash
docker logs -f dharti-drishti-app
```

**Restart container:**
```bash
docker restart dharti-drishti-app
```

**Update application:**
```bash
cd ~/dharti-drishti
git pull  # or upload new files
docker stop dharti-drishti-app
docker rm dharti-drishti-app
docker build -t dharti-drishti:latest .
docker run -d --name dharti-drishti-app -p 80:5000 --env-file .env --restart unless-stopped dharti-drishti:latest
```

**Stop application:**
```bash
docker stop dharti-drishti-app
```

#### EC2 Cost Optimization
- Use t2.micro for testing (free tier eligible)
- Use t2.small/medium for production
- Stop instance when not in use to save costs
- Consider Reserved Instances for long-term use

### Option C: Deploy to AWS ECS

1. Install AWS CLI and authenticate
2. Create ECR repository:
```bash
aws ecr create-repository --repository-name dharti-drishti
```

3. Build and push:
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

docker tag dharti-drishti:latest YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/dharti-drishti:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/dharti-drishti:latest
```

4. Create ECS task definition and service through AWS Console or CLI

### Option C: Deploy to DigitalOcean App Platform

1. Push code to GitHub
2. Connect GitHub repo to DigitalOcean App Platform
3. Set environment variables in the dashboard
4. Deploy automatically

### Option D: Deploy to Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add environment variables:
```bash
railway variables set GOOGLE_API_KEY=your_key
railway variables set GROQ_API_KEY=your_key
# ... add all other variables
```

### Option E: Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render dashboard
3. Connect GitHub repository
4. Set environment variables in dashboard
5. Deploy automatically

## Docker Compose (Optional)

Create `docker-compose.yml` for easier management:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - ./storage_service:/app/storage_service
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Troubleshooting

### Container won't start
```bash
docker logs dharti-drishti-app
```

### Check container status
```bash
docker ps -a
```

### Access container shell
```bash
docker exec -it dharti-drishti-app /bin/bash
```

### Rebuild after code changes
```bash
docker build --no-cache -t dharti-drishti:latest .
```

## Security Best Practices

1. Never commit `.env` file to Git
2. Use secrets management in production (AWS Secrets Manager, Google Secret Manager)
3. Enable HTTPS in production
4. Use non-root user in container (add to Dockerfile if needed)
5. Regularly update base images and dependencies
6. Scan images for vulnerabilities:
```bash
docker scan dharti-drishti:latest
```

## Monitoring

### Check resource usage
```bash
docker stats dharti-drishti-app
```

### View real-time logs
```bash
docker logs -f dharti-drishti-app
```

## Scaling

For production, consider:
- Load balancer (nginx, AWS ALB, GCP Load Balancer)
- Multiple container instances
- Auto-scaling based on CPU/memory
- CDN for static assets
- Database for persistent storage

## Cost Optimization

- Use smaller base images (alpine)
- Multi-stage builds to reduce image size
- Clean up unused images: `docker system prune -a`
- Use cloud provider free tiers initially

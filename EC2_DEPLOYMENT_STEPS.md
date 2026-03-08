# EC2 Deployment - Step by Step Guide

## Prerequisites
- AWS Account
- Your project files ready
- .env file with all API keys

## Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Configure:
   - **Name**: dharti-drishti-server
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: t2.small (or t2.micro for testing)
   - **Key pair**: Create new key pair
     - Name: dharti-drishti-key
     - Type: RSA
     - Format: .pem
     - Download and save it safely!
   - **Network Settings**: 
     - Click "Edit"
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
     - Allow HTTPS (port 443) from anywhere (0.0.0.0/0)
   - **Storage**: 20 GB (default is fine)
3. Click "Launch Instance"
4. Wait for instance to start
5. Note down the **Public IPv4 address** (e.g., 54.123.45.67)

## Step 2: Connect to Your EC2 Instance

Open Terminal on your Mac and run:

```bash
# Move the key file to a safe location
mv ~/Downloads/dharti-drishti-key.pem ~/.ssh/

# Set correct permissions
chmod 400 ~/.ssh/dharti-drishti-key.pem

# Connect to EC2 (replace with your actual IP)
ssh -i ~/.ssh/dharti-drishti-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Example:
```bash
ssh -i ~/.ssh/dharti-drishti-key.pem ubuntu@54.123.45.67
```

Type "yes" when asked about fingerprint.

## Step 3: Install Docker on EC2

Once connected to EC2, run these commands:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install docker-compose (optional but useful)
sudo apt-get install -y docker-compose

# Verify installation
docker --version
```

**Important**: After adding user to docker group, logout and login again:
```bash
exit
# Then SSH back in
ssh -i ~/.ssh/dharti-drishti-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

## Step 4: Upload Your Project to EC2

### Option A: Using SCP (Copy files from your Mac)

Open a NEW terminal on your Mac (not the EC2 connection):

```bash
# Navigate to your project directory
cd ~/path/to/Dharti---Drishti

# Copy entire project to EC2
scp -i ~/.ssh/dharti-drishti-key.pem -r . ubuntu@YOUR_EC2_PUBLIC_IP:~/dharti-drishti/
```

This will take a few minutes to upload all files.

### Option B: Using Git (Recommended if you have GitHub)

On EC2:
```bash
# Install git if not installed
sudo apt-get install -y git

# Clone your repository
git clone https://github.com/your-username/your-repo.git dharti-drishti
cd dharti-drishti
```

## Step 5: Create .env File on EC2

On EC2:
```bash
cd ~/dharti-drishti

# Create .env file
nano .env
```

Copy and paste your environment variables:
```
GOOGLE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_key_here
# ... add all your other variables
```

Press `Ctrl + X`, then `Y`, then `Enter` to save.

## Step 6: Build and Run Docker Container

On EC2:
```bash
# Make sure you're in the project directory
cd ~/dharti-drishti

# Build the Docker image
docker build -t dharti-drishti:latest .

# Run the container (mapping port 80 to container's port 5000)
docker run -d \
  --name dharti-drishti-app \
  -p 80:5000 \
  --env-file .env \
  --restart unless-stopped \
  dharti-drishti:latest

# Check if it's running
docker ps

# View logs
docker logs dharti-drishti-app
```

## Step 7: Test Your Application

Open your browser and go to:
```
http://YOUR_EC2_PUBLIC_IP/
```

Example: `http://54.123.45.67/`

You should see your Dharti Drishti application!

Test the API:
```
http://YOUR_EC2_PUBLIC_IP/api/health
```

## Common Commands for Managing Your App

### View logs
```bash
docker logs -f dharti-drishti-app
```

### Restart the app
```bash
docker restart dharti-drishti-app
```

### Stop the app
```bash
docker stop dharti-drishti-app
```

### Update the app (after making changes)
```bash
cd ~/dharti-drishti

# If using git
git pull

# If using scp, upload new files from your Mac first

# Rebuild and restart
docker stop dharti-drishti-app
docker rm dharti-drishti-app
docker build -t dharti-drishti:latest .
docker run -d --name dharti-drishti-app -p 80:5000 --env-file .env --restart unless-stopped dharti-drishti:latest
```

### Check container status
```bash
docker ps -a
```

### Check system resources
```bash
docker stats dharti-drishti-app
```

## Troubleshooting

### Container won't start
```bash
docker logs dharti-drishti-app
```

### Can't access from browser
1. Check EC2 Security Group allows port 80
2. Check container is running: `docker ps`
3. Check logs: `docker logs dharti-drishti-app`

### Out of disk space
```bash
# Clean up unused Docker images
docker system prune -a
```

### Need to update .env variables
```bash
cd ~/dharti-drishti
nano .env
# Make changes, save
docker restart dharti-drishti-app
```

## Security Best Practices

1. **Restrict SSH access**: In EC2 Security Group, change SSH (port 22) to "My IP" instead of "Anywhere"
2. **Use HTTPS**: Follow the HTTPS setup in DEPLOYMENT.md for production
3. **Regular updates**: Keep your EC2 instance updated
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```
4. **Backup .env**: Keep a secure backup of your .env file
5. **Monitor costs**: Check AWS billing dashboard regularly

## Cost Estimation

- **t2.micro** (1 vCPU, 1GB RAM): ~$8-10/month (Free tier: 750 hours/month for 12 months)
- **t2.small** (1 vCPU, 2GB RAM): ~$17/month
- **t2.medium** (2 vCPU, 4GB RAM): ~$34/month

Stop instance when not in use to save costs!

## Next Steps (Optional)

1. **Setup custom domain**: Point your domain to EC2 IP
2. **Enable HTTPS**: Use Let's Encrypt (free SSL certificate)
3. **Setup monitoring**: Use CloudWatch for logs and metrics
4. **Auto-scaling**: Use AWS Auto Scaling for high traffic
5. **Load balancer**: Use AWS ELB for multiple instances

## Quick Reference

**Your EC2 Public IP**: _________________ (write it down!)

**SSH Command**:
```bash
ssh -i ~/.ssh/dharti-drishti-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**App URL**: http://YOUR_EC2_PUBLIC_IP/

**API URL**: http://YOUR_EC2_PUBLIC_IP/api/health

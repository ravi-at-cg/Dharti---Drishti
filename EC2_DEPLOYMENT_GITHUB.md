# EC2 Deployment via GitHub - Step by Step

## Overview
You'll push your code to GitHub from your current laptop, then pull it on EC2.

---

## Part 1: Push Code to GitHub (On Your Current Laptop)

### Step 1: Initialize Git (if not already done)
```bash
cd ~/path/to/Dharti---Drishti

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for deployment"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com
2. Click "New Repository"
3. Name: `dharti-drishti` (or any name you want)
4. Keep it **Private** (recommended since you have API keys)
5. Don't initialize with README
6. Click "Create Repository"

### Step 3: Push to GitHub
```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/dharti-drishti.git

# Push code
git branch -M main
git push -u origin main
```

**IMPORTANT**: Make sure `.env` is in `.gitignore` so your API keys are NOT uploaded!

Check `.gitignore` contains:
```
.env
```

---

## Part 2: Deploy on EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Configure:
   - **Name**: dharti-drishti-server
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: t2.small (recommended) or t2.micro (for testing)
   - **Key pair**: Create new key pair
     - Name: dharti-drishti-key
     - Type: RSA
     - Format: .pem
     - **Download and save it!**
   - **Network Settings** → Edit:
     - ✅ Allow SSH (port 22) - From "My IP"
     - ✅ Allow HTTP (port 80) - From "Anywhere" (0.0.0.0/0)
     - ✅ Allow HTTPS (port 443) - From "Anywhere" (0.0.0.0/0)
   - **Storage**: 20 GB
3. Click "Launch Instance"
4. **Note down the Public IPv4 address** (e.g., 54.123.45.67)

### Step 2: Connect to EC2

```bash
# Set correct permissions on key file
chmod 400 ~/Downloads/dharti-drishti-key.pem

# Connect (replace YOUR_EC2_IP with actual IP)
ssh -i ~/Downloads/dharti-drishti-key.pem ubuntu@YOUR_EC2_IP
```

Example:
```bash
ssh -i ~/Downloads/dharti-drishti-key.pem ubuntu@54.123.45.67
```

Type "yes" when asked about fingerprint.

### Step 3: Install Docker on EC2

Run these commands on EC2:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install git
sudo apt-get install -y git

# Verify Docker installation
docker --version
```

**Important**: Logout and login again for docker group to take effect:
```bash
exit
# SSH back in
ssh -i ~/Downloads/dharti-drishti-key.pem ubuntu@YOUR_EC2_IP
```

### Step 4: Clone Your Repository on EC2

```bash
# Clone your repository (replace with your GitHub URL)
git clone https://github.com/YOUR_USERNAME/dharti-drishti.git

# Enter the directory
cd dharti-drishti
```

**If repository is private**, you'll need to authenticate:

Option A - Use Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Copy the token
4. When cloning, use:
```bash
git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/dharti-drishti.git
```

Option B - Use SSH key (recommended):
```bash
# Generate SSH key on EC2
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter for all prompts

# Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this key

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Paste the key

# Clone using SSH
git clone git@github.com:YOUR_USERNAME/dharti-drishti.git
```

### Step 5: Create .env File on EC2

```bash
cd ~/dharti-drishti

# Create .env file
nano .env
```

Paste your environment variables:
```
GOOGLE_API_KEY=your_actual_key_here
GROQ_API_KEY=your_actual_key_here
AWS_ACCESS_KEY_ID=your_actual_key_here
AWS_SECRET_ACCESS_KEY=your_actual_key_here
ROBOFLOW_API_KEY=your_actual_key_here
# Add all your other variables
```

Press `Ctrl + X`, then `Y`, then `Enter` to save.

### Step 6: Deploy the Application

```bash
# Make deployment script executable
chmod +x deploy-to-ec2.sh

# Run deployment script
./deploy-to-ec2.sh
```

The script will:
- Build the Docker image
- Start the container
- Show you the URL to access your app

### Step 7: Access Your Application

Open browser and go to:
```
http://YOUR_EC2_IP/
```

Example: `http://54.123.45.67/`

Test API:
```
http://YOUR_EC2_IP/api/health
```

---

## Updating Your Application Later

### On Your Laptop (when you make changes):
```bash
git add .
git commit -m "Updated features"
git push
```

### On EC2 (to deploy updates):
```bash
cd ~/dharti-drishti

# Pull latest code
git pull

# Redeploy
./deploy-to-ec2.sh
```

---

## Useful Commands

### View application logs
```bash
docker logs -f dharti-drishti-app
```

### Restart application
```bash
docker restart dharti-drishti-app
```

### Stop application
```bash
docker stop dharti-drishti-app
```

### Check if running
```bash
docker ps
```

### Update environment variables
```bash
cd ~/dharti-drishti
nano .env
# Make changes
docker restart dharti-drishti-app
```

### Check system resources
```bash
docker stats dharti-drishti-app
```

### Clean up old Docker images
```bash
docker system prune -a
```

---

## Troubleshooting

### Can't access the app from browser
1. Check Security Group allows port 80
2. Check container is running: `docker ps`
3. Check logs: `docker logs dharti-drishti-app`
4. Try: `curl http://localhost/api/health` from EC2

### Git clone fails
- Check repository URL is correct
- For private repos, use personal access token or SSH key
- Make sure you have internet access on EC2

### Docker build fails
- Check logs for specific error
- Make sure all files were cloned properly: `ls -la`
- Check .env file exists: `cat .env`

### Out of memory
- Use larger instance type (t2.small or t2.medium)
- Check memory usage: `free -h`

---

## Security Checklist

✅ `.env` is in `.gitignore` (never commit API keys!)
✅ EC2 Security Group restricts SSH to your IP only
✅ Use strong passwords/keys
✅ Keep system updated: `sudo apt-get update && sudo apt-get upgrade`
✅ Consider setting up HTTPS for production

---

## Cost Estimate

- **t2.micro** (1GB RAM): ~$8-10/month (Free tier eligible)
- **t2.small** (2GB RAM): ~$17/month (Recommended)
- **t2.medium** (4GB RAM): ~$34/month

**Tip**: Stop instance when not in use to save money!

---

## Quick Reference

**GitHub Repository**: https://github.com/YOUR_USERNAME/dharti-drishti

**EC2 Public IP**: _________________ (write it here!)

**SSH Command**:
```bash
ssh -i ~/Downloads/dharti-drishti-key.pem ubuntu@YOUR_EC2_IP
```

**App URL**: http://YOUR_EC2_IP/

**Update Command** (on EC2):
```bash
cd ~/dharti-drishti && git pull && ./deploy-to-ec2.sh
```

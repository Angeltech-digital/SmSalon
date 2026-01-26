# Salon MVP - Deployment Guide

## Prerequisites
- DigitalOcean Account
- Domain name
- SSH key pair

## Step 1: Create DigitalOcean Droplet

1. Create a droplet with:
   - Ubuntu 22.04 LTS
   - 2GB RAM (minimum)
   - 50GB SSD

2. Choose your region (closest to your users)

## Step 2: Initial Server Setup

```bash
# SSH into droplet
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y python3.10 python3-pip python3-venv mysql-server nginx redis-server
apt install -y build-essential libmysqlclient-dev
```

## Step 3: Clone Repository

```bash
# Install git
apt install -y git

# Create app directory
mkdir -p /var/www/salon
cd /var/www/salon

# Clone your repository
git clone your-repo-url .
```

## Step 4: Setup Backend

```bash
cd Backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with production settings
nano .env
```

### Production .env Settings:
```
SECRET_KEY=your-very-long-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST_USER=your-salon-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Step 5: Setup Database

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE salon_db;
CREATE USER 'salon_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON salon_db.* TO 'salon_user'@'localhost';
FLUSH PRIVILEGES;
exit;
```

Update .env:
```
DB_ENGINE=django.db.backends.mysql
DB_NAME=salon_db
DB_USER=salon_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=3306
```

## Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Step 7: Setup Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/salon-gunicorn.service
```

Paste:
```ini
[Unit]
Description=Gunicorn application server for Salon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/salon/Backend
ExecStart=/var/www/salon/Backend/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/salon-gunicorn.sock \
    salon_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start salon-gunicorn
sudo systemctl enable salon-gunicorn
```

## Step 8: Setup Nginx

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/salon
```

Paste:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://unix:/run/salon-gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/salon/Backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/salon/Backend/media/;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/salon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 9: Setup SSL (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is enabled by default
sudo systemctl enable certbot.timer
```

## Step 10: Deploy Frontend

```bash
cd /var/www/salon/Frontend

# Create simple HTTP server or use Nginx to serve static files
# Add to Nginx config above:
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    root /var/www/salon/Frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://unix:/run/salon-gunicorn.sock;
    }
}
```

## Step 11: Setup Celery (Optional - for background tasks)

```bash
# Create Celery service
sudo nano /etc/systemd/system/salon-celery.service
```

Paste:
```ini
[Unit]
Description=Celery Service for Salon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/salon/Backend
ExecStart=/var/www/salon/Backend/venv/bin/celery \
    -A salon_project \
    worker \
    -l info

[Install]
WantedBy=multi-user.target
```

## Step 12: Monitoring & Logs

```bash
# View Gunicorn logs
sudo journalctl -u salon-gunicorn -f

# View Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# View Django logs
tail -f /var/www/salon/Backend/logs/salon.log
```

## Step 13: Backup Strategy

```bash
# Create backup script
sudo nano /var/www/salon/backup.sh
```

Paste:
```bash
#!/bin/bash
BACKUP_DIR="/backups/salon"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="salon_db"
DB_USER="salon_user"

mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u $DB_USER -p salon_db > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/salon/Backend/media/

echo "Backup completed: $DATE"
```

Schedule with cron:
```bash
sudo crontab -e
# Add: 0 2 * * * /var/www/salon/backup.sh
```

## Maintenance Commands

```bash
# Update code
cd /var/www/salon
git pull origin main
cd Backend

# Restart services
sudo systemctl restart salon-gunicorn
sudo systemctl restart nginx

# Run migrations after code update
python manage.py migrate
```

## Security Checklist

- ✅ Set SECRET_KEY to a random string
- ✅ Set DEBUG=False in production
- ✅ Use environment variables for sensitive data
- ✅ Enable SSL/HTTPS
- ✅ Configure ALLOWED_HOSTS
- ✅ Setup firewall (ufw)
- ✅ Regular backups
- ✅ Monitor logs
- ✅ Update dependencies regularly

---

**Need help?** Contact your hosting provider or refer to Django/DigitalOcean documentation.

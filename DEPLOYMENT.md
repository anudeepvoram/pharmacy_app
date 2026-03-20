# 🚀 Production Deployment Guide

## Pharmacy Management System - Production Ready

This guide covers deploying the Pharmacy Management System in a production environment.

---

## Pre-Deployment Checklist

- [ ] Update credentials in `config.py`
- [ ] Set up environment variables
- [ ] Configure database backups
- [ ] Set up SSL/TLS certificates
- [ ] Create user accounts for all staff
- [ ] Test all modules thoroughly
- [ ] Back up existing data
- [ ] Document custom configurations

---

## Security Hardening

### 1. Authentication

**Update credentials immediately:**
```python
# config.py
DEFAULT_USERNAME = "your_secure_username"
DEFAULT_PASSWORD = "your_secure_password_here"
```

**Recommended**: Implement LDAP or OAuth2 integration for enterprise authentication.

### 2. Environment Variables

Create `.env` file (add to .gitignore):
```
DATABASE_URL=sqlite:///pharmacy.db
SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
MAX_LOGIN_ATTEMPTS=5
SESSION_TIMEOUT=1800
```

### 3. Database Security

```bash
# Restrict database file permissions
chmod 600 pharmacy.db
chmod 700 database/

# Regular backups
0 2 * * * /path/to/backup_script.sh
```

### 4. HTTPS Configuration

Create `streamlit_config.toml`:
```toml
[server]
port = 8501
ssl_keyfile = "/path/to/key.pem"
ssl_certfile = "/path/to/cert.pem"
headerConfigs = {"Access-Control-Allow-Origin": "https://yourdomain.com"}

[client]
showErrorDetails = false
toolbarMode = "minimal"

[logger]
level = "info"
```

---

## Deployment Options

### Option 1: Self-Hosted (Linux/Ubuntu)

#### Using Systemd Service

Create `/etc/systemd/system/pharmacy-app.service`:
```ini
[Unit]
Description=Pharmacy Management System
After=network.target

[Service]
Type=simple
User=pharmacy
WorkingDirectory=/opt/pharmacy_app
Environment="PATH=/opt/pharmacy_app/venv/bin"
ExecStart=/opt/pharmacy_app/venv/bin/streamlit run app.py --server.port 8501 --logger.level=warning
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable pharmacy-app
sudo systemctl start pharmacy-app
sudo systemctl status pharmacy-app
```

#### Using Nginx Reverse Proxy

Create `/etc/nginx/sites-available/pharmacy`:
```nginx
upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name pharmacy.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name pharmacy.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/pharmacy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create database
RUN python database/db.py

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  pharmacy-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./pharmacy.db:/app/pharmacy.db
      - ./bills:/app/bills
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - pharmacy-net

networks:
  pharmacy-net:
    driver: bridge
```

**Deploy:**
```bash
docker-compose up -d
docker-compose logs -f
```

### Option 3: Cloud Platforms

#### Streamlit Cloud (Easiest)
```bash
# Push to GitHub first
git push origin main

# Then deploy on https://streamlit.io/cloud
```

#### AWS EC2
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect via SSH
# Follow self-hosted Linux guide above
```

#### Google Cloud Run
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && python database/db.py
EXPOSE 8080
ENV PORT=8080
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
```

```bash
gcloud run deploy pharmacy-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Database Management

### Automated Backup Script

Create `backup_db.sh`:
```bash
#!/bin/bash

BACKUP_DIR="/backups/pharmacy_db"
DATE=$(date +%Y%m%d_%H%M%S)
SOURCE_DB="/opt/pharmacy_app/pharmacy.db"
BACKUP_FILE="$BACKUP_DIR/pharmacy_db_$DATE.db"

# Create backup
cp "$SOURCE_DB" "$BACKUP_FILE"

# Compress
gzip "$BACKUP_FILE"

# Keep only last 30 days
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

# Send alert if backup fails
if [ $? -ne 0 ]; then
    echo "Backup failed!" | mail -s "Pharmacy DB Backup Failed" admin@example.com
fi

echo "Backup completed: $BACKUP_FILE.gz" >> /var/log/pharmacy_backup.log
```

**Schedule with cron:**
```bash
# Run daily at 2 AM
0 2 * * * /opt/pharmacy_app/backup_db.sh
```

### Database Maintenance

```bash
# Optimize database
sqlite3 pharmacy.db "VACUUM;"

# Check integrity
sqlite3 pharmacy.db "PRAGMA integrity_check;"

# Analyze for query optimization
sqlite3 pharmacy.db "ANALYZE;"
```

---

## Monitoring & Logging

### Application Logs

Create `logging_config.py`:
```python
import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger("pharmacy_app")
    logger.setLevel(logging.INFO)
    
    # File handler
    handler = logging.handlers.RotatingFileHandler(
        '/var/log/pharmacy_app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### Health Monitoring

```bash
# Monitor application status
watch -n 5 'ps aux | grep streamlit'

# Check system resources
htop

# Monitor database size
du -h pharmacy.db
```

### Alerts Setup

Create monitoring alerts for:
- Application crashes
- High CPU/Memory usage
- Database size threshold
- Backup failures
- Login attempts (brute force)

---

## Performance Optimization

### Database Indexes

```python
# database/db.py - add to create_tables()
def create_indexes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_medicines_name ON medicines(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bills_customer ON bills(customer_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bills_date ON bills(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bill_items_bill ON bill_items(bill_id)")
    
    conn.commit()
    conn.close()
```

### Caching Strategy

For high-traffic scenarios, add Redis:
```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

# Cache dashboard metrics for 5 minutes
def get_cached_metrics():
    cached = cache.get('dashboard_metrics')
    if cached:
        return json.loads(cached)
    # Fetch from DB and cache
```

---

## User Management

### Create System User

```bash
# Create dedicated user
sudo useradd -m -s /bin/bash pharmacy

# Set permissions
sudo chown -R pharmacy:pharmacy /opt/pharmacy_app
sudo chmod 700 /opt/pharmacy_app/pharmacy.db
```

### Role-Based Access (Future Enhancement)

```python
# config.py additions
ROLES = {
    'admin': ['view_all', 'create', 'edit', 'delete', 'reports'],
    'pharmacist': ['view_all', 'create', 'edit', 'reports'],
    'cashier': ['view_medicines', 'create_bills'],
    'viewer': ['view_all']
}
```

---

## Disaster Recovery

### Recovery Procedure

1. **Database Corruption:**
   ```bash
   # Restore from backup
   cp /backups/pharmacy_db/pharmacy_db_YYYYMMDD.db.gz .
   gunzip pharmacy_db_YYYYMMDD.db.gz
   mv pharmacy_db_YYYYMMDD.db pharmacy.db
   ```

2. **Application Crash:**
   ```bash
   # Check logs
   tail -f /var/log/pharmacy_app.log
   
   # Restart service
   sudo systemctl restart pharmacy-app
   ```

3. **Data Loss:**
   - Restore from latest backup
   - Contact backup provider if using cloud storage

---

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Database Backup | Daily | `backup_db.sh` |
| Database Optimization | Weekly | `VACUUM; ANALYZE;` |
| Log Rotation | Monthly | Automated |
| Security Updates | As needed | `pip install --upgrade` |
| Full System Audit | Quarterly | Manual review |

---

## Compliance & Regulations

### Data Protection
- GDPR compliance for EU customers
- CCPA compliance for California
- Implement data encryption at rest
- Regular security audits

### Healthcare Compliance (if applicable)
- HIPAA compliance (for health data)
- Medical device compliance
- Regulatory documentation

---

## Support & Maintenance Contacts

**Technical Support:**
- Email: support@example.com
- Phone: +1-XXX-XXX-XXXX

**Emergency Contacts:**
- On-call: escalation@example.com
- Status Page: status.example.com

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Maintained By**: Development Team
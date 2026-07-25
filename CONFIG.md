# Configuration Guide

## Environment Variables

All configuration is done through environment variables in `.env` file.

### Discord Configuration

```env
# Bot token from Discord Developer Portal (REQUIRED)
DISCORD_TOKEN=your_bot_token_here

# Your Discord user ID (REQUIRED)
BOT_OWNER_ID=123456789

# Role IDs for admin and premium users (optional)
BOT_ADMIN_ROLE_ID=admin_role_id
BOT_PREMIUM_ROLE_ID=premium_role_id

# Command prefix (default: /)
DISCORD_PREFIX=/
```

### Processing Configuration

```env
# Maximum jobs allowed in queue (default: 500)
MAX_QUEUE_SIZE=500

# Maximum concurrent job processing (default: 10)
MAX_CONCURRENT_JOBS=10

# Maximum file size in MB (default: 25)
MAX_FILE_SIZE_MB=25

# Job timeout in seconds (default: 300)
JOB_TIMEOUT_SECONDS=300

# Cleanup interval in seconds (default: 3600)
CLEANUP_INTERVAL_SECONDS=3600
```

### Obfuscation Configuration

```env
# Default obfuscation level 1-10 (default: 5)
DEFAULT_OBFUSCATION_LEVEL=5

# Maximum obfuscation level allowed (default: 10)
MAX_OBFUSCATION_LEVEL=10
```

### Rate Limiting

```env
# Free user: requests per window (default: 10)
RATE_LIMIT_REQUESTS=10

# Time window in seconds (default: 3600 = 1 hour)
RATE_LIMIT_WINDOW_SECONDS=3600

# Premium user: requests per window (default: 50)
PREMIUM_RATE_LIMIT_REQUESTS=50
```

### Database Configuration

```env
# SQLite (default)
DATABASE_URL=sqlite:///./obfbot.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/obfbot

# Echo SQL queries (debug only)
SQLALCHEMY_ECHO=false
```

### Logging Configuration

```env
# Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
LOG_LEVEL=INFO

# Log file path (default: logs/obfbot.log)
LOG_FILE=logs/obfbot.log
```

### Storage Configuration

```env
# Temporary files directory (default: ./temp)
TEMP_DIR=./temp

# Output files directory (default: ./output)
OUTPUT_DIR=./output

# Backup directory (default: ./backups)
BACKUP_DIR=./backups
```

### API Configuration (Future)

```env
# API host (default: 0.0.0.0)
API_HOST=0.0.0.0

# API port (default: 8000)
API_PORT=8000

# Enable API (default: false)
API_ENABLED=false
```

## Advanced Configuration

### Production Settings

```env
# Use PostgreSQL
DATABASE_URL=postgresql://obfbot:secure_password@db.example.com/obfbot

# Higher limits
MAX_QUEUE_SIZE=1000
MAX_CONCURRENT_JOBS=20

# Strict rate limiting
RATE_LIMIT_REQUESTS=5
PREMIUM_RATE_LIMIT_REQUESTS=25

# Logging
LOG_LEVEL=WARNING
```

### Development Settings

```env
# Debug logging
LOG_LEVEL=DEBUG
SQLALCHEMY_ECHO=true

# Lower limits for testing
MAX_QUEUE_SIZE=10
MAX_CONCURRENT_JOBS=2

# Relaxed rate limiting
RATE_LIMIT_REQUESTS=100
```

### High Performance Settings

```env
# Increase concurrency
MAX_QUEUE_SIZE=2000
MAX_CONCURRENT_JOBS=50

# Larger file size
MAX_FILE_SIZE_MB=100

# Longer timeout for large files
JOB_TIMEOUT_SECONDS=600

# Use PostgreSQL for better concurrency
DATABASE_URL=postgresql://...
```

## Per-User Obfuscation Settings

Users can customize obfuscation behavior (stored in database):

- **Obfuscation Level** (1-10) - Controls protection intensity
- **Rename Variables** (true/false) - Enable variable renaming
- **Encrypt Strings** (true/false) - Enable string encryption
- **Encode Constants** (true/false) - Enable number encoding
- **Flatten Control Flow** (true/false) - Enable control flow flattening
- **Dead Code Amount** (0-10) - Amount of dead code to insert
- **Runtime Size** (small/medium/large) - Size of runtime support code
- **Anti-Tamper** (true/false) - Enable integrity checks
- **Anti-Debug** (true/false) - Enable debug detection
- **Output Formatting** (minified/formatted) - Code formatting
- **Compression** (true/false) - Compress output

## Environment-Specific Configuration

### Docker

Pass environment variables when running:

```bash
docker run -e DISCORD_TOKEN=token -e LOG_LEVEL=WARNING obfbot
```

Or create `.env` file and reference it:

```bash
docker run --env-file .env obfbot
```

### Kubernetes

Create ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: obfbot-config
data:
  DISCORD_TOKEN: "your_token"
  LOG_LEVEL: "INFO"
  DATABASE_URL: "postgresql://..."
```

## Validation

The bot validates configuration on startup:

```
ERROR: DISCORD_TOKEN is not set
ERROR: BOT_OWNER_ID is not set
```

All required variables must be set or the bot will exit.

## Monitoring Configuration

Check if configuration is correct:

```bash
# View logs
tail -f logs/obfbot.log

# Check startup
python -m bot.bot
```

Successful startup log:
```
2026-07-25 13:30:00 - obfbot - INFO - Bot logged in as ObfBot#1234
2026-07-25 13:30:01 - obfbot - INFO - Database initialized successfully
2026-07-25 13:30:02 - obfbot - INFO - Worker started (total: 1/10)
```

## Performance Tuning

### For High Load

1. Increase concurrency:
   ```env
   MAX_CONCURRENT_JOBS=50
   MAX_QUEUE_SIZE=2000
   ```

2. Use PostgreSQL instead of SQLite:
   ```env
   DATABASE_URL=postgresql://...
   ```

3. Increase timeouts:
   ```env
   JOB_TIMEOUT_SECONDS=600
   ```

### For Low Resource Usage

1. Decrease concurrency:
   ```env
   MAX_CONCURRENT_JOBS=2
   MAX_QUEUE_SIZE=50
   ```

2. Increase timeout between cleanup:
   ```env
   CLEANUP_INTERVAL_SECONDS=7200
   ```

3. Use SQLite:
   ```env
   DATABASE_URL=sqlite:///./obfbot.db
   ```

## Security Recommendations

1. **Never commit `.env` to version control**
   ```bash
   echo .env >> .gitignore
   ```

2. **Use strong database password** (PostgreSQL)

3. **Restrict file permissions**
   ```bash
   chmod 600 .env
   ```

4. **Use environment variables in production**
   - Don't store sensitive data in code
   - Use secrets management (Kubernetes, AWS Secrets, etc.)

5. **Enable logging**
   ```env
   LOG_LEVEL=WARNING
   ```

6. **Implement rate limiting**
   ```env
   RATE_LIMIT_REQUESTS=5
   ```

## Getting Help

For configuration issues:
1. Check logs: `logs/obfbot.log`
2. Review this guide
3. Check [GitHub Issues](https://github.com/nevawork/obfbot/issues)
4. Join support Discord

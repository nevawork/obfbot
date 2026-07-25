# Installation Guide

## Prerequisites

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **Discord Bot Token** - [Create Bot](https://discord.com/developers/applications)
- **Optional: PostgreSQL** - For production use

## Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your application "ObfBot"
4. Go to "Bot" section and click "Add Bot"
5. Under TOKEN, click "Copy" to copy your bot token
6. Save the token somewhere safe

## Step 2: Set Bot Permissions

1. In Developer Portal, go to OAuth2 → URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - `Send Messages`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
4. Copy the generated URL
5. Open the URL in your browser to invite the bot to your server

## Step 3: Clone Repository

```bash
git clone https://github.com/nevawork/obfbot.git
cd obfbot
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Configure Environment

1. Copy the example config:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```bash
nano .env
```

3. Set your configuration:
```env
# Required
DISCORD_TOKEN=your_bot_token_here
BOT_OWNER_ID=your_discord_user_id

# Optional
BOT_ADMIN_ROLE_ID=admin_role_id
BOT_PREMIUM_ROLE_ID=premium_role_id

# Processing settings
MAX_CONCURRENT_JOBS=10
MAX_FILE_SIZE_MB=25
JOB_TIMEOUT_SECONDS=300

# Rate limiting
RATE_LIMIT_REQUESTS=10
PREMIUM_RATE_LIMIT_REQUESTS=50
```

## Step 6: Initialize Database

The database is automatically initialized on first run. For production, you can use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/obfbot
```

## Step 7: Run the Bot

```bash
python -m bot.bot
```

You should see:
```
2026-07-25 13:30:00 - obfbot - INFO - Bot logged in as ObfBot#1234
2026-07-25 13:30:01 - obfbot - INFO - Guild count: 1
2026-07-25 13:30:02 - obfbot - INFO - Worker started (total: 10)
```

## Step 8: Test the Bot

1. In your Discord server, type `/help`
2. You should see the help menu
3. Try `/obfuscate` with a small Lua file

## Docker Installation

### Prerequisites
- Docker
- Docker Compose (optional)

### Quick Start

```bash
# Build image
docker build -t obfbot .

# Run container
docker run -e DISCORD_TOKEN=your_token obfbot
```

### With Docker Compose

1. Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      DISCORD_TOKEN: ${DISCORD_TOKEN}
      DATABASE_URL: postgresql://obfbot:password@db:5432/obfbot
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: obfbot
      POSTGRES_PASSWORD: password
      POSTGRES_DB: obfbot
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

2. Run:
```bash
docker-compose up
```

## Troubleshooting

### Bot Not Responding

1. Check if token is correct in `.env`
2. Verify bot is invited to server
3. Check bot has necessary permissions
4. Check logs for errors

### Database Errors

```bash
# Reset database (SQLite)
rm obfbot.db
python -m bot.bot
```

### Permission Errors

- Make sure bot role is above user roles
- Check server permissions for the bot
- Verify admin/premium role IDs in `.env`

### File Upload Issues

- Check max file size in config
- Ensure `/tmp` and `/output` directories have write permissions
- Verify enough disk space available

## Production Deployment

### Using systemd (Linux)

1. Create `/etc/systemd/system/obfbot.service`:
```ini
[Unit]
Description=ObfBot Discord Obfuscator
After=network.target

[Service]
Type=simple
User=obfbot
WorkingDirectory=/home/obfbot/obfbot
EnvironmentFile=/home/obfbot/obfbot/.env
ExecStart=/home/obfbot/obfbot/venv/bin/python -m bot.bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable obfbot
sudo systemctl start obfbot
```

### Using PM2 (Node.js-like process manager)

```bash
npm install -g pm2
pm2 start "python -m bot.bot" --name obfbot
pm2 startup
pm2 save
```

### Using Systemd with PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Start bot
sudo systemctl start obfbot
```

## Next Steps

- Read [CONFIG.md](./CONFIG.md) for detailed configuration
- Check [DOCKER.md](./DOCKER.md) for Docker specifics
- Review [API.md](./API.md) for programmatic usage
- Join [Support Server](https://discord.gg/example) for help

## Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [GitHub Issues](https://github.com/nevawork/obfbot/issues)
3. Join support Discord for help

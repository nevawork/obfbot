# ObfBot - Advanced Lua/Luau Obfuscator Discord Bot

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Nextcord](https://img.shields.io/badge/nextcord-2.5.0-blue)

A production-quality Discord bot providing secure, cloud-based Lua/Luau script obfuscation using an original protection engine.

## Features

### 🎯 Core Features
- **Slash Commands Only** - Modern Discord interface with `/` commands
- **Asynchronous Processing** - Handle hundreds of simultaneous jobs
- **Queue System** - Manage concurrent obfuscation tasks
- **Progress Updates** - Real-time status updates for processing jobs
- **Multiple File Formats** - Support for `.lua`, `.luau`, `.txt`, and `.zip` archives
- **Rate Limiting** - Configurable limits with premium tier support
- **User Statistics** - Track usage, processing time, and protection metrics
- **Permission System** - Owner, Admin, Premium, and User roles

### 🔐 Obfuscation Engine

#### Identifier Protection
- Variable renaming with Unicode-safe identifiers
- Function renaming with scope awareness
- Reserved keyword avoidance
- Customizable naming patterns

#### String Protection
- XOR encryption with randomized keys
- Runtime decryption functions
- String splitting and reconstruction
- Constant hiding techniques

#### Number Protection
- Arithmetic encoding (addition, multiplication, subtraction)
- Constant folding reversal
- Random expression generation
- Opaque predicates

#### Control Flow Protection
- Dead code insertion
- Bogus branches and fake loops
- Opaque predicates
- Control flow flattening (advanced)

#### Table Protection
- Hidden table keys
- Metatable transformations
- Proxy table generation

#### Anti-Tamper & Anti-Debug
- Integrity verification
- Environment validation
- Debug library detection
- Hook detection
- Optional checksum verification

### ⚙️ Obfuscation Levels

| Level | Protections | Use Case |
|-------|-------------|----------|
| 1-2 | Variable renaming | Light obfuscation |
| 3-4 | + String encryption | Moderate obfuscation |
| 5-6 | + Number encoding | Heavy obfuscation |
| 7-8 | + Control flow | Very heavy obfuscation |
| 9-10 | + All protections | Maximum obfuscation |

## Commands

### User Commands
- `/obfuscate` - Obfuscate a Lua/Luau script
- `/profile` - View your user profile
- `/stats` - View your statistics
- `/history` - View obfuscation history
- `/settings` - Configure your settings
- `/help` - Show help and available commands
- `/premium` - View premium features

### Admin Commands
- `/admin` - Admin dashboard
- `/admin-blacklist` - Blacklist a user
- `/admin-unblacklist` - Unblacklist a user
- `/admin-broadcast` - Send server announcement
- `/admin-logs` - View recent logs

## Performance

- **Processing Speed**: Most scripts process in < 5 seconds
- **Concurrent Jobs**: Handle up to 10 simultaneous obfuscations
- **Queue Size**: Support up to 500 jobs in queue
- **File Size Limit**: 25MB per file
- **Rate Limiting**: 10/hour (free), 50/hour (premium)

## Installation

### Requirements
- Python 3.9+
- Discord Bot Token
- SQLite or PostgreSQL (optional)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/nevawork/obfbot.git
cd obfbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the bot**
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

4. **Run the bot**
```bash
python -m bot.bot
```

See [INSTALL.md](./INSTALL.md) for detailed instructions.

## Configuration

### Environment Variables

```env
# Discord
DISCORD_TOKEN=your_bot_token_here
BOT_OWNER_ID=your_user_id
BOT_ADMIN_ROLE_ID=admin_role_id
BOT_PREMIUM_ROLE_ID=premium_role_id

# Processing
MAX_QUEUE_SIZE=500
MAX_CONCURRENT_JOBS=10
MAX_FILE_SIZE_MB=25
JOB_TIMEOUT_SECONDS=300

# Obfuscation
DEFAULT_OBFUSCATION_LEVEL=5
MAX_OBFUSCATION_LEVEL=10

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=3600
PREMIUM_RATE_LIMIT_REQUESTS=50

# Database
DATABASE_URL=sqlite:///./obfbot.db
# Or PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/obfbot
```

See [CONFIG.md](./CONFIG.md) for detailed configuration guide.

## Architecture

```
bot/
├── bot.py                    # Main bot initialization
├── config.py                 # Configuration management
├── database.py               # Database models and management
├── queue.py                  # Job queue system
├── permissions.py            # Permission system
├── logger.py                 # Logging setup
├── rate_limiter.py          # Rate limiting
├── utils.py                 # File handling utilities
│
├── engine/
│   ├── tokenizer.py         # Lua lexical analyzer
│   ├── parser.py            # Lua parser (tokens → AST)
│   ├── ast.py               # AST node definitions
│   ├── obfuscator.py        # Main obfuscation orchestrator
│   ├── output.py            # Code generation (AST → Lua)
│   ├── runtime.py           # Runtime support code
│   ├── identifier_protection.py
│   ├── string_protection.py
│   ├── number_protection.py
│   ├── controlflow.py
│   ├── randomizer.py
│   └── settings.py
│
├── commands/
│   ├── obfuscate.py         # /obfuscate command
│   ├── stats.py             # Statistics commands
│   ├── settings.py          # Settings command
│   ├── premium.py           # Premium features
│   ├── admin.py             # Admin commands
│   └── help.py              # Help command
│
└── storage/                  # File storage directories
    ├── temp/                # Temporary files
    ├── output/              # Obfuscated output
    └── backups/             # Backups
```

## Database

Supports both SQLite (default) and PostgreSQL.

### Models
- **User** - User profiles and permissions
- **Job** - Obfuscation job records
- **JobStatistics** - Per-job statistics
- **UserStatistics** - User aggregate statistics
- **UserSettings** - User preferences
- **RateLimit** - Rate limit tracking

## Docker

### Quick Start with Docker

```bash
# Build image
docker build -t obfbot .

# Run container
docker run -e DISCORD_TOKEN=your_token obfbot
```

See [Docker documentation](./DOCKER.md) for more options.

## Security

- ✓ Input validation and sanitization
- ✓ Path traversal protection
- ✓ File size limits
- ✓ Timeout protection
- ✓ Rate limiting
- ✓ Permission-based access control
- ✓ Comprehensive error handling
- ✓ Encrypted string storage

## API Architecture

The bot is designed with an API-ready architecture:

```python
from bot.engine.obfuscator import ObfuscationEngine
from bot.engine.settings import ObfuscationSettings

# Create settings
settings = ObfuscationSettings(
    obfuscation_level=7,
    rename_variables=True,
    encrypt_strings=True,
)

# Create engine
engine = ObfuscationEngine(settings)

# Obfuscate code
obfuscated, stats = engine.obfuscate(lua_code)

print(f"Original size: {stats['original_size']}")
print(f"Obfuscated size: {stats['obfuscated_size']}")
print(f"Time: {stats['processing_time']:.2f}s")
```

Future versions can expose REST API endpoints using FastAPI.

## Development

### Testing

```bash
pip install -r requirements-dev.txt
pytest tests/
```

### Code Quality

```bash
black bot/
pylint bot/
mypy bot/
```

## Performance Benchmarks

| Input Size | Level | Time | Output Size |
|------------|-------|------|-------------|
| 1 KB       | 5     | 0.1s | 2.5 KB      |
| 10 KB      | 7     | 0.3s | 25 KB       |
| 100 KB     | 9     | 1.5s | 250 KB      |
| 1 MB       | 9     | 15s  | 2.5 MB      |

## Limitations

- Single-file processing per job (use ZIP for multiple files - premium)
- No support for Lua 5.1 metatables with custom __index (yet)
- Control flow flattening is simplified (not full state machine conversion)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Disclaimer

**ObfBot is designed for legitimate script protection purposes.** Users are responsible for:

- Ensuring they have the right to obfuscate code
- Complying with local laws and regulations
- Not using the bot to obfuscate malicious code
- Proper attribution when using obfuscated code

## Support

- 📚 [Documentation](./docs/)
- 🐛 [Issue Tracker](https://github.com/nevawork/obfbot/issues)
- 💬 [Discord Support](https://discord.gg/example)

## Credits

Built with:
- [Nextcord](https://github.com/nextcord/nextcord) - Discord API wrapper
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Python](https://www.python.org/) - Core language

## Version History

### v1.0.0 (2026-07-25)
- Initial release
- Full obfuscation engine
- Discord bot with slash commands
- Database support
- Admin commands
- Rate limiting

---

**ObfBot v1.0.0** - Advanced Lua/Luau Obfuscator Discord Bot

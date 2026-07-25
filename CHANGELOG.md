# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-25

### Added
- Initial release
- Complete Lua/Luau obfuscation engine
- Identifier protection (variable/function renaming)
- String protection (XOR encryption)
- Number protection (arithmetic encoding)
- Control flow protection (dead code, opaque predicates)
- Anti-debug and anti-tamper features
- Discord bot with slash commands
- Job queue system with concurrent processing
- Database models for users, jobs, statistics
- Rate limiting (free and premium tiers)
- Permission system (owner, admin, premium, user)
- Admin commands (blacklist, broadcast, logs)
- User statistics and history tracking
- File handling (drag-and-drop, ZIP support)
- Docker and Docker Compose support
- Comprehensive documentation
- SQLite and PostgreSQL support

### Features
- 10 obfuscation levels
- Support for .lua, .luau, .txt files
- ZIP archive support (premium)
- Up to 10 concurrent jobs
- Queue support for 500 jobs
- Processing statistics
- User profiles and settings

### Security
- Input validation and sanitization
- Rate limiting
- Permission-based access control
- Timeout protection
- File size limits
- Path traversal protection

## [Unreleased]

### Planned
- REST API endpoints
- Web dashboard
- WebSocket support
- Advanced control flow flattening
- Metatable transformations
- Lua 5.1 compatibility improvements
- Performance optimizations
- Multi-language support
- Custom obfuscation profiles
- Batch processing
- Premium tier features expansion
- Database query optimization
- Caching system
- Webhook notifications

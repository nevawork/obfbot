"""Main Discord bot."""

import asyncio
from nextcord.ext import commands, tasks
from nextcord import Intents, Status, Activity, ActivityType
from bot.config import config
from bot.database import db_manager
from bot.queue import JobQueue
from bot.logger import logger
from bot.engine.obfuscator import ObfuscationEngine
from bot.engine.settings import ObfuscationSettings


class ObfBot(commands.Bot):
    """Advanced Lua/Luau Obfuscator Discord Bot."""

    def __init__(self):
        """Initialize bot."""
        intents = Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=config.DISCORD_PREFIX,
            intents=intents,
            help_command=None,
        )

        # Initialize subsystems
        self.job_queue = JobQueue(
            max_queue_size=config.MAX_QUEUE_SIZE,
            max_concurrent=config.MAX_CONCURRENT_JOBS,
        )
        self.obfuscation_engine = ObfuscationEngine()
        self.cleanup_task = None

    async def on_ready(self) -> None:
        """Bot ready event."""
        logger.info(f"Bot logged in as {self.user}")
        logger.info(f"Guild count: {len(self.guilds)}")

        # Set status
        activity = Activity(
            type=ActivityType.watching,
            name="/help for commands",
        )
        await self.change_presence(status=Status.online, activity=activity)

        # Start job processing
        asyncio.create_task(self.job_queue.process_jobs(self._process_obfuscation_job))

        # Start cleanup task
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _process_obfuscation_job(self, job) -> bytes:
        """Process obfuscation job.

        Args:
            job: Job object

        Returns:
            Obfuscated code as bytes
        """
        try:
            # Decode input
            code = job.input_data.decode("utf-8")

            # Create settings from job settings
            settings = ObfuscationSettings(**job.settings)
            engine = ObfuscationEngine(settings)

            # Obfuscate
            obfuscated, stats = engine.obfuscate(code)

            # Update job with stats
            job.metadata = stats
            job.progress = 100

            logger.info(f"Job {job.job_id} processed successfully")
            return obfuscated.encode("utf-8")

        except Exception as e:
            logger.error(f"Job {job.job_id} failed: {e}")
            job.error = str(e)
            raise

    async def _cleanup_loop(self) -> None:
        """Periodic cleanup of old jobs."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await asyncio.sleep(config.CLEANUP_INTERVAL_SECONDS)
                await self.job_queue.cleanup_old_jobs(max_age_hours=24)
                logger.info("Cleanup task completed")
            except Exception as e:
                logger.error(f"Cleanup task failed: {e}")

    async def load_commands(self) -> None:
        """Load command cogs."""
        commands_dir = "bot/commands"
        for file in [
            "obfuscate.py",
            "stats.py",
            "settings.py",
            "premium.py",
            "admin.py",
            "help.py",
        ]:
            try:
                await self.load_extension(f"bot.commands.{file[:-3]}")
                logger.info(f"Loaded command: {file}")
            except Exception as e:
                logger.error(f"Failed to load command {file}: {e}")

    async def shutdown(self) -> None:
        """Shutdown bot."""
        logger.info("Shutting down bot...")
        await self.job_queue.shutdown()
        db_manager.close()
        await super().close()


async def main() -> None:
    """Main entry point."""
    # Validate configuration
    config.validate()

    # Initialize directories
    config.init_directories()

    # Initialize database
    db_manager.init_db()

    # Create bot
    bot = ObfBot()

    # Load commands
    await bot.load_commands()

    # Start bot
    try:
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        await bot.shutdown()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

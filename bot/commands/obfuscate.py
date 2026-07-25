"""Obfuscate command."""

import uuid
from typing import Optional
import nextcord
from nextcord.ext import commands
from bot.queue import Job, JobStatus
from bot.logger import logger
from bot.utils import FileHandler
from bot.rate_limiter import rate_limiter
from bot.permissions import permission_manager
from bot.config import config


class ObfuscateCommand(commands.Cog):
    """Obfuscate command cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot

    @nextcord.slash_command(
        name="obfuscate",
        description="Obfuscate a Lua/Luau script",
        guild_ids=None,  # Global command
    )
    async def obfuscate(
        self,
        interaction: nextcord.Interaction,
        script: Optional[nextcord.Attachment] = nextcord.SlashCommandOption(
            description="Lua script file (.lua, .luau, .txt, or .zip)",
            required=False,
        ),
        level: Optional[int] = nextcord.SlashCommandOption(
            description="Obfuscation level (1-10)",
            min_value=1,
            max_value=10,
            required=False,
            default=5,
        ),
    ) -> None:
        """Obfuscate command.

        Args:
            interaction: Discord interaction
            script: Script file
            level: Obfuscation level
        """
        # Defer response
        await interaction.response.defer(ephemeral=True)

        try:
            user_id = interaction.user.id
            is_premium = permission_manager.is_premium(user_id)

            # Check rate limit
            if rate_limiter.is_rate_limited(user_id, is_premium):
                remaining = rate_limiter.get_remaining(user_id, is_premium)
                embed = nextcord.Embed(
                    title="Rate Limited",
                    description=f"You've reached your rate limit. Try again later.\nRemaining: {remaining}",
                    color=nextcord.Color.red(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Validate file
            if not script:
                embed = nextcord.Embed(
                    title="Error",
                    description="Please attach a Lua script file (.lua, .luau, .txt, or .zip)",
                    color=nextcord.Color.red(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Validate file
            is_valid, error = FileHandler.validate_file(script.filename, script.size)
            if not is_valid:
                embed = nextcord.Embed(
                    title="Invalid File",
                    description=error,
                    color=nextcord.Color.red(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Download file
            file_data = await script.read()

            # Create job
            job_id = str(uuid.uuid4())
            job = Job(
                job_id=job_id,
                user_id=user_id,
                filename=script.filename,
                input_data=file_data,
                settings={
                    "obfuscation_level": level,
                    "random_seed": None,
                },
            )

            # Add to queue
            added = await self.bot.job_queue.add_job(job)
            if not added:
                embed = nextcord.Embed(
                    title="Queue Full",
                    description="Server is busy. Please try again later.",
                    color=nextcord.Color.red(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Send progress embed
            embed = nextcord.Embed(
                title="Obfuscation Started",
                description=f"Processing: {script.filename}\nLevel: {level}/10\nJob ID: `{job_id[:8]}`",
                color=nextcord.Color.blue(),
            )
            embed.add_field(name="Status", value="Queued", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

            # Wait for completion with timeout
            import asyncio
            timeout = config.JOB_TIMEOUT_SECONDS + 10
            start_time = asyncio.get_event_loop().time()

            while True:
                job_status = await self.bot.job_queue.get_job_status(job_id)
                if job_status.status == JobStatus.COMPLETED:
                    await self._send_completion_embed(interaction, job_status)
                    break
                elif job_status.status == JobStatus.FAILED:
                    await self._send_error_embed(interaction, job_status)
                    break

                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed > timeout:
                    await interaction.followup.send(
                        "Processing timed out. Please try again.",
                        ephemeral=True,
                    )
                    break

                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Obfuscate command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=f"An error occurred: {str(e)[:100]}",
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    async def _send_completion_embed(
        self, interaction: nextcord.Interaction, job
    ) -> None:
        """Send completion embed.

        Args:
            interaction: Discord interaction
            job: Completed job
        """
        stats = job.metadata
        embed = nextcord.Embed(
            title="Obfuscation Complete",
            description=f"Successfully obfuscated: {job.filename}",
            color=nextcord.Color.green(),
        )
        embed.add_field(
            name="Size Reduction",
            value=f"{stats['original_size']} → {stats['obfuscated_size']} bytes",
            inline=False,
        )
        embed.add_field(
            name="Processing Time",
            value=f"{stats['processing_time']:.2f}s",
            inline=False,
        )
        embed.add_field(
            name="Protections Applied",
            value=stats['protection_summary'],
            inline=False,
        )

        # Send file
        obfuscated_code = job.result.decode("utf-8")
        await interaction.followup.send(
            embed=embed,
            file=nextcord.File(
                fp=None,
                filename=job.filename.replace(".lua", ".obf.lua"),
            ),
            ephemeral=True,
        )

    async def _send_error_embed(
        self, interaction: nextcord.Interaction, job
    ) -> None:
        """Send error embed.

        Args:
            interaction: Discord interaction
            job: Failed job
        """
        embed = nextcord.Embed(
            title="Obfuscation Failed",
            description=f"Error: {job.error}",
            color=nextcord.Color.red(),
        )
        await interaction.followup.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
    """Setup cog.

    Args:
        bot: Discord bot
    """
    bot.add_cog(ObfuscateCommand(bot))

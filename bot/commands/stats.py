"""Statistics and profile commands."""

import nextcord
from nextcord.ext import commands
from bot.logger import logger
from bot.permissions import permission_manager


class StatsCommand(commands.Cog):
    """Statistics and profile commands cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot

    @nextcord.slash_command(
        name="profile",
        description="View your obfuscation profile",
    )
    async def profile(self, interaction: nextcord.Interaction) -> None:
        """View user profile.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = interaction.user.id
            perm = permission_manager.get_user_permission(user_id)
            
            embed = nextcord.Embed(
                title="Your Profile",
                color=nextcord.Color.blue(),
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.add_field(name="User ID", value=f"`{user_id}`", inline=False)
            embed.add_field(name="Permission Level", value=perm.value.upper(), inline=False)
            embed.add_field(name="Premium", value="✓ Yes" if permission_manager.is_premium(user_id) else "✗ No", inline=False)
            embed.add_field(name="Admin", value="✓ Yes" if permission_manager.is_admin(user_id) else "✗ No", inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Profile command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=str(e),
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(
        name="stats",
        description="View your obfuscation statistics",
    )
    async def stats(self, interaction: nextcord.Interaction) -> None:
        """View user statistics.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = interaction.user.id
            user_jobs = await self.bot.job_queue.get_user_jobs(user_id)
            
            total_jobs = len(user_jobs)
            completed = sum(1 for job in user_jobs if job.status.value == "completed")
            failed = sum(1 for job in user_jobs if job.status.value == "failed")
            
            total_input = sum(job.metadata.get('original_size', 0) for job in user_jobs if job.metadata)
            total_output = sum(job.metadata.get('obfuscated_size', 0) for job in user_jobs if job.metadata)
            
            embed = nextcord.Embed(
                title="Your Statistics",
                color=nextcord.Color.blue(),
            )
            embed.add_field(name="Total Jobs", value=str(total_jobs), inline=True)
            embed.add_field(name="Completed", value=str(completed), inline=True)
            embed.add_field(name="Failed", value=str(failed), inline=True)
            embed.add_field(name="Total Input Size", value=f"{total_input:,} bytes", inline=False)
            embed.add_field(name="Total Output Size", value=f"{total_output:,} bytes", inline=False)
            
            if total_input > 0:
                ratio = (total_output / total_input) * 100
                embed.add_field(name="Avg Size Ratio", value=f"{ratio:.1f}%", inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Stats command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=str(e),
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(
        name="history",
        description="View your obfuscation history",
    )
    async def history(self, interaction: nextcord.Interaction) -> None:
        """View user history.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = interaction.user.id
            user_jobs = await self.bot.job_queue.get_user_jobs(user_id)
            
            if not user_jobs:
                embed = nextcord.Embed(
                    title="No History",
                    description="You haven't obfuscated any scripts yet.",
                    color=nextcord.Color.yellow(),
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Show last 10 jobs
            jobs_to_show = user_jobs[-10:]
            embed = nextcord.Embed(
                title="Your History (Last 10)",
                color=nextcord.Color.blue(),
            )
            
            for job in reversed(jobs_to_show):
                status_emoji = {
                    "completed": "✓",
                    "failed": "✗",
                    "processing": "⏳",
                    "queued": "📋",
                    "cancelled": "⛔",
                }.get(job.status.value, "?")
                
                embed.add_field(
                    name=f"{status_emoji} {job.filename}",
                    value=f"ID: `{job.job_id[:8]}`\nStatus: {job.status.value}",
                    inline=False,
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"History command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=str(e),
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
    """Setup cog.

    Args:
        bot: Discord bot
    """
    bot.add_cog(StatsCommand(bot))

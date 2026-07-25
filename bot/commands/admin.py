"""Admin commands."""

import nextcord
from nextcord.ext import commands
from bot.logger import logger
from bot.permissions import permission_manager, Permission


class AdminCommand(commands.Cog):
    """Admin commands cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot
        self.blacklist = set()

    async def _check_admin(self, interaction: nextcord.Interaction) -> bool:
        """Check if user is admin.

        Args:
            interaction: Discord interaction

        Returns:
            True if admin
        """
        return permission_manager.has_permission(interaction.user.id, Permission.ADMIN)

    @nextcord.slash_command(
        name="admin",
        description="Admin dashboard",
    )
    async def admin(self, interaction: nextcord.Interaction) -> None:
        """Admin dashboard.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        
        if not await self._check_admin(interaction):
            embed = nextcord.Embed(
                title="Unauthorized",
                description="You don't have permission to use admin commands.",
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            embed = nextcord.Embed(
                title="Admin Dashboard",
                color=nextcord.Color.red(),
            )
            embed.add_field(
                name="Queue Status",
                value=f"Size: {self.bot.job_queue.queue.qsize()}/{self.bot.job_queue.max_queue_size}\n"
                      f"Workers: {len(self.bot.job_queue.workers)}/{self.bot.job_queue.max_concurrent}",
                inline=False,
            )
            embed.add_field(
                name="Blacklist",
                value=f"Blacklisted users: {len(self.blacklist)}",
                inline=False,
            )
            embed.add_field(
                name="Available Commands",
                value="`/admin-blacklist` - Blacklist a user\n"
                      "`/admin-unblacklist` - Unblacklist a user\n"
                      "`/admin-broadcast` - Send announcement\n"
                      "`/admin-logs` - View recent logs",
                inline=False,
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Admin command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=str(e),
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(
        name="admin-blacklist",
        description="Blacklist a user",
    )
    async def blacklist(
        self,
        interaction: nextcord.Interaction,
        user_id: int = nextcord.SlashCommandOption(
            description="User ID to blacklist",
        ),
    ) -> None:
        """Blacklist user.

        Args:
            interaction: Discord interaction
            user_id: User ID to blacklist
        """
        await interaction.response.defer(ephemeral=True)
        
        if not await self._check_admin(interaction):
            embed = nextcord.Embed(
                title="Unauthorized",
                description="You don't have permission to use this command.",
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            self.blacklist.add(user_id)
            embed = nextcord.Embed(
                title="User Blacklisted",
                description=f"User `{user_id}` has been blacklisted.",
                color=nextcord.Color.green(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"User {user_id} blacklisted by {interaction.user.id}")
        except Exception as e:
            logger.error(f"Blacklist command error: {e}")
            embed = nextcord.Embed(
                title="Error",
                description=str(e),
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(
        name="admin-unblacklist",
        description="Unblacklist a user",
    )
    async def unblacklist(
        self,
        interaction: nextcord.Interaction,
        user_id: int = nextcord.SlashCommandOption(
            description="User ID to unblacklist",
        ),
    ) -> None:
        """Unblacklist user.

        Args:
            interaction: Discord interaction
            user_id: User ID to unblacklist
        """
        await interaction.response.defer(ephemeral=True)
        
        if not await self._check_admin(interaction):
            embed = nextcord.Embed(
                title="Unauthorized",
                description="You don't have permission to use this command.",
                color=nextcord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            self.blacklist.discard(user_id)
            embed = nextcord.Embed(
                title="User Unblacklisted",
                description=f"User `{user_id}` has been unblacklisted.",
                color=nextcord.Color.green(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"User {user_id} unblacklisted by {interaction.user.id}")
        except Exception as e:
            logger.error(f"Unblacklist command error: {e}")
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
    bot.add_cog(AdminCommand(bot))

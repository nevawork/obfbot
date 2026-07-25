"""Premium features command."""

import nextcord
from nextcord.ext import commands
from bot.logger import logger
from bot.permissions import permission_manager


class PremiumCommand(commands.Cog):
    """Premium features command cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot

    @nextcord.slash_command(
        name="premium",
        description="View premium features",
    )
    async def premium(self, interaction: nextcord.Interaction) -> None:
        """View premium features.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = interaction.user.id
            is_premium = permission_manager.is_premium(user_id)
            
            embed = nextcord.Embed(
                title="Premium Features",
                color=nextcord.Color.gold() if is_premium else nextcord.Color.greyple(),
            )
            
            if is_premium:
                embed.add_field(
                    name="Status",
                    value="✓ You have Premium access!",
                    inline=False,
                )
            else:
                embed.add_field(
                    name="Status",
                    value="✗ You don't have Premium access",
                    inline=False,
                )
            
            embed.add_field(
                name="Features",
                value="**Free:**\n"
                      "• 10 obfuscations/hour\n"
                      "• Basic protection (Level 1-5)\n"
                      "• Standard file support\n\n"
                      "**Premium:**\n"
                      "• 50 obfuscations/hour\n"
                      "• Maximum protection (Level 1-10)\n"
                      "• ZIP archive support\n"
                      "• Priority processing\n"
                      "• Advanced statistics\n"
                      "• Custom settings\n",
                inline=False,
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Premium command error: {e}")
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
    bot.add_cog(PremiumCommand(bot))

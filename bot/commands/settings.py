"""Settings command."""

import nextcord
from nextcord.ext import commands
from bot.logger import logger


class SettingsCommand(commands.Cog):
    """Settings command cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot
        self.user_settings = {}  # user_id -> settings dict

    @nextcord.slash_command(
        name="settings",
        description="Configure your obfuscation settings",
    )
    async def settings(self, interaction: nextcord.Interaction) -> None:
        """Configure settings.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = interaction.user.id
            
            # Get or create user settings
            if user_id not in self.user_settings:
                self.user_settings[user_id] = {
                    "level": 5,
                    "rename_vars": True,
                    "encrypt_strings": True,
                    "encode_numbers": True,
                    "dead_code": True,
                    "anti_debug": False,
                }
            
            settings = self.user_settings[user_id]
            
            embed = nextcord.Embed(
                title="Your Settings",
                description="Configure your obfuscation preferences",
                color=nextcord.Color.blue(),
            )
            embed.add_field(name="Default Level", value=f"{settings['level']}/10", inline=True)
            embed.add_field(name="Rename Variables", value="✓" if settings['rename_vars'] else "✗", inline=True)
            embed.add_field(name="Encrypt Strings", value="✓" if settings['encrypt_strings'] else "✗", inline=True)
            embed.add_field(name="Encode Numbers", value="✓" if settings['encode_numbers'] else "✗", inline=True)
            embed.add_field(name="Insert Dead Code", value="✓" if settings['dead_code'] else "✗", inline=True)
            embed.add_field(name="Anti-Debug", value="✓" if settings['anti_debug'] else "✗", inline=True)
            
            embed.add_field(
                name="How to Change",
                value="Use `/obfuscate level:<1-10>` to set obfuscation level.\n"
                      "More options coming soon!",
                inline=False,
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Settings command error: {e}")
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
    bot.add_cog(SettingsCommand(bot))

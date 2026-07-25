"""Help command."""

import nextcord
from nextcord.ext import commands
from bot.logger import logger


class HelpCommand(commands.Cog):
    """Help command cog."""

    def __init__(self, bot: commands.Bot):
        """Initialize cog.

        Args:
            bot: Discord bot
        """
        self.bot = bot

    @nextcord.slash_command(
        name="help",
        description="Show help and available commands",
    )
    async def help(self, interaction: nextcord.Interaction) -> None:
        """Show help.

        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        try:
            embed = nextcord.Embed(
                title="ObfBot - Advanced Lua/Luau Obfuscator",
                description="A high-performance Discord bot for obfuscating Lua scripts",
                color=nextcord.Color.blue(),
            )
            
            embed.add_field(
                name="📄 Main Commands",
                value="`/obfuscate` - Obfuscate a Lua script\n"
                      "`/profile` - View your profile\n"
                      "`/stats` - View your statistics\n"
                      "`/history` - View obfuscation history\n"
                      "`/settings` - Configure your settings\n"
                      "`/premium` - View premium features",
                inline=False,
            )
            
            embed.add_field(
                name="🔐 Protections Applied",
                value="✓ Variable renaming\n"
                      "✓ String encryption\n"
                      "✓ Number encoding\n"
                      "✓ Control flow protection\n"
                      "✓ Dead code insertion\n"
                      "✓ Anti-debug measures",
                inline=False,
            )
            
            embed.add_field(
                name="📁 Supported Formats",
                value="• `.lua` - Lua script files\n"
                      "• `.luau` - Luau script files\n"
                      "• `.txt` - Text files\n"
                      "• `.zip` - Archives (premium)",
                inline=False,
            )
            
            embed.add_field(
                name="⚙️ Obfuscation Levels",
                value="**1-2:** Light (variable renaming)\n"
                      "**3-4:** Moderate (+ string encryption)\n"
                      "**5-6:** Heavy (+ number encoding)\n"
                      "**7-8:** Very Heavy (+ control flow)\n"
                      "**9-10:** Maximum (all protections)",
                inline=False,
            )
            
            embed.add_field(
                name="⚡ Performance",
                value="Processes scripts in seconds\n"
                      "Rate limiting: 10/hour (50/hour for premium)\n"
                      "Max file size: 25MB",
                inline=False,
            )
            
            embed.add_field(
                name="📚 Documentation",
                value="For more info, visit: https://github.com/nevawork/obfbot",
                inline=False,
            )
            
            embed.set_footer(text="ObfBot v1.0.0")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Help command error: {e}")
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
    bot.add_cog(HelpCommand(bot))

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from colors import Color
from functions.userRoles import getUserSubject, hasUserAcceptedAlready
from settings import Settings
from files import Files
import json

class accept(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="accept",
        description="Accept the rules of this server."
    )

    async def accept(
        self,
        interaction: discord.Interaction):

        with open(Files.settings) as f:
            settings = json.load(f)
        f.close()

        user = await interaction.guild.fetch_member(interaction.user.id)
        if(hasUserAcceptedAlready(user)):
            await interaction.response.send_message(embed=discord.Embed(title=f":x: You already accepted the rules.", color=Color.red), ephemeral=True)
        else:
            role = interaction.guild.get_role(settings["roles"]["accepted"])
            await user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(title=":white_check_mark: You accepted the rules.", color=Color.green), ephemeral=True)
        
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        accept(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
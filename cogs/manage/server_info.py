import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from colors import Color
from functions.userRoles import getUserSubject
from settings import Settings
from files import Files
import json

subjectList = []
with open(Files.subjects) as f:
    subjects = json.load(f)
f.close()

for subject in subjects:
    subjectList.append(Choice(name=subject, value=subject))

class server_info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="server_info",
        description="Choose your subject."
    )

    async def server_info(
        self,
        interaction: discord.Interaction):

        membersWithoutSubject = interaction.guild.member_count

        memberCountStr = ""
        for subject in subjects:
            membersWithoutSubject -= len(interaction.guild.get_role(subjects[subject]["role"]).members)
            memberCountStr  += f"<@&" + str(subjects[subject]["role"]) + ">**:** " + str(len(interaction.guild.get_role(subjects[subject]["role"]).members)) + "\n"
        memberCountStr += f"**Ohne Studiengang-Rolle:** {membersWithoutSubject}"
        embedVar = discord.Embed(title=":information_source: Server-Informationen", color=Color.green)
        embedVar.add_field(name="Rollenverteilung", value=memberCountStr)
        await interaction.response.send_message(embed=embedVar)

    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        server_info(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
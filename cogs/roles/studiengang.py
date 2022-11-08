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
    subjectList.append(Choice(name=subjects[subject]["german"], value=subject))

class studiengang(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="studiengang",
        description="Wähle deinen Studiengang."
    )

    @app_commands.choices(
        studiengang = subjectList
    )

    async def studiengang(
        self,
        interaction: discord.Interaction,
        studiengang: str):

        user = await interaction.guild.fetch_member(interaction.user.id)
        role = interaction.guild.get_role(subjects[studiengang]["role"])
        userSubject = getUserSubject(user, interaction)
        if(userSubject == role):
            await interaction.response.send_message(embed=discord.Embed(title=f":x: Du hast diesen Studiengang bereits.", description=f"Studiengang: **{userSubject.name}**", color=Color.red), ephemeral=True)
        elif(userSubject != None):
            await user.remove_roles(userSubject)
            await user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: Du hast deinen Studiengang gewechselt.", description=f"Alter Studiengang: **{userSubject.name}**\nNeuer Studiengang: **{role.name}**", color=Color.green), ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: Du hast einen Studiengang ausgewählt.", description=f"Studiengang: **{role.name}**", color=Color.green), ephemeral=True)
        
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        studiengang(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
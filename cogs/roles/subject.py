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

class subject(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="subject",
        description="Choose your subject."
    )

    @app_commands.choices(
        subject = subjectList
    )

    async def subject(
        self,
        interaction: discord.Interaction,
        subject: str):

        user = await interaction.guild.fetch_member(interaction.user.id)
        role = interaction.guild.get_role(subjects[subject]["role"])
        userSubject = getUserSubject(user, interaction)
        if(userSubject == role):
            await interaction.response.send_message(embed=discord.Embed(title=f":x: You already have this subject.", description=f"Subject: **{userSubject.name}**", color=Color.red), ephemeral=True)
        elif(userSubject != None):
            await user.remove_roles(userSubject)
            await user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: You changed your subject.", description=f"Old subject: **{userSubject.name}**\nNew subject: **{role.name}**", color=Color.green), ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: You selected a subject.", description=f"Subject: **{role.name}**", color=Color.green), ephemeral=True)
        
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        subject(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
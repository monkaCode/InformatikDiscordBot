import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from colors import Color
from settings import Settings
from files import Files
import json

coursesList = []
with open(Files.courses) as f:
    courses = json.load(f)
f.close()
for course in courses["2"]:
    courseText = course.replace("Ã¼", "ü")
    coursesList.append(Choice(name=courseText, value=course))

class leave_course2(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="leave_course2",
        description="Leave a course."
    )

    @app_commands.choices(
        course = coursesList
    )

    async def leave_course2(
        self,
        interaction: discord.Interaction,
        course: str):

        courseText = course.replace("Ã¼", "ü")
        
        channel = courses["2"][course]["channel"]
        targetChannel = await interaction.guild.fetch_channel(channel)
        user = await interaction.guild.fetch_member(interaction.user.id)
        perms = targetChannel.overwrites_for(user)
        if(perms.view_channel == False):
            await interaction.response.send_message(embed=discord.Embed(title=":x: You are not in this course.", description=f"Course: **{courseText}**", color=Color.red), ephemeral=True)
            return
        elif(perms.view_channel == True):
            perms.view_channel = False
            await targetChannel.set_permissions(user, overwrite=perms)
            await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: You have been removed from the course.", description=f"Course: **{courseText}**", color=Color.green), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title=":x: You are not in this course.", description=f"Course: **{courseText}**", color=Color.red), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        leave_course2(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
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
for course in courses["1"]:
    courseText = course.replace("Ã¼", "ü")
    coursesList.append(Choice(name=courseText, value=course))

class join_course1(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="join_course1",
        description="Join a course."
    )

    @app_commands.choices(
        course = coursesList
    )

    async def join_course1(
        self,
        interaction: discord.Interaction,
        course: str):

        courseText = course.replace("Ã¼", "ü")

        channel = courses["1"][course]["channel"]
        targetChannel = await interaction.guild.fetch_channel(channel)
        user = await interaction.guild.fetch_member(interaction.user.id)
        perms = targetChannel.overwrites_for(user)
        if(perms.view_channel == True):
            await interaction.response.send_message(embed=discord.Embed(title=":x: You are already in this course.", description=f"Course: **{courseText}**", color=Color.red), ephemeral=True)
            return
        perms.view_channel = True
        await targetChannel.set_permissions(user, overwrite=perms)
        
        await interaction.response.send_message(embed=discord.Embed(title=f":white_check_mark: You have been added to the course.", description=f"Course: **{courseText}**", color=Color.green), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        join_course1(bot),
        guilds=[discord.Object(Settings.guildID)]
    )
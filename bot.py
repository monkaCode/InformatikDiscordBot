import json
import discord
from discord.ext import commands
from settings import Settings

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="?",
            intents=discord.Intents.all(),
            application_id=901956406050168862
        )
        self.initial_extensions = [
            "cogs.manage.server_info"
        ]
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        await bot.tree.sync(guild=discord.Object(id=Settings.guildID))

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message):
        with open(r"data/settings.json") as f:
            settings = json.load(f)
        f.close()

        try:
            if(type(message) == discord.Message and (message.channel.id == settings["channels"]["rules"] or message.channel.id == settings["channels"]["roles"])):
                await message.delete()
        except:
            return
    
    async def on_voice_state_update(self, member, before, after):
        with open(r"data/settings.json") as f:
            settings = json.load(f)
        f.close()

        guild = self.get_guild(settings["guildID"])
        channels = await guild.fetch_channels()
        voiceChannels = []

        for i in channels:
            if(i.category_id == settings["channels"]["voiceCategory"]):
                voiceChannels.append(i)

        allChannelsFull = True
        for i in voiceChannels:
            if(len(i.members) == 0):
                if(not allChannelsFull):
                    await i.delete()
                allChannelsFull = False

        if(allChannelsFull):
            newChannel = await guild.create_voice_channel(f"talk[{len(voiceChannels)}]", category=await guild.fetch_channel(settings["channels"]["voiceCategory"]))
            voiceChannels.append(newChannel)
        
        for vc in range(0, len(voiceChannels)):
            if(voiceChannels[vc].name != f"talk[{vc}]"):
                voiceChannels[vc].edit(name=f"talk[{vc}]")

    
bot = MyBot()
bot.run(Settings.token)
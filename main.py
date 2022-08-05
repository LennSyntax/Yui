import discord
import traceback
import sys
import os
from discord.ext import commands

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music and /help!"))

@bot.slash_command(Name="Help", description="Get some help using this command uwu!", guild_ids=None)
async def help(ctx):
    embed = discord.Embed(title="Commands list", description= "All the commands are listed below.", color=0xD684FF)
    embed.add_field(name="Music", value="`play`, `stop`, `loop`, `queue`, `pause`, `resume`, `shuffle`, `soundcloud`, `now playing`, `lyrics`, `skip`, `panel`")
    embed.add_field(name="Admin", value="`vc channel`, `vc private`, `vc delete`, `vc kick`, `vc mute`, `vc unmute`, `vc lock`, `vc unlock`, `vc deafen`, `vc undeafen`")
    embed.set_footer(icon_url="https://media.discordapp.net/attachments/971981567339687956/971981650177196042/FUmn6td.jpg", text="Please use / before all the commands")
    await ctx.respond(embed=embed)

@bot.slash_command(Name="Ping", description="Pong?", guild_ids=None)
async def ping(ctx):
     embed = discord.Embed(title="Ping!!!",description=f"Pong: `{round(bot.latency * 1000)}ms`", color=0xD684FF)
     await ctx.respond(embed=embed)

extentions=[
            'cogs.music',
            'cogs.extra',
            'cogs.info',
            'cogs.panel',
]
if __name__ == "__main__":
    for extension in extentions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Error loading {extension}', file=sys.stderr)
            traceback.print_exc()
   
bot.run("OTkxNzQyMjUzNjM2Nzg4MzI1.GyTZzr.cNmPSpsqzgoA7S2xftGy3NimyINbnh3SAWJPZw")
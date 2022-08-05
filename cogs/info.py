from email import header
from turtle import title
from unittest import async_case
import aiohttp
import discord
import wavelink
import datetime
import requests
from discord.ext import commands 
from discord.commands import slash_command

class Info(commands.Cog, name='slashinfo'):
    def __init__(self, bot):
        self.bot = bot

    now = discord.SlashCommandGroup("now", "now group", guild_ids=None)

    @now.command(description="Check the now playing status using this.")
    async def playing(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I play the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        embed = discord.Embed(title = f"<:music:991690031553073212> now playing {vc.track.title}", description = f"Artist: {vc.track.author}", color=0xD684FF)
        embed.add_field(name = "Duration:", value = f"{str(datetime.timedelta(seconds=vc.track.length))}")
        embed.add_field(name = "Extra info:", value = f"Song link:- [{vc.track.title}]({str(vc.track.uri)})", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(Name="lyrics", description="Get the lyrics of the song that is playing.", guild_ids=[964893663610155088])
    async def lyrics(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I play the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        name = f"{vc.track.title} by {vc.track.author}"
        r=requests.get(f"https://some-random-api.ml/lyrics?title={name}")
        data = r.json()
        lyrics = data["lyrics"]
        embed = discord.Embed(title = f"<:music:991690031553073212> {name}", description = f"{lyrics[:2000]}[...](<{data['links']['genius']}>)", color=0xD684FF)
        await ctx.respond(embed=embed)
        print(f"{lyrics}")

def setup(bot):
    bot.add_cog(Info(bot))
    print("Info cog is loaded!")

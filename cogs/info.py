import aiohttp
import discord
import wavelink
import datetime
import logging
from discord.ext import commands
from discord.commands import slash_command

logging.basicConfig(level=logging.INFO)

class Info(commands.Cog, name='slashinfo'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    now = discord.SlashCommandGroup("now", "now group", guild_ids=None)

    @now.command(description="Check the now playing status using this.")
    async def playing(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I play the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        
        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        
        embed = discord.Embed(
            title=f"Now playing {vc.track.title}",
            description=f"Artist: {vc.track.author}",
            color=0xD684FF
        )
        embed.add_field(name="Duration:", value=str(datetime.timedelta(seconds=vc.track.length)))
        embed.add_field(name="Extra info:", value=f"Song link: [{vc.track.title}]({vc.track.uri})", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="lyrics", description="Get the lyrics of the song that is playing.", guild_ids=None)
    async def lyrics(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I play the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        
        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        
        name = f"{vc.track.title} by {vc.track.author}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/lyrics?title={name}") as response:
                if response.status != 200:
                    embed = discord.Embed(description="Could not fetch lyrics at this time. Please try again later.", color=0xD684FF)
                    return await ctx.respond(embed=embed)
                data = await response.json()
        
        lyrics = data.get("lyrics", "Lyrics not found.")
        genius_link = data.get("links", {}).get("genius", "")
        embed = discord.Embed(
            title=f"{name}",
            description=f"{lyrics[:2000]}{'...' if len(lyrics) > 2000 else ''}",
            color=0xD684FF
        )
        if genius_link:
            embed.add_field(name="Full Lyrics", value=f"[Genius]({genius_link})", inline=False)
        await ctx.respond(embed=embed)
        logging.info(f"Lyrics fetched for {name}")

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
    logging.info("Info cog is loaded!")

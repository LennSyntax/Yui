import discord
import wavelink
import datetime
import random
from discord.ext import commands 
from discord.commands import Option
from discord.commands import slash_command

class Extra(commands.Cog, name='extra'):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(Name="leave", description="Disconnect trash bot using this command.", guild_ids=None)
    async def leave(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!", description="Don't try to break me, I'm not in the voice channel you cannot disconnect me.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(title="Error!", description="You have to join a voice channel first to disconnect me!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        embed = discord.Embed(description="Have a Nice day 😊", color=0xD684FF)
        return await ctx.respond(embed=embed)

    @slash_command(Name="pause", description="Pause the playing music.", guild_ids=None)
    async def pause(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!", description="Don't try to break me, I'm not in the voice channel how will I pause the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(title="Error!", description="You have to join a voice channel first to pause!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        embed = discord.Embed(description=f"<:pause:991587278403158067> the song has been paused.", color=0xD684FF)
        await ctx.respond(embed=embed)

    @slash_command(Name="resume", description="Resume the paused music.", guild_ids=None)
    async def resume(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!", description="Don't try to break me, I'm not in the voice channel how will I resume the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(title="Error!", description="You have to join a voice channel first to resume!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.resume()
        embed = discord.Embed(description="<:play:991587195397865523> the song has been resumed.", color=0xD684FF)
        await ctx.respond(embed=embed)

    @slash_command(Name="seek", description="Seek for the favorite part of the song.", guild_ids=None)
    async def seek(self, ctx, seconds: Option(int, description="Enter the value in seconds")):
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!", description="Don't try to break me, I'm not in the voice channel how will I seek the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(title="Error!", description="You have to join a voice channel first to play some music to seek!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            if vc.is_playing():
                old_position = vc.position
                position = old_position + seconds
                if position > vc.source.length:
                    embed = discord.Embed(title="Error!", description="You can't seek the end of the track!", color=0xD684FF)
                    return await ctx.respond(embed=embed)
                if position < 0:
                    position = 0
                await vc.seek(seconds *1000)
                embed = discord.Embed(description=f"<:extra:991697564325924885> you have seeked {seconds} seconds.", color=0xD684FF)
        return await ctx.respond(embed=embed)

    @slash_command(Name="stop", description="Stop the playing music.", guild_ids=None)
    async def stop(self,ctx):  
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!", description="Don't try to break me, I'm not in the voice channel how will I stop the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(title="Error!", description="You have to join a voice channel first to stop!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.queue.clear()
        await vc.stop()
        embed = discord.Embed(description=f"<:stop:991596294659387422> the song has been stopped.", color=0xD684FF)
        return await ctx.respond(embed=embed)
 
    @slash_command(Name="skip", description="Move to the next song.", guild_ids=None)
    async def skip(self,ctx):  
        if not ctx.voice_client:
            embed = discord.Embed(title="Error!",description="Don't try to break me, I'm not in the voice channel how will I skip the music?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to skip!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.stop()
        embed = discord.Embed(description=f"<:skip:991688147341688892> the Song have been skipped", color=0xD684FF)
        await ctx.respond(embed=embed)
        if vc.queue.is_empty:
                embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
                return await ctx.respond(embed=embed)

    @slash_command(Name="shuffle", description="Shuffle the existing queue using this.", guild_ids=None)
    async def shuffle(self,ctx):  
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I shuffle the queue?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first and create a queue to shuffle!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            random.shuffle(vc.queue._queue)
            embed = discord.Embed(description="<:shuffle:991585631539036210> queue have been shuffled!", color=0xD684FF)
            await ctx.respond(embed=embed)
        if vc.queue.is_empty:
                embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
                return await ctx.respond(embed=embed)

    @slash_command(Name="clear", description="Clear the current queue using this.", guild_ids=None)
    async def clear(self,ctx):  
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel how will I clear the queue?", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.queue.clear()
            embed = discord.Embed(description=f"<:delete:991697459040497685> queue have been cleared", color=0xD684FF)
            await ctx.respond(embed=embed)

    @slash_command(Name="queue", description="Get the queued music using this.", guild_ids=None)
    async def queue(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not ctx.author.voice:
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            embed = discord.Embed(description="You must be in the same voice channel to use that command.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

            if vc.queue.is_empty:
                embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
                return await ctx.respond(embed=embed)

            embed = discord.Embed(title = "Queue", color=0xD684FF)
            queue = vc.queue.copy()
            song_count = 0
            for song in queue:
                song_count += 1
                embed.add_field(name=f"**#{song_count}** <:arrow:991585305759055972> {song.title} ", value=f"<:space:992037334767898735> **Duration** `[{str(datetime.timedelta(seconds=vc.track.length))}]`", inline=False)
            return await ctx.respond(embed=embed)

    @slash_command(Name="loop", description="loop your favorite song using this.", guild_ids=None)
    async def loop(self,ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not ctx.author.voice:
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            embed = discord.Embed(description="You must be in the same voice channel to use that command.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
         vc.loop ^= True
        except Exception:
         setattr(vc, "loop", False)

        if vc.loop:
            embed = discord.Embed(description="<:loop:991587722051457134> looping have been enabled", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else: 
            embed = discord.Embed(description="<:wrong_mark:991708719798825000> looping have been disabled", color=0xD684FF)
            return await ctx.respond(embed=embed)

    @slash_command(name="volume", description="Control the music volume using this.", guild_ids=None)
    async def volume(self, ctx, volume: Option(int, description="Please enter a number less than or equal to 100")): 
        if not ctx.voice_client: 
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel so how will I change the volume on anything?.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client 
            if not vc.is_playing(): 
                embed = discord.Embed(description="You must play some music to change thr volume!", color=0xD684FF)
                return await ctx.respond(embed=embed)
            if volume > 100:
                embed = discord.Embed(description="That's way to high.", color=0xD684FF)
                return await ctx.respond(embed=embed)
            elif volume < 0:
                embed = discord.Embed(description="That's way to low.", color=0xD684FF)
                return await ctx.respond(embed=embed)
            embed = discord.Embed(description=f"<:volume:991585824938410045> set the volume to {volume}%", color=0xD684FF)
            await ctx.respond(embed=embed)
            return await vc.set_volume(volume)

    @slash_command(name="equaliser", description="Control the music equaliser using this.", guild_ids=[964893663610155088])
    async def equaliser(self, ctx, preset: Option(str, description="Please enter a number less than or equal to 100")): 
        if not ctx.voice_client: 
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel so how will I change the volume on anything?.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client 
            if not vc.is_playing(): 
                embed = discord.Embed(description="You must play some music to change thr volume!", color=0xD684FF)
                return await ctx.respond(embed=embed)
            eq = getattr(wavelink.eqs.Equalizer, preset, None)
            if not eq:
                embed = discord.Embed(description="Equaliser have not been adjusted", color=0xD684FF)
                return await ctx.respond(embed=embed)
            await vc.set_eq(eq())
            embed = discord.Embed(description=f"Equaliser adjusted to the {preset} preset.", color=0xD684FF)
            await ctx.respond(embed=embed)
                
def setup(bot):
    bot.add_cog(Extra(bot))
    print("Extra cog is loaded!")
import discord
import wavelink
from discord.ext import commands
from discord.commands import Option, slash_command

class Music(commands.Cog, name='music'):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='lavalink.oops.wtf', port=443, password='www.freelavalink.ga', https=True)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            await vc.play(track)
        else:
            next_song = vc.queue.get()
            await vc.play(next_song)
            embed = discord.Embed(description=f"Now playing: {next_song.title}", color=0xD684FF)
            await ctx.send(embed=embed, delete_after=20)

    @slash_command(name="play", description="Play music from YouTube.", guild_ids=None)
    async def play(self, ctx, *, search: Option(str, description="Enter the song name or artist.")):
        search = await wavelink.YouTubeMusicTrack.search(query=search, return_first=True)
        if not ctx.voice_client:
            if ctx.author.voice:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                embed = discord.Embed(description="You need to join a voice channel first!", color=0xD684FF)
                return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            embed = discord.Embed(color=0xD684FF)
            embed.add_field(name="Now playing", value=f"{search.title}...")
            await ctx.respond(embed=embed)
        else:
            await vc.queue.put_wait(search)
            embed = discord.Embed(description=f"Added {search.title} to the queue.", color=0xD684FF)
            await ctx.respond(embed=embed)
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @slash_command(name="soundcloud", description="Play music from SoundCloud.", guild_ids=None)
    async def soundcloud(self, ctx, *, search: Option(str, description="Enter the song name or artist.")):
        search = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
        if not ctx.voice_client:
            if ctx.author.voice:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                embed = discord.Embed(description="You need to join a voice channel first!", color=0xD684FF)
                return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            embed = discord.Embed(color=0xD684FF)
            embed.add_field(name="Now playing", value=f"{search.title}...")
            await ctx.respond(embed=embed)
        else:
            await vc.queue.put_wait(search)
            embed = discord.Embed(description=f"Added {search.title} to the queue.", color=0xD684FF)
            await ctx.respond(embed=embed)
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @slash_command(name="pause", description="Pause the current track.", guild_ids=None)
    async def pause(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await vc.pause()
            await ctx.respond("Paused the music.")
        else:
            await ctx.respond("No music is playing.")

    @slash_command(name="resume", description="Resume the current track.", guild_ids=None)
    async def resume(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_paused():
            await vc.resume()
            await ctx.respond("Resumed the music.")
        else:
            await ctx.respond("Music is not paused.")

    @slash_command(name="stop", description="Stop the current track.", guild_ids=None)
    async def stop(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await vc.stop()
            await ctx.respond("Stopped the music.")
        else:
            await ctx.respond("No music is playing.")

    @slash_command(name="skip", description="Skip the current track.", guild_ids=None)
    async def skip(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            await vc.stop()
            await ctx.respond("Skipped the track.")
        else:
            await ctx.respond("No music is playing.")

    @slash_command(name="queue", description="Show the current music queue.", guild_ids=None)
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty:
            await ctx.respond("The queue is empty.")
        else:
            queue_list = "\n".join([f"{i+1}. {track.title}" for i, track in enumerate(vc.queue)])
            embed = discord.Embed(title="Music Queue", description=queue_list, color=0xD684FF)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))
    print("Music cog is loaded!")

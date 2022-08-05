import discord
import wavelink
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

class Music(commands.Cog, name='music'):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='lavalink.oops.wtf', port=443, password='www.freelavalink.ga', https=True)
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
        next_song = vc.queue.get()
        await vc.play(next_song)
        embed = discord.Embed(description=f"<:music:991690031553073212> now playing: {next_song.title}", color=0xD684FF)
        await ctx.send(embed=embed, delete_after=20)

    @slash_command(Name="play", description="Using this command you can play music.", guild_ids=None)
    async def play(self, ctx, *, search: Option(str, description="Please enter your song name/artist name here.")):
        search = await wavelink.YouTubeMusicTrack.search(query=search, return_first=True)
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            embed = discord.Embed(color=0xD684FF)
            embed.add_field(name="<:music:991690031553073212> now playing", value=f"{search.title}...")
            return await ctx.respond(embed=embed)
        else:
            queue = vc.queue.copy()
            number_count = 1
            for number in queue:
                number_count += 1
            await vc.queue.put_wait(search)
            embed = discord.Embed(description=f"<:extra:991697564325924885> added {search.title}... to the queue - Position #{number_count}", color=0xD684FF)
            await ctx.respond(embed=embed)
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @slash_command(Name="soundCloud", description="Using this command you can play SoundCloud links.", guild_ids=None)
    async def soundcloud(self, ctx, *, search: Option(str, description="Please enter your song name/artist name here.")):
        search = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to play some music!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            embed = discord.Embed(color=0xD684FF)
            embed.add_field(name="<:music:991690031553073212> now playing", value=f"{search.title}...")
            return await ctx.respond(embed=embed)
        else:
            queue = vc.queue.copy()
            number_count = 1
            for number in queue:
                number_count += 1
            await vc.queue.put_wait(search)
            embed = discord.Embed(description=f"<:extra:991697564325924885> added {search.title}... to the queue - Position {number_count}", color=0xD684FF)
            await ctx.respond(embed=embed, allowed_mentions = discord.AllowedMentions(replied_user=False))
        vc.ctx = ctx
        setattr(vc, "loop", False)
   
def setup(bot):
    bot.add_cog(Music(bot))
    print("Music cog is loaded!")
import discord
import wavelink
import datetime
import requests
from discord.ui import Button, View, Select
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

class ControlPanel(discord.ui.View):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx

    @discord.ui.button(label="Resume/Pause", style=discord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.edit(content="<:play:991587195397865523> the song has been resumed.", view=self)
        else: 
            await self.vc.pause()
            await interaction.message.edit(content="<:pause:991587278403158067> the song has been paused.", view=self)
  
    @discord.ui.button(label="Queue", style=discord.ButtonStyle.blurple)
    async def queue(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        button.disabled = False
        if self.vc.queue.is_empty:
            embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title = "Queue", color=0xD684FF)
        queue = self.vc.queue.copy()
        song_count = 0
        for song in queue:
             song_count += 1
             embed.add_field(name=f"**#{song_count}** <:arrow:991585305759055972> {song.title} ", value=f"<:space:992037334767898735> **Duration** `[{str(datetime.timedelta(seconds=self.vc.track.length))}]`", inline=False)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.blurple)
    async def skip(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        button.disabled = False
        if self.vc.queue.is_empty:
            embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        try:
           next_song = self.vc.queue.get()
           await self.vc.play(next_song)
           embed = discord.Embed(color=0xD684FF)
           embed.add_field(name="<:music:991690031553073212> now playing:", value=f"{next_song}...")
           await interaction.message.edit(embed=embed, view=self)
        except Exception:
           embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
           return await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Now Playing", style=discord.ButtonStyle.blurple)
    async def now_playing(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        button.disabled = False
        if not self.vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title = f"<:music:991690031553073212> now playing {self.vc.track.title}", description = f"Artist: {self.vc.track.author}", color=0xD684FF)
        embed.add_field(name = "Duration:", value = f"{str(datetime.timedelta(seconds=self.vc.track.length))}")
        embed.add_field(name = "Extra info:", value = f"Song link:- [{self.vc.track.title}]({str(self.vc.track.uri)})", inline=False)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Lyrics", style=discord.ButtonStyle.blurple)
    async def lyrics(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        button.disabled = False
        if not self.vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        name = f"{self.vc.track.title} by {self.vc.track.author}"
        r=requests.get(f"https://some-random-api.ml/lyrics?title={name}")
        data = r.json()
        lyrics = data["lyrics"]
        embed = discord.Embed(title = f"<:music:991690031553073212> {name}", description = f"{lyrics[:2000]}[...](<{data['links']['genius']}>)", color=0xD684FF)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.blurple)
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = False
        button.disabled = False
        vc: wavelink.Player = self.ctx.voice_client
        self.vc.queue.clear()
        await self.vc.stop()
        embed = discord.Embed(description="<:stop:991596294659387422> the song has been stopped.", color=0xD684FF)
        await interaction.message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Disconnect", style=discord.ButtonStyle.red)
    async def disconnect(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user == self.ctx.author:
            embed = discord.Embed(title="Error!", description="Oh no you can't do that, run the panel command to use these buttons.", color=0xD684FF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        for child in self.children:
            child.disable = True
        await self.vc.disconnect()
        embed = discord.Embed(description="Have a Nice day 😊", color=0xD684FF)
        await interaction.message.edit(embed=embed, view=self)

class Panel(commands.Cog, name='panel'):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(Name="panel", description="Get the music panel control using this.", guild_ids=None)
    async def panel(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="Don't try to break me, I'm not in the voice channel you cannot disconnect me.", color=0xD684FF)
            return await ctx.respond(embed=embed)
        elif not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to disconnect me!", color=0xD684FF)
            return await ctx.respond(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="Oh no please play some song first.", color=0xD684FF)
            await ctx.respond(embed=embed)

        embed = discord.Embed(title = "Music Panel", description="Control the bot by clicking the buttons below", color=0xD684FF)
        view = ControlPanel(vc, ctx)
        await ctx.respond(embed=embed, view=view)
    
def setup(bot):
    bot.add_cog(Panel(bot))
    print("Panel cog is loaded!")
import discord
import wavelink
import datetime
import aiohttp
import logging
from discord.ui import Button, View
from discord.ext import commands
from discord.commands import Option, slash_command

logging.basicConfig(level=logging.INFO)

class ControlPanel(discord.ui.View):
    def __init__(self, vc: wavelink.Player, ctx: commands.Context):
        super().__init__()
        self.vc = vc
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            embed = discord.Embed(
                title="Error!",
                description="Oh no you can't do that, run the panel command to use these buttons.",
                color=0xD684FF
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    async def update_message(self, interaction: discord.Interaction, content: str = None, embed: discord.Embed = None):
        for child in self.children:
            child.disabled = False
        await interaction.message.edit(content=content, embed=embed, view=self)

    @discord.ui.button(label="Resume/Pause", style=discord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.vc.is_paused():
            await self.vc.resume()
            await self.update_message(interaction, content="<:play:991587195397865523> The song has been resumed.")
        else:
            await self.vc.pause()
            await self.update_message(interaction, content="<:pause:991587278403158067> The song has been paused.")

    @discord.ui.button(label="Queue", style=discord.ButtonStyle.blurple)
    async def queue(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.vc.queue.is_empty:
            embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(title="Queue", color=0xD684FF)
        queue = self.vc.queue.copy()
        for idx, song in enumerate(queue, start=1):
            embed.add_field(
                name=f"**#{idx}** <:arrow:991585305759055972> {song.title}",
                value=f"<:space:992037334767898735> **Duration** `[{str(datetime.timedelta(seconds=song.length))}]`",
                inline=False
            )
        await self.update_message(interaction, embed=embed)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.blurple)
    async def skip(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.vc.queue.is_empty:
            embed = discord.Embed(description="The queue is empty.", color=0xD684FF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        next_song = self.vc.queue.get()
        await self.vc.play(next_song)
        embed = discord.Embed(color=0xD684FF)
        embed.add_field(name="<:music:991690031553073212> Now playing:", value=f"{next_song.title}...")
        await self.update_message(interaction, embed=embed)

    @discord.ui.button(label="Now Playing", style=discord.ButtonStyle.blurple)
    async def now_playing(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"<:music:991690031553073212> Now playing {self.vc.track.title}",
            description=f"Artist: {self.vc.track.author}",
            color=0xD684FF
        )
        embed.add_field(name="Duration:", value=f"{str(datetime.timedelta(seconds=self.vc.track.length))}")
        embed.add_field(name="Extra info:", value=f"Song link: [{self.vc.track.title}]({self.vc.track.uri})", inline=False)
        await self.update_message(interaction, embed=embed)

    @discord.ui.button(label="Lyrics", style=discord.ButtonStyle.blurple)
    async def lyrics(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.vc.is_playing():
            embed = discord.Embed(description="There is no song playing right now.", color=0xD684FF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        name = f"{self.vc.track.title} by {self.vc.track.author}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/lyrics?title={name}") as response:
                data = await response.json()
                lyrics = data["lyrics"]
                embed = discord.Embed(
                    title=f"<:music:991690031553073212> {name}",
                    description=f"{lyrics[:2000]}[...](<{data['links']['genius']}>)",
                    color=0xD684FF
                )
                await self.update_message(interaction, embed=embed)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.blurple)
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.vc.queue.clear()
        await self.vc.stop()
        embed = discord.Embed(description="<:stop:991596294659387422> The song has been stopped.", color=0xD684FF)
        await self.update_message(interaction, embed=embed)

    @discord.ui.button(label="Disconnect", style=discord.ButtonStyle.red)
    async def disconnect(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        embed = discord.Embed(description="Have a nice day 😊", color=0xD684FF)
        await self.update_message(interaction, embed=embed)

class Panel(commands.Cog, name='panel'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="panel", description="Get the music panel control using this.")
    async def panel(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = discord.Embed(description="I'm not in a voice channel, you cannot disconnect me.", color=0xD684FF)
            await ctx.respond(embed=embed)
            return

        if not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You have to join a voice channel first to disconnect me!", color=0xD684FF)
            await ctx.respond(embed=embed)
            return

        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed = discord.Embed(description="Please play a song first.", color=0xD684FF)
            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(title="Music Panel", description="Control the bot by clicking the buttons below", color=0xD684FF)
        view = ControlPanel(vc, ctx)
        await ctx.respond(embed=embed, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(Panel(bot))
    logging.info("Panel cog is loaded!")

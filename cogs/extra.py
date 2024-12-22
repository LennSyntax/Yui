import discord
import wavelink
import datetime
import random
from discord.ext import commands
from discord.commands import Option, slash_command

ERROR_COLOR = 0xD684FF
SUCCESS_COLOR = 0xD684FF

class Extra(commands.Cog, name='extra'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_error(self, ctx: commands.Context, message: str) -> None:
        embed = discord.Embed(title="Error!", description=message, color=ERROR_COLOR)
        await ctx.respond(embed=embed)

    async def send_success(self, ctx: commands.Context, message: str) -> None:
        embed = discord.Embed(description=message, color=SUCCESS_COLOR)
        await ctx.respond(embed=embed)

    @slash_command(name="leave", description="Disconnect the bot from the voice channel.")
    async def leave(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        await self.send_success(ctx, "Disconnected from the voice channel. Have a nice day 😊")

    @slash_command(name="pause", description="Pause the currently playing music.")
    async def pause(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        await self.send_success(ctx, "The song has been paused.")

    @slash_command(name="resume", description="Resume the paused music.")
    async def resume(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        await vc.resume()
        await self.send_success(ctx, "The song has been resumed.")

    @slash_command(name="seek", description="Seek to a specific part of the song.")
    async def seek(self, ctx: commands.Context, seconds: Option(int, description="Enter the value in seconds")) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            new_position = vc.position + seconds * 1000
            if new_position > vc.source.length:
                await self.send_error(ctx, "You can't seek beyond the end of the track.")
                return
            if new_position < 0:
                new_position = 0
            await vc.seek(new_position)
            await self.send_success(ctx, f"Seeked {seconds} seconds.")

    @slash_command(name="stop", description="Stop the currently playing music.")
    async def stop(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        vc.queue.clear()
        await vc.stop()
        await self.send_success(ctx, "The song has been stopped.")

    @slash_command(name="skip", description="Skip to the next song.")
    async def skip(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        await vc.stop()
        await self.send_success(ctx, "The song has been skipped.")
        if vc.queue.is_empty:
            await self.send_success(ctx, "The queue is empty.")

    @slash_command(name="shuffle", description="Shuffle the current queue.")
    async def shuffle(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        random.shuffle(vc.queue._queue)
        await self.send_success(ctx, "The queue has been shuffled.")
        if vc.queue.is_empty:
            await self.send_success(ctx, "The queue is empty.")

    @slash_command(name="clear", description="Clear the current queue.")
    async def clear(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        vc.queue.clear()
        await self.send_success(ctx, "The queue has been cleared.")

    @slash_command(name="queue", description="Display the current queue.")
    async def queue(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not ctx.author.voice:
            await self.send_error(ctx, "You need to join a voice channel first.")
            return
        if ctx.author.voice.channel != ctx.voice_client.channel:
            await self.send_error(ctx, "You must be in the same voice channel to use this command.")
            return

        vc: wavelink.Player = ctx.voice_client
        if vc.queue.is_empty:
            await self.send_success(ctx, "The queue is empty.")
            return

        embed = discord.Embed(title="Queue", color=SUCCESS_COLOR)
        queue = vc.queue.copy()
        for idx, song in enumerate(queue, start=1):
            embed.add_field(name=f"**#{idx}** {song.title}",
                            value=f"**Duration** `[{str(datetime.timedelta(seconds=song.length))}]`",
                            inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="loop", description="Loop the current song.")
    async def loop(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not ctx.author.voice:
            await self.send_error(ctx, "You need to join a voice channel first.")
            return
        if ctx.author.voice.channel != ctx.voice_client.channel:
            await self.send_error(ctx, "You must be in the same voice channel to use this command.")
            return

        vc: wavelink.Player = ctx.voice_client
        vc.loop = not getattr(vc, "loop", False)
        if vc.loop:
            await self.send_success(ctx, "Looping has been enabled.")
        else:
            await self.send_success(ctx, "Looping has been disabled.")

    @slash_command(name="volume", description="Set the music volume.")
    async def volume(self, ctx: commands.Context, volume: Option(int, description="Enter a number between 0 and 100")) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            await self.send_error(ctx, "You need to play some music first.")
            return
        if volume > 100:
            await self.send_error(ctx, "Volume too high. Please enter a value between 0 and 100.")
            return
        if volume < 0:
            await self.send_error(ctx, "Volume too low. Please enter a value between 0 and 100.")
            return

        await vc.set_volume(volume)
        await self.send_success(ctx, f"Volume set to {volume}%.")

    @slash_command(name="equaliser", description="Set the music equaliser.")
    async def equaliser(self, ctx: commands.Context, preset: Option(str, description="Enter the equaliser preset")) -> None:
        if not ctx.voice_client:
            await self.send_error(ctx, "I'm not in a voice channel.")
            return
        if not getattr(ctx.author.voice, "channel", None):
            await self.send_error(ctx, "You need to join a voice channel first.")
            return

        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            await self.send_error(ctx, "You need to play some music first.")
            return

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            await self.send_error(ctx, "Invalid equaliser preset.")
            return

        await vc.set_eq(eq())
        await self.send_success(ctx, f"Equaliser set to the {preset} preset.")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extra(bot))
    print("Extra cog is loaded!")

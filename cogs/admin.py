import discord
import wavelink
import datetime
import aiosqlite
from discord.commands import Option
from discord.commands import slash_command
from discord.ext import commands 

class Admin(commands.Cog, name='admin'):
    def __init__(self, bot):
        self.bot = bot

    vc = discord.SlashCommandGroup("vc", "vc group", guild_ids=None)

    @vc.command(description="Create a new voice channel.")
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, *, name: Option(str, description="Enter the name of the channel.")):
        channel = await ctx.guild.create_voice_channel(name=name)
        embed = discord.Embed(description=f"{channel.name} voice channel has been created.", color=0xD684FF)
        await ctx.respond(embed=embed, delete_after=20)
    
    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Create a new private voice channel.")
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def private(self, ctx, role: Option(discord.Role, description="Mention the role for the channel."), *, name: Option(str, description="Enter the name of the channel.")):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_voice_channel(name=name, overwrites=overwrites)
        embed = discord.Embed(description=f"{channel.name} private voice channel has been created.", color=0xD684FF)
        await ctx.respond(embed=embed, delete_after=20)
    
    @private.error
    async def private_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Delete a voice channel.")    
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def delete(self, ctx, *, channel: Option(discord.VoiceChannel, description="Mention the channel to delete.")):
        await channel.delete()
        embed = discord.Embed(description=f"{channel.name} voice channel has been deleted.", color=0xD684FF)
        await ctx.respond(embed=embed, delete_after=20)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)
 
    @vc.command(description="Kick a user from the voice channel.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: Option(discord.Member, description="Mention the user to kick.", required=True)):
        if ctx.author.top_role > member.top_role or ctx.guild.owner == ctx.author:
            if member.guild_permissions.ban_members and ctx.guild.owner != ctx.author:
                embed = discord.Embed(description="Something went wrong, please try again.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else: 
                await member.edit(voice_channel=None)
                await ctx.respond(f"{member.mention} was kicked from the VC.")
        else:
            embed = discord.Embed(description="You can't kick this user.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Mute a user in the voice channel.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def mute(self, ctx, member: Option(discord.Member, description="Mention the user to mute.", required=True)):
        if ctx.author.top_role > member.top_role or ctx.guild.owner == ctx.author:
            if member.guild_permissions.ban_members and ctx.guild.owner != ctx.author:
                embed = discord.Embed(description="Something went wrong, please try again.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else: 
                await member.edit(mute=True)
                await ctx.respond(f"{member.mention} was muted in the VC.")
        else:
            embed = discord.Embed(description="You can't mute this user.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)
         
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Unmute a user in the voice channel.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def unmute(self, ctx, member: Option(discord.Member, description="Mention the user to unmute.", required=True)):
        if ctx.author.top_role > member.top_role or ctx.guild.owner == ctx.author:
            if member.guild_permissions.ban_members and ctx.guild.owner != ctx.author:
                embed = discord.Embed(description="Something went wrong, please try again.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else: 
                await member.edit(mute=False)
                await ctx.respond(f"{member.mention} was unmuted in the VC.")
        else:
            embed = discord.Embed(description="You can't unmute this user.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Lock the current voice channel.")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lock(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(description=f"{channel.name} has been locked 🔒", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=20)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

    @vc.command(description="Unlock the current voice channel.")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(description=f"{channel.name} has been unlocked 🔓", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=20)

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)
    
    @slash_command(name="VC Deafen", description="Deafen a user in the voice channel.", guild_ids=None)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def deafen(self, ctx, member: Option(discord.Member, description="Mention the user to deafen.", required=True)):
        if ctx.author.top_role > member.top_role or ctx.guild.owner == ctx.author:
            if member.guild_permissions.ban_members and ctx.guild.owner != ctx.author:
                embed = discord.Embed(description="Something went wrong, please try again.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else: 
                await member.edit(deafen=True)
                await ctx.respond(f"{member.mention} was deafened in the VC.")
        else:
            embed = discord.Embed(description="You can't deafen this user.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)
         
    @deafen.error
    async def deafen_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description="You don't have permission to run this command.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)
    
    @slash_command(name="VC Undeafen", description="Undeafen a user in the voice channel.", guild_ids=None)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def undeafen(self, ctx, member: Option(discord.Member, description="Mention the user to undeafen.", required=True)):
        asdf = ctx.author
        f = member.top_role
        h = asdf.top_role
        if h > f or ctx.guild.owner == ctx.author and not member == ctx.author:
            if member.guild_permissions.ban_members and not ctx.guild.owner == ctx.author:
                embed = discord.Embed(description=f"Something went wrong please try again.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else: 
                await member.edit(deafen=False)
                await ctx.respond(f"{member.mention} was undeafen in the VC.")
        else:
            if member == ctx.author:
                embed = discord.Embed(description=f"You were never deafen and you can't undeafen yourself.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)
            else:
                embed = discord.Embed(description=f"Hmm don't try to break, that person has a higher or equal role to you.", color=0xD684FF)
                await ctx.respond(embed=embed, delete_after=10)

    @undeafen.error
    async def undeafen_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description=f"Oh no! you don't have the permission to run this commands.", color=0xD684FF)
            await ctx.respond(embed=embed, delete_after=10)

def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin cog is loaded!")

import discord
from discord.ext import commands

import sys

command_attrs = {
    'hidden': True
}

class Owner(commands.Cog, name='Owner Commands', command_attrs=command_attrs):
    def __init__(self, bot):
        self.bot = bot

    """ Shutdown Bot """
    @commands.command(name='shutdown', aliases=['quit'], hidden=True)
    async def shutdown(self, ctx):
        await ctx.send('**`Shutting Down`** Goodbye.')
        await self.bot.logout()
        sys.exit(0)

    """ Restart Bot """
    @commands.command(name='restart', aliases=['reboot'], hidden=True)
    async def restart(self, ctx):
        await ctx.send('**`Rebooting`**')
        await self.bot.logout()
        sys.exit(6)

    """ Change Bot Activity """
    @commands.command(name='activity', aliases=['change_activity'], hidden=True)
    async def activity(self, ctx, type: str, *, name: str):
        # Checking which activity type was specified
        type = type.lower()
        if type == 'playing':
            activity_type = discord.ActivityType.playing
        elif type == 'watching':
            activity_type = discord.ActivityType.watching
        elif type == 'listening':
            activity_type = discord.ActivityType.listening
        elif type == 'streaming':
            activity_type = discord.ActivityType.streaming

        guild_count = len(self.bot.guilds)
        member_count = len(list(self.bot.get_all_members()))
        name = name.format(guilds=guild_count, members=member_count)

        # Setting bot activity
        await self.bot.change_presence(activity=discord.Activity(type=activity_type, name=name))
        await ctx.send(f'**`Success:`** bot activity has been changed')

    """ Change Bot Status """
    @commands.command(name='status', hidden=True)
    async def status(self, ctx, status: str):
        # Check which status was specified
        status = status.lower()
        if status in ['offline', 'off', 'invisible', 'ghost']:
            bot_status = discord.Status.invisible
        elif status in ['idle', 'waiting']:
            bot_status = discord.Status.idle
        elif status in ['dnd', 'disturb', 'away']:
            bot_status = discord.Status.dnd
        else:
            # Default to online status
            bot_status = discord.Status.online

        # Setting bot status
        try:
            await self.bot.change_presence(status=bot_status)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS:`** bot status changed to { bot_status }')

    """ Owner Check """
    async def cog_check(self, ctx):
        # Making sure author of these commands is the bot owner
        return await ctx.bot.is_owner(ctx.author)

    """ Error Check """
    async def cog_command_error(self, ctx, error):
        # Handling any errors within commands
        await ctx.send(f'Error in { ctx.command.qualified_name }: { error }')

def setup(bot):
    bot.add_cog(Owner(bot))
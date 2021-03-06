import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Mod(commands.Cog, name="Moderator Commands"):
    def __init__(self, bot):
        self.bot = bot

    """ Kick Member """
    @commands.command()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member=None, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = None

        # Kick member
        try:
            await member.kick(reason=reason)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS`** User { member.display_name } has been kicked')

    """ Ban Member """
    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member=None, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = None

        # Ban member
        try:
            await member.ban(reason=reason)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS:`** User { member.display_name } has been banned')

    """ Unban Member """
    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, member: int=None, *reason):
        if reason:
            reason = ' '.join(reason)
        else:
            reason = None
        user = await self.bot.fetch_user(member)

        # Unban Member
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS: `** User { user.display_name } has been unbanned')
        
    """ Add Role """
    @commands.command(aliases=['setrole', 'ar', 'sr'])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def addrole(self, ctx, member: discord.Member=None, *role):
        role = discord.utils.get(ctx.guild.roles, name=' '.join(role))
        
        # Add role to member
        try:
            await member.add_roles(role)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS:`** role { role.name } added to { member.display_name }')

    """ Remove Role """
    @commands.command(aliases=['rmrole', 'rr'])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def removerole(self, ctx, member: discord.Member=None, *role):
        role = discord.utils.get(ctx.guild.roles, name=' '.join(role))

        # Remove role from member
        try:
            await member.remove_roles(role)
        except Exception as e:
            # Handle errors if any
            await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
        else:
            await ctx.send(f'**`SUCCESS:`** role { role.name } removed from { member.display_name }')

    """ Error Check """
    async def cog_command_error(self, ctx, error):
        # Handling any errors within commands
        await ctx.send(f'Error in { ctx.command.qualified_name }: { error }')

def setup(bot):
    bot.add_cog(Mod(bot))
import discord
from discord.ext import commands
from datetime import datetime
from lib import database, checks
from constants.emojis import MAIN_EMOJIS


async def setup_guild(guild_id, guild_data):
    guild_data['guilds'][guild_id] = {'verify': False,
                                      'verifyname': '{discord}',
                                      'verifyrole': 0}
    await database.store_data('guild_info', guild_data, 'celestial', 'discord')
    return guild_data


class Config(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.check(checks.is_admin)
    async def config(self, ctx):
        guild_data = await database.get_data('guild_info', 'celestial', 'discord')

        # Check If Guild Database Exists
        if str(ctx.guild.id) not in guild_data['guilds']:
            guild_data = await setup_guild(str(ctx.guild.id), guild_data)

        verify_role = guild_data['guilds'][str(ctx.guild.id)]['verifyrole']
        verify_status = guild_data['guilds'][str(ctx.guild.id)]['verify']
        verify_name = guild_data['guilds'][str(ctx.guild.id)]['verifyname']
        role_mention = (f"<@&{verify_role}>" if verify_role != 0 else '**None**')

        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_footer(text='sb!config')

        embed.add_field(name='Verification',
                        value=f"More Info: `sb!verifyhelp`\n"
                              f"Status: **{MAIN_EMOJIS['True'] if verify_status is True else MAIN_EMOJIS['False']} |** `sb!toggle verify`\n"
                              f"Name: `{verify_name}` **|** `sb!verifyname <string>`\n"
                              f"Role: {role_mention} **|** `sb!verifyrole <role id>`")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.check(checks.is_admin)
    async def toggle(self, ctx, command):
        guild_data = await database.get_data('guild_info', 'celestial', 'discord')
        verify_status = guild_data['guilds'][str(ctx.guild.id)]['verify']

        if command.lower() == 'verify':
            guild_data['guilds'][str(ctx.guild.id)]['verify'] = (True if verify_status is False else False)
            verify_status = (True if verify_status is False else False)
            await database.store_data('guild_info', guild_data, 'celestial', 'discord')
            embed = discord.Embed(description=f"**Toggle Commands**\n"
                                              f"Toggled Verify: **{MAIN_EMOJIS[f'{verify_status}']}**",
                                  color=discord.Colour.gold(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='sb!toggle <command>')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.check(checks.is_admin)
    async def verifyname(self, ctx, *, input_string):
        string = ''.join(key for key in input_string if len(input_string) > 1)

        guild_data = await database.get_data('guild_info', 'celestial', 'discord')
        guild_data['guilds'][str(ctx.guild.id)]['verifyname'] = string
        await database.store_data('guild_info', guild_data, 'celestial', 'discord')

        embed = discord.Embed(description=f"**Verify Name**\n"
                                          f"String: `{string}`",
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text='sb!verifyname <string>')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.check(checks.is_admin)
    async def verifyrole(self, ctx, role: discord.Role):
        guild_data = await database.get_data('guild_info', 'celestial', 'discord')
        guild_data['guilds'][str(ctx.guild.id)]['verifyrole'] = role.id
        await database.store_data('guild_info', guild_data, 'celestial', 'discord')

        embed = discord.Embed(description=f"**Verify Role**\n"
                                          f"Role: {role.mention}",
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text='sb!verifyrole <role id>')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Config(client))


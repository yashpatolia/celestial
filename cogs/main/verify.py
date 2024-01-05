import discord
import logging
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from lib import database
from lib.common_functions import get_skyblock_player
from api_wrapper.utils.errors import InvalidIGN


class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def verify(self, ctx, mc_name=None, profile=None):
        guild_data = await database.get_data('guild_info', 'celestial', 'discord')
        logging.info(f'COMMAND Verify\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n')

        if str(ctx.guild.id) in guild_data['guilds'] and guild_data['guilds'][str(ctx.guild.id)]['verify'] is True:
            name_template = guild_data['guilds'][str(ctx.guild.id)]['verifyname']
            role_id = guild_data['guilds'][str(ctx.guild.id)]['verifyrole']
            call_hypixel_data = (True if ('{cata}' in name_template or '{class}' in name_template or '{ign}' in name_template) else False)
            call_skyblock_data = (True if ('{cata}' in name_template or '{class}' in name_template) else False)
            if call_hypixel_data and mc_name is None:
                raise InvalidIGN
            print(call_skyblock_data)
            player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=call_skyblock_data, call_hypixel_data=call_hypixel_data)
            valid_discord = True

            name_template = name_template.replace('{discord}', ctx.author.name)
            if call_hypixel_data is True and player.linked_discord.lower() == str(ctx.author).lower():
                name_template = name_template.replace('{ign}', player.mc_name)
                if call_skyblock_data:
                    name_template = name_template.replace('{cata}', str(player.cata_level))
                    name_template = name_template.replace('{class}', player.dungeon_class[0])
            elif call_hypixel_data is True and player.linked_discord.lower() != str(ctx.author).lower():
                valid_discord = False
                embed = discord.Embed(description=f'Discord not set correctly on Hypixel!',
                                      color=discord.Colour.red(),
                                      timestamp=datetime.utcnow())
                embed.set_footer(text='sb!verify <name>')
                await ctx.send(embed=embed)

            if valid_discord is True:
                try:
                    await ctx.author.edit(nick=f'{name_template}')
                except Exception as e:
                    pass

                if int(role_id) != 0:
                    verify_role = get(ctx.guild.roles, id=int(role_id))
                    if verify_role not in ctx.author.roles:
                        await ctx.author.add_roles(verify_role)

                if call_hypixel_data:
                    description = f'Successfully verified as: **{player.mc_name}**'
                else:
                    description = f'Successfully verified!'

                embed = discord.Embed(description=description,
                                      color=discord.Colour.gold(),
                                      timestamp=datetime.utcnow())
                embed.set_footer(text='sb!verify <name>')
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Verify(client))

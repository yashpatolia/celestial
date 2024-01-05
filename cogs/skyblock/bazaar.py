import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from api_wrapper.utils.errors import NoItemSpecified


class Bazaar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bz'])
    @commands.guild_only()
    async def bazaar(self, ctx, *, item_name=None):
        if item_name is None:
            raise NoItemSpecified
        player, leaderboard_data = await get_skyblock_player(call_bazaar_data=True)
        logging.info(f'COMMAND Bazaar\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})')

        amount = 1
        item_list = list(item_name.split(' '))

        # Amount
        item_list[0] = item_list[0].replace(',', '')
        if item_list[0].isdecimal():
            amount = (int(item_list[0]) if int(item_list[0]) > 0 else 1)
            item_list.pop(0)

        item_query = ' '.join(item for item in item_list)
        item_name = await common_functions.get_matches(item_query, player.bazaar_info.keys())
        item_image = f"https://sky.lea.moe/item/{player.bazaar_info[item_name]['id']}"

        embed = discord.Embed(description=f'Item: **{item_name} |** Quantity: **{amount}**',
                              color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name='Bazaar')
        embed.set_footer(text='sb!bazaar [amount] <item>')
        embed.add_field(name='Product Info', value=f"Instant Buy: **{await common_functions.get_suffix(player.bazaar_info[item_name]['instant_buy'] * amount, True)}**\nInstant Sell: **{await common_functions.get_suffix(player.bazaar_info[item_name]['instant_sell'] * amount, True)}**")
        embed.set_thumbnail(url=f'{item_image}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Bazaar(client))

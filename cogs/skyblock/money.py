import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from constants.emojis import PROFILE_EMOJIS, MONEY_EMOJIS


class Money(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bank', 'purse'])
    @commands.guild_only()
    async def money(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Money\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')
        
        if isinstance(player.bank, int):
            player.bank = f'{player.bank:,}'
        
        embed = discord.Embed(color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=f"{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]")
        embed.set_footer(text='sb!bank <name> [profile]')
        
        embed.add_field(name='Money', value=f"{MONEY_EMOJIS['purse']} Purse\n"
                                            f"{MONEY_EMOJIS['bank']} Bank")
        embed.add_field(name='\u200b', value=f"**{player.purse:,}**\n"
                                             f" **{player.bank}**")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Money(client))

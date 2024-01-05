import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from constants.emojis import COOP_UPGRADE_EMOJIS, PROFILE_EMOJIS


class CoopUpgrades(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['upgrades', 'coopupgrades'])
    @commands.guild_only()
    async def upgrade(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Coop Upgrades\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        upgrades_text = ''
        for key, value in player.coop_upgrades.items():
            upgrades_text += f'{COOP_UPGRADE_EMOJIS[key]} {value["name"]}: **{value["level"]}** / {value["max_level"]}\n'

        embed = discord.Embed(description=f'**Currently Upgrading:** {player.currently_upgrading}',
                              color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!upgrades <name> [profile]')
        embed.add_field(name='Coop Upgrades', value=f'{upgrades_text}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CoopUpgrades(client))

import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from constants.emojis import PROFILE_EMOJIS, SLAYER_EMOJIS


class Slayer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['slayers'])
    @commands.guild_only()
    async def slayer(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Slayer\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')
        
        slayer_level_text = ""
        slayer_xp_text = ""
        for key, value in player.slayer_info.items():
            slayer_level_text += f"{SLAYER_EMOJIS[key]} {value['name']} **{value['level']}**\n"
            slayer_xp_text += f"**{value['xp']:,}** XP\n"
        
        embed = discord.Embed(description=f"Total Slayer: **{player.total_slayer_xp:,}** XP\n",
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!slayer <name> [profile]')
        
        embed.add_field(name='Slayer Stats', value=f'{slayer_level_text}')
        embed.add_field(name='\u200b', value=f'{slayer_xp_text}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Slayer(client))

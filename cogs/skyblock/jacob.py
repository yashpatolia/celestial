import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from constants.emojis import MEDAL_EMOJIS, ANITA_UPGRADE_EMOJIS, MAIN_EMOJIS, JACOBS_CROPS_EMOJIS,PROFILE_EMOJIS


class Jacob(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['jacobs', 'farming'])
    @commands.guild_only()
    async def jacob(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Jacobs\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        jacobs_medals_text = ''
        for medal_name, medal_amount in player.jacob_medals.items():
            jacobs_medals_text += f'{MEDAL_EMOJIS[medal_name]} {medal_name.capitalize()}: **{medal_amount}**\n'

        anita_text = f"{ANITA_UPGRADE_EMOJIS['double_drops']} Double Drops: **{player.jacob_upgrades['double_drops']['level'] * 2}% / {player.jacob_upgrades['double_drops']['max_level'] * 2}%**\n{ANITA_UPGRADE_EMOJIS['farming_level_cap']} Farming Level Cap: **{player.jacob_upgrades['farming_level_cap']['level']} / {player.jacob_upgrades['farming_level_cap']['max_level']}**"

        highscore_text = ''
        unique_gold_text = ''
        for crop_name, crop_value in player.jacob_info.items():
            highscore_text += f"{JACOBS_CROPS_EMOJIS[crop_name]} {crop_value['name']} **{crop_value['highscore']:,}**\n"
            unique_gold_text += f"{JACOBS_CROPS_EMOJIS[crop_name]} {crop_value['name']} {MAIN_EMOJIS[str(crop_value['gold_status'])]}\n"

        embed = discord.Embed(description=f"Farming Level: **{await common_functions.get_skill_level(player.skills_info['experience_skill_farming']['xp'])}**", color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!jacob <name> [profile]')
        embed.add_field(name='Jacob\'s Medals', value=f'{jacobs_medals_text}')
        embed.add_field(name='Anita Purchases', value=f'{anita_text}')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='Highscores', value=f'{highscore_text}')
        embed.add_field(name='Unique Golds', value=f'{unique_gold_text}')
        embed.add_field(name='\u200b', value='\u200b')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Jacob(client))

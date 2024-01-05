import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from constants.skyblock import *
from constants.emojis import PROFILE_EMOJIS, SKILL_EMOJIS
from api_wrapper.utils.errors import *


class Skills(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['skills'])
    @commands.guild_only()
    async def skill(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Skills\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        skill_avg = 0
        true_skill_avg = 0
        # Get all skills (excluding Runecrafting & Carpentry)
        for skill_name, skill_value in player.skills_info.items():
            if skill_name not in BLACKLISTED_SKILLS:
                skill_level = await common_functions.get_skill_level(skill_value['xp'])
                true_skill_avg += min(skill_level, SKILLS_TEMPLATE[skill_name]['max_level'])
                skill_avg += (min(skill_level, SKILLS_TEMPLATE[skill_name]['max_level']) + ((skill_value['xp'] - SKILL_XP_TABLE[skill_level]) / (SKILL_INDIVIDUAL_XP_TABLE[skill_level + 1]) if skill_level < SKILLS_TEMPLATE[skill_name]['max_level'] else 0))

        # Calculate Skill Avg. & True Skill Avg.
        true_skill_avg /= (len(list(player.skills_info.keys())) - len(BLACKLISTED_SKILLS))
        skill_avg /= (len(list(player.skills_info.keys())) - len(BLACKLISTED_SKILLS))

        embed = discord.Embed(description=f"Total XP: **{await common_functions.get_suffix(round(player.total_xp))} |** Skill Avg. **{round(skill_avg, 2)} |** True Skill Avg. **{round(true_skill_avg, 2)}**",
                              color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!skills <name> [profile]')

        for skill_name, skill_value in player.skills_info.items():
            runecrafting = False
            if skill_name == 'experience_skill_runecrafting':
                runecrafting = True
            skill_level = await common_functions.get_skill_level(skill_value['xp'], runecrafting)
            embed.add_field(name=f"{SKILL_EMOJIS[skill_name]} {skill_value['name']} {skill_level}", value=f"**{await common_functions.get_suffix(round(skill_value['xp']) - SKILL_XP_TABLE[skill_level]) if runecrafting is False else await common_functions.get_suffix(round(skill_value['xp']) - RUNECRAFTING_XP_TABLE[skill_level])}** {f'/ {await common_functions.get_suffix(SKILL_INDIVIDUAL_XP_TABLE[skill_level + 1]) if runecrafting is False else await common_functions.get_suffix(RUNECRAFTING_INDIVIDUAL_XP_TABLE[skill_level + 1])}' if skill_level < (SKILLS_TEMPLATE[skill_name]['max_level'] if skill_name in BLACKLISTED_SKILLS else 60) else ''} (**{await common_functions.get_suffix(round(skill_value['xp']))}**)")
        if skill_avg == 0:
            raise APIDisabled
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Skills(client))

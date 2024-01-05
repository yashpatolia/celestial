import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from constants.emojis import PROFILE_EMOJIS, MILESTONE_EMOJIS


class PetMilestone(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ms', 'milestones'])
    @commands.guild_only()
    async def milestone(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Pet Milestone\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')
        
        embed = discord.Embed(color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=f"{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]")
        embed.set_footer(text='sb!milestone <name> [profile]')
        
        embed.add_field(name='Pet Milestones', value=f"{MILESTONE_EMOJIS['rock']} {player.rock_rarity}\n"
                                                     f"{MILESTONE_EMOJIS['dolphin']} {player.dolphin_rarity}")
        embed.add_field(name='\u200b', value=f"**{player.rock_milestone:,}** {f'/ {player.next_rock_milestone:,}' if player.next_rock_milestone != 'Complete' else ''}\n"
                                             f"**{player.dolphin_milestone:,}** {f'/ {player.next_dolphin_milestone:,}' if player.next_dolphin_milestone != 'Complete' else ''}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PetMilestone(client))

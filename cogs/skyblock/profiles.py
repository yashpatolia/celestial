import discord
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from constants.emojis import PROFILE_EMOJIS


class Profiles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['profiles'])
    @commands.guild_only()
    async def profile(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        
        profiles_text = ''
        profiles_text += f"**Latest:** \{PROFILE_EMOJIS[player.latest_profile_name.lower()]} {player.latest_profile_name}\n"
        for profile in player.profiles:
            if profile != player.latest_profile_name:
                profiles_text += f"\{PROFILE_EMOJIS[profile.lower()]} {profile}\n"
        
        embed = discord.Embed(description=f'{profiles_text}',
                              color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} Profiles')
        embed.set_footer(text='sb!profiles <name> [profile]')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Profiles(client))

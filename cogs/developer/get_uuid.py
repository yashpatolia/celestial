from discord.ext import commands
from lib import checks
from lib.common_functions import get_skyblock_player


class GetUUID(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(checks.is_developer)
    async def uuid(self, ctx, mc_name):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=None)
        await ctx.send(player.uuid)


def setup(client):
    client.add_cog(GetUUID(client))

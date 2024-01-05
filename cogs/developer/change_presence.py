import discord
from discord.ext import commands
from lib import checks


class ChangePresence(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(checks.is_developer)
    async def playing(self, ctx, *, game):
        game = discord.Game(game)
        await self.client.change_presence(status=discord.Status.idle, activity=game)
        await ctx.message.delete()


def setup(client):
    client.add_cog(ChangePresence(client))

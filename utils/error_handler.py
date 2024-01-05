import discord
import logging
from discord.ext import commands
from api_wrapper.utils.errors import *
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    datefmt="[%Y/%m/%d %X]",
    format="%(message)s"
)


class ErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        # Invalid IGN
        if isinstance(error, InvalidIGN):
            embed = discord.Embed(description='**Invalid IGN Provided!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # Skyblock API
        elif isinstance(error, SkyblockAPIError):
            embed = discord.Embed(description='**Skyblock API Error!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # Hypixel API
        elif isinstance(error, HypixelAPIError):
            embed = discord.Embed(description='**Hypixel API Error!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # Bazaar API
        elif isinstance(error, BazaarAPIError):
            embed = discord.Embed(description='**Bazaar API Error!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # No Profiles
        elif isinstance(error, NoProfilesFound):
            embed = discord.Embed(description='**No Profiles Found!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # API Disabled
        elif isinstance(error, APIDisabled):
            embed = discord.Embed(description='**API Disabled!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # No Jacob Data
        elif isinstance(error, NoJacobData):
            embed = discord.Embed(description='**No Jacob Data!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # No Item Specified
        elif isinstance(error, NoItemSpecified):
            embed = discord.Embed(description='**No Item Specified!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)

        # Role Not Found
        elif isinstance(error, discord.ext.commands.RoleNotFound):
            embed = discord.Embed(description='**Invalid Role!**',
                                  color=discord.Colour.red(),
                                  timestamp=datetime.utcnow())
            embed.set_footer(text='Error')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ErrorHandler(client))

import os
from discord.ext import commands
from lib import checks
from constants.bot_config import BOT_ID, BOT_PREFIXES
from constants.emojis import MAIN_EMOJIS
from lib.cache_auction_house import auction_house_cache

client = commands.Bot(command_prefix=BOT_PREFIXES, help_command=None, owner_id=249592874285531137)

# Skyblock Cogs
for folder in os.listdir('./cogs'):
    for filename in os.listdir(f'./cogs/{folder}'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{folder}.{filename[:-3]}')

# Util Cogs
for filename in os.listdir(f'./utils'):
    if filename.endswith('.py'):
        client.load_extension(f'utils.{filename[:-3]}')


# On Startup
@client.event
async def on_ready():
    print('Bot Loaded!')


# Load Cog
@client.command(aliases=['enable'])
@commands.check(checks.is_developer)
async def load(ctx, in_folder, extension):
    client.load_extension(f'{in_folder}.{extension}')
    await ctx.message.add_reaction(MAIN_EMOJIS['True'])


# Unload Cog
@client.command(aliases=['disable'])
@commands.check(checks.is_developer)
async def unload(ctx, in_folder, extension):
    client.unload_extension(f'{in_folder}.{extension}')
    await ctx.message.add_reaction(MAIN_EMOJIS['True'])


# Start Auction House Caching
@client.command()
@commands.check(checks.is_developer)
async def startahcaching(ctx):
    await ctx.message.add_reaction(MAIN_EMOJIS['True'])
    await auction_house_cache(client)

client.run(BOT_ID)

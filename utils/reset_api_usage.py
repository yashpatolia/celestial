from discord.ext import commands, tasks
from lib import database


class ResetAPI(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reset_usage.start()

    @tasks.loop(seconds=60)
    async def reset_usage(self):
        api_usage = await database.get_data('guild_info', 'celestial', 'discord')

        # API Over Usage
        if api_usage['api_usage'] > 100:
            user = self.client.get_user(249592874285531137)
            await user.send('API Overused!')

        api_usage['api_usage'] = 0
        await database.store_data('guild_info', api_usage, 'celestial', 'discord')


def setup(client):
    client.add_cog(ResetAPI(client))

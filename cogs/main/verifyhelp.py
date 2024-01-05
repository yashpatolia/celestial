import discord
from discord.ext import commands
from datetime import datetime
from lib import checks


class VerifyHelp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.check(checks.is_admin)
    async def verifyhelp(self, ctx):
        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_footer(text='sb!verifyhelp')
        embed.add_field(name='__Set Verify Name__', value="**Command:** `sb!verifyname <string>`\n"
                                                          "**Note #1:** This will set nicks of users who verify with `sb!verify <name>`.\n"
                                                          "**Note #2:** Keep in mind the discord name limit **(32 Characters)**.\n"
                                                          "String can include the following data:\n"
                                                          "`{discord}` - Discord Name\n"
                                                          "`{ign}`     - Minecraft IGN\n"
                                                          "`{cata}`    - Catacombs Level\n"
                                                          "`{class}`   - Dungeon Class (First Letter) Ex: `A`\n\n"
                                                          "**Example String:** `[{class}] <{cata}> {ign}`\n"
                                                          "**Nick Will Set To:** `[M] <36> Seazyns`\n"
                                                          "**Default:** `{discord}`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='__Set Verify Role__', value="Command: `sb!verifyrole <role>`\n"
                                                          "**Note #1:** This will give the users who verify with `sb!verify <name>` the role.\n"
                                                          "**Note #2:** Make sure the role you want to give is below Celestial's role.\n"
                                                          "**Note #3:** If you want no role to be given, set role_id to `0`\n\n"
                                                          "**Role ID Example:** `751133702364594287`\n"
                                                          "**Example Command:** `sb!verifyrole 751133702364594287` or `sb!verifyrole @Example`\n"
                                                          "**Default:** 0")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(VerifyHelp(client))

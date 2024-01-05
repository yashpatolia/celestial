import discord
from discord.ext import commands
from datetime import datetime
from constants.emojis import *


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(description='`<>: Required` **|** `[]: Optional`\n'
                                          'Join the discord: <https://discord.gg/T24XQ93>\n'
                                          'Support Celestial: <https://ko-fi.com/seazyns>',
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text='Created by: Seazyns#0001')

        embed.add_field(name='__Main Commands__', value="**Config\n"
                                                        "Invite Celestial\n"
                                                        "Celestial Stats**")
        embed.add_field(name='\u200b', value='sb!config\n'
                                             'sb!invite\n'
                                             'sb!stats')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='__Skyblock Commands__', value=f"**{MAIN_EMOJIS['Profiles']} Profiles\n"
                                                            f"{MONEY_EMOJIS['purse']} Bank / Purse\n"
                                                            f"{SLAYER_EMOJIS['zombie']} Slayers\n"
                                                            f"{MILESTONE_EMOJIS['dolphin']} Pet Milestones\n"
                                                            f"{COOP_UPGRADE_EMOJIS['minion_slots']} Coop Upgrades\n"
                                                            f"{CATACOMBS_EMOJIS['Floor 1']} Catacombs\n"
                                                            f"{SKILL_EMOJIS['experience_skill_combat']} Skills\n"
                                                            f"{JACOBS_CROPS_EMOJIS['WHEAT']} Jacobs Events\n"
                                                            f"{SKILL_EMOJIS['experience_skill_alchemy']} Alchemy Calculator\n"
                                                            f"{MEDAL_EMOJIS['gold']} Bazaar\n"
                                                            f"{MAIN_EMOJIS['Weight']} Weight**")
        embed.add_field(name='\u200b',
                        value='sb!profiles <name>\n'
                              'sb!money <name> [profile]\n'
                              'sb!slayer <name> [profile]\n'
                              'sb!milestone <name> [profile]\n'
                              'sb!upgrades <name> [profile]\n'
                              'sb!cata <name> [profile]\n'
                              'sb!skills <name> [profile]\n'
                              'sb!jacob <name> [profile]\n'
                              'sb!alch <name> [wanted level] [profile]\n'
                              'sb!bz [amount] <item>\n'
                              'sb!we <name> [profile]')
        embed.add_field(name='\u200b', value='\u200b')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))

import discord
from datetime import datetime
from discord.ext import commands


class Celestial(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['stats', 'stat'])
    @commands.guild_only()
    async def info(self, ctx):
        servers_text = ''
        members_text = ''
        total_members = 0

        sorted_list = sorted(self.client.guilds, key=lambda var: var.member_count, reverse=True)
        for item in sorted_list:
            total_members += int(item.member_count)
        for x in range(0, min(10, len(self.client.guilds))):
            servers_text += f"{sorted_list[x]}\n"
            members_text += f"**{sorted_list[x].member_count}** Members\n"

        embed = discord.Embed(description=f'Supporting **{total_members:,}** users across **{len(self.client.guilds)}** Servers!',
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=f'Celestial Info')
        embed.set_footer(text='sb!info')
        embed.add_field(name='Top Servers', value=f'{servers_text}')
        embed.add_field(name='\u200b', value=f'{members_text}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['getinvite'])
    @commands.guild_only()
    async def invite(self, ctx):
        embed = discord.Embed(description='[Celestial Invite Link](https://discord.com/api/oauth2/authorize?client_id=736290426461618307&permissions=355392&scope=bot%20applications.commands "Click Here!")',
                              color=discord.Colour.gold(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=f'Celestial Invite')
        embed.set_footer(text='sb!invite')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Celestial(client))

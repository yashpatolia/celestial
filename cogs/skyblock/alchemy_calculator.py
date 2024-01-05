import discord
import asyncio
import math
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from constants.emojis import ALCHEMY_EMOJIS, PROFILE_EMOJIS, MAIN_EMOJIS, SKILL_EMOJIS
from constants.skyblock import SKILL_XP_TABLE
from api_wrapper.api_data import get_bazaar_data
# from api_wrapper.skyblock_data import get_bazaar_info


async def get_alchemy_boost(player, god_pot, cookie, barry, derpy, two_x_multiplier):
    base_boost = 1
    if player.slayer_info['spider']['level'] > 7:
        base_boost *= 1.1
    if god_pot is True:
        base_boost *= 1.2
    if cookie is True:
        base_boost *= 1.2
    if barry is True:
        base_boost *= 1.15
    if derpy is True:
        base_boost *= 1.5
    if two_x_multiplier is True:
        base_boost *= 2
    return base_boost


class Alchemy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['alch', 'alchemy'])
    @commands.guild_only()
    async def alc(self, ctx, mc_name=None, wanted_level=50, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True, call_bazaar_data=True)
        logging.info(f'COMMAND Alchemy\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        alchemy_level = await common_functions.get_skill_level(player.skills_info['experience_skill_alchemy']['xp'])

        if alchemy_level >= 50 and (wanted_level < 50 or wanted_level > 60):
            wanted_level = 60
        if 60 > alchemy_level >= wanted_level:
            wanted_level = alchemy_level + 1

        alchemy_calculator_reactions = [ALCHEMY_EMOJIS['god_pot'], ALCHEMY_EMOJIS['booster_cookie'], ALCHEMY_EMOJIS['barry'],
                                        ALCHEMY_EMOJIS['derpy'], ALCHEMY_EMOJIS['two_x_multiplier'], MAIN_EMOJIS['True']]
        god_pot = False
        booster_cookie = False
        mayor_barry = False
        mayor_derpy = False
        two_x_multiplier = False
        run = (True if alchemy_level < 60 else False)

        embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!alchemy <name> [wanted-level] [profile]')

        embed.description = (f"React with {MAIN_EMOJIS['True']} when done!\n"
                             f"**__Calculator Options__**\n"
                             f"{alchemy_calculator_reactions[0]} God Pot: **{MAIN_EMOJIS[f'{god_pot}']}**\n"
                             f"{alchemy_calculator_reactions[1]} Booster Cookie: **{MAIN_EMOJIS[f'{booster_cookie}']}**\n"
                             f"{alchemy_calculator_reactions[2]} Mayor Barry: **{MAIN_EMOJIS[f'{mayor_barry}']}**\n"
                             f"{alchemy_calculator_reactions[3]} Mayor Derpy: **{MAIN_EMOJIS[f'{mayor_derpy}']}**\n"
                             f"{alchemy_calculator_reactions[4]} 2x Multiplier: **{MAIN_EMOJIS[f'{two_x_multiplier}']}**"
                             if alchemy_level < 60 else
                             f"Alchemy Level: **{alchemy_level}** (**{await common_functions.get_suffix(round(player.skills_info['experience_skill_alchemy']['xp']))}** XP)\n"
                             f"You are already the highest known alchemy level: **60**")

        calculator = await ctx.send(embed=embed)
        if alchemy_level < 60:
            for reaction in alchemy_calculator_reactions:
                await calculator.add_reaction(reaction)

            while run:
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in alchemy_calculator_reactions and reaction.message.id == calculator.id
                try:
                    reaction = await self.client.wait_for('reaction_add', timeout=120, check=check)
                except asyncio.TimeoutError:
                    for reaction in alchemy_calculator_reactions:
                        await calculator.clear_reaction(reaction)
                else:
                    if str(reaction[0]) == f"{alchemy_calculator_reactions[0]}":
                        god_pot = (True if god_pot is False else False)
                    elif str(reaction[0]) == f"{alchemy_calculator_reactions[1]}":
                        booster_cookie = (True if booster_cookie is False else False)
                    elif str(reaction[0]) == f"{alchemy_calculator_reactions[2]}":
                        mayor_barry = (True if mayor_barry is False else False)
                    elif str(reaction[0]) == f"{alchemy_calculator_reactions[3]}":
                        mayor_derpy = (True if mayor_derpy is False else False)
                    elif str(reaction[0]) == f"{alchemy_calculator_reactions[4]}":
                        two_x_multiplier = (True if two_x_multiplier is False else False)
                    elif str(reaction[0]) == f"{alchemy_calculator_reactions[5]}":
                        await calculator.clear_reactions()

                        alchemy_boost = await get_alchemy_boost(player, god_pot, booster_cookie, mayor_barry, mayor_derpy, two_x_multiplier)
                        material_amount = math.ceil(((SKILL_XP_TABLE[wanted_level]) - player.skills_info['experience_skill_alchemy']['xp']) / (45000 * alchemy_boost))
                        cane_price = round(player.bazaar_info['Enchanted Sugar Cane']['instant_buy'])
                        cane_resell_value = (5833 * 3) * material_amount
                        spidereye_price = round(player.bazaar_info['Enchanted Fermented Spider Eye']['instant_buy'])
                        spidereye_resell_value = (12900 * 3) * material_amount

                        embed.description = f"{SKILL_EMOJIS['experience_skill_alchemy']} Alchemy Level: **{alchemy_level}** (**{await common_functions.get_suffix(round(player.skills_info['experience_skill_alchemy']['xp']))}** / {await common_functions.get_suffix(SKILL_XP_TABLE[wanted_level])}) **|** Wanted Level: **{wanted_level}**\n" \
                                            f"**Tip #1:** Brew normal {ALCHEMY_EMOJIS['glowstone']} after brewing pots to resell for more money.\n" \
                                            f"**Tip #2:** Brew enchanted {ALCHEMY_EMOJIS['redstone_lamp']} after brewing pots (no {ALCHEMY_EMOJIS['glowstone']}) to resell for more money if {ALCHEMY_EMOJIS['redstone_lamp']} are below 68.5k per.\n" \
                                            f"**Note:** Prices - Instant Buy | Resell - Brew normal {ALCHEMY_EMOJIS['glowstone']}."
                        embed.add_field(name=f"{ALCHEMY_EMOJIS['sugar_cane']} Enchanted Sugar Cane", value=f"Amount: **{material_amount}**\n"
                                                                                                           f"Price Per Unit: **{await common_functions.get_suffix(cane_price)}**\n"
                                                                                                           f"Total Without Resell: **{await common_functions.get_suffix(material_amount * cane_price)}**\n"
                                                                                                           f"Total With Resell: **{await common_functions.get_suffix(material_amount * cane_price - cane_resell_value)}**")
                        embed.add_field(name=f"{ALCHEMY_EMOJIS['spider_eye']} Enchanted Fermented Spider-Eye", value=f"Amount: **{material_amount}**\n"
                                                                                                                     f"Price Per Unit: **{await common_functions.get_suffix(spidereye_price)}**\n"
                                                                                                                     f"Total Without Resell: **{await common_functions.get_suffix(material_amount * spidereye_price)}**\n"
                                                                                                                     f"Total With Resell: **{await common_functions.get_suffix(material_amount * spidereye_price - spidereye_resell_value)}**")
                        await calculator.edit(embed=embed)
                        break
                    if run is True:
                        await calculator.remove_reaction(str(reaction[0]), ctx.author)
                        embed.description = f"React with {MAIN_EMOJIS['True']} when done!\n" \
                                            f"**__Calculator Options__**\n" \
                                            f"{alchemy_calculator_reactions[0]} God Pot: **{MAIN_EMOJIS[f'{god_pot}']}**\n" \
                                            f"{alchemy_calculator_reactions[1]} Booster Cookie: **{MAIN_EMOJIS[f'{booster_cookie}']}**\n" \
                                            f"{alchemy_calculator_reactions[2]} Mayor Barry: **{MAIN_EMOJIS[f'{mayor_barry}']}**\n" \
                                            f"{alchemy_calculator_reactions[3]} Mayor Derpy: **{MAIN_EMOJIS[f'{mayor_derpy}']}**\n" \
                                            f"{alchemy_calculator_reactions[4]} 2x Multiplier: **{MAIN_EMOJIS[f'{two_x_multiplier}']}**"
                        await calculator.edit(embed=embed)


def setup(client):
    client.add_cog(Alchemy(client))

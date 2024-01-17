from constants.bot_config import CELESTIAL_DEVELOPER


def is_developer(ctx):
    if ctx.author.id == CELESTIAL_DEVELOPER:
        return True


def is_tom_foolery(ctx):
    if ctx.author.id in [363199691946459136, CELESTIAL_DEVELOPER]:
        return True


def is_admin(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.id == CELESTIAL_DEVELOPER:
        return True

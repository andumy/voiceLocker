import os

import interactions
from interactions import GuildVoice, OptionType, SlashContext, slash_command, slash_option

bot = interactions.Client(token=os.environ['DISCORD_BOT_TOKEN'],
                          intents=interactions.Intents.GUILDS
                          | interactions.Intents.GUILD_VOICE_STATES)

interactions.listen()


async def on_startup():
  print("Bot is ready!")


@slash_command(
    name="lock_voice",
    description="Lock a voice channel",
)
@slash_option(name="push_id",
              description="Push Channel Id",
              required=True,
              opt_type=OptionType.INTEGER)
async def lock_voice(ctx: SlashContext, push_id: int):
  status = await toggleChannel(ctx, push_id, False)
  if (not status):
    return

  await ctx.send("Channel 'Push " + str(push_id) + "' is now locked.")


@slash_command(
    name="unlock_voice",
    description="Unlock a voice channel",
)
@slash_option(name="push_id",
              description="Push Channel Id",
              required=True,
              opt_type=OptionType.INTEGER)
async def unlock_voice(ctx: SlashContext, push_id: int):
  status = await toggleChannel(ctx, push_id, True)
  if (not status):
    return

  await ctx.send("Channel 'Push " + str(push_id) + "' is now unlocked.")


async def toggleChannel(ctx: SlashContext, push_id: int, can_connect: bool):
  await ctx.defer()

  if (ctx.guild_id is None):
    await ctx.send("Internal error: g100")
    return False

  guild = bot.get_guild(ctx.guild_id)
  if (guild is None):
    await ctx.send("Internal error: g101")
    return False

  selected_channel = None
  for channel in guild.channels:
    if (channel.name != "Push " + str(push_id)):
      continue

    if (type(channel) is GuildVoice):
      selected_channel = channel

  if (selected_channel is None):
    await ctx.send("Selected Channel doesn't exists")
    return False

  await selected_channel.set_permission(connect=can_connect,
                                        target=guild.default_role)

  return True


bot.start()

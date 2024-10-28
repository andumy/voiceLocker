import os

import interactions
from interactions import GuildVoice, OptionType, SlashContext, SlashCommandChoice, slash_command, slash_option, listen
from interactions.api.events import VoiceUserLeave, VoiceUserMove

bot = interactions.Client(token=os.environ['DISCORD_BOT_TOKEN'],
                          intents=interactions.Intents.GUILDS
                          | interactions.Intents.GUILD_VOICE_STATES)

async def on_startup():
  print("Bot is ready!")


@slash_command(
    name="lock_voice",
    description="Lock a voice channel",
)
@slash_option(name="push_id",
              description="Push Channel Id",
              required=True,
              opt_type=OptionType.INTEGER,
              choices=[
                  SlashCommandChoice(name="1", value=1),
                  SlashCommandChoice(name="2", value=2),
                  SlashCommandChoice(name="3", value=2)
              ]
)
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
              opt_type=OptionType.INTEGER,
              choices=[
                  SlashCommandChoice(name="1", value=1),
                  SlashCommandChoice(name="2", value=2),
                  SlashCommandChoice(name="3", value=2)
              ]
)
async def unlock_voice(ctx: SlashContext, push_id: int):
  status = await toggleChannel(ctx, push_id, True)
  if (not status):
    return

  await ctx.send("Channel 'Push " + str(push_id) + "' is now unlocked.")


async def toggleChannel(ctx: SlashContext, push_id: int, can_connect: bool):
  await ctx.defer()

  if(ctx.author.voice is None or ctx.author.voice.channel is None):
    await ctx.send("You cannot lock/unlock a channel you are not in.")
    return False

  if(ctx.author.voice.channel.name != "Push " + str(push_id)):
    await ctx.send("You cannot lock/unlock a channel you are not in.")
    return False

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

@listen()
async def on_voice_user_leave(event: VoiceUserLeave):
  if event.channel.name.startswith("Push"):
    if len(event.channel.voice_members) == 1: # the voice_members is part of the state before the leave. Having only 1 member means 
      await event.channel.set_permission(connect=True, target=event.channel.guild.default_role)

@listen()
async def on_voice_user_move(event: VoiceUserMove):
  if event.previous_channel.name.startswith("Push"):
    if len(event.previous_channel.voice_members) == 1: # the voice_members is part of the state before the leave. Having only 1 member means 
      await event.previous_channel.set_permission(connect=True, target=event.previous_channel.guild.default_role)


bot.start()

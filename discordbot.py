from discord.ext import commands
import os
import logging
import traceback


logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def join(ctx):
    voice_state = ctx.author.voice
    if not voice_state: return
    await voice_state.connect()


@bot.command()
async def disconnect(ctx):
    voice_client = ctx.voice_client
    if not voice_client: return
    await voice_client.disconnect()


bot.run(token)

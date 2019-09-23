from discord.ext import commands
import os
import logging
import traceback
import io
import sys
from contextlib import redirect_stdout
import textwrap

from discord import opus
import subprocess

def find_library(name):
    proc = subprocess.run(["find","/usr/lib", "-type", "f", "-name", f"*lib{name}.so*"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return proc.stdout.decode("utf8")

try:
    opus._lib = opus.libopus_loader((find_library("opus").split("/")[3][:-1]))
except Exception:
    pass
del opus

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print(f'logged on as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')

_ = None
@bot.command()
async def eval(ctx, *, body: str):
    """Evaluates a code"""
    global _
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': _
    }
    
    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            _ = ret
            await ctx.send(f'```py\n{value}{ret}\n```')


@bot.command()
async def join(ctx):
    voice_state = ctx.author.voice
    if not voice_state: return
    await voice_state.channel.connect()


@bot.command()
async def disconnect(ctx):
    voice_client = ctx.voice_client
    if not voice_client: return
    await voice_client.disconnect()


bot.run(token)

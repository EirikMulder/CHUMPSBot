import discord
from discord.ext import commands
import os

# bot = discord.client()
bot = commands.Bot(command_prefix="!")



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hello noob!")

    if message.content.startswith("!joinus"):
        await join()


@bot.command(name="joinus")
async def join(context):
    channel = context.author.voice.channel
    await channel.connect()

@bot.command(name="leaveus")
async def leave(context):
    await context.voice_bot.disconnect()

bot.run("OTMyODM4MTkzNjk3NTIxNjY1.YeYzRA.ei7LevdTg802Krokzr024Q4zzKo")

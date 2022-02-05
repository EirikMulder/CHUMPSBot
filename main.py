import discord
from time import sleep
from random import randint
import datetime
import logging

# import nacl # Voice

from discord.ext import commands
from collections import Counter


bot = commands.Bot(command_prefix="$")
people = {
    "jack": 766415398530187305,
    "karina": 533680717062733844,
    "joey": 493254647780343808,
    "eirik": 541302616068456448,
}
games = []
with open("games.txt", "r") as file:
    for line in file:
        games.append(line.strip())


@bot.event
async def on_ready():
    global eirik, last_picked
    last_picked = datetime.datetime.now() - datetime.timedelta(minutes=60)
    eirik = await bot.fetch_user(541302616068456448)
    global poll_running, poll_votes, poll_options
    poll_running = False
    poll_votes = Counter()
    poll_options = []


@bot.event
async def reset_pick():
    last_picked = datetime.datetime.now() - datetime.timedelta(minutes=60)


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await eirik.send(message.author.name + ":")
        await eirik.send(message.content)
    await bot.process_commands(message)


@bot.command(
    help="Looks like you need some help.",
    brief="Prints the list of values back to the channel.",
)
async def say(ctx, *args):
    response = ""

    for arg in args:
        response = response + " " + arg

    await ctx.channel.send(response)


@bot.command()
async def hello(ctx, *args):
    await ctx.channel.send("Hello noob!")
    user = await bot.fetch_user(ctx.author.id)
    await user.send("Hello! I'm CHUMPSBot!")


@bot.command()
async def pick_game(ctx):
    global last_picked
    if (datetime.datetime.now() - last_picked) > datetime.timedelta(minutes=30):
        game = games[randint(0, len(games) - 1)]
        await ctx.channel.send(f"Selected Game: {game}")
        last_picked = datetime.datetime.now()
    else:
        await ctx.channel.send("guys you have to play the game... XD")


@bot.command()
async def msg(ctx, *args):
    if args[0] in people:
        user = await bot.fetch_user(people[args[0]])
        print(user.name)
        await eirik.send("messaging " + user.name + ": " + " ".join(args[1:]))
        await user.send(" ".join(args[1:]))


@bot.command()
async def joinus(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def poll(ctx, *args):
    # if poll_running:
    #     print("There is already a poll running, use $stop_poll to stop it.")
    global poll_running, poll_votes, poll_options

    poll_running = True
    poll_options = " ".join(args)
    if "," in poll_options:
        poll_options = poll_options.split(",")
    else:
        poll_options = poll_options.split(" ")
    poll_options = [i.lower().strip() for i in poll_options]
    if poll_options[-1].startswith("and"):
        poll_options[-1] = poll_options[-1][3:].strip()
    await ctx.channel.send(f"The poll_options are:\n" + "\n".join(poll_options))
    await ctx.channel.send(
        "Use $vote 'something' to vote. Use $stop_poll to stop the poll."
    )


@bot.command()
async def stop_poll(ctx):
    global poll_running, poll_votes, poll_options
    if not poll_running:
        await ctx.channel.send("No poll is running. Use $poll 'options' to start one.")
    await ctx.channel.send("The poll is finished!")
    for option, votes in poll_votes.items():
        await ctx.channel.send(f"{option} recieved {votes} votes!")
    poll_running = False
    poll_options = []
    poll_votes = Counter()


@bot.command()
async def vote(ctx, *args):
    global poll_running, poll_votes, poll_options
    if not poll_running:
        await ctx.channel.send(
            "No poll is active. Use $poll 'option1,option2' to start one"
        )
        return
    pick = " ".join(args).strip().lower()
    if pick in poll_options:
        poll_votes[pick] += 1
        await ctx.channel.send(f"Your vote for {pick} has been registered!")
    else:
        await ctx.channel.send("That is not one of the poll options.")


with open("key.txt", "r") as file:
    key = file.readline()
bot.run(key)

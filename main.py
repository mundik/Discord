from discord.ext import commands
import discord
import Workout
import Anime_database as Anime
import System

TOKEN = 'NzMzOTE5NTQ2MTg0MDQwNTA5.XxKJ1w.fkLthMofrT3g7DSGBWB59BGrYKo'
GUILD = '508295043153526816'
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot is ready')
    Workout.check()


@bot.command()
async def w(ctx, *args):
    await workout(ctx, *args)


@bot.command()
async def workout(ctx, *args):
    try:
        func = args[0]
    except IndexError:
        await ctx.send("Available functions: sub, status")
        return
    if func == "sub":
        if len(args) != 3:
            await ctx.send("Type and number needed")
        else:
            option = args[1]
            num = args[2]
            remain = Workout.substract(option, num)
            if remain == "":
                await ctx.send("Wrong type of operation.")
            else:
                await ctx.send(f"Substracted {num} points from {option}.\nNew value: {remain}")
    elif func == "status" or func == "stat":
        num = Workout.status()
        await ctx.send(f"Remaining workout points:\n {num}")
    else:
        await ctx.send("Wrong function(available: status,sub)")


@bot.command()
async def today(ctx):
    await ctx.send(f"{System.today()}, {System.today().timetuple().tm_yday}")


@bot.command()
async def a(ctx, *args):
    await anime(ctx, *args)


@bot.command()
async def anime(ctx, *args):
    try:
        func = args[0]
    except IndexError:
        await ctx.send("Available functions: watched, add, add_going, finished, status, waiting, update")
        return
    if func == "watched" or func == "w":
        data = Anime.watched(args[1], args[2]) if len(args) == 3 else \
            "Missing parameters (syntax: watched Name Num_of_ep)"
        await ctx.send(data)
    elif func == "add":
        data = Anime.new_anime(args[1], args[2], args[3]) if len(args) == 4 else \
            "Missing parameters (syntax: add Name Act_ep Num_of_ep)"
        await ctx.send(data)
    elif func == "add_going":
        data = Anime.new_anime_going(args[1], args[2], args[3], args[4], args[5], args[6]) if len(args) == 7 else \
            "Missing parameters (syntax: add Name Act_ep Num_ep Day Last_updated, Update_hour)"
        await ctx.send(data)
    elif func == "finished" or func == "f":
        data = Anime.delete_anime(args[1]) if len(args) == 2 else "Missing parameters (syntax: finished Name)"
        await ctx.send(data)
    elif func == "status" or func == "stat":
        await ctx.send(Anime.status())
    elif func == "waiting" or func == "wait":
        await ctx.send(Anime.waiting())
    elif func == "update" or func == "u":
        await ctx.send(Anime.new_episode())
    elif func == "change":
        data = Anime.change_time(args[1], args[2]) if len(args) == 3 else \
            "Missing parameters (syntax: change Name Hour)"
        await ctx.send(data)
    else:
        await ctx.send("Wrong function(available: watched, add, add_going, finished, status, waiting, update, change)")


@bot.command()
async def log(ctx, *args):
    try:
        name = args[0]
    except IndexError:
        ctx.send("Need file to input")
    else:
        file = discord.File(f"./{name}")
        await ctx.send(file=file, content=" ")

"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
    else:
        await ctx.send(str(error))
"""
bot.run(TOKEN)

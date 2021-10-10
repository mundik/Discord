from discord.ext import commands
import discord
import Workout
import Anime
import System
import Notes
import time as Time

TOKEN = 'NzMzOTE5NTQ2MTg0MDQwNTA5.XxKJ1w.fkLthMofrT3g7DSGBWB59BGrYKo'
GUILD = '508295043153526816'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready')
    Workout.check()
    Notes.clear_due()


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
        data = Workout.status()
        await ctx.send(f"Remaining workout points:\n {data}")
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
        data = Anime.watched(args[1:-1], args[-1]) if len(args) >= 3 else \
            "Missing parameters (syntax: watched Name Num_of_ep)"
        await ctx.send(data)
    elif func == "add":
        data = Anime.new_anime(args[1:-2], args[-2], args[-1]) if len(args) >= 4 else \
            "Missing parameters (syntax: add Name Act_ep Num_of_ep)"
        await ctx.send(data)
    elif func == "add_going":
        data = Anime.new_anime_going(args[1:-4], args[-4], args[-3], args[-2], args[-1]) if len(args) >= 6 \
            else "Missing parameters (syntax: add Name Act_ep Num_ep Day Last_updated, Update_hour)"
        await ctx.send(data)
    elif func == "finished" or func == "f":
        data = Anime.finished(args[1:]) if len(args) >= 2 else "Missing parameters (syntax: finished Name)"
        await ctx.send(data)
    elif func == "status" or func == "stat":
        data = Anime.status()
        data = "No anime in database" if data == "" else data
        await ctx.send(data)
    elif func == "waiting" or func == "wait":
        data = Anime.waiting()
        data = "Nothing on waitlist" if data == "" else data
        await ctx.send(data)
    elif func == "update" or func == "u":
        data = Anime.update()
        data = "Nothing to update" if data == "" else data
        await ctx.send(data)
    elif func == "transfer" or func == "t":
        data = Anime.transfer(args[1:]) if len(args) >= 2 else "Missing parameters (syntax: transfer Name)"
        await ctx.send(data)
    elif func == "change":
        data = Anime.change_time(args[1:-1], args[-1]) if len(args) >= 3 else \
            "Missing parameters (syntax: change Name Hour)"
        await ctx.send(data)
    else:
        await ctx.send(
            "Wrong function(available: watched, add, add_going, finished, status, waiting, update, change, transfer)")


@bot.command()
async def log(ctx, *args):
    try:
        name = args[0]
    except IndexError:
        ctx.send("Need file to input")
    else:
        file = discord.File(f"./{name}")
        await ctx.send(file=file, content=" ")


@bot.command()
async def n(ctx, *args):
    await note(ctx, *args)


@bot.command()
async def note(ctx, *args):
    try:
        func = args[0]
    except IndexError:
        await ctx.send("Available functions: add, delete")
        return
    if func == "add" or func == "a":
        if len(args) > 4:
            name = args[1]
            date = args[2]
            time = args[3]
            text = ' '.join(args[4:])
            data = Notes.add_note(name, date, time, text)
        else:
            await ctx.send("Missing parameters (syntax: note add name date text)")
            return
        await ctx.send(data[0])
        bot.loop.create_task(mention(ctx, name, text, data[1]))
    if func == "delete" or func == "d":
        data = Notes.delete_note(args[1]) if len(args) == 2 else "Missing parameters (syntax: note delete name)"
        await ctx.send(data)


@bot.command()
async def clear(ctx, *args):
    if len(args) == 0:
        ctx.send("Insert number of messages to delete")
        return
    number = int(args[-1]) + 1
    if len(args) > 2:
        order = args[-2]
    else:
        order = ""
    if order == "u" or order == "U":
        await ctx.channel.purge(limit=number, oldest_first=True)
    else:
        await ctx.channel.purge(limit=number)


async def mention(ctx, name, text, sleep_time):
    Time.sleep(sleep_time)
    respond = f"{name.replace('_', ' ')}\n{text}\n{ctx.author.mention}"
    await ctx.send(respond)
    Notes.delete_note(name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
    else:
        await ctx.send(str(error))

bot.run(TOKEN)

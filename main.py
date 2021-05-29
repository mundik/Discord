from discord.ext import commands
import threading
import Server
import Workout
import Anime
import System

# TOKEN = 'NzM1ODg1ODk2OTQ3MDczMDc1.XxmxUg.6-Bd3aKYITMiVsCxIAx7wU2YGa0' old from minecraft server bot
TOKEN = 'NzMzOTE5NTQ2MTg0MDQwNTA5.XxKJ1w.fkLthMofrT3g7DSGBWB59BGrYKo'
GUILD = '508295043153526816'
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot is ready')
    Workout.daily_check()


@bot.command()
async def status(ctx, *args):
    typ = ""
    if len(args) == 1:
        typ = args[0]
    if typ == "":
        stand_run, response = Server.probe("S")
        await ctx.send(response)
        test_run, response = Server.probe("T")
        await ctx.send(response)
        if not (test_run or stand_run):
            await ctx.send("!S - Start standart server\n!T - Start testing server")
    else:
        run, response = Server.probe(typ)
        await ctx.send(response)


@bot.command()
async def T(ctx):
    stat = Server.probe("T")[0]
    if stat == 1:
        await ctx.send('Testing server already running')
    else:
        await ctx.send('Starting server.....')
        thread_test = threading.Thread(target=Server.start("T"), daemon=True)
        thread_test.start()


@bot.command()
async def S(ctx):
    stat = Server.probe("S")[0]
    if stat == 1:
        await ctx.send('Standart server already running')
    else:
        await ctx.send('Starting server.....')
        thread_stan = threading.Thread(target=Server.start("S"), daemon=True)
        thread_stan.start()


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
        await ctx.send(str("Remaining workout points: " + str(num)))
    else:
        await ctx.send("Wrong function(available: status,sub)")


@bot.command()
async def today(ctx):
    await ctx.send(str(System.today()) + ", " + str(System.today().timetuple().tm_yday))


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
        if len(args) == 3:
            await ctx.send(Anime.watched(args[1], args[2]))
        else:
            await ctx.send("Missing parameters (syntax: watched Name Num_of_ep)")
    elif func == "add":
        if len(args) == 4:
            await ctx.send(Anime.new_anime(args[1], args[2], args[3]))
        else:
            await ctx.send("Missing parameters (syntax: add Name Num_of_act_ep Num_of_ep)")
    elif func == "add_going":
        if len(args) == 6:
            await ctx.send(Anime.new_anime_going(args[1], args[2], args[3], args[4], args[5]))
        else:
            await ctx.send("Missing parameters (syntax: add Name Num_of_act_ep Last_ep_num Day Last_updated)")
    elif func == "finished" or func == "f":
        if len(args) == 2:
            await ctx.send(Anime.delete_anime(args[1]))
        else:
            await ctx.send("Missing parameters (syntax: finished Name)")
    elif func == "status" or func == "stat":
        await ctx.send(Anime.status())
    elif func == "waiting":
        await ctx.send(Anime.waiting())
    elif func == "update" or func == "u":
        await ctx.send(Anime.new_episode())
    else:
        await ctx.send("Wrong function(available: watched, add, add_going, finished, status, waiting, update)")


"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
    else:
        await ctx.send(str(error))
"""
bot.run(TOKEN)

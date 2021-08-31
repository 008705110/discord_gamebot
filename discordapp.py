import discord
from discord.errors import DiscordServerError
from discord.ext import commands
import json
import os
import random

client = commands.Bot(command_prefix = "$")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    
    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = "wallet",value = wallet_amt)
    em.add_field(name = "bank",value = bank_amt)

    await ctx.send(embed = em)



@client.command()
async def beg(ctx):
    users = await get_bank_data()
    user = ctx.author
    await open_account(ctx.author)

    earnings = random.randrange(101)
    await ctx.send(f"someone gave you {earnings} coins")
    users[str(user.id)]["wallet"] += earnings

    
    with open("mainbank.json","w") as f:
        json.dump(users,f)




async def open_account(user):
    
    users = await get_bank_data()

fdsfdsfdsfds
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    return users



    







client.run('ODgxNzc2NjY0NTM3ODgyNzA1.YSxwgw.D0cJ9htfHXCJZLFKF7PuMinOzkA')
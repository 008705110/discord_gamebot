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

    earnings = random.randrange(1000)
    await ctx.send(f"someone gave you {earnings} coins")
    users[str(user.id)]["wallet"] += earnings
    



    
    with open("mainbank.json","w") as f:
        json.dump(users,f)


@client.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("fsdfsd")
        return 
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send("error")
        return

    if amount < 0:
        await ctx.send("error")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"you took out {amount}")

@client.command()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("fsdfsd")
        return 
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("123")
        return

    if amount < 0:
        await ctx.send("dfsfsdf")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"jian is a cock sucker {amount}")

@client.command()
async def send(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("error")
        return 
    bal = await update_bank(ctx.author)

    amount = int(amount)


    if amount > bal[1]:
        await ctx.send("error")
        return
    if amount < 0:
        await ctx.send("error")
        return
    if amount.is_integer() == False:
        await ctx.send("error")
        return


    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"you gave {amount}")


async def open_account(user):
    
    users = await get_bank_data()


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

async def update_bank(user,change = 0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

    







client.run('')
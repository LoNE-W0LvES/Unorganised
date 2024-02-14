import discord
import random
import asyncio

TOKEN = "MTEwNDA3ODE3MDAzMTkxOTE4NQ.GepJZd._uecomW7O6EjEEgTfUH36pozUAe0FgmIE4hsag"
intents = discord.Intents.all()  # this will enable all the intents

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message, ctx):
    if message.content.startswith('!start'):
        playersnum = 0
        players = []
        await message.channel.send("Welcome to Chor Dakat! Please react with ☑️ to join the game.")

        def check(reaction, user):
            return user != client.user and str(reaction.emoji) != '' and len(players) < 6

        while len(players) < 6:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=5.0, check=check)
            except asyncio.TimeoutError:
                break
            else:
                playersnum += 1
                players.append(user.name)
        await message.channel.send(f"Got {playersnum} players: {', '.join(players)}")
        emojis = random.sample(
            [u"\U0001F47B", u"\U0001F408", u"\U0001F451", u"\U0001F478", u"\U0001F46E", u"\U0001F480"], playersnum)
        await message.channel.send("Starting in 5 seconds...")
        await asyncio.sleep(1)
        for i in range(4, 0, -1):
            await message.channel.send(f"{i}...")
            await asyncio.sleep(1)
        await message.channel.send("Pick your card!")
        msg = await message.send_message(ctx.message.channel)
        await message.add_reaction(msg, "😮")
        # await message.add_reaction(message, "😮")
        # await asyncio.sleep(2)
        # if message.content == 'Pick your card!':
        #     await message.add_reaction("\U0001F408")
        # for emoji in emojis:

        #     await message.add_reaction(msg, "😮")

        card_values = random.sample(["chor", "dakat", "raja", "rani", "police", "methor"], playersnum)

        def check(reaction, user):
            return user != client.user and str(
                reaction.emoji) in emojis and user.name in players and reaction.count == 1

        for i in range(playersnum):
            reaction, user = await client.wait_for('reaction_add', check=check)
            player_index = emojis.index(str(reaction.emoji))
            await user.send(f"You got {card_values[player_index]}!")
            del emojis[player_index]
            del card_values[player_index]
        await message.channel.send("Thanks For playing")


client.run(TOKEN)
import discord
from discord.ext import commands

bot = discord.Client(command_prefix="!", intents=discord.Intents.default())

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked



bot.run("MTEwNDA3ODE3MDAzMTkxOTE4NQ.GepJZd._uecomW7O6EjEEgTfUH36pozUAe0FgmIE4hsag")
import discord
from discord.ext import commands
import system.lib as lib

global client
client=None

def init(bot_client:commands.Bot):
    global client
    client=bot_client

class Questionnaire(discord.ui.Modal, title='Pendu'):
    answer = discord.ui.TextInput(label='Lettre', style=discord.TextStyle.paragraph, placeholder="Saisir une lettre", min_length=1 ,max_length=1)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Tu as choisi la lettre, {self.answer}!', ephemeral=True)


class input_view(discord.ui.View):
    def init(self, *, timeout = 180):
        super().init(timeout=timeout)

    @discord.ui.button(label="Saisir",style=discord.ButtonStyle.gray)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(Questionnaire())

async def test(ctx:commands.context.Context):
    await ctx.send(content="oui")
    try:
        view=input_view()
        await ctx.send(view=view)
    except Exception as error:
        print(error)

command=[lib.Command(command=test, name="test", aliases=["test1"])]
task=[]
import discord, requests, os, aiohttp
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents, case_insensitive=True)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()
    
@tree.command(name="is_odd", description="Check if a number is odd")
@discord.app_commands.user_install
@discord.app_commands.guild_install
async def is_odd(interaction: discord.Interaction, number: int):
    await interaction.response.defer()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://is-odd-api.mewtru.com/v1/numbers/{number}") as response:
            if response.status == 200:
                data = await response.json()
                if data["odd"]: embed: discord.Embed = discord.Embed(title="Is Odd?", color=discord.Color.green(), description=f"The number {number} is odd.")
                elif data["even"]: embed: discord.Embed = discord.Embed(title="Is Odd?", color=discord.Color.green(), description=f"The number {number} is not odd.")
                else: embed: discord.Embed = discord.Embed(title="Is Odd?", color=discord.Color.red(), description=f"An error occurred while checking if the number {number} is odd.")
                await interaction.followup.send(embed=embed)
            elif response.status == 404:
                embed: discord.Embed = discord.Embed(title="Is Odd?", color=discord.Color.red(), description=f"Unable to confirm if the number {number} is odd.")                
                await interaction.followup.send(embed=embed)
            else: 
                embed: discord.Embed = discord.Embed(title="Is Odd?", color=discord.Color.red(), description=f"An error occurred while checking if the number {number} is odd.")                
                await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    client.run(TOKEN)
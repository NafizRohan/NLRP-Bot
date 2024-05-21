import config
import datetime
from defines import GetResult, GetGender, GetFactionName, ReturnAge, ReturnDays, ReturnHour
import discord
from discord.ext import commands
from discord import app_commands as app, Interaction, Color as c
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
from samp_py.client import SampClient as client

class PlayerCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def channel_check(interact:Interaction):
        if interact.channel.id == 1232408881007951915:
            return True
        else:
            await interact.response.send_message("This command is only allowed in the specified channel. Use <#1232408881007951915>.")
            return False
    
    @app.command(name= "top", description="Show top list of the server")
    @app.commands.check(channel_check)
    @app.choices(type=[
        app.Choice(name= "Rich", value= 1),
        app.Choice(name= "Poor", value= 2),
        app.Choice(name= "Crimes", value= 3),
        app.Choice(name= "Hours", value= 4)
    ])
    async def top(self, interact:Interaction, type: app.Choice[int]):
        embed = discord.Embed(color= c.brand_green(), title= f'NewLife RolePlay [S1]')
        embed.set_author(name = "NewLife RolePlay", url = "https://www.newliferoleplay.xyz/")
        if type.value == 1:
            top_rich = PrettyTable(['Username', 'Money'])
            top_rich.align['Username'] = "l"#[left align]
            top_rich.align['Money'] = "r"#[right align]
            rows = GetResult("SELECT `BankMoney`, `Money`, `Character` FROM characters ORDER BY `BankMoney`+`Money` DESC LIMIT 10")
            for row in rows:
                total_cash = row[0] + row[1]
                top_rich.add_row([row[2], total_cash])
            rich_list = f'```\n{top_rich}\n```'
            embed.description = f"\n**Top {len(rows)} Richest PLAYERS:**\n\n{rich_list}"
            await interact.response.send_message(embed= embed)
            return
        elif type.value == 2:
            top_poor = PrettyTable(['Username', 'Money'])
            top_poor.align['Username'] = "l"#[left align]
            top_poor.align['Money'] = "r"#[right align]
            rows = GetResult("SELECT `BankMoney`, `Money`, `Character` FROM characters ORDER BY `BankMoney`+`Money` ASC LIMIT 10")
            for row in rows:
                total_cash = row[0] + row[1]
                top_poor.add_row([row[2], total_cash])
            poor_list = f'```\n{top_poor}\n```'
            embed.description = f"\n**Top {len(rows)} Poor PLAYERS:**\n\n{poor_list}"
            await interact.response.send_message(embed= embed)
        elif type.value == 3:
            top_criminals = PrettyTable(['Username', 'Crimes'])
            top_criminals.align['Username'] = "l"#[left align]
            top_criminals.align['Crimes'] = "r"#[right align]
            rows = GetResult("SELECT `Warrants`, `Character` FROM characters ORDER BY `Warrants` DESC LIMIT 10")
            
            for row in rows:
                top_criminals.add_row([row[1], row[0]])
            criminals = f'```\n{top_criminals}\n```'
            embed.description = f"**Top {len(rows)} Players With Most Crimes**:\n{criminals}"
            await interact.response.send_message(embed= embed)  
        elif type.value == 4:
            top_criminals = PrettyTable(['Username', 'Hours'])
            top_criminals.align['Username'] = "l"#[left align]
            top_criminals.align['Hours'] = "r"#[right align]
            rows = GetResult("SELECT `PlayingHours`, `Character` FROM characters ORDER BY `PlayingHours` DESC LIMIT 10")
            
            for row in rows:
                top_criminals.add_row([row[1], row[0]])
            criminals = f'```\n{top_criminals}\n```'
            embed.description = f"**Top {len(rows)} Players With Most Hours**:\n{criminals}"
            await interact.response.send_message(embed= embed) 
        else:
            await interact.response.send_message("Invalid type bruh. Select a valid type like Rich/Poor/Crimes/Hour")
            return
        return
    
    @app.command(name='ip', description="Show server Address") 
    @app.commands.check(channel_check)
    async def ip(self, interaction:Interaction):
        try:
            ip = discord.Embed(title="Server Address", description=f"```css\n{config.IP}:{config.PORT}```", color= c.green())
            await interaction.response.send_message(embed= ip) 
        except Exception as e:
            print(e)
        return#Simple Command No Comments needed
    
    @app.command(name="players", description="Show online players")
    @app.commands.check(channel_check)
    async def players(self, interact:Interaction):
        try:
            try:
                game = client(address= config.IP, port= config.PORT)
                samp = game.connect()
                info = samp.get_server_info()
            except Exception as e:
                error = discord.Embed(color= c.red(), title= "Server Offline")
                error.add_field(name= "IP ADDRESS", value= f"```css\n{config.IP}:{config.PORT}\n```")
                error.add_field(name="Players", value= "```\n0/0\n```")
                error.add_field(name= "Status", value= "```\n⛔Offline!\n```")
                error.add_field(name="Information", value= "```diff\n- Server currently offline......\n```")
                await interact.response.send_message(content="", embed= error)
            else:
                TotalPlayers = info.players
                ServerName = info.hostname

                players = [samp.name for samp in samp.get_server_clients_detailed()]
                score = [samp.score for samp in samp.get_server_clients_detailed()]
                Status = discord.Embed(color= c.green(), title= ServerName)
                
                if TotalPlayers == 0:
                    Status.add_field(name="City Status", value= "```diff\n- No Players Are Playing:(```", inline= False)
                elif TotalPlayers >= 100:
                    Status.add_field(name= "City Status", value= "```bash\n\"We Reached 100 Players In Our Server, Thats Great!\"```", inline= False)
                else:
                    list = PrettyTable(["Username", "Score"])
                    list.align["Username"] = "l"
                    list.align["Score"] = "r"
                    for i in range(TotalPlayers):
                        list.add_row([f"{players[i]:<22}", f"{score[i]:<2}"])
                    player_list = f"```\n{list}\n```"
                    Status.description = player_list
                await interact.response.send_message(embed= Status)
        except Exception as e:
            print(e)
        return
    
    @app.command(name="player-stats", description="Instant player details at your fingertips.")
    @app.commands.check(channel_check)
    async def playerstats(self, interact: Interaction, name: str):
        try:
            result = GetResult(f"SELECT `Gender`, `Level`, `Faction`, `BirthDate`, `LastLogin`, `Phone`, `CreateDate`  FROM `characters` WHERE `Character` = '{name}'")
            if result is False:
                await interact.response.send_message("Invalid character name. Enter a correct character name.")
        except Exception as e:
            print(e)
        else:
            for x in result:
                gender = GetGender(x[0])
                level = x[1]
                faction = GetFactionName(x[2])
                age = ReturnAge(x[3])
                lastlogin = ReturnHour(x[4])
                Phone = x[5]
                reg = ReturnDays(x[6])
            

            print(f"{gender}, {level}, {faction}, {age}, {lastlogin}, {Phone}, {reg}")
        return
    


async def setup(bot):
    await bot.add_cog(PlayerCmds(bot))
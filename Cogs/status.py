import config
import discord
from discord import Color as c
from discord.ext import commands, tasks
from samp_py.client import SampClient as client
from prettytable import PrettyTable

import time


class status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @tasks.loop(seconds= 30)
    async def UpdateEmbed(self):
        channel = await self.bot.fetch_channel(config.STATUS)
        message = await channel.fetch_message(1193449116752171059)
        time__ = time.localtime()
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
            error.set_footer(icon_url= "https://cdn.discordapp.com/attachments/1192082796689248377/1192355981083029555/NewLifeRP.png?ex=65a8c70a&is=6596520a&hm=9de86cb92922a5d9d7d7d13b4db6860a0bfc01ab4f402318b0d522fb2a13ed1e&",
                                text=f"Server Status ・ Updated every 30 seconds")
            await message.edit(content="", embed= error)
        else:
            try:
                host = info.hostname
                players = info.players
                max_players = info.max_players
                lang = info.language
                gamemode = info.gamemode
                locked = info.password
                clients = [samp.name for samp in samp.get_server_clients_detailed()]
                score = [samp.score for samp in samp.get_server_clients_detailed()]
                map = "San Andreas"
                url = "www.newliferoleplay.xyz"
                #A condition to replace True and False to Yes and No
                if locked == False:
                    locked = 'No'
                else:
                    locked = 'Yes'
                #embed Part
                server = discord.Embed(color= c.green())#embed creation
                server.set_author(name=f"{host}", url=f"https://{url}")
                server.add_field(name="IP Address", value= f"```\n{config.IP}:{config.PORT}\n```", inline= True)
                server.add_field(name="Players", value= f"```\n{players}/{max_players}\n```", inline= True)
                server.add_field(name="Language", value= f"```\n{lang}\n```", inline= True)
                server.add_field(name= "Version", value= f"```\n{gamemode}\n```", inline= True)
                server.add_field(name="Locked", value= f"```\n{locked}\n```")
                server.add_field(name="Map", value= f"```\n{map}\n```")
                if clients and len(clients) <= 100:
                    embed_fields = []
                    for i in range(0, len(clients), 15):
                        table = ""
                        for j in range(i, min(i + 15, len(clients))):
                            table += f"\n{clients[j]}|{score[j]}"
                        player_list = f"```\n{table}\n```"
                        embed_fields.append({"name": "Now Playing", "value": player_list, "inline": False})
                    
                    for field in embed_fields:
                        server.add_field(name=field["name"], value=field["value"], inline=field["inline"])


                server.set_footer(icon_url= "https://cdn.discordapp.com/attachments/1192082796689248377/1192355981083029555/NewLifeRP.png?ex=65a8c70a&is=6596520a&hm=9de86cb92922a5d9d7d7d13b4db6860a0bfc01ab4f402318b0d522fb2a13ed1e&",
                                    text=f"Server Status ・ Updated every 30 seconds")
                await message.edit(content="", embed=server)
            except Exception as e:
                print(e)
            game.disconnect()
        return
    
    @tasks.loop(seconds= 30)
    async def UpdateChannel(self): 
        channel = await self.bot.fetch_channel(config.STATUS)
        try:
            game = client(address= config.IP, port= config.PORT)
            samp = game.connect()
            info = samp.get_server_info()
        except Exception as e:
            if channel.name == "𝗣𝗟𝗔𝗬𝗘𝗥𝗦︙Offline":
                return
            else:
                await channel.edit(name="𝗣𝗟𝗔𝗬𝗘𝗥𝗦︙Offline")
            print(e)
        else:
            players  = info.players
            tempname =f"𝗣𝗟𝗔𝗬𝗘𝗥𝗦︙{players}" 
            if channel.name == tempname:
                return
            else:
                await channel.edit(name=f"𝗣𝗟𝗔𝗬𝗘𝗥𝗦︙{players}")
            game.disconnect()
        return
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.UpdateChannel.start() 
        self.UpdateEmbed.start()
        return True
    
async def setup(bot):
    await bot.add_cog(status(bot))
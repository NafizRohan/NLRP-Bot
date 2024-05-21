import discord
from discord import ui
from discord import TextStyle
from discord.ext import commands
from discord import app_commands as ac, Interaction
import hashlib 
from defines import CheckQuery, sql_query
from datetime import datetime
import whirlpool

def encodepassword(password):
    password_bytes = password.encode()
    wp = whirlpool.new(password_bytes)
    hashed_string = wp.hexdigest()
    return hashed_string.upper()

class info(ui.View):
    def __init__(self, name: str, passcode: str) -> None:
        super().__init__(timeout = None)
        self.username = name
        self.password = passcode
    
    @ui.button(label= "✅| Confirm", style= discord.ButtonStyle.green)
    async def yes(self, interaction:Interaction, button: ui.Button):
        try:
            self.stop()
            query = sql_query(f"INSERT INTO `accounts` (`Username`, `Password`, `RegisterDate`, `DiscordID`) VALUES('{self.username}', '{self.password}', NOW(), {interaction.user.id});")
            if query:
                embed = discord.Embed(title="SUCCESSFULLY REGISTERED",
                      description=f"{interaction.user.mention} You have registered your username ({self.username}) successfully.\n\n> Welcome to New Life Roleplay. Please do follow our city rules while roleplay. Checkout our websites for more information. Happy Gaming <:GreenHeart:1192113434435801229>\n\n<:greenlink:1192113419617321020> **CITY RULES** <a:arrow4:1192100243215491103> [CLICK HERE](https://docs.google.com/document/d/1Iuo7_vDWIkCMqQg6yK24SN_yhYuajjpMKLokGMPJ-j8/edit?usp=sharing)\n<:greenlink:1192113419617321020> **WEBSITE** <a:arrow4:1192100243215491103> [CLICK HERE](https://www.newliferoleplay.xyz/)\n<a:6159_earthgreen:1197285831275200563> **IP** <a:arrow4:1192100243215491103>  <#1190908018867572736>",
                      colour=0x63b752,
                      timestamp=datetime.now())

                embed.set_author(name="NLRP",
                                url="https://newliferoleplay.xyz/",
                                icon_url="https://cdn.discordapp.com/attachments/1192082796689248377/1202993194506133504/Picsart_23-12-27_15-01-23-589.png?ex=66291fb8&is=6627ce38&hm=c4d5cedb6d9f7c1fd2eff729bb5d24c87bb534573501db0a12b70cac5ec2c6b9&")

                embed.set_image(url="https://cdn.discordapp.com/attachments/1192082796689248377/1232400245636202576/registered.gif?ex=662951ab&is=6628002b&hm=2b366998a4dbeaabae28440ac31f2ebc64f547420cf2d06eee081a3186169fd3&")

                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1192118155787640922.webp?size=96&quality=lossless")

                embed.set_footer(text="New Life",
                                icon_url="https://cdn.discordapp.com/attachments/1192082796689248377/1202993194506133504/Picsart_23-12-27_15-01-23-589.png?ex=66291fb8&is=6627ce38&hm=c4d5cedb6d9f7c1fd2eff729bb5d24c87bb534573501db0a12b70cac5ec2c6b9&")
                channel_id = 1192196787713351720
                channel = interaction.guild.get_channel(channel_id)
                await channel.send(embed= embed, allowed_mentions= discord.AllowedMentions.all())
                role = interaction.guild.get_role(1192115027847675954)
                await interaction.user.add_roles(role)
                await interaction.response.send_message(content="Registration Successfull", delete_after= 15)
                return
            else:
                await interaction.response.send_message(content="Something went wrong try again.", delete_after= 120, ephemeral= True)
                return
        except Exception as e:
            print(e)
    @ui.button(label= "❌| Cancel", style= discord.ButtonStyle.red)
    async def no(self, interaction:Interaction, button: ui.Button):
        self.stop()
        await interaction.response.send_message(content="Nevermind I will delete this contant", delete_after= 15,ephemeral= True)
        return

class Regmodal(ui.Modal, title= "NewLife registration from"):
        name = ui.TextInput(label="Username", style=TextStyle.short, placeholder="Ex:- Nafiz, Monu, Human", required= True, min_length= 4, max_length= 12)
        password = ui.TextInput(label="Password", style=TextStyle.short, placeholder="Your password", required=True, min_length= 6, max_length= 12)
        async def on_submit(self, interaction: Interaction) -> None:
            try:
                if "_" in self.name.value:
                    return await interaction.response.send_message(content="Underscore('_') not allowed in master account name.")
                check = CheckQuery(f"SELECT * FROM `accounts` WHERE `Username` = '{self.name}';")
                check1 = CheckQuery(f"SELECT * FROM `accounts` WHERE `DiscordID` = '{interaction.user.id}';")
                if check:
                    return await interaction.response.send_message(content="This name is already registered use a differnt one.", ephemeral= True, delete_after= 25)
                elif check1:
                    return await interaction.response.send_message(content="You can create only one account with a discord id.", ephemeral= True, delete_after= 25)
                else:
                    embed = discord.Embed(title="Registration form",
                      url="https://newliferoleplay.xyz/",
                      description=f"**Confirm your identity**\nConfirm your registration for NewLife SanAndreas RolePlay by reviewing and verifying your registration details.\n\n**Username**\nYour username is ``{self.name}``.\nOnly with this username you can login to your account. Never share your id with others.\n\n**Password**\nYour password is ||{self.password}||.\nDo not share this password to anyone. Remember NewLife staffs never ask your password for anything.",
                      colour=0x4fcf51,
                      timestamp=datetime.now())

                    embed.set_author(name="NLRP",
                                    url="https://newliferoleplay.xyz/",
                                    icon_url="https://cdn.discordapp.com/attachments/1192082796689248377/1202993194506133504/Picsart_23-12-27_15-01-23-589.png?ex=6629c878&is=662876f8&hm=e3a3d64b781fb55e23607479ad4160f599ecdb0c5951ff3cef84154f362aec96&")

                    embed.set_image(url="https://cdn.discordapp.com/attachments/1192082796689248377/1232246195527749702/standard.gif?ex=66296af3&is=66281973&hm=dbcd64c4e91ba95171e15de28ceed4ec8bcad3b2e00fa0d645d2e32a442e6e00&")

                    embed.set_footer(text="React with ✅ to confirm or ❌ to cancel.",
                                    icon_url="https://cdn.discordapp.com/attachments/1192082796689248377/1202993194506133504/Picsart_23-12-27_15-01-23-589.png?ex=6629c878&is=662876f8&hm=e3a3d64b781fb55e23607479ad4160f599ecdb0c5951ff3cef84154f362aec96&")
                    view = info(name= f"{self.name}", passcode= encodepassword(f"{self.password}"))
                    await interaction.response.send_message(embed=embed, view=view, ephemeral= True, delete_after=120)
                    return
            except Exception as e:
                print(e)

class registration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @ac.command(name="register", description="Creates a new user account for accessing NewLife RolePlay")
    async def register(self, interact:Interaction):
        if interact.channel.id == 1231995952689057944 or interact.channel.id == 1232108332160909374:
            await interact.response.send_modal(Regmodal())
        else:
            await interact.response.send_message(content="Wrong channel. Use <#1231995952689057944>")
        return


async def setup(bot):
    await bot.add_cog(registration(bot))
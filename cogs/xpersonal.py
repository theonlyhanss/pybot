import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
import asyncio

# Personal Class
class Personal(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Personal is online.")
        # self.auto_send.start()
        # self.auto_send2.start()
        # self.pinging.start()

    #auto send msgs
    @tasks.loop(hours = 9)
    async def auto_send(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(889630744312446987)
        msgs = ["ثبح" , "ثباحو" , "مثا" , "مثائو"]
        await channel.send(f"{random.choice(msgs)}")

    @tasks.loop(hours = 10)
    async def auto_send2(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(866821284486971393)
        msgs = ["ثبح" , "ثباحو" , "مثا" , "مثائو"]
        await channel.send(f"{random.choice(msgs)}")

    @tasks.loop(hours = 1)
    async def pinging(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1015399602536595497)
        await channel.send("I am alive...")

    #number of servers
    @app_commands.command(name = "guilds", description = "guilds.")
    async def guilds(self, interaction: discord.Interaction):
        if interaction.user.id == 543172445155098624: await interaction.response.send_message(f"I'm in {str(len(self.bot.guilds))} servers!")
        else: await interaction.response.send_message("You can not use this command..", ephemeral=True)

    #list of servers
    @app_commands.command(name = "guildslist", description = "guildslist.")
    async def guildslist(self, interaction: discord.Interaction):
        if interaction.user.id == 543172445155098624:
            servers = list(self.bot.guilds)
            for server in servers:
                print(f'"{server.id}": "",')
            await interaction.response.send_message(f"Connected on {str(len(self.bot.guilds))} servers:\n>>> " + '\n'.join(server.name for server in servers))
        else:
            await interaction.response.send_message("You can not use this command..", ephemeral=True)

    #on join
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        #send msg
        channel = self.bot.get_channel(1027328777828712479)
        await channel.send(f"I joined {guild.name}")
    #on join
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        #send msg
        channel = self.bot.get_channel(1027328806236721283)
        await channel.send(f"I left {guild.name}")

    #on messages events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        # hidden commands
        if message.content == "sb_join":
            if message.author.voice is None: return await message.channel.send("You are not connected to a voice channel.")
            if message.guild.voice_client is not None: await message.guild.voice_client.disconnect()
            await message.author.voice.channel.connect()
            await message.channel.send("Joined")
        elif message.content == "sb_leave":
            if message.guild.voice_client is not None:
                await message.guild.voice_client.disconnect()
                return await message.channel.send("Left")
            await message.channel.send("I am not connected to a voice channel.")
        elif message.content == "sb_guilds":
            if message.author.id == 543172445155098624: await message.channel.send(f"I'm in {str(len(self.bot.guilds))} servers!")
        elif message.content == "sb_guildslist":
            if message.author.id == 543172445155098624:
                servers = list(self.bot.guilds)
                for server in servers:
                    print(f'"{server.id}": "",')
                await message.channel.send(f"Connected on {str(len(self.bot.guilds))} servers:\n>>> " + '\n'.join(server.name for server in servers))
            else:
                await message.channel.send("You can not use this command..", ephemeral=True)

        #السلام عليكم
        if message.content.startswith("السلام عليكم"):
            if message.guild.id != 1006375287434530896: return await message.reply("وعليكم السلام ورحمة اللّٰه وبركاته")

        #ثباحو
        elif message.content.startswith("ثباحو"): return await message.channel.send("ثبح")
        #مثائو
        elif message.content.startswith("مثائو"): return await message.channel.send("مثا")
        #ثبح
        elif message.content.startswith("ثبح"): return await message.channel.send("ثباحو")
        #مثا
        elif message.content.startswith("مثا"): return await message.channel.send("مثائو")

        #يالبوت
        if "يالبوت" in message.content:
            async with message.channel.typing(): await asyncio.sleep(3)
            normal_responses = [
                  "اكيد يسطا" , "اكيد يبرو" , "بدون شك" , "يب اكيد" , "طبعا" , "اومال" , "ايوه" ,
                  "يب" , "يب يب" , "اتكل علي الله يعم" , "مش فايقلك" ,
                  "هي دي محتاجه سؤال!؟" , "لا" , "انا بقولك لا" , "اكيد لا" , "نوب" , "معرفش" ,
                  "اكيد يغالي" , "اكيد ينقم" , "لا هه" , "صدقني انا ذات نفسي معرفش" , "انا لو أعرف هقولك"]
            hellos = ["نعم" , "نعم يغالي" , "نعم ينقم" , "عايز ايه" , "نعم يخويا"]
            steins_keys = ["stein" , "شتاين" , "ستاين"]
            steins = ["شتاينز الأعظم" , "شتاينز فوق" , "شتاينز فوق مستوي التقييم البشري" , "شتاينز اعظم انمي"]
            shinobi_keywords = ["shinobi" , "شنوبي" , "شنبي" , "شنوب" , "شينوبي"]
            father = ["شنوبي ابويا وعمي وعم عيالي" , "شنبي ابويا وعمي" , "شنوبي احسن اب في العالم"]
            azab = ["ده حنين عليا خالث" , "بابا شنبي مش بيمد ايده عليا" , "مش بيلمسني"]
            tabla = ["لا طبعا يغالي" , "شنوبي عمي وعم عيالي" , "شنوبي عمك" , "شنوبي فوق"]
            love = ["حبك" , "حبق" , "وانا كمان يغالي" , "+1"]
            win = ["مش هتكسب هه" , "نصيبك مش هتكسب" , "انا بقولك لا" , "على ضمانتي"]
            elhal = ["الحمدلله يخويا", "الحمدلله يغالي", "تمام الحمدلله"]

            #me responses
            if "انا" in message.content:
                user = self.bot.get_user(900749453651238953)
                if message.author == user:
                    if "ابوك" in message.content: return await message.channel.send(f"{random.choice(father)}")
            #shinobi responses
            for word in shinobi_keywords:
                if word in message.content:
                    if "ابوك" in message.content: return await message.channel.send(f"{random.choice(father)}")
                    if "بيعذبك" in message.content: return await message.channel.send(f"{random.choice(azab)}")
                    if "بتطبل" in message.content: return await message.channel.send(f"{random.choice(tabla)}")
            #steins responses
            for word in steins_keys:
                if word in message.content: return await message.channel.send(f"{random.choice(steins)}")
            #exceptions
            if "هكسب" in message.content: return await message.channel.send(f"{random.choice(win)}")
            if "حبك" in message.content or "حبق" in message.content: return await message.channel.send(f"{random.choice(love)}")
            if "عامل ايه" in message.content or "عامل إيه" in message.content or "كيف حالك" in message.content: return await message.channel.send(f"{random.choice(elhal)}")
            #normal respones
            if " " in message.content: await message.channel.send(f"{random.choice(normal_responses)}")
            #hellos responses
            else: return await message.channel.send(f"{random.choice(hellos)}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Personal(bot))
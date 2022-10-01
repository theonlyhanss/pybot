from email.errors import MessageError
import discord
from discord.ext import commands
import random
import asyncio
import json
from cogs.utils.alerts import swears


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events is online.")


    #on member join
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("jsons/welcome.json", "r") as f:
            channel = json.load(f)
        welcome_channel = channel[str(member.guild.id)]
        if welcome_channel == 123:
            return
        else:
            date_format = "%d/%m/%Y %H:%M"
            channel = self.bot.get_channel(welcome_channel)
            e = discord.Embed(title=f"Welcome {member.name}!", description=f"{member.mention} joined the server.")
            e.set_author(name=member.name, icon_url=member.avatar.url)
            e.set_thumbnail(url=member.avatar.url)
            e.add_field(name="🕛 Age of Account:", value=f"`{member.created_at.strftime(date_format)}`")
            e.set_footer(text=f"{member.guild.name} • {member.joined_at.strftime(date_format)}")
            await channel.send(embed=e)


    #on member leave
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open("jsons/welcome.json", "r") as f:
            channel = json.load(f)
        welcome_channel = channel[str(member.guild.id)]
        if welcome_channel == 123:
            return
        else:
            date_format = "%d/%m/%Y %H:%M"
            channel = self.bot.get_channel(welcome_channel)
            e = discord.Embed(title=f"**{member.name}** has left!", description=f"{member.mention} left the server.")
            e.set_author(name=member.name, icon_url=member.avatar.url)
            e.set_thumbnail(url=member.avatar.url)
            e.add_field(name="🕛 Age of Account:", value=f"`{member.created_at.strftime(date_format)}`")
            e.set_footer(text=f"Joined At: {member.joined_at.strftime(date_format)}")
            await channel.send(embed=e)


    #on messages events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return


        #prefix if mention
        if message.content.startswith(f'{self.bot.user.mention}'):
            pre_em = discord.Embed(title="Did you mention me?",
                                   description=f"Use `/sbhelp` for info about the bot!\nOr `<catogery name> <command name>` for info about a specific command!")
            await message.reply(embed=pre_em)


        #get suggest id
        with open("jsons/suggest.json", "r", encoding="utf8") as f:
            channels = json.load(f)
        sugg_ch_id = channels[str(message.guild.id)]["suggch"]
        #get rev id
        with open("jsons/suggest.json", "r", encoding="utf8") as f:
            channels = json.load(f)
        rev_ch_id = channels[str(message.guild.id)]["revch"]
        #suggestions
        if message.channel.id != sugg_ch_id:
            pass
        else:
            suggest = message.content
            await message.channel.purge(limit=1)
            emb = discord.Embed(title=f"Thanks **{message.author}**",
                                description="Your suggetion was sent.",
                                colour=discord.Colour.gold())
            msg = await message.channel.send(embed=emb)
            await asyncio.sleep(3)
            await msg.delete()
            channel = self.bot.get_channel(rev_ch_id)
            suggestEmbed = discord.Embed(color=0xffd700)
            suggestEmbed.set_author(name=f"Suggested by {message.author}",
                                    icon_url=f"{message.author.avatar.url}")
            suggestEmbed.add_field(name="__New Suggestion__", value=f"{suggest}")
            sgt = await channel.send(embed=suggestEmbed)
            await sgt.add_reaction("👍")
            await sgt.add_reaction("👎")


        #words filter
        with open("jsons/filter.json", "r", encoding="utf8") as f:
            toggle = json.load(f)
        if toggle[str(message.guild.id)] == "disabled":
            pass
        elif toggle[str(message.guild.id)] == "enabled":
            for word in swears:
                if word in message.content.lower():
                    messageContent = message.content.lower()
                    embed = discord.Embed(color=discord.Color.red())
                    embed.set_author(name=f"Hey! Watch Your Language.", icon_url=self.bot.user.avatar.url)
                    embed.add_field(name="__Your Message__", value=f">>> {messageContent}")
                    embed.add_field(name="__Your Warning__", value=f">>> Your message got deleted because you used the word `{word}`")
                    await message.author.send(embed=embed)
                    await message.delete()
                    emb = discord.Embed(title="Hey! Watch Your Language.",
                                        description=f">>> Hey {message.author.mention}! Your message got deleted because you used the word `{word}`",
                                        color=discord.Color.red())
                    emb.set_footer(text="message will be self deleted", icon_url=self.bot.user.avatar.url)
                    msg = await message.channel.send(embed=emb)
                    await asyncio.sleep(5)
                    await msg.delete()
                    return


        #السلام عليكم
        if message.content.startswith('السلام عليكم'):
            return await message.reply('وعليكم السلام ورحمة اللّٰه وبركاته')
        #ثبح
        if message.content.startswith('ثبح'):
            return await message.channel.send('ثباحو')
        #مثا
        if message.content.startswith('مثا'):
            return await message.channel.send('مثائو')
        #ثباحو
        if message.content.startswith('ثباحو'):
            return await message.channel.send('ثبح')
        #مثائو
        if message.content.startswith('مثائو'):
            return await message.channel.send('مثا')


        #arabic stuff

        #يالبوت
        if "يالبوت" in message.content:
            async with message.channel.typing():
                await asyncio.sleep(3)
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
                    if "ابوك" in message.content:
                        return await message.channel.send(f"{random.choice(father)}")

            #shinobi responses
            for word in shinobi_keywords:
                if word in message.content:
                    if "ابوك" in message.content:
                        return await message.channel.send(f"{random.choice(father)}")
                    if "بيعذبك" in message.content:
                        return await message.channel.send(f"{random.choice(azab)}")
                    if "بتطبل" in message.content:
                        return await message.channel.send(f"{random.choice(tabla)}")

            #steins responses
            for word in steins_keys:
                if word in message.content:
                    return await message.channel.send(f"{random.choice(steins)}")

            #exceptions
            if "هكسب" in message.content:
                return await message.channel.send(f"{random.choice(win)}")
            if "حبك" in message.content or "حبق" in message.content:
                return await message.channel.send(f"{random.choice(love)}")
            if "عامل ايه" in message.content or "عامل إيه" in message.content or "كيف حالك" in message.content:
                return await message.channel.send(f"{random.choice(elhal)}")

            #normal respones
            if " " in message.content:
                await message.channel.send(f"{random.choice(normal_responses)}")

            #hellos responses
            else:
                return await message.channel.send(f"{random.choice(hellos)}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
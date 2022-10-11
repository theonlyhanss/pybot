from importlib.util import resolve_name
import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime
from cogs.utils.alerts import swears


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events is online.")


    #on role update
    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before, role_after):
        with open("jsons/roles_log.json", "r") as f:
            channel = json.load(f)
        roles_log = channel[str(role_after.guild.id)]
        if roles_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{role_after.guild.name}", icon_url = f"{role_after.guild.icon.url}")
            embed.add_field(name = f"**:family: Role Updated:**", value=f"`{role_after}`")
            embed.set_footer(text = role_after.guild.name)
            channel = self.bot.get_channel(roles_log)
            await channel.send(embed=embed)


    #on role delete
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        with open("jsons/roles_log.json", "r") as f:
            channel = json.load(f)
        roles_log = channel[str(role.guild.id)]
        if roles_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{role.guild.name}", icon_url = f"{role.guild.icon.url}")
            embed.add_field(name = f"**:family: Role Deleted:**", value=f"`{role}`")
            embed.set_footer(text = role.guild.name)
            channel = self.bot.get_channel(roles_log)
            await channel.send(embed=embed)


    #on role create
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        with open("jsons/roles_log.json", "r") as f:
            channel = json.load(f)
        roles_log = channel[str(role.guild.id)]
        if roles_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{role.guild.name}", icon_url = f"{role.guild.icon.url}")
            embed.add_field(name = f"**:family: Role Created:**", value=f"`{role}`")
            embed.set_footer(text = role.guild.name)
            channel = self.bot.get_channel(roles_log)
            await channel.send(embed=embed)


    #on member unban
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with open("jsons/members_log.json", "r") as f:
            channel = json.load(f)
        members_log = channel[str(guild.id)]
        if members_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{user.name}", icon_url = f"{user.avatar.url}")
            embed.add_field(name = f"**:airplane: Member Unbanned:**", value=f"`{user}`")
            embed.set_thumbnail(url = user.avatar.url)
            embed.set_footer(text = guild.name)
            channel = self.bot.get_channel(members_log)
            await channel.send(embed=embed)


    #on member ban
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with open("jsons/members_log.json", "r") as f:
            channel = json.load(f)
        members_log = channel[str(guild.id)]
        if members_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{user.name}", icon_url = f"{user.avatar.url}")
            embed.add_field(name = f"**:airplane: Member Banned:**", value=f"`{user}`")
            embed.set_thumbnail(url = user.avatar.url)
            embed.set_footer(text = guild.name)
            channel = self.bot.get_channel(members_log)
            await channel.send(embed=embed)


    #on member update
    @commands.Cog.listener()
    async def on_member_update(self, member_before, member_after):
        with open("jsons/members_log.json", "r") as f:
            channel = json.load(f)
        members_log = channel[str(member_after.guild.id)]
        if members_log == 123:
            return
        else:
            if member_before.nick != member_after.nick:
                embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
                embed.set_author(name = f"{member_after.name}", icon_url = f"{member_after.avatar.url}")
                embed.add_field(name = f"**:house: Member's Nickname Updated:**", value=f"`{member_after}`")
                embed.add_field(name = f"**Old Nickname:**", value=f"`{member_before.nick}`")
                embed.add_field(name = f"**New Nickname:**", value=f"`{member_after.nick}`")
                embed.set_thumbnail(url = member_after.avatar.url)
                embed.set_footer(text = member_after.guild.name)
                channel = self.bot.get_channel(members_log)
                await channel.send(embed=embed)
            elif member_before.roles != member_after.roles:
                embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
                embed.set_author(name = f"{member_after.name}", icon_url = f"{member_after.avatar.url}")
                embed.add_field(name = f"**:house: Member's Roles Updated:**", value=f"`{member_after}`")
                embed.set_thumbnail(url = member_after.avatar.url)
                embed.set_footer(text = member_after.guild.name)
                channel = self.bot.get_channel(members_log)
                await channel.send(embed=embed)
            else:
                pass


    #on guild emojis update
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        with open("jsons/channels_log.json", "r") as f:
            channel = json.load(f)
        channels_log = channel[str(guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{guild.name}", icon_url = f"{guild.icon.url}")
            embed.add_field(name = f"**:house: Guild Emojis Updated:**", value=f"`{guild}`")
            embed.set_footer(text = guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on guild sticker update
    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
        with open("jsons/channels_log.json", "r") as f:
            channel = json.load(f)
        channels_log = channel[str(guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{guild.name}", icon_url = f"{guild.icon.url}")
            embed.add_field(name = f"**:house: Guild Stickers Updated:**", value=f"`{guild}`")
            embed.set_footer(text = guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on guild update
    @commands.Cog.listener()
    async def on_guild_update(self, guild_before, guild_after):
        with open("jsons/channels_log.json", "r") as f:
            channel = json.load(f)
        channels_log = channel[str(guild_after.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{guild_after.name}", icon_url = f"{guild_after.icon.url}")
            embed.add_field(name = f"**:house: Guild Updated:**", value=f"`{guild_after}`")
            embed.set_footer(text = guild_after.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on private channel pins update
    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, channel, last_pin):
        with open("jsons/channels_log.json", "r") as f:
            ch = json.load(f)
        channels_log = ch[str(channel.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel.guild.name}", icon_url = f"{channel.guild.icon.url}")
            embed.add_field(name = f"**:house: Private Channel Pins Updated:**", value=f"`{channel}`")
            embed.set_footer(text = channel.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on private channel update
    @commands.Cog.listener()
    async def on_private_channel_update(self, channel_before, channel_after):
        with open("jsons/channels_log.json", "r") as f:
            channel = json.load(f)
        channels_log = channel[str(channel_after.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel_after.guild.name}", icon_url = f"{channel_after.guild.icon.url}")
            embed.add_field(name = f"**:house: Private Channel Updated:**", value=f"`{channel_after}`")
            embed.set_footer(text = channel_after.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on channel pins update
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        with open("jsons/channels_log.json", "r") as f:
            ch = json.load(f)
        channels_log = ch[str(channel.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel.guild.name}", icon_url = f"{channel.guild.icon.url}")
            embed.add_field(name = f"**:house: Channel Pins Updated:**", value=f"`{channel}`")
            embed.set_footer(text = channel.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on channel update
    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before, channel_after):
        with open("jsons/channels_log.json", "r") as f:
            channel = json.load(f)
        channels_log = channel[str(channel_after.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel_after.guild.name}", icon_url = f"{channel_after.guild.icon.url}")
            embed.add_field(name = f"**:house: Channel Updated:**", value=f"`{channel_after}`")
            embed.set_footer(text = channel_after.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on channel delete
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        with open("jsons/channels_log.json", "r") as f:
            ch = json.load(f)
        channels_log = ch[str(channel.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel.guild.name}", icon_url = f"{channel.guild.icon.url}")
            embed.add_field(name = f"**:house: Channel Deleted:**", value=f"`{channel.name}`")
            embed.set_footer(text = channel.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on channel create
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        with open("jsons/channels_log.json", "r") as f:
            ch = json.load(f)
        channels_log = ch[str(channel.guild.id)]
        if channels_log == 123:
            return
        else:
            embed=discord.Embed(color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{channel.guild.name}", icon_url = f"{channel.guild.icon.url}")
            embed.add_field(name = f"**:house: Channel Created:**", value=f"`{channel.name}`")
            embed.set_footer(text = channel.guild.name)
            channel = self.bot.get_channel(channels_log)
            await channel.send(embed=embed)


    #on message delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("jsons/msg_deletes.json", "r") as f:
            channel = json.load(f)
        deletes_channel = channel[str(message.guild.id)]
        if deletes_channel == 123:
            return
        else:
            embed=discord.Embed(description = f"**:wastebasket: Message sent by {message.author.mention} deleted in {message.channel.mention}**",
                                color = 0x000000, timestamp = datetime.now())
            embed.set_author(name = f"{message.author}", icon_url = f"{message.author.avatar.url}")
            embed.add_field(name = "Message:", value=f"`{message.content}`")
            embed.set_footer(text = message.guild.name)
            channel = self.bot.get_channel(deletes_channel)
            await channel.send(embed=embed)


    #on message edit
    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        with open("jsons/msg_edits.json", "r") as f:
            channel = json.load(f)
        edits_channel = channel[str(message_after.guild.id)]
        if edits_channel == 123:
            return
        else:
            if message_before.content == message_after.content:
                return
            try:
                embed=discord.Embed(description = f"**:pencil2: Message sent by {message_after.author.mention} edited in {message_after.channel.mention}. [Jump to Message]({message_after.jump_url})**",
                                    color = 0x000000, timestamp = datetime.now())
                embed.set_author(name = f"{message_after.author}", icon_url = f"{message_after.author.avatar.url}")
                embed.add_field(name = "Old:", value=f"`{message_before.content}`")
                embed.add_field(name = "New:", value=f"`{message_after.content}`")
                embed.set_footer(text = message_after.guild.name)
                channel=self.bot.get_channel(edits_channel)
                await channel.send(embed=embed)
            except:
                pass


    #on member join
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("jsons/joins.json", "r") as f:
            channel = json.load(f)
        joins_channel = channel[str(member.guild.id)]
        if joins_channel == 123:
            return
        else:
            date_format = "%d/%m/%Y %H:%M"
            channel = self.bot.get_channel(joins_channel)
            e = discord.Embed(title=f"Welcome {member.name}!", description=f"{member.mention} joined the server.", color = 0x000000)
            e.set_author(name=member.name, icon_url=member.avatar.url)
            e.set_thumbnail(url=member.avatar.url)
            e.add_field(name="🕛 Age of Account:", value=f"`{member.created_at.strftime(date_format)}`")
            e.set_footer(text=f"{member.guild.name} • {member.joined_at.strftime(date_format)}")
            await channel.send(embed=e)


    #on member leave
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open("jsons/leaves.json", "r") as f:
            channel = json.load(f)
        leaves_channel = channel[str(member.guild.id)]
        if leaves_channel == 123:
            return
        else:
            date_format = "%d/%m/%Y %H:%M"
            channel = self.bot.get_channel(leaves_channel)
            e = discord.Embed(title=f"**{member.name}** has left!", description=f"{member.mention} left the server.", color = 0x000000)
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
                                   description=f"Use `/sbhelp` for info about the bot!\nOr `<catogery name> <command name>` for info about a specific command!",
                                   color = 0x000000)
            await message.reply(embed=pre_em)


        #get suggest id
        try:
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
        except:
            pass


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

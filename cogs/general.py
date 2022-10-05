import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from random import choice
import wikipedia
from deep_translator import GoogleTranslator


class Invite(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)


class Disavatar(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Server's Profile Avatar", style=discord.ButtonStyle.green)
    async def display_avatar(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This avatar is not for you!", ephemeral=True)
        displayAvatar = user.display_avatar.url
        userAvatar = user.avatar.url
        if displayAvatar == userAvatar:
            button.style=discord.ButtonStyle.gray
            await interaction.response.send_message("> This user doesn't have a server's avatar.", ephemeral=True)
            return await interaction.message.edit(view=self)
        e = discord.Embed(title="Server's Profile Avatar Link", url=f"{displayAvatar}",color=0x000000)
        e.set_author(name=f"{user.name}", icon_url=f"{userAvatar}")
        e.set_image(url=f"{displayAvatar}")
        e.set_footer(text=f"requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        view=Avatar()
        await interaction.message.edit(embed=e, view=view)
        await interaction.response.defer()


class Avatar(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Main Avatar", style=discord.ButtonStyle.blurple)
    async def main_avatar(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This avatar is not for you!", ephemeral=True)
        userAvatar = user.avatar.url
        e = discord.Embed(title="Avatar Link", url=f"{userAvatar}",color=0x000000)
        e.set_author(name=f"{user.name}", icon_url=f"{userAvatar}")
        e.set_image(url=f"{userAvatar}")
        e.set_footer(text=f"requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        view=Disavatar()
        await interaction.message.edit(embed=e, view=view)
        await interaction.response.defer()


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #waking
    @commands.Cog.listener()
    async def on_ready(self):
        print("General is online.")


    #ping command
    @commands.hybrid_command(name = "ping", with_app_command = True, description = "Checks bot response time.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.reply(f">>> _**Pingo!**_\n{round(self.bot.latency * 1000)}ms")


    #wikipedia search
    @commands.hybrid_command(name = "search", aliases=["wiki" , "wikipedia" , "define"], with_app_command = True, description = "A wikipedia searcher.")
    @app_commands.describe(search = "Whatever you want to search.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def search(self, ctx, *, search):
        #usually returns a list, so we turn it into a string, suggestion = true includes suggestions
        searchsearch = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
        try:
            #limits the summary to a maximum of 1950 characters, discord's limit is 2,000 per message
            thesummary = wikipedia.summary(search, chars = 1000)
            summ = thesummary
        except:
            #usually returns a list, so we turn it into a string, suggestion = true includes suggestions
            searchsummary = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
            summ = f"I can't seem to find a summary for that.. Did you mean: {searchsummary}"
        try:
            wikipedia.summary(search, auto_suggest = False) #i think auto suggest is on by default
            wiki_search = search.lower().replace(' ', '_').replace('  ', '_')
            url = f"[Click here to visit {search} wiki page](https://en.wikipedia.org/wiki/{wiki_search})"
        except:
            urlsearch = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '') 
            url = f"I can't find what you're talking about, did you mean: {urlsearch}"
        seach_embed = discord.Embed(title="Search", description=f"{url}", colour=discord.Colour.dark_theme())
        seach_embed.add_field(name = "**Definition**", value = f">>> {searchsearch}")
        seach_embed.add_field(name = "**Summery**", value = f">>> {summ}")
        await ctx.send(embed=seach_embed)

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
                                      description=f"> Please check `_help translate` for more info",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #translate command
    @commands.hybrid_command(name = "translate", aliases=["trans"], with_app_command = True, description = "A translator.")
    @app_commands.describe(to_language = "The language you want to translate to.", to_translate = "Whatever you want to translate.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def translate(self, ctx, to_language, *, to_translate):
        translated = GoogleTranslator(source='auto', target=to_language).translate(to_translate)
        em = discord.Embed(title="Translated", colour=discord.Colour.dark_theme())
        em.add_field(name="Original", value=f"> {to_translate}")
        em.add_field(name="Translation", value=f"> {translated}")
        await ctx.send(embed=em)

    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
                                      description=f"> Please check `_help translate` for more info",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #calc command
    @commands.hybrid_command(name = "calc",
                             aliases=["calculator"],
                             with_app_command = True,
                             description = "Makes calculations for you.")
    @app_commands.describe(first_number = "The first number.", operator = "The operator (+, -, ×, ÷).", second_number = "The second number.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def calc(self, ctx, first_number: int, operator, second_number: int):
        if operator == "+":
            await ctx.send(f"Result: **{first_number+second_number}**")
        elif operator == "-":
            await ctx.send(f"Result: **{first_number-second_number}**")
        elif operator == "*" or operator == "×" or operator == "x":
            await ctx.send(f"Result: **{first_number*second_number}**")
        elif operator == "/" or operator == "÷":
            await ctx.send(f"Result: **{first_number/second_number}**")
        else:
            await ctx.reply(f"> You entered a wrong operator.", ephemeral = True)

    @calc.error
    async def calc_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
                                      description=f"> Please check `_help calc` for more info",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #banner command
    @commands.hybrid_command(name = "banner", with_app_command = True, description = "Shows member's banner.")
    @app_commands.describe(member = "Member you want to show their banner.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def banner(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        #check if user has a banner and fetch it
        try:
            user = await self.bot.fetch_user(member.id)
            banner_url = user.banner.url # The URL of the banner
        except:
            await ctx.reply("> The user doesn't have a banner.", ephemeral = True)
        #sending the banner
        userAvatar = member.avatar.url
        e = discord.Embed(title="Banner Link", url=f"{banner_url}",color=0x000000)
        e.set_author(name=f"{member.name}", icon_url=f"{userAvatar}")
        e.set_image(url=f"{banner_url}")
        e.set_footer(text=f"requested by {ctx.message.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=e)

    @banner.error
    async def banner_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!", description=f"> Please check `_help banner` for more info",colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #embed command
    @commands.hybrid_command(name = "embed", with_app_command = True, description = "Change your text into an embed.")
    @app_commands.describe(text = "The text you want to transform.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def embed(self, ctx, *, text):
        icon = ctx.message.author.avatar.url
        emb = discord.Embed(title=f"__**{ctx.author.name}**'s Embed__", description=f"{text}", color = 0x000000)
        emb.set_footer(text=f"Embed by {ctx.message.author}", icon_url=icon)
        emb.set_thumbnail(url=icon)
        await ctx.send(embed=emb)

    @embed.error
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!", description=f"> Please check `_help embed` for more info",colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #nick commands
    @commands.hybrid_command(name = "nick",
                             aliases=["setnick" ,"nickname"],
                             with_app_command = True,
                             description = "Changes the nickname.")
    @app_commands.describe(member = "Member to change their nickname.", nick = "The new nickname.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: commands.MemberConverter, *, nick):
        if ctx.author == member:
          pass
        elif ctx.author.top_role <= member.top_role:
          await ctx.reply(f">>> You can not change **{member.name}**'s nickname!", mention_author=False, ephemeral = True)
          return
        if member.nick == None:
           oldn = member.name
        else:
           oldn = member.nick
        await member.edit(nick=nick)
        await ctx.send(f"> **{member.mention}**'s nickname has been changed from **{oldn}** to **{nick}**")

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
                                      description=f"> You must have __**Manage Nicknames**__ permission!",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
                                      description=f"> Please check `_help nick` for more info",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #giveaway
    @commands.hybrid_command(name = "giveaway", aliases=["give"], with_app_command = True, description = "Set a giveaway.")
    @app_commands.describe(time = "Giveaway's time.", prize = "Giveaway's prize.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def giveaway(self, ctx, time, *, prize):
        icon = str(ctx.guild.icon.url)
        channel = ctx.channel
        if time:
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            timer = time
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try:
                int(c)
            except:
                return await ctx.reply("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", mention_author=False, ephemeral = True)
            try:
                sleep = int(b) * int(c)
            except:
                return await ctx.reply("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", mention_author=False, ephemeral = True)
        emb = discord.Embed(title="__*🎉GIVEAWAY🎉*__", description=f"React with 🎉 to enter!\nHosted by: {ctx.author.mention}\nPrize: **{prize}**",colour=0xff0000)
        emb.set_footer(text=f"Ends after {timer}.")
        emb.set_thumbnail(url=icon)
        msg = await ctx.send(embed=emb)
        message = str(ctx.message.content)
        if "give" in message:
            await ctx.message.delete()
        await msg.add_reaction("🎉")
        await asyncio.sleep(int(sleep))
        #if not self.cancelled:
        myMsg = await channel.fetch_message(msg.id)
        users = [users async for users in myMsg.reactions[0].users()]
        users.pop(users.index(self.bot.user))
        #Check if User list is not empty
        if len(users) <= 0:
            emptyEmbed = discord.Embed(title="Giveaway Time !!",
                               description="No one won the Giveaway")
            emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
            emptyEmbed.set_footer(text=f"{prize}")
            await myMsg.edit(embed=emptyEmbed)
            return
        if len(users) > 0:
            winner = choice(users)
            # winnerEmbed = discord.Embed(title="Giveaway Time !!",
            #                     description=f"Giveway on {prize} ended today",
            #                     colour=0xffd700)
            # winnerEmbed.add_field(name=f"Congratulations On Winning {prize}", value=winner.mention)
            # winnerEmbed.set_image(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/Loli.png?alt=media&token=ab5c8924-9a14-40a9-97b8-dba68b69195d")
            # await ctx.send(embed=winnerEmbed)
            await msg.edit(content=f"__***🎉Giveway ended, {winner.name} won!🎉***__")
            await msg.reply(f">>> **Congratulations {winner.mention} On Winning {prize} 🎉🎉**")
            return

    @giveaway.error
    async def giveaway_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #tax
    @commands.hybrid_command(name = "tax", aliases=["taxes"], with_app_command = True, description = "Calculates ProBot's taxes.")
    @app_commands.describe(amount = "The amount of credits.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tax(self, ctx, amount: int):
        price = int(amount) / 0.95
        price2 = int(amount) * 0.95
        price3 = int(amount) - price2
        emb = discord.Embed(title="__**Taxes**__ ",
                            description=f"How much ProBot will take: **{int(price3)}**\nHow much will be transfered: **{int(price2)}**\nHow much you should transfer: **{int(price+1)}**",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

    @tax.error
    async def tax_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #avatar
    @commands.hybrid_command(name = "avatar", aliases=["a"], with_app_command = True, description = "Shows member's avatar.")
    @app_commands.describe(member = "Member you want to show their avatar.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar.url
        e = discord.Embed(title="Avatar Link ", url=f"{userAvatar}",color=0x000000)
        e.set_author(name=f"{member.name}", icon_url=f"{userAvatar}")
        e.set_image(url=f"{userAvatar}")
        e.set_footer(text=f"requested by {ctx.message.author}", icon_url=ctx.author.avatar.url)
        global user
        global author
        user = member
        author = ctx.message.author
        view = Disavatar()
        await ctx.send(embed=e, view=view)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #timer
    @commands.hybrid_command(name = "timer", aliases=["stopwatch"], with_app_command = True, description = "A stopwatch for you.")
    @app_commands.describe(time = "The time you want to set.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def timer(self, ctx, time):
        get_time = {
        "s": 1, "m": 60, "h": 3600, "d": 86400,
        "w": 604800, "mo": 2592000, "y": 31104000 }
        timer = time
        a = time[-1]
        b = get_time.get(a)
        c = time[:-1]
        try:
            int(c)
        except:
            return await ctx.reply("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", mention_author=False, ephemeral = True)
        try:
            sleep = int(b) * int(c)
            await ctx.send(f"> Timer set to {timer}.", ephemeral = True)
        except:
            return await ctx.reply("> Type time and time unit [s,m,h,d,w,mo,y] correctly.", mention_author=False, ephemeral = True)
        await asyncio.sleep(sleep)
        await ctx.reply("**Time over**")
        member_dm = await ctx.author.create_dm()
        #await channel.send("**Time over**")
        emb = discord.Embed(title="**Time over**",
                            description=f"> Your Timer '{timer}' has been ended",
                            color=discord.Colour.random())
        await member_dm.send(embed=emb)

    @timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #server link
    @commands.hybrid_command(name = "serverlink", aliases = ["serverinvite"], with_app_command = True, description = "Gets an invite link for the server.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverlink(self, ctx):
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        link = await ctx.channel.create_invite(max_age = 300)
        embed = discord.Embed(title = name, color = discord.Color.blue())
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Invite Link", value = link, inline=True)
        await ctx.send(embed=embed)

    @serverlink.error
    async def serverlink_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #bot invite link
    @commands.hybrid_command(name = "invite", aliases=["botlink"], with_app_command = True, description = "Gets an invite link for the bot.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        view=Invite()
        view.add_item(discord.ui.Button(label="Invite",style=discord.ButtonStyle.link,url="https://discord.com/api/oauth2/authorize?client_id=855437723166703616&permissions=8&scope=bot%20applications.commands"))
        emb = discord.Embed(title="Bot's invite link",
                            description="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=855437723166703616&permissions=8&scope=bot%20applications.commands)",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb, view=view)

    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #poll command
    @commands.hybrid_command(name = "poll", with_app_command = True, description = "Make a poll.")
    @app_commands.describe(text = "The text of the poll.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, text):
        emb = discord.Embed(title="__**Poll!**__", description=f"{text}",color=discord.Colour.blue())
        emb.set_footer(text=f"Poll by {ctx.message.author}", icon_url=ctx.message.author.avatar.url)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        # await msg.add_reaction("https://emoji.gg/assets/emoji/7572-pepe-yes.png")
        # await msg.add_reaction("https://emoji.gg/assets/emoji/2439-pepe-no.png")
        await ctx.message.delete()
      
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
                                      description=f"> You must have __**Manage Messages**__ permission!",
                                      colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))

import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import praw
import aiohttp
from bs4 import BeautifulSoup


class nextMeme(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Next Meme",style=discord.ButtonStyle.green)
    async def blurple_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not your meme!", ephemeral=True)
        reddit = praw.Reddit(
                    client_id = "9bb7uOB_UHhLVDm7NIdCMw",
                    client_secret = "U9XEuutRjZKhaLAVJ1Z-iObYuVOuNQ",
                    user_agent = "ShinobiBot",
                    check_for_async=False
                    )
        subreddit = reddit.subreddit("Animemes")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            name = random_sub.title
            url = random_sub.url
            em = discord.Embed(title = name)
            em.set_image(url = url)
        await interaction.message.edit(embed=em)
        await interaction.response.defer()


#web scrabbing function for wyr command
async def web_scrabe(text):
    async with aiohttp.ClientSession() as session:
        async with session.get(text) as r:
            text = await r.text()
            return text


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is online.")


    # #random img tst
    # @commands.command()
    # async def imgtst(self, ctx):
    #     async with aiohttp.ClientSession() as s:
    #         async with s.get('https://source.unsplash.com/random') as r:
    #             r.url
    #     e = discord.Embed(title="tst", description="trdt", colour=discord.Colour.dark_theme())
    #     e.set_image(url=r.url)
    #     await ctx.send(embed = e)


    #dog reddit
    @commands.hybrid_command(name = "dog", with_app_command = True, description = "Dogs. [BETA]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        reddit = praw.Reddit(
                    client_id = "9bb7uOB_UHhLVDm7NIdCMw",
                    client_secret = "U9XEuutRjZKhaLAVJ1Z-iObYuVOuNQ",
                    user_agent = "ShinobiBot",
                    check_for_async=False
                    )
        subreddit = reddit.subreddit("rarepuppers")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            url = random_sub.url
            em = discord.Embed(colour=discord.Colour.dark_theme())
            em.set_image(url = url)
        await ctx.send(embed = em)

    @dog.error
    async def dog_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #cat reddit
    @commands.hybrid_command(name = "cat", with_app_command = True, description = "Cats. [BETA]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):
        reddit = praw.Reddit(
                    client_id = "9bb7uOB_UHhLVDm7NIdCMw",
                    client_secret = "U9XEuutRjZKhaLAVJ1Z-iObYuVOuNQ",
                    user_agent = "ShinobiBot",
                    check_for_async=False
                    )
        subreddit = reddit.subreddit("cats")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            url = random_sub.url
            em = discord.Embed(colour=discord.Colour.dark_theme())
            em.set_image(url = url)
        await ctx.send(embed = em)

    @cat.error
    async def cat_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #headpat reddit
    @commands.hybrid_command(name = "headpat", aliases = ["headp"], with_app_command = True, description = "Headpats. [BETA]")
    @app_commands.describe(member = "Member you want to pat.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def headpat(self, ctx, member: discord.Member = None):
        reddit = praw.Reddit(
                    client_id = "9bb7uOB_UHhLVDm7NIdCMw",
                    client_secret = "U9XEuutRjZKhaLAVJ1Z-iObYuVOuNQ",
                    user_agent = "ShinobiBot",
                    check_for_async=False
                    )
        subreddit = reddit.subreddit("headpats")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            url = random_sub.url
            em = discord.Embed(colour=discord.Colour.dark_theme())
            em.set_image(url = url)
        if member == None:
            await ctx.send(embed = em)
        else:
            await ctx.send(f"UwU {ctx.author.mention} patted {member.mention}", embed = em)

    @headpat.error
    async def headpat_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #wyr command
    @commands.hybrid_command(name = "wyr", with_app_command= True, description = "Would you rather...")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wyr(self, ctx):
        text = await web_scrabe("http://either.io/")
        soup = BeautifulSoup(text, "lxml")
        l = []
        for choice in soup.find_all("span", {"class":"option-text"}):
            l.append(choice.text)
        e = discord.Embed(colour=discord.Colour.dark_theme())
        e.set_author(name="Would you rather...", url="http://either.io/", icon_url=self.bot.user.avatar.url)
        e.add_field(name="EITHER...", value=f":regional_indicator_a: {l[0]}", inline=False)
        e.add_field(name="OR...", value=f":regional_indicator_b: {l[1]}")
        msg = await ctx.send(embed = e)
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")

    @wyr.error
    async def wyr_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)

    #emojify
    @commands.hybrid_command(name = "emojify", with_app_command= True, description = "Convert your words to emojis!")
    @app_commands.describe(text = "Text you want to transform into emojis.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {"0":"zero" , "1":"one" , "2":"two" , "3":"three" , "4":"four" ,
                          "5":"five" , "6":"six" , "7":"seven" , "8":"eight" , "9":"nine"}
                emojis.append(f":{num2emo.get(s)}:")
            elif s.isalpha():
                emojis.append(f":regional_indicator_{s}:")
            else:
                emojis.append(s)
        await ctx.send(" ".join(emojis))

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)

    #rate command
    @commands.hybrid_command(name = "rate", with_app_command = True, description = "Rates.")
    @app_commands.describe(someone = "Someone to rate.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rate(self, ctx, *, someone: discord.Member =None):
        if someone==None:
            text = "Your"
        else:
            text = someone.mention
        async with ctx.typing():
            await asyncio.sleep(5)
        thing = ["handsome" , "beauty" , "luck" , "success" , "happiness" , "sadness" , "intelligence" , "cringe" , "gay"]
        emoji = ["🙂" , "😆" , "🤣" , "😉" , "😘" , "😏" , "😶" , "😱" , "🤯" , "🥳" , "🤥" , "😳" , "😮" , "😯" , "<:kek:959474451584524308>"]
        await ctx.reply(f">>> {text} **{random.choice(thing)}** rate is **{random.randint(0, 100)}%!** {random.choice(emoji)}", mention_author=False)

    @rate.error
    async def rate_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #meme reddit
    @commands.hybrid_command(name = "meme", with_app_command = True, description = "Memes. [BETA]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def meme(self, ctx):
        reddit = praw.Reddit(
                    client_id = "9bb7uOB_UHhLVDm7NIdCMw",
                    client_secret = "U9XEuutRjZKhaLAVJ1Z-iObYuVOuNQ",
                    user_agent = "ShinobiBot",
                    check_for_async=False
                    )
        subreddit = reddit.subreddit("Animemes")
        all_subs = []
        hot = subreddit.hot(limit=50)
        for submission in hot:
            all_subs.append(submission)
            random_sub = random.choice(all_subs)
            name = random_sub.title
            url = random_sub.url
            em = discord.Embed(title = name, colour=discord.Colour.dark_theme())
            em.set_image(url = url)
        global author
        author = ctx.author
        view=nextMeme()
        await ctx.send(embed = em, view=view)

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #choose command
    @commands.hybrid_command(name = "choose", with_app_command = True, description = "Chooses. (maximum 5 choices.)")
    @app_commands.describe(choice1 = "Choice 1.", choice2 = "Choice 2.", choice3 = "Choice 3.", choice4 = "Choice 4.", choice5 = "Choice 5.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def choose(self, ctx, choice1, choice2, choice3 = None, choice4 = None, choice5 = None):
        if choice3 == None:
            opt = [choice1,choice2]
            optext = f"{choice1} and {choice2}"
        elif choice4 == None:
            opt = [choice1,choice2,choice3]
            optext = f"{choice1}, {choice2} and {choice3}"
        elif choice5 == None:
            opt = [choice1,choice2,choice3,choice4]
            optext = f"{choice1}, {choice2}, {choice3} and {choice4}"
        else:
            opt = [choice1, choice2, choice3, choice4, choice5]
            optext = f"{choice1}, {choice2}, {choice3}, {choice4} and {choice5}"
        msg = await ctx.send(f"Choosing from: {optext}.")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"Choosing from: {optext}..")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"Choosing from: {optext}...")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"Choosing from: {optext}.")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"Choosing from: {optext}..")
        await asyncio.sleep(0.5)
        await msg.edit(content=f"Choosing from: {optext}...")
        await asyncio.sleep(0.5)
        await ctx.reply(content=f"{random.choice(opt)}")

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #coinflip
    @commands.hybrid_command(name = "coinflip", aliases=["flip", "coin"], with_app_command = True, description = "Flip a coin.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #f
    @commands.hybrid_command(name = "f", with_app_command = True, description = "Press f to pay respect.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def f(self, ctx, *, someone_or_something: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{someone_or_something}** " if someone_or_something else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @f.error
    async def f_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #reverse
    @commands.hybrid_command(name = "reverse", with_app_command = True, description = "Reverses your words.")
    @app_commands.describe(your_words = "Words to reverse.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reverse(self, ctx, *, your_words: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = your_words[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @reverse.error
    async def reverse_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


    #slot
    @commands.hybrid_command(name = "slot", with_app_command = True, description = "A slot game.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a, b, c = [random.choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f">>> {slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f">>> {slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f">>> {slotmachine} No match, you lost 😢")

    @slot.error
    async def slot_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))

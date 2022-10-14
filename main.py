import discord
from discord import app_commands
import aiohttp
from discord.ext import commands, tasks
import json
import random
from datetime import timedelta
from cogs.ticket import ticket_launcher, main
import logging
import logging.handlers


class MyBot(commands.Bot):

    def __init__(self):
        def get_prefex(client, message):
            with open("jsons/prefixes.json", "r") as f:
                prefixes = json.load(f)
            return prefixes[str(message.guild.id)]

        super().__init__(command_prefix = get_prefex,
                         intents = discord.Intents.all(),
                         case_insensitive=True,
                         application_id = YOUR_APP_ID)
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)
        self.initial_extensions = [
            "cogs.help", "cogs.error_handler", "cogs.events", "cogs.ticket",
            "cogs.moderation", "cogs.general", "cogs.fun", "cogs.serverinfo",
            "cogs.settings", "cogs.connect4", "cogs.tictactoe", "cogs.rps", "cogs.logs"]
        self.added = False

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for cogs in self.initial_extensions: 
            await self.load_extension(cogs)
        await self.tree.sync()
        print(f"Synced for {self.user}!")

    #closing
    async def close(self):
        await super().close()
        await self.session.close()

    #on_ready message
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True
            # Setting `Playing ` status
            await bot.change_presence(activity=discord.Game(name="/sbhelp"))

    #anti spam
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                try:
                    await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
                    await message.author.send("You have been timed out for spamming!")
                except:
                    await message.channel.send(f"> I cann't timeout {message.author.mention}. Check my role.")

bot = MyBot()
bot.remove_command('help')


#logging stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


#feedback button
class feedbackButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    @discord.ui.button(label="Send Feedback", style=discord.ButtonStyle.blurple)
    async def feedback_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds!", ephemeral = True)
        await interaction.response.send_modal(feedbackModal())


#feedback modal
class feedbackModal(ui.Modal, title = "Send Your Feedback"):
    ftitle = ui.TextInput(label = "Title", style = discord.TextStyle.short, placeholder = "Write a title for the issue/suggestion.", required = True, max_length = 50)
    fdes = ui.TextInput(label = "Long Description", style = discord.TextStyle.short, placeholder = "Descripe the issue/suggestion.", required = True, max_length = 1000)
    fsol = ui.TextInput(label = "Solution (optional)", style = discord.TextStyle.short, placeholder = "Write a solution for the issue.", required = False, max_length = 1000)
    async def on_submit(self, interaction: discord.Interaction):
        channel = bot.get_channel(1027230751651012659)
        invite = await interaction.channel.create_invite(max_age = 300)
        try:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            embed.add_field(name = "Solution", value = self.fsol)
            embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            await channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral=True)
        except:
            embed = discord.Embed(title = f"User: {interaction.user}\nServer: {interaction.guild.name}\n{invite}", description = f"**{self.ftitle}**", timestamp = datetime.now())
            embed.add_field(name = "Description", value = self.fdes)
            embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            await channel.send(embed = embed)
            await interaction.response.send_message("Your feedback has been sent succesfully!", ephemeral=True)


#feedback command
@bot.hybrid_command(name = "feedback", with_app_command = True, description = "Send your feedback directly to the developers.")
@commands.cooldown(1, 600, commands.BucketType.user)
async def feedback(ctx: commands.Context):
    global author
    author = ctx.author
    view = feedbackButton()
    embed = discord.Embed(title = "If you had faced any problems or have any suggestions, feel free to send your feedback!")
    await ctx.send(embed = embed, view=view, ephemeral=True)

@feedback.error
async def feedback_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cool_error = discord.Embed(title=f"Wait before sending another feedback", description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
        await ctx.reply(embed=cool_error, ephemeral=True)

#vote button class
class Vote(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)


#vote command links
@bot.hybrid_command(name = "vote", with_app_command = True, description = "Vote me!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def vote(ctx):
    view=Vote()
    view.add_item(discord.ui.Button(label="Vote Here",style=discord.ButtonStyle.link, url="https://top.gg/bot/855437723166703616"))
    view.add_item(discord.ui.Button(label="Or Here",style=discord.ButtonStyle.link, url="https://discordbotlist.com/bots/shinobi-bot"))
    emb = discord.Embed(title="Bot's Vote links",
                        description="[top.gg](https://top.gg/bot/855437723166703616)\n[discordbotlist](https://discordbotlist.com/bots/shinobi-bot)")
    await ctx.send(embed=emb, view=view)

@vote.error
async def vote_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
        await ctx.reply(embed=cool_error, ephemeral=True)
        await ctx.reply(embed=cool_error, ephemeral=True)


#on join
@bot.event
async def on_guild_join(guild):
    #send msg
    channel = bot.get_channel(1027328777828712479)
    await channel.send(f"I joined {guild.name}")

    #add prefix
    with open("jsons/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "_"
    with open("jsons/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


#on leave
@bot.event
async def on_guild_remove(guild):
    #send msg
    channel = bot.get_channel(1027328806236721283)
    await channel.send(f"I left {guild.name}")

    #remove prefix
    with open("jsons/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("jsons/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    #remove filter toggle
    with open("jsons/filter.json", "r") as f:
        toggle = json.load(f)
    toggle.pop(str(guild.id))
    with open("jsons/filter.json", "w") as f:
        json.dump(toggle, f, indent=4)

    #remove suggest
    with open("jsons/suggest.json", "r", encoding="utf8") as f:
        channels = json.load(f)
    channels.pop(str(guild.id))
    with open("jsons/suggest.json", "w", encoding="utf8") as f:
        json.dump(channels, f, sort_keys=True, indent=4, ensure_ascii=False)

    #remove ticket role
    with open("jsons/ticket_roles.json", "r") as f:
        ticket_role = json.load(f)
    ticket_role.pop(str(guild.id))
    with open("jsons/ticket_roles.json", "w") as f:
        json.dump(ticket_role, f, indent=4)

    #remove joins
    with open("jsons/joins.json", "r") as f:
        joins_channel = json.load(f)
    joins_channel.pop(str(guild.id))
    with open("jsons/joins.json", "w") as f:
        json.dump(joins_channel, f, indent=4)

    #remove leaves
    with open("jsons/leaves.json", "r") as f:
        leaves_channel = json.load(f)
    leaves_channel.pop(str(guild.id))
    with open("jsons/leaves.json", "w") as f:
        json.dump(leaves_channel, f, indent=4)

    #remove deletes
    with open("jsons/msg_deletes.json", "r") as f:
        deletes_channel = json.load(f)
    deletes_channel.pop(str(guild.id))
    with open("jsons/msg_deletes.json", "w") as f:
        json.dump(deletes_channel, f, indent=4)

    #remove edits
    with open("jsons/msg_edits.json", "r") as f:
        edits_channel = json.load(f)
    edits_channel.pop(str(guild.id))
    with open("jsons/msg_edits.json", "w") as f:
        json.dump(edits_channel, f, indent=4)

    #remove channels-log
    with open("jsons/channels_log.json", "r") as f:
        channels_log = json.load(f)
    channels_log.pop(str(guild.id))
    with open("jsons/channels_log.json", "w") as f:
        json.dump(channels_log, f, indent=4)

    #remove members-log
    with open("jsons/members_log.json", "r") as f:
        members_log = json.load(f)
    members_log.pop(str(guild.id))
    with open("jsons/members_log.json", "w") as f:
        json.dump(members_log, f, indent=4)

    #remove roles-log
    with open("jsons/roles_log.json", "r") as f:
        roles_log = json.load(f)
    roles_log.pop(str(guild.id))
    with open("jsons/roles_log.json", "w") as f:
        json.dump(roles_log, f, indent=4)

    #remove server-log
    with open("jsons/server_log.json", "r") as f:
        server_log = json.load(f)
    server_log.pop(str(guild.id))
    with open("jsons/server_log.json", "w") as f:
        json.dump(server_log, f, indent=4)


#join voice
@bot.hybrid_command(name = "join", with_app_command = True, description = "Join voice channel.")
async def join(ctx):
    if ctx.author.voice is None:
        return await ctx.send("You are not connected to a voice channel.")
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    await ctx.author.voice.channel.connect()
    await ctx.send("Joined")

#leave voice
@bot.hybrid_command(name = "leave", with_app_command = True, description = "Leave voice channel.")
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        return await ctx.send("Left")
    await ctx.send("I am not connected to a voice channel.")


#number of servers
@bot.hybrid_command(name = "guilds", with_app_command = True, description = "guilds.")
async def guilds(ctx):
    if ctx.author.id == YOUR_ID: # if you want only you to use this command
        await ctx.send(f"I'm in {str(len(bot.guilds))} servers!")
    else:
        await ctx.send("You can not use this command..", ephemeral=True)


#list of servers
@bot.hybrid_command(name = "guildslist", with_app_command = True, description = "guildslist.")
async def guildslist(ctx):
    if ctx.author.id == YOUR_ID: # if you want only you to use this command
        servers = list(bot.guilds)
        await ctx.send(f"Connected on {str(len(bot.guilds))} servers:\n>>> " + '\n'.join(server.name for server in servers))
    else:
        await ctx.send("You can not use this command..", ephemeral=True)


bot.run(YOUR_TOKEN)

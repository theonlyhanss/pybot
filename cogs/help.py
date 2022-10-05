import discord
from discord import app_commands
from discord.ext import commands


class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Index', description='Shows the main help page.', emoji='👋'),
            discord.SelectOption(label='Moderation', description='Shows moderation commands.', emoji='⚒️'),
            discord.SelectOption(label='Utility', description='Shows utility commands.', emoji='🔧'),
            discord.SelectOption(label='Settings', description='Shows Settings commands', emoji='⚙️'),
            discord.SelectOption(label='Fun', description='Shows fun commands', emoji='🎉'),
            discord.SelectOption(label='Games', description='Shows games commands', emoji='🎮'),
            discord.SelectOption(label='Ticket', description='Shows ticket commands', emoji='📩'),
            discord.SelectOption(label='Server Information', description='Shows server information commands', emoji='ℹ️'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select category.', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        #check user
        if interaction.user != author:
            await interaction.response.send_message("> Use your own help command!", ephemeral=True)
            return

        #index page
        if self.values[0] == "Index":
            em = discord.Embed(title = "**Shinobi Bot Help**",
                            description = "Hello! Welcome to the help page.\n\nUse `/vote` to vote me.\nUse `/feedback` to send your feedback directly to the developers.\nUse `<category name> <command name>` for more info on a command.\nUse the dropdown menu below to select a category.\n\n",
                            color = 0x000000)
            em.add_field(name = "**Who are you?**",
                        value = "I'm a bot developed by Shinobi#8010. I'm a multipurpose bot than can do anything. You can get more info using the dropdown menu below.")
            em.add_field(name = "**Features**",
                        value = "- Over 80+ commands ready to use!\n- Moderation, Utility, Games and More!\n- Advanced Ticket System, Suggestions System, Welcomer and Giveways!\n- Anti-Spam and Bad Words Filter!\n- And much more!")
            await interaction.message.edit(embed=em)
            await interaction.response.defer()

        #moderation page
        if self.values[0] == "Moderation":
            embed = discord.Embed(title = "**Moderation**",
                            description = "Moderation commands that helps in moderating the server!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = ">>> kick , multikick , mute , multimute , unmute , warn , multiwarn , unwarn , warnings , jail , multijail , unjail , ban , multiban , unban , unbanall , timeout , multitimeout , clear , role , delrole")
            embed.set_footer(text = "Use `moderation <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #general/utility page
        elif self.values[0] == "Utility":
            embed = discord.Embed(title = "**Utility**",
                            description = "Utility commands contains varies types of commands to use!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> poll , ping , serverlink , invite , timer , avatar , banner , tax , nick , embed , calc , giveaway , translate , search")
            embed.set_footer(text = "Use `utility <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #fun page
        elif self.values[0] == "Fun":
            embed = discord.Embed(title = "**Fun**",
                            description = "Fun commands to have fun!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> meme , rate , f , coinflip , reverse , slot , choose , emojify , wyr , headpat , cat")
            embed.set_footer(text = "Use `fun <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #settings page
        elif self.values[0] == "Settings":
            embed = discord.Embed(title = "**Settings**",
                            description = "Server Settings!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> lock , lockall , unlock , unloackall , hide , hideall , show , showall , filtertoggle , suggest , prvchannel , welcome")
            embed.set_footer(text = "Use `settings <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #games page
        elif self.values[0] == "Games":
            embed = discord.Embed(title = "**Games**",
                            description = "Challange others in games!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> connect4 , tictactoe , rps")
            embed.set_footer(text = "Use `games <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #ticket page
        elif self.values[0] == "Ticket":
            embed = discord.Embed(title = "**Ticket**",
                            description = "Create and moderate a ticket!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> ticket , close , add , remove , ticketrole")
            embed.set_footer(text = "Use `ticket <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        #serverinfo page
        elif self.values[0] == "Server Information":
            embed = discord.Embed(title = "**Server Information**",
                            description = "Know more about your server and members!",
                            color = 0x000000)
            embed.add_field(name = "**Commands**" ,
                            value = "> server , owner , id , members , channels , user , icon , roles")
            embed.set_footer(text = "Use `serverinformation <command>` for extended information on a command.")
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

#dropdown class
class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


#help class
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help is online.")


    #help command
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def help(self, ctx):
        em = discord.Embed(title = "**Shinobi Bot Help**",
                           description = "Hello! Welcome to the help page.\n\nUse `/vote` to vote me.\nUse `/feedback` to send your feedback directly to the developers.\nUse `<category name> <command name>` for more info on a command.\nUse the dropdown menu below to select a category.\n\n",
                           color = 0x000000)
        em.add_field(name = "**Who are you?**",
                    value = "I'm a bot developed by Shinobi#8010. I'm a multipurpose bot than can do anything. You can get more info using the dropdown menu below.")
        em.add_field(name = "**Features**",
                    value = "- Over 80+ commands ready to use!\n- Moderation, Utility, Games and More!\n- Advanced Ticket System, Suggestions System, Welcomer and Giveways!\n- Anti-Spam and Bad Words Filter!\n- And much more!")
        global author
        author = ctx.message.author
        view = DropdownView()
        await ctx.send(embed = em, view=view)

#=====================================================================================================================

    #sbhelp (mainly for slash use)
    @commands.hybrid_command(name = "sbhelp", with_app_command = True, description = "Bot's help command.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def sbhelp(self, ctx):
        await ctx.invoke(self.bot.get_command('help'))

#=====================================================================================================================
                                ###SLASH ONLY###
    #moderation commands help
    @commands.hybrid_command(name = "moderation", with_app_command = True, description = "Bot's moderation catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="mute", value="mute"),
        app_commands.Choice(name="multimute", value="multimute"),
        app_commands.Choice(name="unmute", value="unmute"),
        app_commands.Choice(name="jail", value="jail"),
        app_commands.Choice(name="multijail", value="multijail"),
        app_commands.Choice(name="unjail", value="unjail"),
        app_commands.Choice(name="kick", value="kick"),
        app_commands.Choice(name="multikick", value="multikick"),
        app_commands.Choice(name="ban", value="ban"),
        app_commands.Choice(name="multiban", value="multiban"),
        app_commands.Choice(name="unban", value="unban"),
        app_commands.Choice(name="unbanall", value="unbanall"),
        app_commands.Choice(name="timeout", value="timeout"),
        app_commands.Choice(name="multitimeout", value="multitimeout"),
        app_commands.Choice(name="clear", value="clear"),
        app_commands.Choice(name="role", value="role"),
        app_commands.Choice(name="delrole", value="delrole"),
        app_commands.Choice(name="prefix", value="prefix"),
        app_commands.Choice(name="warn", value="warn"),
        app_commands.Choice(name="multiwarn", value="multiwarn"),
        app_commands.Choice(name="unwarn", value="unwarn"),
        app_commands.Choice(name="warnings", value="warnings")
        ])
    async def moderation(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'mute'):
            await ctx.invoke(self.bot.get_command('help mute'))
        if (command.value == 'multimute'):
            await ctx.invoke(self.bot.get_command('help multimute'))
        elif (command.value == 'unmute'):
            await ctx.invoke(self.bot.get_command('help unmute'))
        elif (command.value == 'jail'):
            await ctx.invoke(self.bot.get_command('help jail'))
        elif (command.value == 'multijail'):
            await ctx.invoke(self.bot.get_command('help multijail'))
        elif (command.value == 'unjail'):
            await ctx.invoke(self.bot.get_command('help unjail'))
        elif (command.value == 'kick'):
            await ctx.invoke(self.bot.get_command('help kick'))
        elif (command.value == 'multikick'):
            await ctx.invoke(self.bot.get_command('help multikick'))
        elif (command.value == 'ban'):
            await ctx.invoke(self.bot.get_command('help ban'))
        elif (command.value == 'multiban'):
            await ctx.invoke(self.bot.get_command('help multiban'))
        elif (command.value == 'unban'):
            await ctx.invoke(self.bot.get_command('help unban'))
        elif (command.value == 'unbanall'):
            await ctx.invoke(self.bot.get_command('help unbanall'))
        elif (command.value == 'timeout'):
            await ctx.invoke(self.bot.get_command('help timeout'))
        elif (command.value == 'multitimeout'):
            await ctx.invoke(self.bot.get_command('help multitimeout'))
        elif (command.value == 'clear'):
            await ctx.invoke(self.bot.get_command('help clear'))
        elif (command.value == 'role'):
            await ctx.invoke(self.bot.get_command('help role'))
        elif (command.value == 'delrole'):
            await ctx.invoke(self.bot.get_command('help delrole'))
        elif (command.value == 'warn'):
            await ctx.invoke(self.bot.get_command('help warn'))
        elif (command.value == 'multiwarn'):
            await ctx.invoke(self.bot.get_command('help multiwarn'))
        elif (command.value == 'unwarn'):
            await ctx.invoke(self.bot.get_command('help unwarn'))
        elif (command.value == 'warnings'):
            await ctx.invoke(self.bot.get_command('help warnings'))


    #utility commands help
    @commands.hybrid_command(name = "utility", with_app_command = True, description = "Bot's utility catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="poll", value="poll"),
        app_commands.Choice(name="invite", value="invite"),
        app_commands.Choice(name="serverlink", value="serverlink"),
        app_commands.Choice(name="avatar", value="avatar"),
        app_commands.Choice(name="banner", value="banner"),
        app_commands.Choice(name="calc", value="calc"),
        app_commands.Choice(name="tax", value="tax"),
        app_commands.Choice(name="nick", value="nick"),
        app_commands.Choice(name="search", value="search"),
        app_commands.Choice(name="translate", value="translate"),
        app_commands.Choice(name="giveaway", value="giveaway"),
        app_commands.Choice(name="embed", value="embed"),
        app_commands.Choice(name="timer", value="timer"),
        app_commands.Choice(name="ping", value="ping")
        ])
    async def utility(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'poll'):
            await ctx.invoke(self.bot.get_command('help poll'))
        elif (command.value == 'invite'):
            await ctx.invoke(self.bot.get_command('help invite'))
        elif (command.value == 'serverlink'):
            await ctx.invoke(self.bot.get_command('help serverlink'))
        elif (command.value == 'avatar'):
            await ctx.invoke(self.bot.get_command('help avatar'))
        elif (command.value == 'banner'):
            await ctx.invoke(self.bot.get_command('help banner'))
        elif (command.value == 'calc'):
            await ctx.invoke(self.bot.get_command('help calc'))
        elif (command.value == 'tax'):
            await ctx.invoke(self.bot.get_command('help tax'))
        elif (command.value == 'nick'):
            await ctx.invoke(self.bot.get_command('help nick'))
        elif (command.value == 'search'):
            await ctx.invoke(self.bot.get_command('help search'))
        elif (command.value == 'translate'):
            await ctx.invoke(self.bot.get_command('help translate'))
        elif (command.value == 'giveaway'):
            await ctx.invoke(self.bot.get_command('help giveaway'))
        elif (command.value == 'embed'):
            await ctx.invoke(self.bot.get_command('help embed'))
        elif (command.value == 'timer'):
            await ctx.invoke(self.bot.get_command('help timer'))
        elif (command.value == 'ping'):
            await ctx.invoke(self.bot.get_command('help ping'))


    #settings commands help
    @commands.hybrid_command(name = "settings", with_app_command = True, description = "Bot's games catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="lock", value="lock"),
        app_commands.Choice(name="lockall", value="lockall"),
        app_commands.Choice(name="unlock", value="unlock"),
        app_commands.Choice(name="unlockall", value="unlockall"),
        app_commands.Choice(name="hide", value="hide"),
        app_commands.Choice(name="hideall", value="hideall"),
        app_commands.Choice(name="show", value="show"),
        app_commands.Choice(name="showall", value="showall"),
        app_commands.Choice(name="filtertoggle", value="filtertoggle"),
        app_commands.Choice(name="suggest", value="suggest"),
        app_commands.Choice(name="prvchannel", value="prvchannel"),
        app_commands.Choice(name="welcome", value="welcome")
        ])
    async def settings(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'lock'):
            await ctx.invoke(self.bot.get_command('help lock'))
        elif (command.value == 'lockall'):
            await ctx.invoke(self.bot.get_command('help lockall'))
        elif (command.value == 'unlock'):
            await ctx.invoke(self.bot.get_command('help unlock'))
        elif (command.value == 'unlockall'):
            await ctx.invoke(self.bot.get_command('help unlockall'))
        elif (command.value == 'hide'):
            await ctx.invoke(self.bot.get_command('help hide'))
        elif (command.value == 'hideall'):
            await ctx.invoke(self.bot.get_command('help hideall'))
        elif (command.value == 'show'):
            await ctx.invoke(self.bot.get_command('help show'))
        elif (command.value == 'showall'):
            await ctx.invoke(self.bot.get_command('help showall'))
        elif (command.value == 'filtertoggle'):
            await ctx.invoke(self.bot.get_command('help filtertoggle'))
        elif (command.value == 'prvchannel'):
            await ctx.invoke(self.bot.get_command('help prvchannel'))
        elif (command.value == 'suggest'):
            await ctx.invoke(self.bot.get_command('help suggest'))
        elif (command.value == 'welcome'):
            await ctx.invoke(self.bot.get_command('help welcome'))


    #fun commands help
    @commands.hybrid_command(name = "fun", with_app_command = True, description = "Bot's fun catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="meme", value="meme"),
        app_commands.Choice(name="rate", value="rate"),
        app_commands.Choice(name="f", value="f"),
        app_commands.Choice(name="coinflip", value="coinflip"),
        app_commands.Choice(name="reverse", value="reverse"),
        app_commands.Choice(name="slot", value="slot"),
        app_commands.Choice(name="choose", value="choose"),
        app_commands.Choice(name="emojify", value="emojify"),
        app_commands.Choice(name="wyr", value="wyr"),
        app_commands.Choice(name="headpat", value="headpat"),
        app_commands.Choice(name="cat", value="cat")
        ])
    async def fun(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'meme'):
            await ctx.invoke(self.bot.get_command('help meme'))
        elif (command.value == 'rate'):
            await ctx.invoke(self.bot.get_command('help rate'))
        elif (command.value == 'serverlink'):
            await ctx.invoke(self.bot.get_command('help serverlink'))
        elif (command.value == 'f'):
            await ctx.invoke(self.bot.get_command('help f'))
        elif (command.value == 'coinflip'):
            await ctx.invoke(self.bot.get_command('help coinflip'))
        elif (command.value == 'reverse'):
            await ctx.invoke(self.bot.get_command('help reverse'))
        elif (command.value == 'slot'):
            await ctx.invoke(self.bot.get_command('help slot'))
        elif (command.value == 'choose'):
            await ctx.invoke(self.bot.get_command('help choose'))
        elif (command.value == 'emojify'):
            await ctx.invoke(self.bot.get_command('help emojify'))
        elif (command.value == 'wyr'):
            await ctx.invoke(self.bot.get_command('help wyr'))
        elif (command.value == 'headpat'):
            await ctx.invoke(self.bot.get_command('help headpat'))
        elif (command.value == 'cat'):
            await ctx.invoke(self.bot.get_command('help cat'))


    #games commands help
    @commands.hybrid_command(name = "games", with_app_command = True, description = "Bot's games catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="connect4", value="connect4"),
        app_commands.Choice(name="tictactoe", value="tictactoe"),
        app_commands.Choice(name="rps", value="rps")
        ])
    async def games(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'connect4'):
            await ctx.invoke(self.bot.get_command('help connect4'))
        elif (command.value == 'tictactoe'):
            await ctx.invoke(self.bot.get_command('help tictactoe'))
        elif (command.value == 'rps'):
            await ctx.invoke(self.bot.get_command('help rps'))


    #ticket commands help
    @commands.hybrid_command(name = "ticket", with_app_command = True, description = "Bot's ticket catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="ticket", value="ticket"),
        app_commands.Choice(name="close", value="close"),
        app_commands.Choice(name="add", value="add"),
        app_commands.Choice(name="remove", value="remove"),
        app_commands.Choice(name="ticketrole", value="ticketrole")
        ])
    async def ticket(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'ticket'):
            await ctx.invoke(self.bot.get_command('help ticket'))
        elif (command.value == 'close'):
            await ctx.invoke(self.bot.get_command('help close'))
        elif (command.value == 'add'):
            await ctx.invoke(self.bot.get_command('help add'))
        elif (command.value == 'remove'):
            await ctx.invoke(self.bot.get_command('help remove'))
        elif (command.value == 'ticketrole'):
            await ctx.invoke(self.bot.get_command('help ticketrole'))

    #serverinformation commands help
    @commands.hybrid_command(name = "serverinformation", with_app_command = True, description = "Bot's server information catogery help.")
    @app_commands.describe(command = "Choose a command to get info about it.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.choices(command=[
        app_commands.Choice(name="server", value="server"),
        app_commands.Choice(name="owner", value="owner"),
        app_commands.Choice(name="id", value="id"),
        app_commands.Choice(name="members", value="members"),
        app_commands.Choice(name="channels", value="channels"),
        app_commands.Choice(name="user", value="user"),
        app_commands.Choice(name="icon", value="icon"),
        app_commands.Choice(name="roles", value="roles"),
        ])
    async def serverinformation(self, ctx, command: app_commands.Choice[str]):
        if (command.value == 'server'):
            await ctx.invoke(self.bot.get_command('help server'))
        elif (command.value == 'owner'):
            await ctx.invoke(self.bot.get_command('help owner'))
        elif (command.value == 'id'):
            await ctx.invoke(self.bot.get_command('help id'))
        elif (command.value == 'members'):
            await ctx.invoke(self.bot.get_command('help members'))
        elif (command.value == 'channels'):
            await ctx.invoke(self.bot.get_command('help channels'))
        elif (command.value == 'user'):
            await ctx.invoke(self.bot.get_command('help user'))
        elif (command.value == 'icon'):
            await ctx.invoke(self.bot.get_command('help icon'))
        elif (command.value == 'roles'):
            await ctx.invoke(self.bot.get_command('help roles'))

#==================================================================================================================================================================
                                ###prefix stuff###

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def kick(self, ctx):
        em = discord.Embed(title = "__**Kick**__", description = "Kicks a member from the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> kick <member> [reason]")
        em.add_field(name = "**Example:**", value = "> `kick @member breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multikick(self, ctx):
        em = discord.Embed(title = "__**Multi-Kick**__", description = "Kicks multiple members from the server. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multikick <member1> <member2> <member3> <member4> <member5> [reason]")
        em.add_field(name = "**Example:**", value = "> `multikick @member1 @member2 @member3 @member4 @member5 breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ban(self, ctx):
        em = discord.Embed(title = "__**Ban**__", description = "Bans a member from the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> ban <member> [reason]")
        em.add_field(name = "**Example:**", value = "> `ban @member breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multiban(self, ctx):
        em = discord.Embed(title = "__**Multi-Ban**__", description = "Bans multiple members from the server. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multiban <member1> <member2> <member3> <member4> <member5> [reason]")
        em.add_field(name = "**Example:**", value = "> `multiban @member1 @member2 @member3 @member4 @member5 breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def jail(self, ctx):
        em = discord.Embed(title = "__**Jail**__", description = "Jails a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> jail <member> [time] [reason]")
        em.add_field(name = "**Example:**", value = "> `jail @member 2h breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multijail(self, ctx):
        em = discord.Embed(title = "__**Multi-Jail**__", description = "Jails multiple members. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multijail <member1> <member2> <member3> <member4> <member5> [time] [reason]")
        em.add_field(name = "**Example:**", value = "> `multijail @member1 @member2 @member3 @member4 @member5 2h breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unjail(self, ctx):
        em = discord.Embed(title = "__**Unjail**__", description = "Unjail a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> Unjail <member>")
        em.add_field(name = "**Example:**", value = "> `Unjail @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mute(self, ctx):
        em = discord.Embed(title = "__**Mute**__", description = "Mutes a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> mute <member> [time] [reason]")
        em.add_field(name = "**Example:**", value = "> `mute @member 2h breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multimute(self, ctx):
        em = discord.Embed(title = "__**Multi-Mute**__", description = "Mutes multiple members. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multimute <member1> <member2> <member3> <member4> <member5> [time] [reason]")
        em.add_field(name = "**Example:**", value = "> `multimute @member1 @member2 @member3 @member4 @member5 2h breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unmute(self, ctx):
        em = discord.Embed(title = "__**Unmute**__", description = "Unmutes a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unmute <member>")
        em.add_field(name = "**Example:**", value = "> `unmute @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unban(self, ctx):
        em = discord.Embed(title = "__**Unban**__", description = "Unbans a user.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unban <user>")
        em.add_field(name = "**Example:**", value = "> `unban <user's id>`")
        em.add_field(name = "**Note:**", value = "> User's ID must be given.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unbanall(self, ctx):
        em = discord.Embed(title = "__**Unbanall**__", description = "Unbans all banned users.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unbanall")
        em.add_field(name = "**Example:**", value = "> `unbanall`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def timeout(self, ctx):
        em = discord.Embed(title = "__**Timeout**__", description = "Timeouts a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> timeout <member> <time> [reason]")
        em.add_field(name = "**Example:**", value = "> `timeout @member 2h bad mood`")
        em.add_field(name = "**Note:**", value = "> A time must be given.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multitimeout(self, ctx):
        em = discord.Embed(title = "__**Multi-Timeout**__", description = "Timeouts multiple members. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multitimeout [time] <member1> <member2> <member3> <member4> <member5> [reason]")
        em.add_field(name = "**Example:**", value = "> `multitimeout 2h @member1 @member2 @member3 @member4 @member5 breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clear(self, ctx):
        em = discord.Embed(title = "__**Clear**__", description = "Clears messages.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> clear [amount]")
        em.add_field(name = "**Example:**", value = "> clear 5`")
        em.add_field(name = "**Note:**", value = "> Deafult amount is 1.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def role(self, ctx):
        em = discord.Embed(title = "__**Role**__", description = "Adds a role to a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> role <member> <role>")
        em.add_field(name = "**Example:**", value = "> `role @member Admin`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def delrole(self, ctx):
        em = discord.Embed(title = "__**Delrole**__", description = "Deletes a role from a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> delrole <member> <role>")
        em.add_field(name = "**Example:**", value = "> `delrole @member Admin`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def lock(self, ctx):
        em = discord.Embed(title = "__**Lock**__", description = "Locks a channel.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> lock [channel]")
        em.add_field(name = "**Example:**", value = "> `lock #channel`")
        em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def lockall(self, ctx):
        em = discord.Embed(title = "__**Lock All**__", description = "Locks all channels in the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> lockall")
        em.add_field(name = "**Example:**", value = "> `lockall`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unlock(self, ctx):
        em = discord.Embed(title = "__**Unlock**__", description = "Unlocks a channel.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unlock [channel]")
        em.add_field(name = "**Example:**", value = "> `unlock #channel`")
        em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unlockall(self, ctx):
        em = discord.Embed(title = "__**Unlockall**__", description = "Unlocks all channels in the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unlockall")
        em.add_field(name = "**Example:**", value = "> `unlockall`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def hide(self, ctx):
        em = discord.Embed(title = "__**Hide**__", description = "Hides a channel.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> hide [channel]")
        em.add_field(name = "**Example:**", value = "> `hide #channel`")
        em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def hideall(self, ctx):
        em = discord.Embed(title = "__**Hide All**__", description = "Hides all channels in the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> hideall")
        em.add_field(name = "**Example:**", value = "> `hideall`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def show(self, ctx):
        em = discord.Embed(title = "__**Show**__", description = "Shows a channel.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> show [channel]")
        em.add_field(name = "**Example:**", value = "> `show #channel`")
        em.add_field(name = "**Note:**", value = "> If no channel is mentioned, deafult is message's channel.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def showall(self, ctx):
        em = discord.Embed(title = "__**Show All**__", description = "Shows all channels in the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> showall")
        em.add_field(name = "**Example:**", value = "> `showall`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def prvchannel(self, ctx):
        em = discord.Embed(title = "__**Prvchannel**__", description = "Creates a temprory private channel.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> prvchannel <time> <channel name>")
        em.add_field(name = "**Example:**", value = "> `prvchannel 3h discussion`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def prefix(self, ctx):
        em = discord.Embed(title = "__**Prefix**__", description = "Changes server's prefix.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> prefix <new prefix>")
        em.add_field(name = "**Example:**", value = "> `prefix !`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def warn(self, ctx):
        em = discord.Embed(title = "__**Warn**__", description = "Warns a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> warn <member> [reason]")
        em.add_field(name = "**Example:**", value = "> `warn @member abusing the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def multiwarn(self, ctx):
        em = discord.Embed(title = "__**Multi-Warn**__", description = "Warns multiple members. (maximum 5 members.)", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> multiwarn <member1> <member2> <member3> <member4> <member5> [reason]")
        em.add_field(name = "**Example:**", value = "> `multiwarn @member1 @member2 @member3 @member4 @member5 breaking the rules`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unwarn(self, ctx):
        em = discord.Embed(title = "__**Unwarn**__", description = "Unwarns a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> unwarn <member>")
        em.add_field(name = "**Example:**", value = "> `unwarn @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def warnings(self, ctx):
        em = discord.Embed(title = "__**Warnings**__", description = "Gets a list of warnings for a member.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> warnings <member>")
        em.add_field(name = "**Example:**", value = "> `warnings @member`")
        em.add_field(name = "**Note:**", value = "> Warnings for users are synced across all servers.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def filtertoggle(self, ctx):
        em = discord.Embed(title = "__**Filter Toggle**__", description = "Enable/Disable swears filter.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> filtertoggle")
        em.add_field(name = "**Example:**", value = "> `filtertoggle`")
        em.add_field(name = "**Note:**", value = "> It's disabled by default.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

#======================================================================================================================================================

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def meme(self, ctx):
        em = discord.Embed(title = "__**Meme**__", description = "Gets a nice meme.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> meme")
        em.add_field(name = "**Example:**", value = "> `meme`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def rate(self, ctx):
        em = discord.Embed(title = "__**Rate**__", description = "Rates.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> rate")
        em.add_field(name = "**Example:**", value = "> `rate`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)
      
    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def coinflip(self, ctx):
        em = discord.Embed(title = "__**Coinflip**__", description = "Flips a coin.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> coinflip")
        em.add_field(name = "**Example:**", value = "> `coinflip`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)
      
    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def f(self, ctx):
        em = discord.Embed(title = "__**F**__", description = "Press f to pay respect.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> f")
        em.add_field(name = "**Example:**", value = "> `f`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)
      
    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reverse(self, ctx):
        em = discord.Embed(title = "__**Reverse**__", description = "Reverses anything you type.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> reverse <words>")
        em.add_field(name = "**Example:**", value = "> `reverse this will be reversed`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def slot(self, ctx):
        em = discord.Embed(title = "__**Slot**__", description = "Slot machine.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> slot")
        em.add_field(name = "**Example:**", value = "> `slot`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choose(self, ctx):
        em = discord.Embed(title = "__**Choose**__", description = "Makes the choosing easier.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> choose <choice 1> <choice 2> [choice 3] [choice 4] [choice 5]")
        em.add_field(name = "**Example:**", value = "> `choose aot kny sao naruto conan`")
        em.add_field(name = "**Note:**", value = "> You must include at least 2 choices and maximum 5")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def emojify(self, ctx):
        em = discord.Embed(title = "__**Emojify**__", description = "Converts any word to emojis.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> emojify <words>")
        em.add_field(name = "**Example:**", value = "> `emojify Hello World`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def wyr(self, ctx):
        em = discord.Embed(title = "__**WYR**__", description = "Would you rather...", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> wyr")
        em.add_field(name = "**Example:**", value = "> `wyr`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def headpat(self, ctx):
        em = discord.Embed(title = "__**Headpat**__", description = "Get a random headpat.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> headpat [member]")
        em.add_field(name = "**Example:**", value = "> `headpat @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cat(self, ctx):
        em = discord.Embed(title = "__**Cat**__", description = "Get a random cat.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> cat")
        em.add_field(name = "**Example:**", value = "> `cat`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

#======================================================================================================================================================

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def server(self, ctx):
        em = discord.Embed(title = "__**Server**__", description = "All information about the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> server")
        em.add_field(name = "**Example:**", value = "> `server`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def owner(self, ctx):
        em = discord.Embed(title = "__**Owner**__", description = "Shows the owner of the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> owner")
        em.add_field(name = "**Example:**", value = "> `owner`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def id(self, ctx):
        em = discord.Embed(title = "__**ID**__", description = "Shows the ID of the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> id")
        em.add_field(name = "**Example:**", value = "> `id`")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def members(self, ctx):
        em = discord.Embed(title = "__**Members**__", description = "Shows the members' count of the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> memebrs")
        em.add_field(name = "**Example:**", value = "> `members`")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def user(self, ctx):
        em = discord.Embed(title = "__**User**__", description = "All information about the user.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> user [member]")
        em.add_field(name = "**Example:**", value = "> `user`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def icon(self, ctx):
        em = discord.Embed(title = "__**Icon**__", description = "Shows server's icon/avatar.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> icon")
        em.add_field(name = "**Example:**", value = "> `icon`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def channels(self, ctx):
        em = discord.Embed(title = "__**Channels**__", description = "Shows server's channels' count.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> channels")
        em.add_field(name = "**Example:**", value = "> `channels`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)
      
    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roles(self, ctx):
        em = discord.Embed(title = "__**Roles**__", description = "Gets a list of all the roles in the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> roles")
        em.add_field(name = "**Example:**", value = "> `roles`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

#======================================================================================================================================================

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def poll(self, ctx):
        em = discord.Embed(title = "__**Poll**__", description = "Makes a poll.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> poll <content>")
        em.add_field(name = "**Example:**", value = "> `poll about the new role...`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ping(self, ctx):
        em = discord.Embed(title = "__**Ping**__", description = "Shows bot's latency.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> ping")
        em.add_field(name = "**Example:**", value = "> `ping`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def serverlink(self, ctx):
        em = discord.Embed(title = "__**Server link**__", description = "Creates an instant invite link for the server.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> serverlink")
        em.add_field(name = "**Example:**", value = "> `serverlink`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def invite(self, ctx):
        em = discord.Embed(title = "__**Invite**__", description = "Send bot's invite link.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> invite")
        em.add_field(name = "**Example:**", value = "> `invite`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def timer(self, ctx):
        em = discord.Embed(title = "__**Timer**__", description = "Starts a timer.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> timer <timer>")
        em.add_field(name = "**Example:**", value = "> `timer 20m`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def avatar(self, ctx):
        em = discord.Embed(title = "__**Avatar**__", description = "Get's member's avatar.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> avatar [member]")
        em.add_field(name = "**Example:**", value = "> `avatar @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def banner(self, ctx):
        em = discord.Embed(title = "__**Banner**__", description = "Get's member's banner.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> banner [member]")
        em.add_field(name = "**Example:**", value = "> `banner @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def tax(self, ctx):
        em = discord.Embed(title = "__**Tax**__", description = "Calculates ProBot tax.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> tax <amount>")
        em.add_field(name = "**Example:**", value = "> `tax 10000`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def giveaway(self, ctx):
        em = discord.Embed(title = "__**Giveaway**__", description = "Starts a giveaway.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> giveaway <time> <prize>")
        em.add_field(name = "**Example:**", value = "> `giveaway 6h credits`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def nick(self, ctx):
        em = discord.Embed(title = "__**Nick**__", description = "Changes member's nickname.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> nick <member> <nickname>")
        em.add_field(name = "**Example:**", value = "> `nick @member tester`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed(self, ctx):
        em = discord.Embed(title = "__**Embed**__", description = "Converts your words to an embed.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> embed <words>")
        em.add_field(name = "**Example:**", value = "> `embed this will be an embed`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def calc(self, ctx):
        em = discord.Embed(title = "__**Calc**__", description = "Calculates for you.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> calc <first number> <operator> <second number>")
        em.add_field(name = "**Example:**", value = "> `calc 20 + 15`")
        em.add_field(name = "**Note:**", value = "> Make sure to put a space between the numbers and the operator.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def translate(self, ctx):
        em = discord.Embed(title = "__**Translate**__", description = "A translator.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> translate <language to translate> <words>")
        em.add_field(name = "**Example:**", value = "> `translate english prueba`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def search(self, ctx):
        em = discord.Embed(title = "__**Search**__", description = "Searches wikipedia for you.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> search <your search>")
        em.add_field(name = "**Example:**", value = "> `search python programming`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def suggest(self, ctx):
        em = discord.Embed(title = "__**Suggest**__", description = "Set channels for suggestions.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> suggest <suggestions channel> <suggestions' review channel>")
        em.add_field(name = "**Example:**", value = "> `suggest #suggestions #suggestions-review`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def welcome(self, ctx):
        em = discord.Embed(title = "__**Welcome**__", description = "Set a channel to announce joining and leaving of members.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> welcome <channel>")
        em.add_field(name = "**Example:**", value = "> `welcome #channel`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

#==============================================================================================================================

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def connect4(self, ctx):
        em = discord.Embed(title = "__**Connect4**__", description = "Challenge others in connect 4!", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> connect4 <player 2>")
        em.add_field(name = "**Example:**", value = "> `connect4 @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def tictactoe(self, ctx):
        em = discord.Embed(title = "__**TicTacTie**__", description = "Challenge others in tictactoe!", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> tictactoe <player 2>")
        em.add_field(name = "**Example:**", value = "> `tictactoe @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def rps(self, ctx):
        em = discord.Embed(title = "__**RPS**__", description = "Challenge others in rock paper scissors!", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> rps [player 2]")
        em.add_field(name = "**Example:**", value = "> `rps @member`")
        em.add_field(name = "**Note:**", value = "> You can challenge the bot itself.")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

#================================================================================================================================

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ticket(self, ctx):
        em = discord.Embed(title = "__**Ticket**__", description = "Creates a ticket embed.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> ticket")
        em.add_field(name = "**Example:**", value = "> `ticket`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def close(self, ctx):
        em = discord.Embed(title = "__**Close**__", description = "Closes a ticket.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> close")
        em.add_field(name = "**Example:**", value = "> `close`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add(self, ctx):
        em = discord.Embed(title = "__**Add**__", description = "Adds a member to view a ticket.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> add <member>")
        em.add_field(name = "**Example:**", value = "> `add @member`")
        em.set_footer(text = "<> means requird, [] means optional")

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def remove(self, ctx):
        em = discord.Embed(title = "__**Remove**__", description = "Remove a member from viewing a ticket.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> remove <member>")
        em.add_field(name = "**Example:**", value = "> `remove @member`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)

    @help.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ticketrole(self, ctx):
        em = discord.Embed(title = "__**Ticket Role**__", description = "Adds a role to view tickets.", color = 0x000000)
        em.add_field(name = "**Syntax:**", value = "> ticketrole <role>")
        em.add_field(name = "**Example:**", value = "> `ticketrole @role`")
        em.set_footer(text = "<> means requird, [] means optional")
        await ctx.send(embed = em)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))

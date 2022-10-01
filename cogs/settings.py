import discord
from discord import app_commands
from discord.ext import commands
import json


#hide all confirm
class hideallConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def hideall_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"All Channels Hid!", description=f"> {interaction.user.mention} had hid all channels in the server.")
        await interaction.response.send_message(embed=emb)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#show all confirm
class showallConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def showall_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"All Channels Showed!", description=f"> {interaction.user.mention} had unhid all channels in the server.")
        await interaction.response.send_message(embed=emb)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#lock all confirm
class lockallConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def lockall_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"All Channels Locked! 🔒", description=f"{interaction.user.mention} had locked all channels in the server.")
        await interaction.response.send_message(embed=emb)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#unlock all confirm
class unlockallConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def unlockall_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"All Channels Unlocked! 🔓", description=f"{interaction.user.mention} had unlocked all channels in the server.")
        await interaction.response.send_message(embed=emb)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#welcome confirm button
class welcomeConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def welcome_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != welcome_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/welcome.json", "r") as f:
            channel = json.load(f)
        with open("jsons/welcome.json", "w") as f:
            channel[str(interaction.user.guild.id)] = welcome_channel
            json.dump(channel, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your welcome channel have been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#suggest confirm button
class suggestConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def suggest_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != suggest_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/suggest.json", "r", encoding="utf8") as f:
            channels = json.load(f)
        with open("jsons/suggest.json", "w", encoding="utf8") as f:
            channels[str(interaction.user.guild.id)] = {}
            channels[str(interaction.user.guild.id)]["suggch"] = sugg_ch_id
            channels[str(interaction.user.guild.id)]["revch"] = rev_ch_id
            json.dump(channels, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your suggestions channels have been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)


#filter toggle buttons
class filterToggle(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Enable",style=discord.ButtonStyle.green)
    async def filter_enable(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/filter.json", "r") as f:
            toggle = json.load(f)
        if toggle[str(interaction.user.guild.id)] == "enabled":
            await interaction.response.send_message("> Your filter is already enabled!", ephemeral = True)
        else:
            toggle[str(interaction.user.guild.id)] = "enabled"
            with open("jsons/filter.json", "w") as f:
                json.dump(toggle, f, indent=4)
            await interaction.response.send_message("> Swears Filter is now **Enabled!**")
            for child in self.children:
                child.disabled=True
            await interaction.message.edit(view=self)

    @discord.ui.button(label="Disable",style=discord.ButtonStyle.red)
    async def filter_disable(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/filter.json", "r") as f:
            toggle = json.load(f)
        if toggle[str(interaction.user.guild.id)] == "disabled":
            await interaction.response.send_message("> Your filter is already disabled!", ephemeral = True)
        else:
            toggle[str(interaction.user.guild.id)] = "disabled"
            with open("jsons/filter.json", "w") as f:
                json.dump(toggle, f, indent=4)
            await interaction.response.send_message("> Swears Filter is now **Disabled!**")
            for child in self.children:
                child.disabled=True
            await interaction.message.edit(view=self)


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #welcome command
    @commands.hybrid_command(name = "welcome", with_app_command = True, description = "Set a channel to announce joining and leaving of members.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel = "Channel to announce in it.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def welcome(self, ctx: commands.Context, channel: discord.TextChannel):
        global welcome_author
        global welcome_channel
        welcome_author = ctx.author
        welcome_channel = channel.id
        view = welcomeConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {channel.mention} to be your welcome channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help welcome` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)

    #suggest command
    @commands.hybrid_command(name = "suggest", with_app_command = True, description = "Set channels for suggestions.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(suggestions_channel = "Set a channel that members will sent their suggetions to.",
                           review_channel = "Set a private channel for admins to review the suggetions. (or make it the same suggestions channel if you want.)")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def suggest(self, ctx: commands.Context, suggestions_channel: discord.TextChannel, review_channel: discord.TextChannel):
        global suggest_author
        global sugg_ch_id
        global rev_ch_id
        suggest_author = ctx.author
        sugg_ch_id = suggestions_channel.id
        rev_ch_id = review_channel.id
        view = suggestConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {suggestions_channel.mention} to be your suggestion channel and {review_channel.mention} to be your suggestions' review channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help suggest` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #filter toggle
    @commands.hybrid_command(name = "filtertoggle", aliases=["filter"], with_app_command = True, description = "Enable/Disable swears filter.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def filtertoggle(self, ctx):
        global author
        author = ctx.author
        with open("jsons/filter.json", "r", encoding="utf8") as f:
            toggle = json.load(f)
        if toggle[str(ctx.guild.id)] == "disabled":
            des = "Your swears filter toggle is currently disabled.\nDo you wish to **enable** it?"
        elif toggle[str(ctx.guild.id)] == "enabled":
            des = "Your swears filter toggle is currently enabled.\nDo you wish to **disable** it?"
        view = filterToggle()
        em = discord.Embed(title="Swears Filter!", description=des, colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @filtertoggle.error
    async def filtertoggle_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Administrator**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #hide
    @commands.hybrid_command(name = "hide", with_app_command = True, description = "Hide a channel.")
    @app_commands.describe(channel = "Channel to hide (default is current channel).")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hidechat(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.read_messages == False:
            await ctx.reply("> The channel is already hidden!", mention_author=False, ephemeral = True)
            return
        overwrite.read_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"Channel Hid!",
                            description=f"> **{channel.mention}** has been hidden.",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

    @hidechat.error
    async def hidechat_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #hide all
    @commands.hybrid_command(name = "hideall", with_app_command = True, description = "Hide all channels in the server.")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hideall(self, ctx):
        hideall_em = discord.Embed(title="Confirm", description="Are you sure that you want to hide all your channels?")
        view = hideallConfirm()
        await ctx.send(embed=hideall_em, view=view, ephemeral=True)

    @hideall.error
    async def hideall_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #show
    @commands.hybrid_command(name = "show", aliases=["unhide"], with_app_command = True, description = "Show a hidden channel.")
    @app_commands.describe(channel = "Channel to unhide (default is current channel).")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def showchat(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.read_messages == True:
            await ctx.reply("> The channel is already shown!", mention_author=False, ephemeral = True)
            return
        overwrite.read_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"Channel Showed!",
                            description=f"> **{channel.mention}** has been shown.",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

    @showchat.error
    async def showchat_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #show all
    @commands.hybrid_command(name = "showall", with_app_command = True, description = "Unhide all channels in the server.")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def showall(self, ctx):
        hideall_em = discord.Embed(title="Confirm", description="Are you sure that you want to unhide all your channels?")
        view = showallConfirm()
        await ctx.send(embed=hideall_em, view=view, ephemeral=True)

    @showall.error
    async def showall_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #lock
    @commands.hybrid_command(name = "lock", with_app_command = True, description = "Lockes a room.")
    @app_commands.describe(channel = "Channel to lock (default is current channel).")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            return await ctx.reply("> The channel is already locked", mention_author=False, ephemeral = True)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"Channel Locked! 🔒",
                            description=f"> **{channel.mention}** has been locked.",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #lock all
    @commands.hybrid_command(name = "lockall", with_app_command = True, description = "Lockes all the channels.")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lockall(self, ctx: commands.Context):
        lockall_em = discord.Embed(title="Confirm", description="Are you sure that you want to lock all your channels?")
        view = lockallConfirm()
        await ctx.send(embed=lockall_em, view=view, ephemeral=True)

    @lockall.error
    async def lockall_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unlock
    @commands.hybrid_command(name = "unlock", with_app_command = True, description = "Unlocks a locked channel.")
    @app_commands.describe(channel = "Channel to unlock (default is current channel).")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
            return await ctx.reply("> The channel is already unlocked", mention_author=False, ephemeral = True)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        emb = discord.Embed(title=f"Channel Unlocked! 🔓",
                            description=f"> **{channel.mention}** has been unlocked.",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unlock all
    @commands.hybrid_command(name = "unlockall", with_app_command = True, description = "unlockes all the channels.")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlockall(self, ctx: commands.Context):
        unlockall_em = discord.Embed(title="Confirm", description="Are you sure that you want to unlock all your channels?")
        view = unlockallConfirm()
        await ctx.send(embed=unlockall_em, view=view, ephemeral=True)

    @unlockall.error
    async def unlockall_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Settings(bot))
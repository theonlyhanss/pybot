import discord
from discord import app_commands
from discord.ext import commands
import json
import asyncio


#edits confirm button
class editsConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def edits_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != edits_log_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/msg_edits.json", "r") as f:
            channel = json.load(f)
        with open("jsons/msg_edits.json", "w") as f:
            channel[str(interaction.user.guild.id)] = edits_log_channel
            json.dump(channel, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your edited message log channel has been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
    #cancel button
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def edits_cancel(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != edits_log_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("> Process Canceled.")


#deletes confirm button
class deletesConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def deletes_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != deletes_log_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/msg_deletes.json", "r") as f:
            channel = json.load(f)
        with open("jsons/msg_deletes.json", "w") as f:
            channel[str(interaction.user.guild.id)] = deletes_log_channel
            json.dump(channel, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your deleted messages log channel has been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
    #cancel button
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def deletes_cancel(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != deletes_log_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("> Process Canceled.")


#joins confirm button
class joinsConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def joins_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != joins_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/joins.json", "r") as f:
            channel = json.load(f)
        with open("jsons/joins.json", "w") as f:
            channel[str(interaction.user.guild.id)] = joins_channel
            json.dump(channel, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your members' joins log channel has been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
    #cancel button
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def welcome_cancel(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != joins_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("> Process Canceled.")


#leaves confirm button
class leavesConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def leaves_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != leaves_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        with open("jsons/leaves.json", "r") as f:
            channel = json.load(f)
        with open("jsons/leaves.json", "w") as f:
            channel[str(interaction.user.guild.id)] = leaves_channel
            json.dump(channel, f, sort_keys=True, indent=4, ensure_ascii=False)
        await interaction.response.send_message("> Your members' leaves log channel has been updated succesfully!")
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
    #cancel button
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def welcome_cancel(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user != leaves_author:
            return await interaction.response.send_message("> This is not for you!", ephemeral=True)
        for child in self.children:
            child.disabled=True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("> Process Canceled.")


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #log msg edit command
    @commands.hybrid_command(name = "edits", with_app_command = True, description = "Log edited messages and send them to a channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel = "Channel to send the log.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def edits(self, ctx: commands.Context, channel: discord.TextChannel):
        global edits_log_author
        global edits_log_channel
        edits_log_author = ctx.author
        edits_log_channel = channel.id
        view = editsConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {channel.mention} to be your edited messages log channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @edits.error
    async def edits_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help deletes` for more info",
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


    #log msg delete command
    @commands.hybrid_command(name = "deletes", with_app_command = True, description = "Log deleted messages and send them to a channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel = "Channel to send the log.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def deletes(self, ctx: commands.Context, channel: discord.TextChannel):
        global deletes_log_author
        global deletes_log_channel
        deletes_log_author = ctx.author
        deletes_log_channel = channel.id
        view = deletesConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {channel.mention} to be your deleted messages log channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @deletes.error
    async def deletes_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help deletes` for more info",
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


    #joins command
    @commands.hybrid_command(name = "joins", with_app_command = True, description = "Log members' joins and send them to a channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel = "Channel to send the log.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def joins(self, ctx: commands.Context, channel: discord.TextChannel):
        global joins_author
        global joins_channel
        joins_author = ctx.author
        joins_channel = channel.id
        view = joinsConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {channel.mention} to be your joins log channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @joins.error
    async def joins_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help joins` for more info",
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


    #leaves command
    @commands.hybrid_command(name = "leaves", with_app_command = True, description = "Log members' leaves and send them to a channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel = "Channel to send the log.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaves(self, ctx: commands.Context, channel: discord.TextChannel):
        global leaves_author
        global leaves_channel
        leaves_author = ctx.author
        leaves_channel = channel.id
        view = leavesConfirm()
        em = discord.Embed(title="Confirmation",
        description=f"Are you sure that you want {channel.mention} to be your leaves log channel?",
        colour=discord.Colour.dark_theme())
        await ctx.reply(embed=em, view = view)

    @leaves.error
    async def leaves_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help leaves` for more info",
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logs(bot))
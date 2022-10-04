import discord
from discord.ext import commands
from discord import app_commands, utils
import json


#get ticket role from  json
def get_ticketrole(client, message):
    with open("jsons/ticket_roles.json", "r", encoding="utf8") as f:
        user = json.load(f)
    return user[str(message.guild.id)]

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
        self.ticket_mod = get_ticketrole

    @discord.ui.button(label = "Create a Ticket", style = discord.ButtonStyle.blurple, custom_id = "ticket_button", emoji="📩")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("jsons/ticket_roles.json", "r", encoding="utf8") as f:
            user = json.load(f)
        tickrole = user[str(interaction.user.guild.id)]
        interaction.message.author = interaction.user
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry: return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds!", ephemeral = True)
        ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral = True)
        else:
            if type(self.ticket_mod) is not discord.Role: 
                self.ticket_mod = interaction.guild.get_role(tickrole)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True), 
                self.ticket_mod: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            }
            overwrites2 = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True), 
            }
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name='tickets')
            if category is None: #If there's no category matching with the `name`
                category = await guild.create_category('tickets') #Creates the category

            try:
                try:
                    channel = await interaction.guild.create_text_channel(name = f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, reason = f"Ticket for {interaction.user}", category=category)
                except:
                    channel = await interaction.guild.create_text_channel(name = f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites2, reason = f"Ticket for {interaction.user}", category=category)
            except:
                return await interaction.response.send_message("Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral = True)
            try:
                await channel.send(f"{self.ticket_mod.mention}, {interaction.user.mention} created a ticket!", view = main())
            except:
                await channel.send(f"{interaction.user.mention} created a ticket!", view = main())
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!", ephemeral = True)

class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction, button):
        try:
            await interaction.channel.delete()
        except:
            await interaction.response.send_message("Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral = True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = "close")
    async def close(self, interaction, button):
        embed = discord.Embed(title = "Are you sure you want to close this ticket?", color = discord.Colour.blurple())
        await interaction.response.send_message(embed = embed, view = confirm(), ephemeral = True)


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ticket_mod = get_ticketrole

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ticket is online.")


    #create ticket comamnd
    @commands.hybrid_command(name = 'ticket', with_app_command = True, description='Launches the ticketing system') #guild specific slash command
    @app_commands.default_permissions(manage_guild = True)
    @app_commands.checks.cooldown(3, 60, key = lambda i: (i.guild_id))
    @app_commands.checks.bot_has_permissions(manage_channels = True)
    async def ticketing(self, ctx):
        embed = discord.Embed(title = "Ticket!", description="If you need support, click the button below and create a ticket!", color = discord.Colour.blue())
        # embed.set_thumbnail(url = ctx.guild.icon.url)
        await ctx.channel.send(embed = embed, view = ticket_launcher())


    #close ticket
    @commands.hybrid_command(name = 'close', with_app_command = True, description='Closes the ticket') #guild specific slash command
    @app_commands.checks.bot_has_permissions(manage_channels = True)
    async def close(self, ctx):
        if "ticket-for-" in ctx.channel.name:
            embed = discord.Embed(title = "> Are you sure you want to close this ticket?", color = discord.Colour.blurple())
            await ctx.send(embed = embed, view = confirm(), ephemeral = True)
        else:
            await ctx.send("> This isn't a ticket!", ephemeral = True)


    #add a member to ticket
    @commands.hybrid_command(name = 'add', with_app_command = True, description='Adds a user to the ticket') #guild specific slash command
    @app_commands.describe(user = "The user you want to add to the ticket")
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.bot_has_permissions(manage_channels = True)
    async def add(self, ctx, user: discord.Member):
        if "ticket-for-" in ctx.channel.name:
            await ctx.channel.set_permissions(user, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
            await ctx.send(f"{user.mention} has been added to the ticket by {ctx.author.mention}!")
        else:
            await ctx.send("> This isn't a ticket!", ephemeral = True)


    #remove a member from ticket
    @commands.hybrid_command(name = 'remove', with_app_command = True, description='Removes a user from the ticket') #guild specific slash command
    @app_commands.describe(user = "The user you want to remove from the ticket")
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.bot_has_permissions(manage_channels = True)
    async def remove(self, ctx, user: discord.Member):
        with open("jsons/ticket_roles.json", "r", encoding="utf8") as f:
            user = json.load(f)
        tickrole = user[str(ctx.guild.id)]
        if "ticket-for-" in ctx.channel.name:
            if type(self.ticket_mod) is not discord.Role: self.ticket_mod = ctx.guild.get_role(tickrole)
            if self.ticket_mod not in ctx.author.roles:
                return await ctx.send("> You aren't authorized to do this!", ephemeral = True)
            if self.ticket_mod not in user.roles:
                await ctx.channel.set_permissions(user, overwrite = None)
                await ctx.send(f"> {user.mention} has been removed from the ticket by {ctx.author.mention}!", ephemeral = True)
            else:
                await ctx.send(f"> {user.mention} is a moderator!", ephemeral = True)
        else:
            await ctx.send("> This isn't a ticket!", ephemeral = True)


    #add role to ticket
    @commands.hybrid_command(name = 'ticketrole', with_app_command = True, description='Adds a role to view the tickets.') #guild specific slash command
    @app_commands.describe(ticket_role = "Provide role's exact name or ID or mention it.")
    @app_commands.default_permissions(manage_channels = True)
    @app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.bot_has_permissions(manage_channels = True)
    async def ticketrole(self, ctx, *, ticket_role: discord.Role):
        discord.utils.find(lambda r: r.name == f"{ticket_role}", ctx.message.guild.roles)
        trole = ticket_role.id
        with open("jsons/ticket_roles.json", "r", encoding="utf8") as f:
            user = json.load(f)
        with open("jsons/ticket_roles.json", "w", encoding="utf8") as f:
            user[str(ctx.guild.id)] = trole
            json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
        role_embed = discord.Embed(title="Ticket Role Updated!",
        description=f"The role **{ticket_role}** has been addded to tickets",
        colour=discord.Colour.blue())
        await ctx.send(embed=role_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))

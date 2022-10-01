import discord
from discord import app_commands
from discord.ext import commands


class Serverinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Serverinfo is online.")


    #roles list
    @commands.hybrid_command(name = "roles", with_app_command = True, description = "A list of roles.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roles(self, ctx):
        roles = ', '.join([str(r.name) for r in ctx.guild.roles])
        embed = discord.Embed(title=f"{ctx.guild.name}", color = 0x00000)
        embed.add_field(name="Roles", value=f"{roles}", inline = True)
        await ctx.send(embed=embed)

    @roles.error
    async def roles_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #server info command
    @commands.hybrid_command(name = "server", aliases=["s"],
                             with_app_command = True,
                             description = "Shows information about the server.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def server(self, ctx):
        embed = discord.Embed(color = 0x00000)
        embed.add_field(name = '🆔Server ID', value = f">>> {ctx.guild.id}", inline = True)
        embed.add_field(name = '📆Created On', value = f">>> {ctx.guild.created_at.strftime('%b %d %Y')}", inline = True)
        embed.add_field(name = '👑Owner', value = f">>> {ctx.guild.owner}", inline = True)
        embed.add_field(name = '👥Members', value = f'>>> {ctx.guild.member_count} Members | {sum(member.status!=discord.Status.offline and not member.bot for member in ctx.guild.members)} Online', inline = True)
        embed.add_field(name = '💬Channels', value = f'>>> {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline = True)
        #embed.add_field(name = '🌎Region', value = f'>>> {ctx.guild.region}', inline = True)
        embed.set_thumbnail(url = ctx.guild.icon.url)
        embed.set_footer(text = "Server Info")
        embed.set_author(name = f'{ctx.guild.name}', icon_url = ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #owner info
    @commands.hybrid_command(name = "owner", with_app_command = True, description = "Shows server's owner.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def owner(self, ctx):
        owner = str(ctx.guild.owner)
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        embed = discord.Embed(
            title=name,
            color=discord.Color.dark_theme())
        embed.set_thumbnail(url=icon)
        embed.add_field(name="__👑Owner__", value=f"**{owner}**", inline=True)
        await ctx.send(embed=embed)

    @owner.error
    async def owner_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #id info
    @commands.hybrid_command(name = "id", with_app_command = True, description = "Shows server's id.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def id(self, ctx):
        id = str(ctx.guild.id)
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        embed = discord.Embed(
            title=name,
            color=discord.Color.dark_theme())
        embed.set_thumbnail(url=icon)
        embed.add_field(name="__🆔Server ID__", value=f"**{id}**", inline=True)
        await ctx.send(embed=embed)

    @id.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    # #region info
    # @commands.command()
    # async def region(self, ctx):
    #     region = str(ctx.guild.region)
    #     name = str(ctx.guild.name)
    #     icon = str(ctx.guild.icon.url)
    #     embed = discord.Embed(
    #         title=name,
    #         color=discord.Color.dark_theme())
    #     embed.set_thumbnail(url=icon)
    #     embed.add_field(name="__Region__", value=region, inline=True)
    #     await ctx.send(embed=embed)


    #member count info
    @commands.hybrid_command(name = "members", with_app_command = True, description = "Shows member's count.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def members(self, ctx):
        memberCount = str(ctx.guild.member_count)
        onlineCount = sum(member.status!=discord.Status.offline and not member.bot for member in ctx.guild.members)
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        embed = discord.Embed(
            title=name,
            color=discord.Color.dark_theme())
        embed.set_thumbnail(url=icon)
        embed.add_field(name="__👥Members__", value=f">>> {memberCount} Members | {onlineCount} Online", inline=True)
        await ctx.send(embed=embed)

    @members.error
    async def members_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #channels count info
    @commands.hybrid_command(name = "channels", with_app_command = True, description = "Shows channel's count.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def channels(self, ctx):
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        embed = discord.Embed(
            title=name,
            color=discord.Color.dark_theme())
        embed.set_thumbnail(url=icon)
        embed.add_field(name="__💬Channels__", value=f">>> {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice", inline=True)
        await ctx.send(embed=embed)

    @channels.error
    async def channels_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #server icon
    @commands.hybrid_command(name = "icon", with_app_command = True, description = "Shows server's icon.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def icon(self, ctx):
        icon = str(ctx.guild.icon.url)
        e = discord.Embed(title="Icon Link", url=f"{icon}",color=discord.Color.dark_theme())
        e.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.message.author.avatar.url}")
        e.set_image(url=f"{icon}")
        e.set_footer(text=f"requested by {ctx.message.author}", icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=e)

    @icon.error
    async def icon_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #userinfo command
    @commands.hybrid_command(name = "user", aliases=["userinfo" , "info" , "u"],
                             with_app_command = True,
                             description = "Shows server's owner.")
    @app_commands.describe(member = "Member to show their info.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def user(self, ctx, *, member: discord.Member = None): # b'\xfc'
        if member is None:
            member = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=discord.Color.dark_theme(), description=member.mention)
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="__Joined__", value=f">>> {member.joined_at.strftime(date_format)}")
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="__Join position__", value=f">>> {str(members.index(member)+1)}")
        embed.add_field(name="__Registered__", value=f">>> {member.created_at.strftime(date_format)}")
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name="__Roles [{}]__".format(len(member.roles)-1), value=f">>> {role_string}", inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.add_field(name="__Guild permissions__", value=f">>> {perm_string}", inline=False)
        embed.set_footer(text='ID: ' + str(member.id))
        return await ctx.send(embed=embed)

    @user.error
    async def user_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Serverinfo(bot))
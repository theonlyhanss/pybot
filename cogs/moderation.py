import discord
from discord import app_commands
from discord.ext import commands
import json
import asyncio
from datetime import timedelta
from discord.ext.commands import guild_only


#unban all confirm
class unbanallConfirm(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def unbanall_confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        for ban_entry in bans:
            await interaction.guild.unban(user=ban_entry.user)
        unbanall_embed = discord.Embed(title="Unban All!",
                                  description=f"{author.mention}" + ' has unbanned all users! (total {})'.format(len(bans)),
                                  colour=discord.Colour.green())
        await interaction.response.send_message(embed=unbanall_embed)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is online.")


    #clear command
    @commands.hybrid_command(name = "clear", with_app_command = True, description = "Clears messages.")
    @app_commands.describe(amount = "Number of messages to clear (default amount is 1).")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clear(self, ctx, amount=1):
        msg = await ctx.send(f">>> Deleting **{amount}** message(s)...")
        await asyncio.sleep(2)
        await msg.delete()
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Messages**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #warn commands
    @commands.hybrid_command(name = "warn", with_app_command = True, description = "Warn a member.")
    @app_commands.describe(member = "Member to warn.", reason = "Reason of warn.")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def warn(self, ctx, member : commands.MemberConverter, *, reason = None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not warn **{member.name}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not warn **{member.name}**!", mention_author=False, ephemeral = True)
        if reason==None:
            reason="no reason given"
        #add warning to json
        with open("jsons/warns.json", "r", encoding="utf8") as f:
            user = json.load(f)
        try:
            with open("jsons/warns.json", "w", encoding="utf8") as f:
                user[str(member.id)] = user[str(member.id)] + 1
                json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
        except:
            with open("jsons/warns.json", "w", encoding="utf8") as f:
                # user = {}
                # user[str(member.id)] = {}
                user[str(member.id)] = 1
                json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
        warn_embed = discord.Embed(title="Warn!",
        description=f"{member.mention} has been warned by {ctx.author.mention} for {reason}",
        colour=discord.Colour.red())
        await ctx.send(embed=warn_embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Moderate Member**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help warn` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Warn
    @commands.hybrid_command(name = "multiwarn", with_app_command = True, description = "Warns multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to warn.", member2 = "Second Member to warn.", member3 = "Third Member to warn.", member4 = "Fourth Member to warn.", member5 = "Fifth Member to warn.", reason = "Reason of warn.")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multiwarn(self, ctx, member1: discord.Member, member2: discord.Member, member3: discord.Member = None, member4: discord.Member = None, member5: discord.Member = None, *, reason = None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not warn **{member.name}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not warn **{member.name}**!", mention_author=False, ephemeral = True)
        if reason==None:
            reason="no reason given"
        #add warning to json
        with open("jsons/warns.json", "r", encoding="utf8") as f:
            user = json.load(f)
        for member in members:
            try:
                with open("jsons/warns.json", "w", encoding="utf8") as f:
                    user[str(member.id)] = user[str(member.id)] + 1
                    json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
            except:
                with open("jsons/warns.json", "w", encoding="utf8") as f:
                    # user = {}
                    # user[str(member.id)] = {}
                    user[str(member.id)] = 1
                    json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
        warn_embed = discord.Embed(title="Multi-Warn!",
        description=f"{memberstext} has been warned by {ctx.author.mention} for {reason}",
        colour=discord.Colour.red())
        await ctx.send(embed=warn_embed)

    @multiwarn.error
    async def multiwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Moderate Member**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help warn` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unwarn commands
    @commands.hybrid_command(name = "unwarn", aliases=["warnremove"], with_app_command = True, description = "Unwarn a member.")
    @app_commands.describe(member = "Member to unwarn.", amount = "Number of warnings to remove (default is 1 warn).")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unwarn(self, ctx, member : commands.MemberConverter, amount=None):
        #check if member = author
        if ctx.author == member:
            return await ctx.send("> You can not unwarn yourself!", ephemeral = True)
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not unwarn **{member.name}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not unwarn **{member.name}**!", mention_author=False, ephemeral = True)
        if amount == None:
            amount = 1
        #add warning to json
        with open("jsons/warns.json", "r", encoding="utf8") as f:
            user = json.load(f)
            #check if warns = 0
            if user[str(member.id)] == 0:
                return await ctx.reply("> This user doesn't have any warnings.", ephemeral = True)
            #check if warns - amount < 0
            warns = user[str(member.id)]
            if int(warns)-int(amount) < 0:
                return await ctx.reply(f"> This user only has **{warns}** warnings.", ephemeral = True)
        try:
            with open("jsons/warns.json", "w", encoding="utf8") as f:
                user[str(member.id)] = user[str(member.id)] - int(amount)
                json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
                warn_embed = discord.Embed(title="Unwarn!",
                description=f"**{amount}** warnings has been removed from {member.mention} by {ctx.author.mention}",
                colour=discord.Colour.green())
                await ctx.send(embed=warn_embed)
        except:
            await ctx.reply("> This user doesn't have any warnings.", ephemeral = True)

    @unwarn.error
    async def unwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Moderate Member**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help warn` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #warnings list commands
    @commands.hybrid_command(name = "warnings", with_app_command = True, description = "Get list of warnings for the user.")
    @app_commands.describe(member = "Member to view their warnings.")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def warnings(self, ctx, member : commands.MemberConverter):
        try:
            with open("jsons/warns.json", "r", encoding="utf8") as f:
                user = json.load(f)
            warns = user[str(member.id)]
            await ctx.reply(f"> {member.mention} user has **{warns}** warnings.")
        except:
            await ctx.reply("> This user doesn't have any warnings.", ephemeral = True)

    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help warnings` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #timeout command
    @commands.hybrid_command(name = "timeout", with_app_command = True, description = "Timeouts members. (maximum 5 members.)")
    @app_commands.describe(member = "Member to timeout.", time = "Time of the timeout.", reason = "Reason to timeout.")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def timeout(self, ctx, member : commands.MemberConverter, time, *, reason = None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not timeout **{member.name}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not timeout **{member.name}**!", mention_author=False, ephemeral = True)
        if reason==None:
            reason="no reason given"
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
        #timing out
        await member.timeout(timedelta(seconds=sleep))
        timeout_embed = discord.Embed(title="Timeout!",
        description=f"{member.mention} has been timed out by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.send(embed=timeout_embed)
        #timeout over message
        await asyncio.sleep(int(sleep))
        timeout_embed = discord.Embed(title="Timeout over!",
        description=f"{member.mention} Timeout for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=timeout_embed)

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Moderate Member**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help timeout` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Timeout
    @commands.hybrid_command(name = "multitimeout", with_app_command = True, description = "Timeouts multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to timeout.", member2 = "Second Member to timeout.", member3 = "Third Member to timeout.", member4 = "Fourth Member to timeout.", member5 = "Fifth Member to timeout.", time = "Time of the timeout.", reason = "Reason to timeout.")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multitimeout(self, ctx, time, member1: commands.MemberConverter, member2: commands.MemberConverter, member3: commands.MemberConverter = None, member4: commands.MemberConverter = None, member5: commands.MemberConverter = None, *, reason = None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not timeout **{member.name}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not timeout **{member.name}**!", mention_author=False, ephemeral = True)
        if reason==None:
            reason="no reason given"
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
        #timing out
        for member in members:
            await member.timeout(timedelta(seconds=sleep))
        timeout_embed = discord.Embed(title="Multi-Time out!",
        description=f"{memberstext} has been timed out by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.send(embed=timeout_embed)
        #timeout over message
        await asyncio.sleep(int(sleep))
        timeout_embed = discord.Embed(title="Multi-Timeout over!",
        description=f"{memberstext} Timeout for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=timeout_embed)

    @multitimeout.error
    async def multitimeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Moderate Member**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help multitimeout` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #kick command
    @commands.hybrid_command(name = "kick", with_app_command = True, description = "Kicks a member.")
    @app_commands.describe(member = "Member to kick.", reason = "Reason to kick.")
    @commands.has_permissions(kick_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason=None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not kick **{member.mention}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not kick **{member.mention}**!", mention_author=False, ephemeral = True)
        if reason == None:
          reason = "no mentioned reason"
        await member.kick(reason = reason)
        kick_embed = discord.Embed(title="Kick!",
                                   description=f"**{member.mention}** has been kicked by {ctx.author.mention} for {reason}",
                                   colour=discord.Colour.red())
        await ctx.send(embed=kick_embed)
        server = str(ctx.guild.name)
        await member.send(f">>> You have been kicked from **{server}** for {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Kick Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help kick` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Kick
    @commands.hybrid_command(name = "multikick", with_app_command = True, description = "Kicks multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to kick.", member2 = "Second Member to kick.", member3 = "Third Member to kick.", member4 = "Fourth Member to kick.", member5 = "Fifth Member to kick.", reason = "Reason to kick.")
    @commands.has_permissions(kick_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multikick(self, ctx, member1: commands.MemberConverter, member2: commands.MemberConverter, member3: commands.MemberConverter = None, member4: commands.MemberConverter = None, member5: commands.MemberConverter = None, *, reason=None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not kick **{member.mention}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not kick **{member.mention}**!", mention_author=False, ephemeral = True)
        if reason == None:
            reason = "no mentioned reason"
        for member in members:
            await member.kick(reason = reason)
            server = str(ctx.guild.name)
            await member.send(f">>> You have been kicked from **{server}** for {reason}")
        kick_embed = discord.Embed(title="Multi-Kick!",
                                   description=f"**{memberstext}** has been kicked by {ctx.author.mention} for {reason}",
                                   colour=discord.Colour.red())
        await ctx.send(embed=kick_embed)

    @multikick.error
    async def multikick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Kick Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help multikick` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #ban command
    @commands.hybrid_command(name = "ban", with_app_command = True, description = "Bans a member.")
    @app_commands.describe(member = "Member to ban.", reason = "Reason to ban.")
    @commands.has_permissions(ban_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not ban **{member.mention}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not ban **{member.mention}**!", mention_author=False, ephemeral = True)
        if reason == None:
          reason = "no mentioned reason"
        await member.ban(reason = reason)
        ban_embed = discord.Embed(title="Ban!",
                                  description=f"{member.mention} has been banned by {ctx.author.mention} for {reason}",
                                  colour=discord.Colour.red())
        await ctx.send(embed=ban_embed)
        server = str(ctx.guild.name)
        await member.send(f">>> You have been banned from **{server}** for {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Ban Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help ban` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Ban
    @commands.hybrid_command(name = "multiban", with_app_command = True, description = "Bans multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to ban.", member2 = "Second Member to ban.", member3 = "Third Member to ban.", member4 = "Fourth Member to ban.", member5 = "Fifth Member to ban.", reason = "Reason to ban.")
    @commands.has_permissions(ban_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multiban(self, ctx, member1: commands.MemberConverter, member2: commands.MemberConverter, member3: commands.MemberConverter = None, member4: commands.MemberConverter = None, member5: commands.MemberConverter = None, *, reason=None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not ban **{member.mention}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not ban **{member.mention}**!", mention_author=False, ephemeral = True)
        if reason == None:
          reason = "no mentioned reason"
        for member in members:
            await member.ban(reason = reason)
            server = str(ctx.guild.name)
            await member.send(f">>> You have been banned from **{server}** for {reason}")
        ban_embed = discord.Embed(title="Multi-Ban!",
                                  description=f"{memberstext} has been banned by {ctx.author.mention} for {reason}",
                                  colour=discord.Colour.red())
        await ctx.send(embed=ban_embed)

    @multiban.error
    async def multiban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Ban Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help multiban` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unban all command
    @commands.hybrid_command(name = "unbanall", with_app_command = True, description = "Unban all banned users.")
    @commands.has_permissions(ban_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @guild_only()  # Might not need ()
    async def unbanall(self, ctx):
        global author
        global bans
        author = ctx.author
        bans = [ban_entry async for ban_entry in ctx.guild.bans()]   # list of discord.BanEntry
        for ban_entry in bans:
            await ctx.guild.unban(user=ban_entry.user)
        unbanall_embed = discord.Embed(title="Confirm", description="Are you sure that you want to unban all banned users?")
        view = unbanallConfirm()
        await ctx.send(embed=unbanall_embed, view=view, ephemeral=True)

    @unbanall.error
    async def unbanall_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Ban Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unban command
    @commands.hybrid_command(name = "unban", with_app_command = True, description = "Unban banned member.")
    @app_commands.describe(id = "ID of the banned member.")
    @commands.has_permissions(ban_members= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @guild_only()  # Might not need ()
    async def unban(self, ctx, id):
        try:
            user = await self.bot.fetch_user(id)
            try:
                await ctx.guild.unban(user)
            except:
                return await ctx.send(f"> {user} is not banned!", ephemeral = True)
        except:
            return await ctx.send("> Enter a valid id.", ephemeral = True)
        unban_embed = discord.Embed(title="Unban!",
                                  description=f"{user} has been unbanned by {ctx.author.mention}",
                                  colour=discord.Colour.green())
        await ctx.send(embed=unban_embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Ban Members**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help unban` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #private channel
    @commands.hybrid_command(name = "prvchannel", aliases=["tempchannel"], with_app_command = True, description = "Makes a temprory private channel.")
    @app_commands.describe(time = "Time of the channel before it gets deleted.", channel_name = "Channel's name.")
    @commands.has_permissions(manage_channels= True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def prvchannel(self, ctx, time, *, channel_name):
        guild = ctx.guild
        category = discord.utils.get(ctx.guild.categories)
        overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True)
                    }
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

        channel = await guild.create_text_channel(name = channel_name , overwrites = overwrites , category = category)
        emb = discord.Embed(title="Channel Created! ✅",
                            description=f"> Private Channel **{channel_name}** has been created for **{timer}**",
                            colour=discord.Colour.dark_theme())
        await ctx.send(embed=emb)

        await asyncio.sleep(int(sleep))
        await channel.delete()
        emb = discord.Embed(title="Channel Deleted!",
                            description=f"> Private Channel **{channel_name}** has been deleted after **{timer}**",
                            colour=discord.Colour.dark_theme())
        await ctx.reply(embed=emb)

    @prvchannel.error
    async def prvchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Channels**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help prvchannel` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #TIMED MUTE!!!!!
    @commands.hybrid_command(name = "mute", with_app_command = True, description = "Mutes a member.")
    @app_commands.describe(member = "Member to mute.", time = "Time of the mute.", reason = "Reason to mute.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mute(self, ctx, member: commands.MemberConverter, time = None , *, reason = None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not mute **{member.name}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not mute **{member.name}**!", mention_author=False, ephemeral = True)
        #check if member is muted
        role = discord.utils.find(lambda r: r.name == 'SB-Muted', ctx.message.guild.roles)
        if role in member.roles:
            return await ctx.send(f"> **{member.mention}** is already muted!", ephemeral = True)
        #check reason
        if reason==None:
            reason="no reason given"
        #time stuff
        if time==None:
            time="no time given"
            timer = time
        else:
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
        #get role
        guild = ctx.guild
        mutedRole = discord.utils.get(ctx.guild.roles, name="SB-Muted")
        #To make the role if it is not in the server
        if not mutedRole:
            mutedRole = await guild.create_role(name="SB-Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole , send_messages=False)
        #Mute starts message
        await member.add_roles(mutedRole)
        mute_embed = discord.Embed(title="Mute!",
        description=f"{member.mention} has been muted by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.send(embed=mute_embed)
        #Mute over message
        await asyncio.sleep(int(sleep))
        await member.remove_roles(mutedRole)
        unmute_embed = discord.Embed(title="Mute over!",
        description=f"{member.mention} Mute for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=unmute_embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help mute` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Mute
    @commands.hybrid_command(name = "multimute", with_app_command = True, description = "Mutes multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to mute.", member2 = "Second Member to mute.", member3 = "Third Member to mute.", member4 = "Fourth Member to mute.", member5 = "Fifth Member to mute.", time = "Time of the mute.", reason = "Reason to mute.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multimute(self, ctx, member1: commands.MemberConverter, member2: commands.MemberConverter, member3: commands.MemberConverter = None, member4: commands.MemberConverter = None, member5: commands.MemberConverter = None, time = None , *, reason = None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not mute **{member.name}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not mute **{member.name}**!", mention_author=False, ephemeral = True)
            #check if member is muted
            role = discord.utils.find(lambda r: r.name == 'SB-Muted', ctx.message.guild.roles)
            if role in member.roles:
                return await ctx.send(f"> **{member.mention}** is already muted!", ephemeral = True)
        #check reason
        if reason==None:
            reason="no reason given"
        #time stuff
        if time==None:
            time="no time given"
            timer = time
        else:
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
        #get role
        guild = ctx.guild
        mutedRole = discord.utils.get(ctx.guild.roles, name="SB-Muted")
        #To make the role if it is not in the server
        if not mutedRole:
            mutedRole = await guild.create_role(name="SB-Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole , send_messages=False)
        for member in members:
            #Mute starts message
            await member.add_roles(mutedRole)
        mute_embed = discord.Embed(title="Multi-Mute!",
        description=f"{memberstext} has been muted by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.send(embed=mute_embed)
        #Mute over message
        await asyncio.sleep(int(sleep))
        for member in members:
            await member.remove_roles(mutedRole)
        unmute_embed = discord.Embed(title="Multi-Mute over!",
        description=f"{memberstext} Mute for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=unmute_embed)

    @multimute.error
    async def multimute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help multimute` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #unmute command
    @commands.hybrid_command(name = "unmute", with_app_command = True, description = "Unmutes a member.")
    @app_commands.describe(member = "Member to unmute.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unmute(self,ctx, member: commands.MemberConverter):
        #check if member is muted
        role = discord.utils.find(lambda r: r.name == 'SB-Muted', ctx.message.guild.roles)
        if role in member.roles:
            pass
        else:
            return await ctx.send(f"> **{member.name}** is not muted!", ephemeral = True)
        #check if unmuting self
        if ctx.author == member:
            return await ctx.reply("> You can not unmute yourself!", mention_author=False, ephemeral = True)
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f">>> You can not unmute **{member.name}**!", mention_author=False)

        mutedRole = discord.utils.get(member.roles, name="SB-Muted")
        await member.send(f">>> you have been unmuted from **{ctx.guild.name}**")
        embed = discord.Embed(title="Unmute!",
        description=f"{member.mention} has been unmuted",
        colour=discord.Colour.green())
        await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help unmute` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #JAIL COMMAND!!!!!
    @commands.hybrid_command(name = "jail", with_app_command = True, description = "Jails a member.")
    @app_commands.describe(member = "Member to jail.", time = "Time of the jail.", reason = "Reason to jail.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def jail(self, ctx, member: commands.MemberConverter, time=None, *, reason=None):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.reply(f"> You can not jail **{member.name}**!", mention_author=False, ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not jail **{member.name}**!", mention_author=False, ephemeral = True)
        #check if member is muted
        role = discord.utils.find(lambda r: r.name == 'SB-Jailed', ctx.message.guild.roles)
        if role in member.roles:
            return await ctx.send(f"> **{member.mention}** is already muted!", ephemeral = True)
        #check reason
        if reason==None:
            reason="no reason given"
        #time stuff
        if time==None:
            time="no time given"
            timer = time
        else:
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
        #get role
        guild = ctx.guild
        jailedRole = discord.utils.get(guild.roles, name="SB-Jailed")
        #To make the role if it is not in the server
        if not jailedRole:
            jailedRole = await guild.create_role(name="SB-Jailed")
            for channel in guild.channels:
                await channel.set_permissions(jailedRole, speak=False, send_messages=False,
                                            read_message_history=True, read_messages=False)
        #create jail channel
        overwrites = {
                    jailedRole: discord.PermissionOverwrite(read_messages=True),
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                } 
        channel = await guild.create_text_channel(name=f"jail-{member.id}", overwrites = overwrites)
        await channel.edit(slowmode_delay=10)
        #Jail starts message
        await member.add_roles(jailedRole)
        mute_embed = discord.Embed(title="Jail!",
        description=f"{member.mention} has been jailed by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.reply(embed=mute_embed)
        await channel.send(f"{member.mention} You have been jailed for {reason} to {timer}.")

        #Jail over message
        await asyncio.sleep(int(sleep))
        await member.remove_roles(jailedRole)
        await channel.delete()
        unmute_embed = discord.Embed(title="Jail over!",
        description=f"{member.mention} jail for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=unmute_embed)

    @jail.error
    async def jail_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help jail` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #Multi-Jail
    @commands.hybrid_command(name = "multijail", with_app_command = True, description = "Jails multiple members. (maximum 5 members.)")
    @app_commands.describe(member1 = "First Member to jail.", member2 = "Second Member to jail.", member3 = "Third Member to jail.", member4 = "Fourth Member to jail.", member5 = "Fifth Member to jail.", time = "Time of the jail.", reason = "Reason to jail.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def multijail(self, ctx, member1: commands.MemberConverter, member2: commands.MemberConverter, member3: commands.MemberConverter = None, member4: commands.MemberConverter = None, member5: commands.MemberConverter = None, time=None, *, reason=None):
        if member3 == None:
            members = [member1,member2]
            memberstext = f"{member1.mention} and {member2.mention}"
        elif member4 == None:
            members = [member1,member2,member3]
            memberstext = f"{member1.mention}, {member2.mention} and {member3.mention}"
        elif member5 == None:
            members = [member1,member2,member3,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention} and {member4.mention}"
        else:
            members = [member1,member2,member3,member4,member4]
            memberstext = f"{member1.mention}, {member2.mention}, {member3.mention}, {member4.mention} and {member5.mention}"
        for member in members:
            #check author role
            if ctx.author.top_role <= member.top_role:
                return await ctx.reply(f"> You can not jail **{member.name}**!", mention_author=False, ephemeral = True)
            #check bot role
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.reply(f"> I can not jail **{member.name}**!", mention_author=False, ephemeral = True)
            #check if member is jailed
            role = discord.utils.find(lambda r: r.name == 'SB-Jailed', ctx.message.guild.roles)
            if role in member.roles:
                return await ctx.send(f"> **{member.mention}** is already muted!", ephemeral = True)
        #check reason
        if reason==None:
            reason="no reason given"
        #time stuff
        if time==None:
            time="no time given"
            timer = time
        else:
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
        #get role
        guild = ctx.guild
        jailedRole = discord.utils.get(guild.roles, name="SB-Jailed")
        #To make the role if it is not in the server
        if not jailedRole:
            jailedRole = await guild.create_role(name="SB-Jailed")
            for channel in guild.channels:
                await channel.set_permissions(jailedRole, speak=False, send_messages=False,
                                            read_message_history=True, read_messages=False)
        for member in members:
            #create jail channel
            overwrites = {
                        jailedRole: discord.PermissionOverwrite(read_messages=True),
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True)
                    } 
            channel = await guild.create_text_channel(name=f"jail-{member.id}", overwrites = overwrites)
            await channel.edit(slowmode_delay=10)
            #Jail starts message
            await member.add_roles(jailedRole)
            await channel.send(f"{member.mention} You have been jailed for {reason} to {timer}.")
        mute_embed = discord.Embed(title="Multi-Jail!",
        description=f"{memberstext} has been jailed by {ctx.author.mention} for {reason} to {timer}",
        colour=discord.Colour.red())
        await ctx.reply(embed=mute_embed)

        #Jail over message
        await asyncio.sleep(int(sleep))
        for member in members:
            await member.remove_roles(jailedRole)
            await channel.delete()
        unmute_embed = discord.Embed(title="Multi-Jail over!",
        description=f"{memberstext} jail for {reason} is over after {timer}",
        colour=discord.Colour.green())
        await ctx.reply(embed=unmute_embed)

    @multijail.error
    async def multijail_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help multijail` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #UNJAIL command
    @commands.hybrid_command(name = "unjail", with_app_command = True, description = "Unjails a member.")
    @app_commands.describe(member = "Member to unjail.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unjail(self,ctx, member: commands.MemberConverter): 
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=f"jail-{member.id}")
        jailedRole = discord.utils.get(member.roles, name="SB-Jailed")
        #check if member is muted
        role = discord.utils.find(lambda r: r.name == 'SB-Jailed', ctx.message.guild.roles)
        if role in member.roles:
            pass
        else:
            return await ctx.send(f"> **{member.name}** is not jailed!", ephemeral = True)
        if ctx.author == member:
            await ctx.reply("> You can not unjail yourself!", mention_author=False, ephemeral = True)
            return
        if ctx.author.top_role <= member.top_role:
            await ctx.reply(f">>> You can not unjail **{member.name}**!", mention_author=False, ephemeral = True)
            return 

        await member.remove_roles(jailedRole)
        await channel.delete()
        await member.send(f"> you have been unjailed from **{ctx.guild.name}**")
        embed = discord.Embed(title="Unjail!",
        description=f"{member.mention} has been unjailed",
        colour=discord.Colour.green())
        await ctx.send(embed=embed)

    @unjail.error
    async def unjail_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help unjail` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)

    #change prefix
    @commands.hybrid_command(name = "prefix", aliases=["changeprefix"], with_app_command = True, description = "Changes the prefix for a server.")
    @app_commands.describe(prefix = "The new prefix.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def prefix(self, ctx, prefix):
        with open("jsons/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("jsons/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        prefix_embed = discord.Embed(title="Prefix Changed!",
        description=f"Prefix has been changed to {prefix}",
        colour=discord.Colour.blue())
        await ctx.send(embed=prefix_embed)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Administrator**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help prefix` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #role command
    @commands.hybrid_command(name = "role", aliases=["addrole"], with_app_command = True, description = "Adds a role to a member.")
    @app_commands.describe(member = "Memebr to give the role.", role = "The role to give.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def role(self, ctx, member: commands.MemberConverter, *, role: discord.Role):
        #check author role
        if ctx.author.top_role <= member.top_role:
            await ctx.reply(f"> You can not add a role to **{member.name}**!", mention_author=False, ephemeral = True)
            return
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not add a role to **{member.name}**!", mention_author=False, ephemeral = True)
        #check if member has the role
        check_role = discord.utils.find(lambda r: r.name == f"{role}", ctx.message.guild.roles)
        if check_role in member.roles:
            return await ctx.send(f"> **{member.name}** already has that role!", ephemeral = True)
        #add the role
        await member.add_roles(role)
        addrole_embed = discord.Embed(title="__Role added!__",
                                      description=f"{member.mention} has been given the role **{role}**",
                                      colour=discord.Colour.green())
        await ctx.send(embed=addrole_embed)

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help role` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


    #remove role command
    @commands.hybrid_command(name = "delrole", aliases=["removerole"], with_app_command = True, description = "Removes a role from a member.")
    @app_commands.describe(member = "Memebr to remove the role from.", role = "The role to remove.")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delrole(self, ctx, member: commands.MemberConverter, *, role: discord.Role):
        #check author role
        if ctx.author.top_role <= member.top_role:
            await ctx.reply(f"> You can not remove a role to **{member.name}**!", mention_author=False, ephemeral = True)
            return
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.reply(f"> I can not remove a role to **{member.name}**!", mention_author=False, ephemeral = True)
        #check if member has the role
        check_role = discord.utils.find(lambda r: r.name == f"{role}", ctx.message.guild.roles)
        if check_role in member.roles:
            pass
        else:
            return await ctx.send(f"> **{member.name}** doesn't have that role!", ephemeral = True)
        #add the role
        await member.remove_roles(role)
        addrole_embed = discord.Embed(title="__Role removed!__",
                                      description=f"{member.mention} no longer has the role **{role}**",
                                      colour=discord.Colour.red())
        await ctx.send(embed=addrole_embed)

    @delrole.error
    async def delrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            per_error = discord.Embed(title="Missing Permissions!",
            description=f"> You must have __**Manage Roles**__ permission!",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=per_error, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            arg_error = discord.Embed(title="Missing Argument!",
            description=f"> Please check `_help delrole` for more info",
            colour=discord.Colour.light_grey())
            await ctx.reply(embed=arg_error, ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            cool_error = discord.Embed(title=f"Slow it down bro!",
            description=f"> Try again in {error.retry_after:.2f}s.",colour=discord.Colour.light_grey())
            await ctx.reply(embed=cool_error, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))

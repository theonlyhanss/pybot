#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>
# MIT Licensed
# Using code from SourSpoon under the MIT License
# https://github.com/SourSpoon/Discord.py-Template

import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from cogs.utils.game import Connect4Game


class Connect4(commands.Cog):
	CANCEL_GAME_EMOJI = '🚫'
	DIGITS = [str(digit) + '\N{combining enclosing keycap}' for digit in range(1, 8)] + ['🚫']
	VALID_REACTIONS = [CANCEL_GAME_EMOJI] + DIGITS
	GAME_TIMEOUT_THRESHOLD = 600

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

  #CONNECT4
	@commands.hybrid_command(name = "connect4", with_app_command = True, description = "play connect 4.")
	@app_commands.describe(player2 = "Player to challenge.")
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def connect4(self, ctx, *, player2: discord.Member):
		"""
		Play connect4 with another player
		"""
		player1 = ctx.message.author

		game = Connect4Game(
			player1.mention,
			player2.mention
		)

		message = await ctx.send(str(game))

		for digit in self.DIGITS:
			await message.add_reaction(digit)

		def check(reaction, user):
			return (
				user == (player1, player2)[game.whomst_turn()-1]
				and str(reaction) in self.VALID_REACTIONS
				and reaction.message.id == message.id
			)

		while game.whomst_won() == game.NO_WINNER:
			try:
				reaction, user = await self.bot.wait_for(
					'reaction_add',
					check=check,
					timeout=self.GAME_TIMEOUT_THRESHOLD
				)
			except asyncio.TimeoutError:
				game.forfeit()
				await message.reply("> Game was ended due to running out of time!")
				break

			await asyncio.sleep(0.2)
			try:
				await message.remove_reaction(reaction, user)
			except discord.errors.Forbidden:
				pass

			if str(reaction) == self.CANCEL_GAME_EMOJI:
				game.forfeit()
				break

			try:
				# convert the reaction to a 0-indexed int and move in that column
				game.move(self.DIGITS.index(str(reaction)))
			except ValueError:
				pass # the column may be full

			await message.edit(content=str(game))

		await self.end_game(game, message)

	@classmethod
	async def end_game(cls, game, message):
		await message.edit(content=str(game))
		await cls.clear_reactions(message)

	@staticmethod
	async def clear_reactions(message):
		try:
			await message.clear_reactions()
		except discord.HTTPException:
			pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Connect4(bot))
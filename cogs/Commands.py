from time import time
import time
import discord
import random
from discord.ext import commands
from discord.utils import get
import json
import asyncio
from discord import Embed
import datetime
from datetime import datetime, timedelta
from random import choice

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from collections import Counter


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return(int(amount), unit)

        raise commands.BadArgument(message='Not a valid duration')

class Commands(commands.Cog):

    def __init__(self, bot):
            self.bot = bot
            self.polls = []
            

  #  @commands.group(invoke_without_command=True)
   # async def help(ctx):
    #    em = discord.Embed(title="Help", description=(f'Type {get_prefix}help <command> for more info on each command'))

     #   em.add_field(name="Moderation", value="kick, ban, unban, tempban, warn, clear, changeprefix, server, mention")
      #  em.add_field(name="Fun", value="woofer")

       # await ctx.send(embed=em)

#add bite command

    @commands.command(aliases=["roll"])
    async def roulette(self, ctx):

        responses = ["click", "click", "click", "click", "click", "BANG :skull:"]

        random_response = random.choice(responses)

        if random_response == "BANG":
            await ctx.send(f"\n{random_response}")
            await ctx.send("GG")
        else:
            await ctx.send("Click")


    @commands.command(name="poll", aliases=["createpoll"])
    async def create_poll(self, ctx, hours: int, question, *options):
        
        if len(options) > 10:
            await ctx.send("You can only have 10 options.")

        else:
            embed = Embed(title="Poll",
                            description=question,
                            colour=ctx.author.colour,
                            timestamp=datetime.utcnow())

            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                        ("Instructions", "React to cast a vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)

            self.polls.append((message.channel.id, message.id))

            mid = message.id
            cid = message.channel.id

            time.sleep(hours)
     
            message = await self.bot.get_channel(cid).fetch_message(mid)

            most_voted = max(message.reactions, key=lambda r: r.count)
            podium = {}

            for reaction in message.reactions:
                podium[reaction] = reaction.count

            # podium.sort(reverse=True)
            # podium = podium[:3]

            res = f"\n Results: "
            
            await message.channel.send(f"Option {most_voted.emoji} won with {most_voted.count-1:,} vote(s)! ggs all around :D")

            for x, y in podium.items():
                res = res + (f"{x.emoji} : ||{y} vote(s)|| ")

            await message.channel.send(res)

            
            self.polls.remove((message.channel.id, message.id))
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

   @help.command()
   async def kick(self, ctx):
       em = discord.Embed(title= "Kick", description="Kicks a member from the server", color = ctx.author.color)
       em.add_field(name= "**Syntax**", value=f'{get_prefix}kick <member> [reason]')
       await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.kick(reason=reason)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Get banned {member.mention}! :cop:')
        await ctx.guild.ban(member)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: commands.MemberConverter, *, reason=None, duration: DurationConverter):
        multiplier = {'s': 1, 'm': 60}
        amount, unit = duration

        await ctx.guild.ban(member)
        await member.ban(reason=reason)
        await ctx.send(f'Get banned {member.mention}! :cop:')
        await ctx.send(f'{member.mention} has been banned for {amount} {unit}.')
        await asyncio.sleep(amount * multiplier[unit])
        await ctx.guild.unban(member)



    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'Prefix for typing commands changed to: {prefix}')

    @commands.command()
    # MENTIONS A ROLE
    async def mention(self, ctx):
        boons = get(ctx.guild.roles, name='boons')
        await ctx.send(f"{boons.mention}")

    @commands.command()
    # MENTIONS A ROLE
    async def warn(self, ctx, member, *, warning):
        print("yo")
        await ctx.send(f"{member.mention} {warning}")

    @commands.command(aliases=['doggo', 'dog', 'doge'])
    async def woofer(self, ctx, *, question):
        responses = ['fren stahp, you are doin me a scare',
                     'heck',
                     'Invest in doggo coin.',
                     'anime = :wastebasket:']
        await ctx.send(f'{ctx.author.mention} {random.choice(responses)}')
    @woofer.error
    async def woofer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please ask the doggo something.')


    @commands.command()
    async def server(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="ServerID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in (poll[1] for poll in self.polls):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            
            for reaction in message.reactions:
                if not payload.member.bot and payload.member in await reaction.users().flatten() and reaction.emoji != payload.emoji.name:
                    await message.remove_reaction(reaction.emoji, payload.member)



def setup(bot):
    bot.add_cog(Commands(bot))
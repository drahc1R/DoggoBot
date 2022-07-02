import discord
import random
from discord.ext import commands
from discord.utils import get
import json
import asyncio


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

  #  @commands.group(invoke_without_command=True)
   # async def help(ctx):
    #    em = discord.Embed(title="Help", description=(f'Type {get_prefix}help <command> for more info on each command'))

     #   em.add_field(name="Moderation", value="kick, ban, unban, tempban, warn, clear, changeprefix, server, mention")
      #  em.add_field(name="Fun", value="woofer")

       # await ctx.send(embed=em)

#add bite command

    @commands.command(alisases=["russian roulette"])
    async def roulette(self, ctx):

        responses = ["click", "click", "click", "click", "click", "BANG"]

        random_response = random.choice(responses)

        if random_response == "BANG":
            await ctx.send(f"\n{random_response}")
            await ctx.send("GG")
        else:
            await ctx.send("Click")



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You are smol pupper!')

 #   @help.command()
  #  async def kick(self, ctx):
   #     em = discord.Embed(title= "Kick", description="Kicks a member from the server", color = ctx.author.color)
    #    em.add_field(name= "**Syntax**", value=f'{get_prefix}kick <member> [reason]')
     #   await ctx.send(embed = em)

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



def setup(bot):
    bot.add_cog(Commands(bot))
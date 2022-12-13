import discord
from datetime import datetime
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["whois", "uinfo"])
    async def userinfo(self, ctx, member: discord.Member = None):
        roles = []
        if not member:
            member = ctx.author
        for role in member.roles:
            roles.append(str(role.mention))

        roles.reverse()

        embed = discord.Embed(title = f"User Info - {member.name}#{member.discriminator}", description = f"ID: {member.id}", color = member.color, timestamp = ctx.message.created_at)
        embed.add_field(name = "Nickname", value = member.display_name, inline = False)
        embed.add_field(name = "Created At", value = datetime.strftime(member.created_at, "%A, %B %-d, %Y"), inline = False)
        embed.add_field(name = "Joined At", value = datetime.strftime(member.joined_at, "%A, %B %-d, %Y"), inline = False)

        if len(str(" | ".join([x.mention for x in member.roles]))) > 1024:
            embed.add_field(name = f"Roles [{len(member.roles)}]", value = "Too many to display", inline = False)
        else:
            embed.add_field(name = f"Roles [{len(member.roles)}]", value = " | ".join(roles), inline = False)

        embed.add_field(name = "Role Color", value = member.color, inline = False)
        embed.add_field(name = "Status", value = member.status)
        embed.set_footer(text = f"Requested by - {ctx.author}", icon_url = ctx.author.avatar.url)
        embed.set_thumbnail(url = member.avatar)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["server", "sinfo"])
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        sinfo = discord.Embed(timestamp = ctx.message.created_at, color = ctx.author.color)
        sinfo.add_field(name = "Name", value = f"{ctx.guild.name}", inline = False)
        sinfo.add_field(name = "Member Count", value = ctx.guild.member_count, inline = False)
        sinfo.add_field(name = "Verification Level", value = str(ctx.guild.verification_level), inline = False)
        sinfo.add_field(name = "Highest Role", value = ctx.guild.roles[-2], inline = False)
        sinfo.add_field(name = "Number of Roles", value = str(role_count), inline = False)
        sinfo.add_field(name = "Bots", value = " | ".join(list_of_bots), inline = False)
        sinfo.set_thumbnail(url = ctx.guild.icon)
        await ctx.send(embed = sinfo)

def setup(client):
    client.add_cog(UserInfo(client))
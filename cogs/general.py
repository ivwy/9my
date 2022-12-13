import discord
from datetime import datetime
from discord.ext import commands

import asyncio
import time

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    ## purge command
    @commands.command(aliases = ["clear"])
    async def purge(self, ctx, amount: int):
        if amount > 1000:
            await ctx.send(f"Too many messages to search given ({amount}/1000)")
        else:
            count_members = {}
            messages = await ctx.channel.history(limit = amount).flatten()
            for message in messages:
                if str(message.author) in count_members:
                    count_members[str(message.author)] += 1
                else:
                    count_members[str(message.author)] = 1

            new_string = []
            messages_deleted = 0
            for author, message_deleted in list(count_members.items()):
                new_string.append(f"**{author}**: {message_deleted}")
                messages_deleted += message_deleted
            
            final_string = "\n".join(new_string)
            await ctx.channel.purge(limit = amount + 1)

            if messages_deleted == 1:
                msg = await ctx.send(f"{messages_deleted} message was removed. \n{final_string}")
            elif messages_deleted == 0:
                msg = await ctx.send("No messages were deleted.")
            else:
                msg = await ctx.send(f"{messages_deleted} messages were removed. \n{final_string}")

            await asyncio.sleep(2)
            await msg.delete()

def setup(client):
    client.add_cog(General(client))
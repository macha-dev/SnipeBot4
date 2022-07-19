import interactions
from embed.osu import create_osu_embed
class Track(interactions.Extension): # must have commands.cog or this wont work
    def __init__(self, client):
        self.client: interactions.Client = client
        self.osu = client.auth
        self.database = client.database

    @interactions.extension_command(
            name="track", 
            description="add a user to be tracked in the channel",
            options=[interactions.Option(
                name="username",
                description="the username of the user",
                type=interactions.OptionType.STRING,
                required=True,
            )
        ]
    )
    async def track(self, ctx: interactions.CommandContext, username: str):
        if await self.database.get_channel(ctx.channel_id._snowflake):
            await ctx.send(f"<@{ctx.author.id}> channel is already being tracked! (1 tracked user per channel)")
            return

        user_data = await self.osu.get_user_data(str(username))
        await self.database.add_channel(ctx.channel_id._snowflake, username, user_data)
        await ctx.send(f"Started tracking user {user_data['username']} in this channel!")

def setup(client):
    Track(client)
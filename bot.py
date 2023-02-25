""" PYTHON VERSION: Python 3.10.4"""

import discord
import sys

# Initialize your bot client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_channel_permissions(guild, channel):
    bot_member = guild.me

    if isinstance(channel, discord.TextChannel):
            permissions = channel.permissions_for(bot_member)
            return permissions.send_messages
                
async def get_all_channel_ids(guild_id):

    current_guild = client.get_guild(guild_id)
    
    channel_ids = []

    idx = 0
    for channel in current_guild.text_channels:

        if await check_channel_permissions(current_guild, channel):
                channel_ids.append((idx, channel.name, channel.id))
                idx += 1

    return channel_ids


async def shutdown():
    print("\nShutting down the bot...")
    await client.close()


@client.event
async def on_connect():
    global full_username
    full_username = f"{client.user.name}#{client.user.discriminator}"
    print(f"{full_username} is connecting...")


@client.event
async def on_ready():
    # This will be called when the bot connects to Discord
    print(f"Logged in as {full_username}\n")

    #Show guilds
    print("Available guilds:")
    guilds = [(index, guild.id, guild.name) for index,guild in enumerate(client.guilds)]

    for guild in guilds:
        print(f"[{guild[0]}] {guild[2]}")
    
    #Select guild
    while True:
        try:
            id = int(input("\nChoose guild by number: "))

            for guild in guilds:
                if guild[0] == id:
                    current_guild = guild[1] #guild[1] has the corresponding guild id
                else:
                    raise Exception("\nInvalid guild\n")
            break
        except Exception as ex:
            print("\n" + str(ex) + "\n")
    
    while True:
        # Show available channels here
        print("\nAvailable channels:")

        all_channels = await get_all_channel_ids(current_guild)
        target = ""

        for channel in all_channels:
            print(f"[{channel[0]}] {channel[1]}")

            available_ids = [channel[0] for channel in all_channels]
            available_channel_ids = [channel[2] for channel in all_channels]

        while True:
            try:
                option = int(input("Select channel by its number: "))
                break
            except:
                print("\nAn index must be of type int\n")

        # Choose target channel by index if it exists
        if option in available_ids:
            target = available_channel_ids[option]
        else:
            print("\nChannel doesn't exist\n")
            continue

        channel = client.get_channel(target)

        # Send message loop
        while True:
            msg = ""
            msg = input("Message to send: ")

            if msg == "shutdown":
                await shutdown()
                sys.exit(0)
                
            if msg == "^END":
                print("\nChanging channel...\n")
                break
            else:
                try:
                        await channel.send(msg)
                except:
                        print("\n403 Forbidden, please choose another channel\n")

TOKEN = "YOUR TOKEN HERE"
client.run(TOKEN, log_handler=None)

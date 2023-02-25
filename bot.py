""" PYTHON VERSION: Python 3.10.4"""

import discord
import sys
import requests
import json

# Initialize your bot client
intents = discord.Intents.default()
intents.members = True
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
            print("\n" + str(ex))
    
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
            stop_dm = False
            
            msg = ""
            msg = input("Message to send: ")

            """COMMANDS"""
            if msg == "^SHUTDOWN":
                await shutdown()
                sys.exit(0)

            #Random english word with API
            if "^RANDOM" in msg:
                
                url = "https://random-word-api.herokuapp.com/word"
                r = requests.get(url)
                j = json.loads(r.content)

                msg = msg.replace("^RANDOM", j[0])

            #DM
            if msg == "^DM":
                try:
                    members = client.get_guild(current_guild).members
                    
                except Exception as ex:
                    print(ex)
                    continue
                
                all_members = []

                #Fetch members
                m_index = 0
                for m in members:
                    if not m.bot:
                        all_members.append((m_index, f"{m.name}#{m.discriminator}", m.id))
                        m_index += 1

                #Show member list
                print("\n#####")
                print("Guild Members:")

                for m in all_members:
                    print(f"[{m[0]}] {m[1]}")
                print("#####\n")
                
                while True:
                    try:
                        select_member = int(input("Enter member index: "))

                        #If doesn't exists
                        exists = select_member in [m[0] for m in all_members]

                        if not exists:
                            raise Exception("Invalid user!")

                        get_members = [m[2] for m in all_members]
                        
                        target_member = await client.fetch_user(get_members[select_member])
                        target_member_channel = await target_member.create_dm()
                        
                        dm_msg = ""
                        print("\nEnstablishing communication...\n")

                        while dm_msg != "^END":
                            dm_msg = input("Enter message to send (^END to stop): ")

                            if not dm_msg == "^END":
                                await target_member_channel.send(dm_msg)

                        stop_dm = True
                        break
                    except Exception as ex:
                        print("\n" + str(ex) + "\n")

            #After we're done sending DMs, return to channel browser
            if stop_dm:
                break
            
            #STOP SENDING MESSAGES AND GO BACK TO CHANNELS BROWSER    
            if msg == "^END":
                print("\nChanging channel...\n")
                break

            #Send message
            else:
                try:
                        await channel.send(msg)
                except:
                        print("\n403 Forbidden, please choose another channel\n")

TOKEN = "YOUR TOKEN HERE"
client.run(TOKEN, log_handler=None)

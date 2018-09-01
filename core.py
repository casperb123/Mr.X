import discord
import asyncio
import time
import os
import json
from discord.ext.commands import Bot
from discord.ext import commands
from itertools import cycle
import sys
import checks

TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '-')
client.remove_command('help')
status = ['Commands: -help', 'Watching you']
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
extensions = ['fun', 'admin', 'utility', 'swarm']

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)

async def create_settings(servers, serverunit):
    servers[serverunit.id] = {}
    servers[serverunit.id]['Ignore_Hierarchy'] = False
    servers[serverunit.id]['DMWarn'] = True
    servers[serverunit.id]['Verify_Role'] = "none"
    servers[serverunit.id]['Mod_Role'] = "none"
    servers[serverunit.id]['Join_Role'] = "none"
    servers[serverunit.id]['Admin_Role'] = "none"
    servers[serverunit.id]['Mute_Role'] = "none"
    servers[serverunit.id]['WarnMute'] = "1h"
    servers[serverunit.id]['JoinToggle'] = False
    servers[serverunit.id]['CanModAnnounce'] = False
    servers[serverunit.id]['Level_System'] = True
    servers[serverunit.id]['Chat_Filter'] = False

async def update_settings(serverunit, setting, set):
    with open('srv_settings.json', 'r') as f:
        servers = json.load(f)
        if not serverunit.id in servers:
            await create_settings(servers, serverunit)

    servers[serverunit.id][setting] = set
    with open('srv_settings.json', 'w') as f:
        json.dump(servers, f)

async def check_settings(serverunit, setting):
    with open('srv_settings.json', 'r') as f:
        servers = json.load(f)
        setting = servers[serverunit.id][setting]
    return setting

@client.event
async def on_ready():
    print("Bot is online.")

@client.event
async def on_server_join(serverunit):
    with open('srv_settings.json') as json_file:
        servers = json.load(json_file)
        if not serverunit.id in servers:
            await create_settings(servers, serverunit)
            with open('srv_settings.json', 'w') as f:
                json.dump(servers, f)
                print("Dumped")

@client.event
async def on_member_join(member):
    server = member.server
    join_toggle = await check_settings(server, "JoinToggle")
    if join_toggle == True:
        join_role = await check_settings(server, "Join_Role")
        role = discord.utils.get(server.roles, name=join_role)
        await client.add_roles(member, role)

@client.event
async def on_member_unban(server, member):
    with open("autobans.json", "r") as f:
        autobans = json.load(f)
        ban_array = autobans[server.id]["banlist"]

        for userid in ban_array:
            if userid == member.id:
                await client.ban(member)

# @client.event
# async def on_message(message):
#     message.content = message.content.lower().replace(' ', '')
#     await client.process_commands(message)

@client.command()
async def botinfo():
    embed = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.blue()
    )
    embed.set_footer(text='Coded in Python - Multi-Purpose Bot')
    embed.set_image(url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
    embed.set_author(name='Bot Information', icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
    embed.add_field(name='Bot Name', value='Mr. X', inline=False)
    embed.add_field(name='Creator', value='Mr. Zer0#8366', inline=False)
    embed.add_field(name='Creator', value='Woody#3599', inline=False)
    embed.add_field(name='Artist', value='SirNeeco#0221', inline=False)
    embed.add_field(name='Version', value='0.5', inline=False)
    embed.add_field(name='Python Version', value=sys.version, inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def settings(ctx):
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    with open('srv_settings.json', 'r') as f:
        servers = json.load(f)
        Ignore_Hierarchy = str(servers[server.id]["Ignore_Hierarchy"])
        DMWarn = str(servers[server.id]["DMWarn"])
        Verify_Role = servers[server.id]["Verify_Role"]
        Mod_Role = servers[server.id]["Mod_Role"]
        Join_Role = servers[server.id]["Join_Role"]
        Admin_Role = servers[server.id]["Admin_Role"]
        Mute_Role = servers[server.id]["Mute_Role"]
        WarnMute = servers[server.id]["WarnMute"]
        JoinToggle = str(servers[server.id]["JoinToggle"])
        CanModAnnounce = str(servers[server.id]["CanModAnnounce"])
        Level_System = str(servers[server.id]["Level_System"])

    await client.say('Do you want the list **Inline** ? (Yes/No)')
    user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
    if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
        inline = True
    elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
        inline = False
    else:
        await self.client.say("Invalid.")
        return

    embed = discord.Embed(
        title = '',
        description = '',
        colour = discord.Colour.blue()
    )

    if server.icon_url != "":
        embed.set_thumbnail(url=server.icon_url)

    embed.set_author(name='{} Server Settings'.format(server), icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
    embed.add_field(name='Ignore Hierarchy', value=Ignore_Hierarchy, inline=inline)
    embed.add_field(name='Direct message on warn', value=DMWarn, inline=inline)
    embed.add_field(name='Verify Role', value=Verify_Role, inline=inline)
    embed.add_field(name='Moderator Role', value=Mod_Role, inline=inline)
    embed.add_field(name='Join Role', value=Join_Role, inline=inline)
    embed.add_field(name='Administrator Role', value=Admin_Role, inline=inline)
    embed.add_field(name='Mute Role', value=Mute_Role, inline=inline)
    embed.add_field(name='Warning mute time', value=WarnMute, inline=inline)
    embed.add_field(name='Auto role on join', value=JoinToggle, inline=inline)
    embed.add_field(name='Can moderator announce', value=CanModAnnounce, inline=inline)
    embed.add_field(name='Level system', value=Level_System, inline=inline)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def mylevel(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        level_sys = json.load(f)
        my_level = level_sys[user.id]["level"]
    embed = discord.Embed(
    title = '',
    description = '{} you are level {}'.format(user.mention, my_level),
    colour = discord.Colour.green()
    )
    await client.say(embed=embed)

@client.command(pass_context=True)
async def whitelist(ctx):
    author = ctx.message.author
    if author.id == 164068466129633280 or author.id == 142002197998206976:
        with open('whitelist.json', 'r') as f:
            servers = json.load(f)
        if not server.id in servers:
            await create_settings(servers, serverunit)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def togglelevel(ctx):
    author = ctx.message.author
    server = author.server
    if author == server.owner or author.id == 164068466129633280:
        toggle = await check_settings(server, "Level_System")
        if toggle == True:
            await update_settings(server, "Level_System", False)
            embed = discord.Embed(
            title = 'Global Level System',
            description = 'You have **disabled** the Level System on this server.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        elif toggle == False:
            await update_settings(server, "Level_System", True)
            embed = discord.Embed(
            title = 'Global Level System',
            description = 'You have **enabled** the Level System on this server.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            print("Error")
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def cmds(ctx):
    await client.say("Please use the -help command.")

@client.command(pass_context=True)
async def cmd(ctx):
    await client.say("Please use the -help command.")

@client.command(pass_context=True)
async def command(ctx):
    await client.say("Please use the -help command.")

@client.command(pass_context=True)
async def commands(ctx):
    await client.say("Please use the -help command.")

@client.command(pass_context=True)
async def dmwarn(ctx):
    author = ctx.message.author
    server = ctx.message.server
    current = await check_settings(server, "DMWarn")
    if author.server_permissions.administrator:
        if current == True:
            await update_settings(server, "DMWarn", False)
            embed = discord.Embed(
            title = 'DMWarn Setting',
            description = 'Direct Message on warning has been set to **False**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = 'DMWarn Setting',
            description = 'Direct Message on warning has been set to **True**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
            await update_settings(server, "DMWarn", True)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def modrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            await update_settings(server, "Mod_Role", newrole)
            embed = discord.Embed(
            title = 'Moderator Role',
            description = 'The Moderator Role has been set to **{}**'.format(rolename),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = 'Moderator Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)
@client.command(pass_context=True)
async def adminrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            await update_settings(server, "Admin_Role", newrole)
            embed = discord.Embed(
            title = 'Administrator Role',
            description = 'The Administrator Role has been set to **{}**'.format(rolename),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = 'Administrator Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def muterole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            await update_settings(server, "Mute_Role", newrole)
            embed = discord.Embed(
            title = 'Muted Role',
            description = 'The Muted Role has been set to **{}**'.format(rolename),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = 'Muted Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)
@client.command(pass_context=True)
async def joinrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                title = 'Join Role',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                await update_settings(server, "Join_Role", newrole)
                embed = discord.Embed(
                title = 'Join Role',
                description = 'The Join Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = 'Join Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def verifyrole(ctx, *, role):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                title = 'Verify Role',
                description = 'Role not found.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                await update_settings(server, "Verify_Role", newrole)
                embed = discord.Embed(
                title = 'Verify Role',
                description = 'The Verify Role has been set to **{}**'.format(rolename),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
        title = 'Verify Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def mutetime(ctx, lenght):
    server = ctx.message.author.server
    if author.server_permissions.administrator:
        if "m" in lenght:
            t_time = lenght.replace("m", "")
            await update_settings(server, "WarnMute", str(lenght))
            embed = discord.Embed(
            title = '',
            description = 'Punish Mute has been set to {} minute(s)'.format(t_time),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        elif "h" in lenght:
            t_time = lenght.replace("h", "")
            await update_settings(server, "WarnMute", str(lenght))
            embed = discord.Embed(
            title = '',
            description = 'Punish Mute has been set to {} hour(s)'.format(t_time),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            await self.client.say("Please use minutes or hours, example: -mutetime 1h")
            return
    else:
        embed = discord.Embed(
            description = 'You do know have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def jointoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    current_toggle = await check_settings(server, "JoinToggle")
    join_role = await check_settings(server, "Join_Role")
    if author.server_permissions.administrator:
        if current_toggle == False:
            if join_role == "None":
                embed = discord.Embed(
                title = 'Join Toggle',
                description = 'Please set a join role before trying to turn on auto role.',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                await update_settings(server, "JoinToggle", True)
                embed = discord.Embed(
                title = 'Join Toggle',
                description = 'Auto role on join has been set to **True**',
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            await update_settings(server, "JoinToggle", False)
            embed = discord.Embed(
            title = 'Join Toggle',
            description = 'Auto role on join has been set to **False**',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = 'Join Toggle',
            description = 'Error',
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
        title = 'Join Role',
        description = 'You do know have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def mod(ctx, user: discord.Member):
    author = ctx.message.author
    server = ctx.message.server
    modrole = await check_settings(server, "Mod_Role")
    if author.server_permissions.administrator:
        if discord.utils.get(user.roles, name=modrole):
                role = discord.utils.get(server.roles, name=modrole)
                await client.remove_roles(user, role)
                embed = discord.Embed(
                title = 'Moderator',
                description = 'Moderator role was removed from {}'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)
                return
        else:
            if modrole == "none":
                embed = discord.Embed(
                title = 'Moderator',
                description = 'The Moderator role has not been set, please use >modrole ROLE',
                colour = discord.Colour.red()
                )
                await client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=modrole)
                await client.add_roles(user, role)
                embed = discord.Embed(
                title = 'Moderator',
                description = '{} has been given the Moderator role.'.format(user.mention),
                colour = discord.Colour.green()
                )
                await client.say(embed=embed)

@client.command(pass_context=True)
async def admin(ctx, user: discord.Member):
    author = ctx.message.author
    server = ctx.message.server
    adminrole = await check_settings(server, "Admin_Role")

    if discord.utils.get(user.roles, name=adminrole):
            role = discord.utils.get(server.roles, name=adminrole)
            await client.remove_roles(user, role)
            embed = discord.Embed(
            title = 'Administrator',
            description = 'Administrator role was removed from {}'.format(user.mention),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
            return
    else:
        if adminrole == "none":
            embed = discord.Embed(
            title = 'Administrator',
            description = 'The Administrator role has not been set, please use >adminrole ROLE',
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)
        else:
            role = discord.utils.get(server.roles, name=adminrole)
            await client.add_roles(user, role)
            embed = discord.Embed(
            title = 'Administrator',
            description = '{} has been given the Administrator role.'.format(user.mention),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)

@client.command(pass_context=True)
async def userid(ctx, user: discord.Member):
    author = ctx.message.author
    user_id = user.id
    embed = discord.Embed(
    title = '',
    description = "{}'s ID is `{}`".format(user.mention, user_id),
    colour = discord.Colour.green()
    )
    await client.say(embed=embed)

@client.command(pass_context=True)
async def members(ctx):
    server = ctx.message.author.server
    embed = discord.Embed(
    title = '',
    description = "There are `{}` members in this server.". format(len(server.members)),
    colour = discord.Colour.green()
    )
    await client.say(embed=embed)


@client.command(pass_context=True)
async def mywarns(ctx):
    user = ctx.message.author
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
    warnpath = path + "warnings.json"
    if not os.path.exists(path):
        embed = discord.Embed(
        title = "Your Warnings".format(user),
        description = 'You have no warnings.',
        colour = discord.Colour.green()
        )
        await client.say(embed=embed)
        return
    else:
        if not os.path.exists(warnpath):
            embed = discord.Embed(
            title = "Your Warnings".format(user),
            description = 'You have no warnings.',
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
            return
        else:
            with open(warnpath, 'r') as f:
                warns_list = json.load(f)
                current_warnings = warns_list[user.id]["Warnings"]

            cnt = 1
            embed = discord.Embed(
                title = "Your Warnings".format(user),
                description = '',
                colour = discord.Colour.blue()
            )
            await client.say('Do you want the list **Inline** ? (Yes/No)')
            user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
            if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
                inline = True
            elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
                inline = False
            else:
                await self.client.say("Invalid.")
                return
            for warn_reason in current_warnings:
                embed.add_field(name='Warning {}'.format(str(cnt)), value=warn_reason, inline=inline)
                cnt += 1
            await client.say(embed=embed)

@client.command(pass_context=True)
async def autoban(ctx, user: discord.Member):
    server = ctx.message.author.server
    if ctx.message.author.id == "164068466129633280" or ctx.message.author.id == "142002197998206976":
        isbanned = False
        with open("autobans.json", "r") as f:
            if "banlist" in f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]

                for userid in ban_array:
                    if userid == user.id:
                        isbanned = True
        if isbanned == True:
            embed = discord.Embed(
                description = "The user {} is already auto banned".format(user.mention),
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
        else:
            with open("autobans.json", "w+") as f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]
                ban_array.append(user.id)
                json.dump(autobans, f)
            await client.ban(user)
            embed = discord.Embed(
                description = "The user {} has been auto banned".format(user.mention),
                colour = discord.Colour.green()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = "You don't have permission to use this command",
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unautoban(ctx, id):
    server = ctx.message.author.server
    if ctx.message.author.id == "164068466129633280" or ctx.message.author.id == "142002197998206976":
        isbanned = False
        with open("autobans.json", "r") as f:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]

            for userid in ban_array:
                if userid == user.id:
                    isbanned = True
        if isbanned == True:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]
            ban_array.remove(id)
            json.dump(autobans, f)
            embed = discord.Embed(
                description = "The user with the id `{}` has been removed from the autoban list".format(id),
                colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "The user with the id {} isn't auto banned".format(id),
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = 'You do know have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def resetsetting(ctx, setting = None):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        if setting != None:
            if setting == "setwarn":
                print("Reset Setwarn")
            else:
                embed = discord.Embed(
                    description = 'Invalid setting. Enter one of the following [setwarn]',
                    colour = discord.Colour.red()
                )
                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = 'You have not entered a setting. Enter one of the following [setwarn]',
                colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description = 'You do not have permission to use this command',
            colour = discord.Colour.red()
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def load(ctx, extension):
    if ctx.message.author.id == 164068466129633280 or ctx.message.author.id == 142002197998206976:
        try:
            client.load_extension(extension)
            embed = discord.Embed(
            title = 'Module Loaded',
            description = 'The module {} has been successfully loaded.'.format(extension),
            colour = discord.Colour.green()
            )
            await client.say(embed=embed)
        except Exception as error:
            client.load_extension(extension)
            embed = discord.Embed(
            title = 'Module Error',
            description = '{} cannot be loaded. [{}]'.format(extension, error),
            colour = discord.Colour.red()
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '',
        description = 'You do not have permission to use this command',
        colour = discord.Colour.red()
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def unload(ctx, extension):
    if ctx.message.author.id == 164068466129633280 or ctx.message.author.id == 142002197998206976:
        try:
            client.unload_extension(extension)
            print('Unloaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be unloaded. [{}]'.format(extension, error))


if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.loop.create_task(change_status())
    client.run(TOKEN)

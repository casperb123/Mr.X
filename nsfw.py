import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
import praw
import random
import pymysql
import os
import aiohttp
from html.parser import HTMLParser

class NSFW:
    def __init__(self, client):
        self.client = client

    async def is_nsfw(self, channel: discord.Channel):
        try:
            _gid = channel.server.id
        except AttributeError:
            return False
        data = await self.client.http.request(discord.http.Route('GET', '/guilds/{guild_id}/channels', guild_id=_gid))
        channeldata = [d for d in data if d['id'] == channel.id][0]
        return channeldata['nsfw']

    def check_database(self, server, setting):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(
            setting, str(server.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        for row in data:
            if row == 1:
                return True
            elif row == 0:
                return False
            else:
                return row

    def check_blacklist(self, setting, server, user):
        path = "blacklist/" + str(user.id) + ".json"
        if not os.path.exists(path):
            return False
        else:
            with open(path, 'r') as f:
                blacklistcheck = json.load(f)
                if str(server.id) in blacklistcheck:
                    current = blacklistcheck[server.id][setting]
                    if current == True:
                        return True
                    else:
                        return False
                else:
                    return False

    def getPornImage(self, url):
        req = urllib.request.Request(url)
        fp = urllib.request.urlopen(req)
        mybytes = fp.read()
        message = mybytes.decode("utf8")
        fp.close()

        images = []
        class MyHTMLParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == "img":
                    toAppend = []
                    if len(attrs) == 6 and "https://images.sex.com" in attrs[2][1]:
                        toAppend.append(attrs[2][1])
                        toAppend.append(attrs[5][1])

                    images.append(toAppend)

        parser = MyHTMLParser()
        parser.feed(message)
        image = []
        while True:
            image = random.choice(images)
            if len(image) == 2:
                break

        return image

    @commands.command(pass_context=True)
    async def porng(self, ctx, *, searchValue = None):
        author = ctx.message.author
        server = author.server

        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            if searchValue == None:
                image = self.getPornImage("https://www.sex.com/gifs/?sort=popular&sub=all")
                embed = discord.Embed(
                    title = "Popular search result",
                    description = image[1],
                    color = 0x800080
                )
                embed.set_image(url=image[0])

                await self.client.say(embed=embed)
            else:
                image = self.getPornImage("https://www.sex.com/search/gifs?query={}".format(searchValue))
                embed = discord.Embed(
                    title = "{} search result".format(searchValue),
                    description = image[1],
                    color = 0x800080
                )
                embed.set_image(url=image[0])

                await self.client.say(embed=embed)

        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def porn(self, ctx, *, searchValue = None):
        author = ctx.message.author
        server = author.server

        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            if searchValue == None:
                image = self.getPornImage("https://www.sex.com/pics/?sort=popular&sub=all")
                embed = discord.Embed(
                    title = "Popular search result",
                    description = image[1],
                    color = 0x800080
                )
                embed.set_image(url=image[0])

                await self.client.say(embed=embed)
            else:
                image = self.getPornImage("https://www.sex.com/search/pics?query={}".format(searchValue))
                embed = discord.Embed(
                    title = "{} search result".format(searchValue),
                    description = image[1],
                    color = 0x800080
                )
                embed.set_image(url=image[0])

                await self.client.say(embed=embed)

        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def fourk(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=4k", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gonewild(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=gonewild", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdneko(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return
        
        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdneko", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def holo(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/hololewd", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gasm(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/gasm", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdkitsune(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdkitsune", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def furry(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            reddit = praw.Reddit(
                client_id="G9hlJ0OTkWFNhw",
                client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
                password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
                user_agent="Alice discord bot",
                username="WoodyTheSecond"
            )
            submissions = reddit.subreddit("yiff").hot()
            post_to_pick = random.randint(1, 50)
            for i in range(0, post_to_pick):
                submission = next(x for x in submissions if not x.stickied)

            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=submission.url)
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def tentai(self, ctx):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            reddit = praw.Reddit(
                client_id="G9hlJ0OTkWFNhw",
                client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
                password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
                user_agent="Alice discord bot",
                username="WoodyTheSecond"
            )
            submissions = reddit.subreddit("Tentai").hot()
            post_to_pick = random.randint(1, 50)
            for i in range(0, post_to_pick):
                submission = next(x for x in submissions if not x.stickied)

            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=submission.url)
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def rule34(self, ctx, tag = None):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            if tag == None:
                embed = discord.Embed(
                    description="You need to write a tag",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

            try:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags={tag}") as r:
                        data = json.loads(await r.text())
                
                non_loli = list(filter(lambda x: 'loli' not in x['tags'] and 'shota' not in x['tags'], data))
                if len(non_loli) == 0:
                    embed = discord.Embed(
                        description = "Loli/Shota is not allowed by discord TOS",
                        color = 0xFF0000
                    )
                    await self.client.say(embed=embed)
                    return

                response = non_loli[random.randint(0, len(non_loli) - 1)]
                img = f"https://img.rule34.xxx/images/{response['directory']}/{response['image']}"
                embed = discord.Embed(
                    color = 0x800080
                )
                embed.set_image(url=img)
                await self.client.say(embed=embed)
            except:
                embed = discord.Embed(
                    description = "Couldn't find anything",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def e621(self, ctx, tag = None):
        author = ctx.message.author
        server = author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if self.check_blacklist("NSFW", server, author) == True:
            embed = discord.Embed(
                description="You are blacklisted",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            if tag == None:
                embed = discord.Embed(
                    description="You need to write a tag",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

            try:
                ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
                async with aiohttp.ClientSession() as cs:
                        async with cs.get(f"https://e621.net/post/index.json?limit=15&tags={tag}",
                                        headers={"User-Agent": ua}) as r:
                            res = await r.json()
                data = random.choice(res)
                if data == []:
                    embed = discord.Embed(
                        description = "No images found",
                        color = 0xFF0000
                    )

                    await self.client.say(embed=embed)
                    return

                if "loli" in data["tags"] or "shota" in data["tags"]:
                    embed = discord.Embed(
                        description = "Loli/Shota is not allowed by discord TOS",
                        color = 0xFF0000
                    )

                    await self.client.say(embed=embed)
                    return

                embed = discord.Embed(
                    color = 0x800080
                )
                embed.set_image(url=data["file_url"])

                await self.client.say(embed=embed)
            except:
                embed = discord.Embed(
                    description = "Couldn't find anything",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
            
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

def setup(client):
    client.add_cog(NSFW(client))

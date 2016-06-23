import requests
import json
import discord
from discord.ext import commands
from random import randint
from random import choice as randchoice
import datetime
import time
import aiohttp
import asyncio



snrl_help = ''' ```
1. What is this?
This is **Saturday Night Rocket League***. Just random pick up games that you can either join or host yourself. :)
2. Who can play?
Anyone! You on PC, Xbox One, or PS4? Good! You're welcome to join!
3. But wait? How do I join?
Easy, either host a match by posting your match at serverleague or join one that someone is already hosting.
4. Can I play in my own hosted games?
Of course you can! You can spectate, play, or stream. We even have a few people using this for casting practice!
5. Is this available for every region?
Thanks to our partnership with ServerLeague it is now available to everyone everywhere!
6. Is there a limit as to what I can host?
Nope! Any map or mode is welcome, when we get more hosters I'll post votes again to see what people are interested in playing to keep it better organized.
7. Should I set a password?
No! Games should be always open, that's the point of drop in drop out. ;)
8. What does it require in terms of hardware or internet?
None, everything is hosted on Psyonix's servers.
9. How do I set my game up?
Hit add server at the top of the ServerLeague page, make sure you hit the Saturday Night Rocket League button to make it an SNRL match, you'll also be able to set start and end times.
If you want to change your match settings hit the "Vote for settings in game" button to re-activate the settings. Set your region, game name, time and date and platform and you're good to go. :)
```
'''
platforms = ['pc', 'ps4', 'xbox']
regions = ['asia-east', 'europe', 'us-east', 'us-west', 'oceania', 'middle-east', 'south america', 'asia-se mainland']

class ServerLeague(object):
    def __init__(self, json_response):
        self.parse_json(json_response)

    def parse_json(self, response):
        self.name = response['name']
        self.region = response['region']
        self.size = response['teamsize']
        self.arenas = response['arenas']
        if response['voteingame'] == "1":
            self.vote = True
            self.mutators = False
        else:
            self.mutators = True
            self.vote = False
            self.maxscore = response['maxscore']
            self.maxspeed = response['maxspeed']
            self.ballmaxspeed = response['ballmaxspeed']
            self.balltype = response['balltype']
            self.ballsize = response['ballsize']
            self.ballbounciness = response['ballbounciness']
            self.boostamount = response['boostamount']
            self.booststrength = response['booststregth']
            self.gravity = response['gravity']
            self.demolish = response['demolish']
            self.respawntime = response['respawntime']
        self.platform = response['platform']
        self.starttime = response['starttime']
        self.endtime = response['endtime']
        if response['snrl'] == 1:
            self.snrl = True
        else:
            self.snrl = False
    def print(self):
        result = '''
        name: {0}
        region: {1}
        platform: {2}
        arenas: {3}
        mutators: {4}
        '''.format(self.name, self.region, self.platform, self.arenas, self.mutators)
        return result


def get_servers(url):
    servers_list = []
    r = requests.get(url)
    response = json.loads(r.text)
    for server in response:
        server_settings = ServerLeague(server)
        servers_list.append(server_settings)
    return servers_list


def count_servers(servers_list):
    return len(servers_list)


def filter_by_region(servers, region):
    filtered_list = []
    for server in servers:
        if server.region == region:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


def filter_by_platform(servers, platform):
    filtered_list = []
    for server in servers:
        if server.platform == platform:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


def filter_by_vote(servers, vote):
    filtered_list = []
    for server in servers:
        if server.vote:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    async def hello(self):
        """hello world."""
        await self.bot.say("hi there!")


    @commands.command(hidden=True)
    async def count_servers(self):
        """servers command returns list of serverleague hosted servers."""
        servers = get_servers(url='http://dev.serverleague.com/api/v1/list')
        await self.bot.say("There are currently **" + str(count_servers(servers))+"** online")


    @commands.command(hidden=True)
    async def snrl(self):
        """FAQ."""
        await self.bot.say(snrl_help)

    @commands.command()
    async def servers(self, *args):
        servers = get_servers(url='http://dev.serverleague.com/api/v1/list')
        for arg in args:
            if arg.lower() in platforms:
                for server in servers:
                    if server.platform != arg.lower():
                        servers.remove(server)
            if arg.lower() in regions:
                for server in servers:
                    if server.region != arg.lower():
                        servers.remove(arg.lower())
        message = ''
        for server in servers:
            message += '/n' + server.print()
        await self.bot.say(message)

def setup(bot):
    bot.add_cog(ServerLeague(bot))

# servers = get_servers('http://dev.serverleague.com/api/v1/list')
# filtered_servers = filter_by_region(servers, "Oceania")
# for servers in filtered_servers[0]:
#     print servers.region
# print filtered_servers

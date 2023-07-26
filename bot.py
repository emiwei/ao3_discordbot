import os
import random

import extra, utils
from chapters import Chapter
from comments import Comment
from search import Search
from series import Series
from session import GuestSession, Session
from users import User
from works import Work

import discord 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "$help":
        await message.channel.send("$fandom <insert fandom or character name here> ~ specify which fandom/character \nexample:\n$fandom shrek\n \n$explicit ~ include this tag if you only want explicit results\n for example, if you want an explicit shrek fanfic, use\n$fandom shrek $explicit \n \n$tags <tag1> <tag2> <tag3> ~ include up to three tags, with a space separating each one\nexample:\n$tags hurt/comfort ")
    fandom = None
    explicit = None
    search_tags = None
    if message.content.split(" ")[0] == "$fandom":
        fandom = message.content.split("$")[1].split(" ")
        fandom = "+".join(fandom[1:])
    else:
        return
    if "$explicit" in message.content:
        explicit = 13
    if "$tags" in message.content:
        #print(message.content.split("$"))
        start_index = message.content.index("$tags")
        start_tags = message.content[start_index:].split("$")[1].split(" ")
        #if len(start_tags) > 3:

        search_tags = ",".join(start_tags[1:])
        #print(search_tags)
    if search_tags is None:
        search = Search(any_field=fandom, word_count=utils.Constraint(100, 10000), rating=explicit)
    else:
        search = Search(any_field=fandom, word_count=utils.Constraint(100, 10000), rating=explicit, tags=search_tags)
    search.update()
    if search.total_results > 0:
        random_num = random.randint(0, len(search.results)-1)
        randwork = search.results[random_num]
        workid = randwork[1]
        work = Work(workid)
        url = work.url
        title = str(randwork[0])
        title = title[7:len(str(randwork[0]))-2]
        rating = work.rating
        warnings = work.warnings
        warnings_str = ""
        for item in warnings:
            warnings_str+=(item + ", ") if item != warnings[-1] else item
        tags = work.tags
        tags_str = ""
        for tag in tags:
            tags_str+=(tag + ", ") if tag != tags[-1] else tag
        characters = work.characters
        char_str = ""
        for char in characters:
            char_str+=(char + ", ") if char != characters[-1] else char
        summary = work.summary
        await message.channel.send("Title: " + title)
        await message.channel.send("Rating: " + rating)
        await message.channel.send("Warnings: " + warnings_str)
        await message.channel.send("Characters: " + char_str)
        await message.channel.send("Tags: " + tags_str)
        await message.channel.send("-------------------------------------------------------------------------------")
        if summary is not None:
            await message.channel.send("Summary:")
            await message.channel.send(summary)
            await message.channel.send("-------------------------------------------------------------------------------")
        await message.channel.send(url)
    else:
        await message.channel.send("No results found")
    

client.run(TOKEN)



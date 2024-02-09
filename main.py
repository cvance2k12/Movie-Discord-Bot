import json
import os
import random

import discord
import requests
from discord import message
from replit import db

my_secret = os.environ['DISCORD_KEY']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "unsure", "sick"]

movie_genre = [
  "action",
  "adventure",
  "animation",
  "biography",
  "comedy",
  "crime",
  "documentary",
  "drama",
  "family",
  "fantasy",
  "film-noir",
  "game-show",
  "history",
  "horror",
  "music",
  "musical",
  "mystery",
  "romance",
  "sci-fi",
  "short",
  "sport",
  "talk-show",
  "thriller",
  "war",
  "western"
]

starter_encouragements = [
  "Cheer up!",
  "Hang in there partner.",
  "You are a great person / bot!",
  "You got this",
  "You will make it",
]

movie_opinions = [
  "I love that movie!",
  "I hate that movie.",
  "I don't like that movie.",
  "I don't know that movie.",
  "I don't care about that movie.",
  "I don't care about that movie.",]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)



def update_encouragements(encouraging_message):
  if "encouragements" in db:
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def update_movie_opinions(movie_opinion):
  if "movie_opinions" in db:
    movie_opinions = db["movie_opinions"]
    if movie_opinions is None:
      movie_opinions = []
    movie_opinions.append(movie_opinion)
    db["movie_opinions"] = movie_opinions
  else:
    db["movie_opinions"] = [movie_opinion]

def delete_movie_opinion(index):
  movie_opinions = db["movie_opinions"]
  if movie_opinions is not None and len(movie_opinions) > index:
    del movie_opinions[index]
    db["movie_opinions"] = movie_opinions


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('!help'):
    await message.channel.send('Hello! I may be a bot')

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db:
      options = options + list(db["encouragements"])
  
    movie_options = movie_opinions
    if "movie_opinions" in db:
      movie_options = movie_options + db["movie_opinions"]

  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(options))


  if any(word in message.content for word in movie_genre):
    await message.channel.send(random.choice(movie_opinions))

  if message.content.startswith("new"):
    encouraging_message = message.content.split("new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("del"):
    encouragements = []
    if "encouragements" in db:
      index = int(message.content.split("del",1)[1])
      delete_encouragement(index)
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  ##if message.content.startswith("new movie"):
   ## movie_opinion = message.content.split("movie ",1)[1]
   ## update_movie_opinions(movie_opinion)
   ## await message.channel.send("New movie opinion added.")

  ##if message.content.startswith("delete movie"):
   ## movie_opinions = []
    ##if "movie_opinions" in db.keys():
     ## index = int(message.content.split("delmovie",1)[1])
     ## delete_movie_opinion(index)
     ## movie_opinions = list(db["movie_opinions"])
  ##  await message.channel.send(movie_opinions)


##if message.content.startswith("list"):
  ##encouragements = []
  ##if "encouragements" in db:
    ##encouragements = db["encouragements"] 
    ##await message.channel.send(encouragements)

##if message.content.startswith("responding"):
  ##value = message.content.split("responding ",1)[1]

  ##if value.lower() == "true":
  ##  db["responding"] = True
   ## await message.channel.send("Responding is on.")
  ##else:
   ## db["responding"] = False
   ## await message.channel.send("Responding is off.")

client.run(my_secret)
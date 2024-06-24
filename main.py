import csolver
import scraper
import dotenv
import os
import discord
import asyncio

dotenv.load_dotenv()
sessionId = os.getenv("DWRSESSIONID")
tc = os.getenv("TC")
url = "https://ebideb.tubitak.gov.tr/olimpiyatSinavSonucSistemi.htm"

def bot():
  ret = scraper.scrape("1", tc, url, "gh.jpg") # you could actually use anything for your session id

  if ret == 0:
    ret = bot()
  
  return ret

def check(type): # if type == 1, then it is a message, otherwise it is a interval check
  usernames = ["kutaja"]
  mentions = ""
  for username in usernames:
    mentions += discord.utils.get(client.get_channel(1038196261309927444).guild.members, name=username).mention + " "
  if bot() == 1:
    return f"results are out (at least for ortaokul bilgisayar birinci asama) {mentions}"
  else:
    if type == 1:
      return f"results are not out (for informatics birinci asama)"
    else:
      return ""

client = discord.Client(intents=discord.Intents.all())
token = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  asyncio.ensure_future(send_message())

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if "birinci asama" not in msg:
    return
  
  response = check(1)

  await message.channel.send(response)

async def send_message():
  await client.wait_until_ready()
  channelids = [1038196261309927444]
  channels = []
  for channelid in channelids:
    channels.append(client.get_channel(channelid))

  while not client.is_closed():
    message = check(0)
    if message != "":
      for channel in channels:
        await channel.send(message)
    await asyncio.sleep(5)

loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(client.login(token))
  loop.run_until_complete(client.connect())
except KeyboardInterrupt:
  loop.run_until_complete(client.close())
finally:
  loop.close()

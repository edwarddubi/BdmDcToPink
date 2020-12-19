from discord.ext import tasks
from flask import Flask
from threading import Thread



app = Flask('')

@app.route('/')
def main():
  return "Bot is running"

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()


@tasks.loop(seconds=10)
async def change_status(client, discord):
  await client.change_presence(activity=discord.Game(next(status)))

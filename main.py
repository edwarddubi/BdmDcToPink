import discord
import os
from itertools import cycle
from keep_bot_alive import keep_alive

client = discord.Client()
token = os.environ.get("BOT_TOKEN")

prefix = "!"
wep_frags_to_pink = 900 * 3
armor_frags_to_pink = 240 * 4
is_wep = "wep="
is_armor = "armor="
wep_coins_cost = 920
armor_cost = [1360, 1200, 1040, 1040]
test = "!wep=300, 435, 678"

status = cycle(['BdmPinkGears | !usage', 'House'])

@client.event
async def on_ready():
    msg = "{0} is logged on.".format(client.user.display_name)
    print(msg)
    await client.change_presence(activity=discord.Game(next(status)))

    
@client.event
async def on_message(message):
    if message.author == client.user:
      return
    cmd = message.content.lower()
    channel = message.channel
    err_msg = "<@{0}>, that's an invalid input. Try again. Type !usage for more info.".format(message.author.id)
    if len(cmd) > 0:
      get_prefix = cmd[0]
      if prefix == get_prefix:
          total_coins_needed = 0
          total_frags_owned = 0
          total_frags_needed = 0
          frags = []
          try:
              if cmd[1:5] == "wep=":
                  frags = cmd[5:]        
                  if len(frags) > 0:
                    frags = frags.strip()
                  else:
                    frags = "0 0 0"
                  print(frags)
                  frags = [int(frag.strip()) for frag in frags.split(" ")]
                  
                  i = len(frags)
                  if(i > 3):
                    return await channel.send(err_msg)
                  while(i < 3):
                      frags.append(0)
                      i+=1
                      
                  print("Calculating weapon coins...")
                  for frag_count in frags:
                    if frag_count < 0:
                      return await channel.send(err_msg)
                    if frag_count > 900:
                      frag_count = 900
                    total_frags_owned+=frag_count
                  
                  total_frags_needed = wep_frags_to_pink - total_frags_owned
                  total_coins_needed = wep_coins_cost * total_frags_needed
                  total_coins_needed = get_coins_with_comma(total_coins_needed)  
                  print("Done calculating coins for weapon.")
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink weapon.".format(message.author.id, total_coins_needed)
                  await channel.send(msg)
                  
              elif cmd[1:7] == "armor=":
                  frags = cmd[7:]
                  if len(frags) > 0:
                    frags = frags.strip()
                  else:
                    frags = "0 0 0"
                  print(frags)
                  frags = [int(frag.strip()) for frag in frags.split(" ")]
                  if(len(frags) > 4):
                    return await channel.send(err_msg)
                  i = 0
                  print("Calculating weapon coins...")
                  while(i < len(frags)):
                    frag = frags[i]
                    if frag < 0:
                      return await channel.send(err_msg)
                    if frag > 240:
                      frag = 240
                    total_coins_needed+= (240 - frag) * armor_cost[i]
                    i+=1
                      
                  total_coins_needed = get_coins_with_comma(total_coins_needed) 
                  print("Done calculating coins for armor.")
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink armor.".format(message.author.id, total_coins_needed)
                  await channel.send(msg)

              elif cmd[1:6] == "usage":
                msg = "This bot takes in the fragments you have and calculates for the number of coins you might need to craft your pink gear. Also, k, d, n, and r, g, b, m represents the first letter of each wb.\nCommands:= (!wep=k d n for weapon or !armor=r g b m for armor coins calculation)."
                await channel.send(msg)
                  
              else:
                  return
          except:
            await channel.send(err_msg)
              
        
    
def get_coins_with_comma(total_coins_needed):
    total_coins_needed = str(total_coins_needed)
    i = len(total_coins_needed) - 1
    with_comma = ""
    j = 0
    while(i >= 0):
        if(j == 3):
            with_comma = "," + with_comma
            j = 0
        with_comma = total_coins_needed[i] + with_comma
        j+=1
        i-=1
            
    return with_comma
    #print(cmd)



if __name__ == "__main__":
    keep_alive()
    client.run(token)
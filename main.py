import discord
import os
from itertools import cycle
from keep_bot_alive import keep_alive

client = discord.Client()
token = os.environ.get("BOT_TOKEN")

prefix = "!"
wep_frags_to_pink = 900 * 3
armor_frags_to_pink = 240 * 4
total_hero_legs_to_pink = 480
is_wep = "wep="
is_armor = "armor="
is_pink_hero = "hero_armor="
wep_coins_cost = 920
armor_cost = [1360, 1200, 1040, 1040]
hero_armor_cost = 2320
test = "!wep=300, 435, 678"

status = cycle(['JoyfulNoise | !usage', 'House'])

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
              if cmd[1:5] == is_wep:
                  frags = cmd[5:]        
                  if len(frags) > 0:
                    frags = frags.strip()
                  else:
                    frags = "0 0 0"
                  print(frags)
                  frags = [int(frag.strip()) for frag in frags.split(" ")]
                  
                  i = len(frags)
                  if(i > 3):
                    embedVar = discord.Embed(title="Error!", color=0xff0000)
                    embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                    return await channel.send(embed=embedVar)              
                  while(i < 3):
                      frags.append(0)
                      i+=1
                      
                  print("Calculating weapon coins...")
                  for frag_count in frags:
                    if frag_count < 0:
                      embedVar = discord.Embed(title="Error!", color=0xff0000)
                      embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                      return await channel.send(embed=embedVar) 
                    if frag_count > 900:
                      frag_count = 900
                    total_frags_owned+=frag_count
                  
                  total_frags_needed = wep_frags_to_pink - total_frags_owned
                  total_coins_needed = wep_coins_cost * total_frags_needed
                  total_coins_needed = get_coins_with_comma(total_coins_needed)  
                  print("Done calculating coins for weapon.")
                  res = wep_frags_needed(frags)
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink weapon.\n{2}".format(message.author.id, total_coins_needed, res)
                  embedVar = discord.Embed(title="Black Coins To Pink Gear Calculator", color=0xff748c)
                  embedVar.add_field(name="Weapon calculaton results:", value=msg, inline=False)
                  await channel.send(embed=embedVar)
                  
              elif cmd[1:7] == is_armor:
                  frags = cmd[7:]
                  if len(frags) > 0:
                    frags = frags.strip()
                  else:
                    frags = "0 0 0 0"
                  print(frags)
                  frags = [int(frag.strip()) for frag in frags.split(" ")]
                  if(len(frags) > 4):
                    embedVar = discord.Embed(title="Error!", color=0xff0000)
                    embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                    return await channel.send(embed=embedVar)
                  i = len(frags)
                  while(i < 4):
                    frags.append(0)
                    i+=1
                  i=0
                  print("Calculating armor coins...")
                  while(i < len(frags)):
                    frag = frags[i]
                    if frag < 0:
                      embedVar = discord.Embed(title="Error!", color=0xff0000)
                      embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                      return await channel.send(embed=embedVar)
                    if frag > 240:
                      frag = 240
                    total_coins_needed+= (240 - frag) * armor_cost[i]
                    i+=1
                      
                  total_coins_needed = get_coins_with_comma(total_coins_needed) 
                  print("Done calculating coins for armor.")
                  res = armor_frags_needed(frags)
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink armor.\n{2}".format(message.author.id, total_coins_needed, res)
                  embedVar = discord.Embed(title="Black Coins To Pink Gear Calculator", color=0xff748c)
                  embedVar.add_field(name="Armor calculation results:", value=msg, inline=False)
                  await channel.send(embed=embedVar)
              elif cmd[1:12] == is_pink_hero:
                    frags=cmd[12:]
                    if len(frags) > 0:
                        frags = frags.strip()
                    else:
                        frags = "0"
                    print(frags)
                    frags = [int(frag.strip()) for frag in frags.split(" ")]
                    if(len(frags) > 1):
                        #print(err_msg)
                        embedVar = discord.Embed(title="Error!", color=0xff0000)
                        embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                        return await channel.send(embed=embedVar)
                    i = len(frags)
                    while(i < 1):
                        frags.append(0)
                        i+=1
                    i=0
                    print("Calculating hero legacy armor coins...")
                    while(i < len(frags)):
                        frag = frags[i]
                        if frag < 0:
                            #print(err_msg)
                            embedVar = discord.Embed(title="Error!", color=0xff0000)
                            embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                            return await channel.send(embed=embedVar)
                        if frag > total_hero_legs_to_pink:
                            frag = total_hero_legs_to_pink
                        total_coins_needed+= (total_hero_legs_to_pink * hero_armor_cost) - (frag * hero_armor_cost)
                        i+=1
                        
                    total_coins_needed = get_coins_with_comma(total_coins_needed) 
                    print("Done calculating coins for armor.")
                    msg = "<@{0}>, you need {1} black coins to craft your first/next hero legacy pink armor.".format(message.author.id, total_coins_needed)
                    embedVar = discord.Embed(title="Black Coins To Pink Gear Calculator", color=0xff748c)
                    embedVar.add_field(name="Hero Legacy pink armor calculation results:", value=msg, inline=False)
                    await channel.send(embed=embedVar)
              elif cmd[1:6] == "usage":
                msg = "This bot takes in the fragments you have and calculates for the number of coins you might need to craft your pink gear. Also, k, d, n, and r, g, b, m represents the first letter of each wb.\nCommands:= (!wep=k d n for weapon or !armor=r g b m for armor coins calculation). For hero legacy pink armor crafting, use command:=(!hero_armor=h) where h represents how many hero legacy frags you have on you."
                embedVar = discord.Embed(title="Usage", color=0xff748c)
                embedVar.add_field(name="How to use this bot:", value=msg, inline=False)
                await channel.send(embed=embedVar)
                  
              else:
                  return
          except:
            embedVar = discord.Embed(title="Error!", color=0xff0000)
            embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
            await channel.send(embed=embedVar)
              
        
    
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

def wep_frags_needed(frags):
    max_frag = 900
    wb = ["k", "d", "n"]
    res = ""
    c = 0
    for frag in frags:
        if frag > max_frag:
            frag = max_frag
        frags_to_obtain = max_frag - frag
        coins = get_coins_with_comma(frags_to_obtain * wep_coins_cost)
        
        res += "{0}: You need {1} frags more. Coins needed to buy exact frags = {2}\n".format(wb[c], frags_to_obtain, coins)
        c+=1
    return res


def armor_frags_needed(frags):
    max_frag = 240
    wb = ["r", "g", "b", "m"]
    res = ""
    c = 0
    for frag in frags:
        if frag > max_frag:
            frag = max_frag
        frags_to_obtain = max_frag - frag
        coins = get_coins_with_comma(frags_to_obtain * armor_cost[c])
        
        res += "{0}: You need {1} frags more. Coins needed to buy exact frags = {2}\n".format(wb[c], frags_to_obtain, coins)
        c+=1
    return res


if __name__ == "__main__":
    keep_alive()
    client.run(token)
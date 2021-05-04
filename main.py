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
gear = ["Weapon","Sub Weapon","Armor/Hero","Helmet","Gloves/Shoes"]
gear_dc = ["Weapon/Sub","Armor","Helmet","Gloves/Shoes", "Hero Legacy"]
gear_dc_total = [138000, 54400, 48000, 41600, 51040]
red_gear_frags = [150, 40, 40, 40, 22]
dim_frags = [25, 18, 20, 15, 12]
dim_cost = 2500
dim_for_chaos = 600
dim_for_all_chaos = 3600

status = cycle(['BdmGears | !usage', 'House'])

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
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink weapon.\n{2}\nMy Fame Code: AMWYKX73CT5S.".format(message.author.id, total_coins_needed, res)
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
                  msg = "<@{0}>, you need {1} black coins to craft your first/next pink armor.\n{2}\nMy Fame Code: AMWYKX73CT5S.".format(message.author.id, total_coins_needed, res)
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
                    msg = "<@{0}>, you need {1} black coins to craft your first/next hero legacy pink armor.\nMy Fame Code: AMWYKX73CT5S.".format(message.author.id, total_coins_needed)
                    embedVar = discord.Embed(title="Black Coins To Pink Gear Calculator", color=0xff748c)
                    embedVar.add_field(name="Hero Legacy pink armor calculation results:", value=msg, inline=False)
                    await channel.send(embed=embedVar)
              
              elif cmd[1:9] == "dim_wep=":
                str_frags = cmd[9:]
                gear_type = "Weapon"
                needed_frags= 150
                i = 0
                horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                embedVar = discord.Embed(title="Weapon Frags to Dim", color=0xff748c)
                embedVar.add_field(name="Results", value=horizon, inline=False)
                await channel.send(embed=embedVar)
              
              elif cmd[1:11] == "dim_armor=":
                  str_frags = cmd[11:]
                  gear_type = "Armor"
                  needed_frags= 40
                  i = 2
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  print(horizon)
                  embedVar = discord.Embed(title="Armor Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:9] == "dim_sub=":
                  str_frags = cmd[9:]
                  gear_type = "Sub Weapon"
                  needed_frags= 150
                  i = 1
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  #print(horizon)
                  embedVar = discord.Embed(title="Sub Weapon Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:12] == "dim_helmet=":
                  str_frags = cmd[12:]
                  gear_type = "Helmet"
                  needed_frags= 40
                  i = 3
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  #print(horizon)
                  embedVar = discord.Embed(title="Helmet Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:12] == "dim_gloves=":
                  str_frags = cmd[12:]
                  gear_type = "Gloves"
                  needed_frags= 40
                  i = 4
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  #print(horizon)
                  embedVar = discord.Embed(title="Glove Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:11] == "dim_shoes=":
                  str_frags = cmd[11:]
                  gear_type = "Shoes"
                  needed_frags= 40
                  i = 4
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  #print(horizon)
                  embedVar = discord.Embed(title="Shoe Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:10] == "dim_hero=":
                  str_frags = cmd[10:]
                  gear_type = "Hero Legacy"
                  needed_frags= 22
                  i = 2
                  horizon = gear_frags_to_dim(str_frags, gear_type, needed_frags, i)
                  #print(horizon)
                  embedVar = discord.Embed(title="Hero Legacy Frags to Dim", color=0xff748c)
                  embedVar.add_field(name="Results:", value=horizon, inline=False)
                  await channel.send(embed=embedVar) 
              
              elif cmd[1:5] == "gtdc":
                  x = 44
                  #11
                  horizon= "```"
                  horizon += " " + "-"*x + "\n"
                  horizon += "| Gear         | No. of Frags | Total Dc     |\n"
                  horizon += " " + "-"*x + "\n"
                  i = 0
                  while i < len(gear_dc):
                      gd = gear_dc[i]
                      gdt = get_coins_with_comma(gear_dc_total[i])
                      num_frags = str(red_gear_frags[i])
                      horizon += "| {0}{1}| {2}{3}| {4}{5}|\n".format(gd, " "*(13-len(gd)),
                      num_frags, " "*(13-len(num_frags)), gdt, " "*(13-len(gdt)))
                      i+=1
                  horizon += " " + "-"*x + "\n"
                  horizon += "```"
                  #print(horizon) 
                  embedVar = discord.Embed(title="Gear Frags and Dc Table", color=0xff748c)
                  embedVar.add_field(name="Table", value=horizon, inline=False)
                  await channel.send(embed=embedVar)  
                
              elif cmd[1:5] == "dim=":
                  gears = cmd[5:]
                  num_of_gears_arr = [int(gear.strip()) for gear in gears.split(" ")]
                  i = len(num_of_gears_arr)                    
                  dim_frags_amount = []
                  while i < len(gear):
                      num_of_gears_arr.append(0)
                      i+=1                    
                  i = 0                    
                  total = 0
                  while i < len(gear):
                      amount = num_of_gears_arr[i] * dim_frags[i]
                      total+=amount
                      dim_frags_amount.append(amount)
                      i+=1
                  x = 45
                  #11
                  # !dim=2 3 4
                  horizon = "```"
                  horizon += " " + "-"*x + "\n"
                  horizon += "| Gear         | No. of Gears | Frags        |\n"
                  horizon += " " + "-"*x + "\n"
                  i = 0
                  while i < len(gear):
                      g_w = gear[i]
                      num_g = str(num_of_gears_arr[i])
                      d_f = str(dim_frags_amount[i])
                      horizon += "| {0}{1}| {2}{3}| {4}{5}|\n".format(g_w, " "*(13-len(g_w)), num_g, " "*(13-len(num_g)), d_f, " "*(13-len(d_f)))
                      i+=1
                  horizon += " " + "-"*x + "\n"
                  horizon+=" You can obtain up to {0} dimentional fragments.\n".format(total)
                  horizon += "```"
                  #print(horizon)
                  embedVar = discord.Embed(title="Gears to Dim Frags", color=0xff748c)
                  embedVar.add_field(name="Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)

              elif cmd[1:4] == "dim":
                  #print(cmd[4])
                  n_dim = cmd[1:]
                  if len(n_dim) > 3:
                      #print(err_msg)
                      embedVar = discord.Embed(title="Error!", color=0xff0000)
                      embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
                      return await channel.send(embed=embedVar)
                  x = 29
                  #11
                  horizon = "```"
                  horizon += " " + "-"*x + "\n"
                  horizon += "| Gear         | Frags        |\n"
                  horizon += " " + "-"*x + "\n"
                  
                  i = 0
                  
                  while i < len(gear):
                      g_w = gear[i]
                      d_f = str(dim_frags[i])
                      horizon += "| {0}{1}| {2}{3}|\n".format(g_w, " "*(13-len(g_w)), d_f, " "*(13-len(d_f)))
                      i+=1
                  horizon += " " + "-"*x + "\n"
                  horizon += "```"
                  #print(horizon)
                  embedVar = discord.Embed(title="Dim Table", color=0xff748c)
                  embedVar.add_field(name="Gear and Dim Frags Table", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:7] == "chaos=":
                  str_dim_frags_owned = cmd[7:]
                  dim_frags_owned = int(str_dim_frags_owned)
                  if dim_frags_owned > dim_for_chaos:
                      dim_frags_owned = dim_for_chaos
                  
                  amount_in_need = dim_for_chaos - dim_frags_owned
                  if amount_in_need == 0:
                    msg="Congrats! You have the required dimentional fragments to make your first/next chaos gear."
                    embedVar = discord.Embed(title="Chaos Gear", color=0xff748c)
                    embedVar.add_field(name="Dc to Dim - Results", value=msg, inline=False)
                    await channel.send(embed=embedVar)
                    #print("Congrats! You have the required dimentional fragments to make your first/next chaos gear.")
                    return
                  else:
                    dc_need = amount_in_need * dim_cost
                    dc_need = get_coins_with_comma(dc_need)
                  gear_type = "Chaos"
                  horizon = dim_to_chaos(gear_type, str_dim_frags_owned, str(amount_in_need), str(dc_need))
                  #print(horizon)
                  embedVar = discord.Embed(title="Chaos Gear", color=0xff748c)
                  embedVar.add_field(name="Dc to Dim - Results", value=horizon, inline=False)
                  await channel.send(embed=embedVar)
              
              elif cmd[1:11] == "all_chaos=":
                str_dim_frags_owned = cmd[11:]
                dim_frags_owned = int(str_dim_frags_owned)
                if dim_frags_owned > dim_for_all_chaos:
                    dim_frags_owned = dim_for_all_chaos
                
                amount_in_need = dim_for_all_chaos - dim_frags_owned
                if amount_in_need == 0:
                  msg="Congrats! You have the required dimentional fragments to make all your chaos gears."
                  embedVar = discord.Embed(title="All Chaos Gear", color=0xff748c)
                  embedVar.add_field(name="Dc to Dim - Results", value=msg, inline=False)
                  await channel.send(embed=embedVar)
                    #print("Congrats! You have the required dimentional fragments to make all your chaos gears.")
                  return
                else:
                    dc_need = amount_in_need * dim_cost
                    dc_need = get_coins_with_comma(dc_need)
                gear_type = "All Chaos"
                horizon = dim_to_chaos(gear_type, str_dim_frags_owned, str(amount_in_need), str(dc_need))
                #print(horizon)
                embedVar = discord.Embed(title="All Chaos Gear", color=0xff748c)
                embedVar.add_field(name="Dc to Dim - Results", value=horizon, inline=False)
                await channel.send(embed=embedVar)
              
              elif cmd[1:6] == "usage":
                msg = "Craft your pink and chaos gear. k, d, n, and r, g, b, m are the first letter of each wb.\nCommands:\n```!wep= k d n \n!armor=r g b m\n!hero_armor=h```\n```!dim\nThis is a gear and dim frag table.```\n```!dim=w s a/h h g\nTakes in the number or red gears you have respectively and tells you how many dim frags you can get after feeding them to the bs.```\n```!chaos=\nTakes the amount of dim frags you have and tells you how many black coins you might need.\n!all_chaos=\nSame as the previous command, but this only works if you want to craft all 6 chaos gears at once.```\n```!dim_wep=\n!dim_armor=\n!dim_sub=\n!dim_helmet=\n!dim_gloves=\n!dim_shoes=\n!dim_hero=\nThe above takes in their respective number of wb frags you have and tells you how many dim frags you might get from it after crafting a red and feeding them to bs.```\n```!gtdc\nThis is a table that tells you the total amount of dc needed per red. Optimize the usage of your dc with this.```\n\nMy Fame Code: AMWYKX73CT5S."
                embedVar = discord.Embed(title="Usage", color=0xff748c)
                embedVar.add_field(name="How to use this bot", value=msg, inline=False)
                await channel.send(embed=embedVar)
                  
              else:
                  return
          except Exception as e:
            print(e)
            embedVar = discord.Embed(title="Error!", color=0xff0000)
            embedVar.add_field(name="Read error description...", value=err_msg, inline=False)
            await channel.send(embed=embedVar)
              
def dim_to_chaos(gear_type, dim_owned, dim_need, dc_need):
    x = 46
    #11
    dim_owned = get_coins_with_comma(dim_owned)
    horizon = "```"
    horizon += " " + "-"*x + "\n"
    horizon += "| Gear     | Owned  | Need   | Total Dc Needed |\n"
    horizon += " " + "-"*x + "\n"
    horizon += "| {0}{1}| {2}{3}| {4}{5}| {6}{7}|\n".format(gear_type, " "*(9-len(gear_type)),
        dim_owned, " "*(7-len(dim_owned)), dim_need, " "*(7-len(dim_need)),  dc_need, " "*(16-len(dc_need)) )
    horizon += " " + "-"*x + "\n"
    horizon += "```"
    return horizon

def gear_frags_to_dim(str_frags, gear_type, needed_frags, i):
    frags = int(str_frags.strip())
    dim_to_get = (frags/needed_frags) * dim_frags[i]
    dim_to_get = int(dim_to_get)
    dim_to_get = str(dim_to_get)
    x = 53
    #11
    horizon = "```"
    horizon += " " + "-"*x + "\n"
    horizon += "| Gear            | No. of Frags    | Total Dim Frags |\n"
    horizon += " " + "-"*x + "\n"
    horizon += "| {0}{1}| {2}{3}| {4}{5}|\n".format(gear_type, " "*(16-len(gear_type)),
        str_frags, " "*(16-len(str_frags)), dim_to_get, " "*(16-len(dim_to_get)))
    horizon += " " + "-"*x + "\n"
    horizon +="```"

    return horizon        
    
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

# coding: utf-8

# In[ ]:


import discord
import asyncio
from riotwatcher import RiotWatcher
from requests import HTTPError
from bs4 import BeautifulSoup
from requests import get
import sys
watcher = RiotWatcher('//token here')
my_region = 'na1'


client = discord.Client()
token = '//token here'
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
           
    
    if message.content.startswith('!LP'):
        name = message.content.strip("!LP")
        try:
            me = watcher.summoner.by_name(my_region, name)
            my_ranked_stats = watcher.league.positions_by_summoner(my_region, me['id'])
            lp = str(my_ranked_stats[0]['leaguePoints'])
            await client.send_message(message.channel, my_ranked_stats[0]['tier'] + " " + my_ranked_stats[0]['rank']+  " " + lp)
        except HTTPError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(e.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                await client.send_message(message.channel, 'Summoner with that name not found.')
            else:
                raise
    elif message.content.startswith('!ADCIN2018'): 
        await client.send_message(message.channel, 'L O L')
    elif message.content.startswith('!Lolcounter'): 
        champ = message.content.replace('!Lolcounter', '').capitalize()
        first_time = True
        url = 'https://lolcounter.com/champions/' + champ
        champ_no = 0
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        type(html_soup)
        soup = html_soup
        await client.send_message(message.channel, champ + " is weak against: ")
        for weak_champs in soup.find_all('div', attrs={'class': 'weak-block'}):
            weak_champs_descendants = weak_champs.descendants
            for champs in weak_champs_descendants:
                if champs.name == 'div' and champs.get('class', '') == ['champ-block'] and champ_no < 6:
                    champ_no += 1
                    await client.send_message(message.channel, champs.text.split('\n')[3])
        champ_no = 0
        await client.send_message(message.channel, '\n'+ champ + " is strong against: ")
        for strong_champs in soup.find_all('div', attrs={'class': 'strong-block'}):
            strong_champs_descendants = strong_champs.descendants
            for champs in strong_champs_descendants:
                if champs.name == 'div' and champs.get('class', '') == ['champ-block'] and champ_no < 6:
                    champ_no += 1
                    await client.send_message(message.channel, champs.text.split('\n')[3])
    elif message.content.startswith('!Probuilds'): 
            champ = message.content.replace('!Probuilds', '')
            champ = champ.strip(" ")
            item_list = []
            item_pics = []
            count = 0
            url = 'https://www.probuilds.net/champions/details/' + champ
            champ_no = 0
            response = get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser') #Organizes the soup
            type(html_soup)
            soup = html_soup
            for i in soup.find_all('div', attrs={'class': 'popular-section'}): #Searches for the popular items
                bigData = i.descendants
                for j in bigData:
                    if j.name == 'div' and j.get('class', '') == ['bigData']: #Gets the "bigData" which means the pop items
                        item_list.append(j.text.split("\n")[5]) #Removes spaces and gets item name
            for i in soup.find_all('div', attrs={'class': 'item tooltip'}): #Gets the image link
                item_pics.append(str(i.img).strip("\""))
            while '' in item_list : item_list.remove('')
            await client.send_message(message.channel, ("Items:"))
            for item in item_list[0:6]:
                print_state = item + " " + item_pics[count][17+len(item):81+len(item)]
                await client.send_message(message.channel, print_state)
                count += 1
            await client.send_message(message.channel, "Summoners:")
            for item in item_list[6:10]:
                if item == 'Ignite':
                    print_state = item + " " + item_pics[count][17+len(item):83+len(item)+len(item)]
                elif item == 'Cleanse':
                    print_state = item + " " + item_pics[count][17+len(item):84+len(item)+len(item)]
                else:
                    print_state = item + " " + item_pics[count][17+len(item):86+len(item)+len(item)]
                await client.send_message(message.channel, print_state)
                count += 1
            await client.send_message(message.channel, ("Boots:"))
            for item in item_list[10:]:
                print_state = item + " " + item_pics[count][17+len(item):81+len(item)] 
                await client.send_message(message.channel, print_state)
                count += 1
            
    elif message.content.startswith('!Suicide'):
        await client.send_message(message.channel, 'Mr.Stark.... I don\'t feel so good...')
        await client.logout()
        
        
                    

client.run(token)


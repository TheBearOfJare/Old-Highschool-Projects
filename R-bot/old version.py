import discord
import pnwkit
import requests
import random
import time
import datetime

key = '51f2058772e1cb'

#data = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {500} max_score: {1000} vmode: false color: "gray" alliance_position: 1) {{ data {{id, last_active, alliance_id, wars {{defid}} }} }} }}''').json()

#print(data['data']['nations']['data'][0]['wars'])


applicant = False
update = False
user = 0
score = 0

client = discord.Client()

prices = [0,0,0,0,0,0,0]

pnwkit.set_key(key)


slotted = []
users = []

##cities = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id:{i},first:1){{data{{nation_name,cities{{coalmine oilwell uramine farm leadmine ironmine bauxitemine}}}}}}}}""").json()
##
##print(cities)
#city = pnwkit.city_query({'id': str(423112)}, "coalmine")
#city = pnwkit.city_query({"id": str(423112)}, "coalmine oilwell uramine farm leadmine ironmine bauxitemine")[0]
#player = pnwkit.nation_query({"discord": str(user)}, "id")
#print(city)

async def raid(message,wars,DM):
        global applicant
        t = time.perf_counter()
        values = []
        global prices

        await message.channel.send('Finding optimal targets')
        
        try:
                player = pnwkit.nation_query({"discord": str(user)}, "id")[0]

        except Exception:
                        await message.channel.send(f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}")
                        return
        
        player = list(str(player))
        del player[:9]
        player = ''.join(player)

        score = requests.post(f"http://politicsandwar.com/api/nation/id={player}/&key={key}")
        score = score.json()

        if 6-score['offensivewars'] < wars:
                
                await message.channel.send(f'You requested more targets than you need...\nFinding you {6-score["offensivewars"]} targets instaid of {wars}.')
                wars = 6-score['offensivewars']
                if wars == 0:
                        await message.channel.send("lol zero wars left.\nEnjoy what you already have in life")
                        return

        battles = score['offensivewar_ids']

        count = 0
        for i in battles:
                if len(battles) == 0:
                        break
                battles[count] = requests.post(f"https://politicsandwar.com/api/war/{i}/&key={key}").json()
                battles[count] = battles[count]['war'][0]['defender_id']
                count+=1

        score = score['score']

        range = [(float(score) * 0.75), (float(score) * 1.75)]

        await message.channel.send('...')
        if applicant == False:
            data = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false color: "gray" alliance_position: 0) {{ data {{id,  last_active, wars {{defid, def_resistance, turnsleft, defpeace}} }} }} }}''').json()
        else:
            #data = requests.post(f"https://politicsandwar.com/api/v2/nations/{key}/&color=gray&min_score={str(range[0])}&max_score={str(range[1])}&alliance_position=1&v_mode=0").json()
            data = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false color: "gray" alliance_position: 1) {{ data {{id,  last_active, alliance_id, wars {{defid, def_resistance, turnsleft, defpeace}} }} }} }}''').json()
			
            alliances = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{alliances(orderBy: {{column: SCORE order: DESC}}, first: 50) {{ data{{ id }} }} }}""").json()
			
			
        length = len(data['data']['nations']['data'])

        if length == 0:
                await message.channel.send('Bummer, there are no inactive raid targets currently availible within your war range :(')
                print(score)
                return

        targets = []
        i = 0
        while i < length:
                inactive = data['data']['nations']['data'][i]['last_active']
                inactive = list(str(inactive))
                inactive = datetime.datetime.strptime(str(inactive[5])+str(inactive[6])+'/'+str(inactive[8])+str(inactive[9])+'/'+str(inactive[2])+str(inactive[3]),'%x')
                inactive = datetime.datetime.now()-inactive
                inactive = (((inactive.total_seconds())/60)/60)/24
                
                if applicant == True:
                        alliance = int(data['data']['nations']['data'][i]['alliance_id'])

                        x = 0
                        while x < len(alliances['data']['alliances']['data']):
                                if int(alliances['data']['alliances']['data'][x]['id']) == alliance:
                                        #print(f"{alliance} : {alliances['data']['alliances']['data'][x]['id']}")
                                        del data['data']['nations']['data'][i]
                                        i = 0
                                        length = len(data['data']['nations']['data'])
                                        break
                                x+=1

                def_wars = 0
                x = 0
                test = data['data']['nations']['data'][i]['id']
                while x < len(data['data']['nations']['data'][i]['wars']):
                    if data['data']['nations']['data'][i]['wars'][x]['defid'] == test and data['data']['nations']['data'][i]['wars'][x]['turnsleft'] > 0:
                            def_wars+=1
						
                    if def_wars > 2:
                        del data['data']['nations']['data'][i]
                        i = 0
                        length = len(data['data']['nations']['data'])
                        break
                    x+=1
                    if length == 0:
                        break
                    
                if inactive < 30:
                    del data['data']['nations']['data'][i]
                    i = 0
                    length = len(data['data']['nations']['data'])
                    if length == 0:
                        break
                
                if str(data['data']['nations']['data'][i]['id']) in battles or data['data']['nations']['data'][i]['id'] in slotted:
                    del data['data']['nations']['data'][i]
                    i = 0
                    length = len(data['data']['nations']['data'])
                    if length == 0:
                        break
                else:
                        i+=1

        length = len(data['data']['nations']['data'])
        if length == 0:
                await message.channel.send('Bummer, there are no inactive raid targets currently availible within your war range :(')
                print(score)
                return

        targets = []
        i = 0
        while i < length:
                targets.append(data['data']['nations']['data'][i]['id'])
                i+=1

        random.shuffle(targets)
        targets = targets[:round(min((6+(6*wars)+(1500/float(score))),60))]
        print(f'Scanning {len(targets)} targets')
        for i in targets:
                value = 0
                cities = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id:{i},first:1){{data{{cities{{coalmine oilwell uramine farm leadmine ironmine bauxitemine}}}}}}}}""").json()

                cities = cities['data']['nations']['data'][0]['cities']

                i = 0
                while i < len(cities):
                        city = cities[i]
                        value = round(value + ((int(city['coalmine'])*prices[2])+(int(city['oilwell'])*prices[3])+(int(city['uramine'])*prices[5])+(int(city['farm'])*prices[0])+(int(city['leadmine'])*prices[4])+(int(city['ironmine'])*prices[1])+(int(city['bauxitemine'])*prices[6]))/1000,2)
                        i+=1
                #cities = pnwkit.city_query({"first": 50, "page": 1, "nation_id": [i]}, """
        #coalmine
        #oilwell
        #uramine
        #farm
        #leadmine
        #ironmine
        #bauxitemine
        #""")[0]

                #print(cities)
                #values.append(cities['coalmine']+cities['oilwell']+cities['uramine']+cities['farm']+cities['leadmine']+cities['ironmine']+cities['bauxitemine'])
##
##                target = requests.post(f"http://politicsandwar.com/api/nation/id={i}/&key={key}")
##                target = target.json()
##                cities = target['cityids']
##                target = i
##
##                value = 0
##                for x in cities:
##
##                        city = pnwkit.city_query({"first": 50, "page": 1, "id": [int(x)]}, """
##        coalmine
##        oilwell
##        uramine
##        farm
##        leadmine
##        ironmine
##        bauxitemine
##        """)[0]

##                        value = round(value + ((int(city['coalmine'])*prices[2])+(int(city['oilwell'])*prices[3])+(int(city['uramine'])*prices[5])+(int(city['farm'])*prices[0])+(int(city['leadmine'])*prices[4])+(int(city['ironmine'])*prices[1])+(int(city['bauxitemine'])*prices[6]))/1000,2)

                        #city = requests.post(f"http://politicsandwar.com/api/city/id={x}&key={key}")
                        #city = city.json()

                        #value = value+int(city['imp_coalmine'])+int(city['imp_oilwell'])+int(city['imp_ironmine'])+int(city['imp_bauxitemine'])+int(city['imp_leadmine'])+int(city['imp_uramine'])+int(city['imp_farm'])

                values.append(value)

        i = 0
        best = [0,0,0,0,0,0]
        target = [0,0,0,0,0,0]
        length = len(targets)

        while i < length:
                test = values[i]
                if test > best[0]:
                        target[5] = target[4]
                        target[4] = target[3]
                        target[3] = target[2]
                        target[2] = target[1]
                        target[1] = target[0]
                        best[5] = best[4]
                        best[4] = best[3]
                        best[3] = best[2]
                        best[2] = best[1]
                        best[1] = best[0]


                        target[0] = targets[i]
                        best[0] = test

                        i+=1
                        continue
                if test > best[1]:
                        target[5] = target[4]
                        target[4] = target[3]
                        target[3] = target[2]
                        target[2] = target[1]
                        best[5] = best[4]
                        best[4] = best[3]
                        best[3] = best[2]
                        best[2] = best[1]

                        target[1] = targets[i]
                        best[1] = test
                        i+=1
                        continue
                if test > best[2]:
                        target[5] = target[4]
                        target[4] = target[3]
                        target[3] = target[2]
                        best[5] = best[4]
                        best[4] = best[3]
                        best[3] = best[2]

                        target[2] = targets[i]
                        best[2] = test
                        i+=1
                        continue
                if test > best[3]:
                        target[5] = target[4]
                        target[4] = target[3]
                        best[5] = best[4]
                        best[4] = best[3]

                        target[3] = targets[i]
                        best[3] = test
                        i+=1
                        continue
                if test > best[4]:
                        target[5] = target[4]
                        best[5] = best[4]

                        target[4] = targets[i]
                        best[4] = test
                        i+=1
                        continue
                if test > best[5]:
                        target[5] = targets[i]
                        best[5] = test
                        i+=1
                else:
                        i+=1

        print(best)
        if wars == 1:
                if DM == False:
                        if best[0] < 100 and best[0] > 0:
                                await message.channel.send("(Not that great)")
                                print(score)
							
                        if best[0] == 0:
                                await message.channel.send("Could not find a good enough target to satisfy your request :(\nperhaps your nation score is a bit too high?")
                        else:
                                await message.channel.send(f'Target aquired:\nhttps://politicsandwar.com/nation/id={target[0]}')

                        await message.channel.send(f'({round(time.perf_counter()-t,1)}s)\n{message.author.mention}')
                        return
                else:
                        try: 
                                if best[0] < 100:
                                        await user.send("(Not that great)")
                                        print(score)
                                await user.send(f'Target aquired:\nhttps://politicsandwar.com/nation/id={target[0]}')
                                await user.send(f'({round(time.perf_counter()-t,1)}s)')
                                await message.channel.send("Complete")
                        except Exception:
                                await message.channel.send(f"Failed to send because {user} had DMs disabled or something... ¯\_(ツ)_/¯\n{message.author.mention}")
                        return
        else:
                if DM == False:
                        await message.channel.send('Targets aquired:')
                        i = 0
                        while i < wars and best[i] > 0:
                                await message.channel.send(f'https://politicsandwar.com/nation/id={target[i]}')
                                i+=1
                                if best[i] < 100:
                                        await message.channel.send("(Not that great)")
                                        print(score)
                        if i < wars:
                                await message.channel.send("Could not find enough good targets to satisfy your request :(\nperhaps your nation score is a bit too high?")
                                        
                        await message.channel.send(f'({round(time.perf_counter()-t,1)}s)\n{message.author.mention}')
                        return
                else:
                        try:
                                await user.send('Targets aquired:')
                                i = 0
                                while i < wars and best[i] > 0:
                                        await user.send(f'https://politicsandwar.com/nation/id={target[i]}')
                                        i+=1
                                        if best[i] < 100:
                                                await user.send("(Not that great)")
                                                print(score)

                                if i < wars:
                                        await user.send("Could not find enough good targets to satisfy your request :(\nperhaps your nation score is a bit too high?")
                                await user.send(f'({round(time.perf_counter()-t,1)}s)\n{message.author.mention}')
                                await message.channel.send("Complete")
                        except Exception:
                                await message.channel.send(f"Failed to send because {user} had DMs disabled or something... ¯\_(ツ)_/¯\n{message.author.mention}")
                        return



async def help(message):
        await message.channel.send("**Commands:**\n`%raid` - finds a singular, inactive, optimal, alliance non-member raid target within your war range. Targets are selected for their high resource count.\n**NOTE:** `%raid` does **not** (yet) take commerce or manufacturing builds into account; *it assumes that all cities are unpowered*.\nAdd a number (2-6) to the end for two or more raid targets (this is faster and more efficent than requesting each target individualy).\nEX: `%raid4`\n`%DM` - same as `%raid` but it DMs you instaid of publicly posting results. `%DM3` is a thing too.\n`%range` - finds your war range.\nRumor has it that there is another, secret command burried in this *raid* bot's *shadowy* depths of *legendary* code.")
        return

async def legendary(message):
        await message.channel.send("ThIs wAr iS sPOnSoREd bY **RAID: Shadow Legends**.",delete_after=20)
        time.sleep(3)
        await message.channel.send("\nShADow LEgeNdS iS a BRanD nEw imMErSiVe RPG tItlE wITh hOUrs oF coNtEnT, anD thRIlLiNg gAMePlaY.",delete_after=20)
        time.sleep(2)
        await message.channel.send("It'S GOt aN AmAziNg sTorYLiNe, aWEsOme 3D GRaPhIcs, gIAnt boSs fIGhTs, PVP baTTlEs, aNd hUnDReDs oF chAmPIoNs yOU cAn CoLlECt aNd cUStOmiZe.",delete_after=20)
        time.sleep(4)
        await message.channel.send(f"\nChEcK ouT RAID tODay aNd uSE tHe coDe: {'BORB'} tO gEt 50,000 SiLVer aNd a FREE LeGeNDarY ChAMpIon.",delete_after=20)
        time.sleep(9)
        await message.channel.send("`Downloading RAID: Shadow Legends...`",delete_after=12)
        time.sleep(3)
        await message.channel.send("`...`",delete_after=12)
        time.sleep(3)
        await message.channel.send("`Finished.\nYour device is now infected with RAID: Shadow Legends`",delete_after=12)
        return


@client.event
async def on_ready():
        print("Online")
        global prices
        prices = [requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=food&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=iron&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=coal&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=oil&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=lead&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=uranium&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=bauxite&key={key}")]

        i = 0
        while i <= 6:
                prices[i] = prices[i].json()
                prices[i] = int(prices[i]['avgprice'])
                i+=1



@client.event
async def on_message(message):

	global applicant
	global slotted
	if message.author == client.user:
		return

	global user
	global name

	name = message.author.id
	try:
		user = await client.fetch_user(name)
	except Exception:
		return       
	
	timestamp = datetime.datetime.now()
	timestamp = timestamp.strftime("%M")
	
	if timestamp == "01" and update == True:
		global prices
		prices = [requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=food&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=iron&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=coal&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=oil&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=lead&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=uranium&key={key}"),requests.post(f"http://politicsandwar.com/api/tradeprice/?resource=bauxite&key={key}")]
		count = 0
		newlist = slotted.copy()

		for s in slotted:
				if requests.post(f"http://politicsandwar.com/api/nation/id={s}/&key={key}").json()['defensivewars'] != 3:
					recipeint = users[count]
					print('Target availible')
					await recipeint.send(f'https://politicsandwar.com/nation/id={s}\nNow properly availible with an open war slot.')
					del users[count]
					del newlist[count]
				count+=1
		slotted = newlist
		print(slotted)
		
		i = 0
		while i <= 6:
			prices[i] = prices[i].json()
			prices[i] = int(prices[i]['avgprice'])
			i+=1
			
	if message.content==('%range'):
		try:
			player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
			
		except Exception:
			await message.channel.send(f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}")
			return
	
		player = list(str(player))
		del player[:9]
		player = ''.join(player)

		score = requests.post(f"http://politicsandwar.com/api/nation/id={player}/&key={key}")
		score = score.json()
		score = score['score']
		
		range = [float(score) * 0.75, float(score) * 1.75]
		await message.channel.send('Your War range is '+str(round(range[0],1))+' to '+str(round(range[1],1))+' nation score')
		
	if message.content.startswith('%slotted htt'):
		id = list(message.content)[9:]
		id = id[37:]
		id = ''.join(id)
		slotted.append(id)
		users.append(user)
		print(slotted)
		print(user)
		await message.channel.send('Success.')

	if message.content==('%raid') or message.content==('%raid1'):
		await raid(message,1,False)
	if message.content==('%raid2'):
		await raid(message,2,False)
	if message.content==('%raid3'):
		await raid(message,3,False)
	if message.content==('%raid4'):
		await raid(message,4,False)
	if message.content==('%raid5'):
		await raid(message,5,False)
	if message.content==('%raid6'):
		await raid(message,6,False)
		
	if message.content==('%DM') or message.content==('DM1'):
		await raid(message,1,True)
	if message.content==('%DM2'):
		await raid(message,2,True)
	if message.content==('%DM3'):
		await raid(message,3,True)
	if message.content==('%DM4'):
		await raid(message,4,True)
	if message.content==('%DM5'):
		await raid(message,5,True)
	if message.content==('%DM6'):
		await raid(message,6,True)
		
	if message.content.startswith('%applicant'):
		await message.channel.send('**Use discretion** when attacking inactive applicants. ALL targets *are* inactive for more than 30 days, but you should check to make sure other attackers have not been countered before raiding.')
		if message.content == ('%applicant'):
			global applicant
			applicant = True
			await raid(message,1,False)
		else:
		    data = message.content
		    data = list(data)
		    i = int(data[10])
		    applicant = True
		    await raid(message,i,False)
	else:
		applicant = False
		
	if message.content==('?raid'):
		await help(message)
        
	if message.content==('%raidshadowlegends'):
		await message.delete()
		await legendary(message)

from keep_alive import keep_alive

keep_alive()

client.run('OTU1MzQwNTUwNjU4MjExODUy.YjgQOA.CZH1sxDcWUQrAp8j2tVEbNtCh3A')
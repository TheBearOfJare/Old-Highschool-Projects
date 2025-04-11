import discord
import pnwkit
import requests
import random
import time
import datetime
from replit import db
from keep_alive import keep_alive


key = '51f2058772e1cb'

#data = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {500} max_score: {1000} vmode: false color: "gray" alliance_position: 1) {{ data {{id, last_active, alliance_id, wars {{defid}} }} }} }}''').json()

#print(data['data']['nations']['data'][0]['wars'])

recipient = ''

new = False
applicant = False
update = True
user = 0
score = 0
cata = False
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.messages = True
client = discord.Client(intents=intents)
nope = ''
pirate = False
prices = [0, 0, 0, 0, 0, 0, 0]

pnwkit.set_key(key)


##cities = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id:{i},first:1){{data{{nation_name,cities{{coalmine oilwell uramine farm leadmine ironmine bauxitemine}}}}}}}}""").json()
##
##print(cities)
#city = pnwkit.city_query({'id': str(423112)}, "coalmine")
#city = pnwkit.city_query({"id": str(423112)}, "coalmine oilwell uramine farm leadmine ironmine bauxitemine")[0]
#player = pnwkit.nation_query({"discord": str(user)}, "id")
#print(city)

async def versus(message,type,victory):
	print('stuff')
	
async def wars(message,id):
	global Rchannel
	nation = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{
  nations(id: {id}) {{
	data {{
	  wars {{
		att_id
		att_resistance
		def_resistance
		turns_left
		defender {{
		  nation_name
		  soldiers
		  tanks
		  aircraft
		  ships
		}}
		attacker {{
		  nation_name
		  soldiers
		  tanks
		  aircraft
		  ships
		}}
	  }}
	}}
  }}
}}''').json()['data']['nations']['data'][0]
	for war in nation['wars']:
		if war['turns_left'] <= 0 or war['att_resistance'] <= 0 or war['def_resistance'] <= 0:
			continue
		if war['att_id'] == id:
			defender = war['defender']
			soldiers = defender['soldiers']
			tanks = defender['tanks']
			aircraft = defender['aircraft']
			ships = defender['ships']
			
			await Rchannel.send(f"War with {defender['nation_name']} (you attacked):\nYour resistance: {war['att_resistance']}\n{defender['nation_name']}'s resistance: {war['def_resistance']}\n\nYou:```\n{war['attacker']['soldiers']} soldiers\n{war['attacker']['tanks']} tanks\n{war['attacker']['aircraft']} planes\n{war['attacker']['ships']} ships\n```\n{defender['nation_name']}:\n```{soldiers} soldiers\n{tanks} tanks\n{aircraft} planes\n{ships} ships\n```")
		else:
			attacker = war['attacker']
			soldiers = attacker['soldiers']
			tanks = attacker['tanks']
			aircraft = attacker['aircraft']
			ships = attacker['ships']
			
			await Rchannel.send(f"War with {attacker['nation_name']} ({attacker['nation_name']} attacked you.):\nYour resistance: {war['def_resistance']}\n{attacker['nation_name']}'s resistance: {war['att_resistance']}\n\nYou:```\n{war['defender']['soldiers']} soldiers\n{war['defender']['tanks']} tanks\n{war['defender']['aircraft']} planes\n{war['defender']['ships']} ships\n```\n{attacker['nation_name']}:\n```{soldiers} soldiers\n{tanks} tanks\n{aircraft} planes\n{ships} ships\n```")
						  


@client.event
async def paywall(message,name):
	global Rchannel
	await Rchannel.send('Lol looks like your alliance wants to use this bot, bucko...')
	await Rchannel.send('But guess what...')
	await Rchannel.send("They're gonna have to pay TRIBUTE!!!\nMessage me (https://politicsandwar.com/nation/id=401657) if you want to use the bot and we might be able to nagotiate a price.\nMeanwhile, have fun with this spam")
	try:
		user = await client.fetch_user(name)
	except Exception:
		return

	try:
		await user.send('Pay up, Chump')
		await user.send('https://i.redditmedia.com/3Qu1lAbCvh9BnrE_8ES04VDlPiTjGV6MtwYf0j-Ju1Y.jpg?w=768&s=a40466207b14929189416bc33e139720')
	except Exception:
		return

async def sim(message,type,att1,att2,def1,def2):
	global Rchannel
	fail = 0
	phyric = 0
	moderate = 0
	triumph = 0
	
	if type == 'ground':
		att1 = att1*1.75
		att2 = att2*40
		def1 = def1*1.75
		def2 = def2*40
		
		wins = 0
		attcas1 = 0
		defcas1 = 0
		attcas2 = 0
		defcas2 = 0
			
		for n in range(3):
			x = [att1*random.randrange(30,100)/100, att2*random.randrange(30,100)/100]
			y = [def1*random.randrange(30,100)/100, def1*random.randrange(30,100)/100]
			
			if x[0]+x[1] > y[0]+y[1]:
				attcas2 += (y[0] * 0.0004060606) + (y[1] * 0.00066666666)
				defcas2 += (x[0] * 0.00043225806) + (x[1] * 0.00070967741)
				wins +=1
			else:
				attcas2 += (y[0] * 0.00043225806) + (y[1] * 0.00070967741)
				defcas2 += (x[0] * 0.0004060606) + (x[1] * 0.00066666666)
				
			attcas1 += (y[0] * 0.0084) + (y[1] * 0.0092)
			defcas1 += (x[0] * 0.0084) + (x[1] * 0.0092)
						
		avcas1 = round(attcas1)
		avcas2 = round(attcas2)
		davcas1 = round(defcas1)
		davcas2 = round(defcas2)
		
		for i in range(1000):
			wins = 0
			attcas1 = 0
			defcas1 = 0
			attcas2 = 0
			defcas2 = 0
			
			for n in range(3):
				x = [att1*random.randrange(30,100)/100, att2*random.randrange(30,100)/100]
				y = [def1*random.randrange(30,100)/100, def1*random.randrange(30,100)/100]
			
				if x[0]+x[1] > y[0]+y[1]:
					attcas2 += (y[0] * 0.0004060606) + (y[1] * 0.00066666666)
					defcas2 += (x[0] * 0.00043225806) + (x[1] * 0.00070967741)
					wins +=1
				else:
					attcas2 += (y[0] * 0.00043225806) + (y[1] * 0.00070967741)
					defcas2 += (x[0] * 0.0004060606) + (x[1] * 0.00066666666)
				
				attcas1 += (y[0] * 0.0084) + (y[1] * 0.0092)
				defcas1 += (x[0] * 0.0084) + (x[1] * 0.0092)

			attcas1 = round(attcas1)
			attcas2 = round(attcas2)
			defcas1 = round(defcas1)
			defcas2 = round(defcas2)

			avcas1 = round((avcas1+attcas1)/2)
			avcas2 = round((avcas2+attcas2)/2)
			davcas1 = round((davcas1+defcas1)/2)
			davcas2 = round((davcas2+defcas2)/2)
			
			if wins == 0:
				fail+=1

			if wins == 1:
				phyric+=1

			if wins == 2:
				moderate+=1

			if wins == 3:
				triumph+=1
				
		await Rchannel.send(f'**Results:**\n```\nUtter Failure: {fail/10}%\nPhyric Victory: {phyric/10}%\nModerate Success: {moderate/10}%\nImmense Triumph: {triumph/10}%```\n**Average Casualties:**\n```\nAttacker: {avcas1} soldiers and {avcas2} tanks.\nDefender: {davcas1} soldiers and {davcas2} tanks.```')
	

	if type == 'air':
		attval = att1*3
		defval = def1*3
		wins = 0
		attcas = 0
		defcas = 0
			
		for n in range(3):
			x = attval*random.randrange(30,100)/100
			y = defval*random.randrange(30,100)/100
			attcas += 0.018337*y
			defcas += 0.018337*x
			if x > y:
				wins +=1

		avcas1 = round(attcas)
		avcas2 = round(defcas)
		
		for i in range(1000):
			wins = 0
			attcas = 0
			defcas = 0
			
			for n in range(3):
				x = attval*random.randrange(30,100)/100
				y = defval*random.randrange(30,100)/100
				attcas += 0.018337*y
				defcas += 0.018337*x
				if x > y:
					wins +=1

			attcas = round(attcas)
			defcas = round(defcas)

			avcas1 = round((avcas1+attcas)/2)
			avcas2 = round((avcas2+defcas)/2)
			
			if wins == 0:
				fail+=1

			if wins == 1:
				phyric+=1

			if wins == 2:
				moderate+=1

			if wins == 3:
				triumph+=1
				
		await Rchannel.send(f'**Results:**\n```\nUtter Failure: {fail/10}%\nPhyric Victory: {phyric/10}%\nModerate Success: {moderate/10}%\nImmense Triumph: {triumph/10}%```\n**Average Casualties:**\n```\nAttacker: {avcas1} planes\nDefender: {avcas2} planes```')
		
		return
				
	if type == 'sea':
		attval = att1*4
		defval = def1*4
		wins = 0
		attcas = 0
		defcas = 0
			
		for n in range(3):
			x = attval*random.randrange(30,100)/100
			y = defval*random.randrange(30,100)/100
			attcas += 0.01375*y
			defcas += 0.01375*x
			if x > y:
				wins +=1

		avcas1 = round(attcas)
		avcas2 = round(defcas)
		
		for i in range(1000):
			wins = 0
			attcas = 0
			defcas = 0
			
			for n in range(3):
				x = attval*random.randrange(30,100)/100
				y = defval*random.randrange(30,100)/100
				attcas += 0.01375*y
				defcas += 0.01375*x
				if x > y:
					wins +=1

			attcas = round(attcas)
			defcas = round(defcas)

			avcas1 = round((avcas1+attcas)/2)
			avcas2 = round((avcas2+defcas)/2)
			
			if wins == 0:
				fail+=1

			if wins == 1:
				phyric+=1

			if wins == 2:
				moderate+=1

			if wins == 3:
				triumph+=1
			
		await Rchannel.send(f'**Results:**\n```\nUtter Failure: {fail/10}%\nPhyric Victory: {phyric/10}%\nModerate Success: {moderate/10}%\nImmense Triumph: {triumph/10}%```\n**Average Casualties:**\n```\nAttacker: {avcas1} ships\nDefender: {avcas2} ships```')
		
		return


async def raid(message, wars, DM):
	global recipient
	global applicant
	global cata
	global nope
	global pirate
	global Rchannel
	t = time.perf_counter()
	values = []
	targets = []
	global prices
	slotted = db.keys()
	print(slotted)
	user = await client.fetch_user(recipient)

	MSGauthor = message.author
	try:
		player = pnwkit.nation_query({"discord": str(user)}, "id")[0]

	except Exception:
		await Rchannel.send(
			f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
		)
		return

	player = list(str(player))
	del player[:9]
	player = ''.join(player)

	score = requests.post(
		f"http://politicsandwar.com/api/nation/id={player}/&key={key}")
	score = score.json()

	if 6 - score['offensivewars'] < wars:

		await Rchannel.send(
			f'You requested more targets than you need...\nFinding you {6-score["offensivewars"]} targets instaid of {wars}.'
		)
		wars = 6 - score['offensivewars']
		if wars == 0:
			await Rchannel.send(
				"lol zero wars left.\nEnjoy what you already have in life")
			return

	battles = score['offensivewar_ids']

	count = 0
	for i in battles:
		if len(battles) == 0:
			break
		battles[count] = requests.post(
			f"https://politicsandwar.com/api/war/{i}/&key={key}").json()
		battles[count] = battles[count]['war'][0]['defender_id']
		count += 1

	score = score['score']

	range = [(float(score) * 0.75), (float(score) * 1.75)]

	if applicant == False:
		if cata == True:
			data = requests.get(
				f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false color: "gray" alliance_position: 1 alliance_id: 7452) {{ data {{id,  last_active, wars {{def_id, def_resistance, turns_left, defpeace}} }} }} }}'''
			).json()
		else:
			data = requests.get(
				f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false color: "gray" alliance_position: 0) {{ data {{id,  last_active, wars {{def_id, def_resistance, turns_left, defpeace}} }} }} }}'''
			).json()

	if applicant == True:
		data = requests.get(
			f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false color: "gray" alliance_position: 1) {{ data {{id,  last_active, alliance_id, wars {{def_id, def_resistance, turns_left, defpeace}} }} }} }}'''
		).json()

		alliances = ['1584','790','4729']

	if pirate == True:
		data = requests.get(
			f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{ nations(min_score: {range[0]} max_score: {range[1]} vmode: false) {{ data {{id, last_active, alliance_position, wars {{def_id, def_resistance, turns_left, defpeace}} }} }} }}'''
		).json()
	length = len(data['data']['nations']['data'])

	if length == 0:
		await Rchannel.send(
			'Bummer, there are no inactive raid targets currently availible within your war range :('
		)
		print(score)
		return

	done = False
	targets = []
	i = 0
	while i < length:
		if len(data['data']['nations']['data']) == 0:
			break
		try:
			thingy = data['data']['nations']['data'][i]
		except Exception:
			i+=1
			try:
				thingy = data['data']['nations']['data'][i]
			except Exception:
				done = True

		if done == True:
			break
		inactive = data['data']['nations']['data'][i]['last_active']
		inactive = list(str(inactive))
		inactive = datetime.datetime.strptime(
			str(inactive[5]) + str(inactive[6]) + '/' + str(inactive[8]) +
			str(inactive[9]) + '/' + str(inactive[2]) + str(inactive[3]), '%x')
		inactive = datetime.datetime.now() - inactive
		inactive = (((inactive.total_seconds()) / 60) / 60) / 24

		if applicant == True:
			alliance = str(data['data']['nations']['data'][i]['alliance_id'])
			nogo = []
			for a in alliances:
				nogo.append(str(a))
			
		if applicant == True and str(alliance) in nogo:
			print(f"Applicant {data['data']['nations']['data'][i]['id']} {alliance} in nogo")
			del data['data']['nations']['data'][i]
			continue
			i = 0
			length = len(data['data']['nations']['data'])
				
		defwars = 0
		if str(data['data']['nations']['data'][i]['id']) not in battles and data['data']['nations']['data'][i]['id'] not in slotted and data['data']['nations']['data'][i]['id'] not in nope:
			for war in data['data']['nations']['data'][i]['wars']:
				if war['turns_left'] >= 0 or war['def_resistance'] >= 0:
					defwars += 1
					
			if defwars < 3:
				if new == False and inactive >= 10:
					targets.append(data['data']['nations']['data'][i]['id'])
				if new == True:
					targets.append(data['data']['nations']['data'][i]['id'])
				if pirate == True:
					if data['data']['nations']['data'][i]['alliance_position'] == 0 or data['data']['nations']['data'][i]['alliance_position'] == 1:
						targets.append(data['data']['nations']['data'][i]['id'])
					
					
		i += 1

	#newtargets = []
	#for i in targets:
		#test = requests.post(f"http://politicsandwar.com/api/nation/id={i}/&key={key}").json()['defensivewars']
		#print(test)
		
		#if test != 3:
			#newtargets.append(i)

	#targets = newtargets.copy()
	if len(targets) == 0:
		await Rchannel.send(
			'Bummer, there are no inactive raid targets currently availible within your war range :('
		)
		print(score)
		return
			
	random.shuffle(targets)
	targets = targets[:round(min((6 + (6 * wars) +
								  (1500 / float(score))), 60))]
	await Rchannel.send(f'Scanning {len(targets)} targets')

			
	for i in targets:
		value = 0
		cities = requests.get(
			f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id:{i},first:1){{data{{soldiers tanks aircraft ships last_active wars{{id}} cities{{barracks factory hangar drydock coalmine oilwell uramine farm leadmine ironmine bauxitemine land}}}}}}}}"""
		).json()
		inactive = cities['data']['nations']['data'][0]['last_active']
		inactive = list(str(inactive))
		inactive = datetime.datetime.strptime(
			str(inactive[5]) + str(inactive[6]) + '/' + str(inactive[8]) +
			str(inactive[9]) + '/' + str(inactive[2]) + str(inactive[3]), '%x')
		inactive = datetime.datetime.now() - inactive
		inactive = (((inactive.total_seconds()) / 60) / 60) / 24

		nation = cities.copy()
		cities = cities['data']['nations']['data'][0]['cities']

		if pirate == True:
			barracks = 0
			factories = 0
			hangars = 0
			drydocks = 0

			x = 0
			while x < len(cities):
				barracks += cities[x]['barracks']
				factories += cities[x]['factory']
				x += 1

			x = 0
			while x < len(cities):
				hangars += cities[x]['hangar']
				x += 1

			x = 0
			while x < len(cities):
				drydocks += cities[x]['drydock']
				x += 1
			
			citycount = len(cities)
			build = [barracks, factories, hangars, drydocks, round(barracks/citycount,1), round(factories/citycount,1), round(hangars/citycount,1), round(drydocks/citycount,1)]

		soldiers = nation['data']['nations']['data'][0]['soldiers']
		tanks = nation['data']['nations']['data'][0]['tanks']
		aircraft = nation['data']['nations']['data'][0]['aircraft']
		ships = nation['data']['nations']['data'][0]['ships']
		if pirate == True:
			count = 0
			for doohicky in build[:5]:
				if doohicky == 0:
					build[count]+=1
				count+=1

			militaryindex = ((soldiers/(build[0]*3000)) + (tanks/(build[1]*250)) + (aircraft/(build[2]*15)) + (ships/(build[3]*5)))/4
													
		i = 0
		while i < len(cities):
			city = cities[i]
			land = int(city['land'])
			if pirate == False:
				value = round(
				value + ((int(city['coalmine']) * prices[2]) +
						 (int(city['oilwell']) * prices[3]) +
						 (int(city['uramine']) * prices[5]) +
						 (int(city['farm']) * prices[0]) +
						 (int(city['leadmine']) * prices[4]) +
						 (int(city['ironmine']) * prices[1]) +
						 (int(city['bauxitemine']) * prices[6])) / 1000, 2)
			else:
				value = round(
				value + (((int(city['coalmine']) * prices[2]) +
						 (int(city['oilwell']) * prices[3]) +
						 (int(city['uramine']) * prices[5]) +
						 (int(city['farm']) * prices[0]) +
						 (int(city['leadmine']) * prices[4]) +
						 (int(city['ironmine']) * prices[1]) +
						 (int(city['bauxitemine']) * prices[6])) / 1000)/militaryindex, 2)
			#value = round((value + ((int(city['coalmine'])*prices[2]*3*inactive/((warcount*1.1494)+1))+(int(city['oilwell'])*prices[3]*3*inactive/((warcount*1.1494)+1))+(int(city['uramine'])*prices[5]*3*inactive/((warcount*1.1494)+1))+(int(city['farm'])*prices[0]*3*inactive*land/((warcount*1.1494)+1))+(int(city['leadmine'])*prices[4]*3*inactive/((warcount*1.1494)+1))+(int(city['ironmine'])*prices[1]*3*inactive/((warcount*1.1494)+1))+(int(city['bauxitemine'])*prices[6]*3*inactive/((warcount*1.1494)+1)))/1000000)*0.14,4)
			i += 1

		values.append(value)

	i = 0
	best = [0, 0, 0, 0, 0, 0]
	target = [0, 0, 0, 0, 0, 0]
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

			i += 1
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
			i += 1
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
			i += 1
			continue
		if test > best[3]:
			target[5] = target[4]
			target[4] = target[3]
			best[5] = best[4]
			best[4] = best[3]

			target[3] = targets[i]
			best[3] = test
			i += 1
			continue
		if test > best[4]:
			target[5] = target[4]
			best[5] = best[4]

			target[4] = targets[i]
			best[4] = test
			i += 1
			continue
		if test > best[5]:
			target[5] = targets[i]
			best[5] = test
			i += 1
		else:
			i += 1

	print(best)
	if wars == 1:
		if DM == False:

			if best[0] == 0:
				await Rchannel.send(
					"Could not find a good enough target to satisfy your request :(\nperhaps your nation score is a bit too high?"
				)
			else:
				await Rchannel.send(
					f'Target aquired:\nhttps://politicsandwar.com/nation/id={target[0]}\nIndex: {best[0]}\n{round(time.perf_counter()-t,1)}s)\n{MSGauthor.mention}')
			return
		else:
			user = await client.fetch_user(recipient)
			try:
				await user.send(
					f'Target aquired:\nhttps://politicsandwar.com/nation/id={target[0]}\nIndex: {best[0]}\n{round(time.perf_counter()-t,1)}s)')
				await Rchannel.send("Complete")
			except Exception:
				await Rchannel.send(
					f"Failed to send because {user} had DMs disabled or something... ¯\_(ツ)_/¯\n{MSGauthor.mention}"
				)
			return
	else:
		if DM == False:
			await Rchannel.send('Targets aquired:')
			i = 0
			while i < wars and best[i] > 0:
				await Rchannel.send(
					f'https://politicsandwar.com/nation/id={target[i]}\nIndex: {best[i]}')
				i += 1
			if i < wars:
				await Rchannel.send(
					"Could not find enough good targets to satisfy your request :(\nperhaps your nation score is a bit too high?"
				)

			await Rchannel.send(
				f'({round(time.perf_counter()-t,1)}s)\n{MSGauthor.mention}'
			)
			return
		else:
			user = await client.fetch_user(recipient)
			try:
				await user.send('Targets aquired:')
				i = 0
				while i < wars and best[i] > 0:
					await user.send(
						f'https://politicsandwar.com/nation/id={target[i]}\nIndex: {best[i]}')
					i += 1

				if i < wars:
					await user.send(
						"Could not find enough good targets to satisfy your request :(\nperhaps your nation score is a bit too high?"
					)
				await user.send(
					f'({round(time.perf_counter()-t,1)}s)\n{MSGauthor.mention}'
				)
				await Rchannel.send("Complete")
			except Exception:
				await Rchannel.send(
					f"Failed to send because {user} had DMs disabled or something... ¯\_(ツ)_/¯\n{MSGauthor.mention}"
				)
			return


async def help(message):
	global Rchannel
	await Rchannel.send(
		"**Commands:**\n`%raid` - finds a singular, inactive, optimal, alliance non-member raid target within your war range. Targets are selected for their high resource count.\n**NOTE:** `%raid` does **not** (yet) take commerce or manufacturing builds into account; *it assumes that all cities are unpowered*.\nAdd a number (2-6) to the end for two or more raid targets (this is faster and more efficent than requesting each target individualy).\nEX: `%raid4`\n`%DM` - same as `%raid` but it DMs you instaid of publicly posting results. `%DM3` is a thing too.\n`%range` - finds your war range.\n`%applicant` - same as `raid` but for applicants (Non top 50 alliance members and still inactive).\n`%new` - you get the drill. Same as `raid` but with no limit on how recently inactive targets are.\n`%slotted nationlink` - bookmarks a target with 3/3 war slots and DMs you when a slot opens up and the nation is not beiged.\nEX: `%slotted https://politicsandwar.com/nation/id=401657`\nRumor has it that there is another, secret command burried in this *raid* bot's *shadowy* depths of *legendary* code."
	)
	return


async def legendary(message):
	global Rchannel
	await Rchannel.send(
		"ThIs wAr iS sPOnSoREd bY **RAID: Shadow Legends**.", delete_after=20)
	time.sleep(3)
	await Rchannel.send(
		"\nShADow LEgeNdS iS a BRanD nEw imMErSiVe RPG tItlE wITh hOUrs oF coNtEnT, anD thRIlLiNg gAMePlaY.",
		delete_after=20)
	time.sleep(2)
	await Rchannel.send(
		"It'S GOt aN AmAziNg sTorYLiNe, aWEsOme 3D GRaPhIcs, gIAnt boSs fIGhTs, PVP baTTlEs, aNd hUnDReDs oF chAmPIoNs yOU cAn CoLlECt aNd cUStOmiZe.",
		delete_after=20)
	time.sleep(4)
	await Rchannel.send(
		f"\nChEcK ouT RAID tODay aNd uSE tHe coDe: {'BORB'} tO gEt 50,000 SiLVer aNd a FREE LeGeNDarY ChAMpIon.",
		delete_after=20)
	time.sleep(9)
	await Rchannel.send("`Downloading RAID: Shadow Legends...`",
							   delete_after=12)
	time.sleep(3)
	await Rchannel.send("`...`", delete_after=12)
	time.sleep(3)
	await Rchannel.send(
		"`Finished.\nYour device is now infected with RAID: Shadow Legends`",
		delete_after=12)
	return


hours = time.perf_counter()

counter  = 0

@client.event
async def on_ready():
	print("Online")
	global prices
	prices = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{tradeprices(first:1){{data{{food iron coal oil lead uranium bauxite}}}}}}""").json()['data']['tradeprices']['data'][0]
	prices = [prices['food'],prices['iron'],prices['coal'],prices['oil'],prices['lead'],prices['uranium'],prices['bauxite']]

check = 0
allert = False

@client.event
async def on_message(message):
	global recipient
	global hours
	global update
	global applicant
	global user
	global name
	global counter
	global check
	global allert
	global nope
	global pirate
	global Rchannel
	nope = db['nope']
	nope = nope.split(', ')

	Rchannel = message.channel
	MSGauthor = message.author
	if MSGauthor == client.user:
		return
	
	timestamp = datetime.datetime.now()
	timestamp = timestamp.strftime("%M")

	if timestamp == "01" or (hours - time.perf_counter()) / 60 / 60 >= 1:
		print('running')
		global prices
		prices = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{tradeprices(first:1){{data{{food iron coal oil lead uranium bauxite}}}}}}""").json()['data']['tradeprices']['data'][0]
		prices = [prices['food'],prices['iron'],prices['coal'],prices['oil'],prices['lead'],prices['uranium'],prices['bauxite']]
		hours = time.perf_counter()
		return
	
	
	slotted = db.keys()
	try:
		slotted.remove('nope')
	except Exception:
		None
	print(nope)
			
	print(slotted)

	applicant = False
	pirate = False

	count = 0
	if len(slotted) > 0 and counter > 20:
		for s in slotted:
			test = requests.post(f"http://politicsandwar.com/api/nation/id={s}/&key={key}").json()
			print(f"{test['defensivewars']} {test['color']}")
			if test['defensivewars'] != 3 and test['color'] != "beige":
				print('Target availible')
				user = await client.fetch_user(db[s])
				print(user)
				await user.send(f'https://politicsandwar.com/nation/id={s}\nNow properly availible with an open war slot.')
				del db[f'{s}']
			count += 1
		counter = 0
	else:
		counter +=1

	content = message.content
	if content.startswith('%') or content.startswith('?'):
		print('')
	else:
		return
	
	if content == ('%range'):
		name = MSGauthor.id
	
		try:
			user = await client.fetch_user(name)
		except Exception:
			return
		
		recipient = name
		try:
			player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
			player = list(str(player))
			del player[:9]
			player = ''.join(player)
			score = requests.get(f"""https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {player}){{data{{score}}}}}}""").json()['data']['nations']['data'][0]['score']
			range = [float(score) * 0.75, float(score) * 1.75]
			await Rchannel.send('Your War range is ' +
								   str(round(range[0], 1)) + ' to ' +
								   str(round(range[1], 1)) + ' nation score')

		except Exception:
			await Rchannel.send(
				f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
			)
			return

		

	if content.startswith('%slotted htt'):
		name = MSGauthor.id
		id = list(message.content)[9:]
		id = id[37:]
		id = ''.join(id)
		
		try:
			test = requests.post(
				f"http://politicsandwar.com/api/nation/id={id}/&key={key}"
			).json()['defensivewars']

		except Exception:
			await Rchannel.send(
				"hmmmmmmmmmmmmmmmmmmmmmm...\n\nThat doesn't seem to be a valid nation link."
			)
		
		db[id] = name

		await Rchannel.send('Success.')
	
	if content == ('%wars'):
		name = MSGauthor.id
		try:
			user = await client.fetch_user(name)
		except Exception:
			return
		
		recipient = name
		
		try:
			player = pnwkit.nation_query({"discord": str(user)}, "id")[0]

		except Exception:
			await Rchannel.send(
				f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
			)
			return

		player = list(str(player))
		del player[:9]
		player = ''.join(player)

		await wars(message,player)

	if content.startswith('%'):
		name = MSGauthor.id
		recipient = name
	
	if content == ('%raid') or message.content == ('%raid1'):
		await raid(message, 1, False)
	if content == ('%raid2'):
		await raid(message, 2, False)
	if content == ('%raid3'):
		await raid(message, 3, False)
	if content == ('%raid4'):
		await raid(message, 4, False)
	if content == ('%raid5'):
		await raid(message, 5, False)
	if content == ('%raid6'):
		await raid(message, 6, False)

	if content == ('%new') or message.content == ('%new1'):
		await raid(message, 1, False)
	if content == ('%new2'):
		await raid(message, 2, False)
	if content == ('%new3'):
		await raid(message, 3, False)
	if content == ('%new4'):
		await raid(message, 4, False)
	if content == ('%new5'):
		await raid(message, 5, False)
	if content == ('%new6'):
		await raid(message, 6, False)

	if content == ('%DM') or message.content == ('DM1'):
		await raid(message, 1, True)
	if content == ('%DM2'):
		await raid(message, 2, True)
	if content == ('%DM3'):
		await raid(message, 3, True)
	if content == ('%DM4'):
		await raid(message, 4, True)
	if content == ('%DM5'):
		await raid(message, 5, True)
	if content == ('%DM6'):
		await raid(message, 6, True)

	if content.startswith('%cata'):
		global cata
		await Rchannel.send(
			'Remember: only nations that are inactive for 10+ days are allowed. All these targets SHOULD be but check just in case.'
		)
		if content == ('%cata'):
			cata = True
			applicant = False
			await raid(message, 1, False)
		else:
			data = message.content
			data = list(data)
			i = int(data[5])
			cata = True
			applicant = False
			await raid(message, i, False)

	if content.startswith('%applicant'):
		await Rchannel.send(
			'**Use discretion** when attacking inactive applicants. ALL targets *are* inactive for more than 30 days and should not be members of alliances who counter, but you should check to make sure, and see if other attackers have not been countered before raiding.'
		)
		if content == ('%applicant'):
			applicant = True
			await raid(message, 1, False)
		else:
			data = message.content
			data = list(data)
			i = int(data[10])
			applicant = True
			await raid(message, i, False)

	if content.startswith('%pirate'):
		await Rchannel.send(
			'https://imgur.com/SmIEua5'
		)
		if content == ('%pirate'):
			pirate = True
			await raid(message, 1, False)
		else:
			data = message.content
			data = list(data)
			i = int(data[7])
			pirate = True
			await raid(message, i, False)
			
	if content.startswith('%sim ground'):
		stats = message.content[12:]
		count = 0
		for i in stats:
			if i == ',':
				att1 = int(str(''.join(stats[0:count])))
				break
			count+=1

		stats = list(stats)
		del stats[0:count+1]
		stats = ''.join(stats)
		
		count = 0
		for i in stats:
			if i == ',':
				att2 = int(str(''.join(stats[0:count])))
				break
			count+=1
		
		stats = list(stats)
		del stats[0:count+1]
		stats = ''.join(stats)
		
		count = 0
		for i in stats:
			if i == ',':
				def1 = int(str(''.join(stats[0:count])))
				break
			count+=1

		stats = list(stats)
		del stats[0:count+1]
		stats = ''.join(stats)
		
		def2 = int(stats)
		await sim(message, 'ground', att1, att2, def1, def2)

	
	if content.startswith('%sim air'):
		stats = message.content[9:]
		
		count = 0
		for i in stats:
			if i == ',':
				att1 = int(str(''.join(stats[0:count])))
				break
			count+=1

		stats = list(stats)
		del stats[0:count+1]
		stats = ''.join(stats)
		
		def1 = int(stats)
		await sim(message, 'air', att1, 0, def1, 0)

	if content.startswith('%sim sea'):
		stats = message.content[9:]
		
		count = 0
		for i in stats:
			if i == ',':
				att1 = int(str(''.join(stats[0:count])))
				break
			count+=1

		stats = list(stats)
		del stats[0:count+1]
		stats = ''.join(stats)
		
		def1 = int(stats)
		await sim(message, 'sea', att1, 0, def1, 0)

	if content.startswith('%hit htt'):
		id = message.content[38:]
		print(id)

	if content.startswith('%nope htt'):
		count = -1
		for i in content:
			count += 1
			if i == '=':
				id = content[count+1:]
				break

		nope.append(id)
		db['nope'] = ', '.join(nope)
		await Rchannel.send('Nope registered!')
		
	if content == ('?raid'):
		await help(message)

	
	if content == ('%raidshadowlegends'):
		await message.delete()
		await legendary(message)


keep_alive()

client.run('OTU1MzQwNTUwNjU4MjExODUy.YjgQOA.CZH1sxDcWUQrAp8j2tVEbNtCh3A')
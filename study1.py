import pandas as pd
import datetime
from nba_api.stats.static import players

all_players = players.get_players()

data = pd.read_csv('injury_data.csv')
for index, item in data.iterrows():
	date = item['Date'].split('-')
	for i, ind in enumerate(date):
		date[i] = int(ind)
	if date[0] >= 1994 and isinstance(item['Injured'], str):
		name = item['Injured'].split(' / ')
		dt = datetime.datetime(date[0], date[1], date[2])
		print(name)
		for spelling in name:
			#Fix special cases
			if 'Jr.' not in spelling:
				spelling = spelling.replace('.', '')
			if 'PJ Washington' in spelling:
				spelling = 'P.J. Washington'
			if 'Michael Frazier II' in spelling:
				spelling = 'Michael Frazier'
			if 'Mike Conley Jr.' in spelling:
				spelling = 'Mike Conley'
			if 'DJ Augustine' in spelling:
				spelling = 'D.J. Augustin'
			for player in all_players:
				if spelling in player['full_name']:
					print(player)
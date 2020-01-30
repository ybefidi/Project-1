import pandas as pd
import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamgamelog
import matplotlib.pyplot as plt

all_players = players.get_players()

years = {}
data = pd.read_csv('injury_data.csv')
gamesDict = {}
for index, item in data.iterrows():
	date = item['Date'].split('-')
	for i, ind in enumerate(date):
		date[i] = int(ind)
	if date[0] >= 2000 and isinstance(item['Injured'], str):
		name = item['Injured'].split(' / ')
		if date[1] >= 10:
			injurySeason = f'{date[0]}-{date[0]+1}'
		else:
			injurySeason = f'{date[0]-1}-{date[0]}'
		if injurySeason in years:
			years[injurySeason] += 1
		else:
			years[injurySeason] = 1
		playerData = ''
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
					if playerData == '':
						playerData = player['id']
		print(playerData)
		playerInfo = playercareerstats.PlayerCareerStats(per_mode36='PerGame', player_id=playerData).season_totals_regular_season.get_data_frame()
		dt = datetime.datetime(date[0], date[1], date[2])
		if len(str(date[2])) == 1:
			hurtDay = '0'+str(date[2])
		else:
			hurtDay = str(date[2])
		if date[1] >= 10:
			seasonDate = f'{date[0]}-{str(date[0]+1)}'.replace('20','')
		else:
			seasonDate = f'{date[0]-1}-{str(date[0])}'.replace('20','')
		playerInfo = playerInfo[playerInfo['SEASON_ID'] == seasonDate]
		try:
			seasonSchedule = teamgamelog.TeamGameLog(season=seasonDate, team_id=playerInfo.iloc[0]['TEAM_ID']).team_game_log.get_data_frame()
			missedGame = seasonSchedule[seasonSchedule['GAME_DATE'] == f'{dt.strftime("%b").upper()} {hurtDay}, {date[0]}']
			#print(missedGame)
			prevGames = []
			for prevDate in range(1, 8):
				prevD = dt-datetime.timedelta(prevDate)
				prevGame = seasonSchedule[seasonSchedule['GAME_DATE'] == f'{prevD.strftime("%b %d, %Y").upper()}']
				try:
					prevGame.iloc[0]['Game_ID']
					prevGames.append(prevGame)
				except:
					pass
			print(len(prevGames))
			if len(prevGames) in gamesDict:
				gamesDict[len(prevGames)] += 1
			else:
				gamesDict[len(prevGames)] = 1
			print(gamesDict)
		except:
			print('ERROR FOUND')
			pass
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams

team = teams.get_teams()
for t in team:

    data = teamgamelog.TeamGameLog(team_id=t['id']).team_game_log.get_data_frame()
    print(data)
    

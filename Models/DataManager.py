import pandas as pd
from PlayerStats import PlayerStats


class DataManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.player_stats = []

    def load_data(self):
        data = pd.read_csv(self.csv_file)
        for _, row in data.iterrows():
            player = PlayerStats(
                rk=row['Rk'],
                player=row['Player'],
                pos=row['Pos'],
                age=row['Age'],
                team=row['Tm'],
                g=row['G'],
                gs=row['GS'],
                mp=row['MP'],
                fg=row['FG'],
                fga=row['FGA'],
                fg_pct=row['FG%'],
                three_p=row['3P'],
                three_pa=row['3PA'],
                three_pct=row['3P%'],
                two_p=row['2P'],
                two_pa=row['2PA'],
                two_pct=row['2P%'],
                efg_pct=row['eFG%'],
                ft=row['FT'],
                fta=row['FTA'],
                ft_pct=row['FT%'],
                orb=row['ORB'],
                drb=row['DRB'],
                trb=row['TRB'],
                ast=row['AST'],
                stl=row['STL'],
                blk=row['BLK'],
                tov=row['TOV'],
                pf=row['PF'],
                pts=row['PTS']
            )
            self.player_stats.append(player)

    # def load_data2(self):
    #     data = pd.read_csv(self.csv_file)
    #     for _, row in data.iterrows():
    #         player = PlayerStats(
    #             rk=1,
    #             # rk=row['Rk'],
    #             player=row['Player'],
    #             pos='C',
    #             # pos=row['Pos'],
    #             age=20,
    #             # age=row['Age'],
    #             team='lol',
    #             # team=row['Tm'],
    #             g=row['G'],
    #             gs=17,
    #             # gs=row['GS'],
    #             mp=20.7,
    #             # mp=row['MP'],
    #             fg=row['FG'],
    #             fga=row['FGA'],
    #             fg_pct=0.1,
    #             # fg_pct=row['FG%'],
    #             three_p=row['3P'],
    #             three_pa=row['3PA'],
    #             three_pct=0.2,
    #             # three_pct=row['3P%'],
    #             two_p=2,
    #             # two_p=row['2P'],
    #             two_pa=8,
    #             # two_pa=row['2PA'],
    #             two_pct=0.5,
    #             # two_pct=row['2P%'],
    #             efg_pct=0.1,
    #             # efg_pct=row['eFG%'],
    #             ft=row['FT'],
    #             fta=row['FTA'],
    #             ft_pct=0.5,
    #             # ft_pct=row['FT%'],
    #             orb=8,
    #             # orb=row['ORB'],
    #             drb=4,
    #             # drb=row['DRB'],
    #             trb=row['TRB'],
    #             ast=row['AST'],
    #             stl=row['STL'],
    #             blk=row['BLK'],
    #             tov=row['TOV'],
    #             pf=6,
    #             # pf=row['PF'],
    #             pts=row['PTS']
    #         )
    #         self.player_stats.append(player)

    def get_player_stats(self):
        return self.player_stats

    def update_player_stats(self, player, **kwargs):
        player.update_stats(**kwargs)

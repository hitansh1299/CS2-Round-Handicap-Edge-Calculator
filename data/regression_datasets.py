import pandas as pd
from data.datasets import BasicDataset
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class RegressionDataset(BasicDataset):
    def __init__(self, db: str, table:str):
        super().__init__(db,table)
        # self.df = self.prepare_data(self.df)
        
    def prepare_data(self, df: pd.DataFrame):      
        #Drop steamid and ticks as they are inconsequential
        steam_id_cols = df.columns[df.columns.str.startswith('steamid')]
        df = df.drop(columns=steam_id_cols)
        df = df.drop(columns='tick')
        

        #Convert team names into Label Encodings.
        team_clan_cols = df.columns[df.columns.str.startswith('team_clan')]
        df[team_clan_cols] = OrdinalEncoder().fit_transform(df[team_clan_cols].values)
        df = df.select_dtypes(include='number')
        return df
    
class BaselineRegressionOverfitDataset(BasicDataset):
    '''
    Keep only rounds where the rounds played is max rounds. 
    '''
    def __init__(self, db, table):
        super().__init__(db, table)
        # self.df = self.prepare_data(self.df)
    
    def _shift_target(self, df: pd.DataFrame):
        df['round_handicap'] = df['round_handicap'] + 13 #Minimum Round handicap
        return df

    def prepare_data(self, df):
        df = df.loc[df.groupby("demo_id")["total_rounds_played"].idxmax()].reset_index(drop=True)
        df = df[['team_rounds_total_player_1','team_rounds_total_player_9','round_handicap']]

        df.to_csv('temp/temp_data.csv', index=False)
        # df = df[df['rounds_played']]
        return df

class TMinusOneFullDataset(BasicDataset):
    '''
    Keep only rounds where the rounds played is max rounds. 
    '''
    def __init__(self, db, table):
        super().__init__(db, table)
    
    def _shift_target(self, df: pd.DataFrame):
        df['round_handicap'] = df['round_handicap'] + 13 #Minimum Round handicap
        return df

    def prepare_data(self, df: pd.DataFrame):
        df = df.loc[df.groupby("demo_id")["total_rounds_played"].idxmax()].reset_index(drop=True)
        df = df.drop(columns=['tick'] + list(df.columns[df.columns.str.startswith('steamid')]))
        df['team_rounds_1'] = df['team_rounds_total_player_1']
        df['team_rounds_2'] = df['team_rounds_total_player_9']

        #Collapse Team Rounds total
        df = df.drop(columns=list(df.columns[df.columns.str.startswith('team_rounds_total_player')]))

        #Rds Played > 12
        df = df[df['total_rounds_played'] > 12]

        # df = df[['team_rounds_total_player_1','team_rounds_total_player_9','round_handicap']]
        df = df.select_dtypes(include='number')
        df.to_csv('temp/temp_data.csv', index=False)
        # df = df[df['rounds_played']]
        return df
    
class TMinusOneFullDatasetStandardised(BasicDataset):
    '''
    Keep only rounds where the rounds played is max rounds. 
    '''
    def __init__(self, db, table):
        super().__init__(db, table)
        self.scaler = StandardScaler()

    
    def _shift_target(self, df: pd.DataFrame):
        df['round_handicap'] = df['round_handicap'] + 13 #Minimum Round handicap
        return df

    def prepare_data(self, df: pd.DataFrame):
        df = df.loc[df.groupby("demo_id")["total_rounds_played"].idxmax()].reset_index(drop=True)
        df = df.drop(columns=['tick'] + list(df.columns[df.columns.str.startswith('steamid')]))
        df['team_rounds_1'] = df['team_rounds_total_player_1']
        df['team_rounds_2'] = df['team_rounds_total_player_9']

        #Collapse Team Rounds total
        df = df.drop(columns=list(df.columns[df.columns.str.startswith('team_rounds_total_player')]))

        #Rds Played > 12
        df = df[df['total_rounds_played'] > 12]

        df = df.select_dtypes(include='number')
        df.to_csv('temp/temp_data.csv', index=False)
        return df
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder
import torch
import pandas as pd
from data.datasets import BasicDataset


class ClassificationDataset(BasicDataset):
    def __init__(self, db: str, table:str):
        super().__init__(db,table)
        self.df = self.prepare_data(self.df)
    
    def _one_hot_encode_target(self, df: pd.DataFrame):
        rounds_played = list(range(-13,14))
        target_col = 'round_handicap'
        ohe = OneHotEncoder(categories=[rounds_played], sparse_output=False)
        x = df[[target_col]]
        one_hot = ohe.fit_transform(x)
        one_hot = pd.DataFrame(one_hot, columns=[f"{target_col}_{i}" for i in rounds_played])
        df = df.drop(target_col, axis=1)
        # print(df)
        df = pd.concat([df, one_hot], axis=1)
        return df
        
    def prepare_data(self, df: pd.DataFrame):      
        #Drop steamid and ticks as they are inconsequential
        steam_id_cols = df.columns[df.columns.str.startswith('steamid')]
        df = df.drop(columns=steam_id_cols)
        df = df.drop(columns='tick')
        

        #Convert team names into Label Encodings.
        team_clan_cols = df.columns[df.columns.str.startswith('team_clan')]
        df[team_clan_cols] = OrdinalEncoder().fit_transform(df[team_clan_cols].values)
        df = df.select_dtypes(include='number')
        
        #Convert round handicap to One Hot Encodings.
        # one_hot = pd.get_dummies(df[column], prefix=column, dtype=float)
        # df = self._one_hot_encode_target(df)
        return df
    
class BaselineClassificationOverfitDataset(ClassificationDataset):
    '''
    Keep only rounds where the rounds played is max rounds. 
    '''
    def __init__(self, db, table):
        super().__init__(db, table)
    
    def _shift_target(self, df: pd.DataFrame):
        df['round_handicap'] = df['round_handicap'] + 13 #Minimum Round handicap
        return df

    def prepare_data(self, df):
        df = df.loc[df.groupby("demo_id")["total_rounds_played"].idxmax()].reset_index(drop=True)
        df = df[['team_rounds_total_player_1','team_rounds_total_player_9','round_handicap']]
        # df = super().prepare_data(df)
        df = self._one_hot_encode_target(df)
        # df = self._shift_target(df)

        df.to_csv('temp/temp_data.csv', index=False)
        # df = df[df['rounds_played']]
        return df
    
if __name__ == "__main__":
    # BaselineTminus1RoundDataModule(db = "data\\master_database.db", table="match_data")
    dataset = BaselineClassificationOverfitDataset(db = "data\\master_database.db", table="match_data")
    # dataset = BaselineDataset(db = "data\\master_database.db", table="match_data")
    for i in dataset[0:10]:
        print(i)

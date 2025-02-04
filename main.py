from demoparser2 import DemoParser
import pandas as pd
from scrape_hltv import get_matches_from_event

COLUMNS = ["current_equip_value", 
                            "total_rounds_played",
                            "kills_total",
                            "deaths_total",
                            "assists_total",
                            "damage_total",
                            "team_rounds_total",
                            "team_clan_name",
                            "balance"]

def extract_gamedata(demofile: str):
    parser = DemoParser(demofile)
    wanted_ticks = parser.parse_event("round_freeze_end")["tick"].tolist()
    df = parser.parse_ticks(COLUMNS, ticks=wanted_ticks)
    return df

def parse_demo(demofile: str):
    df = extract_gamedata(demofile=demofile)
    formatted_df = format_gamedata(df)
    formatted_df.to_csv('formatted_data')
    return formatted_df

def format_gamedata(df: pd.DataFrame | str):
    if type(df) is str:
        df = pd.read_csv(df)
    suffix_list = [f"player_{i}" for i in range(1,11)]
    df['player_name'] = df['name'].replace(dict(zip(list(df['name'].unique()),suffix_list)))
    # df = df[['name','balance','kills_total','team_clan_name']]
    df = df.pivot(index=['tick','total_rounds_played'], columns=['player_name'])
    df.columns = ['_'.join(col) for col in df.columns.values]
    return df



if __name__ == '__main__':
    print('Parsing CSGO demos')
    get_matches_from_event(8229)
    # parse_demo("demos\\iem-katowice-2025-vitality-vs-3dmax-bo3-KNzbDELEQ75v8nvhNNs8tI\\vitality-vs-3dmax-m1-inferno.dem")
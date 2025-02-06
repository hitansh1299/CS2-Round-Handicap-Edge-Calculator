from demoparser2 import DemoParser
import pandas as pd
import sqlite3
import logging_utils
import logging

logger = logging.getLogger(__name__)
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


def parse_demo(demofile: str, save_csv: bool=False, db: str = None, table:str = None):
    """
    Parses a demo file, formats the game data, and optionally saves it to a CSV file or a database.
    
    Parameters:
    ----------
    demofile (str): The path to the demo file to be parsed.
    
    save_csv (bool, optional): If True, saves the formatted data to a CSV file. Defaults to False.
    
    db (str, optional): The path to the SQLite database file. If provided, the formatted data will be saved to this database. Defaults to None.
    
    table (str, optional): The name of the table in the database where the data will be saved. Required if `db` is provided. Defaults to None.

    Returns:
    ----------
    pandas.DataFrame: The formatted game data with an additional 'demo_id' column.
    """
    logger.info(f'Parsing CS2 Demo {demofile}')
    logger.debug('Extracting Gamedata')
    df = extract_gamedata(demofile=demofile)
    logger.debug('Formatting gamedata')
    formatted_df = format_gamedata(df)
    formatted_df['demo_id'] = '/'.join(demofile.rsplit('\\', 2)[1:])
    
    logger.debug('Successfully extracted gamedata')
    if save_csv:
        logger.debug('Saving as csv...')
        formatted_df.to_csv(demofile.rsplit('.', 1)[0] + '.csv')

    if db:
        logger.debug(f'Adding to DB {db} | table: {table}')
        add_map_to_db(formatted_df, db, table)
    
    logger.info(f'Parsing complete for {demofile}')
    return formatted_df

def add_map_to_db(df: pd.DataFrame, con: str = None, table:str = None):
    if type(con) is str:
        con = sqlite3.connect(con)
    df.to_sql(name=table, con=con, if_exists='append')
    
def format_gamedata(df: pd.DataFrame | str):
    if type(df) is str:
        df = pd.read_csv(df)

    #Sort by tick, team name and player name to ensure consistency of column placements
    #This ensures, player 1-5 are from one team and players 5-10 are from other team
    df = df.sort_values(by=['tick','team_clan_name','name'])


    #Replace player names such as ZywOo, s1mple to player1, player2 for consistency in col headers
    suffix_list = [f"player_{i}" for i in range(0,10)]
    df['player_name'] = df['name'].replace(dict(zip(list(df['name'].unique()),suffix_list)))

    # df = df[['name','balance','kills_total','team_clan_name']]
    df = df.pivot(index=['tick','total_rounds_played'], columns=['player_name'])

    df.columns = ['_'.join(col) for col in df.columns.values]
    logger.debug('Calculating Round Handicap')
    df['round_handicap'] = df.loc[df.last_valid_index()]['team_rounds_total_player_0'] - \
                            df.loc[df.last_valid_index()]['team_rounds_total_player_9']

    return df

import glob
def parse_all_demos(demo_dir: str):
    demos = glob.glob(f'{demo_dir}/*/*.dem', recursive=True)
    for demo in demos:
        parse_demo(demo,
                    save_csv=True,
                    table='match_data',
                    db = r'data\master_database.db')
    # print(demos)


if __name__ == '__main__':
    print('Parsing CSGO demos')
    # parse_demo('demos\\iem-katowice-2025-play-in-big-vs-heroic-bo3-KvlmFiXJQmR2f_ILlW2f-R\\big-vs-heroic-m1-nuke.dem',
    #            save_csv=True,
    #            table='match_data'
    #         #    db = r'data\master_database.db'
    #            )
    parse_all_demos('demos')